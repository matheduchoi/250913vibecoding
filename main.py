import streamlit as st
import pandas as pd
import altair as alt
import re
import os

st.set_page_config(page_title="MBTI World TOP10", page_icon="🌍", layout="wide")

st.title("🌍 MBTI 유형별 국가 TOP10 대시보드")
st.write("데이터 파일이 로컬에 있으면 자동으로 불러오고, 없을 경우 업로드를 통해 불러옵니다.")

# --- 데이터 불러오기 ---
@st.cache_data
def load_data():
    filename = "countriesMBTI_16types.csv"
    if os.path.exists(filename):
        df = pd.read_csv(filename)
    else:
        uploaded_file = st.file_uploader("📂 MBTI 데이터 CSV 파일을 업로드하세요", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
        else:
            st.stop()  # 데이터 없으면 앱 중단
    return df

df = load_data()

# MBTI 컬럼 자동 탐지
mbti_pattern = re.compile(r'^[IE][NS][TF][JP]$')
mbti_cols = [c for c in df.columns if isinstance(c, str) and mbti_pattern.match(c)]

# 사용자에게 MBTI 선택 옵션 제공
selected_mbti = st.selectbox("🔎 MBTI 유형을 선택하세요:", mbti_cols, index=0)

# 선택된 MBTI에 대해 국가별 상위 10
top10 = df[['Country', selected_mbti]].sort_values(by=selected_mbti, ascending=False).head(10)

# Altair 그래프 그리기
chart = (
    alt.Chart(top10)
    .mark_bar()
    .encode(
        x=alt.X(f"{selected_mbti}:Q", title=f"{selected_mbti} 비율"),
        y=alt.Y("Country:N", sort='-x', title="국가"),
        tooltip=["Country", selected_mbti]
    )
    .properties(
        width=600,
        height=400,
        title=f"🌟 {selected_mbti} 유형 비율이 가장 높은 국가 TOP10"
    )
)

st.altair_chart(chart, use_container_width=True)

# 데이터 테이블도 함께 표시
st.subheader("📋 데이터 확인")
st.dataframe(top10)
