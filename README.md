# usage-status

**English** | [한국어](docs/README.ko.md) | [简体中文](docs/README.zh-CN.md)

![license](https://img.shields.io/badge/license-MIT-blue) ![version](https://img.shields.io/badge/version-0.2.1-green) ![claude code](https://img.shields.io/badge/Claude_Code-mod-orange)

A Claude Code mod that keeps **this month's API-equivalent spend** and your **5-hour / weekly plan usage** in the status line, in the terminal and in the desktop app (Code tab).

```
This month $31.05 · 5h ██░░░░░░ 24% (resets in 2h05m) · 7d ███░░░░░ 41% (resets in 3d4h)
```

Each bar is 8 cells; `!` appears at 90% or more.

## Install

At the prompt of a terminal session:

```
/plugin install usage-status --marketplace lastnamesong/claude-usage-status
```

From a shell:

```bash
claude plugin install usage-status --marketplace lastnamesong/claude-usage-status
```

In the desktop app, where `/plugin` does not run: click **+** next to the prompt box, then **Plugins**, **Add marketplace** with `lastnamesong/claude-usage-status`, then **Add plugin**.

## How it works

- **This month $**: reads the token usage Claude Code logs locally (`~/.claude/projects/**/*.jsonl`): input, output, cache writes and reads, web searches and fast mode, priced at the official API rates. Recomputed when a turn ends, at most once a minute.
- **5h / 7d**: the plan usage Claude Code receives on Pro and Max subscriptions, with the time left until each window resets. It appears after the session's first response.
- Breakdown in a terminal: `python3 <plugin folder>/scripts/month-cost.py --detail` (add `--month 2026-10` for another month).

## Notes

- The dollar figure is an **estimate** of what the same usage would cost on the API. It is not what your subscription bills.
- Only Claude Code usage on this computer is counted. Chats on claude.ai web or mobile are not.
- Prices as of October 2026 are listed in `scripts/month-cost.py`. A new model needs a row added there; until then its responses are shown as skipped in `--detail`.
- Claude Code deletes old session logs after `cleanupPeriodDays` (30 days by default). Usage from earlier in the month may already be gone, so the total can undercount; raise that setting to keep a full month.
- Requires `python3`.

## License

MIT
