<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'

import { toTop } from '@core/anchors.js'
import Icon from '@core/components/Icon.vue'
import { pages } from '@core/guide.js'

import { shortTitle } from '../lectures.js'

// a lecture's row on the shelf under the menu (App.vue), as the lab's bar: ‹ › — the lecture before and after (in the view
// open now), the lecture's number and theme, and the page's switches (the slot) at one place in the text and on the slides.
// The theme shows once the page's h1 has gone under the menu — one of the two is always in sight; the slides have no h1.
// Its height stands before its data: nothing under it moves. The empty space or the theme, the page scrolled, — to the top.
// `head` — the h1's id: as a template ref it re-rendered the page before the page's v-rich had mounted (rich.js threw)
const props = defineProps({ doc: Object, prev: Object, next: Object, head: String, slides: Boolean })
const title = (d) => shortTitle(pages.value[d?.slug]?.title)
const to = (d) => (props.slides ? { path: d.path, query: { slide: 1 } } : d.path)
const steps = computed(() => [['left', props.prev, 'Попередня', 'Попередньої'], ['right', props.next, 'Наступна', 'Наступної']])

const gone = ref(false)
const look = () => {
  const menu = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 0
  const h = document.getElementById(props.head)
  gone.value = !!h && h.getBoundingClientRect().bottom <= menu
}
watch(() => [props.slides, props.doc], look, { flush: 'post' })
onMounted(() => addEventListener('scroll', look, { passive: true }))
onBeforeUnmount(() => removeEventListener('scroll', look))

const free = ref(false)
const isFree = (e) => scrollY > 0 && !e.target.closest('a, button, .step')
const click = (e) => isFree(e) && toTop()
</script>

<template>
  <Teleport defer to="#top-shelf">
    <nav class="lec-bar" :class="{ free }" :title="free ? 'Нагору' : null" aria-label="Лекція"
         @click="click" @mousemove="free = isFree($event)" @mouseleave="free = false">
      <div class="in page">
        <span class="walk">
          <template v-for="[pic, d, word, none] in steps" :key="pic">
            <RouterLink v-if="d" :to="to(d)" class="step" :title="`${word}: ${d.nav} · ${title(d)}`" :aria-label="`${word} лекція`"><Icon :name="pic" /></RouterLink>
            <span v-else class="step off" aria-disabled="true" :title="`${none} лекції нема`"><Icon :name="pic" /></span>
            <span v-if="pic === 'left'" class="n"><span class="word">Лекція </span>{{ doc?.n }}</span>
          </template>
        </span>
        <b class="theme" :class="{ on: slides || gone }" :aria-hidden="!(slides || gone)">{{ title(doc) }}</b>
        <span class="ends"><slot /></span>
      </div>
    </nav>
  </Teleport>
</template>

<style scoped>
.lec-bar { border-bottom: 1px solid var(--bs-border-color); background: var(--bs-body-bg); }
.lec-bar.free { cursor: pointer; }
.in { display: flex; align-items: center; gap: .75rem; height: 2.5rem; }
.walk { display: flex; flex: none; align-items: center; gap: .15rem; }
.n { padding: 0 .2rem; font-size: .875rem; color: var(--bs-secondary-color); white-space: nowrap; font-variant-numeric: tabular-nums; }
.step { display: inline-flex; align-items: center; justify-content: center; width: 1.75rem; height: 1.75rem; border: 1px solid transparent;
        border-radius: .3rem; color: var(--bs-secondary-color); text-decoration: none; }
.step:hover:not(.off) { border-color: var(--bs-border-color); color: var(--bs-body-color); }
.step.off { opacity: .35; cursor: default; }
.theme { flex: 1 1 auto; min-width: 0; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; font-weight: 650;
         opacity: 0; transition: opacity .2s; }
.theme.on { opacity: 1; }
.ends { display: flex; flex: none; align-items: center; gap: .5rem; margin-left: auto; }
@media (max-width: 575.98px) {  /* a phone: the theme's room — the number without its word, closer gaps */
  .in { gap: .5rem; }
  .walk { gap: 0; }
  .word { display: none; }
  .ends { gap: .35rem; }
}
@media print { .lec-bar { display: none; } }
</style>
