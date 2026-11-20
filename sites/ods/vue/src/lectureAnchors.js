// a place in a lecture's text for a link (T374 §6.3): a slide's number gets id «s12», each block after it up to the next
// number «s12-1», «s12-2»… in reading order — a list item by item, quotes, columns and drafts by their paragraphs;
// headings keep their own ids, a slide's own block (hidden in the text) gets none. Ids only: nothing on the page moves
const INTO = ['lec-cols', 'lec-col', 'lec-text', 'draft']  // boxes whose children are the blocks
const NOT = /^(H[1-6]|HR|SCRIPT|STYLE)$/

export function anchor(root) {
  let n = null, k = 0
  const name = (el, id) => el.id !== id && (el.id = id)
  const mark = (el) => {
    k++
    if (n === null || (el.id && !el.hasAttribute('data-anchor'))) return
    name(el, `s${n}-${k}`)
    el.setAttribute('data-anchor', '')
  }
  const visit = (el) => {
    if (el.classList.contains('slide-at')) {
      n = el.textContent.trim()
      k = 0
      name(el, `s${n}`)
    } else if (NOT.test(el.tagName) || el.classList.contains('lec-slide') || el.id.endsWith('-slot')) return  // -slot: the editor's place
    else if (el.tagName === 'UL' || el.tagName === 'OL') [...el.children].forEach(mark)
    else if (el.tagName === 'BLOCKQUOTE' || (el.tagName === 'DIV' && INTO.some((c) => el.classList.contains(c)))) [...el.children].forEach(visit)
    else mark(el)
  }
  const text = [...root.querySelectorAll('.guide')].find((g) => !g.closest('.editor'))  // the editor's preview would repeat the ids
  if (text) [...text.children].forEach(visit)
}

// the blocks of a slide: from its number up to the next one
export function blocksOf(mark) {
  const out = []
  for (let b = mark.nextElementSibling; b && !b.classList.contains('slide-at'); b = b.nextElementSibling) out.push(b)
  return out
}
