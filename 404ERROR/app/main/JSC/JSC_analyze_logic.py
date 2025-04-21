import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

def plot_date_transport_ratio(df, selected_date):
    date_df = df[df['일자'] == pd.to_datetime(selected_date).date()].copy()
    date_df["지하철_이용비율(%)"] = (date_df["지하철_승차총승객수"] / date_df["총생활인구수"]) * 100
    date_df["버스_이용비율(%)"] = (date_df["버스_승차총승객수"] / date_df["총생활인구수"]) * 100

    fig, ax = plt.subplots(figsize=(10, 6))
    x = np.arange(len(date_df["자치구"]))
    ax.bar(x - 0.2, date_df["지하철_이용비율(%)"], width=0.4, label="지하철")
    ax.bar(x + 0.2, date_df["버스_이용비율(%)"], width=0.4, label="버스")

    ax.set_xticks(x)
    ax.set_xticklabels(date_df["자치구"], rotation=45)
    ax.set_title(f"{selected_date} 자치구별 대중교통 이용 비율")
    ax.set_ylabel("이용 비율 (%)")
    ax.legend()
    plt.tight_layout()
    return fig

def generate_female_gu_chart(df):
    grouped = df.groupby("자치구").agg({
        "여자미성년자": "sum", "여자청년": "sum", "여자중년": "sum", "여자노년": "sum",
        "남자미성년자": "sum", "남자청년": "sum", "남자중년": "sum", "남자노년": "sum",
        "총생활인구수": "sum", "지하철_승차총승객수": "sum", "버스_승차총승객수": "sum"
    }).reset_index()

    grouped["여성인구"] = grouped[["여자미성년자", "여자청년", "여자중년", "여자노년"]].sum(axis=1)
    grouped["총인구"] = grouped["여성인구"] + grouped[["남자미성년자", "남자청년", "남자중년", "남자노년"]].sum(axis=1)
    grouped["여성비율"] = grouped["여성인구"] / grouped["총인구"]
    grouped["지하철이용비율"] = grouped["지하철_승차총승객수"] / grouped["총생활인구수"]
    grouped["버스이용비율"] = grouped["버스_승차총승객수"] / grouped["총생활인구수"]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(data=grouped, x="여성비율", y="지하철이용비율", label="지하철", ax=ax)
    sns.regplot(data=grouped, x="여성비율", y="버스이용비율", label="버스", ax=ax)
    ax.set_title("자치구별 여성비율 vs 교통 이용비율")
    ax.legend()
    return fig

def generate_female_age_chart(df):
    # 자치구별로 데이터 집계
    grouped = df.groupby("자치구").agg({
        "여자미성년자": "sum", "여자청년": "sum", "여자중년": "sum", "여자노년": "sum",
        "남자미성년자": "sum", "남자청년": "sum", "남자중년": "sum", "남자노년": "sum",
        "총생활인구수": "sum", "지하철_승차총승객수": "sum", "버스_승차총승객수": "sum"
    }).reset_index()

    # 연령대 리스트
    age_groups = ["미성년자", "청년", "중년", "노년"]

    # 연령대별 여성비율 계산
    for age in age_groups:
        female_col = f"여자{age}"
        male_col = f"남자{age}"
        grouped[f"{age}_여성비율"] = grouped[female_col] / (grouped[female_col] + grouped[male_col])

    # 교통 이용 비율 계산
    grouped["지하철이용비율"] = grouped["지하철_승차총승객수"] / grouped["총생활인구수"]
    grouped["버스이용비율"] = grouped["버스_승차총승객수"] / grouped["총생활인구수"]

    # 4행 2열 subplot 생성
    fig, axes = plt.subplots(4, 2, figsize=(6, 12))
    fig.suptitle("자치구별 연령대별 여성비율 vs 교통 이용비율", fontsize=16)

    for i, age in enumerate(age_groups):
        x_col = f"{age}_여성비율"

        # 첫 번째 열: 지하철
        sns.regplot(data=grouped, x=x_col, y="지하철이용비율", ax=axes[i, 0])
        axes[i, 0].set_title(f"{age} 여성비율 vs 지하철")
        axes[i, 0].set_xlabel("여성비율")
        axes[i, 0].set_ylabel("지하철 이용비율")

        # 두 번째 열: 버스
        sns.regplot(data=grouped, x=x_col, y="버스이용비율", ax=axes[i, 1])
        axes[i, 1].set_title(f"{age} 여성비율 vs 버스")
        axes[i, 1].set_xlabel("여성비율")
        axes[i, 1].set_ylabel("버스 이용비율")

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 제목 공간 확보
    return fig

def generate_male_gu_chart(df):
    grouped = df.groupby("자치구").agg({
        "남자미성년자": "sum", "남자청년": "sum", "남자중년": "sum", "남자노년": "sum",
        "여자미성년자": "sum", "여자청년": "sum", "여자중년": "sum", "여자노년": "sum",
        "총생활인구수": "sum", "지하철_승차총승객수": "sum", "버스_승차총승객수": "sum"
    }).reset_index()

    grouped["남성인구"] = grouped[["남자미성년자", "남자청년", "남자중년", "남자노년"]].sum(axis=1)
    grouped["총인구"] = grouped["남성인구"] + grouped[["여자미성년자", "여자청년", "여자중년", "여자노년"]].sum(axis=1)
    grouped["남성비율"] = grouped["남성인구"] / grouped["총인구"]
    grouped["지하철이용비율"] = grouped["지하철_승차총승객수"] / grouped["총생활인구수"]
    grouped["버스이용비율"] = grouped["버스_승차총승객수"] / grouped["총생활인구수"]

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.regplot(data=grouped, x="남성비율", y="지하철이용비율", label="지하철", ax=ax)
    sns.regplot(data=grouped, x="남성비율", y="버스이용비율", label="버스", ax=ax)
    ax.set_title("자치구별 남성비율 vs 교통 이용비율")
    ax.legend()
    return fig
##################################################################
# def generate_male_age_chart(df):
#     male_cols = ["남자미성년자", "남자청년", "남자중년", "남자노년"]
#     df["남성총"] = df[male_cols].sum(axis=1)
#     df = df[df["남성총"] > 0]

#     fig, ax = plt.subplots(figsize=(10, 6))
#     for col in male_cols:
#         ratio = df[col] / df["남성총"]
#         ax.plot(ratio.rolling(30).mean(), label=col)
#     ax.set_title("남성 연령대별 교통 이용 비율 (30일 평균)")
#     ax.legend()
#     return fig
###################################################################
def generate_male_age_chart(df):
    # 자치구별로 데이터 집계
    grouped = df.groupby("자치구").agg({
        "여자미성년자": "sum", "여자청년": "sum", "여자중년": "sum", "여자노년": "sum",
        "남자미성년자": "sum", "남자청년": "sum", "남자중년": "sum", "남자노년": "sum",
        "총생활인구수": "sum", "지하철_승차총승객수": "sum", "버스_승차총승객수": "sum"
    }).reset_index()

    # 연령대 리스트
    age_groups = ["미성년자", "청년", "중년", "노년"]

    # 연령대별 남성비율 계산
    for age in age_groups:
        male_col = f"남자{age}"
        female_col = f"여자{age}"
        grouped[f"{age}_남성비율"] = grouped[male_col] / (grouped[male_col] + grouped[female_col])

    # 교통 이용 비율 계산
    grouped["지하철이용비율"] = grouped["지하철_승차총승객수"] / grouped["총생활인구수"]
    grouped["버스이용비율"] = grouped["버스_승차총승객수"] / grouped["총생활인구수"]

    # 4행 2열 subplot 생성
    fig, axes = plt.subplots(4, 2, figsize=(6, 12))
    fig.suptitle("자치구별 연령대별 남성비율 vs 교통 이용비율", fontsize=16)

    for i, age in enumerate(age_groups):
        x_col = f"{age}_남성비율"

        # 첫 번째 열: 지하철
        sns.regplot(data=grouped, x=x_col, y="지하철이용비율", ax=axes[i, 0])
        axes[i, 0].set_title(f"{age} 남성비율 vs 지하철")
        axes[i, 0].set_xlabel("남성비율")
        axes[i, 0].set_ylabel("지하철 이용비율")

        # 두 번째 열: 버스
        sns.regplot(data=grouped, x=x_col, y="버스이용비율", ax=axes[i, 1])
        axes[i, 1].set_title(f"{age} 남성비율 vs 버스")
        axes[i, 1].set_xlabel("남성비율")
        axes[i, 1].set_ylabel("버스 이용비율")

    plt.tight_layout(rect=[0, 0, 1, 0.96])  # 제목 공간 확보
    return fig
