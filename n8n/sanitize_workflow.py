# -*- coding: utf-8 -*-
"""n8n 에서 내보낸 워크플로 JSON 의 비밀값을 <REDACTED> 로 치환한다.

사용법:  python sanitize_workflow.py "My workflow.json"
결과:    workflow.json  (같은 폴더에 생성)
"""
import json
import re
import sys

SRC = sys.argv[1] if len(sys.argv) > 1 else 'My workflow.json'
DST = 'workflow.json'

# 문자열 값 하나를 받아 비밀값이면 가린다
RULES = [
    (re.compile(r'https://hooks\.slack\.com/services/.+'),
     'https://hooks.slack.com/services/<REDACTED>'),
    (re.compile(r'https://discord(?:app)?\.com/api/webhooks/.+'),
     'https://discord.com/api/webhooks/<REDACTED>'),
    (re.compile(r'(https://api\.telegram\.org/bot)[0-9]+:[A-Za-z0-9_\-]+(/.*)?'),
     r'\1<REDACTED>\2'),
]

# JSON 본문(코드/표현식) 안에 박힌 chat_id 같은 값
INLINE = [
    (re.compile(r'("chat_id"\s*:\s*")[0-9]+(")'), r'\1<REDACTED>\2'),
]

SECRET_KEYS = {'x-api-key', 'authorization', 'api_key', 'apikey', 'token'}


def clean_str(s):
    for pat, rep in RULES:
        if pat.fullmatch(s):
            return pat.sub(rep, s)
    for pat, rep in INLINE:
        s = pat.sub(rep, s)
    return s


def walk(node):
    if isinstance(node, dict):
        # 헤더/파라미터 이름이 비밀 키면 값을 통째로 가린다
        name = str(node.get('name', '')).lower()
        if name in SECRET_KEYS and 'value' in node:
            node['value'] = '<REDACTED>'
        for k, v in node.items():
            if isinstance(v, str):
                node[k] = clean_str(v)
            else:
                walk(v)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            if isinstance(v, str):
                node[i] = clean_str(v)
            else:
                walk(v)


data = json.load(open(SRC, encoding='utf-8'))
walk(data)

with open(DST, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f'{DST} 생성 완료 — 업로드 전에 파일을 열어 남은 비밀값이 없는지 눈으로 확인하세요.')
