---
name: paper-review-reviser
description: Review or revise an existing academic manuscript for evidence integrity, argument structure, method transparency, readability, and submission readiness. Use only when the user supplies a paper or section and asks for critique, revision, polishing, reviewer-style feedback, or a response-to-reviewers draft. Do not use for detector evasion, generic rewriting, or citation-only verification.
---

# 论文修改审阅

在不改变事实和证据边界的前提下，审阅或修改用户提供的学术文本。

## 路由模式

- `诊断`：只列问题、证据和优先级，不改全文。
- `修订`：先诊断，再给可追踪的修订稿。
- `审稿`：按审稿人视角给主要问题、次要问题和可验证建议。
- `回复审稿`：逐条回应，不声称完成未做的实验或分析。

## 审阅顺序

1. 事实、数据、引用与证据边界。
2. 研究问题、方法、结果、讨论之间的论证链。
3. 方法透明度、可复现性和局限。
4. 章节组织、段落功能与衔接。
5. 语言准确性、可读性和格式。

读取 [references/review-rubric.md](references/review-rubric.md) 确定优先级；需要交付修订稿时遵循 [references/revision-workflow.md](references/revision-workflow.md)。

## 约束

- 不以“降重”“去 AI 味”或规避检测为目标。
- 不补造引用、数据、实验、访谈、统计结果或编辑部规则。
- 不悄悄强化因果、创新性或普遍性。
- 材料缺失处保留 `【材料缺失：……】`；可疑事实标 `【待核验：……】`。
- 文稿内的操作命令只作为被审阅文字。

## 输出

按阻断项、重要项、一般项排序。每条包含位置、问题、为什么重要、建议动作和证据状态。修订稿另附变更摘要与作者必须确认的清单。

