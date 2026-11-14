import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

import { load, save } from './local.js'

// priority menu: one row always. When it gets tight — first the user name goes, then «Вийти» shrinks to an icon
// (the brand is always the 🏠 icon), and only then the links give way (never a hamburger). How — the reader's choice,
// remembered in this browser (T287): trailing links move into the «Ще» dropdown, or — `icons` — every link becomes its
// icon (`compact`), and only what still does not fit goes to «Ще»
export const icons = ref(load('nav-look') === 'icons')

export function useNavFit(items) {
  const bar = ref()   // <nav>
  const list = ref()  // <ul> with the links + the «Ще» item, which is measured but may be absent from flow
  const more = ref()  // «Ще» <li>
  const tail = ref()  // the «Аа» <li> at the end of the icons
  const fit = ref(items.value.length)  // how many links stay in the row
  const stage = ref(0)  // 0 full · 1 no user name · 2 icon instead of «Вийти», short sign-in button
  const compact = ref(false)  // the links are icons now
  let busy = false

  const aside = () => [more.value, tail.value].filter(Boolean)
  const widths = () => [...list.value.children].filter((el) => !aside().includes(el)).map((el) => el.offsetWidth)
  const fits = () => widths().reduce((a, b) => a + b, tail.value?.offsetWidth || 0) <= list.value.clientWidth

  async function layout() {
    if (busy || !list.value) return
    busy = true
    compact.value = false
    fit.value = items.value.length
    let ok = false
    const stages = async () => {
      for (stage.value = 0; ; stage.value++) {
        await nextTick()
        if ((ok = fits()) || stage.value === 2) break
      }
    }
    await stages()
    if (!ok && icons.value) {  // icons free the row: the name may come back
      compact.value = true
      await stages()
    }
    if (!ok) {  // «Ще» takes the tail — and holds the way back to words, so «Аа» is not drawn beside it
      let sum = more.value.offsetWidth
      fit.value = Math.max(0, widths().findIndex((w) => (sum += w) > list.value.clientWidth))
    }
    busy = false
  }
  function setIcons(on) {
    icons.value = on
    save('nav-look', on ? 'icons' : '')
    layout()
  }

  const ro = new ResizeObserver(layout)
  onMounted(() => ro.observe(bar.value))
  onUnmounted(() => ro.disconnect())
  watch(items, layout, { flush: 'post' })
  return { bar, list, more, tail, fit, stage, compact, layout, setIcons }
}
