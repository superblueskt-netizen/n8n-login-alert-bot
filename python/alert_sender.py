# -*- coding: utf-8 -*-
"""
alert_sender.py  —  과제 1: 파이썬 전송기
경보 목록을 만들어 n8n Webhook 으로 POST 한다.
"""

import json
import requests

# ─────────────────────────────────────────────
# 설정 (바꿀 값은 전부 여기 위에만 있다)
# ─────────────────────────────────────────────
STUDENT = "장성혁"                                              # 본인 식별자 (채점 증적)
N8N_WEBHOOK_URL = "http://localhost:5678/webhook-test/security-alert"  # n8n Webhook 주소
TIMEOUT_SEC = 10                                                # 전송 대기 시간(초)

# 보낼 경보 목록
# level >= 10  → 거부(deny) 대상,  level < 10 → 허용(allow) 대상
ALERTS = [
    {"ip": "1.2.3.114",    "level": 10, "rule": "5712", "fail_count": 8},   # 거부될 것
    {"ip": "192.168.0.10", "level": 3,  "rule": "5501", "fail_count": 1},   # 허용될 것
]


def build_payload():
    """n8n 으로 보낼 JSON 본문을 만든다."""
    return {
        "student": STUDENT,
        "alerts": ALERTS,
    }


def send(payload):
    """Webhook 으로 POST. 실패해도 프로그램이 죽지 않고 오류 메시지만 출력한다."""
    try:
        res = requests.post(
            N8N_WEBHOOK_URL,
            json=payload,                 # Content-Type: application/json 자동 설정
            timeout=TIMEOUT_SEC,
        )
        print(f"[n8n] POST {N8N_WEBHOOK_URL} -> {res.status_code}")
        if res.text:
            print(f"[n8n] 응답: {res.text[:300]}")
        return True

    except requests.exceptions.ConnectTimeout:
        print(f"[오류] n8n 접속 시간 초과 ({TIMEOUT_SEC}초): {N8N_WEBHOOK_URL}")
    except requests.exceptions.ConnectionError:
        print(f"[오류] n8n 에 연결할 수 없음. 컨테이너가 켜져 있는지 확인: {N8N_WEBHOOK_URL}")
    except requests.exceptions.Timeout:
        print(f"[오류] 응답 대기 시간 초과 ({TIMEOUT_SEC}초)")
    except requests.exceptions.RequestException as e:
        print(f"[오류] 전송 실패: {e}")
    return False


def main():
    payload = build_payload()
    print("[보낼 내용]")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("-" * 50)
    send(payload)


if __name__ == "__main__":
    main()
