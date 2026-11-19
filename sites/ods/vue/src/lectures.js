import { pages } from '@core/guide.js'
import { site } from '@core/site.js'

// what the lectures' pages share; the search over their texts is lectureSearch.js

// which lectures each lab stands on (T357 §1); a lab the reader has no page of (hidden from students, T368) is left out —
// the page asks for the guide's list (loadGuide)
export const LEC_LABS = { 1: [3, 4, 14], 2: [6, 9, 12], 3: [7, 11], 4: [8, 10], 5: [5, 13] }
export const labsOf = (n) => Object.keys(LEC_LABS).map(Number).filter((lab) => LEC_LABS[lab].includes(Number(n)) && pages.value[`lab${lab}`])

// the lectures the guide has, in order; the number stands beside a title, so it goes without «Тема N.»
export const lectures = () => site.guide.filter((s) => s.kind === 'lectures' && pages.value[s.slug])
export const shortTitle = (title) => (title || '').replace(/^Тема\s+\d+\.\s*/, '')

// `<!-- слайд N -->` (a note may follow the number) on a line of its own between blocks → the slide's number, a link
// to it; inside a block — a list item, a table, code — it stays an invisible comment
const MARK = /^<!--\s*слайд\s+(\d+)[^>]*-->$/
export function withMarks(text) {
  const lines = text.split('\n')
  let fence = false
  return lines.map((l, i) => {
    if (/^\s*```/.test(l)) fence = !fence
    const m = !fence && l.trimEnd().match(MARK)
    if (!m || lines[i - 1]?.trim() || lines[i + 1]?.trim()) return l
    return `<div class="slide-at"><a class="slide-mark" href="?slide=${m[1]}" title="Слайд ${m[1]}">${m[1]}</a></div>`
  }).join('\n')
}
