// Smoke: the screenless logic of /table (T315) — the state and «this lab», filters, groups, sort, a view in words, two compared.
// Run: node core/ui/tests/smoke_table.mjs
import { pathToFileURL } from 'node:url'
import { resolve } from 'node:path'

const ui = resolve(import.meta.dirname, '..')
const u = (p) => pathToFileURL(resolve(ui, p)).href
const V = await import(u('tableViews.js'))
const T = { ...(await import(u('table.js'))), ...(await import(u('tableFilter.js'))), ...(await import(u('tableOrder.js'))) }
const D = await import(u('tableDiff.js'))

let n = 0, bad = 0
const eq = (name, got, want) => { n++; const a = JSON.stringify(got), b = JSON.stringify(want); if (a !== b) { bad++; console.log(`FAIL ${name}\n  got  ${a}\n  want ${b}`) } }

// «this lab»
eq('abs lab', V.abs('lab', 2), 'lab2')
eq('abs lab.before', V.abs('lab.before', 2), 'lab2.before')
eq('abs field', V.abs('f.q.lab', 3), 'f.q.3')
eq('abs family', V.abs('polls:lab', 2), 'polls:lab2')
eq('abs plain', V.abs('commits', 2), 'commits')
eq('abs explicit', V.abs('lab1.before', 2), 'lab1.before')
eq('rel', [V.rel('lab2', 2), V.rel('lab2.before', 2), V.rel('f.q.2', 2), V.rel('lab1.x', 2), V.rel('f.lab', 2), V.rel('lab12', 1)], ['lab', 'lab.before', 'f.q.lab', 'lab1.x', 'f.lab', 'lab12'])
eq('isRel', [V.isRel('lab'), V.isRel('lab.x'), V.isRel('lab2'), V.isRel('f.q.lab'), V.isRel('group')], [true, true, false, true, false])

// columns to play with
const opts = { ok: { emoji: '✅', text: 'вчасно' }, miss: { emoji: '❌', text: 'не вклався' } }
const mk = (key, type, short, name, more = {}) => ({ key, type, short, name, title: name, get: (r) => r[key], ...more })
const cols = [mk('group', 'text', 'Група', 'Група'), mk('bot', 'bool', '🤖', 'Бот'), mk('commits', 'number', 'Σ', 'Комітів'),
  mk('lab1', 'lab', '📅', 'Стан', { lab: 1, options: opts }), mk('lab2', 'lab', '📅', 'Стан', { lab: 2, options: opts }),
  mk('lab1.before', 'number', '⎇←', 'До', { lab: 1 }), mk('lab2.before', 'number', '⎇←', 'До', { lab: 2 }),
  mk('f.q.1', 'enum', '✨', 'Якість', { lab: 1, own: true, options: {} }), mk('f.q.2', 'enum', '✨', 'Якість', { lab: 2, own: true, options: {} }),
  mk('poll.a', 'poll', 'P', 'Опит', { poll: {}, tags: ['лаба 2'], options: {} }), mk('last', 'date', '👁', 'Візит')]

// state out of a URL and back
const base = { cols: 'bot,lab,lab.before,polls:lab,fields:lab', group: 'group,lab', sort: '-commits,bot', lab: '2', 'f.bot': '1' }
const s = V.readState({}, base)
eq('state', s, { cols: ['bot', 'lab', 'lab.before', 'polls:lab', 'fields:lab'], group: ['group', 'lab'], sort: ['-commits', 'bot'], lab: 2, q: '', filters: { bot: '1' } })
eq('shown ids', V.shown(s, cols).map((c) => c.id), ['bot', 'lab', 'lab.before', 'poll.a', 'f.q.lab'])
eq('shown keys', V.shown(s, cols).map((c) => c.key), ['bot', 'lab2', 'lab2.before', 'poll.a', 'f.q.2'])
eq('saved round trip', V.toSaved(s), { cols: 'bot,lab,lab.before,polls:lab,fields:lab', group: 'group,lab', sort: '-commits,bot', lab: '2', 'f.bot': '1' })
eq('no groups', V.readState({ group: '-' }, base).group, [])
eq('default group', V.readState({}, { cols: 'bot' }).group, ['group'])
eq('url cols say it all', V.readState({ cols: 'bot' }, base).filters, {})
eq('lab kept out without rel', V.toQuery(V.readState({}, { cols: 'bot,lab1', lab: '2' }), 'x').lab, undefined)
eq('unchanged', D.changed(s, base, cols), false)
eq('family vs explicit — same', D.changed({ ...s, cols: ['bot', 'lab', 'lab.before', 'poll.a', 'f.q.lab'] }, base, cols), false)
eq('explicit lab — same', D.changed({ ...s, cols: ['bot', 'lab2', 'lab2.before', 'poll.a', 'f.q.2'] }, base, cols), false)
eq('changed sort', D.changed({ ...s, sort: ['bot'] }, base, cols), true)
eq('changed lab', D.changed({ ...s, lab: 1 }, base, cols), true)

// filters
const row = { group: '25-1', bot: true, commits: 7, lab1: 'ok', last: new Date(Date.now() - 3 * 864e5).toISOString() }
const c = (k) => cols.find((x) => x.key === k)
eq('passes', [T.passes(c('bot'), row, '1'), T.passes(c('bot'), row, '0'), T.passes(c('commits'), row, '5-'), T.passes(c('commits'), row, '-5'), T.passes(c('commits'), row, '>7'),
  T.passes(c('lab1'), row, 'miss,ok'), T.passes(c('lab2'), row, '-'), T.passes(c('lab2'), row, '+'), T.passes(c('last'), row, '~7'), T.passes(c('last'), row, '^7'), T.passes(c('last'), row, '^2'),
  T.passes(c('group'), row, '25'), T.passes(c('group'), row, '-')], [true, false, true, false, false, true, true, false, true, false, true, true, false])
eq('filterText', [T.filterText(c('bot'), '0'), T.filterText(c('commits'), '5-'), T.filterText(c('commits'), '2-9'), T.filterText(c('lab1'), 'ok,-'), T.filterText(c('last'), '~7'), T.filterText(c('group'), '+')],
  ['ні', 'від 5', '2–9', '✅ ∅', 'за 7 дн.', 'є'])

// groups inside groups, facets, sort by levels
const rows = [{ name: 'Б', group: '25-2', bot: true, commits: 1, lab1: 'ok' }, { name: 'А', group: '25-1', bot: false, commits: 5, lab1: 'miss' },
  { name: 'В', group: '25-1', bot: true, commits: 5, lab1: 'ok' }, { name: 'Г', group: '25-1', bot: true, commits: 2 }]
const g = T.groups(rows, [c('group'), c('lab1')])
eq('groups', g.map((x) => [x.text, x.rows.length, x.kids.map((k) => [k.text, k.rows.length])]), [['25-1', 3, [['✅ вчасно', 1], ['❌ не вклався', 1], ['📅 порожньо', 1]]], ['25-2', 1, [['✅ вчасно', 1]]]])
eq('facets', [T.facets(c('bot'), rows), T.facets(c('lab1'), rows).map((f) => [f.id, f.n]), T.facets(c('commits'), rows)[0].n], [[{ id: '1', text: '✅', n: 3 }], [['ok', 2], ['miss', 1]], 13])
eq('sorter', [...rows].sort(T.sorter([{ col: c('commits'), desc: true }, { col: c('bot'), desc: false }])).map((r) => r.name), ['В', 'А', 'Г', 'Б'])

// a column hidden: only the family it stood in opens
eq('hide one of a family', V.without(s, cols, 'poll.a'), ['bot', 'lab', 'lab.before', 'fields:lab'])
eq('hide a plain column', V.without(s, cols, 'bot'), ['lab', 'lab.before', 'polls:lab', 'fields:lab'])

// a column dragged: a family opens only when the move takes one out of it or cuts into it
eq('drag beside a family', V.reorder(s, cols, 'lab.before', 'bot'), ['lab.before', 'bot', 'lab', 'polls:lab', 'fields:lab'])
eq('drag to the end', V.reorder(s, cols, 'bot', ''), ['lab', 'lab.before', 'polls:lab', 'fields:lab', 'bot'])
eq('drag before a family', V.reorder(s, cols, 'bot', 'poll.a'), ['lab', 'lab.before', 'bot', 'polls:lab', 'fields:lab'])
eq('drag out of a family', V.reorder(s, cols, 'poll.a', 'bot'), ['poll.a', 'bot', 'lab', 'lab.before', 'fields:lab'])
eq('a family against itself opened', D.changed({ ...s, cols: ['bot', 'lab', 'lab.before', 'poll.a', 'fields:lab'] }, base, cols), false)

// a view in words, two views compared
eq('describe', D.describe(base, cols).map((p) => p.text), ['лаба 2', '5 колонок', 'Група › 📅', '🤖 так', 'Σ ↓, 🤖 ↑'])
const d1 = D.diff(base, { ...base, lab: '1' }, cols)
eq('diff lab only', [d1.brief, d1.lines.length], [['лаба 2 → 1'], 1])  // the poll of lab 2 is of the same family: nothing was taken out
const d2 = D.diff(base, { ...base, cols: 'lab,bot,commits', sort: '', 'f.bot': '0', 'f.commits': '5-' }, cols)
eq('diff brief', d2.brief, ['＋1 колонка', '−3 колонки', 'порядок колонок', 'сортування', 'фільтри (2)'])
eq('diff lines', d2.lines.map((l) => `${l.what}:${l.kind}:${l.text}`), ['Колонки:add:Σ Комітів', 'Колонки:del:⎇← До', 'Колонки:del:P Опит', 'Колонки:del:✨ Якість', 'Колонки:move:інший порядок',
  'Сортування:chg:Σ ↓, 🤖 ↑ → без сортування', 'Фільтри:chg:🤖 так → 🤖 ні', 'Фільтри:add:Σ від 5'])
eq('diff same', D.diff(base, { ...base }, cols).same, true)

console.log(bad ? `${bad} of ${n} failed` : `ok ${n}/${n}`)
process.exit(bad ? 1 : 0)
