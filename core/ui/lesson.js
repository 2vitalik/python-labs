// a lesson as the site shows it: the transcript's line grammar (.claude/skills/lesson/merge.md), links by host, Zoom's chat
const LINE = /^\*\*([^*]+)\*\*(?: · (\d{1,2}:\d{2}))? — (.+)$/
const HEAD = /^## (.+?)(?: · (\d{1,2}:\d{2}))?$/
const NOTE = /^\*\[(.+)\]\*$/
const CHAT = /^(\d\d:\d\d:\d\d)\s+From\s+(.+?)\s+to\s+(.+?):\s*(.*)$/

export const KINDS = { pz: 'ПЗ', lab: 'Лаба', lec: 'Лекція', cons: 'Консультація', x: 'Зустріч' }
export const KINDS_MANY = { pz: 'ПЗ', lab: 'Лаби', lec: 'Лекції', cons: 'Консультації', x: 'Зустрічі' }
export const timeId = (t) => `t-${t.replace(':', '')}`  // «15:01» → t-1501: the anchor of a section, the summary's «Теми» point there

// [{id, title, time, items}], items: {who, time, text} a line · {note} a remark · {text} anything outside the grammar
export function parseTranscript(md) {
  let body = md || ''
  if (body.startsWith('---\n')) body = body.split('---\n').slice(2).join('---\n')
  const sections = []
  let cur = null
  for (const raw of body.split('\n')) {
    const line = raw.trim()
    if (!line || line.startsWith('# ')) continue
    let m = line.match(HEAD)
    if (m) {
      cur = { id: m[2] ? timeId(m[2]) : `s-${sections.length}`, title: m[1], time: m[2] || '', items: [] }
      sections.push(cur)
      continue
    }
    if (!cur) sections.push((cur = { id: 's-0', title: '', time: '', items: [] }))
    if ((m = line.match(LINE))) cur.items.push({ who: m[1].trim(), time: m[2] || '', text: m[3] })
    else if ((m = line.match(NOTE))) cur.items.push({ note: m[1] })
    else cur.items.push({ text: line })
  }
  return sections
}

export function stats(sections) {
  const lines = sections.flatMap((s) => s.items).filter((i) => i.who)
  return { sections: sections.filter((s) => s.title).length, lines: lines.length,
           words: lines.reduce((n, l) => n + l.text.split(/\s+/).length, 0), speakers: new Set(lines.map((l) => l.who)).size }
}

// seconds into the recording for a line's clock time; null when the start is unknown or the line is before it
export function seek(time, start) {
  if (!time || !start) return null
  const [h, m] = time.split(':').map(Number)
  const [sh, sm, ss = 0] = start.split(':').map(Number)
  const s = (h * 60 + m) * 60 - ((sh * 60 + sm) * 60 + ss)
  return s >= 0 ? s : null
}

// the icon and a default label by host; `at(s)` — the same video from second s, where the host can
export function linkInfo(url) {
  let host = ''
  try { host = new URL(url).hostname.replace(/^www\./, '') } catch { /* not a url */ }
  if (/(^|\.)(youtube\.com|youtu\.be)$/.test(host)) return { icon: '🎬', label: 'Відео', at: (s) => `${url}${url.includes('?') ? '&' : '?'}t=${s}s` }
  if (/zoom\.us$/.test(host)) return { icon: '🎬', label: 'Запис Zoom' }
  if (/(^|\.)google\.com$/.test(host)) return { icon: '📁', label: 'Google Drive' }
  if (host === 't.me' || host === 'telegram.me') return { icon: '✈️', label: 'Telegram' }
  if (host === 'github.com') return { icon: '🐙', label: 'GitHub' }
  return { icon: '🔗', label: host || 'Посилання' }
}
export const withInfo = (links) => links.map((l) => ({ ...linkInfo(l.url), ...l, label: l.label || linkInfo(l.url).label }))

export const fmtDate = (iso, long = false) => (iso ? new Date(`${iso}T00:00:00`).toLocaleDateString('uk-UA',
  long ? { day: 'numeric', month: 'long', year: 'numeric' } : { day: 'numeric', month: 'short' }) : '')
export const fmtSize = (n) => (n < 1024 ? `${n} Б` : n < 2 ** 20 ? `${Math.round(n / 1024)} КБ` : `${(n / 2 ** 20).toFixed(1)} МБ`)
export const fmtWords = (n) => (n >= 1000 ? `${(n / 1000).toFixed(1).replace('.0', '')} тис. слів` : `${n} слів`)

// Zoom's saved chat: «HH:MM:SS From Who to Everyone:» then the message on the same or the next (tab-indented) lines
export function parseChat(text) {
  const rows = []
  for (const line of (text || '').split('\n')) {
    const m = line.match(CHAT)
    if (m) rows.push({ time: m[1].slice(0, 5), who: m[2], to: m[3] === 'Everyone' ? '' : m[3], text: m[4] })
    else if (rows.length && line.trim()) rows[rows.length - 1].text = `${rows[rows.length - 1].text}\n${line.trim()}`.trim()
    else if (line.trim()) rows.push({ time: '', who: '', to: '', text: line.trim() })
  }
  return rows
}

// the summary for the page: without its own h1 (the page has one), the times of «Теми» lead into the transcript
export const summaryView = (md) => (md || '').replace(/^# .*\n+/, '')
  .replace(/^(- .+?) · (\d{1,2}:\d{2})( —|$)/gm, (_, head, t, tail) => `${head} · [${t}](#${timeId(t)})${tail}`)
