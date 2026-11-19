import { load, save } from '@core/local.js'

// rich.js's helpers over a page's .guide, and the two parts of its markup that rebuild the text: the case's passport, tabs
export const own = (g, sel) => [...g.querySelectorAll(sel)].filter((x) => x.closest('.guide') === g)  // not the editor's preview inside
export const make = (tag, cls, html = '') => Object.assign(document.createElement(tag), { className: cls, innerHTML: html })
export const button = (cls, html, click) => Object.assign(make('button', cls, html), { type: 'button', onclick: click })

// 🎯 first on the page: «**підпис:** значення · …» → a strip of chips
export function passport(g) {
  const q = g.firstElementChild, p = q?.querySelector('p')
  if (!p || !q.matches('blockquote.callout.check') || q.classList.contains('passport')) return
  q.classList.add('passport')
  const [, lead, rest] = p.innerHTML.match(/^\s*(\p{Extended_Pictographic}️?)?\s*([\s\S]*)$/u)
  p.className = 'chips'
  p.innerHTML = (lead ? `<span class="lead">${lead}</span>` : '') + rest.split(/\s+·\s+/).map((c) => `<span class="chip">${c}</span>`).join('')
}

// a run of <details name="X">: one panel at a time under a row of tabs; the bold part of a summary names the tab, the rest
// opens the panel. `name` goes, or the browser would close a panel of another run of X; the choice is kept per X, site-wide
export function tabs(g, target) {
  for (const first of own(g, 'details[name]')) {
    if (!first.hasAttribute('name')) continue  // taken by the run before it
    const name = first.getAttribute('name'), key = `rich-tab:${name}`, run = [first]
    for (let d = first.nextElementSibling; d?.tagName === 'DETAILS' && d.getAttribute('name') === name; d = d.nextElementSibling) run.push(d)
    if (run.length < 2) continue
    const labels = run.map(head)
    const btns = labels.map((l, i) => button('nav-link', l, () => { pick(i); save(key, l) }))
    const pick = (i) => run.forEach((d, j) => { d.open = i === j; btns[j].classList.toggle('active', i === j) })
    const box = make('div', 'tabs'), row = make('div', 'nav nav-tabs')
    first.before(box)
    row.append(...btns)
    box.append(row, ...run)
    run.forEach((d, i) => {
      d.dataset.tab = name
      d.removeAttribute('name')
      d.addEventListener('toggle', () => d.open && pick(i))  // opened from outside: a #link into the panel
    })
    const at = [run.findIndex((d) => target && d.contains(target)), labels.indexOf(load(key)), run.findIndex((d) => d.open)]
    pick(at.find((i) => i >= 0) ?? 0)
  }
}
function head(d) {
  const sum = d.querySelector(':scope > summary'), bold = sum?.querySelector('b, strong')
  if (!bold) return sum?.innerHTML.trim() || '…'
  const rest = sum.cloneNode(true)
  rest.querySelector('b, strong').remove()
  const html = rest.innerHTML.replace(/^\s*[—–:-]?\s*/, '').trim()
  if (html) sum.after(make('p', 'tab-lead', html))
  return bold.innerHTML
}
