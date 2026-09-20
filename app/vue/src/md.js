import { Marked } from 'marked'

// guide markdown: `{#id}` anchors, 🔗 on headings, emoji callouts, responsive tables, external links in new tabs
const TR = {
  а: 'a', б: 'b', в: 'v', г: 'h', ґ: 'g', д: 'd', е: 'e', є: 'ie', ж: 'zh', з: 'z', и: 'y', і: 'i', ї: 'i', й: 'i',
  к: 'k', л: 'l', м: 'm', н: 'n', о: 'o', п: 'p', р: 'r', с: 's', т: 't', у: 'u', ф: 'f', х: 'kh', ц: 'ts', ч: 'ch',
  ш: 'sh', щ: 'shch', ь: '', ю: 'iu', я: 'ia',
}
export const slugify = (s) => s.toLowerCase().replace(/[а-яґєії]/g, (c) => TR[c] ?? c)
  .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

const ANCHOR = /\s*\{#([\w-]+)\}/g
const SPAN = /<span id="([\w-]+)" class="anchor"><\/span>\s*/
const isEmoji = (html) => /^<p>\s*\p{Extended_Pictographic}/u.test(html)

let prefix = ''
const withPrefix = (id) => (prefix ? `${prefix}-${id}` : id)

const md = new Marked({
  renderer: {
    heading({ tokens, depth }) {
      let html = this.parser.parseInline(tokens)
      const m = html.match(SPAN)  // explicit id is already prefixed by renderMd()
      const id = m ? m[1] : withPrefix(slugify(tokens.map((t) => t.text ?? '').join(' ')))
      if (m) html = html.replace(SPAN, '').trimEnd()
      return `<h${depth} id="${id}">${html} <a class="link" href="#${id}" title="Скопіювати посилання">🔗</a></h${depth}>\n`
    },
    blockquote({ tokens }) {
      const body = this.parser.parse(tokens)
      return `<blockquote${isEmoji(body) ? ' class="callout"' : ''}>\n${body}</blockquote>\n`
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
export function renderMd(text, idPrefix = '') {
  prefix = idPrefix
  const src = (text || '').replace(ANCHOR, (_, id) => `<span id="${withPrefix(id)}" class="anchor"></span>`)
  return md.parse(src).replace(/<table>/g, '<div class="table-responsive"><table class="table table-sm">')
    .replace(/<\/table>/g, '</table></div>')
}

// [{depth, id, text}] for h2/h3 — the page's table of contents
export function tocOf(text, idPrefix = '') {
  return md.lexer(text || '').filter((t) => t.type === 'heading' && t.depth <= 3).map((t) => {
    const m = t.text.match(/\{#([\w-]+)\}/)
    const plain = t.text.replace(ANCHOR, '').replace(/[*_`]/g, '')
    const id = m ? m[1] : slugify(plain)
    return { depth: t.depth, id: idPrefix ? `${idPrefix}-${id}` : id, text: plain }
  })
}
