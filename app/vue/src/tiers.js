// repeats and a falling price (T291 §13, app/api/pricing.py): the n-th claim of a card in a game is worth amount × factor(n).
// Price steps `tiers` [[upto, factor], …], upto growing, 0 in the last one — «on with no end»; no steps — `max_count`
// (1 — once · N — up to N · 0 — no cap), each in full

export const repeatable = (task) => !!task?.tiers?.length || (task?.max_count ?? 1) !== 1

// how many claims of the card count; 0 — no cap
export const capOf = (task) => (task?.tiers?.length ? task.tiers.at(-1)[0] : task?.max_count ?? 1)

// one more claim still counts
export const roomFor = (task, count) => repeatable(task) && (!capOf(task) || count < capOf(task))

export function factorOf(task, n) {
  const cap = capOf(task)
  if (cap && n > cap) return 0
  const step = (task?.tiers || []).find(([upto]) => !upto || n <= upto)
  return step ? step[1] : 1
}

const FRACTIONS = [[1 / 2, '½'], [1 / 4, '¼'], [1 / 3, '⅓'], [3 / 4, '¾'], [2 / 3, '⅔']]
const frac = (f) => FRACTIONS.find(([x]) => Math.abs(x - f) < 0.005)?.[1] || String(+f.toFixed(2))

// «×½» beside a repeat's coin; '' — full price
export const factorText = (f) => (f === 1 ? '' : `×${frac(f)}`)

// claim id → its share of the price: the accepted take the dearest places, the rest follow in order (as coins_of counts);
// `task` — the card, or its entry in a passport's `tasks` (no slug there)
export function factorsOf(slug, task, claims) {
  const mine = (claims || []).filter((c) => c.task === slug)
  const placed = [...mine.filter((c) => c.status === 'accepted'), ...mine.filter((c) => c.status !== 'accepted')]
  return Object.fromEntries(placed.map((c, i) => [c.id, factorOf(task, i + 1)]))
}

// the price ladder, a line a step: ['1–3 — повна ціна', '4–10 — ×½', 'далі — ×¼']
export function ladder(task) {
  const tiers = task?.tiers || []
  const cap = capOf(task)
  if (!tiers.length) return [cap === 1 ? 'один раз' : cap ? `до ${cap} разів, кожна за повну ціну` : 'скільки завгодно, кожна за повну ціну']
  let from = 1
  const lines = tiers.map(([upto, f]) => {
    const range = !upto ? (from === 1 ? 'усі' : 'далі') : upto === from ? `${from}` : `${from}–${upto}`
    from = upto + 1
    return `${range} — ${f === 1 ? 'повна ціна' : factorText(f)}`
  })
  return cap ? [...lines, `понад ${cap} — не зараховується`] : lines
}
