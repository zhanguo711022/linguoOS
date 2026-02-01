# LinguoOS External Interface Layer

## 启动
```bash
uvicorn linguoos.main:app --reload
```

## 说明
- 当前仅提供 mock 接口层。
- 不包含任何教学逻辑。

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

### POST /api/v1/practice/submit
请求体：TaskSubmissionRequest

响应体：FeedbackResponse
