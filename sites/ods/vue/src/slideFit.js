// a slide's type size (T359 §4): the biggest of the steps at which its body fits the sheet — in height, and in width: its
// own (a long word of a title) and its formulas' and tables' (they would scroll sideways). --fit scales the body's font and
// with it formulas, tables, pictures; none fits — the smallest one, and the body scrolls. All of it sits on the body: its
// class is static, so Vue's re-render of the sheet's classes does not wipe it
const STEPS = [1.25, 1.15, 1.05, 1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]
const wide = (body) => [...body.querySelectorAll('.katex-display, .table-responsive')].some((e) => e.scrollWidth > e.clientWidth + 1)
const over = (body) => body.scrollHeight > body.clientHeight + 1 || body.scrollWidth > body.clientWidth + 1 || wide(body)

export async function fit(body) {
  // a picture has no height until decoded; a formula's font starts loading only once laid out
  await Promise.all([...body.querySelectorAll('img')].map((img) => img.decode().catch(() => null)))
  void body.offsetHeight
  await document.fonts.ready
  // mostly a picture: the picture takes the height
  body.classList.toggle('pic', !!body.querySelector('p.fig') && body.textContent.replace(/\s+/g, ' ').trim().length < 160)
  body.classList.remove('scroll')
  let i = 0
  for (; i < STEPS.length; i++) {
    body.style.setProperty('--fit', STEPS[i])
    if (!over(body)) break
  }
  body.classList.toggle('scroll', i === STEPS.length)
  body.dataset.fit = STEPS[Math.min(i, STEPS.length - 1)]
}
