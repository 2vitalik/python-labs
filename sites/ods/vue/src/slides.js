import katex from 'katex'

// a lecture's slides: its text cut at `<!-- слайд N -->` (T166 Q2–Q3; a note may follow the number); a slide with nothing
// on it is left out. `sec` — the numbered section the slide is in, for its running head (T359 §2.2): «2. Метод…» of
// `## 2. Метод…` at the level where the text's first «N. » heading stands; '' on the slide that opens it — its title says it
const MARK = /<!--\s*слайд\s+(\d+)[^>]*-->/
const ONLY_HEADS = /^(#{1,6} [^\n]*\n+)*$/

export function slidesOf(text) {
  const all = text || ''
  const level = all.match(/^(#{2,4}) \d+\.\s/m)?.[1]
  const SEC = level && new RegExp(`^${level} (\\d+\\.\\s.*?)(?:\\s*\\{#[\\w-]+\\})?$`, 'gm')
  const parts = all.split(MARK)  // [before, n, text, n, text, …]
  const out = []
  let sec = ''
  for (let i = 0; i < parts.length; i += 2) {
    const body = parts[i].trim()
    const heads = SEC ? [...body.matchAll(SEC)] : []
    const opens = heads.length && ONLY_HEADS.test(body.slice(0, heads[0].index))
    if (body) out.push({ n: i ? Number(parts[i - 1]) : 0, text: body, sec: opens ? '' : sec })
    if (heads.length) sec = heads.at(-1)[1].replace(/\*\*/g, '')
  }
  return out
}

// the first slide is the lecture's cover: «Тема N» and the name of `title`, the course above them, the slide's own text
// (the plan) under them. Without a title — the slide's first heading, taken off the text
export const COURSE = 'Основи Data Science'
const HEAD = /^#{1,6}\s+(.+)\n*/
export function coverOf(slide, title) {
  const own = title || slide.text.match(HEAD)?.[1] || ''
  const [, topic = '', name = own] = own.match(/^(Тема\s+\d+)\.?\s*(.*)$/) || []
  return { topic, name, text: title ? slide.text : slide.text.replace(HEAD, '') }
}

// the running head is a line of text with the section's formulas
const esc = (s) => s.replace(/[&<>]/g, (c) => `&#${c.charCodeAt(0)};`)
export const headHtml = (sec) => (sec || '').split(/\$([^$]+)\$/)
  .map((s, i) => (i % 2 ? katex.renderToString(s, { throwOnError: false }) : esc(s))).join('')
