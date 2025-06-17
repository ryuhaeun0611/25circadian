import streamlit as st
import numpy as np
import plotly.graph_objs as go
from datetime import datetime, timedelta

# --- 앱 제목 및 설명 ---
st.title("🧠 맞춤형 서카디안 리듬 시각화")

st.markdown("""
### 서카디안 리듬(각성도)이란?
**서카디안 리듬(각성도)**는 생체 시계에 따라 뇌의 **깨어 있음과 집중력 수준**을 나타냅니다.  
- **각성도(값)가 높을수록**: 집중력, 에너지, 반응 속도 ↑  
- **각성도(값)가 낮을수록**: 졸림, 피로감, 사고 위험 ↑  
이 리듬은 일반적으로 기상 후 약 7시간 후에 최고조에 도달하고, 밤에는 자연스럽게 감소합니다.
""")

# --- 사용자 입력 ---
st.subheader("🛏️ 수면 정보 입력")
sleep_time = st.time_input("취침 시간", value=datetime.strptime("23:00", "%H:%M").time())
wake_time = st.time_input("기상 시간", value=datetime.strptime("07:00", "%H:%M").time())

# --- 보조 함수 ---
def get_hour_float(t):
    return t.hour + t.minute / 60

def adjust_hours_range(start, end):
    """자정을 넘길 경우 시간대를 0~24로 정규화"""
    if end < start:
        return list(np.arange(start, 24, 0.1)) + list(np.arange(0, end, 0.1))
    else:
        return list(np.arange(start, end, 0.1))

def wrap_hour(h):
    """24시간 안으로 정규화"""
    return h % 24

# --- 시간 계산 ---
sleep_start = get_hour_float(sleep_time)
sleep_end = get_hour_float(wake_time)
wake_hour = sleep_end  # 기상 시간

# --- 서카디안 리듬 모델 ---
base_hours = np.arange(0, 24, 0.1)
peak_shift = (wake_hour + 7) % 24
adjusted_hours = (base_hours - peak_shift + 15) % 24
alertness = np.cos((adjusted_hours - 15) / 12 * np.pi)

# --- Plotly 그래프 생성 ---
fig = go.Figure()

# 서카디안 리듬 곡선
fig.add_trace(go.Scatter(
    x=base_hours,
    y=alertness,
    mode='lines',
    name='서카디안 리듬 (각성도)',
    line=dict(color='orange')
))

# 1. 수면 시간 음영 처리
sleep_range = adjust_hours_range(sleep_start, sleep_end)
fig.add_trace(go.Scatter(
    x=sleep_range + sleep_range[::-1],
    y=[-1.2]*len(sleep_range) + [1.2]*len(sleep_range),
    fill='toself',
    fillcolor='rgba(0, 100, 255, 0.15)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name='수면 시간대'
))

# 2. 멜라토닌 분비 시간 (수면 2시간 전 ~ 취침 시각)
melatonin_start = wrap_hour(sleep_start - 2)
melatonin_end = sleep_start
melatonin_range = adjust_hours_range(melatonin_start, melatonin_end)
fig.add_trace(go.Scatter(
    x=melatonin_range + melatonin_range[::-1],
    y=[-1.2]*len(melatonin_range) + [1.2]*len(melatonin_range),
    fill='toself',
    fillcolor='rgba(150, 0, 200, 0.1)',
    line=dict(color='rgba(255,255,255,0)'),
    hoverinfo="skip",
    showlegend=True,
    name='멜라토닌 분비 예상 시간'
))

# 3. 활동 추천 시간대
# - 오전 집중 구간: 기상 후 2~4시간
# - 오후 집중 구간: 기상 후 7~9시간
focus_blocks = [(wake_hour + 2, wake_hour + 4), (wake_hour + 7, wake_hour + 9)]
for i, (start, end) in enumerate(focus_blocks):
    focus_range = adjust_hours_range(wrap_hour(start), wrap_hour(end))
    fig.add_trace(go.Scatter(
        x=focus_range + focus_range[::-1],
        y=[-1.2]*len(focus_range) + [1.2]*len(focus_range),
        fill='toself',
        fillcolor='rgba(0, 200, 100, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=(i == 0),
        name='활동 추천 시간대'
    ))

# --- 그래프 설정 ---
fig.update_layout(
    title="⏰ 당신의 하루 각성도 예측 (서카디안 리듬 기반)",
    xaxis=dict(title="시간 (시)", tickmode='array', tickvals=list(range(0, 25, 3))),
    yaxis=dict(title="각성도", range=[-1.2, 1.2]),
    template='plotly_white',
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5)
)

st.plotly_chart(fig, use_container_width=True)
