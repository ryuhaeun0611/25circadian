import streamlit as st
from datetime import datetime, timedelta
import plotly.graph_objects as go

st.set_page_config(page_title="렘수면 수면 시간 계산기", layout="centered")
st.title("🛌 렘수면 기반 수면 시간 계산기 + 시각화")

mode = st.radio("모드를 선택하세요:", ("자러 가는 시간 → 기상 시간 추천", "기상 시간 → 자러 가야 할 시간 추천"))

# 시간 포맷 함수
def format_time(dt):
    return dt.strftime("%H:%M")

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
        height=400,
        showlegend=False,
    )
    return fig

# 모드 1: 자는 시간 → 기상 시간 추천
if mode.startswith("자러"):
    sleep_input = st.time_input("🕒 자러 가는 시간 선택", value=datetime.strptime("23:00", "%H:%M").time(), key="sleep_time")

    if st.button("기상 시간 계산"):
        now = datetime.now()
