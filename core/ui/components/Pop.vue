<script setup>
import { nextTick, onBeforeUnmount, ref, watch } from 'vue'

import Icon from './Icon.vue'

// a floating panel at its trigger: it opens over the page, so nothing around shifts; Esc or a click outside closes it.
// It hangs under the trigger, or over it where the window ends; one that fits neither way stays under and slides up over
// its trigger as far as the window asks — never under the shelf at the top (T344).
// <Pop v-model="open"><template #trigger="{ toggle }">…</template> panel content </Pop>
const open = defineModel({ type: Boolean, default: false })
defineProps({ width: { type: String, default: '22rem' }, block: Boolean })
const root = ref()
const panel = ref()
const side = ref({})  // which way the panel hangs so that it stays inside the window
const lift = ref('')

const outside = (e) => !root.value?.contains(e.target) && (open.value = false)
const esc = (e) => e.key === 'Escape' && (open.value = false)
function listen(on) {
  const f = on ? 'addEventListener' : 'removeEventListener'
  document[f]('mousedown', outside)
  document[f]('keydown', esc)
}
watch(open, async (on) => {
  listen(on)
  if (!on) return
  side.value = {}
  lift.value = ''
  await nextTick()
  if (!panel.value) return
  const r = panel.value.getBoundingClientRect()
  const shelf = (parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--nav-h')) || 0) + 4
  const over = r.bottom - (innerHeight - 8)  // how much of it is below the window
  const up = over > 0 && root.value.getBoundingClientRect().top - r.height - 4 >= shelf
  side.value = { right: r.right > innerWidth - 8, up }
  if (over > 0 && !up) lift.value = `0 -${Math.max(0, Math.min(over, r.top - shelf))}px`
}, { immediate: true })  // a panel may be born open
onBeforeUnmount(() => listen(false))
</script>

<template>
  <span ref="root" class="pop" :class="{ block }">
    <slot name="trigger" :open :toggle="() => (open = !open)" />
    <div v-if="open" ref="panel" class="pop-panel shadow border rounded bg-body" :class="side" :style="{ width, translate: lift }">
      <button type="button" class="iact pop-x" title="Закрити" @click="open = false"><Icon name="x" /></button>
      <slot :close="() => (open = false)" />
    </div>
  </span>
</template>

<style scoped>
.pop { position: relative; display: inline-block; max-width: 100%; }
.pop.block { display: block; }
.pop-panel { position: absolute; z-index: 40; top: calc(100% + .25rem); left: 0; max-width: calc(100vw - 1rem); padding: .6rem;
             font-size: .875rem; font-weight: 400; text-align: start; cursor: auto; }
.pop-panel.right { left: auto; right: 0; }
.pop-panel.up { top: auto; bottom: calc(100% + .25rem); }
.pop-x { display: none; }
/* on a phone the panel is a sheet at the bottom of the screen: no room to hang it beside its trigger */
@media (max-width: 575px) {
  .pop-panel { position: fixed; inset: auto .5rem .5rem .5rem; width: auto !important; max-height: 70vh; overflow-y: auto; }
  .pop-x { display: flex; margin: -.3rem -.3rem .1rem auto; }  /* the sheet may lie over what opened it */
}
</style>
