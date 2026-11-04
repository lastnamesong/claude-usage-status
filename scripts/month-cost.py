#!/usr/bin/env python3
"""Tally this month's Claude Code token usage from local logs (~/.claude/projects/**/*.jsonl) at API prices (USD).
An estimate of what the usage would cost on the API, not what a subscription is billed.
Usage: month-cost.py            -> "$12.34"
       month-cost.py --detail   -> per-model table
      month-cost.py --month 2026-10
"""
import glob, json, os, sys
from collections import defaultdict
from datetime import datetime

# $/MTok: (input, output, cache_read). Cache writes = input x1.25 (5m) / x2 (1h). Official prices as of 2026-10.
# shortcut: prices are hardcoded; add a row here when a new model ships.
PRICES = {
    "claude-fable-5-1": (10, 50, 0.25), "claude-mythos-5-1": (10, 50, 0.25),
    "claude-fable-5": (10, 50, 1.0), "claude-mythos-5": (10, 50, 1.0),
    "claude-opus-5-5": (4, 20, 0.20), "claude-opus-5": (5, 25, 0.50),
    "claude-opus-4-8": (5, 25, 0.50), "claude-opus-4-7": (5, 25, 0.50), "claude-opus-4-6": (5, 25, 0.50),
    "claude-sonnet-5-5": (2, 10, 0.20), "claude-sonnet-5": (2, 10, 0.20), "claude-sonnet-4-6": (3, 15, 0.30),
    "claude-haiku-5-5": (0.10, 0.50, 0.01), "claude-haiku-4-5": (1, 5, 0.10),
}
WEB_SEARCH_USD = 0.01  # $10 / 1,000 searches


def price_for(model):
    if model in PRICES:
        return PRICES[model]
    for k in sorted(PRICES, key=len, reverse=True):  # match dated or suffixed model ids
        if model.startswith(k):
            return PRICES[k]
    return None


def cost(model, u):
    p = price_for(model)
    if p is None:
        return None
    inp, out, rd = p
    cc = u.get("cache_creation") or {}
    w1h = cc.get("ephemeral_1h_input_tokens", 0)
    w5m = cc.get("ephemeral_5m_input_tokens", u.get("cache_creation_input_tokens", 0) - w1h)
    usd = (u.get("input_tokens", 0) * inp + u.get("output_tokens", 0) * out
           + u.get("cache_read_input_tokens", 0) * rd + w5m * inp * 1.25 + w1h * inp * 2) / 1e6
    if u.get("speed") == "fast":
        usd *= 2
    usd += (u.get("server_tool_use") or {}).get("web_search_requests", 0) * WEB_SEARCH_USD
    return usd


def collect(month, root=os.path.expanduser("~/.claude/projects")):
    seen, by_model, unknown = set(), defaultdict(float), defaultdict(int)
    for f in glob.glob(os.path.join(root, "**", "*.jsonl"), recursive=True):
        if datetime.fromtimestamp(os.path.getmtime(f)).strftime("%Y-%m") < month:
            continue  # skip files last modified before this month
        with open(f, errors="ignore") as fh:
            for line in fh:
                if '"usage"' not in line:
                    continue
                try:
                    r = json.loads(line)
                except ValueError:
                    continue
                m, ts = r.get("message") or {}, r.get("timestamp", "")
                u, model = m.get("usage"), m.get("model", "")
                if not u or not ts or model == "<synthetic>":
                    continue
                local = datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone()
                if local.strftime("%Y-%m") != month:
                    continue
                key = (m.get("id"), r.get("requestId"))
                if key != (None, None):  # no ids -> cannot dedupe; count the line instead of merging all such lines
                    if key in seen:
                        continue  # a streamed response logs the same usage on several lines
                    seen.add(key)
                c = cost(model, u)
                if c is None:
                    unknown[model] += 1
                else:
                    by_model[model] += c
    return by_model, unknown


def _selfcheck():
    u = {"input_tokens": 1_000_000, "output_tokens": 1_000_000, "cache_read_input_tokens": 1_000_000,
         "cache_creation_input_tokens": 1_000_000,
         "cache_creation": {"ephemeral_1h_input_tokens": 1_000_000, "ephemeral_5m_input_tokens": 0}}
    assert abs(cost("claude-opus-5-5", u) - (4 + 20 + 0.2 + 8)) < 1e-9
    assert abs(cost("claude-sonnet-5-5", {**u, "speed": "fast"}) - 2 * (2 + 10 + 0.2 + 4)) < 1e-9
    assert cost("unknown-model", u) is None


if __name__ == "__main__":
    _selfcheck()
    args = sys.argv[1:]
    month = args[args.index("--month") + 1] if "--month" in args else datetime.now().strftime("%Y-%m")
    by_model, unknown = collect(month)
    total = sum(by_model.values())
    if "--detail" in args:
        print(f"{month} API-equivalent cost (estimate)")
        for k, v in sorted(by_model.items(), key=lambda x: -x[1]):
            print(f"  {k:22s} ${v:8.2f}")
        print(f"  {'Total':22s} ${total:8.2f}")
        for k, n in unknown.items():
            print(f"  (skipped {n} responses from {k}: no price listed)")
    else:
        print(f"${total:.2f}")
