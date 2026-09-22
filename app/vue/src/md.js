import { Marked } from 'marked'

import { fieldHtml } from './field.js'
import { ANCHOR, headingId } from './headings.js'

// guide markdown: `{#id}` anchors, 🔗 (+ ✏️ for the editor) on headings, emoji callouts, ```field grids,
// responsive tables, external links in new tabs
const SPAN = /<span id="([\w-]+)" class="anchor"><\/span>\s*/
const isEmoji = (html) => /^<p>\s*\p{Extended_Pictographic}/u.test(html)

let prefix = ''
let editable = false
const withPrefix = (id) => (prefix ? `${prefix}-${id}` : id)

const md = new Marked({
  renderer: {
    heading({ tokens, depth, text }) {
      let html = this.parser.parseInline(tokens)
      const m = html.match(SPAN)  // explicit id is already prefixed by renderMd()
      const id = m ? m[1] : withPrefix(headingId(text)[0])
      if (m) html = html.replace(SPAN, '').trimEnd()
      const local = prefix ? id.slice(prefix.length + 1) : id  // the id inside the page's own text, for the editor
      const edit = editable ? ` <a class="edit" href="#" data-id="${local}" title="Редагувати розділ">✏️</a>` : ''
      const slot = editable ? `<div id="${id}-slot"></div>\n` : ''  // where the inline editor lands (Teleport)
      return `<h${depth} id="${id}">${html} <a class="link" href="#${id}" title="Скопіювати посилання">🔗</a>${edit}</h${depth}>\n${slot}`
    },
    blockquote({ tokens }) {
      const body = this.parser.parse(tokens)
      return `<blockquote${isEmoji(body) ? ' class="callout"' : ''}>\n${body}</blockquote>\n`
    },
    code({ text, lang }) {
      return lang === 'field' ? fieldHtml(text) : false
    },
    link({ href, title, tokens }) {
      const text = this.parser.parseInline(tokens)
      const t = title ? ` title="${title}"` : ''
      if (/^https?:/.test(href)) return `<a href="${href}"${t} target="_blank" rel="noopener">${text}</a>`
      if (href.startsWith('#')) return `<a href="#${withPrefix(href.slice(1))}"${t}>${text}</a>`
      return `<a href="${href}"${t}>${text}</a>`
    },
  },
})

// `{#id}` → id on the heading itself, or an invisible span inside a list item / paragraph
export function renderMd(text, idPrefix = '', edit = false) {
  prefix = idPrefix
  editable = edit
  const src = (text || '').replace(ANCHOR, (_, id) => `<span id="${withPrefix(id)}" class="anchor"></span>`)
  return md.parse(src).replace(/<table>/g, '<div class="table-responsive"><table class="table table-sm">')
    .replace(/<\/table>/g, '</table></div>')
}

// [{depth, id, text}] for h2/h3 — the page's table of contents
export function tocOf(text, idPrefix = '') {
  return md.lexer(text || '').filter((t) => t.type === 'heading' && t.depth <= 3).map((t) => {
    const [id, plain] = headingId(t.text)
    return { depth: t.depth, id: idPrefix ? `${idPrefix}-${id}` : id, text: plain }
  })
}
