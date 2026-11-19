import katex from 'katex'
import { Marked } from 'marked'

import math from './math.js'

// a student's notebook text: the site's formulas (math.js) and Jupyter's `$$…$$` over several lines. Guide pages trust
// their HTML (the teacher wrote it); this text is a student's — raw HTML shows as text, only web links stay links
const BLOCK = /^ {0,3}\$\$([\s\S]+?)\$\$[ \t]*(?:\n|$)/
const WEB = /^https?:\/\//i
const PIC = /^(https?:\/\/|data:image\/(png|jpe?g|gif|webp);)/i
const esc = (s) => s.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c])

export const tex = (src, block = true) => katex.renderToString(src, { displayMode: block, throwOnError: false })

const md = new Marked(math, {
  extensions: [{
    name: 'mathBlock',
    level: 'block',
    start: (src) => src.match(/^ {0,3}\$\$/m)?.index,
    tokenizer(src) {
      const m = BLOCK.exec(src)
      if (m) return { type: 'mathBlock', raw: m[0], tex: m[1].trim() }
    },
    renderer: (t) => `<div class="nb-tex">${tex(t.tex)}</div>\n`,
  }],
  renderer: {
    html: ({ text }) => esc(text),
    link({ href, tokens }) {
      const text = this.parser.parseInline(tokens)
      return WEB.test(href) ? `<a href="${esc(href)}" target="_blank" rel="noopener nofollow">${text}</a>` : text
    },
    image: ({ href, text }) => (PIC.test(href) ? false : esc(text)),
  },
})

// tables as on guide pages (core md.js)
export const nbMd = (text) => md.parse(text || '').replace(/<table>/g, '<div class="table-responsive"><table class="table table-sm">')
  .replace(/<\/table>/g, '</table></div>')

// a latex output of a cell comes with its delimiters: $$…$$, $…$ or \[…\]
export const texOut = (src) => tex(String(src).trim().replace(/^\$\$?|\$\$?$/g, '').replace(/^\\\[|\\\]$/g, ''))
