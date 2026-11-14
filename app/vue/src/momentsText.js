// a game's examples text ⇄ the moments editor's model (T276): the store stays Markdown, the editor is a form over it, and
// build(parse(text)) === text. The model, in the order the text goes:
//   before · legendTitle + legend [{ icons, name }] («- 😎 — **гравець** …» lines) · notes (features, any Markdown) · mark
//   («**Приклад ігрового моменту**») · scenarios [{ title (a «### » heading; the first may have none), frames, tail }]
// A frame is { caption, fence, grid: [[{ icon, mark: '' | 'who' | 'new' }]], note } — the paragraphs before a ```field
// grid, the grid ([x] who moved, (x) what changed — as core/ui/field.js draws them) and the quote right after it.
// A scenario's tail is the text after its last grid: nothing in a frame claims it, so the editor shows it and leaves it be
const GRID = /^```(field)?\s*$/  // a bare fence counts too: some grids were written without the word
const MARK = /^\*\*[^*\n]*момент[^*\n]*\*\*:?$/i
const PLAIN = /^(?!(?:[-*+] |\d+\. |[>#|]|```)|\*\*[^*\n]+\*\*:?$)/  // a caption's paragraph: not a list, quote, heading, table, code or bold label
const H3 = /^### (\S[^\n]*)$/
const LABEL = /^\*\*[^*\n]+\*\*:?$/
const LINE = /^- (\S.*?)([  ]— )(.*)$/  // some lines have a no-break space before the dash: kept as it was
export const FENCE = '```field'
const seg = new Intl.Segmenter('uk', { granularity: 'grapheme' })
const graphemes = (s) => [...seg.segment(s)].map((x) => x.segment)

// paragraphs and fenced blocks in order, each as {text, grid, quote}
export function blocks(text) {
  const out = []
  const lines = text.replace(/\r/g, '').split('\n')
  for (let i = 0; i < lines.length;) {
    if (!lines[i].trim()) { i++; continue }
    const start = i
    if (lines[i].startsWith('```')) {
      while (++i < lines.length && !lines[i].startsWith('```'));
      i++
    } else {
      while (i < lines.length && lines[i].trim() && !lines[i].startsWith('```')) i++
    }
    const body = lines.slice(start, i).join('\n')
    out.push({ text: body, grid: GRID.test(lines[start]), quote: body.split('\n').every((l) => l.startsWith('>')) })
  }
  return out
}
const join = (list) => list.filter(Boolean).join('\n\n')

export function parseGrid(text) {
  return text.split('\n').filter((l) => l.trim() && !l.startsWith('```')).map((line) => {
    const row = []
    let mark = ''
    for (const g of graphemes(line)) {
      if (/^\s$/.test(g) || g === ']' || g === ')') continue
      if (g === '[' || g === '(') mark = g === '[' ? 'who' : 'new'
      else { row.push({ icon: g, mark }); mark = '' }
    }
    return row
  })
}
// a marked cell's brackets take the place of the spaces around it: «▫️ ▫️[😎]⬛ 🗝️»
const cellText = (c) => (c.mark === 'who' ? `[${c.icon}]` : c.mark === 'new' ? `(${c.icon})` : c.icon)
export const gridText = (grid) => grid.map((row) => row.map((c, i) => (i && !c.mark && !row[i - 1].mark ? ' ' : '') + cellText(c)).join('')).join('\n')
export const fenced = (f, fence = f.fence) => `${fence}\n${gridText(f.grid)}\n\`\`\``
export const quoted = (note) => note.split('\n').map((l) => (l ? `> ${l}` : '>')).join('\n')

// «- ↗️, ↘️ — **щити** *(…)*» → { icons, name }; a line whose head is not a row of single emoji is not a legend's
function legendItem(line) {
  const m = line.match(LINE)
  const icons = m?.[1].split(', ')
  return icons?.every((i) => graphemes(i).length === 1 && !/^[\p{L}\p{N}\p{P}]$/u.test(i)) ? { icons, name: m[3], ...(m[2] !== ' — ' && { dash: m[2] }) } : null
}
const legendOf = (b) => { const items = b.text.split('\n').map(legendItem); return items.every(Boolean) ? items : null }

function scenario(title, list) {
  const frames = []
  let caption = []
  for (let i = 0; i < list.length; i++) {
    if (!list[i].grid) { caption.push(list[i].text); continue }
    const quote = list[i + 1]?.quote ? list[++i].text : ''
    const fence = list[i - (quote ? 1 : 0)].text
    frames.push({ caption: join(caption), fence: fence.split('\n')[0], grid: parseGrid(fence), note: quote.split('\n').map((l) => l.replace(/^> ?/, '')).join('\n') })
    caption = []
  }
  return { title, frames, tail: join(caption) }
}

export function parse(text) {
  const bs = blocks(text || '')
  const first = bs.findIndex((b) => b.grid)
  const upto = first < 0 ? bs.length : first
  const mark = bs.slice(0, upto).findLastIndex((b) => MARK.test(b.text))
  let start = mark + 1
  // without the label the moments start at the plain paragraphs (and scenario headings) right before the first grid
  if (mark < 0) for (start = upto; start > 0 && first >= 0 && (PLAIN.test(bs[start - 1].text) || H3.test(bs[start - 1].text)); start--);
  const head = bs.slice(0, mark < 0 ? start : mark)
  const at = head.findIndex((b) => legendOf(b))
  const titled = at > 0 && LABEL.test(head[at - 1].text)
  const model = {
    before: at < 0 ? '' : join(head.slice(0, at - titled).map((b) => b.text)),
    legendTitle: titled ? head[at - 1].text : '',
    legend: at < 0 ? [] : legendOf(head[at]),
    notes: join(head.slice(at + 1).map((b) => b.text)),
    mark: mark < 0 ? '' : bs[mark].text,
    scenarios: [],
  }
  for (const b of bs.slice(start)) {
    const h = !b.grid && b.text.match(H3)
    if (h || !model.scenarios.length) model.scenarios.push({ title: h ? h[1] : '', list: [] })
    if (!h) model.scenarios.at(-1).list.push(b)
  }
  model.scenarios = model.scenarios.map((s) => scenario(s.title, s.list))
  return model
}

export const legendText = (m) => (m.legend.length ? join([m.legendTitle, m.legend.map((l) => `- ${l.icons.join(', ')}${l.dash || ' — '}${l.name}`).join('\n')]) : '')
export const headText = (m) => join([m.before, legendText(m), m.notes, m.mark])
export const frameText = (f) => join([f.caption, fenced(f), f.note && quoted(f.note)])
export const scenarioText = (s) => join([s.title && `### ${s.title}`, ...s.frames.map(frameText), s.tail])
export const build = (m) => join([headText(m), ...m.scenarios.map(scenarioText)])
