from flask import Blueprint, render_template, session, redirect, url_for, request, send_file
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import platform
import io
import base64
from datetime import datetime
import requests
from xml.etree import ElementTree
from scipy.stats import ttest_ind
import seaborn as sns
from werkzeug.security import generate_password_hash

all_holidays = None

# 공휴일 가져오기
def get_holidays_from_api(year):
    api_key = "2wHgjlBWqAWdWRSOb6tUatjRQcROFAbFWlBPEkXmw4unB0cTUN5fXZ+9o8VMNZSruA52pRecVbaI8ljyHUqy7Q=="
    url = "http://apis.data.go.kr/B090041/openapi/service/SpcdeInfoService/getRestDeInfo"
    params = {
        'serviceKey': api_key,
        'numOfRows': 1000,  # 한 페이지에 1000개의 공휴일 정보
        'pageNo': 1,  # 첫 번째 페이지
        'solYear': year,  # 공휴일을 가져올 연도
        'solMonth': "",  # 월을 지정하지 않으면 전체 연도 데이터를 가져옴
    }
    response = requests.get(url, params=params)
    if response.status_code !=200:
        return print("공휴일 Open API 오류")
    
    root = ElementTree.fromstring(response.text)
    holidays = []
    for item in root.findall('.//item'):
        date = pd.to_datetime(item.find('locdate').text)
        holidays.append({'일시': date.strftime('%Y-%m-%d'), '공휴일': item.find('dateName').text})
    
    return pd.DataFrame(holidays)

def get_gu_list():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT 자치구 FROM bus ORDER BY 자치구")
    result = cursor.fetchall()
    conn.close()

    gu_list = [row[0] for row in result]
    return gu_list

##########################################

def register_LHK_routes(main_bp):
    @main_bp.route('/weather', methods = ['GET', 'POST'])
    def weather():

        global all_holidays

        gu_list = None
        plot_img = None
        selected_gu = None

        # 공휴일 수집
        if all_holidays is None:
            print("공휴일 수집")
            all_holidays = pd.concat([get_holidays_from_api(y) for y in range(2020, 2025)], ignore_index=True)
            # print("✅ all_holidays.head():", all_holidays.head())
            # print("📦 컬럼:", all_holidays.columns)

        # 구 목록 만들어 넘겨주기
        if not gu_list:
            gu_list = get_gu_list()

        if request.method == 'GET':
            return render_template('LHK/weather.html', gu_list = gu_list)

        elif request.method == 'POST':
            set_gu = request.form['gu']

            # DB 함수 호출을 통한 DB 사용 준비
            conn = get_db_connection()

            # DB에서 필요한 데이터만 쿼리 (자치구 필터 포함)
            bus = pd.read_sql(f"SELECT * FROM bus WHERE 자치구 = '{set_gu}'", conn)
            train = pd.read_sql(f"SELECT * FROM train WHERE 자치구 = '{set_gu}'", conn)
            weather = pd.read_sql(f"SELECT * FROM weather", conn)

            conn.close()

            # 날짜 포맷 맞추기
            weather['일시'] = pd.to_datetime(weather['일시']).dt.strftime('%Y%m%d')
            all_holidays['일시'] = pd.to_datetime(all_holidays['일시']).dt.strftime('%Y%m%d')

            # 병합
            merged = pd.merge(bus, train, on=['일시', '자치구'], suffixes=('_버스', '_지하철'))
            merged = pd.merge(merged, weather, on='일시', how='left')
            merged = pd.merge(merged, all_holidays, on='일시', how='left')

            # 요일 계산
            merged['요일'] = pd.to_datetime(merged['일시'], format="%Y%m%d").dt.dayofweek

            # 주말 여부
            merged['주말여부'] = merged.apply(
                lambda row: 1 if row['요일'] >= 5 or pd.notna(row['공휴일']) else 0,
                axis = 1
            )

            # 그룹 분리 (1: 주말, 0: 평일)
            weekend = merged[merged['주말여부'] == 1]
            weekday = merged[merged['주말여부'] == 0]

            # 비 여부 분리
            group = lambda weather: {
                'rain': weather[weather['일강수량'] > 0],
                'no_rain': weather[weather['일강수량'] == 0]
            }
            wkd = group(weekday)
            wknd = group(weekend)

            # 평균 승차량 계산
            def mean_boarding(df, mode):
                return df[f'승차총승객수_{mode}'].mean()
            
            # 평균 하차량 계산
            def mean_alighting(df, mode):
                return df[f'하차총승객수_{mode}'].mean()
            
            # 변화율 계산
            def calc_diff(before, after):
                return [(after[i] - before[i]) / (after[i] + before[i]) for i in range(len(before))]
            
            # 절대값 계산
            def calc_absolute_diff(before, after):
                return [abs(after[i] - before[i]) for i in range(len(before))]

            # 각각 계산
            bus_boarding_no_rain = [mean_boarding(wknd['no_rain'], '버스'), mean_boarding(wkd['no_rain'], '버스')]
            bus_boarding_rain = [mean_boarding(wknd['rain'], '버스'), mean_boarding(wkd['rain'], '버스')]

            bus_alighting_no_rain = [mean_alighting(wknd['no_rain'], '버스'), mean_alighting(wkd['no_rain'], '버스')]
            bus_alighting_rain = [mean_alighting(wknd['rain'],'버스'), mean_alighting(wkd['rain'], '버스')]

            subway_boarding_no_rain = [mean_boarding(wknd['no_rain'], '지하철'), mean_boarding(wkd['no_rain'], '지하철')]
            subway_boarding_rain = [mean_boarding(wknd['rain'], '지하철'), mean_boarding(wkd['rain'], '지하철')]

            subway_alighting_no_rain = [mean_alighting(wknd['no_rain'], '지하철'), mean_alighting(wkd['no_rain'], '지하철')]
            subway_alighting_rain = [mean_alighting(wknd['rain'],'지하철'), mean_alighting(wkd['rain'], '지하철')]

            # 변화율 계산
            bus_boarding_diff = calc_diff(bus_boarding_no_rain, bus_boarding_rain)
            bus_alighting_diff = calc_diff(bus_alighting_no_rain, bus_alighting_rain)
            subway_boarding_diff = calc_diff(subway_boarding_no_rain, subway_boarding_rain)
            subway_alighting_diff = calc_diff(subway_alighting_no_rain, subway_alighting_rain)

            # 절대값 계산
            bus_boarding_abs_diff = calc_absolute_diff(bus_boarding_no_rain, bus_boarding_rain)
            bus_alighting_abs_diff = calc_absolute_diff(bus_alighting_no_rain, bus_alighting_rain)
            subway_boarding_abs_diff = calc_absolute_diff(subway_boarding_no_rain, subway_boarding_rain)
            subway_alighting_abs_diff = calc_absolute_diff(subway_alighting_no_rain, subway_alighting_rain)

            # T-test 버스 승차
            t_stat_bus_boarding, p_val_bus_boarding = ttest_ind(
                wknd['rain']['승차총승객수_버스'].dropna(),
                wknd['no_rain']['승차총승객수_버스'].dropna(),
                equal_var = False
            )

            # T-test 버스 하차
            t_stat_bus_alighting, p_val_bus_alighting = ttest_ind(
                wknd['rain']['하차총승객수_버스'].dropna(),
                wknd['no_rain']['하차총승객수_버스'].dropna(),
                equal_var = False
            )

            # T-test 지하철 승차
            t_stat_subway_boarding, p_val_subway_boarding = ttest_ind(
                wknd['rain']['승차총승객수_지하철'].dropna(),
                wknd['no_rain']['승차총승객수_지하철'].dropna(),
                equal_var = False
            )

            # T-test 지하철 하차
            t_stat_subway_alighting, p_val_subway_alighting = ttest_ind(
                wknd['rain']['하차총승객수_지하철'].dropna(),
                wknd['no_rain']['하차총승객수_지하철'].dropna(),
                equal_var = False
            )

            p_values = {
                'bus_boarding' : round(p_val_bus_boarding, 4),
                'bus_alighting' : round(p_val_bus_alighting, 4),
                'subway_boarding' : round(p_val_subway_boarding, 4),
                'subway_alighting' : round(p_val_subway_alighting, 4)
            }

            ####### 시각화 ######
            plt.rcParams['font.family'] = 'Malgun Gothic'
            plt.rcParams['axes.unicode_minus'] = False
            fig, ax = plt.subplots(2, 2, figsize=(9,7))
            x = range(2)

            diffs = (
                bus_boarding_diff +
                bus_alighting_diff +
                subway_boarding_diff +
                subway_alighting_diff
            )
            y_min = min(diffs)
            y_max = max(diffs)

            if y_max <= 0:
                y_max = 0.001 # 양수 여유 공간을 추가
            
            y_min -= 0.002
            y_max += 0.002

            for v in diffs:
                print(type(v), v)

            # 버스 - 승차
            ax[0,0].bar(x, bus_boarding_diff, color='royalblue')
            ax[0,0].set_title('버스 승차 이용량 변화율')
            ax[0,0].axhline(0, color='gray', linestyle='--')
            ax[0,0].set_xticks(x)
            ax[0,0].set_xticklabels([f'주말 ({bus_boarding_abs_diff[0]:,.0f}명)', f'평일 ({bus_boarding_abs_diff[1]:,.0f}명)'])
            ax[0,0].set_ylim(y_min, y_max)

            # 버스 - 하차
            ax[0,1].bar(x, bus_alighting_diff, color='cornflowerblue')
            ax[0,1].set_title('버스 하차 이용량 변화율')
            ax[0,1].axhline(0, color='gray', linestyle='--')
            ax[0,1].set_xticks(x)
            ax[0,1].set_xticklabels([f'주말 ({bus_alighting_abs_diff[0]:,.0f}명)', f'평일 ({bus_alighting_abs_diff[1]:,.0f}명)'])
            ax[0,1].set_ylim(y_min, y_max)

            # 지하철 - 승차
            ax[1,0].bar(x, subway_boarding_diff, color='salmon')
            ax[1,0].set_title('지하철 승차 이용량 변화율')
            ax[1,0].axhline(0, color='gray', linestyle='--')
            ax[1,0].set_xticks(x)
            ax[1,0].set_xticklabels([f'주말 ({subway_boarding_abs_diff[0]:,.0f}명)', f'평일 ({subway_boarding_abs_diff[1]:,.0f}명)'])
            ax[1,0].set_ylim(y_min, y_max)

            # 지하철 - 하차
            ax[1,1].bar(x, subway_alighting_diff, color='lightcoral')
            ax[1,1].set_title('지하철 하차 이용량 변화율')
            ax[1,1].axhline(0, color='gray', linestyle='--')
            ax[1,1].set_xticks(x)
            ax[1,1].set_xticklabels([f'주말 ({subway_alighting_abs_diff[0]:,.0f}명)', f'평일 ({subway_alighting_abs_diff[1]:,.0f}명)'])
            ax[1,1].set_ylim(y_min, y_max)

            plt.suptitle(f'{set_gu} - 비 오는 날 대중교통 승하차 감소율', fontsize = 16)
            plt.tight_layout()

            buf = io.BytesIO()
            plt.tight_layout()
            plt.savefig(buf, format = 'png')
            buf.seek(0)

            plot_img = base64.b64encode(buf.getvalue()).decode('utf-8')
            buf.close()

            return render_template('LHK/weather.html', plot_img=plot_img, selected_gu=set_gu, gu_list = gu_list, p_values=p_values)
    
    @main_bp.route('/profile_edit')
    def profile_edit():
        return render_template('LHK/profile_edit.html')
    
    @main_bp.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == "POST":
            email = request.form['email']
            password = request.form['password']
            confirm = request.form['confirm']
            nickname = request.form['nickname']

            if '@' not in email:
                return render_template('LHK/signup.html', error="올바른 이메일 형식을 입력해주세요.")
            if password != confirm:
                return render_template('LHK/signup.html', error="비밀번호가 일치하지 않습니다.")
            
            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM members WHERE email = %s", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                cursor.close()
                conn.close()
                return render_template('LHK/signup.html', error="이미 등록된 이메일입니다.")
            
            hashed_pw = generate_password_hash(password)
            cursor.execute("""
                           INSERT INTO members (email, password, nickname, grade, points, can_message)
                           VALUES (%s, %s, %s, %s, %s, %s)
                           """, (email, hashed_pw, nickname, '일반', 0, 1))
            conn.commit()

            cursor.close()
            conn.close()

            return redirect(url_for('auth.login')) # 회원가입 후 로그인 페이지로 이동
        return render_template('LHK/signup.html')
    
    @main_bp.route('/main')
    def forcing_main():
        return render_template('common/main.html')
    #@...
    