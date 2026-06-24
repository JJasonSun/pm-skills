![GitHub stars](https://img.shields.io/github/stars/phuryn/pm-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](https://github.com/phuryn/pm-skills/blob/main/LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square)](https://github.com/phuryn/pm-skills/blob/main/CONTRIBUTING.md)
[![Companion: pm-skills](https://img.shields.io/badge/companion-pm--brain-blue)](https://github.com/phuryn/pm-brain)
[![Companion: burnstop](https://img.shields.io/badge/companion-burnstop-blue)](https://github.com/phuryn/burnstop)
[![Companion: claude-usage](https://img.shields.io/badge/companion-claude--usage-blue)](https://github.com/phuryn/claude-usage)

[English](README.md) | 中文

# PM Skills Marketplace：更好产品决策的 AI 操作系统

> 68 个产品管理技能和 42 个链式工作流，分布在 9 个插件中。支持 Claude Code、QoderWork 等。覆盖从产品发现到策略、执行、上市、增长和 AI 代码交付的全流程。

![PM Skills marketplace: skills, commands, and all 9 plugins at a glance](.docs/images/plugins.png)

为 Claude Code 和 Cowork 设计。技能可兼容其他 AI 助手。

## 从这里开始

有新想法？→ `/discover`
需要战略清晰度？→ `/strategy`
在写 PRD？→ `/write-prd`
规划上市？→ `/plan-launch`
定义指标？→ `/north-star`

如果这个项目对你有帮助，请给仓库点个 ⭐。

## 为什么选择 PM Skills Marketplace？

通用 AI 给你文字。PM Skills Marketplace 给你结构。

每个技能封装了一个经过验证的 PM 框架——发现、假设映射、优先级排序、策略——并引导你一步步完成。你把 Teresa Torres、Marty Cagan 和 Alberto Savoia 的严谨方法论融入到日常工作流中，而不是放在书架上。

结果：更好的产品决策，而不仅仅是更快的文档。

## 工作原理（技能、命令、插件）

![Example prompts: a skill and two commands (/write-prd, /ship-check) in action](.docs/images/examples.png)

**技能（Skills）** 是市场的构建模块。每个技能赋予 Claude 特定 PM 任务的领域知识、分析框架或引导式工作流。一些技能也作为可复用的基础被多个命令共享。

技能在对话相关时自动加载——无需显式调用。如需强制加载（例如优先使用技能而非通用知识），可以用 `/plugin-name:skill-name` 或 `/skill-name`（Claude 会自动补全前缀）。

**命令（Commands）** 是用户通过 `/command-name` 触发的工作流。它们将一个或多个技能串联成端到端流程。例如，`/discover` 将四个技能串联在一起：brainstorm-ideas → identify-assumptions → prioritize-assumptions → brainstorm-experiments。

**插件（Plugins）** 将相关技能和命令分组为可安装的包。每个插件覆盖一个 PM 领域——发现、策略、执行等。安装市场后你将一次获得全部 9 个插件。

命令使用技能。一些技能服务多个命令。一些技能（如 `prioritization-frameworks` 或 `opportunity-solution-tree`）是独立参考，Claude 在相关时自动调用——无需命令。

命令设计为可链式流转，匹配 PM 工作流。任何命令完成后，它会建议相关的后续命令——只需跟随提示即可。

## 安装

### Claude Cowork（推荐非开发者使用）

1. 打开 **Customize**（左下角）
2. 进入 **Browse plugins** → **Personal** → **+**
3. 选择 **Add marketplace from GitHub**
4. 输入：`phuryn/pm-skills`

全部 9 个插件自动安装。你将同时获得命令（`/discover`、`/strategy` 等）和技能。

![Installing PM Skills in Claude Cowork](.docs/images/pm-skills-install.gif)

### Claude Code（CLI）

```bash
# 第一步：添加市场
claude plugin marketplace add phuryn/pm-skills

# 第二步：安装各个插件
claude plugin install pm-toolkit@pm-skills
claude plugin install pm-product-strategy@pm-skills
claude plugin install pm-product-discovery@pm-skills 
claude plugin install pm-market-research@pm-skills 
claude plugin install pm-data-analytics@pm-skills
claude plugin install pm-marketing-growth@pm-skills
claude plugin install pm-go-to-market@pm-skills
claude plugin install pm-execution@pm-skills
claude plugin install pm-ai-shipping@pm-skills
```

### Codex CLI (OpenAI)

Codex 读取与 Claude Code 相同的插件市场文件，因此可以原生安装 PM Skills——无需转换或复制文件：

```bash
# 第一步：添加市场
codex plugin marketplace add phuryn/pm-skills

# 第二步：安装你需要的插件
codex plugin add pm-toolkit@pm-skills
codex plugin add pm-product-strategy@pm-skills
codex plugin add pm-product-discovery@pm-skills
codex plugin add pm-market-research@pm-skills
codex plugin add pm-data-analytics@pm-skills
codex plugin add pm-marketing-growth@pm-skills
codex plugin add pm-go-to-market@pm-skills
codex plugin add pm-execution@pm-skills
codex plugin add pm-ai-shipping@pm-skills
```

**你将获得：** 每个技能（PM 框架），可被 Codex 按名称调用。建议安装整个插件而非单独挑选技能——一个工作流通常依赖多个一起发布的技能。

**与 Claude Code 的区别：** `/slash` 命令（`/discover`、`/write-prd`……）会安装但不会作为 Codex slash 命令运行——Codex 插件不暴露命令。要运行工作流，只需用自然语言描述步骤，例如：

> 对*[你的想法]*进行产品发现：头脑风暴选项、映射假设、优先排序风险最高的假设、然后设计实验——每步之间暂停。

**可选——让 Codex 将工作流转为技能。** 因为命令文件随插件一起安装，你可以请 Codex 转换你最常用的：

> 阅读 pm-execution 插件中的命令文件，为我最常用的工作流创建等效的 Codex 技能。

这是一种尽力而为的模型驱动转换（某些 Claude 专有命令语法无法翻译），但这是在 Codex 上获得引导式工作流的快捷方式。

### QoderWork

```bash
# 从仓库根目录运行
python3 targets/qoderwork/convert.py --install
```

将 9 个 Claude 插件合并为 1 个 QoderWork 套件，自动安装到 `~/.qoderworkcn/plugins-custom/pm-skills/`。详见 [targets/README.md](targets/README.md)。

### 其他 AI 助手（仅技能）

`skills/*/SKILL.md` 文件遵循通用技能格式，可与任何读取该格式的工具配合使用。命令（`/slash-commands`）是 Claude 专有的。

| 工具                 | 使用方法                                 | 支持内容 |
| -------------------- | ---------------------------------------- | -------- |
| **Gemini CLI** | 将技能文件夹复制到 `.gemini/skills/`   | 仅技能   |
| **OpenCode**   | 将技能文件夹复制到 `.opencode/skills/` | 仅技能   |
| **Cursor**     | 将技能文件夹复制到 `.cursor/skills/`   | 仅技能   |
| **Kiro**       | 将技能文件夹复制到 `.kiro/skills/`     | 仅技能   |

```bash
# 示例：为 OpenCode 复制所有技能（项目级）
for plugin in pm-*/; do
  mkdir -p .opencode/skills/
  cp -r "$plugin/skills/"* .opencode/skills/ 2>/dev/null
done

# 示例：为 Gemini CLI 复制所有技能（全局）
for plugin in pm-*/; do
  cp -r "$plugin/skills/"* ~/.gemini/skills/ 2>/dev/null
done
```

---

## 可用插件

<details>
<summary><strong>1. pm-product-discovery</strong> — 构思、实验、假设测试、OST、访谈（13 个技能，5 个命令）</summary>

**技能（13）：**

- `brainstorm-ideas-existing` — 针对现有产品的多视角构思（PM、设计师、工程师）
- `brainstorm-ideas-new` — 针对新产品的初始发现阶段构思
- `brainstorm-experiments-existing` — 为现有产品设计实验来测试假设
- `brainstorm-experiments-new` — 为新产品设计精益创业 pretotype（Alberto Savoia）
- `identify-assumptions-existing` — 识别价值、可用性、可行性和可行性方面的风险假设
- `identify-assumptions-new` — 识别 8 个风险类别的风险假设，包括 GTM、策略和团队
- `prioritize-assumptions` — 使用影响 × 风险矩阵优先排序假设，并建议实验
- `prioritize-features` — 基于影响、工作量、风险和战略对齐度优先排序功能待办
- `analyze-feature-requests` — 按主题和战略契合度分析和分类功能请求
- `opportunity-solution-tree` — 构建机会解决方案树（Teresa Torres）— 结果 → 机会 → 方案 → 实验
- `interview-script` — 创建带有 JTBD 探究问题的结构化客户访谈脚本
- `summarize-interview` — 将访谈记录总结为 JTBD、满意度信号和行动项
- `metrics-dashboard` — 设计包含 North Star、输入指标和告警阈值的产品指标看板

**命令（5）：**

- `/discover` — 完整发现周期：构思 → 假设映射 → 优先排序 → 实验设计
- `/brainstorm` — 多视角构思（`ideas|experiments` × `existing|new`）
- `/triage-requests` — 分析和优先排序一批功能请求
- `/interview` — 准备访谈脚本或总结记录（`prep|summarize`）
- `/setup-metrics` — 设计产品指标看板

</details>

<details>
<summary><strong>2. pm-product-strategy</strong> — 愿景、商业模式、定价、竞争格局（12 个技能，5 个命令）</summary>

产品策略、愿景、商业模式、定价和宏观环境分析。覆盖从愿景制定到竞争格局扫描的完整战略工具箱。

**技能（12）：**

- `product-strategy` — 全面的 9 部分 Product Strategy Canvas（愿景 → 防御性）
- `startup-canvas` — 创业画布，结合 Product Strategy（9 部分）+ Business Model — BMC 和 Lean Canvas 的替代方案
- `product-vision` — 构思鼓舞人心、可实现且富有情感的产品愿景
- `value-proposition` — 6 部分 JTBD 价值主张（谁、为什么、之前怎样、如何做、之后怎样、替代方案）
- `lean-canvas` — 适用于初创企业的新产品的 Lean Canvas 商业模式
- `business-model` — 包含全部 9 个构建块的 Business Model Canvas
- `monetization-strategy` — 头脑风暴 3-5 个变现策略并附验证实验
- `pricing-strategy` — 定价模型、竞争分析、支付意愿和价格弹性
- `swot-analysis` — SWOT 分析及可操作建议
- `pestle-analysis` — 宏观环境：政治、经济、社会、技术、法律、环境
- `porters-five-forces` — 竞争力量分析（现有竞争、供应商、买方、替代品、新进入者）
- `ansoff-matrix` — 跨市场和产品的增长策略映射

**命令（5）：**

- `/strategy` — 创建完整的 9 部分 Product Strategy Canvas
- `/business-model` — 探索商业模式（`lean|full|startup|value-prop|all`）
- `/value-proposition` — 使用 6 部分 JTBD 模板设计价值主张
- `/market-scan` — 宏观环境分析，结合 SWOT + PESTLE + Porter's + Ansoff
- `/pricing` — 设计定价策略及竞争分析和实验

</details>

<details>
<summary><strong>3. pm-execution</strong> — PRD、OKR、路线图、Sprint、回顾、发布说明、利益相关者管理（16 个技能，11 个命令）</summary>

日常产品管理：PRD、OKR、路线图、Sprint、回顾、发布说明、事前分析、利益相关者管理、用户故事和优先级排序框架。

**技能（16）：**

- `create-prd` — 全面的 8 部分 PRD 模板
- `brainstorm-okrs` — 与公司目标对齐的团队级 OKR
- `outcome-roadmap` — 将功能列表转化为以结果为导向的路线图
- `sprint-plan` — Sprint 规划含容量估算、故事选择和风险识别
- `retro` — 结构化 Sprint 回顾引导
- `release-notes` — 从工单、PRD 或变更日志生成面向用户的发布说明
- `pre-mortem` — 风险分析含 Tigers/Paper Tigers/Elephants 分类
- `stakeholder-map` — 权力 × 利益网格及定制沟通计划
- `summarize-meeting` — 会议记录 → 决策 + 行动项
- `user-stories` — 遵循 3 C's 和 INVEST 标准的用户故事
- `job-stories` — Job stories：When [情境]，I want to [动机]，so I can [结果]
- `wwas` — Why-What-Acceptance 格式的产品待办项
- `test-scenarios` — 测试场景：正常路径、边界情况、错误处理
- `dummy-dataset` — 生成 CSV、JSON、SQL 或 Python 格式的逼真假数据集
- `prioritization-frameworks` — 9 个优先级排序框架参考指南（Opportunity Score、ICE、RICE、MoSCoW、Kano 等）
- `strategy-red-team` — 对抗性压力测试：浮现承重假设，找出导致失败的因素，按最低成本测试排序

**命令（11）：**

- `/write-prd` — 从功能想法或问题陈述创建 PRD
- `/plan-okrs` — 头脑风暴团队级 OKR
- `/transform-roadmap` — 将基于功能的路线图转化为以结果为导向
- `/sprint` — Sprint 生命周期（`plan|retro|release`）
- `/pre-mortem` — 对 PRD 或上市计划进行事前风险分析
- `/red-team-prd` — 对抗性压力测试 PRD、路线图或策略，按最低成本测试排序风险最高的假设
- `/meeting-notes` — 将会议记录总结为结构化笔记
- `/stakeholder-map` — 映射利益相关者并创建沟通计划
- `/write-stories` — 将功能拆分为待办项（`user|job|wwa`）
- `/test-scenarios` — 从用户故事生成测试场景
- `/generate-data` — 创建逼真的假数据集

</details>

<details>
<summary><strong>4. pm-market-research</strong> — 画像、细分、旅程图、市场规模、竞品分析（7 个技能，3 个命令）</summary>

用户研究和竞争分析：画像、细分、旅程图、市场规模、竞品分析和反馈分析。

**技能（7）：**

- `user-personas` — 从研究数据创建精炼的用户画像
- `market-segments` — 识别 3-5 个客户细分，含人口统计、JTBD 和产品契合度
- `user-segmentation` — 基于行为、JTBD 和需求从反馈数据中细分用户
- `customer-journey-map` — 端到端旅程图，含阶段、触点、情感和痛点
- `market-sizing` — TAM、SAM、SOM 自上而下和自下而上估算
- `competitor-analysis` — 竞品优势、弱点和差异化机会
- `sentiment-analysis` — 用户反馈的情感分析和主题提取

**命令（3）：**

- `/research-users` — 构建画像、细分用户、映射客户旅程
- `/competitive-analysis` — 分析竞争格局
- `/analyze-feedback` — 用户反馈的情感分析和细分洞察

</details>

<details>
<summary><strong>5. pm-data-analytics</strong> — SQL 生成、同期群分析、A/B 测试分析（3 个技能，3 个命令）</summary>

PM 的数据分析：SQL 查询生成、同期群分析和 A/B 测试分析。

**技能（3）：**

- `sql-queries` — 从自然语言生成 SQL（BigQuery、PostgreSQL、MySQL）
- `cohort-analysis` — 按同期群的留存曲线、功能采用和参与趋势
- `ab-test-analysis` — 统计显著性、样本量验证和发布/扩展/停止建议

**命令（3）：**

- `/write-query` — 从自然语言生成 SQL 查询
- `/analyze-cohorts` — 用户参与数据的同期群分析
- `/analyze-test` — 分析 A/B 测试结果

</details>

<details>
<summary><strong>6. pm-go-to-market</strong> — 滩头阵地、ICP、增长循环、GTM 模式、战斗卡（6 个技能，3 个命令）</summary>

上市策略：滩头阵地、理想客户画像、增长循环、GTM 模式和竞争战斗卡。

**技能（6）：**

- `gtm-strategy` — 完整 GTM 策略：渠道、信息、成功指标和上市计划
- `beachhead-segment` — 识别第一个滩头市场细分
- `ideal-customer-profile` — 含人口统计、行为、JTBD 和需求的 ICP
- `growth-loops` — 设计可持续增长循环（飞轮）
- `gtm-motions` — 评估 GTM 模式和工具（产品驱动、销售驱动等）
- `competitive-battlecard` — 面向销售的战斗卡含异议处理和制胜策略

**命令（3）：**

- `/plan-launch` — 从滩头阵地到上市计划的完整 GTM 策略
- `/growth-strategy` — 设计增长循环并评估 GTM 模式
- `/battlecard` — 创建竞争战斗卡

</details>

<details>
<summary><strong>7. pm-marketing-growth</strong> — 营销创意、定位、价值主张、命名、North Star 指标（5 个技能，2 个命令）</summary>

产品营销和增长：营销创意、定位、价值主张陈述、产品命名和 North Star 指标。

**技能（5）：**

- `marketing-ideas` — 创意、低成本的营销方案含渠道和信息
- `positioning-ideas` — 与竞品差异化的产品定位
- `value-prop-statements` — 面向营销、销售和用户引导的价值主张陈述
- `product-name` — 符合品牌价值和受众的产品命名头脑风暴
- `north-star-metric` — North Star 指标 + 输入指标含商业博弈分类

**命令（2）：**

- `/market-product` — 头脑风暴营销创意、定位、价值主张和产品名称
- `/north-star` — 定义你的 North Star 指标和支撑输入指标

</details>

<details>
<summary><strong>8. pm-toolkit</strong> — 简历审查、法律文件、校对（4 个技能，5 个命令）</summary>

核心产品工作之外的 PM 实用工具：简历审查、法律文件和校对。

**技能（4）：**

- `review-resume` — PM 简历审查和定制，基于 10 个最佳实践（XYZ+S 公式、关键词、结构）
- `draft-nda` — 含适用司法管辖区条款的保密协议
- `privacy-policy` — 覆盖 GDPR/CCPA 合规的隐私政策
- `grammar-check` — 语法、逻辑和流畅度检查并提供针对性修改

**命令（5）：**

- `/review-resume` — 全面的 PM 简历审查
- `/tailor-resume` — 针对特定职位描述定制简历
- `/draft-nda` — 起草保密协议
- `/privacy-policy` — 起草隐私政策
- `/proofread` — 检查语法、逻辑和流畅度

</details>

<details>
<summary><strong>9. pm-ai-shipping</strong> — AI 交付工具包：记录 vibe-coded 应用、审计安全和性能、映射测试覆盖、编写交付包（2 个技能，5 个命令）</summary>

面向对 AI 生成代码负责的 PM 和创始人。AI 代理写代码很快，但不留下意图记录——系统应该做什么、谁可以做什么、密钥在哪里、哪些规则被实际验证。这个工具包恢复可审查性：它记录系统，然后审计文档描述与代码实际行为之间的差距——通用扫描器遗漏的 bug 类型。

**技能（2）：**

- `shipping-artifacts` — 使 AI 构建的应用可审查的持久文档集：每个应用需要的核心文档（架构、用户/权限流程、权限、变量/密钥、测试覆盖图）加上条件性文档（邮件、定时任务、SEO、嵌入式代理/自动化）。定义每个文档必须捕获什么以及审查者如何使用它
- `intended-vs-implemented` — 找出系统文档描述与代码实际行为之间差距的方法，双面引用证据

**命令（5）：**

- `/ship-check` — 将 vibe-coded 仓库转化为可审查的交付包：文档、连接代理上下文、运行安全和性能审计、映射测试覆盖、编译结果
- `/document-app` — 将代码库逆向工程为审查者和审计者需要的系统文档——核心集（架构、流程、权限、变量）加上条件性文档（邮件、定时任务、SEO、自动化）
- `/derive-tests` — 将文档描述的意图转化为测试覆盖图：盘点现有测试、区分提议测试和未验证缺口、推荐合并前 CI 门禁
- `/security-audit-static` — 静态安全审计：映射信任边界、交叉引用文档意图、自我反驳每个发现、只报告有证据支持的风险
- `/performance-audit-static` — 静态性能审计：发现过度获取、缺失索引和缓存机会，按工作量和影响排序

</details>

---

## 关于

这个市场随产品实践和 AI 能力的发展而演进。

精选技能基于以下作者的著作：

- Teresa Torres — [*Continuous Discovery Habits*](https://www.amazon.com/Continuous-Discovery-Habits-Discover-Products/dp/1736633309/)
- Marty Cagan — [*INSPIRED*](https://www.amazon.com/INSPIRED-Create-Tech-Products-Customers/dp/1119387507/) 和 [*TRANSFORMED*](https://www.amazon.com/dp/1119697336/)
- Alberto Savoia — [*The Right It*](https://www.amazon.com/Right-Many-Ideas-Yours-Succeed/dp/0062884654)
- Dan Olsen — [*The Lean Product Playbook*](https://www.amazon.com/dp/1118960874/)
- Roger L. Martin — [*Playing to Win*](https://www.amazon.com/Playing-Win-Expanded-Bonus-Articles/dp/B0F25SDYWV/)
- Ash Maurya — [*Running Lean*](https://www.amazon.com/dp/B004J4XGN6/)
- Strategyzer — [*Business Model Generation*](https://www.amazon.com/dp/0470876417/) 和 [*Value Proposition Design*](https://www.amazon.com/dp/1118968050/)
- Christina Wodtke — [*Radical Focus*](https://www.amazon.com/Radical-Focus-Achieving-Important-Objectives/dp/0996006052)
- Anthony W. Ulwick — [*Jobs to Be Done*](https://jobs-to-be-done-book.com/)
- Alistair Croll & Benjamin Yoskovitz — [*Lean Analytics*](https://www.amazon.com/Lean-Analytics-Better-Startup-Faster/dp/1449335675/)
- Sean Ellis — [*Hacking Growth*](https://www.amazon.com/Hacking-Growth-Fastest-Growing-Companies-Breakout/dp/045149721X/)
- Maja Voje — [*Go-To-Market Strategist*](https://gtmstrategist.com/)

由 Paweł Huryn 从 [The Product Compass Newsletter](https://www.productcompass.pm) 策划。

## 与 PM Brain 组合使用

![PM Brain composes with PM Skills](.docs/images/pm-brain-pm-skills.webp)

[PM Brain](https://github.com/phuryn/pm-brain) 是产品经理的第二大脑。你笔记本上一个文件夹里的纯 markdown 文件。Claude 在回答前读取它们，回答后写入它们，每周五清扫。没有向量数据库，没有云，没有代理记忆技巧。

## 多平台支持

本仓库作为通用源，通过 `targets/` 目录下的转换脚本支持多个平台。详见 [targets/README.md](targets/README.md)。

## 贡献

参见 [CONTRIBUTING.md](CONTRIBUTING.md)。

## Windows 已知问题

如果你的 Cowork 不稳定且无法启动 VM（[claude-code/issues/27010](https://github.com/anthropics/claude-code/issues/27010)），尝试：

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-WindowStyle Hidden -Command `"if ((Get-Service CoworkVMService).Status -ne 'Running') { Start-Service CoworkVMService }`""

$trigger = New-ScheduledTaskTrigger -RepetitionInterval (New-TimeSpan -Minutes 1) -Once -At (Get-Date)

$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries

Register-ScheduledTask -TaskName "CoworkVMServiceMonitor" `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -RunLevel Highest `
  -User "SYSTEM"
```

这解决了 Windows 上 90% 的问题。
剩余 10%：打开 services.msc > 手动启动 "Claude" 服务。

## 许可证

MIT — 详见 [LICENSE](LICENSE)。
