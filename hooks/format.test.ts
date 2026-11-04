import { expect, test } from 'claude-code/testing'

import { bar, formatLimits, untilReset } from './register'

test('rate-limit formatting', async () => {
  const now = Date.parse('2026-11-04T10:00:00Z')
  expect(untilReset('2026-11-04T12:05:00Z', now)).toBe('2h05m')
  expect(untilReset('2026-11-07T14:00:00Z', now)).toBe('3d4h')
  expect(untilReset('2026-11-04T09:00:00Z', now)).toBe('')
  expect(bar(0)).toBe('░░░░░░░░')
  expect(bar(130)).toBe('████████')
  expect(
    formatLimits(
      [
        { kind: 'five_hour', percentUsed: 23.5, resetsAt: '2026-11-04T12:05:00Z' },
        { kind: 'seven_day', percentUsed: 95 },
        { kind: 'spend_limit', percentUsed: 10 },
      ],
      now,
    ),
  ).toBe('5h ██░░░░░░ 24% (resets in 2h05m) · 7d ████████ 95%!')
})
