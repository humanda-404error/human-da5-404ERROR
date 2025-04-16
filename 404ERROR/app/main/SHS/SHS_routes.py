from flask import Blueprint, render_template, session, redirect, url_for
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train

import pandas as pd

def register_SHS_routes(main_bp):
    #-직접적(대중교통+인구)
    #코로나19 전후 교통 및 유동인구 변화 분석 (2020년 기준)
    #분석 예시: 연령대별 생활 인구 감소율 비교
    #활용 예시: 비상상황 시 교통 이용률 변화 예측을 통한 대응 계획 수립, 상권 변화 분석 등
    @main_bp.route('/compare')
    def compare():
        conn = get_db_connection()
        # 1. DB → Pandas
        train_df = pd.read_sql("SELECT * FROM train", conn)
        pop_df = pd.read_sql("SELECT * FROM population", conn)
        weather_df = pd.read_sql("SELECT * FROM weather", conn)

        #data debug#
        print("\ntrain_df shape:", train_df.shape)
        print("\npop_df shape:", pop_df.shape)
        print("\nweather_df shape:", weather_df.shape)

        # 2. 전처리 및 시기 구분
        for df in [train_df, pop_df, weather_df]:
            df['일시'] = pd.to_datetime(df['일시'])
        train_df['총이용자수'] = train_df['승차총승객수'] + train_df['하차총승객수']
        pop_df = pop_df[pop_df['시간대구분'] == '12'][['일시', '자치구', '총생활인구수']]

        def classify_period(date):
            if date < pd.Timestamp('2021-01-01'):
                return '전개기'
            elif date < pd.Timestamp('2022-07-01'):
                return '절정기'
            elif date < pd.Timestamp('2024-01-01'):
                return '종식기'
            else:
                return '기타'

        for df in [train_df, pop_df, weather_df]:
            df['시기'] = df['일시'].apply(classify_period)

        #data debug#
        print("▶ train_df 시기별 분포:\n", train_df['시기'].value_counts())
        print("▶ pop_df 시기별 분포:\n", pop_df['시기'].value_counts())
        print("▶ weather_df 시기별 분포:\n", weather_df['시기'].value_counts())



        # 3. 병합 및 분석
        merged = pd.merge(train_df, pop_df, on=['일시', '자치구', '시기'], how='inner')
        merged = pd.merge(merged, weather_df, on=['일시', '시기'], how='left')
        agg_df = merged.groupby(['시기', '자치구']).agg({
            '총이용자수': 'mean',
            '총생활인구수': 'mean',
            '평균기온': 'mean',
            '일강수량': 'mean'
        }).reset_index()


        #data debug#
        print("▶ merged shape:", merged.shape)
        print("▶ merged 샘플:\n", merged[['일시', '자치구', '총이용자수', '총생활인구수', '시기']].head())
        print("▶ merged 시기 분포:\n", merged['시기'].value_counts())

        # 4. 통계검정 (ANOVA)
        agg_df = agg_df[agg_df['시기'].isin(['전개기', '절정기', '종식기'])]
        from scipy.stats import f_oneway
        before = agg_df[agg_df['시기'] == '전개기']['총이용자수']
        peak = agg_df[agg_df['시기'] == '절정기']['총이용자수']
        after = agg_df[agg_df['시기'] == '종식기']['총이용자수']
        f_stat, p_val = f_oneway(before, peak, after)

        # 5. 시각화
        import matplotlib
        matplotlib.use('Agg')
        import matplotlib.font_manager as fm
        import matplotlib.pyplot as plt
        import seaborn as sns

        #matplotlib.rc('font', family='Malgun Gothic')  # 이거 먼저
        #matplotlib.rc('axes', unicode_minus=False)     # 마이너스 깨짐 방지

        #plt.rc('font', family='Malgun Gothic')  # Windows인 경우
        #plt.rc('axes', unicode_minus=False)     # 마이너스 깨짐 방지
        #font_path = 'C:/Windows/Fonts/malgun.ttf'  # Windows용 예시
        #fontprop = fm.FontProperties(fname=font_path)
        #plt.rcParams['font.family'] = fontprop.get_name()
        #plt.rcParams['axes.unicode_minus'] = False
        #sns.set_theme(style="whitegrid")
        #plt.figure(figsize=(10, 6))
        #sns.boxplot(data=agg_df, x='시기', y='총이용자수', palette='Set2')
        #plt.title('시기별 자치구 평균 교통량')
        #plt.savefig('app/static/compare_plot.png')  # static 폴더에 저장
        #plt.close()
        # 폰트 경로 설정
        font_path = 'C:/Windows/Fonts/malgun.ttf'
        fontprop = fm.FontProperties(fname=font_path)
        font_name = fontprop.get_name()

        # 폰트 이름 확인
        print("폰트 이름:", font_name)

        # 적용
        plt.rcParams['font.family'] = font_name
        plt.rcParams['axes.unicode_minus'] = False

        # 테스트 그래프
        plt.figure(figsize=(6,4))
        plt.plot([1,2,3], [10, 20, 15])
        plt.title('한글 제목 테스트')
        plt.xlabel('가로축')
        plt.ylabel('세로축')
        plt.tight_layout()
        plt.savefig('test_plot.png')



        return render_template(
            'SHS/compare.html',
            p_val=round(p_val, 4),
            plot_url=url_for('static', filename='compare_plot.png')
        )
    
    @main_bp.route('/chat')
    def chat():
        return render_template('SHS/chat.html')

    @main_bp.route('/support')
    def support():
        return render_template('SHS/support.html')
    
    @main_bp.route('/outlier')
    def outlier():
        return render_template('outlier.html')

    @main_bp.route('/explorer')
    def explorer():
        return render_template('explorer.html') 

    #@main_bp.route('/tables')
    #@main_bp.route('/tables')
    #@main_bp.route('/tables')

