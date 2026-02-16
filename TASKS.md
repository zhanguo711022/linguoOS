# TASKS · LinguoOS · 接手即用

## 操作规范

- 任何变更：新分支 → PR → Merge（分支前缀 bot/* 或 codex/*）。
- 绝不改 /api/v1/* 的契约；不直连外网；路由不含判断逻辑。
- 任务需幂等，基于 main HEAD 自检缺啥补啥。

## 即刻执行的任务（A→G）

A) Verify v0.2/v0.3（自检补齐可观测性、Providers 骨架、事件接口、Docker/脚本）。

B) History(SQLite)：练习提交入库 + /history/recent|clear + /ui 两按钮。

C) Agents wiring batch：/practice/next→PracticeAgent；/practice/submit→FeedbackAgent；/explain/concept→ExplainAgent。

D) Orchestrator v1.1：reason 完整（first step / keep momentum / after wrong answer）。

E) Visitor‑ID：请求头 X‑Visitor-Id；UI 自动带；/history 可按 user 过滤。

F) README 刷新：Quickstart/ENV/数据落点。

G) 验证脚本：scripts/verify_v0_3.sh（或 .http）跑通。

## 运行与自测

- 本地：
  - `PYTHONPATH=$PWD python3 -m uvicorn linguoos.main:app --reload`
- UI：
  - `/ui`
- API：
  - `/docs`
- Docker：
  - `./scripts/run_with_docker.sh`
- 一键打包：
  - `./scripts/package_bundle.sh`

## 自动化收尾

- 新建分支：`bot/handoff-and-tasks-docs`
- 在仓库根创建 `HANDOFF.md`、`TASKS.md`，并在 README 顶部插入这两个文档的链接
- 创建指向 main 的 PR（标题：Add HANDOFF.md & TASKS.md links）
- 若允许自动合并则自动合并；否则仅创建 PR
- 最终仅输出两行：状态 + 链接
