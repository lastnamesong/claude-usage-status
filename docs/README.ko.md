# usage-status

[English](../README.md) | **한국어** | [简体中文](README.zh-CN.md)

![license](https://img.shields.io/badge/license-MIT-blue) ![version](https://img.shields.io/badge/version-0.2.1-green) ![claude code](https://img.shields.io/badge/Claude_Code-mod-orange)

Claude Code 상태줄에 **이번 달 API 환산 비용**과 **5시간·주간 구독 한도 사용률**을 항상 띄워 주는 mod입니다. 터미널과 데스크톱 앱(Code 탭) 모두에서 보입니다.

```
This month $31.05 · 5h ██░░░░░░ 24% (resets in 2h05m) · 7d ███░░░░░ 41% (resets in 3d4h)
```

막대는 8칸이며, 90% 이상이면 `!`가 붙습니다.

## 설치

터미널 세션의 프롬프트에서:

```
/plugin install usage-status --marketplace lastnamesong/claude-usage-status
```

셸에서:

```bash
claude plugin install usage-status --marketplace lastnamesong/claude-usage-status
```

데스크톱 앱에서는 `/plugin`이 동작하지 않습니다. 프롬프트 입력창 옆의 **+** → **Plugins** → **Add marketplace**에 `lastnamesong/claude-usage-status`를 넣은 뒤 **Add plugin**을 누르세요.

## 동작 방식

- **This month $**: Claude Code가 로컬에 남기는 로그(`~/.claude/projects/**/*.jsonl`)의 토큰 사용량(입력·출력·캐시 쓰기/읽기·웹 검색·fast 모드)을 공식 API 단가로 환산합니다. 턴이 끝날 때, 최대 1분에 한 번 계산합니다.
- **5h / 7d**: Pro·Max 구독에서 Claude Code가 받는 한도 사용률과 리셋까지 남은 시간입니다. 세션의 첫 응답 이후부터 나옵니다.
- 터미널에서 자세히 보기: `python3 <플러그인 폴더>/scripts/month-cost.py --detail` (다른 달은 `--month 2026-10`)

## 주의

- 금액은 같은 사용량을 API로 썼다면 얼마였을지의 **추정치**입니다. 구독 실제 청구액이 아닙니다.
- 이 컴퓨터의 Claude Code 사용분만 셉니다. claude.ai 웹·모바일 채팅은 포함되지 않습니다.
- 단가는 2026년 10월 기준으로 `scripts/month-cost.py`에 적혀 있습니다. 새 모델은 표에 한 줄을 추가해야 하며, 그 전까지는 `--detail`에서 제외로 표시됩니다.
- Claude Code는 `cleanupPeriodDays`(기본 30일)가 지난 세션 로그를 삭제합니다. 월초 사용량이 이미 지워졌다면 합계가 적게 나올 수 있으니, 한 달 전체를 보려면 이 설정을 늘리세요.
- `python3`가 필요합니다.

## 라이선스

MIT
