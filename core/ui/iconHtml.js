import { h, render } from 'vue'

import Icon from './components/Icon.vue'

// an Icon as an HTML string, for markup built outside templates (rendered markdown, T291 §12): drawn by Icon.vue itself,
// so its paths are not copied here
const cache = {}
export function iconHtml(name) {
  if (!cache[name]) {
    const el = document.createElement('div')
    render(h(Icon, { name }), el)
    cache[name] = el.innerHTML
    render(null, el)
  }
  return cache[name]
}
