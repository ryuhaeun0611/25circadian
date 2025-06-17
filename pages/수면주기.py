import streamlit as st
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="렘수면 기반 수면 시간 계산기", layout="centered")
st.title("🛌 렘수면 기반 수면 시간 계산기")

mode = st.radio("모드를 선택하세요:", ("자러 가는 시간 → 기상 시간", "기상 시간 → 자러 가야 할 시간"))

def format_time(dt):
    return dt.strftime("%H:%M")

# 수면 시간 → 기상 시간 추천
if mode == "자러 가는 시간 → 기상 시간":
    sleep_time = st.time_input("자러 가는 시간 입력 (잠자리에 드는 시간)", value=datetime.now().time())

    if st.button("기상 시간 추천"):
        now = datetime.now()
        sleep_dt = now.replace(hour=sleep_time.hour, minute=sleep_time.minute, second=0, microsecond=0)

        # 이미 지난 시간이면 내일로 설정
        if sleep_dt < now:
            sleep_dt += timedelta(days=1)

        sleep_dt += timedelta(minutes=15)  # 잠드는 데 걸리는 시간

        st.subheader("💡 추천 기상 시간")
        for i in range(3, 7):  # 3~6 주기
            wake_time = sleep_dt + timedelta(minutes=90 * i)
            st.markdown(f"- {i}주기 ({i*90}분 수면): **{format_time(wake_time)}**")

# 기상 시간 → 수면 시간 추천
else:
    wake_time = st.time_input("기상 시간 입력", value=(datetime.now() + timedelta(hours=7)).time())

    if st.button("취침 시간 추천"):
        now = datetime.now()
        wake_dt = now.replace(hour=wake_time.hour, minute=wake_time.minute, second=0, microsecond=0)

        # 이미 지난 시간이면 내일로 설정
        if wake_dt < now:
            wake_dt += timedelta(days=1)

        st.subheader("💡 추천 취침 시간")
        for i in range(6, 2, -1):  # 6~3 주기
            sleep_time = wake_dt - timedelta(minutes=90 * i) - timedelta(minutes=15)
            st.markdown(f"- {i}주기 ({i*90}분 수면): **{format_time(sleep_time)}**")
