import { fmtWhen } from '@core/labs.js'

// the videos of «Супровід» (T318, videos.py): rows every game has — nobody adds them as cards. What the course asks of
// whom is the guide's (/score): a demo for everyone, an async defense from 70, a video per gold card from 85
export const GROUPS = [
  { kind: 'demo', icon: '🎬', title: 'Демки', who: 'усім · умова дедлайну лаби',
    hint: 'Запис гри на 1–5 хвилин: запуск, як грається, виграш і програш' },
  { kind: 'defense', icon: '🔒', title: 'Асинхронний захист', who: 'на 70+ · без дедлайну',
    hint: 'Відео на 3–10 хвилин: пояснюєш свій код. Дедлайну нема — орієнтир лише підказує, коли зручно; після онлайн-захисту викладач може зняти' },
  { kind: 'gold', icon: '⭐', title: 'Золоті картки', who: 'на 85+ · відео на кожну',
    hint: 'Окреме відео на кожну золоту картку: як працює алгоритм. Рядок зʼявляється сам, щойно картку заявлено' },
]
const AFTER = { 1: 3, 2: 4 }  // a defense has no deadline: the lab it usually follows

export const titleOf = (v, info) => (v.kind === 'demo' ? `Демка до лаби ${v.lab}` : v.kind === 'defense' ? `Захист ${v.n}` : info(v.task)?.title || v.task)
export const anchorOf = (v) => `v-${v.slot}`

// what stands by the row's name: { text, tone: bad | ok | late | off | '' , tip }
export function tagOf(v, now = Date.now()) {
  const filled = v.versions.length > 0
  if (v.need === 'skip') return { text: 'не потрібно', tone: 'off', tip: v.why || 'викладач зняв це відео' }
  if (v.need === 'must' && !filled) return { text: 'обовʼязково', tone: 'bad', tip: v.why || 'викладач чекає це відео' }
  if (v.kind === 'demo' && v.due) {
    const day = fmtWhen(v.due, true), full = `дедлайн лаби ${v.lab} — ${fmtWhen(v.due)}`
    if (v.on_time) return { text: 'вчасно', tone: 'ok', tip: `перше посилання — до дедлайну (${fmtWhen(v.due)}); новіші версії цього не міняють` }
    if (v.on_time === false) return { text: 'після дедлайну', tone: 'late', tip: full }
    return new Date(v.due) < now ? { text: `дедлайн минув ${day}`, tone: 'bad', tip: full } : { text: `до ${day}`, tone: '', tip: full }
  }
  if (v.need === 'must') return { text: 'обовʼязково', tone: '', tip: v.why || 'викладач чекав це відео' }
  if (v.kind === 'defense' && !filled) return { text: `орієнтовно після лаби ${AFTER[v.n] || v.n}`, tone: '', tip: 'не дедлайн: можна й пізніше' }
  return null
}

// the demo whose deadline is near or gone and no link yet — for «чого бракує»
export function dueSoon(videos, days = 14, now = Date.now()) {
  return (videos || []).find((v) => v.kind === 'demo' && !v.versions.length && v.need !== 'skip' && v.due && new Date(v.due) - now < days * 864e5)
}
