# 보안 이벤트 모의 발생기 — 대시보드를 빨리 보고 싶을 때만 쓴다
# 실제 방어에서 나온 기록은 Day16 통합 노트북을 실행하면 쌓인다. 이 파일은 "하루치를 압축한 가짜 데이터"다.
# 실행: python simulate_security.py   (이 폴더에서)
import random
import sys

from security_events import init_db, log_event

sys.stdout.reconfigure(encoding="utf-8")  # Windows 콘솔(cp949)에서 한글 출력이 깨지지 않게
random.seed(7)

init_db()

# Day 12 — 입력(인젝션) 방어
for _ in range(12):
    log_event("injection_blocked", "입력", "blocked", actor="user",
              detail=random.choice(["키워드", "LLM 분류기"]))
for _ in range(30):
    log_event("injection_blocked", "입력", "passed", actor="user", detail="정상 입력")

# Day 13 — 출력(가드레일)
for _ in range(5):
    log_event("guardrail_action", "출력", "blocked", detail="Moderation")
for _ in range(8):
    log_event("guardrail_action", "출력", "rewritten", detail=random.choice(["정책 P1", "정책 P2"]))
for _ in range(4):
    log_event("guardrail_action", "출력", "masked", detail="개인정보 전화번호")

# Day 14 — 행동(도구 권한·사람 승인)
for _ in range(6):
    log_event("permission_denied", "행동", "blocked", actor="상담원", detail="delete_account")
for _ in range(9):
    log_event("hitl_decision", "행동", "approved", actor="관리자", detail="refund_order")
for _ in range(3):
    log_event("hitl_decision", "행동", "rejected", actor="관리자", detail="refund_order")

# Day 15 — 접근(역할 × 데이터): 작성자가 자기 글의 검토 결과를 쓰려 한 시도
for _ in range(7):
    log_event("permission_denied", "접근", "blocked", actor="writer", detail="review 칸 쓰기")

print("보안 이벤트 모의 생성 완료 (84건) → python security_metrics.py로 집계하세요.")
