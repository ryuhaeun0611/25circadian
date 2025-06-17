import streamlit as st
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.title("🧠 맞춤형 서카디안 리듬 시각화")

# --- 사용자 입력 ---
st.subheader("🛏️ 수면 정보 입력")
sleep_time = st.time_input("취침 시간", value=datetime.strptime("23:00", "%H:%M").time())
wake_time = st.time_input("기상 시간", value=datetime.strptime("07:00", "%H:%M").time())

# --- 시간 계산 함수 ---
def get_hour_float(t):
    return t.hour + t.minute / 60

def adjust_hours_range(start, end):
    """수면 시간이 자정을 넘길 경우를 고려한 시간 범위 반환"""
    if end < start:
        return [(h % 24) for h in np.arange(start, end + 24, 0.1)]
    else:
        return list(np.arange(start, end, 0.1))

# --- 서카디안 리듬 모델 (cos 기반) ---
base_hours = np.arange(0, 24, 0.1)
# 사용자의 기상 시간 기준 위상 이동
user_wake_hour = get_hour_float(wake_time)
peak_shift = (user_wake_hour + 7) % 24  # 기상 후 7시간 후 최고 각성

# 코사인 함수 기반 각성도: 최고점은 15시
adjusted_hours = (base_hours - peak_shift + 15) % 24
alertness = np.cos((adjusted_hours - 15) / 12 * np.pi)

# --- Plotly 그래프 ---
fig = go.Figure()

# 각성도 곡선
fig.add_trace(go.Scatter(
    x=base_hours,
    y=alertness,
    mode='lines',
    name='서카디안 리듬 (각성도)',
    line=dict(color='orange')
))

# 수면 시간 음영 처리
sleep_start = get_hour_float(sleep_time)
sleep_end = get_hour_float(wake_time)

shaded_hours = adjust_hours_range(sleep_start, sleep_end)

fig.add_trace(go.Scatter(
    x=shaded_hours + shaded_hours[::-1],
    y=[-1.2]*len(shaded_hours) + [1.2]*len(shaded_hours),
    fill='toself',
    fillcolor='rgba(0, 100, 255, 0.2)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name='수면 시간대'
))

# --- 그래프 레이아웃 설정 ---
fig.update_layout(
    title="서카디안 리듬 예측 (맞춤형)",
    xaxis=dict(title="시간 (시)", tickmode='array', tickvals=list(range(0, 25, 3))),
    yaxis=dict(title="각성도", range=[-1.2, 1.2]),
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)
