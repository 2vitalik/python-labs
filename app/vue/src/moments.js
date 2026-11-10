// a game's examples cut into a legend and frames (T274 §8), the text itself unchanged: a frame is its caption (the paragraphs
// before a ```field grid), the grid and the quoted notes right after it; the legend is what comes before the first frame.
// Nothing is dropped: the text after the last grid stays with the last frame
const GRID = /^```(field)?\s*$/  // a bare fence counts too: some grids were written without the word
const MARK = /^\*\*[^*\n]*момент[^*\n]*\*\*:?$/i  // «**Приклад ігрового моменту**» — the frames start right after it
const PLAIN = /^(?!(?:[-*+] |\d+\. |[>#|]|```)|\*\*[^*\n]+\*\*:?$)/  // a caption's paragraph: not a list, quote, heading, table, code or bold label

// paragraphs and fenced blocks in order, each as {text, grid, quote}
function blocks(text) {
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

const join = (list) => list.map((b) => b.text).join('\n\n')

export function moments(text) {
  const bs = blocks(text || '')
  const grids = bs.flatMap((b, i) => (b.grid ? [i] : []))
  if (!grids.length) return { legend: text || '', frames: [] }
  // the first caption: what follows the «moment» label; without one, the plain paragraphs right before the grid
  const mark = bs.slice(0, grids[0]).findLastIndex((b) => MARK.test(b.text))
  let start = mark + 1
  if (mark < 0) for (start = grids[0]; start > 0 && PLAIN.test(bs[start - 1].text); start--);
  let from = start
  const frames = grids.map((g, k) => {
    let end = g + 1
    while (end < bs.length && bs[end].quote) end++
    if (k === grids.length - 1) end = bs.length
    const frame = join(bs.slice(from, end))
    from = end
    return frame
  })
  return { legend: join(bs.slice(0, start)), frames }
}
