# usage-status

[English](../README.md) | [한국어](README.ko.md) | **简体中文**

![license](https://img.shields.io/badge/license-MIT-blue) ![version](https://img.shields.io/badge/version-0.2.1-green) ![claude code](https://img.shields.io/badge/Claude_Code-mod-orange)

一个 Claude Code mod，在状态栏中常驻显示**本月按 API 价格折算的费用**，以及**5 小时 / 每周订阅额度的使用率**。终端和桌面应用（Code 标签页）中均可显示。

```
This month $31.05 · 5h ██░░░░░░ 24% (resets in 2h05m) · 7d ███░░░░░ 41% (resets in 3d4h)
```

进度条共 8 格，用量达到 90% 以上会显示 `!`。

## 安装

在终端会话的提示符中：

```
/plugin install usage-status --marketplace lastnamesong/claude-usage-status
```

在 shell 中：

```bash
claude plugin install usage-status --marketplace lastnamesong/claude-usage-status
```

桌面应用中无法使用 `/plugin`：点击输入框旁的 **+** → **Plugins** → **Add marketplace**，输入 `lastnamesong/claude-usage-status`，然后点击 **Add plugin**。

## 工作原理

- **This month $**：读取 Claude Code 在本地记录的日志（`~/.claude/projects/**/*.jsonl`）中的 token 用量（输入、输出、缓存写入/读取、网页搜索、fast 模式），按官方 API 价格折算。每轮对话结束时重新计算，最多每分钟一次。
- **5h / 7d**：Pro 和 Max 订阅下 Claude Code 收到的额度使用率，以及距离重置的剩余时间。会话收到第一条回复后才会显示。
- 在终端查看明细：`python3 <插件目录>/scripts/month-cost.py --detail`（其他月份加 `--month 2026-10`）。

## 注意

- 金额是同等用量按 API 计费的**估算值**，不是订阅的实际扣费。
- 只统计本机上的 Claude Code 用量，不包括 claude.ai 网页版或移动端的聊天。
- 价格为 2026 年 10 月的官方价格，写在 `scripts/month-cost.py` 中。新模型需要在表中添加一行，在此之前其用量会在 `--detail` 中显示为已跳过。
- Claude Code 会删除超过 `cleanupPeriodDays`（默认 30 天）的旧会话日志。月初的用量可能已被清除，合计可能偏低；要统计整月请调大该设置。
- 需要 `python3`。

## 许可证

MIT
