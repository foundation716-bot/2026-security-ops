# Day 16 실습 키트 — 보안 운영 체계 (M3·과정 통합)

Day 12~15 방어를 M1 리서치 팀에 입혀 하나의 서비스로 조립하고, 방어가 발동할 때마다 보안 이벤트로 기록해 대시보드로 본다.

## 구성

| 경로 | 내용 | 연결 |
| --- | --- | --- |
| `Day16-보안운영체계·과정통합-실습.ipynb` | 통합 실습 (학생용, TODO 주석 아래를 직접 작성) | 작업 폴더에서 연다 |
| `service_parts.py` | Day 12~15 방어 부품 + M1 팀의 일 (정답 기준) | 노트북이 불러 조립한다 |
| `security_events.py` | 보안 이벤트 테이블·기록 (비치명) | M2 Day 11 이력의 보안판 |
| `security_metrics.py` | 보안 지표 데이터 계층. 직접 실행하면 요약 출력 | M2 Day 11 `dashboard_data.py` 패턴 |
| `security_dashboard.py` | Streamlit 보안 대시보드 | M2 Day 11 대시보드 패턴 |
| `simulate_security.py` | 모의 이벤트 84건 (빠른 데모용 — 실제 방어 기록 아님) | |
| `SECURITY_POLICY.md` | 보안 정책 문서 (위협 모델·통제·운영·점검·사고 대응) | |
| `.env.example` | 복사해 `.env`로 만든다. OpenAI 키, Day 11 DB 주소 | |
| `requirements.txt` | 작업 폴더의 가상환경에 설치할 패키지 (노트북 커널용 `ipykernel` 포함) | |

## 사전 준비 — Day 11 DB

보안 이벤트는 M2 Day 11의 DB에 쌓는다. **Day 11의 DB 컨테이너 하나만** 띄운다. Day 11 키트 폴더에서:

```powershell
docker compose up -d db
```

- Day 11의 app·dashboard 컨테이너는 필요 없다. 특히 dashboard 컨테이너가 떠 있으면 **8501 포트가 겹쳐** Day 16 대시보드 대신 Day 11 화면이 나온다 → Day 11 키트 폴더에서 `docker compose stop app dashboard`
- Docker Desktop에서 프로젝트(`day11-dashboard-lab`) 전체를 ▶로 시작하면 만들어 둔 컨테이너가 모두 뜬다. `db-1` 한 줄만 시작한다

## 실행 순서

작업 폴더 `C:\apps\security-ops-lab`으로 복사해서 실습한다 (Day 8~10과 같은 방식).

```powershell
Copy-Item -Recurse <배포 위치>\day16-security-ops-lab C:\apps\security-ops-lab
cd C:\apps\security-ops-lab
uv venv --python 3.11              # 처음 한 번 — 이 폴더에 .venv
uv pip install -r requirements.txt
copy .env.example .env             # 복사한 뒤 .env에 키와 DB 주소를 넣는다

# 1) VS Code로 이 폴더를 열고 노트북 커널을 이 폴더의 .venv로 골라 실행
#    → 실제 방어 기록이 security_events에 쌓인다
code .
# 2) 화면 없이 지표 확인
uv run python security_metrics.py
# 3) 보안 대시보드 → 브라우저에서 http://localhost:8501
uv run streamlit run security_dashboard.py
```

- 노트북은 같은 폴더의 `service_parts.py`, `security_events.py`를 불러오므로 **이 폴더에서** 연다.
- `.env`는 이 폴더의 것을 읽는다. `KeyError: 'DATABASE_URL'`이 나면 `.env`를 만들지 않았거나 주소가 비어 있는 것이다.

> 노트북 첫 셀이 `clear_events()`로 이전 기록을 비운다 (데모용). 운영 중에는 기록을 지우지 않는다.

모의 데이터로 대시보드만 빨리 보려면:

```powershell
uv run python simulate_security.py
```
