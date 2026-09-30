import { load, save } from './local.js'

// polls (T174): an answer is a line with its emoji first; the table shows the emoji alone
const seg = new Intl.Segmenter('uk', { granularity: 'grapheme' })
const EMOJI = /\p{Extended_Pictographic}|\p{Regional_Indicator}|⃣/u

export const LIMITS = { question: 300, option: 100, title: 60, fewest: 2, most: 12 }  // Telegram's, and the column header's
export const chars = (s) => [...s].length  // code points, as Telegram and the API count them

// «✅ так» → { emoji: '✅', text: 'так' }; a line that does not start with an emoji keeps its text whole
export function parseOption(line) {
  const s = line.trim()
  const first = seg.segment(s)[Symbol.iterator]().next().value?.segment ?? ''
  return EMOJI.test(first) ? { emoji: first, text: s.slice(first.length).trim() } : { emoji: '', text: s }
}
export const parseOptions = (lines) => lines.split('\n').filter((l) => l.trim()).map(parseOption)
export const optionLabel = (o) => [o.emoji, o.text].filter(Boolean).join(' ')
// a table cell: the chosen answers' emoji, or their numbers when an answer has none
export const mark = (options, ids) => ids.map((i) => options[i]?.emoji || String(i + 1)).join(' ')

export const STATUS = {
  draft: { icon: '📝', text: 'чернетка', cls: 'text-bg-light border' },
  open: { icon: '🟢', text: 'відкрите', cls: 'text-bg-success' },
  closed: { icon: '⚪', text: 'закрите', cls: 'text-bg-secondary' },
}
export const SENDS = { queued: '⏳ в дорозі', sent: '✔️ надіслано', failed: '❌ не надіслано', closed: '⏹ закрито' }
const STALE = 120_000  // ms a send may stay «в дорозі» before it counts as stuck (the API's polls_send.STALE)
export const stuck = (s) => s.status === 'failed' || (s.status === 'queued' && Date.now() - new Date(s.at) > STALE)

// the places picked last time: next week's class goes to the same topic; `places` — GET /api/polls/chats
const TARGETS = 'poll-targets'
export function lastTargets(places) {
  const ids = new Set([...places.chats.filter((c) => !c.hidden && !c.left).map((c) => c.id), ...(places.me ? ['me'] : [])])
  try {
    return JSON.parse(load(TARGETS) || '[]').filter((t) => ids.has(t))
  } catch {
    return []
  }
}
export const keepTargets = (targets) => save(TARGETS, JSON.stringify(targets))

// the form keeps the answers as lines: typed or pasted in one go
export const emptyForm = () => ({ title: '', question: '', lines: '', multiple: false, tags: [], template: '' })
export const fromPoll = (p) => ({ title: p.title, question: p.question, lines: p.options.map(optionLabel).join('\n'), multiple: p.multiple,
                                  tags: [...p.tags], template: p.template || '' })
export const toPayload = (f) => ({ title: f.title, question: f.question, options: parseOptions(f.lines), multiple: f.multiple, tags: f.tags,
                                   template: f.template })

// what stops the form (errors: the API would refuse) and what only deserves a look (warnings)
export function review(f) {
  const options = parseOptions(f.lines)
  const labels = options.map(optionLabel)
  const emoji = options.map((o) => o.emoji).filter(Boolean)
  const twins = [...new Set(emoji.filter((e, i) => emoji.indexOf(e) !== i))]
  const long = labels.find((l) => chars(l) > LIMITS.option)
  const bare = options.filter((o) => !o.emoji).length
  const errors = [
    chars(f.question.trim()) > LIMITS.question && `Питання довше за ${LIMITS.question} символів — Telegram не прийме`,
    options.length > LIMITS.most && `Варіантів більше за ${LIMITS.most} — стільки Telegram не дозволяє`,
    long && `Варіант довший за ${LIMITS.option} символів: «${long.slice(0, 30)}…»`,
    new Set(labels).size < labels.length && 'Два однакові варіанти — Telegram їх не розрізнить',
    chars(f.title.trim()) > LIMITS.title && `Заголовок довший за ${LIMITS.title} символів — він стає назвою колонки`,
  ].filter(Boolean)
  const warnings = [
    bare && `${bare} ${plural(bare, 'варіант', 'варіанти', 'варіантів')} без емодзі — у таблиці замість емодзі буде номер`,
    twins.length && `${twins.join(' ')} — у кількох варіантів: у таблиці їх не розрізнити`,
  ].filter(Boolean)
  const ready = !!f.question.trim() && options.length >= LIMITS.fewest && !errors.length
  return { options, errors, warnings, ready }
}

export function plural(n, one, few, many) {
  const d = n % 10
  const t = n % 100
  return d === 1 && t !== 11 ? one : d >= 2 && d <= 4 && (t < 12 || t > 14) ? few : many
}

export const today = () => new Date().toLocaleDateString('uk-UA', { day: '2-digit', month: '2-digit' })
export const moment = (iso) => iso && new Date(iso).toLocaleString('uk-UA', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })

// a voter: a person of the site (`nick`), or a Telegram account it does not know
export const whoKey = (w) => w.nick || `tg:${w.tg_id ?? w.username}`
// no tg id — an anonymous admin who voted as the chat: `username` holds the chat's title
export const whoName = (w) => (w.nick ? w.name || w.nick : w.tg_id == null ? w.username : w.username ? `@${w.username}` : `tg ${w.tg_id}`)
