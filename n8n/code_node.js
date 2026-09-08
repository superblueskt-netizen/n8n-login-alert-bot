// n8n Code 노드 (JavaScript) — 경보 판정
// Mode: Run Once for All Items

// ── 설정: 거부 기준은 여기 하나만 바꾸면 판정이 바뀐다 ──
const DENY_LEVEL   = 10;   // 이 값 이상이면 거부(deny)
const MEDIUM_LEVEL = 7;    // 이 값 이상이면 Medium

const payload = $input.first().json;
const body    = payload.body ?? payload;      // Webhook 은 body 안에 들어온다
const student = body.student ?? 'unknown';
const alerts  = body.alerts  ?? [];

// 경보 1건 = 아이템 1개로 펼친다
return alerts.map((a) => {
  const level = Number(a.level);

  let severity, decision;
  if (level >= DENY_LEVEL) {
    severity = 'High';   decision = 'deny';
  } else if (level >= MEDIUM_LEVEL) {
    severity = 'Medium'; decision = 'allow';
  } else {
    severity = 'Low';    decision = 'allow';
  }

  return {
    json: {
      student,
      src_ip:     a.ip,
      level,
      rule:       String(a.rule),
      fail_count: Number(a.fail_count ?? 0),
      severity,
      decision,
      reason:     `level ${level} (rule ${a.rule}) → ${decision}`,
    },
  };
});
