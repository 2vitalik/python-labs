import { STATES, doneOf, fmtWhen, labName } from './labs.js'
import { site } from './site.js'

// the columns of /table (T240, T315 §3): where a row's facts come from and how they read; the page picks and orders them.
// a column: key · type (table.js knows how each filters, sorts, sums) · name · short (the narrow header) · get(row) ·
// group (the band above its header: «Лаба 2») · cat (its section of the catalog: «Лаба») · lab (the lab it is of) ·
// fam (a family: like columns stand in one line of the catalog, the first leads) · title (the full name, for a hover)
const P = 'Профіль'
const R = 'Репозиторій'
const col = (key, group, type, name, short, get, more = {}) => ({ key, group, cat: group, type, name, title: name, short, get, ...more })
export const REG = { full: { emoji: '✅', text: 'усе: сайт, бот, GitHub', color: 'green' }, part: { emoji: '🟡', text: 'частина', color: 'yellow' }, none: { emoji: '❌', text: 'нічого', color: 'red' } }
export const REPO = { ok: { emoji: '🟢', text: 'клоновано, доступ є', color: 'green' }, err: { emoji: '⚠️', text: 'нема доступу', color: 'red' }, new: { emoji: '🐙', text: 'ще не тягнули' } }
export const EXT = { until: { emoji: '⏳', text: 'подовжено до дати', color: 'yellow' }, open: { emoji: '⏳', text: 'подовжено, дата невідома', color: 'orange' } }
export const MET = { yes: { emoji: '✅', text: 'вклався — слово викладача', color: 'green' }, no: { emoji: '❌', text: 'не вклався — слово викладача', color: 'red' } }
export const VERDICT = { done: { emoji: '🟢', text: 'зроблено', color: 'green' }, partial: { emoji: '🟡', text: 'частково', color: 'yellow' }, none: { emoji: '🔴', text: 'нема', color: 'red' } }
export const KIND = { game: { emoji: '🎮', text: 'гра на клітинках', color: 'green' }, tasks: { emoji: '📝', text: 'вправи без гри', color: 'yellow' }, other: { emoji: '🧩', text: 'інший код', color: 'orange' }, none: { emoji: '∅', text: 'коду нема', color: 'red' } }
const TONE = { ok: 'green', bad: 'red', meh: 'yellow' }
const LAB = Object.fromEntries(Object.entries(STATES).map(([k, s]) => [k, { emoji: s.emoji, text: s.text, color: TONE[s.cls] }]))
const FIELD = { bool: 'bool', select: 'enum', multi: 'multi', number: 'number', text: 'text', date: 'date' }

// registered everywhere (the first deadline's bar): the site, the bot, a GitHub link — and what is missing
const STEPS = [['🔑', (r) => r.seen], ['🤖', (r) => r.tg_linked], ['🐙', (r) => !!r.github]]
const missing = (r) => STEPS.filter(([, f]) => !f(r)).map(([e]) => e)
const profile = () => [
  col('reg', P, 'enum', 'Реєстрація: сайт, бот, GitHub', '🎫', (r) => ['full', 'part', 'part', 'none'][missing(r).length],
      { options: REG, sub: (r) => (missing(r).length % 3 ? `без ${missing(r).join(' ')}` : '') }),
  col('group', P, 'text', 'Група', 'Група', (r) => r.group, { fam: 'who' }),
  col('fio', P, 'bool', 'ПІБ заповнено', '🪪', (r) => r.fio, { fam: 'who' }),
  col('email', P, 'text', 'Пошта', '📧', (r) => r.email, { fam: 'who' }),
  col('seen', P, 'bool', 'Заходив на сайт', '🔑', (r) => r.seen, { fam: 'site', hint: (r) => r.seen_at && `перший вхід ${fmtWhen(r.seen_at)}` }),
  col('last', P, 'date', 'Останній візит', '👁', (r) => r.last_seen_at, { fam: 'site' }),
  col('bot', P, 'bool', 'Бот привʼязаний', '🤖', (r) => r.tg_linked, { fam: 'tg', hint: (r) => r.tg_linked_at && `з ${fmtWhen(r.tg_linked_at, true)}` }),
  col('tg', P, 'text', 'Нік у Telegram', '✈️', (r) => r.tg_username, { fam: 'tg', link: (r) => r.tg_username && `https://t.me/${r.tg_username}` }),
  // the lessons with attendance taken (attendance_read.summary): how many the student was at, of how many for the group
  col('att', P, 'number', 'Був на парах', '🎓', (r) => r.attendance?.seen, { fam: 'att', sub: (r) => (r.attendance?.total ? `з ${r.attendance.total}` : ''),
      hint: (r) => r.attendance && `разом ${r.attendance.minutes} хв` }),
  col('attlast', P, 'date', 'Остання пара, де був', '🎓ⁿ', (r) => r.attendance?.last, { fam: 'att' }),
]
const repo = () => [
  col('gh', R, 'link', 'Посилання на GitHub', '🐙', (r) => r.github, { fam: 'repo' }),
  col('repo', R, 'enum', 'Репозиторій на диску викладача', '💾', (r) => (r.repo ? (r.repo.ok ? 'ok' : 'err') : r.github ? 'new' : null),
      { fam: 'repo', options: REPO, hint: (r) => r.repo?.error || (r.repo && `pull ${fmtWhen(r.repo.pulled_at)}`) }),
  col('commits', R, 'number', 'Комітів усього', 'Σ', (r) => r.repo?.commits, { fam: 'commits' }),
  col('firstc', R, 'date', 'Перший коміт', '⎇¹', (r) => r.repo?.first, { fam: 'commits' }),
  col('lastc', R, 'date', 'Останній коміт', '⎇ⁿ', (r) => r.repo?.last, { fam: 'commits' }),
]
function lab(n) {
  const g = labName(n)
  const c = (r) => r.labs[n]
  const m = (r) => c(r).mark || {}
  const L = (key, type, name, short, get, more = {}) => ({ ...col(`lab${n}${key}`, g, type, name, short, get, more), cat: 'Лаба', lab: n, title: `${g}: ${name.toLowerCase()}` })
  return [
    L('', 'lab', 'Стан', '📅', (r) => c(r).state, { fam: 'state', options: LAB, sub: (r) => (m(r).until ? { pre: '→', at: m(r).until } : c(r).facts.last && { at: c(r).facts.last }) }),
    L('.due', 'date', 'Дедлайн студента', '⏰', (r) => c(r).due, { fam: 'state' }),
    L('.before', 'number', 'Комітів до дедлайну', '⎇←', (r) => c(r).facts.before, { fam: 'labc' }),
    L('.after', 'number', 'Комітів після дедлайну', '⎇→', (r) => c(r).facts.after, { fam: 'labc' }),
    L('.last', 'date', 'Останній коміт до дедлайну', '🕒', (r) => c(r).facts.last, { fam: 'labc' }),
    L('.review', 'enum', 'Звіт агента', '🤖', (r) => c(r).review?.verdict, { fam: 'review', options: VERDICT, hint: (r) => c(r).review?.summary, sub: (r) => doneOf(c(r).review?.required) }),
    L('.required', 'text', 'Обовʼязкових зроблено на зрізі', '✔/6', (r) => doneOf(c(r).review?.required) || null, { fam: 'review' }),
    L('.kind', 'enum', 'Що за код (звіт агента)', '🎮', (r) => c(r).review?.kind || null, { fam: 'review', options: KIND, hint: (r) => c(r).review?.summary }),
    L('.asked', 'bool', 'Просив подовжити', '🙋', (r) => m(r).asked, { fam: 'ext', edit: 'mark', field: 'asked', sub: (r) => m(r).asked_for }),
    L('.asked_for', 'text', 'На скільки просив', '🙋…', (r) => m(r).asked_for, { fam: 'ext', edit: 'mark', field: 'asked_for' }),
    L('.ext', 'enum', 'Подовження', '⏳', (r) => (m(r).until ? 'until' : m(r).open ? 'open' : null), { fam: 'ext', options: EXT, sub: (r) => m(r).until && { at: m(r).until } }),
    L('.met', 'enum', 'Слово викладача', '✍', (r) => (m(r).met === true ? 'yes' : m(r).met === false ? 'no' : null), { fam: 'ext', options: MET }),
    L('.note', 'text', 'Нотатка', '📝', (r) => m(r).note, { edit: 'mark', field: 'note' }),
  ]
}
// what an answer claims, checked against what the site sees — by the answer's emoji (the «Перший дедлайн» poll and its kin)
const BASE = { '🌐': (r) => r.seen, '💬': (r) => r.tg_linked, '🤖': (r) => r.tg_linked, '🐙': (r) => !!r.github, '⬇️': (r) => !!r.repo?.commits }
const FACTS = { ...BASE, '✅': (r) => Object.values(BASE).every((f) => f(r)) }  // «зробив усе» — every fact at once
const claims = (p) => Object.fromEntries(p.options.map((o, i) => [String(i), FACTS[o.emoji]]).filter(([, f]) => f))
// the answers the student gave that the site does not see: «🐙» with no link in the profile
const doubtful = (p, checks) => (r) => (r.polls[p.id]?.ids || []).map(String).filter((id) => checks[id] && !checks[id](r))
function polls(list) {
  return list.flatMap((p) => {
    const checks = claims(p)
    const more = { tags: p.tags, poll: p, fam: `poll.${p.id}` }
    const poll = col(`poll.${p.id}`, 'Опитування', 'poll', p.title, p.title, (r) => r.polls[p.id]?.ids.map(String), { ...more,
      options: Object.fromEntries(p.options.map((o, i) => [String(i), { emoji: o.emoji || String(i + 1), text: o.text }])),
      hint: (r) => r.polls[p.id] && `голос ${fmtWhen(r.polls[p.id].at)}`, doubt: doubtful(p, checks),
    })
    if (!Object.keys(checks).length) return [poll]
    return [poll, { ...col(`poll.${p.id}.doubt`, 'Опитування', 'bool', 'Відповідь розходиться з фактами сайту', '⚖️', (r) => poll.doubt(r).length > 0, { ...more,
      hint: (r) => poll.doubt(r).map((id) => `${poll.options[id].emoji} ${poll.options[id].text} — сайт цього не бачить`).join('\n') || (r.polls[p.id] ? 'збігається' : '') }),
      title: `${p.title}: відповідь розходиться з фактами сайту` }]
  })
}
// the site's part of a row: its own columns, and its /students filters as checkmarks (a filter with `table: false` has
// a column of its own among them)
const own = () => {
  const g = site.students.page || 'Сайт'
  return [...(site.table?.cols || []).map((c) => ({ group: g, cat: g, name: c.title, ...c })),
          ...site.students.facets.filter((f) => f.table !== false).map((f) => col(f.key, g, 'bool', f.title, f.text.split(' ')[0], (s) => !!f.has(s)))]
}
function fields(list, labs) {
  const make = (f, n) => ({ ...col(n ? `f.${f.key}.${n}` : `f.${f.key}`, n ? labName(n) : 'Свої', FIELD[f.type], f.title, f.emoji || f.title, (r) => r.fields[n ? `${f.key}.${n}` : f.key] ?? null,
    { options: Object.fromEntries(f.options.map((o) => [o.id, o])), edit: 'field', field: f, own: true }), ...(n ? { cat: 'Лаба', lab: n, title: `${labName(n)}: ${f.title}` } : {}) })
  return list.flatMap((f) => (f.scope === 'lab' ? labs.map((n) => make(f, n)) : [make(f, 0)]))
}

export function columns(data) {
  const labs = data.labs.map((l) => l.n)
  return [...profile(), ...repo(), ...labs.flatMap(lab), ...polls(data.polls), ...own(), ...fields(data.fields, labs)]
}
// the lab a view speaks of when it does not say: the one whose deadline is nearest to now
export function nearestLab(labs) {
  const at = (l) => Math.min(...l.deadlines.map((d) => Math.abs(new Date(d.at) - Date.now())), Infinity)
  return [...labs].sort((a, b) => at(a) - at(b))[0]?.n || 1
}
