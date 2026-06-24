# 修改记录

## 2026-06-23 ~ 24: QoderWork 专家套件适配

### 背景

将 [phuryn/pm-skills](https://github.com/phuryn/pm-skills) 仓库（68 个 PM 技能 + 42 个链式工作流命令，分布在 9 个 Claude 插件中）转换为 QoderWork 专家套件，同时保持仓库作为多平台通用源。

### 一、Git 远程配置

- `origin` → `https://github.com/JJasonSun/pm-skills.git`（个人 fork）
- 新增 `upstream` → `https://github.com/phuryn/pm-skills.git`（上游同步）

### 二、多平台架构

```
targets/
├── README.md                    # 多平台支持说明
└── qoderwork/
    └── convert.py               # 转换脚本（读取源文件，生成 QoderWork 插件）
```

源文件保持 Claude 原生格式不修改；各平台通过 `targets/` 下的独立脚本生成目标格式。Claude / Cowork / Gemini CLI / Cursor / Codex CLI 均直接使用根目录，无需转换。

### 三、转换脚本 `convert.py`

**68 个 skill 转换**
- 补充 `version: 1.0.0`、`user-invocable: true`
- 替换 `$ARGUMENTS` → `the user's request`
- 清理重复的 `## Metadata` 段
- 新增 `description_zh` frontmatter 字段（68 条中文翻译，保留 SWOT/RICE/OKR/PRD 等专业术语）

**42 个 command 转换**
- 新增 `convert_command_md()` 函数，将 `pm-*/commands/*.md` 转为 QoderWork skill 格式
- 提取 `description` + `argument-hint`，写入 `description_zh`、`version`、`user-invocable`
- 替换 `$ARGUMENTS` → `the user's request`
- 清理 `## Invocation` 段（Claude 专属 /command 语法）
- 新增 `COMMAND_DESCRIPTION_ZH` 映射表（42 条中文描述）

**名称冲突合并**
- 8 个命令与同名 skill 冲突：`business-model`、`draft-nda`、`pre-mortem`、`privacy-policy`、`review-resume`、`stakeholder-map`、`test-scenarios`、`value-proposition`
- 合并策略：skill 方法论保留为主体，command 工作流以 `## Workflow Orchestration` 章节追加
- `plugin.json` 去重，仅保留唯一 skill 路径

**安装方式**
- `install_plugin()` 使用 `Path.symlink_to`（软链接指向 build 目录），重新 build 后自动生效

### 四、产出

| 类型 | 数量 |
|------|------|
| Skills | 68 |
| 工作流技能（独立） | 34 |
| 工作流技能（与 skill 合并） | 8 |
| **总 skill 模块** | **102** |

**技能分组统计**

| 分组 | 原 plugin 目录 | 方法论技能 | 工作流技能 |
|------|---------------|-----------|-----------|
| 产品战略 | pm-product-strategy | 12 | 5 |
| 产品发现 | pm-product-discovery | 13 | 5 |
| 执行落地 | pm-execution | 16 | 11 |
| 市场研究 | pm-market-research | 7 | 3 |
| 数据分析 | pm-data-analytics | 3 | 3 |
| 上市策略 | pm-go-to-market | 6 | 3 |
| 营销增长 | pm-marketing-growth | 5 | 2 |
| 通用工具 | pm-toolkit | 4 | 5 |
| AI 交付 | pm-ai-shipping | 2 | 5 |
| **合计** | | **68** | **42** |

### 五、其他文件

- `README_zh.md` — 原版 README 的完整中文翻译，含 9 个插件详情和 QoderWork 安装指引
- `README.md` — 增加语言切换链接 `English | [中文](README_zh.md)`
- `targets/README.md` — 多平台支持文档，含上游同步说明

### 六、源文件改动

- 无。所有 `pm-*/skills/*/SKILL.md` 和 `pm-*/commands/*.md` 保持原样，Claude 兼容性完整保留。
- `.claude-plugin/marketplace.json` 未转换（Claude 市场元数据，QoderWork 使用 `.qoder-plugin/plugin.json`）。

### 验证

```bash
# 构建并安装
python3 targets/qoderwork/convert.py --output ./build/qoderwork/
# → Skills: 68, Commands: 42, Merged: 8, Total unique: 102

python3 validate_plugins.py
# → ✓ ALL CHECKS PASSED (0 warnings)

# 工作流技能存在性检查
ls build/qoderwork/skills/ | grep -E "discover|write-prd|plan-launch|north-star|strategy"

# 合并 skill 内容检查
grep "Workflow Orchestration" build/qoderwork/skills/pre-mortem/SKILL.md

# 软链接检查
ls -ld ~/.qoderworkcn/plugins-custom/pm-skills
# → lrwxr-xr-x ... pm-skills -> /Users/jjsun/WorkSpace/pm-skills/build/qoderwork
```
