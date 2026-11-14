import { computed, ref, shallowRef } from 'vue'

// the contents of the page on screen: Toc.vue puts its items here, PageJump.vue shows them where the side column does not
// fit and keeps `tocActive` — the section being read: the last one whose place has reached the top of the window.
// An item is {id, text, depth} or a {label} between groups; `quiet` — a place the page knows but the list does not show
// (a catalog subcategory): TocBar names it, the list marks the chapter it belongs to
export const tocItems = shallowRef([])
export const tocActive = ref('')
export const tocUnder = ref('')  // the same, once its heading has gone under the menu: until then the heading itself says where we are
export const tocBar = ref(true)  // TocBar names the section under the menu; false — the page sticks headings of its own
export const tocListed = computed(() => tocItems.value.filter((h) => !h.quiet))
export const tocMarked = computed(() => {
  const i = tocItems.value.findIndex((h) => h.id === tocActive.value)
  const h = tocItems.value[i]
  return (h?.quiet ? tocItems.value.slice(0, i).findLast((x) => x.id && !x.quiet) : h)?.id || ''
})

export function spy() {
  const css = getComputedStyle(document.documentElement)
  const line = parseFloat(css.scrollPaddingTop) + 20, menu = parseFloat(css.getPropertyValue('--nav-h')) || 0
  const placed = tocItems.value.map((h) => h.id && document.getElementById(h.id)).filter((el) => el?.offsetParent)  // folded away — not on the page
  const atEnd = innerHeight + scrollY >= document.documentElement.scrollHeight - 2  // a short last section never reaches the line
  const el = atEnd ? placed.at(-1) : placed.findLast((x) => x.getBoundingClientRect().top <= line)
  tocActive.value = el?.id || ''
  tocUnder.value = placed.findLast((x) => x.getBoundingClientRect().top < menu)?.id || ''
}
