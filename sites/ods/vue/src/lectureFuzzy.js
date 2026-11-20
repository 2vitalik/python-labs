import { fold } from './lectureText.js'

// a word nobody wrote → the corpus word it meant: the same keys in the other layout (abith → фішер), Latin ↔ Cyrillic
// (fisher → фішер), a slip of a letter or two (Damerau–Levenshtein: ≤ 1 up to 6 letters, ≤ 2 longer); nearest, then most used

const EN = "`qwertyuiop[]asdfghjkl;'zxcvbnm,.s']`"
const UA = "'йцукенгшщзхїфівапролджєячсмитьбюыэъё"  // the tail: the Russian layout's own keys
const toUA = new Map([...EN.slice(0, 33)].map((c, i) => [c, UA[i]]))
const toEN = new Map()
;[...UA].forEach((c, i) => toEN.has(fold(c)) || toEN.set(fold(c), EN[i]))  // и and є fold into і and е: their keys go first
export const swap = (w) => fold([...w].map((c) => (/[a-z]/.test(w) ? toUA : toEN).get(c) ?? c).join(''))

const LAT = { а: 'a', б: 'b', в: 'v', г: 'h', ґ: 'g', д: 'd', е: 'e', ж: 'zh', з: 'z', і: 'i', ї: 'i', й: 'i', к: 'k', л: 'l',
  м: 'm', н: 'n', о: 'o', п: 'p', р: 'r', с: 's', т: 't', у: 'u', ф: 'f', х: 'kh', ц: 'ts', ч: 'ch', ш: 'sh', щ: 'shch', ь: '',
  ю: 'iu', я: 'ia', "'": '', ы: 'y', э: 'e', ё: 'e', ъ: '' }
const latin = (w) => [...w].map((c) => LAT[c] ?? c).join('')
const english = (w) => w.replace(/ph/g, 'f').replace(/ck|c|q/g, 'k').replace(/w/g, 'v').replace(/x/g, 'ks').replace(/y/g, 'i')
const isLatin = (w) => /^[a-z0-9'-]+$/.test(w)

// optimal string alignment distance, given up past `max`
export function dist(a, b, max) {
  if (Math.abs(a.length - b.length) > max) return max + 1
  let pp = [], p = Array.from({ length: b.length + 1 }, (_, j) => j)
  for (let i = 1; i <= a.length; i++) {
    const c = [i]
    let low = i
    for (let j = 1; j <= b.length; j++) {
      c[j] = Math.min(p[j] + 1, c[j - 1] + 1, p[j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1))
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) c[j] = Math.min(c[j], pp[j - 2] + 1)
      low = Math.min(low, c[j])
    }
    if (low > max) return max + 1
    pp = p
    p = c
  }
  return p[b.length]
}

// (word) → { to, as, d } | null; the pools of the corpus' words by length are made on the first use
export function fixerOf(ix, lex) {
  let pools
  const cache = new Map()
  const pool = (key, w, into) => (into.get(key.length) || into.set(key.length, []).get(key.length)).push([key, w])
  const make = () => {
    pools = { cyr: new Map(), lat: new Map() }
    for (const w of ix.words) {
      if (/\p{L}/u.test(w) && w.length >= 2) pool(isLatin(w) ? english(w) : latin(w), w, pools.lat)
      if (!isLatin(w)) pool(w, w, pools.cyr)
    }
  }
  const best = (key, from, max) => {
    let out = null
    for (let len = key.length - max; len <= key.length + max; len++) {
      for (const [k, w] of from.get(len) || []) {
        const d = dist(key, k, max)
        if (d <= max && (!out || d < out.d || (d === out.d && ix.vocab.get(w).n > ix.vocab.get(out.to).n))) out = { to: w, d }
      }
    }
    return out
  }
  const fix = (w) => {
    if (w.length < 3 || /^\d+$/.test(w)) return null
    const s = swap(w)  // another layout: the word itself, or (still typing) the start of the most used one
    if (ix.vocab.has(s) || lex.knows(s)) return { to: s, d: 0 }
    const starts = s.length >= 3 && ix.words.filter((v) => v.startsWith(s)).sort((a, b) => ix.vocab.get(b).n - ix.vocab.get(a).n)[0]
    if (starts) return { to: starts, d: 0 }
    pools || make()
    const max = w.length <= 6 ? 1 : 2
    const near = (x) => (isLatin(x) ? best(english(x), pools.lat, max) : best(x, pools.cyr, max))
    return [near(w), near(s)].filter(Boolean).sort((x, y) => x.d - y.d)[0] ?? null  // ыегвуте → student → студент
  }
  return (w) => {
    if (!cache.has(w)) {
      const f = fix(w)
      cache.set(w, f && { ...f, as: ix.vocab.get(f.to)?.as ?? lex.lemma(f.to, f.to) })  // as written: the folded и/і, е/є differ
    }
    return cache.get(w)
  }
}
