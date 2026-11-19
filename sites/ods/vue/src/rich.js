import { iconHtml } from '@core/iconHtml.js'
import { showShot } from '@core/lightbox.js'
import { load, save } from '@core/local.js'

import './rich.css'
import { button, make, own, passport, tabs } from './richTabs.js'

// v-rich="slug" (or { key: slug }) on a wrapper of GuideBody / GuideText — the lab pages' markup over markdown (T357 §4):
// folds that remember, tabs, the case's passport, pictures in the lightbox, «копіювати» on code, marks for steps.
// v-html swaps the text whenever it changes, so a MutationObserver runs enrich() again; it touches only what is new
const ICONS = { demo: 'play', lecture: 'book', ref: 'info', hint: 'help' }
const live = new WeakMap()  // wrapper → { key, obs }
const keyOf = (v) => (v && typeof v === 'object' ? v.key : v) || ''

// folds: a drawn chevron and the class's icon in the summary; open / shut is remembered per page and summary text
function folds(g, slug, target) {
  const seen = {}
  for (const d of own(g, 'details:not([data-tab])')) {
    const sum = d.querySelector(':scope > summary'), text = sum?.textContent.trim()
    seen[text] = (seen[text] || 0) + 1
    if (!sum || sum.querySelector('.fold-mark')) continue
    const cls = Object.keys(ICONS).find((c) => d.classList.contains(c))
    const ico = cls ? `<span class="fold-ico">${iconHtml(ICONS[cls])}</span>` : ''
    sum.insertAdjacentHTML('afterbegin', `<span class="fold-mark">${iconHtml('right')}</span>${ico}`)
    if (d.hasAttribute('name')) continue  // a lone member of an accordion: the browser's
    const key = `rich-fold:${slug}:${text}${seen[text] > 1 ? `#${seen[text]}` : ''}`, kept = load(key)
    if (kept !== null && !(target && d.contains(target))) d.open = kept === '1'
    d.addEventListener('toggle', () => save(key, d.open ? '1' : '0'))
  }
}

function zoom(g) {
  for (const img of own(g, 'img:not(.zoom)').filter((i) => !i.closest('a'))) {
    img.classList.add('zoom')
    img.addEventListener('click', () => {
      const all = own(g, 'img.zoom')
      showShot(all.map((i) => i.src), all.indexOf(img))
    })
  }
}
function copies(g) {
  const word = (icon, text) => `${iconHtml(icon)}<span>${text}</span>`
  for (const pre of own(g, 'pre').filter((p) => !p.parentElement.classList.contains('code'))) {
    const box = make('div', 'code')
    const btn = button('copy', word('copy', 'копіювати'), async () => {
      try { await navigator.clipboard.writeText(pre.textContent) } catch { return }
      btn.innerHTML = word('check', 'скопійовано')
      btn.classList.add('done')
      setTimeout(() => { btn.innerHTML = word('copy', 'копіювати'); btn.classList.remove('done') }, 1500)
    })
    pre.before(box)
    box.append(pre, btn)
  }
}

function enrich(g, slug) {
  const target = location.hash && document.getElementById(location.hash.slice(1))  // flash() has opened its fold: keep it
  passport(g)
  tabs(g, target)
  folds(g, slug, target)
  zoom(g)
  copies(g)
  for (const h of own(g, ':is(h2, h3, h4)[id^="s"]')) {  // {#s14} — step 1.4 of the notebook: its ⬜ / ✅ / ❌ later
    const m = h.id.match(/^s(\d)(\d)$/)
    if (m && !h.querySelector('.step-mark')) h.insertAdjacentHTML('afterbegin', `<span class="step-mark" data-step="${m[1]}.${m[2]}"></span>`)
  }
}

// our own changes are made with the observer off: they do not come back as mutations
function run(el, s) {
  s.obs.disconnect()
  el.querySelectorAll('.guide').forEach((g) => enrich(g, s.key))
  s.obs.observe(el, { childList: true, subtree: true })
}

export const vRich = {
  mounted(el, { value }) {
    el.classList.add('rich')
    const s = { key: keyOf(value) }
    s.obs = new MutationObserver(() => run(el, s))
    live.set(el, s)
    run(el, s)
  },
  beforeUpdate(el, { value }) { live.get(el).key = keyOf(value) },
  unmounted(el) { live.get(el)?.obs.disconnect() },
}
