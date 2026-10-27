import { STATES, fmtWhen, labName } from './labs.js'
import { site } from './site.js'

// the columns of /table (T240): where a row's facts come from and how they read; the page picks and orders them.
// a column: key · group (the header above) · type (table.js knows how each filters, sorts, sums) · title · short (the narrow header) · get(row)
const P = 'Профіль'
const R = 'Репозиторій'
const col = (key, group, type, title, short, get, more = {}) => ({ key, group, type, title, short, get, ...more })
export const REPO = { ok: { emoji: '🟢', text: 'клоновано, доступ є', color: 'green' }, err: { emoji: '⚠️', text: 'нема доступу', color: 'red' }, new: { emoji: '🐙', text: 'ще не тягнули' } }
export const EXT = { until: { emoji: '⏳', text: 'подовжено до дати', color: 'yellow' }, open: { emoji: '⏳', text: 'подовжено, дата невідома', color: 'orange' } }
export const MET = { yes: { emoji: '✅', text: 'вклався — слово викладача', color: 'green' }, no: { emoji: '❌', text: 'не вклався — слово викладача', color: 'red' } }
export const VERDICT = { done: { emoji: '🟢', text: 'зроблено', color: 'green' }, partial: { emoji: '🟡', text: 'частково', color: 'yellow' }, none: { emoji: '🔴', text: 'нема', color: 'red' } }
const TONE = { ok: 'green', bad: 'red', meh: 'yellow' }
const LAB = Object.fromEntries(Object.entries(STATES).map(([k, s]) => [k, { emoji: s.emoji, text: s.text, color: TONE[s.cls] }]))
const FIELD = { bool: 'bool', select: 'enum', multi: 'multi', number: 'number', text: 'text', date: 'date' }

const profile = () => [
  col('group', P, 'text', 'Група', 'Група', (r) => r.group),
  col('fio', P, 'bool', 'ПІБ заповнено', '🪪', (r) => r.fio),
  col('seen', P, 'bool', 'Заходив на сайт', '🔑', (r) => r.seen, { hint: (r) => r.seen_at && `перший вхід ${fmtWhen(r.seen_at)}` }),
  col('last', P, 'date', 'Останній візит', '👁', (r) => r.last_seen_at),
  col('bot', P, 'bool', 'Бот привʼязаний', '🤖', (r) => r.tg_linked, { hint: (r) => r.tg_linked_at && `з ${fmtWhen(r.tg_linked_at, true)}` }),
  col('tg', P, 'text', 'Нік у Telegram', '✈️', (r) => r.tg_username, { link: (r) => r.tg_username && `https://t.me/${r.tg_username}` }),
  col('gh', P, 'link', 'GitHub-репозиторій', '🐙', (r) => r.github),
  col('email', P, 'text', 'Пошта', '📧', (r) => r.email),
]
const repo = () => [
  col('repo', R, 'enum', 'Репозиторій на диску викладача', '💾', (r) => (r.repo ? (r.repo.ok ? 'ok' : 'err') : r.github ? 'new' : null),
      { options: REPO, hint: (r) => r.repo?.error || (r.repo && `pull ${fmtWhen(r.repo.pulled_at)}`) }),
  col('commits', R, 'number', 'Комітів усього', 'Σ', (r) => r.repo?.commits),
  col('firstc', R, 'date', 'Перший коміт', '⎇¹', (r) => r.repo?.first),
  col('lastc', R, 'date', 'Останній коміт', '⎇ⁿ', (r) => r.repo?.last),
]
function lab(n) {
  const g = labName(n)
  const c = (r) => r.labs[n]
  const m = (r) => c(r).mark || {}
  return [
    col(`lab${n}`, g, 'lab', `${g}: стан`, '📅', (r) => c(r).state, { options: LAB, lab: n, sub: (r) => (m(r).until ? `→ ${fmtWhen(m(r).until, true)}` : c(r).facts.last && fmtWhen(c(r).facts.last, true)) }),
    col(`lab${n}.before`, g, 'number', `${g}: комітів до дедлайну`, '⎇←', (r) => c(r).facts.before),
    col(`lab${n}.after`, g, 'number', `${g}: комітів після дедлайну`, '⎇→', (r) => c(r).facts.after),
    col(`lab${n}.last`, g, 'date', `${g}: останній коміт до дедлайну`, '🕒', (r) => c(r).facts.last),
    col(`lab${n}.due`, g, 'date', `${g}: дедлайн студента`, '⏰', (r) => c(r).due),
    col(`lab${n}.asked`, g, 'bool', `${g}: просив подовжити`, '🙋', (r) => m(r).asked, { edit: 'mark', lab: n, field: 'asked', sub: (r) => m(r).asked_for }),
    col(`lab${n}.asked_for`, g, 'text', `${g}: на скільки просив`, '🙋…', (r) => m(r).asked_for, { edit: 'mark', lab: n, field: 'asked_for' }),
    col(`lab${n}.ext`, g, 'enum', `${g}: подовження`, '⏳', (r) => (m(r).until ? 'until' : m(r).open ? 'open' : null), { options: EXT, sub: (r) => m(r).until && fmtWhen(m(r).until, true) }),
    col(`lab${n}.met`, g, 'enum', `${g}: слово викладача`, '✍', (r) => (m(r).met === true ? 'yes' : m(r).met === false ? 'no' : null), { options: MET }),
    col(`lab${n}.note`, g, 'text', `${g}: нотатка`, '📝', (r) => m(r).note, { edit: 'mark', lab: n, field: 'note' }),
    col(`lab${n}.review`, g, 'enum', `${g}: звіт агента`, '🤖', (r) => c(r).review?.verdict, { options: VERDICT, hint: (r) => c(r).review?.summary }),
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
    const poll = col(`poll.${p.id}`, 'Опитування', 'poll', p.title, p.title, (r) => r.polls[p.id]?.ids.map(String), {
      options: Object.fromEntries(p.options.map((o, i) => [String(i), { emoji: o.emoji || String(i + 1), text: o.text }])),
      hint: (r) => r.polls[p.id] && `голос ${fmtWhen(r.polls[p.id].at)}`, tags: p.tags, poll: p, doubt: doubtful(p, checks),
    })
    if (!Object.keys(checks).length) return [poll]
    return [poll, col(`poll.${p.id}.doubt`, 'Опитування', 'bool', `${p.title}: відповідь розходиться з фактами сайту`, '⚖️', (r) => poll.doubt(r).length > 0,
      { tags: p.tags, poll: p, hint: (r) => poll.doubt(r).map((id) => `${poll.options[id].emoji} ${poll.options[id].text} — сайт цього не бачить`).join('\n') || (r.polls[p.id] ? 'збігається' : '') })]
  })
}
// the site's part of a row: its own columns, and its /students filters as checkmarks
const own = () => [
  ...(site.table?.cols || []).map((c) => ({ group: site.students.page || 'Сайт', ...c })),
  ...site.students.facets.map((f) => col(f.key, site.students.page || 'Сайт', 'bool', f.title, f.text.split(' ')[0], (s) => !!f.has(s))),
]
function fields(list, labs) {
  const make = (f, lab) => col(lab ? `f.${f.key}.${lab}` : `f.${f.key}`, lab ? labName(lab) : 'Мої поля', FIELD[f.type], lab ? `${f.title} · ${labName(lab)}` : f.title,
    f.emoji || f.title, (r) => r.fields[lab ? `${f.key}.${lab}` : f.key] ?? null, { options: Object.fromEntries(f.options.map((o) => [o.id, o])), edit: 'field', field: f, lab, own: true })
  return list.flatMap((f) => (f.scope === 'lab' ? labs.map((n) => make(f, n)) : [make(f, 0)]))
}

export function columns(data) {
  const labs = data.labs.map((l) => l.n)
  return [...profile(), ...repo(), ...labs.flatMap(lab), ...polls(data.polls), ...own(), ...fields(data.fields, labs)]
}
