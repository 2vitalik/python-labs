import { nextTick, onMounted, onUnmounted, ref, watch } from 'vue'

// priority menu: one row always. When it gets tight — first the user name goes, then the brand and «Вийти»
// shrink to icons, and only then trailing links move into the «Ще» dropdown (never a hamburger)
export function useNavFit(items) {
  const bar = ref()   // <nav>
  const list = ref()  // <ul> with the links + the «Ще» item, which is measured but may be absent from flow
  const more = ref()  // «Ще» <li>
  const fit = ref(items.value.length)  // how many links stay in the row
  const stage = ref(0)  // 0 full · 1 no user name · 2 icons instead of brand and «Вийти»
  let busy = false

  async function layout() {
    if (busy || !list.value) return
    busy = true
    for (stage.value = 0; stage.value <= 2; stage.value++) {
      fit.value = items.value.length
      await nextTick()
      const widths = [...list.value.children].filter((el) => el !== more.value).map((el) => el.offsetWidth)
      const free = list.value.clientWidth
      if (widths.reduce((a, b) => a + b, 0) <= free) break
      if (stage.value === 2) {
        let sum = more.value.offsetWidth
        fit.value = Math.max(0, widths.findIndex((w) => (sum += w) > free))
      }
    }
    stage.value = Math.min(stage.value, 2)
    busy = false
  }

  const ro = new ResizeObserver(layout)
  onMounted(() => ro.observe(bar.value))
  onUnmounted(() => ro.disconnect())
  watch(items, layout, { flush: 'post' })
  return { bar, list, more, fit, stage, layout }
}
