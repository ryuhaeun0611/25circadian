import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# 페이지 설정
st.set_page_config(page_title="나의 생체리듬 집중력 리포트", layout="wide")
st.title("🌙 나의 생체리듬 집중력 리포트 (Plotly 기반)")

# --- 사용자 직접 입력 ---
st.sidebar.header("🕒 당신의 수면 습관을 입력해주세요 (예: 23:30)")

sleep_time_str = st.sidebar.text_input("취침 시간", "23:30")
wake_time_str = st.sidebar.text_input("기상 시간", "07:00")
school_time_str = st.sidebar.text_input("학교 시작 시간", "08:00")

def parse_time_str(t_str):
    try:
        return datetime.strptime(t_str, "%H:%M").time()
    except ValueError:
        st.error(f"❌ 시간 형식이 올바르지 않습니다: '{t_str}' (예: 23:30)")
        st.stop()

sleep_time = parse_time_str(sleep_time_str)
wake_time = parse_time_str(wake_time_str)
school_time = parse_time_str(school_time_str)

# 수면 시간 계산
def calculate_sleep_duration(sleep_t, wake_t):
    sleep_dt = datetime.combine(datetime.today(), sleep_t)
    wake_dt = datetime.combine(datetime.today(), wake_t)
    if wake_dt <= sleep_dt:
        wake_dt += timedelta(days=1)
    duration = wake_dt - sleep_dt
    return duration.total_seconds() / 3600  # hours

sleep_hours = calculate_sleep_duration(sleep_time, wake_time)
st.sidebar.markdown(f"🛌 평균 수면 시간: **{sleep_hours:.1f}시간**")

# --- 청소년 평균 수면시간과 비교 ---
avg_sleep = 7.2  # KOSIS 기준
st.sidebar.markdown(f"🔍 국내 청소년 평균 수면 시간: **{avg_sleep:.1f}시간**")

# --- 수면시간 비교 그래프 (Plotly) ---
st.subheader("📊 당신 vs 청소년 평균 수면 시간 비교")

bar_fig = go.Figure(data=[
    go.Bar(name='당신', x=['수면시간'], y=[sleep_hours], marker_color='cornflowerblue'),
    go.Bar(name='청소년 평균', x=['수면시간'], y=[avg_sleep], marker_color='lightgreen')
])
bar_fig.update_layout(
    yaxis=dict(title='수면 시간 (시간)', range=[0, 12]),
    barmode='group',
    title="🔎 수면시간 비교",
    height=400
)
st.plotly_chart(bar_fig)

# --- 비교 해석 메시지 ---
st.markdown("### 📝 수면 시간 비교 분석")
diff = sleep_hours - avg_sleep

if diff > 0.5:
    st.success(f"✅ 평균보다 {diff:.1f}시간 더 자고 있어요! 생체리듬이 잘 유지되고 있을 가능성이 높습니다.")
elif diff < -0.5:
    st.warning(f"⚠️ 평균보다 {abs(diff):.1f}시간 덜 자고 있어요. 집중력 저하에 주의가 필요해요.")
else:
    st.info("📌 평균 수면 시간과 비슷해요. 유지하는 게 좋아요!")

# --- 서카디안 리듬 집중력 곡선 생성 ---
def circadian_focus_curve():
    hours = list(range(24))
    times = [f"{h:02d}:00" for h in hours]
    focus = []

    for h in hours:
        if 9 <= h <= 11:
            score = 90 - abs(10 - h) * 10
        elif 16 <= h <= 18:
            score = 85 - abs(17 - h) * 10
        elif 13 <= h <= 15:
            score = 40
        else:
            score = 30 if 0 <= h <= 6 else 50
        focus.append(score)

    return pd.DataFrame({'시간': times, '집중력': focus})

focus_df = circadian_focus_curve()

# --- Plotly 라인차트로 시각화 ---
st.subheader("📈 당신의 하루 집중력 곡선 (서카디안 리듬 기준)")

focus_fig = go.Figure()

focus_fig.add_trace(go.Scatter(
    x=focus_df["시간"], y=focus_df["집중력"],
    mode='lines+markers', name='집중력',
    line=dict(color='royalblue')
))

focus_fig.add_vline(
    x=school_time.strftime("%H:%M"),
    line_dash="dash", line_color="red",
    annotation_text="학교 시작 시간", annotation_position="top right"
)

focus_fig.update_layout(
    yaxis=dict(title="집중력 (0~100)", range=[0, 100]),
    xaxis=dict(title="시간대", tickangle=45),
    height=450
)
st.plotly_chart(focus_fig)

# --- 수면 평가 메시지 ---
st.subheader("🧠 수면 분석 및 전략 제안")

if sleep_hours >= 8:
    st.success("✅ 수면이 충분해요! 생체리듬이 잘 유지되고 있어요.")
elif sleep_hours >= 6
