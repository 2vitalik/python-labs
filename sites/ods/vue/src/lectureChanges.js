import { ref } from 'vue'

import { load, save } from '@core/local.js'

import { getLectureChanges, getLectureHunks } from './api.js'

// the lectures' changes against the lecturer's slides (T374 §3) without the screen: the catalogue's words, the data.
// A group's colour lives in changes.css (--g-<group>) and is the same wherever the group shows
export const GROUPS = {
  content: ['зміст', 'помилки змісту, формул, чисел'], lang: ['мова', 'російське, кальки, терміни, опечатки, граматика'],
  look: ['оформлення', 'виділення, розмітка, запис формул, заголовки, підписи'], media: ['картинки', 'таблиці-картинки й картинки'],
  set: ['склад', 'прибрано, повернуто, додано'], open: ['на рішення', 'сумнівні місця й розкладка'], todo: ['без типу', 'ще не класифіковано'],
}
export const KINDS = {
  error: ['помилка змісту', 'content'], formula: ['помилка у формулі', 'content'], number: ['помилка в числі', 'content'],
  gap: ['пропущене слово', 'content'], ref: ['посилання не туди', 'content'],
  ru: ['російський фрагмент', 'lang'], calque: ['русизм, калька', 'lang'], term: ['термін', 'lang'], typo: ['опечатка', 'lang'],
  grammar: ['граматика', 'lang'], style: ['перефразовано', 'lang'], punct: ['пунктуація', 'lang'],
  emph: ['виділення', 'look'], markup: ['розмітка слайда', 'look'], notation: ['запис формул і чисел', 'look'],
  heading: ['заголовки', 'look'], caption: ['підписи', 'look'],
  pic2text: ['таблиця-картинка → текст', 'media'], pic: ['картинка', 'media'],
  removed: ['прибрано', 'set'], restored: ['повернуто з оригіналу', 'set'], added: ['додано', 'set'],
  doubt: ['сумнівне місце', 'open'], layout: ['розкладка', 'open'], todo: ['не класифіковано', 'todo'],
}
export const SEVS = {
  3: ['критично', 'зміст був хибний: формула, число, твердження'], 2: ['суттєво', 'без правки важко зрозуміти'],
  1: ['дрібно', 'зміст зрозумілий і так'], 0: ['косметика', 'пунктуація, виділення, розмітка'],
}
export const STATUSES = { fixed: ['виправлено', 'правка вже в тексті'], open: ['чекає рішення', 'сумнівне — вирішити тобі'], noted: ['до відома', 'різниця не важить'] }
export const WHERES = {  // [word, Icon]
  text: ['текст', 'lines'], formula: ['формула', 'sigma'], table: ['таблиця', 'table'], heading: ['заголовок', 'short'],
  caption: ['підпис', 'tag'], alt: ['опис картинки', 'image'], slide: ['слайд загалом', 'win'],
}
export const ORIGINS = {
  slide: ['зі слайда', 'так на слайді лектора'], convert: ['конвертація', 'внесла конвертація pptx → md; на слайді правильно'],
  site: ['сайт', 'наслідок перенесення на сайт'],
}
export const SIZES = { S: ['S', 'до 12 символів'], M: ['M', '13–60 символів'], L: ['L', 'понад 60 символів'] }

export const sizeOf = (it) => (it.size <= 12 ? 'S' : it.size <= 60 ? 'M' : 'L')
export const groupOf = (it) => (GROUPS[it.group] ? it.group : KINDS[it.kind]?.[1] || 'todo')
export const kindWord = (it) => KINDS[it.kind]?.[0] || it.kind
export const slidePic = (it) => `/api/media/${it.slug}/orig/s${String(it.slide).padStart(2, '0')}.webp`
export const slideLink = (it) => `/lectures/${it.lec}${it.slide ? `?slide=${it.slide}` : ''}`

// every lecture's items in one list, as a reader meets them: lecture, slide, block, place in the block; `hay` — the
// words the search looks through
const hunkNo = (h) => Number(String(h || '').replace(/\D/g, '')) || 0
const at = (it) => it.edits[0]?.a?.[0] ?? 0
const order = (x, y) => x.lec - y.lec || x.slide - y.slide || hunkNo(x.hunk) - hunkNo(y.hunk) || at(x) - at(y)
const hay = (it) => [it.id, it.title, it.note, it.why, ...it.edits.flatMap((e) => [e.del, e.ins])].join('\n').toLowerCase()
export async function loadChanges() {
  const { lectures } = await getLectureChanges()
  const items = lectures.flatMap((l) => l.items.map((it) => ({ ...it, lec: it.lec ?? l.lec, slug: l.slug, edits: it.edits || [] })))
  for (const it of items) it.hay = hay(it)
  return { lectures, items: items.sort(order) }
}

// an open change shows its blocks as on the site or as their raw markdown — one choice for all, remembered here
export const raw = ref(load('chg-raw') === '1')
export const setRaw = (v) => save('chg-raw', (raw.value = v) ? '1' : '0')

// a lecture's blocks, asked once when its first change opens
const hunks = {}
export const hunksOf = (slug) => (hunks[slug] ??= getLectureHunks(slug).then((r) => r.hunks || {})
  .catch((e) => { delete hunks[slug]; throw e }))

// the row's one line: the journal's title; else «було → стало» of the first edit; else the note or the why's first line
const plain = (s) => (s || '').replace(/<\/?c-[a-z]>|\*\*|<!--[^>]*-->/g, '').replace(/\s+/g, ' ').trim()
export function lineOf(it) {
  if (it.title) return { text: it.title }
  const e = it.edits[0]
  if (e) return { del: plain(e.del), ins: plain(e.ins), more: it.edits.length - 1 }
  return { text: it.note || (it.why || '').split('\n').find((l) => l.trim())?.replace(/[*_`#>]/g, '') || kindWord(it) }
}
