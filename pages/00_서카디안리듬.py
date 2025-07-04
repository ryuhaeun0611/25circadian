import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="서카디안 리듬과 수면", layout="wide")

st.title("🕒 서카디안 리듬과 수면")
st.markdown("---")

# 1. 서카디안 리듬이란?
st.header("🌞 서카디안 리듬이란?")
st.markdown("""
**서카디안 리듬(circadian rhythm)** 은 약 24시간 주기로 반복되는 생물학적 리듬으로,  
수면, 체온, 호르몬 분비, 소화 등 다양한 생체 기능을 조절합니다.

- 뇌 속 **시교차상핵(SCN)** 이 중심 조절 역할
- **빛(자연광)** 에 의해 리듬 조절
- **멜라토닌** 분비를 통해 수면 유도
""")

# 2. 수면과의 관계
st.header("😴 수면과 서카디안 리듬의 관계")
st.markdown("""
수면은 두 가지 시스템에 의해 조절됩니다:

| 시스템 | 설명 |
|--------|------|
| **서카디안 리듬** | 언제 자고 일어날지를 조절 |
| **수면 항상성** | 얼마나 오래 깨어 있었는지에 따라 수면 욕구 증가 |

---

- 밤이 되면 **멜라토닌**이 분비되어 졸음 유도
- 아침 햇빛은 멜라토닌 분비를 억제하고 **각성 유도**
""")

# 3. 리듬이 깨졌을 때
st.header("⚠️ 서카디안 리듬이 깨질 때 생기는 문제")
st.markdown("""
| 원인 | 결과 |
|------|------|
| 야간 근무 | 피로 누적, 수면 질 저하 |
| 밤샘 활동 | 집중력 저하, 우울감 증가 |
| 스마트폰 과다 사용 | 멜라토닌 억제 → 수면 지연 |
| 시차 적응 실패 | 낮에 졸리고 밤에 각성 |

이런 상태가 지속되면 **불면증, 우울증, 비만, 당뇨** 등의 건강 문제로 이어질 수 있습니다.
""")

# 4. 건강한 수면을 위한 팁
st.header("✅ 건강한 수면과 리듬 유지를 위한 팁")
st.markdown("""
- 🕰️ **일정한 수면 시간 유지** (주말 포함)
- ☀️ **아침 햇빛 쬐기**: 멜라토닌 억제, 리듬 조절
- 💡 **밤엔 조명 낮추기**: 수면 유도
- 📵 **자기 전 스마트폰 금지**
- 🍽️ **규칙적인 식사와 운동**

꾸준한 습관이 **리듬 회복의 핵심**입니다.
""")

# 5. 설문: 서카디안 리듬 유형 체크
st.header("📝 나의 서카디안 리듬 체크")
st.markdown("다음 간단한 문항에 답해 보세요. 당신은 아침형 인간일까요? 저녁형 인간일까요?")

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
        st.success("당신은 **아침형 인간(early chronotype)** 이에요! 아침에 집중력이 좋고, 밤엔 일찍 졸려요.")
    elif score >= 4:
        st.info("당신은 **중간형(mid-type)** 이에요. 일반적인 수면/활동 패턴을 가지고 있어요.")
    else:
        st.warning("당신은 **저녁형 인간(late chronotype)** 이에요! 밤에 더 활발하지만 아침엔 느릴 수 있어요.")

# 6. Plotly 그래프 시각화
st.header("📈 서카디안 리듬 분석 예시 그래프 (Plotly)")

time = np.linspace(0, 24, 100)

melatonin = np.maximum(0, np.sin((time - 21) / 24 * 2 * np.pi))  # 밤에 상승
alertness = np.maximum(0, np.sin((time - 10) / 24 * 2 * np.pi))  # 낮에 상승
body_temp = 0.5 + 0.5 * np.sin((time - 17) / 24 * 2 * np.pi)     # 오후에 최고조
sleep_drive = 1 - alertness                                       # 졸림은 반비례

fig = go.Figure()

fig.add_trace(go.Scatter(x=time, y=melatonin, mode='lines', name='멜라토닌', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=time, y=alertness, mode='lines', name='집중력(각성)', line=dict(color='orange')))
fig.add_trace(go.Scatter(x=time, y=body_temp, mode='lines', name='체온', line=dict(color='green')))
fig.add_trace(go.Scatter(x=time, y=sleep_drive, mode='lines', name='졸림(수면 압력)', line=dict(color='purple')))

fig.update_layout(
    title="서카디안 리듬의 생리적 변화 (예시)",
    xaxis_title="시간 (시)",
    yaxis_title="활성도 (상대 수치)",
    xaxis=dict(tickmode='array', tickvals=list(range(0, 25, 3))),
    template="plotly_white",
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
    margin=dict(t=60, b=60)
)

st.plotly_chart(fig, use_container_width=True)

# 7. 추가 정보
with st.expander("📚 추가 정보: 청소년과 노인의 수면 차이"):
    st.markdown("""
    - **청소년기**에는 멜라토닌 분비 시간이 늦춰져 밤에 늦게 자고 늦게 일어나는 경향이 있어요.
    - **노년기**에는 멜라토닌 분비량이 감소해 **짧고 얕은 수면**을 겪는 경우가 많습니다.
    """)

st.markdown("---")
st.caption("ⓒ 2025 건강한 생활 리듬 프로젝트")
