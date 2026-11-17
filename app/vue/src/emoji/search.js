// the search of the emoji picker (T309). Every word of the query must hit something of an item — its name, one of its
// words (ours and CLDR's, three languages) or its colour — and the nearer the hit, the higher the item; what stands at
// the head of its group (hand-picked as the likeliest in a game) gets ahead of an equal hit elsewhere. A word in another
// case or a diminutive («стіни», «квадратик») hits by its stem. Nothing found — the same keys in the other keyboard
// layout are tried («ghbdbl» → «привид»)
export const COLORS = [  // letter of emoji/colors.py · name · its paint on a chip · the words that ask for it
  ['r', 'червоний', '#e53935', 'червоний красный red'],
  ['o', 'помаранчевий', '#fb8c00', 'помаранчевий оранжевий оранжевый orange'],
  ['y', 'жовтий', '#fdd835', 'жовтий золотий желтый yellow'],
  ['g', 'зелений', '#43a047', 'зелений зеленый green'],
  ['b', 'синій', '#1e88e5', 'синій блакитний голубий синий голубой blue cyan'],
  ['p', 'фіолетовий', '#8e24aa', 'фіолетовий бузковий фиолетовый purple violet'],
  ['k', 'рожевий', '#f48fb1', 'рожевий розовый pink'],
  ['n', 'коричневий', '#795548', 'коричневий брунатний коричневый brown'],
  ['d', 'чорний', '#212121', 'чорний темний черный black dark'],
  ['s', 'сірий', '#9e9e9e', 'сірий срібний серый gray grey silver'],
  ['w', 'білий', '#fafafa', 'білий белый white'],
]
const EN = "qwertyuiop[]asdfghjkl;'zxcvbnm,.", UK = 'йцукенгшщзхїфівапролджєячсмитьбю'
const ENDS = /(?:ями|ами|ові|еві|ого|ому|ими|іми|ий|ій|ою|ею|ах|ях|ам|ям|ом|ем|ів|їв|es|[аяоеєіїиуюьs])$/

export const fold = (s) => String(s).toLowerCase().replace(/[ʼ'’`]/g, '').replace(/ґ/g, 'г').replace(/ё/g, 'е')
export const wordsOf = (s) => fold(s).split(/[^\p{L}\p{N}]+/u).filter(Boolean)
export const stem = (w) => (w.length > 4 ? w.replace(ENDS, '') : w)
export const swapped = (q) => [...q.toLowerCase()].map((c) => UK[EN.indexOf(c)] || EN[UK.indexOf(c)] || c).join('')
const colorOf = (q, s) => COLORS.find(([, , , ws]) => ws.split(' ').some((w) => (q.length > 2 && w.startsWith(q)) || stem(w) === s))?.[0]

// the best hit of one query word in an item: [score, the word that was hit — '' when it is of the name]. A whole word
// beats a word's start, the name beats the other words
function hit(q, s, it) {
  let top = 0, why = ''
  const look = (list, exact, start, soft, named) => {
    for (const [w, ws] of list) {
      const score = w === q ? exact : w.startsWith(q) ? start + 10 * q.length / w.length
        : s.length > 2 && (ws === s || (ws.length > 4 && s.startsWith(ws) && s.length - ws.length < 4)) ? soft : 0
      if (score > top) [top, why] = [score, named ? '' : w]
    }
  }
  look(it.names, 92, 70, 50, true)
  look(it.words, 85, 55, 45)
  return [top, why]
}

// [{ it, score, why }] — why: the word that brought the item when its name did not
export function search(items, query) {
  const qs = wordsOf(query).map((q) => [q, stem(q), colorOf(q, stem(q))])
  const out = []
  for (const it of items) {
    let score = 0, why = ''
    for (const [q, s, c] of qs) {
      let [top, w] = hit(q, s, it)
      const tint = c ? it.colors.indexOf(c) : -1
      if (tint >= 0 && 36 - 6 * tint > top) [top, w] = [36 - 6 * tint, '']
      if (!top) { score = 0; break }
      score += top
      why ||= w
    }
    if (score) out.push({ it, score: score + 15 * Math.max(0, 1 - it.rank / 60) - it.i / 1e7, why })
  }
  return out.sort((a, b) => b.score - a.score)
}

// { rows, as } — as: the query as read in the other layout, when only that found something
export function find(items, query) {
  const same = items.find((it) => it.char === query.trim())  // the icon itself, typed or pasted
  if (same) return { rows: [{ it: same, score: 1, why: '' }] }
  const rows = search(items, query)
  const other = swapped(query)
  if (rows.length || other === query.toLowerCase()) return { rows }
  const again = search(items, other)
  return again.length ? { rows: again, as: other } : { rows }
}

// icons for a thing by its words («Привид ворог»): all the words at once first, then each word's best few
export function suggest(items, hint, most = 11) {
  const seen = new Set(search(items, hint).slice(0, 4).map((r) => r.it))
  for (const w of wordsOf(hint)) if (w.length > 2) for (const r of search(items, w).slice(0, 5)) if (r.score >= 44) seen.add(r.it)
  return [...seen].slice(0, most)
}
