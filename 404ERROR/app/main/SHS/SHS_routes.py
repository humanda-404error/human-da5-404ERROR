from flask import Blueprint, render_template, request, current_app, session, jsonify, json
from app.auth.routes import get_db_connection
from app.main.blueprint import main_bp
from app.models import Member, Notice, Update, Weather, Population, Train
from datetime import datetime

import pandas as pd
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.font_manager as fm
import seaborn as sns

from scipy.stats import f_oneway



def register_SHS_routes(main_bp):
    #회귀선, 상관계수.. 우리가 날씨랑 연관있는거 같은데 아니더라 why? 
    
    @main_bp.route('/compare', methods=['GET', 'POST'])
    def compare():
        method = request.form.get("method")
        # 회귀, ANOVA, ANCOVA
        from statsmodels.formula.api import ols
        from statsmodels.stats.anova import anova_lm
        # MANOVA
        from statsmodels.multivariate.manova import MANOVA
        # Mixed Effects Model
        import statsmodels.api as sm
        import statsmodels.formula.api as smf
        # 상관 분석
        from scipy.stats import pearsonr


        def format_y_axis(ax, unit=''):
            ax.yaxis.set_major_formatter(
                ticker.FuncFormatter(lambda x, pos: f'{int(x):,}{unit}')
            )
        def COVID19_periods(ax): # COVID-19 period
            ax.axvspan(pd.to_datetime('2020-01-01'), pd.to_datetime('2021-01-01'), color='gray', alpha=0.2, label='코로나 전개기')
            ax.axvspan(pd.to_datetime('2021-07-01'), pd.to_datetime('2022-07-01'), color='orange', alpha=0.2, label='코로나 절정기')
            ax.axvspan(pd.to_datetime('2023-01-01'), pd.to_datetime('2024-12-31'), color='green', alpha=0.2, label='코로나 종식기')
       
        # 1. ANOVA (단일 분산분석)
        def run_anova(data, group_col, value_col):
            grouped = data.groupby(group_col)[value_col]
            samples = [group.dropna() for _, group in grouped]
            if len(samples) > 1:
                return f_oneway(*samples).pvalue
            return None
        def run_anova_and_plot(data, group_col, value_col, title, filename, plot_dir, analysis_images, result_details):
            p_val = run_anova(data, group_col, value_col)
            result_details.append(f"<p>{title} ANOVA p-value: {p_val}</p>")

            plt.figure(figsize=(10, 5))
            sns.boxplot(data=data, x=group_col, y=value_col)
            plt.title(title)
            plt.tight_layout()
            
            path = os.path.join(plot_dir, filename)
            plt.savefig(path)
            analysis_images.append(f"img/SHS/{filename}")
            plt.close()
        
        # 2. ANCOVA (공변량 포함)
        def run_ancova(data, group_col, covariate_col, value_col):
            data = data[[group_col, covariate_col, value_col]].dropna()
            formula = f"{value_col} ~ C({group_col}) + {covariate_col}"
            model = ols(formula, data=data).fit()
            return anova_lm(model)
        
        def run_ancova_and_plot(data, group_col, covariate_col, value_col, title, filename, plot_dir, analysis_images, result_details):
            data = data[[group_col, covariate_col, value_col]].dropna()

            formula = f"{value_col} ~ C({group_col}) + {covariate_col}"
            model = ols(formula, data=data).fit()
            p_table = anova_lm(model)

            img_path = os.path.join(plot_dir, filename)
            sns.lmplot(data=data, x=covariate_col, y=value_col, hue=group_col, ci=None)
            plt.title(title)
            plt.tight_layout()
            plt.savefig(img_path)
            plt.close()

            analysis_images.append(f"img/SHS/{filename}")
            result_details.append(
                f"<p>{title} ANCOVA 결과:<br><pre>{p_table}</pre><img src='/static/img/SHS/{filename}' width='500'></p>"
            )

        # 4. MANCOVA (공변량 포함 다변량 분산분석)
        def run_mancova(data, group_col, covariate_cols, dependent_cols):
            cols = [group_col] + covariate_cols + dependent_cols
            data = data[cols].dropna()

            # 공식 생성 예: "지하철 + 버스 ~ 코로나시기 + 인구 + 온도"
            formula = " + ".join(dependent_cols) + " ~ " + f"C({group_col})"
            if covariate_cols:
                formula += " + " + " + ".join(covariate_cols)

            mv = MANOVA.from_formula(formula, data)
            return mv.mv_test()

        def add_legend(ax,ax2):
            lines, labels = ax.get_legend_handles_labels()
            lines2, labels2 = ax2.get_legend_handles_labels()
            all_lines = lines + lines2
            all_labels = labels + labels2

            # 범례가 있을 때만 생성 및 스타일 적용
            if all_lines:
                legend = ax.legend(all_lines, all_labels,
                                loc='lower right', frameon=True,
                                fontsize=9, framealpha=1,
                                edgecolor='black', facecolor='white')
                
                if legend:  # legend가 None이 아닌 경우에만
                    frame = legend.get_frame()
                    frame.set_facecolor('none')         # 배경 없애기
                    frame.set_edgecolor('black')        # 테두리 색
                    frame.set_linewidth(1.2)            # 테두리 굵기
                    frame.set_boxstyle('round,pad=0.3') # 살짝 둥글게
        
        def draw_plot(): pass

        def preprocess_weather(weather_df):
            weather_df = weather_df.copy()
            weather_df['기온범주'] = pd.cut(weather_df['평균기온'], [-float('inf'), 0, 30, float('inf')], labels=['0℃ 이하', '0~30℃', '30℃ 이상'])
            max_rain = weather_df['일강수량'].max()
            weather_df['강우비율'] = weather_df['일강수량'] / max_rain
            return weather_df

        def label_covid_period(df):
            df['코로나시기'] = pd.cut(df['일시'],
                [pd.Timestamp('2019-12-31'), pd.Timestamp('2021-01-01'), pd.Timestamp('2022-07-01'), pd.Timestamp('2024-01-01'), pd.Timestamp('2025-01-01')],
                labels=['전개기', '절정기', '종식기', '이후'],
                right=False)
            return df
        
        ########VIP 이상기능########
        from statsmodels.stats.multicomp import pairwise_tukeyhsd
        def perform_advanced_analysis(datasets, train_range, bus_range, pop_range, weather_range, plot_dir):
            results = []
            images = []

            # 지하철
            if "지하철" in datasets:
                df = train_range.dropna(subset=['코로나시기', '승차총승객수'])
                tukey = pairwise_tukeyhsd(df['승차총승객수'], df['코로나시기'])
                results.append("<h5>지하철 Tukey HSD</h5><pre>" + str(tukey.summary()) + "</pre>")

                plt.figure(figsize=(8, 5))
                sns.barplot(data=df, x='코로나시기', y='승차총승객수', ci='sd', palette='pastel')
                plt.title("지하철 - 시기별 평균 승차 수")
                plt.tight_layout()
                path = os.path.join(plot_dir, "advanced_barplot_subway.png")
                plt.savefig(path)
                images.append("img/SHS/advanced_barplot_subway.png")
                plt.close()

            # 버스
            if "버스" in datasets:
                df = bus_range.dropna(subset=['코로나시기', '승차총승객수'])
                tukey = pairwise_tukeyhsd(df['승차총승객수'], df['코로나시기'])
                results.append("<h5>버스 Tukey HSD</h5><pre>" + str(tukey.summary()) + "</pre>")

                plt.figure(figsize=(8, 5))
                sns.barplot(data=df, x='코로나시기', y='승차총승객수', ci='sd', palette='pastel')
                plt.title("버스 - 시기별 평균 승차 수")
                plt.tight_layout()
                path = os.path.join(plot_dir, "advanced_barplot_bus.png")
                plt.savefig(path)
                images.append("img/SHS/advanced_barplot_bus.png")
                plt.close()

            # 인구
            if "인구" in datasets:
                pop_group = pop_range.groupby(['일시', '코로나시기'])['총생활인구수'].sum().reset_index()
                tukey = pairwise_tukeyhsd(pop_group['총생활인구수'], pop_group['코로나시기'])
                results.append("<h5>생활인구 Tukey HSD</h5><pre>" + str(tukey.summary()) + "</pre>")

                plt.figure(figsize=(8, 5))
                sns.barplot(data=pop_group, x='코로나시기', y='총생활인구수', ci='sd', palette='pastel')
                plt.title("생활 인구 - 시기별 총합 평균")
                plt.tight_layout()
                path = os.path.join(plot_dir, "advanced_barplot_pop.png")
                plt.savefig(path)
                images.append("img/SHS/advanced_barplot_pop.png")
                plt.close()

            # 날씨
            if "날씨" in datasets:
                df = weather_range.dropna(subset=['평균기온', '일시']).copy()
                df = label_covid_period(df)
                df = df.dropna(subset=['코로나시기'])
                tukey = pairwise_tukeyhsd(df['평균기온'], df['코로나시기'])
                results.append("<h5>평균기온 Tukey HSD</h5><pre>" + str(tukey.summary()) + "</pre>")

                plt.figure(figsize=(8, 5))
                sns.barplot(data=df, x='코로나시기', y='평균기온', ci='sd', palette='pastel')
                plt.title("날씨 - 시기별 평균기온")
                plt.tight_layout()
                path = os.path.join(plot_dir, "advanced_barplot_weather.png")
                plt.savefig(path)
                images.append("img/SHS/advanced_barplot_weather.png")
                plt.close()

            return results, images

        # 한글 폰트 설정
        font_path = 'C:/Windows/Fonts/malgun.ttf'
        if os.path.exists(font_path):
            fontprop = fm.FontProperties(fname=font_path)
            font_name = fontprop.get_name()
            matplotlib.rcParams['font.family'] = font_name
            matplotlib.rcParams['axes.unicode_minus'] = False
            sns.set_theme(style="whitegrid", font=font_name, rc={"axes.unicode_minus": False})
        else:
            print("폰트 미적용")

        # 데이터 불러오기
        conn = get_db_connection()
        train_df = pd.read_sql("SELECT * FROM train", conn)
        pop_df = pd.read_sql("SELECT * FROM population", conn)
        weather_df = pd.read_sql("SELECT * FROM weather", conn)
        bus_df = pd.read_sql("SELECT * FROM bus", conn)

        # 날짜 파라미터 처리
        start_date_str = request.args.get("start_date", "2020-01-01")
        end_date_str = request.args.get("end_date", "2024-12-31")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
        except ValueError:
            return "날짜 형식 오류", 400

        for df in [train_df, pop_df, weather_df, bus_df]:
            df['일시'] = pd.to_datetime(df['일시'])

        # 기간 필터링
        train_range = train_df[(train_df['일시'] >= start_date) & (train_df['일시'] <= end_date)]
        bus_range = bus_df[(bus_df['일시'] >= start_date) & (bus_df['일시'] <= end_date)]
        weather_range = weather_df[(weather_df['일시'] >= start_date) & (weather_df['일시'] <= end_date)]
        pop_range = pop_df[(pop_df['일시'] >= start_date) & (pop_df['일시'] <= end_date)]

        # 데이터 검정용 코로나기간 필터링
        train_range = label_covid_period(train_range)
        bus_range = label_covid_period(bus_range)
        pop_range = label_covid_period(pop_range)
        weather_range = label_covid_period(weather_range)
        weather_range = preprocess_weather(weather_range) 

        # 강우량 정규화 데이터 준비
        rain_df = weather_range.groupby(weather_range['일시'].dt.date)['일강수량'].sum().fillna(0)
        max_rain = rain_df.max()
        rain_norm = rain_df / max_rain if max_rain > 0 else rain_df

        # 그래프 저장 경로
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(BASE_DIR, '..', '..'))
        plot_dir = os.path.join(project_root, 'static', 'img', 'SHS')
        os.makedirs(plot_dir, exist_ok=True)

        # 날씨 그래프
        fig, ax = plt.subplots(figsize=(10, 4))
        weather_daily = weather_range.groupby(weather_range['일시'].dt.date)['평균기온'].mean()
        weather_daily.plot(ax=ax, color='orange', label='평균기온')
        ax.set_title("날씨")
        ax.set_xlabel("날짜")
        ax.set_xlim([start_date, end_date])
        COVID19_periods(ax)
        format_y_axis(ax)
        ax2 = ax.twinx()
        rain_norm.plot(ax=ax2, color='blue', alpha=0.3, label='강우비율')
        ax2.set_ylabel("강우량 비율", color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')
        add_legend(ax, ax2) # 범례처리
        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, "weather_plot.png"))
        plt.close()

        # 지하철 그래프
        fig, ax = plt.subplots(figsize=(10, 4))
        train_daily = train_range.groupby(train_range['일시'].dt.date)[['승차총승객수', '하차총승객수']].sum()
        train_daily['승차총승객수'].plot(ax=ax, color='red', label='승차')
        train_daily['하차총승객수'].plot(ax=ax, color='green', label='하차')
        ax.set_title("지하철")
        ax.set_xlabel("날짜")
        ax.set_xlim([start_date, end_date])
        COVID19_periods(ax)
        format_y_axis(ax, '명')
        ax2 = ax.twinx()
        rain_norm.plot(ax=ax2, color='blue', alpha=0.3, label='강우비율')
        ax2.set_ylabel("강우량 비율", color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        add_legend(ax, ax2) # 범례처리

        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, "subway_plot.png"))
        plt.close()

        # 버스 그래프
        fig, ax = plt.subplots(figsize=(10, 4))
        bus_daily = bus_range.groupby(bus_range['일시'].dt.date)[['승차총승객수', '하차총승객수']].sum()
        bus_daily['승차총승객수'].plot(ax=ax, color='red', label='승차')
        bus_daily['하차총승객수'].plot(ax=ax, color='green', label='하차')
        ax.set_title("버스")
        ax.set_xlabel("날짜")
        ax.set_xlim([start_date, end_date])
        COVID19_periods(ax)
        format_y_axis(ax, '명')
        ax2 = ax.twinx()
        rain_norm.plot(ax=ax2, color='blue', alpha=0.3, label='강우비율')
        ax2.set_ylabel("강우량 비율", color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        add_legend(ax, ax2) # 범례처리

        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, "bus_plot.png"))
        plt.close()

        # 인구 그래프
        fig, ax = plt.subplots(figsize=(10, 4))
        pop_0 = pop_range[pop_range['시간대구분'] == '0']
        pop_12 = pop_range[pop_range['시간대구분'] == '12']
        pop_0_daily = pop_0.groupby(pop_0['일시'].dt.date)['총생활인구수'].sum()
        pop_12_daily = pop_12.groupby(pop_12['일시'].dt.date)['총생활인구수'].sum()
        pop_0_daily.plot(ax=ax, color='red', label='0시')
        pop_12_daily.plot(ax=ax, color='green', label='12시')
        ax.set_title("생활 인구")
        ax.set_xlabel("날짜")
        ax.set_xlim([start_date, end_date])
        COVID19_periods(ax)
        format_y_axis(ax, '명')
        ax2 = ax.twinx()
        rain_norm.plot(ax=ax2, color='blue', alpha=0.3, label='강우비율')
        ax2.set_ylabel("강우량 비율", color='blue')
        ax2.tick_params(axis='y', labelcolor='blue')

        add_legend(ax, ax2) # 범례처리

        plt.tight_layout()
        plt.savefig(os.path.join(plot_dir, "pop_plot.png"))
        plt.close()

        #분석기법#
        method = request.args.get("method")             #검정기법 name
        datasets = request.args.getlist("dataset")      #분석 대상 checklist

        #init#
        analysis_result = None
        result_details = []
        analysis_images = []  


        

        match method:
            case "ANOVA":
                        #get debug#
                if method:
                    print("선택된 검정 기법:", method)
                datasets = request.args.getlist("dataset")
                if len(datasets) == 1 and ',' in datasets[0]:
                    datasets = datasets[0].split(',')

                if "지하철" in datasets:              
                    p_val = run_anova(train_range, '코로나시기', '승차총승객수')
                   # result_details.append(f"<p>지하철 ANOVA p-value: {p_val:.5f}</p>")
                    run_anova_and_plot(
                        train_range, '코로나시기', '승차총승객수',
                        "코로나 시기별 지하철 이용량 (ANOVA 시각화)",
                        "anova_subway.png",
                        plot_dir,  # << 추가됨
                        analysis_images, result_details
                    )
                if "버스" in datasets:
                    run_anova_and_plot(
                        bus_range, '코로나시기', '승차총승객수',
                        "코로나 시기별 버스 이용량 (ANOVA 시각화)",
                        "anova_bus.png",
                        plot_dir,
                        analysis_images, result_details
                    )
                if "인구" in datasets:
                    pop_sum = pop_range.groupby(['일시', '코로나시기'])['총생활인구수'].sum().reset_index()
                    run_anova_and_plot(
                        pop_sum, '코로나시기', '총생활인구수',
                        "코로나 시기별 총생활인구수 (ANOVA 시각화)",
                        "anova_pop.png",
                        plot_dir,
                        analysis_images, result_details
                    )
                if "날씨" in datasets:
                    # 평균기온
                    weather_temp = weather_range.groupby(['일시', '코로나시기'])['평균기온'].mean().reset_index()
                    run_anova_and_plot(
                        weather_temp, '코로나시기', '평균기온',
                        "코로나 시기별 평균기온 (ANOVA 시각화)",
                        "anova_temp.png",
                        plot_dir,
                        analysis_images, result_details
                    )

                    # 강수량
                    weather_rain = weather_range.groupby(['일시', '코로나시기'])['일강수량'].sum().reset_index()
                    run_anova_and_plot(
                        weather_rain, '코로나시기', '일강수량',
                        "코로나 시기별 일강수량 (ANOVA 시각화)",
                        "anova_rain.png",
                        plot_dir,
                        analysis_images, result_details
                    )

            case "ANCOVA":
                # 파라미터 처리
                method = request.args.get("method")
                datasets = request.args.getlist("dependent")
                covariates = request.args.getlist("cov")

                if len(datasets) == 1 and ',' in datasets[0]:
                    datasets = datasets[0].split(',')
                if len(covariates) == 1 and ',' in covariates[0]:
                    covariates = covariates[0].split(',')

                print("=== ANCOVA DEBUG ===")
                print("선택된 종속변수:", datasets)
                print("선택된 공변량:", covariates)

                for dep in datasets:
                    # 공변량에서 자기 자신 제거
                    valid_covs = [cov for cov in covariates if cov != dep]

                    # 종속 변수에 따른 데이터셋, 컬럼 정의
                    if dep == "지하철":
                        data = train_range.copy()
                        value_col = "승차총승객수"
                    elif dep == "버스":
                        data = bus_range.copy()
                        value_col = "승차총승객수"
                    elif dep == "인구":
                        data = pop_range.copy()
                        value_col = "총생활인구수"
                    else:
                        continue

                    # 공변량 데이터 병합 및 매핑
                    covariate_map = {}
                    for cov in valid_covs:
                        if cov == "지하철":
                            data = data.merge(train_range[["일시", "승차총승객수"]], on="일시", suffixes=('', '_지하철'))
                            covariate_map[cov] = "승차총승객수_지하철"
                        elif cov == "버스":
                            data = data.merge(bus_range[["일시", "승차총승객수"]], on="일시", suffixes=('', '_버스'))
                            covariate_map[cov] = "승차총승객수_버스"
                        elif cov == "인구":
                            data = data.merge(pop_range[["일시", "총생활인구수"]], on="일시")
                            covariate_map[cov] = "총생활인구수"
                        elif cov == "온도":
                            data = data.merge(weather_range[["일시", "평균기온"]], on="일시")
                            covariate_map[cov] = "평균기온"
                        elif cov == "강수량":
                            data = data.merge(weather_range[["일시", "일강수량"]], on="일시")
                            covariate_map[cov] = "일강수량"

                    # ANCOVA 수행
                    for cov in valid_covs:
                        cov_col = covariate_map.get(cov)
                        if not cov_col or cov_col not in data.columns:
                            continue

                        title = f"{dep} (공변량: {cov})"
                        filename = f"ancova_{dep}_{cov}.png"

                        run_ancova_and_plot(
                            data=data,
                            group_col="코로나시기",
                            covariate_col=cov_col,
                            value_col=value_col,
                            title=title,
                            filename=filename,
                            plot_dir=plot_dir,
                            analysis_images=analysis_images,
                            result_details=result_details
                        )

            case "MANOVA":
                # 예시: 종속변수 = ['지하철', '버스'], 공변량 = ['인구', '온도']
                dependent_cols = []
                covariate_cols = []

                # 종속변수 추출
                if "지하철" in datasets:
                    dependent_cols.append('지하철')
                    train_range = train_range.rename(columns={'승차총승객수': '지하철'})
                if "버스" in datasets:
                    dependent_cols.append('버스')
                    bus_range = bus_range.rename(columns={'승차총승객수': '버스'})

                # 공변량 수동 지정 예시 (사용자가 선택한 값 기반으로 처리 가능)
                covariate_cols = ['인구', '온도']

                # 데이터 병합
                df_merged = train_range.merge(bus_range, on=['일시', '코로나시기'], how='inner') \
                                    .merge(pop_range[['일시', '총생활인구수']], on='일시') \
                                    .merge(weather_range[['일시', '평균기온']], on='일시')
                df_merged = df_merged.rename(columns={'총생활인구수': '인구', '평균기온': '온도'})

                result = run_mancova(df_merged, '코로나시기', covariate_cols, dependent_cols)
                result_details.append(f"<p>MANCOVA 결과:<br><pre>{result}</pre></p>")



        analysis_result = {
            "method": method,
            "conditions": datasets,
            "result_html": ''.join(result_details),
            "result_imgs": analysis_images
        }
        grade = session.get('grade', '일반')
        advanced_mode = request.args.get('advanced', default=0, type=int)
        if advanced_mode and grade in ['VIP', '관리자']:
            tukey_result, barplot_imgs = perform_advanced_analysis(
                datasets, train_range, bus_range, pop_range, weather_range, plot_dir
            )

            return render_template(
                "SHS/compare.html",
                start_date=start_date_str,
                end_date=end_date_str,
                analysis_result=analysis_result,
                barplot_imgs=barplot_imgs,
                tukey_result=tukey_result,
                advanced=True
            )

        return render_template(
            "SHS/compare.html",
            start_date=start_date_str,
            end_date=end_date_str,
            analysis_result=analysis_result,
            advanced=False
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

