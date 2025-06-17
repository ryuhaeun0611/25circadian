import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="나의 생체리듬 집중력 리포트", layout="wide")
st.title("🌙 나의 생체리듬 집중력 리포트")


# --- 사용자 입력 (수면 습관) ---
st.sidebar.header("🕒 수면 습관 입력 (예: 23:30)")

def parse_time(t_str):
    try:
        return datetime.strptime(t_str, "%H:%M").time()
    except:
        st.error("❌ 시간 형식이 올바르지 않습니다. 예: 23:30")
        st.stop()

sleep_time = parse_time(st.sidebar.text_input("취침 시간", "23:30"))
wake_time = parse_time(st.sidebar.text_input("기상 시간", "07:00"))
school_time = parse_time(st.sidebar.text_input("학교 시작 시간", "08:00"))

# --- 수면 시간 계산 ---
def calculate_sleep_duration(sleep_t, wake_t):
    today = datetime.today()
    sleep_dt = datetime.combine(today, sleep_t)
    wake_dt = datetime.combine(today, wake_t)
    if wake_dt <= sleep_dt:
        wake_dt += timedelta(days=1)
    return (wake_dt - sleep_dt).total_seconds() / 3600

sleep_hours = calculate_sleep_duration(sleep_time, wake_time)
avg_sleep = 7.2  # KOSIS 청소년 평균 수면시간

st.sidebar.markdown(f"🛌 수면 시간: **{sleep_hours:.1f}시간**")
st.sidebar.markdown(f"📊 청소년 평균: **{avg_sleep}시간**")

# --- 수면시간 비교 (Plotly) ---
st.subheader("📊 당신 vs 청소년 평균 수면 시간 비교")

bar_fig = go.Figure(data=[
    go.Bar(name="당신", x=["수면 시간"], y=[sleep_hours], marker_color="cornflowerblue"),
    go.Bar(name="청소년 평균", x=["수면 시간"], y=[avg_sleep], marker_color="lightgreen")
])
bar_fig.update_layout(
    yaxis_title="수면 시간 (시간)",
    barmode="group",
    height=400
)
st.plotly_chart(bar_fig)

# --- 해석 메시지 ---
st.markdown("### 📝 수면 시간 분석")
diff = sleep_hours - avg_sleep

if diff > 0.5:
    st.success(f"✅ 평균보다 {diff:.1f}시간 더 자고 있어요! 생체리듬이 잘 유지되고 있을 가능성이 높습니다.")
elif diff < -0.5:
    st.warning(f"⚠️ 평균보다 {abs(diff):.1f}시간 덜 자고 있어요. 집중력 저하에 주의가 필요해요.")
else:
    st.info("📌 평균 수면 시간과 비슷해요. 꾸준히 유지하는 것이 좋아요!")


# --- 수면 전략 제안 ---
st.subheader("💡 수면 전략 및 집중 팁")

if sleep_hours >= 8:
    st.success("✅ 수면이 충분해요! 생체리듬이 잘 유지되고 있어요.")
elif sleep_hours >= 6:
    st.warning("⚠️ 수면이 약간 부족해요. 집중력 저하에 유의하세요.")
else:
    st.error("🚨 수면이 매우 부족합니다. 아침 집중력, 감정 조절, 기억력에 문제가 생길 수 있어요!")

st.markdown("### 🔍 맞춤 전략 추천")
if sleep_hours < 7:
    st.markdown("- 💤 **낮잠 추천**: 오후 2~3시에 20분 낮잠을 시도해보세요.")
st.markdown("- 🧠 **딥워크 시간**: 오전 10시, 오후 5시에 집중 업무를 배치해보세요.")
st.markdown("- 📵 **수면 위생**: 취침 1시간 전에는 스마트폰 사용을 줄여보세요.")
st.markdown("- 📚 **공부 추천 시간**: 저녁 8~10시, 신체가 안정되고 집중력이 높아져요.")

# --- 학교 시간과 집중력 리듬 비교 ---
school_hour = school_time.hour
if school_hour < 9:
    st.warning("📌 학교 시작 시간이 뇌가 깨어나기 전입니다. 아침 루틴을 단순하게 유지해보세요.")
else:
    st.success("👍 학교 시작 시간이 비교적 리듬과 잘 맞습니다!")
