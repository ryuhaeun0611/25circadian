import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="렘수면 기반 수면 계산기", layout="centered")
st.title("🛌 렘수면 기반 수면 시간 계산기 + 시각화")

# 모드 선택
mode = st.radio("모드를 선택하세요:", ("자러 가는 시간 → 기상 시간 추천", "기상 시간 → 자러 가야 할 시간 추천"))

# 시간 포맷 함수
def format_time(dt):
    return dt.strftime("%H:%M")

# Plotly 그래프 생성
def create_sleep_chart(times, title):
    fig = go.Figure()
    for i, (label, time_obj) in enumerate(times):
        fig.add_trace(go.Bar(
            x=[1],
            y=[1],
            base=i,
            orientation='h',
            name=f"{label} - {format_time(time_obj)}",
            hovertext=format_time(time_obj),
            marker=dict(color=f"rgba({50+i*30}, {100+i*20}, 200, 0.6)")
        ))
    fig.update_layout(
        title=title,
        xaxis=dict(showticklabels=False),
        yaxis=dict(
            tickvals=list(range(len(times))),
            ticktext=[f"{label} ({format_time(time)})" for label, time in times],
            autorange="reversed"
        ),
        height=60 * len(times) + 100,
        showlegend=False,
    )
    return fig

# 수면 시간 → 기상 시간 추천
if mode.startswith("자러"):
    sleep_input = st.time_input("🕒 자러 가는 시간 선택", value=datetime.strptime("23:00", "%H:%M").time(), key="sleep_time_input")

    if st.button("기상 시간 계산", key="calculate_wake_time"):
        now = datetime.now()
        sleep_time = now.replace(hour=sleep_input.hour, minute=sleep_input.minute, second=0, microsecond=0)

        if sleep_time < now:
            sleep_time += timedelta(days=1)

        sleep_time += timedelta(minutes=15)  # 잠드는 데 걸리는 시간

        st.subheader("추천 기상 시간 ⏰")
        results = []
        for i in range(3, 7):  # 3~6 주기
            wake_time = sleep_time + timedelta(minutes=90 * i)
            st.markdown(f"- {i}주기: **{format_time(wake_time)}**")
            results.append((f"{i}주기", wake_time))

        fig = create_sleep_chart(results, "예상 기상 시간")
        st.plotly_chart(fig, use_container_width=True)

# 기상 시간 → 수면 시간 추천
else:
    wake_input = st.time_input("🕒 기상 시간 선택", value=datetime.strptime("07:00", "%H:%M").time(), key="wake_time_input")

    if st.button("취침 시간 계산", key="calculate_sleep_time"):
        now = datetime.now()
        wake_time = now.replace(hour=wake_input.hour, minute=wake_input.minute, second=0, microsecond=0)

        if wake_time < now:
            wake_time += timedelta(days=1)

        st.subheader("추천 취침 시간 🌙")
        results = []
        for i in range(6, 2, -1):  # 6~3 주기
            sleep_time = wake_time - timedelta(minutes=90 * i) - timedelta(minutes=15)
            st.markdown(f"- {i}주기: **{format_time(sleep_time)}**")
            results.append((f"{i}주기", sleep_time))

        fig = create_sleep_chart(results[::-1], "추천 취침 시간")
        st.plotly_chart(fig, use_container_width=True)
