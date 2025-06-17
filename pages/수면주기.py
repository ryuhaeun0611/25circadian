import streamlit as st
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="렘수면 기반 수면 시간 계산기", layout="centered")
st.title("🛌 렘수면 기반 수면 시간 계산기")

# 모드 선택
mode = st.radio("모드를 선택하세요:", ("자러 가는 시간 → 기상 시간", "기상 시간 → 자러 가야 할 시간"))

# 시간 포맷 함수
def format_time(dt):
    return dt.strftime("%H:%M")

# 수면 시간 → 기상 시간 추천
if mode == "자러 가는 시간 → 기상 시간":
    sleep_time = st.time_input("자러 가는 시간 입력 (잠자리에 드는 시간)", value=datetime.now().time())

    if st.button("기상 시간 추천"):
        sleep_datetime = datetime.combine(datetime.today(), sleep_time) + timedelta(minutes=15)
        st.subheader("💡 추천 기상 시간")
        for i in range(3, 7):  # 3~6 수면 주기
            wake_time = sleep_datetime + timedelta(minutes=90 * i)
            st.markdown(f"- {i}주기 ({i*90}분 수면): **{format_time(wake_time)}**")

# 기상 시간 → 수면 시간 추천
else:
    wake_time = st.time_input("기상 시간 입력", value=(datetime.now() + timedelta(hours=7)).time())

    if st.button("취침 시간 추천"):
        wake_datetime = datetime.combine(datetime.today(), wake_time)
        st.subheader("💡 추천 취침 시간")
        for i in range(6, 2, -1):  # 6~3 수면 주기
            sleep_time = wake_datetime - timedelta(minutes=90 * i) - timedelta(minutes=15)
            st.markdown(f"- {i}주기 ({i*90}분 수면): **{format_time(sleep_time)}**")
