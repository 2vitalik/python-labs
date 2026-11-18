// tolerant search over the RU/UA/EN mixed corpus: case + и/і + е/є folded
export const norm = (s) => String(s).toLowerCase().replace(/и/g, 'і').replace(/є/g, 'е')
export const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]))

// every match of q wrapped in <mark>; norm() keeps the length, so indices from the folded copy apply to the original
export function hl(text, q, escape = esc) {
  text = String(text ?? '')
  const n = norm(text), nq = norm(q || '')
  let out = '', i = 0, j
  while (nq && (j = n.indexOf(nq, i)) >= 0) {
    out += escape(text.slice(i, j)) + '<mark>' + escape(text.slice(j, j + nq.length)) + '</mark>'
    i = j + nq.length
  }
  return out + escape(text.slice(i))
}
// the same over rendered html: only the text between tags (already escaped by the renderer)
export const markHtml = (html, q) => (q ? html.split(/(<[^>]+>)/).map((s) => (s.startsWith('<') ? s : hl(s, q, (t) => t))).join('') : html)
