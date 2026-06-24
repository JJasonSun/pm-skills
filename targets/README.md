# pm-skills 多平台支持

本仓库是 pm-skills 的通用源，通过 `targets/` 下的转换脚本生成各平台格式的插件/套件。源文件保持 Claude 原生格式，不修改。

## 当前支持的平台

| 平台 | 目录 | 说明 |
|------|------|------|
| Claude Code / Cowork / Gemini CLI / Cursor / Codex CLI | 根目录 | 原生支持，无需转换 |
| QoderWork | `targets/qoderwork/` | Python 转换脚本 |

## QoderWork 转换

```bash
# 生成插件到 build/qoderwork/
python3 targets/qoderwork/convert.py

# 直接安装到 QoderWork
python3 targets/qoderwork/convert.py --install

# 指定输出目录 + 安装
python3 targets/qoderwork/convert.py --output ./build/qoderwork/ --install
```

### 转换内容

- 补充 `version: 1.0.0`、`user-invocable: true` 到 frontmatter
- 替换 `$ARGUMENTS` → `the user's request`
- 清理 `## Metadata` 段（与 frontmatter 重复）
- 合并 9 个 Claude plugin 为 1 个 QoderWork 套件
- 生成 `.qoder-plugin/plugin.json` 和 `README.md`

## 上游同步

本仓库 fork 自 [phuryn/pm-skills](https://github.com/phuryn/pm-skills)，`upstream` 远程已配置。同步上游更新：

```bash
# 拉取上游最新代码
git fetch upstream

# 合并到当前分支
git merge upstream/main

# 如有冲突，解决后：
# 1. 运行 validate_plugins.py 确认 Claude 侧正常
python3 validate_plugins.py

# 2. 运行 QoderWork 转换确认产出正常
python3 targets/qoderwork/convert.py --output ./build/qoderwork/

# 3. 如需更新已安装的 QoderWork 插件
python3 targets/qoderwork/convert.py --install
```

## 添加新平台

1. 在 `targets/` 下创建平台目录
2. 编写转换脚本（推荐 Python）
3. 更新本 README 的平台表格

## 源文件改动规则

- 修改 `pm-*/skills/*/SKILL.md` 前确认所有平台兼容
- 修改后运行 `python3 validate_plugins.py` 确认 Claude 侧不受影响
- 修改后运行各平台转换脚本确认产出正常