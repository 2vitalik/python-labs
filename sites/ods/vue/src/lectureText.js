import { norm } from '@core/search.js'

// the lectures' words as the search sees them: markdown → plain text, folded, cut into words

// norm (case, и/і, е/є) and one apostrophe of three; the length stays, so an index in the folded text is one in the plain
export const fold = (s) => norm(s).replace(/[’ʼ]/g, "'")

// [from, to, word]: letters and digits, an apostrophe or a hyphen inside; a hyphened word gives its parts too
// («хі-квадрат» → хі, квадрат), each [from, to, part, true]
const WORD = /[\p{L}\p{N}]+(?:['-][\p{L}\p{N}]+)*/gu
export function tokens(f, parts = true) {
  const out = []
  for (const m of f.matchAll(WORD)) {
    out.push([m.index, m.index + m[0].length, m[0]])
    if (!parts || !m[0].includes('-')) continue
    let at = m.index
    for (const p of m[0].split('-')) {
      out.push([at, at + p.length, p, true])
      at += p.length + 1
    }
  }
  return out
}
export const words = (s) => tokens(fold(s), false).map((t) => t[2])

// prepositions, conjunctions, particles (UA, RU, EN): a query does not need them in the block
export const STOP = new Set(fold(`в у на з із зі зо до від од для по при про за над під перед між через без крізь о об біля після
  серед понад і й та а але або чи ні ані що щоб як коли якщо бо тому хоча ніж то же ж б би не лише тільки навіть ось от ще вже
  хай нехай саме також теж це и с к от что как the a an of in on to and or for is are be with by at from as it this that`).split(/\s+/))

// markdown → plain words; a short formula keeps its letters ($S_{1}^{2}$ → S_1^2), a long one is «…»
const FORMULA = /\$\$([^\n]+?)\$\$|\$([^\n$]+?)\$/g
const GREEK = { alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ε', varepsilon: 'ε', theta: 'θ', lambda: 'λ', mu: 'μ', nu: 'ν', xi: 'ξ',
  pi: 'π', rho: 'ρ', sigma: 'σ', tau: 'τ', phi: 'φ', varphi: 'φ', chi: 'χ', psi: 'ψ', omega: 'ω', Delta: 'Δ', Sigma: 'Σ', Omega: 'Ω', Phi: 'Φ', Xi: 'Ξ' }
const letters = (tex) => {
  // `\col{b}{…}` is the colour of a part (math.js): its key is not a letter of the formula
  const s = tex.replace(/\\col\{[a-z]\}/g, '').replace(/\\([a-zA-Z]+)/g, (_, w) => GREEK[w] || '').replace(/[{}\\]/g, '').replace(/\s+/g, ' ').trim()
  return s.length <= 15 ? s : '…'
}
export const inline = (md) => md
  .replace(FORMULA, (_, block, line) => ` ${letters(block ?? line)} `)
  .replace(/!\[[^\]]*\]\([^)]*\)/g, ' ').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1')
  .replace(/<!--[\s\S]*?(?:-->|$)/g, ' ').replace(/<\/?c-[a-z]>/g, '')  // a colour tag sits flush against its words
  .replace(/<\/?[a-zA-Z][^>]*>|\{#[\w-]+\}/g, ' ')
  .replace(/[*`\\]/g, '').replace(/\|/g, ' ').replace(/\s+/g, ' ').replace(/ ([,.;:!?)])/g, '$1').trim()
// a block's lines: without the slides' fences, a table's rule, the marks of a list, a quote, a heading
export const bare = (md) => inline(md.replace(/^[ \t]*:::.*$/gm, ' ').replace(/^[ \t|:-]+$/gm, ' ')
  .replace(/^[ \t>]*(?:(?:#{1,6}|[-*+]|\d+\.)[ \t]+)?/gm, ''))
