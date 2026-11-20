<script setup>
import { onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import Icon from '@core/components/Icon.vue'

import { anchor, blocksOf } from '../lectureAnchors.js'
import { flash } from '../lectureFoundPlace.js'

// the text's places for links (lectureAnchors.js), kept as the text is drawn anew; an address with #s12 / #s12-3 is
// reached once they exist — at once, with a flash. On a wide screen with a mouse a quiet link sign stands on the margin
// beside the block under the pointer and copies the block's address; it hangs over the page, so nothing moves
const props = defineProps({ root: Object })
const route = useRoute()
const at = ref(null)  // { id, top, left } of the sign
const done = ref(false)
const wide = matchMedia('(hover: hover) and (min-width: 56rem)')

let reached = false
async function keep() {
  anchor(props.root)
  const id = route.hash.slice(1)
  if (reached || !/^s\d+(-\d+)?$/.test(id) || !document.getElementById(id)) return
  reached = true
  await Promise.all([...props.root.querySelectorAll('img')].map((img) => img.decode().catch(() => null)))
  const el = document.getElementById(id)  // at once: Bootstrap makes the browser's own «auto» a smooth ride
  el?.scrollIntoView({ block: 'start', behavior: 'instant' })
  if (el) flash(el.classList.contains('slide-at') ? blocksOf(el) : [el])
}
const seen = new MutationObserver(keep)
watch(() => props.root, (el) => {
  seen.disconnect()
  if (el) (seen.observe(el, { childList: true, subtree: true }), keep())
}, { immediate: true, flush: 'post' })

let hide
function over(e) {
  const b = wide.matches && e.target.closest?.('[data-anchor]')
  if (!b || !props.root.contains(b)) return
  clearTimeout(hide)
  const r = b.getBoundingClientRect(), css = getComputedStyle(b), line = parseFloat(css.lineHeight) || 24
  const first = parseFloat(css.paddingTop) + parseFloat(css.borderTopWidth) + (Math.min(line, r.height) - 24) / 2  // beside the first line
  at.value = { id: b.id, top: r.top + scrollY + first, left: props.root.getBoundingClientRect().left + scrollX - 32 }
}
const stay = () => clearTimeout(hide)
const later = () => (stay(), (hide = setTimeout(() => (at.value = null), 400)))
async function copy() {
  try { await navigator.clipboard.writeText(`${location.origin}${location.pathname}#${at.value.id}`) } catch { return }
  done.value = true
  setTimeout(() => (done.value = false), 1500)
}
watch(() => props.root, (el, was) => {
  was?.removeEventListener('mouseover', over)
  was?.removeEventListener('mouseleave', later)
  el?.addEventListener('mouseover', over)
  el?.addEventListener('mouseleave', later)
}, { immediate: true })
onUnmounted(() => (seen.disconnect(), stay()))
</script>

<template>
  <Teleport to="body">
    <a v-if="at" class="lec-link" :href="`#${at.id}`" :style="{ top: `${at.top}px`, left: `${at.left}px` }"
       :title="done ? 'Скопійовано' : 'Скопіювати посилання на це місце'" @click.prevent="copy" @mouseenter="stay"
       @mouseleave="later"><Icon :name="done ? 'check' : 'link'" /></a>
  </Teleport>
</template>

<style scoped>
.lec-link { position: absolute; z-index: 5; display: flex; align-items: center; justify-content: center; width: 1.5rem; height: 1.5rem;
            font-size: .9rem; color: var(--bs-tertiary-color); opacity: .75; text-decoration: none; border-radius: .25rem; }
.lec-link:hover { opacity: 1; color: var(--bs-body-color); background: var(--bs-tertiary-bg); }
@media print { .lec-link { display: none; } }
</style>
