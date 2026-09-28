import { ref } from 'vue'

import { load, save } from './local.js'

// drafts in guide text (T157): `<!-- … -->` is the admin's notes and unfinished parts. The API sends both texts:
// `body` with the drafts and `public` without them (drafts.py). Which one the admin looks at is remembered in this browser
const KEY = 'guide-drafts'
export const shown = ref(load(KEY) !== '0')
export function toggleDrafts() {
  shown.value = !shown.value
  save(KEY, shown.value ? '1' : '0')
}

export const textOf = (page) => (shown.value ? page?.body : page?.public) || ''
export const hasDrafts = (page) => !!page?.body?.includes('<!--')
// is the text right after `before` inside a draft
export const inDraft = (before) => before.lastIndexOf('<!--') > before.lastIndexOf('-->')

// for the renderer: a draft that takes whole lines becomes a block, one inside a line — a span;
// an unclosed draft runs to the end of the text
const DRAFT = /<!--([\s\S]*?)(?:-->|$)/g
export const markDrafts = (text) => text.replace(DRAFT, (all, body, at) => {
  if (!body.trim()) return ''
  const pad = text.slice(text.lastIndexOf('\n', at - 1) + 1, at)
  const lines = !pad.trim() && /^[ \t]*(\n|$)/.test(text.slice(at + all.length))
  if (!lines) return `<span class="draft">${body.trim()}</span>`
  const first = /^\s*\n/.test(body) ? '' : pad  // text that starts on its own line brings its indent
  return `\n\n${pad}<div class="draft">\n\n${first}${body.replace(/^\s*\n|^[ \t]+|\s+$/g, '')}\n\n${pad}</div>\n\n`
})
