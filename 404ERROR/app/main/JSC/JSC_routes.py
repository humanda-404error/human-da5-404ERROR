from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, jsonify, make_response
from xml.etree import ElementTree as ET
import os
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
from pathlib import Path
import json
import base64
from svgpathtools import parse_path
import plotly.graph_objs as go
import platform
import datetime
from .JSC_analyze_logic import (
    plot_date_transport_ratio,
    generate_female_gu_chart,
    generate_female_age_chart,
    generate_male_gu_chart,
    generate_male_age_chart
)
import platform
from bs4 import BeautifulSoup
import os

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'    # 맥
else:
    plt.rcParams['font.family'] = 'NanumGothic'    # 리눅스나 Colab 같은 환경

gu_names = [
    "도봉구", "동대문구", "동작구", "은평구", "강북구", "강동구", "강서구", "금천구", "구로구",
    "관악구", "광진구", "강남구", "종로구", "중구", "중랑구", "마포구", "노원구", "서초구",
    "서대문구", "성북구", "성동구", "송파구", "양천구", "영등포구", "용산구"
]

# 정확한 절대 경로 사용

bp_path = main_bp.root_path
app_path = Path(bp_path).parent
svg_input_path = os.path.join(app_path,'static', 'img', 'seoul_map.svg')
svg_output_path = os.path.join(app_path, 'static', 'img', 'seoul_map_with_data_gu.svg')

# 파일 읽기
try:
    with open(svg_input_path, 'r', encoding='utf-8') as file:
        svg_content = file.read()
except FileNotFoundError:
    print(f"[ERROR] 파일을 찾을 수 없습니다: {svg_input_path}")
    raise

# BeautifulSoup을 사용하여 SVG 파싱
soup = BeautifulSoup(svg_content, 'xml')
paths = soup.find_all('path')

# 각 path에 data-gu 속성 추가
for path, gu_name in zip(paths, gu_names):
    path['data-gu'] = gu_name

# 수정된 SVG 저장
with open(svg_output_path, 'w', encoding='utf-8') as file:
    file.write(str(soup))

print(f"[INFO] 수정된 SVG 저장 완료: {svg_output_path}")

# 마이너스 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False
def register_JSC_routes(main_bp):
    @main_bp.route("/dashboard")
    def dashboard():
        default_date = "2024-12-31"

        gu_names = [
        "도봉구", "동대문구", "동작구", "은평구", "강북구", "강동구", "강서구", "금천구", "구로구",
        "관악구", "광진구", "강남구", "종로구", "중구", "중랑구", "마포구", "노원구", "서초구",
        "서대문구", "성북구", "성동구", "송파구", "양천구", "영등포구", "용산구"
    ]
        
        # 여기서 svg는 사전에 파싱해 놓은 지도 SVG 문자열
        with open(os.path.join(app_path, "static", "img", "seoul_map_with_data_gu.svg"), "r", encoding="utf-8") as f:
            svg = f.read()
        
        return render_template("JSC/dashboard.html", svg=svg, default_date=default_date, gu_list=gu_names)



    # 자치구 + 날짜에 따른 데이터 반환
@main_bp.route("/district-info/<gu_name>")
def district_info(gu_name):
    selected_date = request.args.get('date')  # "YYYY-MM-DD"

    if not selected_date:
        return jsonify({"error": "날짜가 필요합니다"}), 400

    try:
        bp_path = main_bp.root_path
        app_path = Path(bp_path).parent
        csv_path = os.path.join(app_path,'main','JSC', 'merged_data.csv')
        df = pd.read_csv(csv_path, parse_dates=["일시"])
    except Exception as e:
        return jsonify({"error": f"데이터 로드 실패: {str(e)}"}), 500

    # 날짜, 자치구 필터링
    filtered_df = df[(df['일시'] == selected_date) & (df['자치구'] == gu_name)]

    if filtered_df.empty:
        return jsonify({"error": "해당 날짜와 자치구에 대한 데이터가 없습니다."}), 404

    total_subway = filtered_df['지하철_승차총승객수'].sum()
    total_bus = filtered_df['버스_승차총승객수'].sum()

    # fig = go.Figure()
    # fig.add_trace(go.Bar(
    #     x=["지하철", "버스"],
    #     y=[total_subway, total_bus],
    #     marker_color=["#1f77b4", "#2ca02c"]
    # ))
    # fig.update_layout(
    #     title=f"{selected_date} {gu_name} 교통 이용량",
    #     yaxis_title="승차 총승객수"
    # )

    summary = f"{selected_date} 기준 {gu_name}의 지하철 이용객 수는 {int(total_subway):,}명, 버스는 {int(total_bus):,}명입니다."
    json_result = json.dumps({
        "name": str(gu_name),
        "summary": str(summary),
        "plot_data": { "x" : ["지하철", "버스"], "y": [int(total_subway), int(total_bus)] }
    }, ensure_ascii=False)
    return make_response(json_result)

#############################################################################
@main_bp.route('/district', methods=['GET', 'POST'])
def district():
    graphs = {}
    selected_date = None

    # CSV 경로 (같은 폴더 기준)
    csv_path = os.path.join(os.path.dirname(__file__), "merged_data.csv")

    # 데이터 로드 및 전처리
    df = pd.read_csv(csv_path)
    df["일시"] = pd.to_datetime(df["일시"])
    df["일자"] = df["일시"].dt.date

    if request.method == 'POST':
        selected_date = request.form.get('selected_date')

        # 그래프 1: 날짜별 자치구 대중교통 이용 비율
        fig1 = plot_date_transport_ratio(df, selected_date)
        graphs["date_graph"] = fig_to_base64(fig1)

        # 그래프 2~5: 성별 및 연령별 분석
        graphs["female_ratio_gu"] = fig_to_base64(generate_female_gu_chart(df))
        graphs["female_age"] = fig_to_base64(generate_female_age_chart(df))
        graphs["male_ratio_gu"] = fig_to_base64(generate_male_gu_chart(df))
        graphs["male_age"] = fig_to_base64(generate_male_age_chart(df))

    return render_template("JSC/district.html", graphs=graphs, selected_date=selected_date)

def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")
    buf.seek(0)
    return base64.b64encode(buf.read()).decode("utf-8")