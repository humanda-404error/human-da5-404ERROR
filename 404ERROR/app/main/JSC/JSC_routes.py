from flask import Flask, Blueprint, render_template, session, redirect, url_for, request, jsonify
from xml.etree import ElementTree as ET
import os
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
from svgpathtools import parse_path
# from svgpathtools import Path as svg_path
from .JSC_analyze_logic import (
    plot_date_transport_ratio,
    generate_female_gu_chart,
    generate_female_age_chart,
    generate_male_gu_chart,
    generate_male_age_chart
)
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'  # 윈도우
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'    # 맥
else:
    plt.rcParams['font.family'] = 'NanumGothic'    # 리눅스나 Colab 같은 환경

# 마이너스 깨짐 방지
plt.rcParams['axes.unicode_minus'] = False

def register_JSC_routes(main_bp):
    @main_bp.route("/dashboard")
    def dashboard():
        svg_input_path = os.path.join(os.path.dirname(__file__), "../../static/img", "Seoul_districts.svg")
        svg_output_path = os.path.join(os.path.dirname(__file__), "../../static/img", "Seoul_districts_labeled.svg")

        # # 자치구 이름 리스트 (SVG path id 순서와 일치해야 함)
        # district_names = [
        #     "강남구", "강동구", "강북구", "강서구", "관악구", "광진구", "구로구", "금천구", "노원구",
        #     "도봉구", "동대문구", "동작구", "마포구", "서대문구", "서초구", "성동구", "성북구", "송파구",
        #     "양천구", "영등포구", "용산구", "은평구", "종로구", "중구", "중랑구"
        # ]

        # # SVG 파싱
        # tree = ET.parse(svg_input_path)
        # root = tree.getroot()

        # ET.register_namespace("", "http://www.w3.org/2000/svg")

        # ns = {"svg": "http://www.w3.org/2000/svg"}
        # paths = root.findall(".//svg:path", ns)

        # for i, path in enumerate(paths):
        #     if i >= len(district_names):
        #         break
        #     gu_name = district_names[i]
        #     d_attr = path.attrib.get("d", "")

        #     # 중심 좌표 추정 (단순히 첫 M 좌표 사용)
        #     try:
        #         parts = d_attr.split()
        #         m_index = parts.index("M") if "M" in parts else 0
        #         x = float(parts[m_index + 1])
        #         y = float(parts[m_index + 2])

        #         text_el = ET.Element("{http://www.w3.org/2000/svg}text", {
        #             "x": str(x),
        #             "y": str(y),
        #             "font-size": "10",
        #             "fill": "black",
        #             "text-anchor": "middle",
        #             "font-family": "Arial"
        #         })
        #         text_el.text = gu_name
        #         root.append(text_el)
        #     except Exception as e:
        #         print(f"Error processing path {i}: {e}")

        # tree.write(svg_output_path, encoding="utf-8", xml_declaration=True)

        # # HTML에서 삽입할 SVG 문자열 읽기
        # with open(svg_output_path, "r", encoding="utf-8") as f:
        #     svg = f.read()

        # return render_template("JSC/dashboard.html", svg=svg)
        # # return render_template("JSC/dashboard.html")

        # 자치구 이름 리스트 (SVG path id 순서와 일치해야 함)
        # district_names = [
        #     "도봉구", "동대문구", "동작구", "은평구", "강북구", "강동구", "강서구", "금천구", "구로구",
        #     "관악구", "광진구", "강남구", "종로구", "중구", "중량구", "마포구", "노원구", "서초구",
        #     "서대문구", "성북구", "성동구", "송파구", "양천구", "영등포구", "용산구"
        # ]

        # # SVG 파싱
        # tree = ET.parse(svg_input_path)
        # root = tree.getroot()

        # ET.register_namespace("", "http://www.w3.org/2000/svg")

        # ns = {"svg": "http://www.w3.org/2000/svg"}
        # paths = root.findall(".//svg:path", ns)

        # for i, path in enumerate(paths):
        #     if i >= len(district_names):
        #         break
        #     gu_name = district_names[i]
        #     d_attr = path.attrib.get("d", "")

        #     # 중심 좌표 추정 (단순히 첫 M 좌표 사용)
        #     try:
        #         path = parse_path(d_attr)
        #         xmin, xmax, ymin, ymax = path.bbox()

        #         center_x = (xmin + xmax) / 2
        #         center_y = (ymin + ymax) / 2

        #         text_el = ET.Element("{http://www.w3.org/2000/svg}text", {
        #             "x": str(center_x),
        #             "y": str(center_y),
        #             "font-size": "larger",
        #             "fill": "black",
        #             "text-anchor": "middle",
        #             "font-family": "Arial"
        #         })
        #         text_el.text = gu_name
        #         root.append(text_el)
        #     except Exception as e:
        #         print(f"Error processing path {i}: {e}")

        # tree.write(svg_output_path, encoding="utf-8", xml_declaration=True)

        # # HTML에서 삽입할 SVG 문자열 읽기
        # with open(svg_output_path, "r", encoding="utf-8") as f:
        #     svg = f.read()

        # return render_template("JSC/dashboard.html", svg=svg)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

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
