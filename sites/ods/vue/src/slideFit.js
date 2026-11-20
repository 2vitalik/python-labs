// a slide's type size (T359 §4): the biggest of the steps at which its body fits the sheet — in height, and in width: its
// own (a long word of a title) and its formulas' and tables' (they would scroll sideways). --fit scales the body's font and
// with it formulas, tables, pictures. None fits — denser lines and gaps and two steps more (T374: 0.5 of a laptop's sheet
// is 13 px still); none of those either — back to the smallest plain step, and the body scrolls. All of it sits on the
// body: its class is static, so Vue's re-render of the sheet's classes does not wipe it. `fit` is told to the body after
const STEPS = [1.25, 1.15, 1.05, 1, 0.95, 0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]
const DENSE = [0.7, 0.65, 0.6, 0.55, 0.5]
const TRIES = [...STEPS.map((s) => [s, false]), ...DENSE.map((s) => [s, true])]
const wide = (body) => [...body.querySelectorAll('.katex-display, .table-responsive')].some((e) => e.scrollWidth > e.clientWidth + 1)
const over = (body) => body.scrollHeight > body.clientHeight + 1 || body.scrollWidth > body.clientWidth + 1 || wide(body)
function set(body, step, dense) {
  body.style.setProperty('--fit', step)
  body.classList.toggle('dense', dense)
  body.dataset.fit = step
}

export async function fit(body) {
  // a picture has no height until decoded; a formula's font starts loading only once laid out
  await Promise.all([...body.querySelectorAll('img')].map((img) => img.decode().catch(() => null)))
  void body.offsetHeight
  await document.fonts.ready
  // mostly a picture — one: the picture takes the height (three at 70 % each would not fit)
  body.classList.toggle('pic', body.querySelectorAll('p.fig img').length === 1 && body.textContent.replace(/\s+/g, ' ').trim().length < 160)
  body.classList.remove('scroll')
  const fits = TRIES.some(([step, dense]) => (set(body, step, dense), !over(body)))
  if (!fits) set(body, STEPS.at(-1), false)
  body.classList.toggle('scroll', !fits)
  body.dispatchEvent(new Event('fit'))
}
