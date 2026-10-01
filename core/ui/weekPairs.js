import { best, worst } from './weekSum.js'

// two classes instead of one: the pairs of windows that leave the fewest people with no class to come to.
// The windows are best()'s: none of them runs into another
export function pairs(laid, list, len, count) {
  const tops = best(list, len)
  const red = new Map(tops.map((w) => [w, laid.map(({ cells }) => worst(cells[w.day], w.r0, w.r0 + w.n) === 'no')]))
  const out = []
  tops.forEach((a, i) => tops.slice(i + 1).forEach((b) => {
    const [ra, rb] = [red.get(a), red.get(b)]
    const none = laid.filter((_, k) => ra[k] && rb[k]).map(({ s }) => s)
    const onlyA = ra.filter((x, k) => !x && rb[k]).length
    const onlyB = rb.filter((x, k) => !x && ra[k]).length
    out.push({ a, b, none, onlyA, onlyB, both: laid.length - none.length - onlyA - onlyB })
  }))
  return out.sort((x, y) => x.none.length - y.none.length || x.a.no + x.b.no - y.a.no - y.b.no).slice(0, count)
}
