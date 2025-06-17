import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

st.title("맞춤형 서카디안 리듬 시각화")

# --- 사용자 입력 ---
st.subheader("당신의 수면 정보를 입력해주세요")
sleep_time = st.time_input("취침 시간 (예: 23:00)", value=datetime.strptime("23:00", "%H:%M").time())
wake_time = st.time_input("기상 시간 (예: 07:00)", value=datetime.strptime("07:00", "%H:%M").time())

# 시간 계산
def get_sleep_duration(start, end):
    dt_start = datetime.combine(datetime.today(), start)
    dt_end = datetime.combine(datetime.today(), end)
    if dt_end < dt_start:
        dt_end += timedelta(days=1)
    return (dt_end - dt_start).seconds / 3600

sleep_duration = get_sleep_duration(sleep_time, wake_time)

# --- 서카디안 리듬 모델 ---
# 24시간 기준, 각성도 곡선 (간단한 코사인 함수 사용)
hours = np.arange(0, 24, 0.1)
# 기본 서카디안 리듬 (최고 각성 시점: 오후 3시)
# wake_time을 기준으로 위상을 조정
peak_hour = (wake_time.hour + wake_time.minute/60 + 7) % 24  # 보통 기상 후 7시간 후 최고조
phase_shift = (15 - peak_hour)  # 15시는 기본 최고조
adjusted_hours = (hours + phase_shift) % 24

# 활동도(각성 수준): [-1, 1] 사이 값
alertness = np.cos((adjusted_hours - 15) / 12 * np.pi)  # 최고 각성 시간은 15시 기준

# --- 시각화 ---
st.subheader("당신의 서카디안 리듬 그래프")
fig, ax = plt.subplots()
ax.plot(hours, alertness, label="서카디안 리듬 (각성도)", color="orange")
ax.set_xlabel("시간 (시)")
ax.set_ylabel("각성도 (Alertness)")
ax.set_title("24시간 서카디안 리듬 예측")
ax.set_xticks(np.arange(0, 25, 3))
ax.set_ylim(-1.1, 1.1)
ax.axvspan(sleep_time.hour + sleep_time.minute/60, 
           wake_time.hour + wake_time.minute/60 if wake_time > sleep_time else wake_time.hour + wake_time.minute/60 + 24,
           color='blue', alpha=0.2, label="수면 시간대")

ax.legend()
st.pyplot(fig)

