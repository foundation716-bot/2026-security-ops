# 보안 이벤트 이력 — Day 12~15 방어가 발동할 때마다 여기에 남긴다
# (M2 Day 11 이력 테이블의 보안판 — 같은 비치명 원칙: 기록이 실패해도 서비스는 계속)
import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

# 이벤트 유형 (event_type)과 계층 (layer)
#   injection_blocked  입력  Day 12 입력 검증        outcome: blocked / passed
#   guardrail_action   출력  Day 13 출력 가드레일    outcome: passed / masked / warned / rewritten / blocked
#   hitl_decision      행동  Day 14 사람 승인        outcome: approved / rejected
#   permission_denied  행동  Day 14 도구 권한        outcome: blocked
#   permission_denied  접근  Day 15 데이터 권한      outcome: blocked
CREATE_SQL = """
CREATE TABLE IF NOT EXISTS security_events (
    id          SERIAL PRIMARY KEY,
    ts          TIMESTAMPTZ NOT NULL DEFAULT now(),
    event_type  TEXT NOT NULL,
    layer       TEXT NOT NULL,      -- 입력/출력/행동/접근
    actor       TEXT,               -- 역할·사용자
    detail      TEXT,               -- 무엇을 막았나
    outcome     TEXT NOT NULL
);
"""


def get_conn():
    """DB 연결을 새로 연다. 매번 새로 열어 DB가 돌아오면 저절로 다시 붙는다 (Day 11)."""
    return psycopg2.connect(os.environ["DATABASE_URL"], connect_timeout=2)


def init_db():
    """테이블을 만든다. DB가 없어도 서비스는 뜨게 경고만 남긴다 (Day 11 비치명 원칙)."""
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(CREATE_SQL)
    except Exception as exc:  # noqa: BLE001
        print(f"[경고] 보안 이벤트 테이블 준비 실패: {exc}")


def clear_events():
    """데모를 처음부터 다시 할 때만 쓴다. 운영 중에는 기록을 지우지 않는다."""
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("TRUNCATE security_events")


def log_event(event_type, layer, outcome, actor=None, detail=None):
    """보안 이벤트 한 건 기록. 비치명적(실패해도 서비스는 계속)."""
    try:
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO security_events (event_type, layer, actor, detail, outcome) "
                "VALUES (%s, %s, %s, %s, %s)",
                (event_type, layer, actor, detail, outcome),
            )
    except Exception as exc:  # noqa: BLE001
        print(f"[경고] 보안 이벤트 기록 실패: {exc}")
