<script setup>
import { nextTick, onBeforeUnmount, onMounted, ref } from 'vue'

import Icon from './Icon.vue'

// a long block shown in short (T284 §3): the first `height` rem of it, fading into «Показати все». A block only a little
// longer than that is not cut — hiding a few lines is not worth a button. `open` — the reader asks for all of it; a panel
// opened inside that the cut would clip asks for it too
const props = defineProps({ on: Boolean, height: { type: Number, default: 28 } })
const emit = defineEmits(['open'])
const root = ref()
const inner = ref()
const tall = ref(false)
const rem = () => parseFloat(getComputedStyle(document.documentElement).fontSize)
const sized = new ResizeObserver(() => (tall.value = inner.value.offsetHeight > props.height * rem() * 1.3))
onMounted(() => sized.observe(inner.value))
onBeforeUnmount(() => sized.disconnect())
async function clicked() {
  if (!props.on || !tall.value) return
  await nextTick()
  const end = root.value.getBoundingClientRect().bottom
  if ([...root.value.querySelectorAll('.pop-panel')].some((p) => p.getBoundingClientRect().bottom > end)) emit('open')
}
</script>

<template>
  <div ref="root" class="clamp" :class="{ cut: on && tall }" :style="{ '--clamp': `${height}rem` }" @click="clicked">
    <div ref="inner"><slot /></div>
    <button v-if="on && tall" type="button" class="more" @click.stop="emit('open')"><span>Показати все <Icon name="down" /></span></button>
  </div>
</template>

<style scoped>
.cut { position: relative; max-height: var(--clamp); overflow: hidden; }
.more { position: absolute; inset: auto 0 0; display: flex; align-items: flex-end; justify-content: center; height: 5rem; padding: 0 0 .35rem; border: 0;
        background: linear-gradient(transparent, var(--bs-body-bg) 70%); color: var(--bs-link-color); font-size: .85rem; }
.more span { padding: .1rem .7rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; background: var(--bs-body-bg); }
.more:hover span { border-color: var(--bs-link-color); }
</style>
