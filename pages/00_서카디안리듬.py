import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="서카디안 리듬과 수면", layout="wide")

st.title("🕒 서카디안 리듬과 수면")
st.markdown("---")

# 1. 서카디안 리듬 설명
st.header("🌞 서카디안 리듬이란?")
st.markdown("""
**서카디안 리듬(circadian rhythm)** 은 약 24시간 주기로 반복되는 생물학적 리듬입니다.
- 수면, 체온, 호르몬, 소화 등 생체 기능 조절
- **시교차상핵(SCN)** 과 **멜라토닌**이 주요 조절자
- 빛 자극에 의해 동기화됨
""")

# 2. 수면과 서카디안 리듬
st.header("😴 수면과 서카디안 리듬의 관계")
st.markdown("""
수면은 다음 두 시스템이 조절합니다:
- **서카디안 리듬**: 수면 시점 조절 (언제 자야 하는가)
- **수면 항상성**: 수면 압력 조절 (얼마나 졸린가)

밤에는 멜라토닌이 분비되고, 아침 햇빛은 멜라토닌을 억제해 각성을 유도합니다.
""")

# 3. 리듬 붕괴 문제
st.header("⚠️ 리듬이 깨질 때 발생하는 문제")
st.markdown("""
| 원인 | 문제 |
|------|------|
| 야간 근무 | 수면의 질 저하, 피로 누적 |
| 밤샘 작업 | 생체 리듬 붕괴, 집중력 저하 |
| 블루라이트 노출 | 멜라토닌 억제 → 수면 지연 |
""")

# 4. 수면 개선 팁
st.header("✅ 건강한 수면을 위한 팁")
st.markdown("""
- 일정한 수면/기상 시간 유지
- 아침 햇빛 쬐기
- 자기 전 조명 줄이기
- 스마트폰 자제
- 규칙적인 식사, 운동
""")

# 5. 간단한 서카디안 설문
st.header("📝 나의 서카디안 리듬 체크")

score = 0

q1 = st.radio("1. 언제 가장 활력이 느껴지나요?", ["아침", "오후", "저녁"])
if q1 == "아침": score += 2
elif q1 == "오후": score += 1

q2 = st.radio("2. 주말에 자연스럽게 일어나는 시간은?", ["6~8시", "8~10시", "10시 이후"])
if q2 == "6~8시": score += 2
elif q2 == "8~10시": score += 1

q3 = st.radio("3. 밤 11시쯤이면?", ["이미 졸리다", "조금 피곤하다", "정신이 맑다"])
if q3 == "이미 졸리다": score += 2
elif q3 == "조금 피곤하다": score += 1

q4 = st.radio("4. 아침에 일어나자마자?", ["금방 활동 가능", "조금 힘듦", "정말 힘듦"])
if q4 == "금방 활동 가능": score += 2
elif q4 == "조금 힘듦": score += 1

if st.button("📊 결과 보기"):
    st.markdown("### 🔍 결과:")
    if score >= 7:
        st.success("당신은 **아침형 인간(early chronotype)** 이에요!")
    elif score >= 4:
        st.info("당신은 **중간형(mid-type)** 이에요.")
    else:
        st.warning("당신은 **저녁형 인간(late chronotype)** 이에요!")

# 6. 그래프 시각화
st.header("📈 서카디안 리듬 분석 예시 그래프")

time = np.linspace(0, 24, 100)

# 예시 리듬 curves (정규화된 곡선)
melatonin = np.maximum(0, np.sin((time - 21) / 24 * 2 * np.pi))  # 밤에 상승
alertness = np.maximum(0, np.sin((time - 10) / 24 * 2 * np.pi))  # 낮에 상승
body_temp = 0.5 + 0.5 * np.sin((time - 17) / 24 * 2 * np.pi)     # 오후에 최고조
sleep_drive = 1 - alertness                                       # 졸림은 반비례

fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(time, melatonin, label="멜라토닌", color="blue")
ax.plot(time, alertness, label="집중력(각성)", color="orange")
ax.plot(time, body_temp, label="체온", color="green")
ax.plot(time, sleep_drive, label="졸림 (수면 압력)", color="purple")

ax.set_xticks(np.arange(0, 25, 3))
ax.set_xlabel("시간 (시)")
ax.set_ylabel("활성도 (상대)")
ax.set_title("서카디안 리듬의 생리적 변화 (예시)")
ax.legend()
ax.grid(True)

st.pyplot(fig)

# 7. 추가 정보
with st.expander("📚 청소년과 노인의 리듬 변화"):
    st.markdown("""
    - 청소년: 멜라토닌 분비가 늦어져 **밤형 인간**이 되기 쉬움  
    - 노인: 멜라토닌 분비 감소 → **짧고 얕은 수면**
    """)

st.markdown("---")
st.caption("ⓒ 2025 건강한 생활 리듬 프로젝트")
