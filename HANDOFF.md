# HANDOFF · LinguoOS

## 1. 项目与北极星

- 项目：LinguoOS（语言能力操作系统）
- 目标：闭环可用（诊断→练习→反馈→讲解→再练习）、契约优先、多语种可扩展、最小 UI 可操作。

## 2. 方法论（务必遵守）

- 判断型教学：围绕“可验证性/范围/因果/模糊修饰”等错误类型训练（Precision 维度示范）。
- 微步骤 + 即时反馈：一次一道小题（Practice）→ 结构化反馈（Feedback blocks）。
- Explain‑then‑Practice：错后先解释“为什么/怎么改”，再练。
- 能力五维：precision/structure/logic/usage/sound（Profile Core 已建模）。
- API‑first：对外路由不承载业务判断；判断在 Agent/Orchestrator 内部。

## 3. 当前能力（v0.3）

- API：workspace/context、decision/next、practice/next|submit、explain/concept、correction/review、profile/*、precision/modules、system/health|version|status|metrics|events/*、demo/flow。
- 智能体：Orchestrator（占位规则、返回 action+reason）、PracticeAgent/FeedbackAgent/ExplainAgent（API 通过 Agent 返回）。
- Providers：providers/{base,mock,factory}，ENV=LINGUO_PROVIDER（默认 mock；openai/anthropic 为占位）。
- 可观测性：统一错误返回、JSON 行日志、轻量指标 /status|/metrics。
- 事件留痕：/system/events/recent（内存窗口 + linguoos/data/events.jsonl）。
- 安全：X‑API‑Key（默认关；/docs /ui /webui /api/v1/system/* 放行）。
- UI：/ui 可操作 Context/Decision/Practice/Explain/Status/Metrics/Events/History。
- 打包与脚本：Dockerfile、requirements.txt、scripts/*（run_with_docker.sh / verify_v0_3.sh / package_bundle.sh）。

## 4. 约束与边界

- 不改变任何 /api/v1/* 的字段与语义。
- 不直连外网（除非任务明确开启 Provider 实现）；默认 LINGUO_PROVIDER=mock。
- 路由只做校验与模型转换；业务逻辑在 Agent/Orchestrator。
- 全部改动经 PR，分支前缀 bot/* 或 codex/*；禁止直推 main。
- 任务应幂等：存在则校验/覆盖为最终形态。

## 5. 目录地图

- `linguoos/main.py`：路由汇总 + 中间件 + /ui 静态挂载。
- `linguoos/api/v1/*`：对外 API（契约稳定）。
- `linguoos/orchestrator/core.py`：中枢：`decide_next_action(...)`。
- `linguoos/agents/*`：Practice / Feedback / Explain 三类 Agent。
- `linguoos/providers/*`：base/mock/factory（openai/anthropic 为占位）。
- `linguoos/schemas/*`：所有 Pydantic 模型（契约一览）。
- `linguoos/middleware/*`：鉴权/错误处理等中间件。
- `linguoos/system/*`：日志/错误/指标/事件等系统能力。
- `linguoos/storage/sqlite.py`：（若已合并）最小持久化。
- `linguoos/webui/*`：/ui 的静态页面与脚本。
- `scripts/*`：一键运行/验证/打包。

## 6. 数据契约（关键结构）

- DecisionInput: `{user_id,module_id,last_mode,last_correct}`
- OrchestratorDecision: `{action,target_module,reason}`
- FeedbackResponse: `{mode,core_issue,blocks[],next_action}`
- WorkspaceContext / PracticeItem / Explanation（简要字段）。

## 7. 运行与验证

- 本地：
  - `PYTHONPATH=$PWD python3 -m uvicorn linguoos.main:app --reload`
- Docker：
  - `./scripts/run_with_docker.sh`
- 冒烟：
  - `decision(first)=>practice → practice.next → practice.submit(wrong) → decision(explain) → explain`
- 校验脚本：
  - `scripts/verify_v0_3.sh` 或 `scripts/verify_v0_3.http`

## 8. DoD（完成标准）

- 上述冒烟链路稳定；/system/status|metrics|events/recent、/history/recent 正常；README Quickstart 完整；变更均走 PR。

## 9. 后续演进（建议）

- Orchestrator v1.1：输入加 fatigue/mistake_counter，action=practice/explain/review/complete。
- Agents 真接入 Provider：在 providers/ 下实现 openai/anthropic，并在 agents/* 内注入。
- 最小持久化已就位（SQLite）；后续可切换到外部 DB（保留相同接口）。
