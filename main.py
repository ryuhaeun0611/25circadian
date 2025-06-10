import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, time, timedelta

# 페이지 설정
st.set_page_config(page_title="나의 생체리듬 집중력 리포트", layout="wide")

st.title("🌙 나의 생체리듬 집중력 리포트")

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

# 수면 시간 계산 함수
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
avg_sleep = 7.2  # KOSIS 기준 청소년 평균 수면시간
st.sidebar.markdown(f"🔍 국내 청소년 평균 수면 시간: **{avg_sleep:.1f}시간**")

# --- 비교 그래프 ---
st.subheader("📊 당신 vs 청소년 평균 수면 시간 비교")

labels = ['당신', '청소년 평균']
values = [sleep_hours, avg_sleep]

fig2, ax2 = plt.subplots(figsize=(6, 4))
bars = ax2.bar(labels, values, color=['cornflowerblue', 'lightgreen'])
ax2.set_ylim(0, 12)
ax2.set_ylabel("수면 시간 (시간)")
ax2.set_title("🔎 수면시간 비교")
for bar in bars:
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
             f"{bar.get_height():.1f}h", ha='center')
st.pyplot(fig2)

# --- 비교 해석 메시지 ---
st.markdown("### 📝 수면 시간 비교 분석")
diff = sleep_hours - avg_sleep

if diff > 0.5:
    st.success(f"✅ 평균보다 {diff:.1f}시간 더 자고 있어요! 생체리듬이 잘 유지되고 있을 가능성이 높습니다.")
elif diff < -0.5:
    st.warning(f"⚠️ 평균보다 {abs(diff):.1f}시간 덜 자고 있어요. 집중력 저하에 주의가 필요해요.")
else:
    st.info("📌 평균 수면 시간과 비슷해요. 유지하는 게 좋아요!")

# --- 서카디안 리듬 기반 집중력 곡선 ---
def circadian_focus_curve():
    times = [f"{h:02d}:00" for h in range(24)]
    focus = []

    for h in range(24):
        if 9 <= h <= 11:
            score = 90 - abs(10 - h) * 10
        elif 16 <= h <= 18:
            score = 85 - abs(17 - h) * 10
        elif 13 <= h <= 15:
            score = 40  # 낮잠 시간대
        else:
            score = 30 if 0 <= h <= 6 else 50
        focus.append(score)

    df = pd.DataFrame({
        "시간": times,
        "집중력": focus
    })
    return df

focus_df = circadian_focus_curve()

# --- 집중력 시각화 ---
st.subheader("📈 당신의 하루 집중력 곡선 (서카디안 리듬 기준)")
fig, ax = plt.subplots(figsize=(10, 4))
ax.plot(focus_df["시간"], focus_df["집중력"], marker='o', label="집중력")
ax.axvline(school_time.strftime("%H:%M"), color='red', linestyle='--', label="학교 시작 시간")
ax.set_ylabel("집중력 (0~100)")
ax.set_ylim(0, 100)
ax.set_xticks(np.arange(0, 24, 2))
plt.xticks(rotation=45)
plt.legend()
st.pyplot(fig)

# --- 수면 평가 메시지 ---
st.subheader("🧠 수면 분석 및 전략 제안")

if sleep_hours >= 8:
    st.success("✅ 수면이 충분해요! 생체리듬이 잘 유지되고 있어요.")
elif sleep_hours >= 6:
    st.warning("⚠️ 수면이 약간 부족해요. 집중력 저하에 유의하세요.")
else:
    st.error("🚨 수면이 매우 부족합니다. 아침 집중력, 감정 조절, 기억력에 문제가 생길 수 있어요!")

# --- 전략 제안 ---
st.markdown("### 💡 맞춤 집중 전략")

if sleep_hours < 7:
    st.markdown("- 💤 **낮잠 추천**: 오후 2~3시에 20분 낮잠을 자보세요.")
st.markdown("- 🧠 **집중 잘 되는 시간**: 오전 10시, 오후 5시쯤 딥워크에 도전해보세요.")
st.markdown("- 🕹️ **스마트폰 사용**: 취침 1시간 전엔 화면 사용을 줄이면 멜라토닌 분비에 좋아요.")
st.markdown("- 📚 **공부 추천 시간**: 저녁 8~10시, 신체가 안정되고 집중력이 높아져요.")

# --- 학교 시간과 집중력 리듬 비교 ---
school_hour = school_time.hour
if school_hour < 9:
    st.warning("📌 학교 시작 시간이 뇌가 깨어나기 전입니다. 아침 루틴을 단순하게 유지해보세요.")
else:
    st.success("👍 학교 시작 시간이 비교적 리듬과 잘 맞습니다!")
