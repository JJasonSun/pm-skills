#!/usr/bin/env python3
"""Convert pm-skills to QoderWork plugin format.

Reads source SKILL.md files (Claude format) from pm-*/skills/*/SKILL.md,
and command files from pm-*/commands/*.md, converts them to QoderWork
format, and generates a complete plugin directory.

Usage:
    python3 targets/qoderwork/convert.py --output ./build/qoderwork/
    python3 targets/qoderwork/convert.py --install
    python3 targets/qoderwork/convert.py --output ./build/qoderwork/ --install
"""

import argparse
import os
import re
import shutil
from pathlib import Path

# Plugin directories to process (Claude-format source)
PLUGIN_DIRS = [
    "pm-ai-shipping",
    "pm-data-analytics",
    "pm-execution",
    "pm-go-to-market",
    "pm-market-research",
    "pm-marketing-growth",
    "pm-product-discovery",
    "pm-product-strategy",
    "pm-toolkit",
]

# Category mapping: plugin_dir -> (cn_name, en_name)
PLUGIN_CATEGORIES = {
    "pm-product-discovery": ("产品发现", "Product Discovery"),
    "pm-product-strategy": ("产品战略", "Product Strategy"),
    "pm-execution": ("执行落地", "Execution"),
    "pm-market-research": ("市场研究", "Market Research"),
    "pm-data-analytics": ("数据分析", "Data Analytics"),
    "pm-go-to-market": ("上市策略", "Go-to-Market"),
    "pm-marketing-growth": ("营销增长", "Marketing & Growth"),
    "pm-toolkit": ("通用工具", "Toolkit"),
    "pm-ai-shipping": ("AI交付", "AI Shipping"),
}

# Plugin metadata
PLUGIN_META = {
    "name": "pm-skills",
    "displayName": "产品管理技能箱",
    "version": "1.0.0",
    "description": "Structured AI workflows for better product decisions. 68 domain-specific skills and 42 chained workflow commands (102 unique modules) across discovery, strategy, execution, market research, data analytics, go-to-market, marketing growth, toolkit, and AI shipping.",
    "descriptionZh": "产品管理全流程技能箱，覆盖产品发现、策略、执行、市场调研、数据分析、GTM、营销增长、工具箱和AI交付九大方向，共68个技能+42个工作流编排命令。每个技能内置行业方法论和分析框架，命令将多个技能串联成端到端工作流，产出可直接交付。",
    "author": {
        "name": "Paweł Huryn",
        "url": "https://www.productcompass.pm"
    },
    "category": "product-management",
    "tags": ["product-management", "PRD", "strategy", "discovery", "analytics", "go-to-market"],
}

# Chinese descriptions for skills (keeps professional English terms)
DESCRIPTION_ZH = {
    "intended-vs-implemented": "找出系统文档描述与代码实际行为之间差距的方法——通用扫描器遗漏的 bug 类型。用于审计 AI 生成代码、对照文档验证权限控制、检查代码库是否与自身文档一致。",
    "shipping-artifacts": "使 AI 构建（vibe-coded）的应用在交付前可审查的持久文档集：架构、用户/权限流程、权限、变量/密钥、测试覆盖图，加上条件性文档（邮件、定时任务、SEO、嵌入式代理）。用于代码库交接、安全或性能审计准备。",
    "ab-test-analysis": "分析 A/B 测试结果，含统计显著性、样本量验证、置信区间和发布/扩展/停止建议。用于评估实验结果、检查测试是否达到显著性、决定是否发布某个变体。",
    "cohort-analysis": "对用户参与数据进行同期群分析——留存曲线、功能采用趋势和细分洞察。用于按同期群分析留存、研究功能随时间的采用情况、调查流失模式。",
    "sql-queries": "从自然语言描述生成 SQL 查询，支持 BigQuery、PostgreSQL、MySQL 等方言。用于编写 SQL、构建数据报告、探索数据库或将业务问题翻译为查询。",
    "brainstorm-okrs": "头脑风暴与公司目标对齐的团队级 OKR——定性目标加可衡量的关键结果。用于设定季度 OKR、将团队目标与公司策略对齐、学习如何编写有效的 OKR。",
    "create-prd": "使用全面的 8 部分 PRD 模板创建产品需求文档，覆盖问题、目标、细分、价值主张、方案和发布规划。用于撰写 PRD、记录产品需求、准备功能规格。",
    "dummy-dataset": "生成逼真的测试数据集，支持自定义列、约束和输出格式（CSV、JSON、SQL、Python 脚本）。用于创建测试数据、构建 mock 数据集或生成开发和演示用的样本数据。",
    "job-stories": "使用 'When [情境], I want to [动机], so I can [结果]' 格式创建 Job Stories，含详细验收标准。用于编写 JTBD 风格的待办项或表达用户情境和动机。",
    "outcome-roadmap": "将输出导向的路线图转化为结果导向的路线图，传达战略意图。用于转向结果路线图、使路线图更具战略性、将功能列表重写为结果。",
    "pre-mortem": "对 PRD 或上市计划进行事前风险分析，将风险分类为 Tigers（真实问题）、Paper Tigers（过度担忧）和 Elephants（未说出口的顾虑）。用于发布前准备、压力测试产品计划。",
    "prioritization-frameworks": "9 个优先级排序框架参考指南，含公式、使用场景和模板——RICE、ICE、Kano、MoSCoW、Opportunity Score 等。用于选择排序方法、比较 RICE vs ICE 等框架。",
    "release-notes": "从工单、PRD 或变更日志生成面向用户的发布说明，按类别组织（新功能、改进、修复）。用于撰写发布说明、创建变更日志、宣布产品更新。",
    "retro": "引导结构化 Sprint 回顾——做得好的、做得不好的、以及带负责人和截止日期的优先行动项。用于运行回顾、反思 Sprint、从团队反馈创建行动项。",
    "sprint-plan": "规划 Sprint，含容量估算、故事选择、依赖映射和风险识别。用于准备 Sprint 规划、估算团队容量、选择故事或平衡 Sprint 范围与速度。",
    "stakeholder-map": "使用权力/利益网格构建利益相关者地图，识别每个象限的沟通策略并生成沟通计划。用于管理利益相关者、准备发布、对齐跨职能团队。",
    "strategy-red-team": "通过攻击 PRD、路线图或策略的承重假设来进行红队测试。先钢铁人再攻击每个论点，按影响 × 可能性 × 测试成本排序失败模式。用于压力测试计划、挑战假设或准备高管审查。",
    "summarize-meeting": "将会议记录总结为结构化笔记，含日期、参与者、主题、关键决策、摘要要点和行动项。用于处理会议录音、创建会议纪要或回顾讨论。",
    "test-scenarios": "从用户故事创建全面的测试场景，含测试目标、起始条件、用户角色、步骤和预期结果。用于编写 QA 测试用例、创建测试计划或定义验收测试。",
    "user-stories": "遵循 3 C's（Card、Conversation、Confirmation）和 INVEST 标准创建用户故事，含描述、设计链接和验收标准。用于编写用户故事、将功能拆分为待办项。",
    "wwas": "以 Why-What-Acceptance 格式创建产品待办项——独立、有价值、可测试的条目，含战略上下文。用于编写结构化待办项或将功能拆分为工作项。",
    "beachhead-segment": "为产品发布识别第一个滩头市场细分，按痛点强度、支付意愿、可赢取的市场份额和推荐潜力评估。用于选择首个市场、瞄准初始客户细分或规划市场进入策略。",
    "competitive-battlecard": "创建面向销售的竞争战斗卡，比较你的产品与特定竞品——定位、功能对比、异议处理和赢/输模式。用于准备销售团队、创建竞争材料。",
    "growth-loops": "识别增长循环（飞轮）以获得可持续增长。评估 5 种循环类型：Viral、Usage、Collaboration、User-Generated、Referral。用于设计增长机制或构建产品驱动的增长。",
    "gtm-motions": "在 7 种 GTM 模式中识别最佳模式及工具：Inbound、Outbound、Paid Digital、Community、Partners、ABM、PLG。用于选择营销渠道或规划跨渠道活动。",
    "gtm-strategy": "创建 GTM 策略，覆盖营销渠道、信息、成功指标和发布时间线。用于规划产品发布、从零创建 GTM 计划或为新市场定义发布策略。",
    "ideal-customer-profile": "从研究数据识别理想客户画像（ICP），含人口统计、行为、JTBD 和需求。用于定义 ICP、分析 PMF 调查数据或理解最佳客户是谁。",
    "competitor-analysis": "分析竞品的优势、弱点和差异化机会，识别直接竞争对手并映射竞争格局。用于竞争研究、准备竞争简报或寻找差异化机会。",
    "customer-journey-map": "创建端到端客户旅程图，含阶段、触点、情感、痛点和机会。用于映射客户体验、识别摩擦点、改善用户引导或可视化用户旅程。",
    "market-segments": "识别 3-5 个潜在客户细分，含人口统计、JTBD 和产品契合度分析。用于探索市场细分、识别目标受众、评估新市场或学习如何进行市场细分。",
    "market-sizing": "使用 TAM、SAM、SOM 估算市场规模，含自上而下和自下而上方法。用于估算市场规模、准备投资者路演或评估市场进入。",
    "sentiment-analysis": "分析用户反馈数据，识别细分群体的情感分数、JTBD 和产品满意度洞察。用于大规模分析用户反馈、对评论或调查进行情感分析。",
    "user-personas": "从研究数据创建精炼的用户画像——3 个画像含 JTBD、痛点、增益和意外洞察。用于从调查数据构建画像、从研究创建用户档案。",
    "user-segmentation": "基于行为、JTBD 和需求从反馈数据中细分用户，识别至少 3 个不同的用户细分。用于细分用户群、分析多样化的用户反馈或构建细分模型。",
    "marketing-ideas": "生成 5 个创意、低成本的营销方案，含渠道、信息和参与理由。用于头脑风暴营销活动、规划产品推广或寻找创意营销策略。",
    "north-star-metric": "定义 North Star Metric 和 3-5 个支撑输入指标，形成指标星座。分类商业博弈类型（Attention、Transaction、Productivity）并按 7 项标准验证。用于选择 North Star Metric、搭建指标框架。",
    "positioning-ideas": "头脑风暴与竞品差异化的产品定位，识别主要竞品并生成带理由的定位声明。用于开发产品定位、与竞品差异化或制定品牌定位策略。",
    "product-name": "头脑风暴 5 个独特、易记的产品名称，符合品牌价值和目标受众。用于命名新产品、品牌重塑或探索产品名称创意。",
    "value-prop-statements": "从现有价值主张生成面向营销、销售和用户引导的价值主张陈述。用于撰写营销文案、创建销售信息或制作用户引导信息。",
    "analyze-feature-requests": "按主题、战略对齐度、影响、工作量和风险分析和优先排序功能请求列表。用于审查客户功能请求、分类待办或做优先级决策。",
    "brainstorm-experiments-existing": "为现有产品设计实验来测试假设——原型、A/B 测试、spike 和其他低成本验证方法。用于验证假设、低成本测试功能想法或规划产品实验。",
    "brainstorm-experiments-new": "为新产品设计精益创业实验（pretotype），创建 XYZ 假设并建议低成本验证方法如落地页、解说视频和预购。用于验证新产品想法、创建 pretotype 或测试市场需求。",
    "brainstorm-ideas-existing": "使用 PM、设计师和工程师多视角构思为现有产品头脑风暴功能想法。用于生成新功能想法、为已识别的机会构思解决方案或与产品三人组进行构思。",
    "brainstorm-ideas-new": "从 PM、设计师和工程师视角为新产品头脑风暴功能想法。用于启动新产品的产品发现、为创业想法探索功能或进行初始构思。",
    "identify-assumptions-existing": "从价值、可用性、可行性和可行性四个维度识别现有产品功能想法的风险假设，使用多视角魔鬼代言人思维。用于压力测试功能想法或进行风险评估。",
    "identify-assumptions-new": "为新产品想法识别 8 个风险类别的风险假设，包括 GTM、策略和团队。用于评估创业风险、评估新产品概念或为新企业映射假设。",
    "interview-script": "创建结构化的客户访谈脚本，含 JTBD 探究问题、热身、核心探索和总结部分。遵循 The Mom Test 原则——无引导性问题、无推销、聚焦过去行为。用于准备用户访谈或规划发现研究。",
    "metrics-dashboard": "定义和设计产品指标看板，含关键指标、数据源、可视化类型和告警阈值。用于创建指标看板、定义 KPI、搭建产品分析或构建数据监控计划。",
    "opportunity-solution-tree": "构建机会解决方案树（OST）来结构化产品发现——将期望结果映射到机会、方案和实验。基于 Teresa Torres 的 Continuous Discovery Habits。用于结构化发现工作或决定下一步做什么。",
    "prioritize-assumptions": "使用影响 × 风险矩阵优先排序假设并为每个建议实验。用于排序假设列表、决定先测试什么或应用假设优先级画布。",
    "prioritize-features": "基于影响、工作量、风险和战略对齐度优先排序功能待办，给出前 5 名推荐。用于优先排序功能待办、做范围决策或排序产品想法。",
    "summarize-interview": "将客户访谈记录总结为结构化模板，含 JTBD、满意度信号和行动项。用于处理访谈录音或记录、综合发现访谈或创建访谈摘要。",
    "ansoff-matrix": "生成 Ansoff Matrix 分析，映射市场渗透、市场开发、产品开发和多元化四种增长策略。用于考虑增长选项、规划市场扩展或评估战略增长路径。",
    "business-model": "生成包含全部 9 个构建块的 Business Model Canvas。用于创建商业模式、记录企业如何创造价值或分析现有商业模式。",
    "lean-canvas": "生成 Lean Canvas，含问题、方案、指标、成本结构、UVP、不公平优势、渠道、细分和收入。用于探索精益创业画布、测试商业假设或建模新企业。",
    "monetization-strategy": "头脑风暴 3-5 个变现策略，含受众契合度、风险和验证实验。用于探索收入模式、评估定价策略或决定如何变现产品。",
    "pestle-analysis": "执行 PESTLE 分析，覆盖政治、经济、社会、技术、法律和环境因素。用于评估宏观环境、进行战略规划或评估影响企业的外部因素。",
    "porters-five-forces": "执行 Porter's Five Forces 分析——竞争强度、供应商议价能力、买方议价能力、替代品威胁和新进入者威胁。用于分析行业动态或评估市场吸引力。",
    "pricing-strategy": "分析和设计定价策略，含定价模型、竞争定价分析、支付意愿估算和价格弹性。用于设定价格、评估定价模型或比较 freemium vs 付费模式。",
    "product-strategy": "使用 9 部分 Product Strategy Canvas 创建全面的产品策略——愿景、细分、成本、价值主张、权衡、指标、增长、能力和防御性。用于构建产品策略或定义产品方向。",
    "product-vision": "头脑风暴鼓舞人心、可实现且富有情感的产品愿景，激励团队并对齐利益相关者。用于定义或优化产品愿景、创建愿景声明或围绕共同方向对齐团队。",
    "startup-canvas": "生成创业画布，结合 Product Strategy（9 部分）和 Business Model（成本 + 收入）。BMC 和 Lean Canvas 的替代方案，将策略与商业模式分离。用于发布新产品或评估创业概念。",
    "swot-analysis": "执行详细的 SWOT 分析——优势、劣势、机会和威胁，附可操作建议。用于战略评估、竞争分析或评估产品/商业定位。",
    "value-proposition": "使用 6 部分 JTBD 模板设计详细的价值主张——谁、为什么、之前怎样、如何做、之后怎样、替代方案。用于创建价值主张或分析客户价值交付。",
    "draft-nda": "起草两方之间的保密协议（NDA），覆盖信息类型、司法管辖区和需要法律审查的条款。用于创建保密协议或准备合作 NDA。",
    "grammar-check": "识别文本中的语法、逻辑和流畅度错误并提供针对性修改建议，而非重写整篇文本。用于校对内容、检查写作质量或审查草稿。",
    "privacy-policy": "起草详细的隐私政策，覆盖数据类型、司法管辖区、GDPR 和合规考量，以及需要法律审查的条款。用于创建隐私政策或更新数据保护文档。",
    "review-resume": "全面的 PM 简历审查和定制，基于 10 个最佳实践含 XYZ+S 公式、关键词优化、职位定向定制和结构。用于审查 PM 简历或准备求职申请。",
}

# Chinese descriptions for command-workflow skills
COMMAND_DESCRIPTION_ZH = {
    "ship-check": "将 vibe-coded 仓库转化为可审查的交付包：文档、连接代理上下文、运行安全和性能审计、映射测试覆盖、编译结果。",
    "document-app": "将代码库逆向工程为审查者和审计者需要的系统文档——核心集加条件性文档。",
    "derive-tests": "将文档描述的意图转化为测试覆盖图：盘点现有测试、区分提议测试和未验证缺口、推荐合并前 CI 门禁。",
    "security-audit-static": "静态安全审计：映射信任边界、交叉引用文档意图、自我反驳每个发现、只报告有证据支持的风险。",
    "performance-audit-static": "静态性能审计：发现过度获取、缺失索引和缓存机会，按工作量和影响排序。",
    "analyze-cohorts": "同期群分析：留存曲线、功能采用趋势和参与洞察。",
    "analyze-test": "A/B 测试分析：统计显著性、样本量验证和发布/扩展/停止建议。",
    "write-query": "从自然语言生成 SQL 查询，支持 BigQuery、PostgreSQL、MySQL 等方言。",
    "generate-data": "生成逼真的测试数据集，支持 CSV、JSON、SQL 或 Python 脚本格式。",
    "meeting-notes": "将会议记录总结为结构化笔记，含决策和行动项。",
    "plan-okrs": "头脑风暴与公司目标对齐的团队级 OKR。",
    "pre-mortem": "事前风险分析：Tigers/Paper Tigers/Elephants 分类框架。",
    "red-team-prd": "红队测试 PRD/策略：攻击承重假设，返回最低成本测试。",
    "sprint": "Sprint 生命周期：规划、回顾或发布说明。",
    "stakeholder-map": "利益相关者地图：权力/利益网格加沟通计划。",
    "test-scenarios": "从用户故事生成全面的测试场景。",
    "transform-roadmap": "将功能路线图转化为结果导向路线图。",
    "write-prd": "从功能想法或问题陈述创建 PRD。",
    "write-stories": "将功能拆分为待办项（user stories / job stories / WWA）。",
    "battlecard": "创建面向销售的竞争战斗卡。",
    "growth-strategy": "设计增长循环和评估 GTM 模式。",
    "plan-launch": "创建完整的 GTM 策略：滩头阵地、ICP、渠道和发布计划。",
    "analyze-feedback": "大规模用户反馈情感分析和主题提取。",
    "competitive-analysis": "分析竞争格局：竞品、弱点和差异化机会。",
    "research-users": "用户研究：画像、细分和客户旅程图。",
    "market-product": "头脑风暴营销创意、定位、价值主张和产品命名。",
    "north-star": "定义 North Star Metric 和支撑输入指标。",
    "brainstorm": "多视角构思产品想法或实验（existing/new × ideas/experiments）。",
    "discover": "完整产品发现周期：构思→假设映射→优先排序→实验设计。",
    "interview": "客户访谈：准备脚本或总结记录。",
    "setup-metrics": "设计产品指标看板含 North Star 和告警阈值。",
    "triage-requests": "分析和优先排序一批功能请求。",
    "business-model": "探索商业模式：Lean Canvas / BMC / Startup Canvas / 价值主张。",
    "market-scan": "宏观环境分析：SWOT + PESTLE + Porter's + Ansoff 一站扫描。",
    "pricing": "设计定价策略：模型、竞品分析、支付意愿和实验。",
    "strategy": "使用 9 部分 Product Strategy Canvas 创建产品策略。",
    "value-proposition": "使用 6 部分 JTBD 模板设计价值主张。",
    "draft-nda": "起草保密协议（NDA）。",
    "privacy-policy": "起草隐私政策含 GDPR 合规。",
    "proofread": "检查语法、逻辑和流畅度。",
    "review-resume": "PM 简历审查含 XYZ+S 公式。",
    "tailor-resume": "针对职位描述定制 PM 简历。",
}

INSTALL_PATH = os.path.expanduser("~/.qoderworkcn/plugins-custom/pm-skills")


def convert_skill_md(content: str, skill_name: str) -> str:
    """Convert a SKILL.md from Claude format to QoderWork format."""
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not fm_match:
        return content

    fm_text = fm_match.group(1)
    body = fm_match.group(2)

    name_match = re.search(r'^name:\s*(.+)$', fm_text, re.MULTILINE)
    desc_match = re.search(r'description:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)

    name = name_match.group(1).strip() if name_match else "unknown"
    description = desc_match.group(1).strip() if desc_match else ""
    desc_zh = DESCRIPTION_ZH.get(skill_name, description)

    new_fm = f"""---
name: {name}
version: 1.0.0
description: "{description}"
description_zh: "{desc_zh}"
user-invocable: true
---"""

    body = body.replace('$ARGUMENTS', "the user's request")
    body = re.sub(r'## Metadata\n(?:- \*\*[^*]+\*\*:.*\n)+', '', body)

    return f'{new_fm}\n{body}'


def convert_command_md(content: str, cmd_name: str) -> str:
    """Convert a command .md from Claude format to QoderWork skill format."""
    fm_match = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
    if not fm_match:
        return content

    fm_text = fm_match.group(1)
    body = fm_match.group(2)

    desc_match = re.search(r'description:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)
    hint_match = re.search(r'argument-hint:\s*["\']?(.*?)["\']?\s*$', fm_text, re.MULTILINE)

    description = desc_match.group(1).strip() if desc_match else ""
    hint = hint_match.group(1).strip() if hint_match else ""
    desc_zh = COMMAND_DESCRIPTION_ZH.get(cmd_name, description)

    new_fm = f"""---
name: {cmd_name}
version: 1.0.0
description: "{description}"
description_zh: "{desc_zh}"
argument-hint: "{hint}"
user-invocable: true
---"""

    # Clean Claude-specific syntax from body
    # Replace /command invocation examples with natural language
    body = body.replace('$ARGUMENTS', "the user's request")

    # Remove Invocation sections (Claude-specific /command syntax)
    body = re.sub(r'## Invocation\n(?:.*?\n)*?\n', '', body)

    return f'{new_fm}\n{body}'


def collect_all(repo_root: Path) -> dict:
    """Scan all plugin directories and collect skills + commands."""
    skills_by_category = {}
    commands_by_category = {}
    all_skills = []
    all_commands = []

    for plugin_dir in PLUGIN_DIRS:
        # Collect skills
        skills_path = repo_root / plugin_dir / "skills"
        cn_name, en_name = PLUGIN_CATEGORIES[plugin_dir]
        skills_by_category[plugin_dir] = {"cn": cn_name, "en": en_name, "skills": []}
        commands_by_category[plugin_dir] = {"cn": cn_name, "en": en_name, "commands": []}

        if skills_path.exists():
            for skill_dir in sorted(skills_path.iterdir()):
                if not skill_dir.is_dir():
                    continue
                skill_md_path = skill_dir / "SKILL.md"
                if not skill_md_path.exists():
                    continue

                skill_name = skill_dir.name
                content = skill_md_path.read_text(encoding='utf-8')
                converted = convert_skill_md(content, skill_name)
                desc_zh = DESCRIPTION_ZH.get(skill_name, "")

                all_skills.append(skill_name)
                skills_by_category[plugin_dir]["skills"].append({
                    "name": skill_name,
                    "desc_zh": desc_zh,
                    "content": converted,
                    "src_dir": skill_dir,
                })

        # Collect commands
        commands_path = repo_root / plugin_dir / "commands"
        if commands_path.exists():
            for cmd_file in sorted(commands_path.iterdir()):
                if not cmd_file.is_file() or cmd_file.suffix != '.md':
                    continue

                cmd_name = cmd_file.stem  # e.g., "discover" from "discover.md"
                content = cmd_file.read_text(encoding='utf-8')
                converted = convert_command_md(content, cmd_name)
                desc_zh = COMMAND_DESCRIPTION_ZH.get(cmd_name, "")

                all_commands.append(cmd_name)
                commands_by_category[plugin_dir]["commands"].append({
                    "name": cmd_name,
                    "desc_zh": desc_zh,
                    "content": converted,
                })

    return {
        "skills": all_skills,
        "commands": all_commands,
        "skills_by_category": skills_by_category,
        "commands_by_category": commands_by_category,
    }


def build_plugin(repo_root: Path, output_dir: Path):
    """Build a complete QoderWork plugin directory."""
    data = collect_all(repo_root)
    skills_by_cat = data["skills_by_category"]
    commands_by_cat = data["commands_by_category"]

    # Index skills by name for collision detection
    skill_by_name = {}
    for info in skills_by_cat.values():
        for s in info["skills"]:
            skill_by_name[s["name"]] = s

    # Track written names and merged count
    written_names = set()
    merged_count = 0

    # Write skill files
    skills_dir = output_dir / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    for plugin_dir, info in skills_by_cat.items():
        for s in info["skills"]:
            dst = skills_dir / s["name"]
            dst.mkdir(parents=True, exist_ok=True)
            (dst / "SKILL.md").write_text(s["content"], encoding='utf-8')
            refs_src = s["src_dir"] / "references"
            if refs_src.exists():
                refs_dst = dst / "references"
                if refs_dst.exists():
                    shutil.rmtree(refs_dst)
                shutil.copytree(refs_src, refs_dst)
            written_names.add(s["name"])

    # Write command-workflow skill files (merge if name collides with a skill)
    for plugin_dir, info in commands_by_cat.items():
        for c in info["commands"]:
            dst = skills_dir / c["name"]
            dst.mkdir(parents=True, exist_ok=True)
            if c["name"] in written_names:
                # Collision: append command workflow to existing skill
                existing = (dst / "SKILL.md").read_text(encoding='utf-8')
                # Extract body from command (after frontmatter)
                cmd_body = c["content"].split('---\n', 2)[-1] if '---\n' in c["content"] else c["content"]
                merged = f"{existing}\n\n---\n\n## Workflow Orchestration\n{cmd_body}"
                (dst / "SKILL.md").write_text(merged, encoding='utf-8')
                merged_count += 1
            else:
                (dst / "SKILL.md").write_text(c["content"], encoding='utf-8')
                written_names.add(c["name"])

    # Generate plugin.json (unique names only)
    meta_dir = output_dir / ".qoder-plugin"
    meta_dir.mkdir(parents=True, exist_ok=True)

    skills_array = [f"skills/{name}" for name in sorted(written_names)]
    import json
    plugin_json = {**PLUGIN_META, "skills": skills_array}
    (meta_dir / "plugin.json").write_text(
        json.dumps(plugin_json, indent=2, ensure_ascii=False) + "\n",
        encoding='utf-8',
    )

    # Generate README.md
    n_skills = len(data["skills"])
    n_commands = len(data["commands"])
    n_total = len(written_names)
    readme = generate_readme(skills_by_cat, commands_by_cat, n_skills, n_commands, n_total, merged_count)
    (output_dir / "README.md").write_text(readme, encoding='utf-8')

    print(f"Built plugin at {output_dir}")
    print(f"  Skills: {n_skills}, Commands: {n_commands}, Merged: {merged_count}, Total unique: {n_total}")
    for plugin_dir in PLUGIN_DIRS:
        s_info = skills_by_cat.get(plugin_dir)
        c_info = commands_by_cat.get(plugin_dir)
        if s_info and c_info:
            print(f"  {s_info['cn']} ({s_info['en']}): {len(s_info['skills'])} skills, {len(c_info['commands'])} commands")


def generate_readme(skills_by_cat: dict, commands_by_cat: dict, n_skills: int, n_commands: int, n_total: int, merged_count: int = 0) -> str:
    """Generate README.md from category data."""
    lines = [
        "# 产品管理技能箱",
        "",
        f"产品管理全流程技能箱，覆盖产品发现、策略、执行、市场调研、数据分析、GTM、营销增长、工具箱和AI交付九大方向，共{n_total}个技能模块（{n_skills}个方法论技能 + {n_commands}个工作流技能，其中{merged_count}个同名合并）。方法论技能提供行业分析框架，工作流技能将多个技能串联成端到端工作流。源自 Paweł Huryn 的 [pm-skills](https://github.com/phuryn/pm-skills) 开源项目。",
        "",
        "> **Disclaimer:** 本插件辅助产品管理专业工作流程，不替代专业判断。所有产出应在决策前由合格的专业人员审查。",
        "",
        "## Target Roles",
        "",
        "- **产品经理** — 从需求发现到PRD撰写，覆盖产品全生命周期",
        "- **产品总监** — 战略规划、竞品分析、路线图制定",
        "- **增长PM** — GTM策略、营销增长、数据驱动决策",
        "- **创业PM** — 从0到1的产品验证和商业模式设计",
        "",
        "## 快速入门",
        "",
        "有新想法？→ `discover`",
        "需要战略清晰度？→ `strategy`",
        "在写 PRD？→ `write-prd`",
        "规划上市？→ `plan-launch`",
        "定义指标？→ `north-star`",
        "",
        "## 技能（Skills）",
        "",
    ]

    for plugin_dir in PLUGIN_DIRS:
        info = skills_by_cat.get(plugin_dir)
        if not info or not info["skills"]:
            continue
        lines.append(f"### {info['cn']} ({info['en']}) — {len(info['skills'])} skills")
        lines.append("")
        lines.append("| Skill | 说明 |")
        lines.append("|-------|------|")
        for s in info["skills"]:
            lines.append(f"| {s['name']} | {s['desc_zh']} |")
        lines.append("")

    lines.append("## 工作流技能（Workflow Skills）")
    lines.append("")
    lines.append("工作流技能将多个方法论技能串联成端到端工作流，是本套件的核心使用方式。")
    lines.append("")

    for plugin_dir in PLUGIN_DIRS:
        info = commands_by_cat.get(plugin_dir)
        if not info or not info["commands"]:
            continue
        cn = info["cn"]
        en = info["en"]
        lines.append(f"### {cn} ({en}) — {len(info['commands'])} skills")
        lines.append("")
        lines.append("| Skill | 说明 |")
        lines.append("|---------|------|")
        for c in info["commands"]:
            lines.append(f"| {c['name']} | {c['desc_zh']} |")
        lines.append("")

    lines.extend([
        "## Connectors (Optional Enhancement)",
        "",
        "本插件所有技能均可独立使用，无需连接器。连接文档协作平台（如Notion、飞书文档）后可将产出自动发布为文档。",
        "",
        "> All skills work fully without connectors.",
        "",
    ])

    return "\n".join(lines)


def install_plugin(output_dir: Path):
    """Create symlink from install path to build output."""
    target = Path(INSTALL_PATH)
    if target.is_symlink() or target.exists():
        if target.is_symlink():
            target.unlink()
        else:
            shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(output_dir.resolve())
    print(f"Symlinked {target} -> {output_dir.resolve()}")


def main():
    parser = argparse.ArgumentParser(description="Convert pm-skills to QoderWork plugin")
    parser.add_argument("--output", default="./build/qoderwork/",
                        help="Output directory (default: ./build/qoderwork/)")
    parser.add_argument("--install", action="store_true",
                        help="Create symlink at ~/.qoderworkcn/plugins-custom/pm-skills/")
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent.parent
    output_dir = Path(args.output)
    if not output_dir.is_absolute():
        output_dir = repo_root / output_dir

    print(f"Source: {repo_root}")
    print(f"Output: {output_dir}")

    build_plugin(repo_root, output_dir)

    if args.install:
        install_plugin(output_dir)


if __name__ == "__main__":
    main()