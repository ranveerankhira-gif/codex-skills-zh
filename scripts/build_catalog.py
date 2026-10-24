#!/usr/bin/env python3
"""Build the stable public Skill catalog from curated release metadata."""

from __future__ import annotations

import json
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
V01 = [
    "academic-literature-search", "citation-analysis", "citation-management", "literature-evidence-checker",
    "literature-review", "publication-integrity-check", "research-source-acquisition", "asreview-screening-v3",
    "causal-inference-analysis", "meta-analysis", "qualitative-research-analysis", "research-ethics-consent",
    "research-reproducibility-auditor", "survey-and-psychometrics", "paper-review-reviser", "research-grants",
    "research-prose-naturalizer", "research-workflow", "scientific-critical-thinking", "scientific-paper-reading",
    "scientific-translation", "scientific-writing", "shopping-research-assistant",
]
V02 = [
    "ai-output-renamer", "conversation-handoff", "main-account-takeover", "cross-device-project-sync",
    "diannao-kongzhi", "zhuomian-zhengli", "windows-storage-cleanup", "dryad-data-fetcher",
    "resource-fetcher-router", "web-tool-router", "framepack-video", "video-project-library-maintainer",
    "codex-task-renamer", "wechat-cli", "wechat-intelligence-hub",
]

PURPOSE = {
    "academic-literature-search": "从公开学术数据库检索论文与题录元数据",
    "citation-analysis": "对可追溯论文语料开展引文与文献计量分析",
    "citation-management": "离线规范化、去重和导出参考文献",
    "literature-evidence-checker": "核验引用、书目信息与主张对应关系",
    "literature-review": "规划和执行可复现的文献综述",
    "publication-integrity-check": "核验论文状态、期刊身份与出版诚信风险",
    "research-source-acquisition": "寻找并记录论文全文或研究数据的获取证据",
    "asreview-screening-v3": "使用 ASReview 3 辅助题录筛选",
    "causal-inference-analysis": "规划、审计与解释观察性因果分析",
    "meta-analysis": "严谨合并研究效应量并报告异质性",
    "qualitative-research-analysis": "分析访谈、观察和开放题等定性材料",
    "research-ethics-consent": "准备或审计研究伦理与知情同意材料",
    "research-reproducibility-auditor": "审计方法、分析项目与复现条件",
    "survey-and-psychometrics": "设计、修订和审计问卷与心理测量",
    "paper-review-reviser": "审阅或修订现有科研稿件",
    "research-grants": "准备和核对科研基金申请材料",
    "research-prose-naturalizer": "在保持事实与引用不变时减少科研模板腔",
    "research-workflow": "协调多阶段端到端科研工作流",
    "scientific-critical-thinking": "评估偏倚风险与证据确定性",
    "scientific-paper-reading": "深读单篇科研论文并追踪原文证据",
    "scientific-translation": "忠实翻译科研与学术材料",
    "scientific-writing": "依据真实研究材料起草科研文本",
    "shopping-research-assistant": "基于当前商品证据开展选购调研",
    "ai-output-renamer": "安全整理 AI 输出副本并生成中文语义名称",
    "conversation-handoff": "创建或恢复可核验的长对话交接包",
    "main-account-takeover": "在显式配置的本机 Codex 账号间接力任务",
    "cross-device-project-sync": "完整备份、验证并恢复跨设备项目与会话",
    "diannao-kongzhi": "通过受限 Windows UI Automation 控制桌面应用",
    "zhuomian-zhengli": "盘点并安全调整 Windows 桌面图标布局",
    "windows-storage-cleanup": "审计磁盘占用并按确认清单安全清理",
    "dryad-data-fetcher": "列出或下载公开 Dryad 数据文件",
    "resource-fetcher-router": "按资源类型选择本地下载器并验证结果",
    "web-tool-router": "在免费本地联网工具间安全路由与故障切换",
    "framepack-video": "操作用户配置的本地 FramePack 安装",
    "video-project-library-maintainer": "登记、索引和维护本地视频工程资料库",
    "codex-task-renamer": "预览并在确认后批量重命名 Codex 任务",
    "wechat-cli": "只读检索本地微信聊天并辅助首次接入",
    "wechat-intelligence-hub": "基于本地微信证据生成个人情报报告",
}

NETWORK = {"academic-literature-search", "literature-review", "publication-integrity-check", "research-source-acquisition", "research-grants", "research-workflow", "shopping-research-assistant", "cross-device-project-sync", "dryad-data-fetcher", "resource-fetcher-router", "web-tool-router", "framepack-video"}
WRITES = {"citation-management", "meta-analysis", "ai-output-renamer", "conversation-handoff", "main-account-takeover", "cross-device-project-sync", "diannao-kongzhi", "zhuomian-zhengli", "windows-storage-cleanup", "dryad-data-fetcher", "resource-fetcher-router", "framepack-video", "video-project-library-maintainer", "codex-task-renamer", "wechat-cli", "wechat-intelligence-hub"}
CREDENTIALS = {"cross-device-project-sync", "web-tool-router", "wechat-cli", "wechat-intelligence-hub"}
EXTERNAL = {"cross-device-project-sync", "diannao-kongzhi", "zhuomian-zhengli", "windows-storage-cleanup", "dryad-data-fetcher", "resource-fetcher-router", "web-tool-router", "framepack-video", "codex-task-renamer"}
COST = {"cross-device-project-sync", "dryad-data-fetcher", "resource-fetcher-router", "framepack-video"}
ADAPTED = {"citation-analysis", "research-grants", "scientific-critical-thinking"}


def display_name(name: str) -> str:
    text = (SKILLS / name / "agents" / "openai.yaml").read_text(encoding="utf-8")
    match = re.search(r'^\s*display_name:\s*["\']?(.+?)["\']?\s*$', text, re.M)
    return match.group(1) if match else name


def main() -> int:
    existing = {}
    catalog_path = ROOT / "catalog.json"
    if catalog_path.exists():
        existing = {row["name"]: row for row in json.loads(catalog_path.read_text(encoding="utf-8"))["skills"]}
    rows = []
    for name in V01 + V02:
        if not (SKILLS / name).is_dir():
            continue
        version = "0.1.0" if name in V01 else "0.2.0"
        high = name in V02
        rows.append({
            "name": name,
            "display_name_zh": display_name(name),
            "purpose_zh": PURPOSE[name],
            "release": f"v{version}",
            "platforms": ["windows"] if name in {"diannao-kongzhi", "zhuomian-zhengli", "windows-storage-cleanup", "framepack-video"} else ["cross-platform"],
            "risk_level": "high" if high else ("medium" if name in NETWORK or name in WRITES else "low"),
            "permissions": {
                "network": name in NETWORK,
                "filesystem_read": True,
                "filesystem_write": name in WRITES,
                "credentials": name in CREDENTIALS,
                "external_state": name in EXTERNAL,
                "cost_or_quota": name in COST,
            },
            "dependencies": [],
            "invocation_policy": "explicit-only" if high else "narrow-auto-or-explicit",
            "license": "MIT (adapted; see local license/source files)" if name in ADAPTED else "MIT",
            "version": version,
            "archive_sha256": existing.get(name, {}).get("archive_sha256"),
        })
    payload = {"schema_version": 1, "repository": "ranveerankhira-gif/codex-skills-zh", "skills": rows}
    catalog_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote {catalog_path} with {len(rows)} skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

