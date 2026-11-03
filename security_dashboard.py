# 보안 운영 대시보드 — 실행: uv run streamlit run security_dashboard.py
import streamlit as st

from security_events import init_db
from security_metrics import by_layer, load_events, outcome_dist, recent_blocks, summary

init_db()   # 테이블이 아직 없으면 먼저 만든다 (실패해도 경고만)

st.set_page_config(page_title="AI 서비스 — 보안 대시보드", layout="wide")
st.title("AI 서비스 — 보안 운영 대시보드")


@st.cache_data(ttl=5)
def load():
    return load_events()


df = load()
if df.empty:
    st.warning("보안 이벤트가 없습니다. 통합 노트북이나 simulate_security.py를 먼저 실행하세요.")
    st.stop()

# 1. 지표 카드
s = summary(df)
c1, c2, c3, c4 = st.columns(4)
c1.metric("총 보안 이벤트", f"{s['total_events']}건")
c2.metric("차단", f"{s['blocked']}건")
c3.metric("인젝션 차단", f"{s['injections_blocked']}건")
c4.metric("사람 승인율", f"{s['hitl_approval_rate']:.0f}%")

# 2. 계층별 차단
st.subheader("계층별 차단 건수 (입력/출력/행동/접근)")
st.bar_chart(by_layer(df))

# 3. 처리 결과 분포
st.subheader("처리 결과 분포")
st.bar_chart(outcome_dist(df))

# 4. 최근 차단·거부
st.subheader("최근 차단·거부 이벤트")
st.dataframe(recent_blocks(df), width="stretch")  # 화면 폭에 맞춘다 (use_container_width는 폐기 예정)
