import { computed, ref, shallowRef } from 'vue'

// the contents of the page on screen: Toc.vue puts its items here, PageJump.vue shows them where the side column does not
// fit and keeps `tocActive` — the section being read: the last one whose place has reached the top of the window.
// An item is {id, text, depth} or a {label} between groups; `quiet` — a place the page knows but the list does not show
// (a catalog subcategory): TocBar names it, the list marks the chapter it belongs to
export const tocItems = shallowRef([])
export const tocActive = ref('')
// the last heading gone under the menu, and under the menu with TocBar's section row: until then the heading itself says
// where we are
export const tocUnder = ref('')
export const tocUnderRow = ref('')
export const TOC_ROW = 2  // rem, the height of TocBar's section row
export const tocBar = ref(true)  // TocBar names the section under the menu; false — the page sticks headings of its own
export const tocListed = computed(() => tocItems.value.filter((h) => !h.quiet))
export const tocMarked = computed(() => {
  const i = tocItems.value.findIndex((h) => h.id === tocActive.value)
  const h = tocItems.value[i]
  return (h?.quiet ? tocItems.value.slice(0, i).findLast((x) => x.id && !x.quiet) : h)?.id || ''
})
// a sub-section's chapter: the heading above it, unless a group's label comes first
export function chapterOf(items, i) {
  const p = items[i].depth === 3 && items.slice(0, i).findLast((x) => x.label || x.depth < 3)
  return p && !p.label ? p : null
}

export function spy() {
  const css = getComputedStyle(document.documentElement)
  const line = parseFloat(css.scrollPaddingTop) + 20, menu = parseFloat(css.getPropertyValue('--nav-h')) || 0
  const placed = tocItems.value.map((h) => h.id && document.getElementById(h.id)).filter((el) => el?.offsetParent)  // folded away — not on the page
  const atEnd = innerHeight + scrollY >= document.documentElement.scrollHeight - 2  // a short last section never reaches the line
  const el = atEnd ? placed.at(-1) : placed.findLast((x) => x.getBoundingClientRect().top <= line)
  const under = (y) => placed.findLast((x) => x.getBoundingClientRect().top < y)?.id || ''
  tocActive.value = el?.id || ''
  tocUnder.value = under(menu)
  tocUnderRow.value = under(menu + TOC_ROW * parseFloat(css.fontSize))
}
