<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

import { isOff, setOff } from '../tips.js'
import Icon from './Icon.vue'

// an explanation — the same look wherever one is needed (T291 §5): small grey text behind «ⓘ» in a dashed frame.
// With `id` the reader can put it away for every place that shows this id: its icon glides to the caption it belongs to
// (T294 §21) — the `.tip-dock` of the nearest `[data-dock]` or `<section>` around it, never out of a floating panel —
// else stays where the box was. Under the mouse the icon shows the text; a click brings the box back.
// <Tip id="rule-when">КОЛИ — що запускає правило…</Tip>
defineOptions({ inheritAttrs: false })
const props = defineProps({ id: String })
const off = computed(() => !!props.id && isOff(props.id))
const spot = ref()  // a hidden mark where the box stands: the way to its dock
const dock = ref(null)
const box = ref()
const btn = ref()
const peek = ref(null)  // where the text under the mouse hangs
let timer

function findDock() {
  for (let n = spot.value?.closest('[data-dock], section, .pop-panel'); n && !n.matches('.pop-panel'); n = n.parentElement?.closest('[data-dock], section, .pop-panel')) {
    const d = n.querySelector('.tip-dock')
    if (d) return d
  }
  return null
}
onMounted(() => (dock.value = findDock()))
onBeforeUnmount(() => clearTimeout(timer))

async function hide() {
  const from = box.value?.querySelector('.tipbox-i')?.getBoundingClientRect()
  setOff(props.id, true)
  await nextTick()
  const to = btn.value?.getBoundingClientRect()
  if (from && to) btn.value.animate([{ transform: `translate(${from.left - to.left}px, ${from.top - to.top}px)` }, { transform: 'none' }],
    { duration: 450, easing: 'cubic-bezier(.2, .7, .2, 1)' })
}
function show() {
  clearTimeout(timer)
  peek.value = null
  setOff(props.id, false)
}
function hover(on) {
  clearTimeout(timer)
  timer = setTimeout(() => {
    const r = on && btn.value?.getBoundingClientRect()
    peek.value = r ? { left: `${Math.max(8, Math.min(r.left - 8, innerWidth - 328))}px`, top: `${r.bottom + 6}px` } : null
  }, on ? 120 : 180)
}
</script>

<template>
  <span ref="spot" hidden />
  <Teleport v-if="off" :to="dock || 'body'" :disabled="!dock">
    <button ref="btn" type="button" class="tipbox-ico" v-bind="dock ? {} : $attrs" aria-label="показати пояснення" @click.stop="show"
            @mouseenter="hover(true)" @mouseleave="hover(false)"><Icon name="info" /></button>
  </Teleport>
  <div v-else ref="box" class="tipbox" v-bind="$attrs">
    <Icon name="info" class="tipbox-i" />
    <div class="tipbox-body"><slot /></div>
    <button v-if="id" type="button" class="tipbox-x" title="сховати пояснення — значок лишиться біля заголовка, клік по ньому поверне" @click.stop="hide"><Icon name="x" /></button>
  </div>
  <Teleport v-if="off && peek" to="body">
    <div class="tipbox tipbox-peek" :style="peek" @mouseenter="hover(true)" @mouseleave="hover(false)">
      <Icon name="info" class="tipbox-i" />
      <div class="tipbox-body"><slot /></div>
    </div>
  </Teleport>
</template>

<!-- not scoped: a host styles the box through its own classes; the names are the component's own (a plain `.tip` is
     taken by several pages) -->
<style>
.tipbox { display: flex; align-items: flex-start; gap: .35rem; padding: .2rem .25rem .2rem .4rem; border: 1px dashed var(--bs-info-border-subtle); border-radius: .3rem;
          background: color-mix(in srgb, var(--bs-info-bg-subtle) 45%, transparent); color: var(--bs-secondary-color); font-size: .76rem; font-weight: 400; line-height: 1.3; text-align: start; }
.tipbox-i { margin-top: .1rem; color: var(--bs-info-text-emphasis); opacity: .8; }
.tipbox-body { flex: 1 1 0; min-width: 0; }
.tipbox-body > :last-child { margin-bottom: 0; }
.tipbox-x, .tipbox-ico { display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; padding: 0; border: 0; border-radius: .25rem; background: none; }
.tipbox-x { width: 1.05rem; height: 1.05rem; color: var(--bs-secondary-color); font-size: .7rem; opacity: .45; }
.tipbox-x:hover { background: var(--bs-tertiary-bg); opacity: 1; }
.tipbox-ico { width: 1.25rem; height: 1.25rem; color: var(--bs-info-text-emphasis); font-size: .85rem; font-weight: 400; letter-spacing: 0; opacity: .7; }
.tipbox-ico:hover { background: color-mix(in srgb, var(--bs-info-bg-subtle) 70%, transparent); opacity: 1; }
/* the text under the mouse: the same box, solid and floating */
.tipbox-peek { position: fixed; z-index: 1080; width: max-content; max-width: min(20rem, calc(100vw - 1rem)); padding: .35rem .5rem; border-style: solid;
               background: var(--bs-body-bg); box-shadow: 0 .25rem .75rem rgb(0 0 0 / .15); text-transform: none; letter-spacing: 0; }
/* where a put-away icon lands (a heading, a caption): nothing until one does */
.tip-dock { display: inline-flex; align-items: center; gap: .1rem; }
.tip-dock:empty { display: none; }
</style>
