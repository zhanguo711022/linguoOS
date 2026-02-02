# LinguoOS External Interface Layer

## 启动
```bash
uvicorn linguoos.main:app --reload
```

## 说明
- 当前仅提供 mock 接口层。
- 不包含任何教学逻辑。

## Frontend Quickstart · 3 Calls
访问 `/docs` 作为可视化调试入口，下面 3 次调用即可跑通 Context → Decision → Practice 的最小闭环。

1) 入口与健康检查
- Swagger: `GET /docs`
- Health:
  ```bash
  curl -s http://127.0.0.1:8000/api/v1/system/health
  # {"ok":true}
  ```

2) Context
```bash
curl -s http://127.0.0.1:8000/api/v1/workspace/context
# {"current_module":{"id":"precision.generalization","name":"Generalization"}}
```

3) Decision
```bash
curl -s -X POST http://127.0.0.1:8000/api/v1/decision/next \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","module_id":"precision.generalization","last_mode":"practice","last_correct":false}'
# {"action":"explain","target_module":"precision.generalization"}
```

4) Practice
```bash
curl -s "http://127.0.0.1:8000/api/v1/practice/next?module_id=precision.generalization"
# {"mode":"practice","module_id":"precision.generalization"}
```

## Workspace · Minimal Web UI
- 打开 http://127.0.0.1:8000/ui 体验最小工作台
- 打开： http://127.0.0.1:8000/ui
- 按按钮顺序 A → B → C1 → C2 → D → E 即可看到闭环（或用 “Alt. Demo Flow” 一键查看）

## System API
- 健康检查：GET /api/v1/system/health
- 版本号：GET /api/v1/system/version

## v0.2 · Observability pack
- 结构化日志（JSON 行）默认开启：
  ```json
  {"event":"request_start","method":"GET","path":"/api/v1/system/status","rid":"..."}
  {"event":"request_end","method":"GET","path":"/api/v1/system/status","rid":"...","status":200,"dur_ms":2}
  ```
- 统一错误返回示例：
  ```json
  {"ok":false,"error":{"type":"http_error","status":404,"message":"Not Found"}}
  ```
- System 状态与指标：
  ```bash
  curl -s http://127.0.0.1:8000/api/v1/system/status
  curl -s http://127.0.0.1:8000/api/v1/system/metrics
  ```
- Web UI：打开 http://127.0.0.1:8000/ui 后点击 “System Status / System Metrics”。

### v0.2 自测方法
```bash
curl -s http://127.0.0.1:8000/api/v1/system/status
curl -s http://127.0.0.1:8000/api/v1/system/metrics
```

## CORS
- 为前端联调临时全放开跨域（allow_origins=["*"] 等）。

## Auth (X-API-Key)
- 开启方式：
  ```bash
  LINGUO_REQUIRE_API_KEY=1 LINGUO_API_KEY=your-key
  ```
- 请求示例（curl）：
  ```bash
  curl -H "X-API-Key: your-key" http://127.0.0.1:8000/api/v1/system/health
  ```

## Orchestrator Skeleton
- 提供教学调度中枢与 Agent 接口占位。
- 仅包含可扩展的空壳实现，不包含任何教学规则或业务逻辑。

## Precision Spine
- Precision 维度的内容骨架与模块注册表，仅提供静态数据与只读查询接口。

### GET /api/v1/precision/modules
响应（示例）：
```json
[
  {
    "module_id": "precision.generalization",
    "name": "Generalization",
    "description": "Over-broad claims without limits.",
    "error_type": "generalization",
    "prerequisites": [],
    "mastery_condition": {}
  }
]
```

## Explain API

### GET /api/v1/explain/concept
/explain/concept 现由 ExplainAgent.explain(module_id) 提供占位讲解（外部契约不变）
响应（示例）：
```json
{
  "title": "Generalization",
  "one_liner": "SAT favors specific, verifiable claims over broad generalizations.",
  "structure_template": ["Scope", "Object", "Measurable evidence"],
  "example": "In Grade 10, average scores rose 12% after a 4-week program.",
  "return_to": "practice"
}
```

## Demo Flow API

### GET /api/v1/demo/flow
示例：
```
GET /api/v1/demo/flow?module_id=precision.generalization&wrong_first=true
```

说明：
- 返回 steps 数组，依次包含 decision_1、practice_next、practice_submit、decision_2（如需则有 explain_concept）。

## Decision API

### POST /api/v1/decision/next
请求：
```json
{
  "user_id": "u1",
  "module_id": "precision.generalization",
  "last_mode": "practice",
  "last_correct": false
}
```

响应：
```json
{
  "action": "explain",
  "target_module": "precision.generalization",
  "reason": "placeholder"
}
```

## Profile API

### GET /api/v1/profile/current
请求：
```bash
curl "http://localhost:8000/api/v1/profile/current?user_id=demo-user"
```

响应：
```json
{
  "user_id": "demo-user",
  "language": "en",
  "current_stage": 2,
  "ability_dimensions": {
    "precision": {"level": 70, "trend": "steady", "last_updated": "2024-01-01T00:00:00Z"},
    "structure": {"level": 65, "trend": "up", "last_updated": "2024-01-01T00:00:00Z"},
    "logic": {"level": 60, "trend": "steady", "last_updated": "2024-01-01T00:00:00Z"},
    "usage": {"level": 72, "trend": "up", "last_updated": "2024-01-01T00:00:00Z"},
    "sound": {"level": 55, "trend": null, "last_updated": "2024-01-01T00:00:00Z"}
  }
}
```

### POST /api/v1/profile/update
请求：
```bash
curl -X POST "http://localhost:8000/api/v1/profile/update" \
  -H "Content-Type: application/json" \
  -d '{"user_id":"demo-user","current_stage":3}'
```

响应：
```json
{"ok": true}
```

## Workspace Context API

### GET /api/v1/workspace/context
请求：
```bash
curl "http://localhost:8000/api/v1/workspace/context"
```

响应：
```json
{
  "current_module": {
    "id": "precision.generalization",
    "name": "Generalization"
  },
  "ability_snapshot": {
    "stage": 2,
    "core_issue": "precision",
    "dimensions": {
      "precision": {"level": 54, "trend": "up"},
      "structure": {"level": 68, "trend": "steady"}
    }
  },
  "allowed_actions": ["submit_task", "continue_practice"]
}
```

## Practice API

### GET /api/v1/practice/next?module_id=precision.generalization
/practice/next 现在通过 PracticeAgent.generate_item() 返回占位题目（外部契约不变）

### POST /api/v1/practice/submit
请求体：TaskSubmissionRequest

响应体：FeedbackResponse

## Correction API

### POST /api/v1/correction/review
请求：
```bash
curl -X POST "http://localhost:8000/api/v1/correction/review" \
  -H "Content-Type: application/json" \
  -d '{"text":"The program improved scores for everyone.","module_id":"precision.generalization"}'
```

响应（示例）：
```json
{
  "mode": "feedback",
  "core_issue": "precision",
  "blocks": [
    {"type": "error_type", "content": "generalization"},
    {"type": "why", "content": "The claim is broad and not verifiable."},
    {"type": "example", "content": "Average scores increased by 12% after 4 weeks."},
    {"type": "how_to_avoid", "content": "Constrain scope and use measurable evidence."}
  ],
  "next_action": "continue_practice"
}
```
