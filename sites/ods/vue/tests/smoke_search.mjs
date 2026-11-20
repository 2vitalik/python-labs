// Smoke: the search over the lectures without a browser (T374, CONTRACT §6.2) — blocks, the five kinds, their order,
// terms, fixed, a query of several words, missing data, speed. The texts and data are made up.
// Run: node sites/ods/vue/tests/smoke_search.mjs
import { registerHooks } from 'node:module'
import { resolve } from 'node:path'
import { pathToFileURL } from 'node:url'

const core = resolve(import.meta.dirname, '../../../../core/ui')  // what vite.config.js calls @core
registerHooks({ resolve: (s, c, next) => next(s.startsWith('@core/') ? pathToFileURL(resolve(core, s.slice(6))).href : s, c) })
const u = (p) => pathToFileURL(resolve(import.meta.dirname, '../src', p)).href
const { engine } = await import(u('lectureEngine.js'))
const { blocksOf } = await import(u('lectureIndex.js'))
const { dist, swap } = await import(u('lectureFuzzy.js'))
const { fold } = await import(u('lectureText.js'))

let n = 0, bad = 0
const eq = (name, got, want) => { n++; const a = JSON.stringify(got), b = JSON.stringify(want); if (a !== b) { bad++; console.log(`FAIL ${name}\n  got  ${a}\n  want ${b}`) } }

const L1 = `# Тема 1. Меблі й дані

*Курс · лекція 1*

<!-- слайд 1 -->

## План лекції

1. <c-p>Стіл і стільці</c-p>
2. Дисперсія

<!-- слайд 2 -->

## 1. Стіл {#stil}

Великий **стіл** стоїть у кімнаті.

- Біля <c-b>столу</c-b> — стілець.
- Під столом лежить кіт.

<!-- правка 01-A1 -->

::: колонки

Формула $S_{1}^{2}$ і критерій Фішера.

:::

<!-- слайд 3 -->

## 2. Дисперсія

| Назва | Значення |
|:--|:--|
| дисперсія вибірки | 4 |

Метод головних компонент зменшує розмірність.

Критерій Стьюдента порівнює середні.
`
const L2 = `# Тема 2. Перевірки

<!-- слайд 1 -->

## 1. Критерії

Фішера критерій тут стоїть навпаки, а стіл — ні.

Дисперсією називають міру розкиду. Зв’язок між ознаками.

<!-- слайд 2 -->

Слайд про гістограму і квантилі.

Метод простий, а головних компонент тут нема.

<!-- слайд 3 -->

Хі-квадрат для частот.
`
const L3 = '# Тема 3. Вступ\n\nПро курс.\n\n<!-- слайд 5 -->\n\nДалі.\n'
const lectures = [{ lec: 1, slug: 'lec01', title: 'Меблі й дані', text: L1 }, { lec: 2, slug: 'lec02', title: 'Перевірки', text: L2 },
  { lec: 3, slug: 'lec03', title: 'Вступ', text: L3 }]
const lexicon = { v: 1, stop: ['біля', 'під'], lemmas: [['стіл', 'стола', 'столу', 'столом', 'столі', 'столи', 'столів'],
  ['дисперсія', 'дисперсії', 'дисперсію', 'дисперсією'], ['фішер', 'фішера', 'фішеру', 'фішером'], ['стьюдент', 'стьюдента', 'стьюденту'],
  ['критерій', 'критерію', 'критерієм', 'критерії'], ['метод', 'методу', 'методом'], ['компонента', 'компонент', 'компоненти'],
  ['головний', 'головних', 'головна'], ['зв\'язок', 'зв\'язку', 'зв\'язком']] }
const thesaurus = { v: 1, groups: [{ main: 'метод головних компонент', also: ['PCA', 'МГК'] }, { main: 'Стьюдент', also: ['Student', 'Стюдент'] },
  { main: 'дисперсія', also: ['розкид', 'variance'] }] }
const keys = { v: 1, lec02: { 2: ['як перевірити нормальність даних', 'графік розподілу'], 3: ['звʼязок частот'] },
  lec01: { 1: ['що таке pca коротко'], 3: ['навіщо зменшувати розмірність pca'] }, lec09: { 1: ['лекції нема'] } }
const find = engine(lectures, { lexicon, thesaurus, keys })
const kinds = (r) => r.hits.map((h) => h.kind)
const at = (h) => [h.lec, h.slide, h.id]

// blocks: slides, sections, bare words
const b1 = blocksOf(L1, { lec: 1 })
eq('block texts', b1.map((b) => b.text), ['Тема 1. Меблі й дані', 'Курс · лекція 1', 'План лекції', 'Стіл і стільці', 'Дисперсія', '1. Стіл',
  'Великий стіл стоїть у кімнаті.', 'Біля столу — стілець.', 'Під столом лежить кіт.', 'Формула S_1^2 і критерій Фішера.', '2. Дисперсія',
  'Назва Значення дисперсія вибірки 4', 'Метод головних компонент зменшує розмірність.', 'Критерій Стьюдента порівнює середні.'])
eq('block slides', b1.map((b) => b.slide), [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3])
eq('block sections', [b1[0].id, b1[3].id, b1[3].heading, b1[6].id, b1[6].heading, b1[11].id], ['', 'plan-lektsii', 'План лекції', 'stil', '1. Стіл', '2-dyspersiia'])
eq('heads', b1.filter((b) => b.head).map((b) => b.text), ['Тема 1. Меблі й дані', 'План лекції', '1. Стіл', '2. Дисперсія'])
eq('before the first mark — its slide', blocksOf(L3, {}).map((b) => [b.text, b.slide]), [['Тема 3. Вступ', 5], ['Про курс.', 5], ['Далі.', 5]])

// exact, then other forms: a heading first, then the lecture's order; the terms the page lights up
let r = find('стіл')
eq('стіл kinds', kinds(r), ['exact', 'exact', 'exact', 'exact', 'form', 'form'])
eq('стіл order', r.hits.map(at), [[1, 2, 'stil'], [1, 1, 'plan-lektsii'], [1, 2, 'stil'], [2, 1, '1-kryterii'], [1, 2, 'stil'], [1, 2, 'stil']])
eq('стіл counts', r.counts, { exact: 4, form: 2, typo: 0, syn: 0, sense: 0 })
eq('стіл via', r.hits.map((h) => h.via), ['', '', '', '', 'столу → стіл', 'столом → стіл'])
eq('стіл terms', [r.hits[0].terms, r.hits[4].terms, r.hits[3].terms], [['стіл'], ['стіл', 'столу', 'столом'], ['стіл']])
eq('marks hold the word', r.hits.flatMap((h) => h.marks.map(([a, b]) => fold(h.snippet.slice(a, b)))), ['стіл', 'стіл', 'стіл', 'стіл', 'столу', 'столом'])
eq('fields', Object.keys(r.hits[0]), ['kind', 'lec', 'slug', 'title', 'slide', 'id', 'heading', 'snippet', 'marks', 'terms', 'via'])
r = find('стіл', 2)
eq('cut per kind, counts in full', [kinds(r), r.counts.exact, r.counts.form], [['exact', 'exact', 'form', 'form'], 4, 2])
eq('a form asked finds the lemma', find('столом').counts, { exact: 1, form: 5, typo: 0, syn: 0, sense: 0 })
eq('и/і, е/є, case', find('ФИШЕРА').counts.exact, 2)
eq('apostrophes', [find("зв'язок").counts.exact, find('звʼязок').counts.exact], [1, 1])
eq('typed start', [find('диспер').counts.form, find('диспер').hits[0].via], [4, 'диспер… → дисперсія'])

// several words: all in one block; side by side in another order is a form
r = find('критерій фішера')
eq('two words', [kinds(r), r.hits.map((h) => h.lec), r.hits[1].via, r.hits[1].terms], [['exact', 'form'], [1, 2], 'критерій фішера → фішера критерій', ['фішера критерій']])
eq('stop words not needed', [find('кіт під столом').counts.form, find('кіт біля столом').counts.form], [1, 1])
eq('a hyphen', [find('хі квадрат').counts.form, find('хі квадрат').hits[0].terms], [1, ['хі-квадрат']])

// another layout, Latin, a slip
eq('swap', [swap('abith'), swap('cnsk'), swap('ыегвуте')], ['фішер', 'стіл', 'student'])
eq('dist', [dist('abcd', 'acbd', 2), dist('фішир', 'фішер', 1), dist('a', 'abcd', 1)], [1, 1, 2])
r = find('abith')
eq('layout', [kinds(r), r.fixed, r.hits[0].via, r.hits[0].terms], [['typo', 'typo'], 'фішер', 'abith → фішер', ['фішера']])
eq('latin', [find('fisher').fixed, find('fisher').counts.typo], ['Фішера', 2])
eq('slip', [find('фішира').fixed, find('фішира').hits[0].via], ['Фішера', 'фішира → Фішера'])
eq('slip in two words', [find('критерій фішира').fixed, kinds(find('критерій фішира'))], ['критерій Фішера', ['typo', 'typo']])
eq('no fixed when found', find('стіл').fixed, null)

// the course's names: as written, by lemmas, a word of the query
r = find('PCA')
eq('syn', [kinds(r), r.hits[0].via, r.hits[0].terms, at(r.hits[0])], [['syn', 'sense'], 'PCA = метод головних компонент', ['метод головних компонент'], [1, 3, '2-dyspersiia']])
eq('sense — only a slide the words did not find', [r.counts.sense, at(r.hits[1]), r.hits[1].via], [1, [1, 1, ''], 'за змістом: що таке pca коротко'])
eq('syn: a name scattered over a block is no name', r.counts.syn, 1)
r = find('методом головних компонент')  // the main name by lemmas: its own blocks are forms, its other names not in the texts
eq('words side by side — one phrase to light up; apart — each word, in its own hit only',
  [kinds(r), r.hits.map((h) => h.lec), r.hits[0].terms, r.hits[1].terms, r.hits[1].via],
  [['form', 'form'], [1, 2], ['метод головних компонент'], ['метод', 'головних', 'компонент'], 'метод → методом'])
eq('syn of a word', [kinds(find('стюдент')), find('стюдент').hits[0].via], [['syn'], 'стюдент = Стьюдент'])
r = find('розкид')
eq('a name the lectures use: its own blocks, then the group', [r.counts.form, r.counts.syn, r.hits.at(-1).via], [1, 3, 'розкид = дисперсія'])

// за змістом
r = find('як перевірити нормальність')
eq('sense', [kinds(r), at(r.hits[0]), r.hits[0].terms, r.hits[0].via], [['sense'], [2, 2, '1-kryterii'], [], 'за змістом: як перевірити нормальність даних'])
eq('sense snippet', [r.hits[0].snippet.startsWith('як перевірити нормальність даних — '), r.hits[0].marks.map(([a, b]) => r.hits[0].snippet.slice(a, b))],
  [true, ['перевірити', 'нормальність']])
eq('sense: apostrophes in keys', at(find("зв'язок частот").hits[0]), [2, 3, '1-kryterii'])
eq('sense skips a slide the words found', find('розмірність').counts, { exact: 1, form: 0, typo: 0, syn: 0, sense: 0 })

// no data: words as written, a slip still by the corpus
const bare = engine(lectures, {}), broken = engine(lectures, { lexicon: { v: 1 }, thesaurus: { groups: 'x' }, keys: [] })
eq('no data', [bare('стіл').counts, bare('PCA').counts.syn, bare('як перевірити нормальність').counts.sense],
  [{ exact: 4, form: 1, typo: 0, syn: 0, sense: 0 }, 0, 0])  // the form: «стілець», a word's start
eq('no data: a slip', [bare('стюдент').fixed, bare('стюдент').counts.typo], ['Стьюдента', 1])
eq('broken data', broken('стіл').counts.exact, 4)
eq('short query', [find('с').hits.length, find('  ').counts.exact, find('').fixed, find('?!').hits.length], [0, 0, null, 0])

// speed: ~5 000 blocks, a query per keystroke
const big = Array.from({ length: 15 }, (_, i) => ({ lec: i + 1, slug: `lec${i + 1}`, title: 'x', text: Array(17).fill(L1 + L2).join('\n') }))
let t = performance.now()
const fast = engine(big, { lexicon, thesaurus, keys })
fast('x')
const built = performance.now() - t, size = big.reduce((s, l) => s + blocksOf(l.text, {}).length, 0)
const qs = ['с', 'ст', 'сті', 'стіл', 'столом', 'фішира', 'критерій фішера', 'PCA', 'як перевірити нормальність', 'диспер']
fast('фішира')  // the slip's pools are made on the first slip
t = performance.now()
for (const q of qs) fast(q)
const per = (performance.now() - t) / qs.length
eq('speed per query < 30 ms', per < 30, true)
console.log(`${size} blocks: built in ${Math.round(built)} ms, ${per.toFixed(1)} ms per query`)

console.log(`${n - bad}/${n} ok`)
process.exit(bad ? 1 : 0)
