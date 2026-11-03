# 보안 지표 데이터 계층 — 대시보드와 조회가 함께 쓴다
import pandas as pd

from security_events import get_conn, init_db


def _read(sql):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute(sql)
        cols = [c[0] for c in cur.description]
        return pd.DataFrame(cur.fetchall(), columns=cols)


def load_events():
    return _read("SELECT ts, event_type, layer, actor, detail, outcome FROM security_events ORDER BY ts")


def summary(df):
    """보안 지표 카드 4종."""
    total = len(df)
    blocked = int((df["outcome"] == "blocked").sum())
    injections = int(((df["event_type"] == "injection_blocked") & (df["outcome"] == "blocked")).sum())
    hitl = df[df["event_type"] == "hitl_decision"]
    approvals = int((hitl["outcome"] == "approved").sum())
    approval_rate = (approvals / len(hitl) * 100) if len(hitl) else 0.0
    return {
        "total_events": total,
        "blocked": blocked,
        "injections_blocked": injections,
        "hitl_approval_rate": approval_rate,
    }


def by_layer(df):
    """계층(입력/출력/행동/접근)별 차단 건수."""
    b = df[df["outcome"] == "blocked"]
    return b.groupby("layer").size().rename("차단 건수")


def outcome_dist(df):
    return df.groupby("outcome").size().rename("건수")


def recent_blocks(df, n=15):
    b = df[df["outcome"].isin(["blocked", "rejected"])].sort_values("ts", ascending=False).head(n)
    return b[["ts", "layer", "event_type", "actor", "detail"]]


if __name__ == "__main__":
    # 화면 없이 지표를 확인한다: python security_metrics.py
    import sys

    sys.stdout.reconfigure(encoding="utf-8")  # Windows 콘솔(cp949)에서 한글 출력이 깨지지 않게
    init_db()   # 테이블이 아직 없으면 먼저 만든다
    events = load_events()
    if events.empty:
        print("보안 이벤트가 없습니다. 통합 노트북이나 simulate_security.py를 먼저 실행하세요.")
    else:
        s = summary(events)
        print(f"총 보안 이벤트 {s['total_events']}건 / 차단 {s['blocked']}건 / "
              f"인젝션 차단 {s['injections_blocked']}건 / 사람 승인율 {s['hitl_approval_rate']:.0f}%")
        print("계층별 차단:", by_layer(events).to_dict())
        print("처리 결과:", outcome_dist(events).to_dict())
