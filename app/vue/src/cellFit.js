import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

// a grid's cell as wide as its box allows (T276): the box is the nearest `.fit-box` around the grid, or its parent — a
// column of cards is narrower than the window. `reserve` — the room the grid's own frame and controls take, in px
export function useCellFit(root, cols, { max = 30, reserve = 12 } = {}) {
  const box = ref(0)
  const sized = new ResizeObserver(([e]) => (box.value = e.contentRect.width))
  onMounted(() => sized.observe(root.value.closest('.fit-box') || root.value.parentElement))
  onBeforeUnmount(() => sized.disconnect())
  return computed(() => (box.value ? Math.max(9, Math.min(max, Math.floor((box.value - reserve) / cols.value))) : max))
}
