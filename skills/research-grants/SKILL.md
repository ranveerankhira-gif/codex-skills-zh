---
name: research-grants
description: 准备、核对或评审明确的科研基金申请材料，覆盖 NSFC、NSF、NIH、DOE、DARPA 和台湾 NSTC 的当年项目指南、申请结构、评审标准、预算说明及重投。仅在用户明确提出科研基金、项目申请书、Specific Aims、基金评审或上述机构时自动调用；不要用于商业提案、融资材料、普通论文写作或自动寻找并提交资助申请。
license: MIT
metadata:
  version: "1.5-safe-cn1"
  upstream: "K-Dense-AI/scientific-agent-skills@a1043ef544e3a100c28e70a736b6cf32554d0677"
---

# 科研基金申请与审计

## 先确定适用规则

每次任务先记录资助机构、项目类别、年度指南或机会编号、修订版本、截止时间与时区、申请资格、当前阶段、页数或字符限制、必交附件、预算规则、评审标准以及官方来源和检索日期。

当年官方项目指南、通知和申请系统说明优先于本 Skill 的参考材料。无法取得官方文件时，只做有边界的结构或内容建议，并列出尚未核验的规则；不得把往年通知、新闻稿、获批案例或模板当成当前有效要求。

## 工作边界

- 只在用户要求的范围内起草、修改或审计；不虚构研究数据、引用、履历、合作承诺、机构资源、伦理批准或预算依据。
- 模板仅是工作底稿，不是官方表格。最终应检查实际导出的 PDF、Word 或系统预览，不能用 Markdown 字数代替页面合规。
- 不登录申请门户、不上传材料、不代替机构提交、不发送邮件，也不创建未经确认的外部账号。
- 不调用付费生图、OpenRouter 或其他外部生成服务。图示如有必要，优先使用本地、可复查的绘图方式，并保持内容由申请人确认。
- 申请人保留研究构思和实质性写作的所有权。资助机构或所在机构限制 AI 参与时，以当前官方政策为准，并清楚标出不能由 AI 实质生成的部分。

## 按需工作

根据任务选择必要部分，而不是强制走完整流水线：

- 建立“要求—官方来源—草稿位置—缺口”合规矩阵；
- 检查研究问题、目标、方法、可行性、时间线、风险和预算是否相互一致；
- 对照正式评审标准提出修改建议，并区分致命合规问题与竞争力改进；
- 审核重投材料是否逐条回应评审意见，同时保持对原始研究计划变更的可追踪性；
- 检查附件、人员角色、合作承诺、数据管理、伦理和机构审批是否有真实依据。

## 机构参考

只在对应机构确实相关时读取相应文件：

- NSFC：`references/nsfc_guidelines.md`
- NSF：`references/nsf_guidelines.md`
- NIH：`references/nih_guidelines.md`
- DOE：`references/doe_guidelines.md`
- DARPA：`references/darpa_guidelines.md`
- 台湾 NSTC：`references/nstc_guidelines.md`

通用组成、评审和写作参考按需读取：

- `references/core_components.md`
- `references/review_criteria.md`
- `references/proposal_types_and_resubmission.md`
- `references/writing_principles.md`
- `references/broader_impacts.md`
- `references/specific_aims_guide.md`

`assets/` 中的 NIH、NSF 和预算说明模板仅是上游示例。只有用户明确要求使用相应模板或交付对应格式时才读取或复制；不得因自动调用本 Skill 就默认套用，也不得把它们当成官方表格。

## 交付检查

交付时分别说明：已核验的当前规则、依赖申请人提供的事实、尚未核验的要求、完成的草稿或审计、以及仍需申请人或机构办理的事项。不得把内容完成说成已经成功提交或获得资助。
