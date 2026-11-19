import './lecture.css'

// a lecture's markup over markdown (T359 §2–3), registered last — useMd(math, richMd, slideMd): marked asks it first.
// (1) `:::` fences become wrapper divs, and CSS shows each where it belongs. Not HTML comments: the platform takes every
// one but `<!-- слайд N -->` for an admin's draft and hides it from students (drafts.js).
// (2) a paragraph or a quote that starts with the lecturer's bold label (Приклад, Примітка, Теорема…) takes its role;
// (3) a paragraph of pictures only is `fig`, the italic line under it (or one that starts «Рис.» / «Табл.») is a `cap`
const FENCE = /^:::[ \t]*(колонки|колонка|на слайді|у тексті)?[ \t]*([\d: \t]*)$/
// a slide's border closes whatever is left open: a mark in a slide's text, or the number withMarks() put in the lecture's
const BORDER = /^(<!--\s*слайд\s+\d|<div class="slide-at">)/
const WRAP = { 'на слайді': 'lec-slide', 'у тексті': 'lec-text' }
// in any case («РОЗВ'ЯЗАННЯ» of lecture 12) and with any apostrophe
const ROLES = [[/^(приклад|наприклад|рішення|розв['’ʼ]язання|відповідь)/iu, 'example'], [/^(примітка|зауваж|увага|важливо)/iu, 'note'],
  [/^(теорема|наслідок|лема|правило|властивост)/iu, 'rule']]
const CAPTION = /^(Рис|Табл)/

// raw html on lines of its own with blank ones around: the markdown inside the wrapper stays markdown
const html = (tag) => ['', tag, '']

// `::: колонки 2:3` … `::: колонка` … `:::` · `::: на слайді` … `:::` · `::: у тексті` … `:::`; a bare `:::` closes the innermost
function preprocess(src) {
  const out = [], open = []
  const close = () => out.push(...html(open.pop() === 'cols' ? '</div></div>' : '</div>'))
  let code = false
  for (const line of src.split('\n')) {
    if (/^\s*```/.test(line)) code = !code
    if (BORDER.test(line)) while (open.length) close()
    const m = !code && line.match(FENCE)
    if (!m) { out.push(line); continue }
    const [, word, arg] = m
    if (!word) { if (open.length) close() }
    else if (word === 'колонка') {
      if (!open.includes('cols')) continue
      while (open.at(-1) !== 'cols') close()
      out.push(...html('</div><div class="lec-col">'))
    } else if (word === 'колонки') {
      const fr = arg.trim() ? ` style="--cols: ${arg.trim().split(':').map((x) => `${x.trim()}fr`).join(' ')}"` : ''
      out.push(...html(`<div class="lec-cols"${fr}><div class="lec-col">`))
      open.push('cols')
    } else {
      out.push(...html(`<div class="${WRAP[word]}">`))
      open.push(WRAP[word])
    }
  }
  while (open.length) close()
  return out.join('\n')
}

const lead = (p) => (p?.type === 'paragraph' && p.tokens[0]?.type === 'strong' ? p.tokens[0].text : '')
const roleOf = (p) => ROLES.find(([rx]) => rx.test(lead(p)))?.[1]
const solid = (p) => p.tokens.filter((t) => t.type !== 'br' && !(t.type === 'text' && !t.text.trim()))

// a caption is told by its neighbour, which a renderer does not see: the tokens are flagged first
function flag(list) {
  let prev = null
  for (const t of list) {
    if (t.type === 'space') continue
    if (t.type === 'paragraph') {
      const kids = solid(t)
      if (kids.length && kids.every((k) => k.type === 'image')) t.fig = true
      else if (kids.length === 1 && kids[0].type === 'em' && (prev?.fig || CAPTION.test(kids[0].text))) t.cap = true
    }
    if (t.type === 'list') t.items.forEach((i) => flag(i.tokens))
    if (t.type === 'blockquote') flag(t.tokens)
    prev = t
  }
}

export default {
  hooks: {
    preprocess,
    processAllTokens(tokens) {
      flag(tokens)
      return tokens
    },
  },
  renderer: {
    paragraph(t) {
      const role = !t.inQuote && roleOf(t)
      const cls = t.fig ? 'fig' : t.cap ? 'cap' : role ? `role ${role}` : ''
      return cls ? `<p class="${cls}">${this.parser.parseInline(t.tokens)}</p>\n` : false
    },
    blockquote({ tokens }) {
      const role = roleOf(tokens[0])
      if (!role) return false
      tokens[0].inQuote = true  // the quote carries the role, its first paragraph stays plain
      return `<blockquote class="role ${role}">\n${this.parser.parse(tokens)}</blockquote>\n`
    },
  },
}
