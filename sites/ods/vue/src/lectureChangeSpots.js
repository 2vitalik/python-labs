// where a change's edits stand in a block's raw text (T374 PAGE §4), and that text with them lit, for the «розмітка» view
const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c])
export const pale = (r) => r.cls.includes('pale')

// python counts code points, a JS string — UTF-16 units: past an astral character (𝑥) the catalogue's offsets move
function units(text) {
  if (!/[\uD800-\uDFFF]/.test(text)) return (i) => i
  const map = [0]
  for (const ch of text) map.push(map.at(-1) + ch.length)
  return (i) => map[Math.min(i, map.length - 1)]
}
function nearest(text, frag, s) {
  let best = -1
  for (let i = text.indexOf(frag); i >= 0; i = text.indexOf(frag, i + 1)) if (best < 0 || Math.abs(i - s) < Math.abs(best - s)) best = i
  return best
}

// the catalogue at times gives an edit's words bare (no `**`, colour tags, line breaks) while its offsets are the raw text's
const bare = (s) => s.replace(/<\/?c-[a-z]>|[*\\]/g, '').replace(/\s+/g, ' ').trim()

// [{s, e, frag, cls, js?}] → where the words really stand (a stale offset is found again by them, the nearest), in order;
// of two that overlap the strong one stays. `js` — offsets already in UTF-16 units
export function locate(text, ranges) {
  const cp = units(text), out = []
  for (const r of [...ranges].sort((x, y) => pale(x) - pale(y))) {
    const u = r.js ? (i) => i : cp
    let s = Math.min(u(r.s), text.length), e = Math.min(Math.max(u(r.e), s), text.length)
    if (r.frag && bare(text.slice(s, e)) !== bare(r.frag)) {
      const i = nearest(text, r.frag, s)
      if (i >= 0) [s, e] = [i, i + r.frag.length]
    }
    if (!out.some((o) => (s < o.e && e > o.s) || (s === e && s >= o.s && s <= o.e))) out.push({ ...r, s, e })
  }
  return out.sort((x, y) => x.s - y.s || x.e - y.e)
}

export function markRaw(text, ranges) {
  let out = '', at = 0
  for (const r of ranges) {
    out += `${esc(text.slice(at, r.s))}<mark class="chg ${r.cls}">${esc(text.slice(r.s, r.e))}</mark>`
    at = r.e
  }
  return out + esc(text.slice(at))
}
