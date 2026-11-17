// node app/vue/emoji/build.mjs — the picker's data (T309): CLDR names and keywords in three languages (emojibase-data,
// fetched once), our groups (groups.mjs), the game words (words/*.txt: «😎 | слова | words»), the plain symbols (symbols.mjs) and
// the colours (colors.json, made by colors.py) → src/emoji/data.json, read by the picker when it first opens:
//   groups [{ key, title, sign, items: [index] }] · items [[char, назва, name, слова, words, слова-ru, colours, version]]
// «слова» and «words» — ours first, then CLDR's
import { mkdir, readFile, readdir, writeFile } from 'node:fs/promises'

import { GROUPS, SKIP } from './groups.mjs'
import { SYMBOLS } from './symbols.mjs'

const SOURCE = 'https://cdn.jsdelivr.net/npm/emojibase-data@18.0.0'
const here = (p) => new URL(p, import.meta.url)
const text = (p) => readFile(here(p), 'utf8')

const CACHE = '../node_modules/.cache/emoji/'  // out of git with node_modules

async function cldr(path) {
  const file = CACHE + path.replace('/', '-')
  try { return JSON.parse(await text(file)) } catch { /* not fetched yet */ }
  const body = await (await fetch(`${SOURCE}/${path}`)).text()
  await mkdir(here(CACHE), { recursive: true })
  await writeFile(here(file), body)
  return JSON.parse(body)
}

const list = (s) => (s || '').split(' ').filter(Boolean)
const words = (s) => String(s).toLowerCase().replace(/[ʼ'’`]/g, '').split(/[^\p{L}\p{N}]+/u).filter((w) => w.length > 1)
// the keywords as one row of words, without those the name already has
const row = (name, tags) => [...new Set(tags.flatMap(words))].filter((w) => !words(name).includes(w)).join(' ')

const [en, uk, ru, meta] = await Promise.all(['en/data.json', 'uk/data.json', 'ru/data.json', 'meta/groups.json'].map(cldr))
const by = (rows) => Object.fromEntries(rows.map((e) => [e.emoji, e]))
const [UK, RU] = [by(uk), by(ru)]
const known = en.filter((e) => e.group !== undefined && e.group !== 2 && !SKIP.includes(e.emoji)).sort((a, b) => a.order - b.order)
const EN = by(known)
const colors = JSON.parse(await text('colors.json').catch(() => '{}'))
const extra = {}  // char → [слова, words]
for (const f of (await readdir(here('words/')).catch(() => [])).filter((f) => f.endsWith('.txt'))) {
  for (const line of (await text(`words/${f}`)).split('\n')) {
    const [char, a = '', b = ''] = line.split('|').map((s) => s.trim())
    if (!char || line.startsWith('# ')) continue
    if (!EN[char]) { console.warn(`words/${f}: unknown «${char}»`); continue }
    extra[char] = [`${extra[char]?.[0] || ''} ${a}`.trim(), `${extra[char]?.[1] || ''} ${b}`.trim()]
  }
}

const items = []
const at = {}
const index = (rec) => (at[rec[0]] ??= items.push(rec) - 1)
const two = (ours, theirs) => [...new Set([...words(ours), ...words(theirs)])].join(' ')
function emoji(char) {
  const e = EN[char], u = UK[char], r = RU[char]
  if (!e) throw new Error(`groups.mjs: unknown «${char}»`)
  const [a = '', b = ''] = extra[char] || []
  return index([char, u.label, e.label, two(a, row(u.label, u.tags || [])), two(b, row(e.label, e.tags || [])),
    r ? [...new Set([...words(r.label), ...(r.tags || []).flatMap(words)])].join(' ') : '', colors[char] || '', e.version])
}

const moved = new Set(GROUPS.flatMap((g) => list(g.first)))
const groups = GROUPS.map((g) => {
  const subs = (g.sub || []).map((name) => Number(Object.keys(meta.subgroups).find((k) => meta.subgroups[k] === name)))
  if (subs.some(Number.isNaN)) throw new Error(`groups.mjs: unknown subgroup in «${g.key}»`)
  const rest = subs.flatMap((s) => known.filter((e) => e.subgroup === s && !moved.has(e.emoji)).map((e) => e.emoji))
  return { key: g.key, title: g.title, sign: g.sign, items: [...new Set([...list(g.first), ...list(g.also), ...rest])].map(emoji) }
})
const lost = known.filter((e) => !(e.emoji in at))
if (lost.length) console.warn(`in no group: ${lost.map((e) => e.emoji).join(' ')}`)

const text_ = groups.find((g) => g.key === 'text')
for (const block of SYMBOLS) {
  for (const line of block.rows.trim().split('\n')) {
    const [char, nameUk, nameEn, a = '', b = ''] = line.split(' | ').map((s) => s.trim())
    text_.items.push(index([char, nameUk, nameEn, `${a} ${block.uk}`.trim(), `${b} ${block.en}`.trim(), '', '', 0]))
  }
}

await mkdir(here('../src/emoji/'), { recursive: true })
const out = JSON.stringify({ groups, items })
await writeFile(here('../src/emoji/data.json'), out)
console.log(`${items.length} items, ${Math.round(out.length / 1024)} KB · ${groups.map((g) => `${g.key} ${g.items.length}`).join(' · ')}`)
console.log(`game words on ${Object.keys(extra).length}, colours on ${items.filter((i) => i[6]).length}`)
