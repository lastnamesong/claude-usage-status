import type { Engine, Register, SessionRateLimit } from 'claude-code'

const LABEL: Record<string, string> = { five_hour: '5h', seven_day: '7d' }
const COST_TTL_MS = 60_000

// Time left until a window resets: "2h05m" / "3d4h"
export function untilReset(resetsAt: string | undefined, now: number): string {
  const ms = resetsAt ? Date.parse(resetsAt) - now : NaN
  if (!(ms > 0)) return ''
  const h = Math.floor(ms / 3_600_000)
  const m = Math.floor((ms % 3_600_000) / 60_000)
  return h >= 24 ? `${Math.floor(h / 24)}d${h % 24}h` : `${h}h${String(m).padStart(2, '0')}m`
}

// 8-cell usage bar: "██░░░░░░"
export function bar(percent: number): string {
  const n = Math.min(8, Math.max(0, Math.round((percent / 100) * 8)))
  return '█'.repeat(n) + '░'.repeat(8 - n)
}

export function formatLimits(limits: readonly SessionRateLimit[], now: number): string {
  return limits
    .filter(l => LABEL[l.kind])
    .map(l => {
      const left = untilReset(l.resetsAt, now)
      const pct = Math.round(l.percentUsed)
      return `${LABEL[l.kind]} ${bar(pct)} ${pct}%${pct >= 90 ? '!' : ''}${left ? ` (resets in ${left})` : ''}`
    })
    .join(' · ')
}

let cost = ''
let costAt = -Infinity
let limits = ''

async function refresh($: Engine, rateLimits?: readonly SessionRateLimit[]) {
  const now = await $.clock.now()
  if (rateLimits) limits = formatLimits(rateLimits, now)
  if (now - costAt >= COST_TTL_MS) {
    costAt = now
    try {
      const r = await $.process.run(['python3', `${$.plugin.root}/scripts/month-cost.py`], { timeoutMs: 20_000 })
      if (r.exitCode === 0) cost = r.stdout.trim()
    } catch {
      // keep the last value if the tally fails
    }
  }
  const text = [cost && `This month ${cost}`, limits].filter(Boolean).join(' · ')
  $.ui.status(text || undefined)
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    const r = await next(e)
    await refresh($)
    return r
  })

  on('session.measure', async ($, e, next) => {
    const r = await next(e)
    await refresh($, e.rateLimits)
    return r
  })
}
