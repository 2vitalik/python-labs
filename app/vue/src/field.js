// ```field blocks: a grid of emoji cells that lines up on every OS, since CSS sizes the cell and not the emoji font.
// [x] marks the cell that just moved, (x) an effect on the field — the brackets Notion frames already used
const seg = new Intl.Segmenter('uk', { granularity: 'grapheme' })
const esc = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' })[c])

export function fieldHtml(text) {
  const rows = text.split('\n').filter((l) => l.trim()).map((line) => {
    let mark = ''
    let cells = ''
    for (const { segment: g } of seg.segment(line)) {
      if (/^\s$/.test(g) || g === ']' || g === ')') continue
      if (g === '[' || g === '(') {
        mark = g === '[' ? ' mark-a' : ' mark-b'
        continue
      }
      cells += `<span class="c${mark}">${esc(g)}</span>`
      mark = ''
    }
    return `<div>${cells}</div>`
  })
  return `<div class="field">${rows.join('')}</div>\n`
}
