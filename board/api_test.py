# -*- coding: utf-8 -*-
"""과제 4 검증 — 게시판 보안 이벤트 REST API 4가지 경우 확인"""
import json
import requests

BASE = "http://localhost:5000/api/security/events"
API_KEY = "<본인_API_키>"
STUDENT = "장성혁"


def call(title, headers, body):
    print("=" * 60)
    print(f"[{title}]")
    try:
        res = requests.post(BASE, headers=headers, json=body, timeout=10)
        print(f"  상태코드: {res.status_code}")
        print(f"  응답: {res.text}")
    except requests.exceptions.RequestException as e:
        print(f"  [오류] {e}")


ok_body = {
    "student": STUDENT, "src_ip": "1.2.3.114", "decision": "deny",
    "severity": "High", "reason": "level 10 (rule 5712) -> deny", "fail_count": 8,
}

# 1) 키 없음 → 401
call("1. X-API-Key 없이 호출 → 401 기대", {}, ok_body)

# 2) 키 틀림 → 401
call("2. X-API-Key 틀림 → 401 기대", {"X-API-Key": "wrong-key-1234"}, ok_body)

# 3) 필수값 누락 → 400
call("3. student 누락 → 400 기대", {"X-API-Key": API_KEY},
     {"src_ip": "1.2.3.114", "decision": "deny"})

# 4) 정상 → 201
call("4. 정상 요청 → 201 기대", {"X-API-Key": API_KEY}, ok_body)

# 5) 조회
print("=" * 60)
print("[5. GET 조회 (본인 것만, 최신순)]")
r = requests.get(BASE, params={"student": STUDENT}, timeout=10)
print(f"  상태코드: {r.status_code}")
print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:1500])
