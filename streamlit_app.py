import streamlit as st
import pandas as pd
import numpy as np

# 여기서부터 자유롭게 작성하세요

# ── 예시 구조 (지우고 새로 써도 됩니다) ────────────────
df = pd.read_csv(
    "10강_과제용_음악_data.txt",
    sep="\t",
    encoding="utf-16"
)

st.title("나의 음악 대시보드")           # ← 제목을 바꾸세요
st.caption("10강 실습 과제")

# [텍스트]
st.header("소개")
st.write("장르별 노래 평점과 월간 재생 수를 살펴보는 대시보드입니다.")  # ← 내용을 채우세요

# [텍스트]
st.header("소개")
st.write("장르별 노래 평점과 월간 재생 수를 살펴보는 대시보드입니다.")

# [위젯 + 위젯-화면 연동]
st.header("설정")

genre = st.selectbox(
    "장르를 선택하세요",
    sorted(df["genre"].unique())
)

# 선택한 장르의 노래만 남김
genre_df = df[df["genre"] == genre].copy()

# 선택한 장르의 평균 평점 표시
average_rating = genre_df["rating"].mean()
st.metric(
    label=f"{genre} 평균 평점",
    value=f"{average_rating:.2f}점"
)

# 표시할 노래 수 선택
# 차트 종류 선택
chart_type = st.radio(
    "차트 종류를 선택하세요",
    ["막대", "꺾은선", "면적"],
    horizontal=True
)

# 차트를 이 위치에 표시할 빈 공간을 먼저 만듭니다.
chart_placeholder = st.empty()

# 표시할 노래 수 선택
song_count = st.slider(
    "차트에 표시할 노래 수",
    min_value=5,
    max_value=len(genre_df),
    value=min(10, len(genre_df))
)

# 재생 수 상위 곡과 평점 상위 곡을 각각 준비합니다.
top_plays = genre_df.nlargest(song_count, "monthly_plays")
plays_data = top_plays.set_index("title")[["monthly_plays"]]
plays_data = plays_data.rename(columns={"monthly_plays": "월간 재생 수"})

top_ratings = genre_df.nlargest(song_count, "rating")
ratings_data = top_ratings.set_index("title")[["rating"]]
ratings_data = ratings_data.rename(columns={"rating": "평점"})

# 차트는 위의 빈 공간에 표시되고, 슬라이더는 그 아래에 놓입니다.
with chart_placeholder.container():
    st.header("차트")

    st.subheader("월간 재생 수 TOP")
    if chart_type == "막대":
        st.bar_chart(plays_data)
    elif chart_type == "꺾은선":
        st.line_chart(plays_data)
    else:
        st.area_chart(plays_data)

    st.subheader("평점 TOP")
    if chart_type == "막대":
        st.bar_chart(ratings_data)
    elif chart_type == "꺾은선":
        st.line_chart(ratings_data)
    else:
        st.area_chart(ratings_data)
