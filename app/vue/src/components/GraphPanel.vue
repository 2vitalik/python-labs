<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { showShot } from '@core/lightbox.js'
import { jump } from '../jump.js'

// the panel of a node on the map of windows: its screenshot (a click — full screen), its description, the way to its card.
// Esc or a click outside closes it; a click on another node or on the full-size picture is the map's and the lightbox's own
const props = defineProps({ win: Object })
const emit = defineEmits(['close'])
const root = ref()
const shots = computed(() => (props.win.screenshots || []).map((s) => `/api/uploads/${props.win.game}/${s}`))
const outside = (e) => !root.value?.contains(e.target) && !e.target.closest?.('.gg-node, .lightbox') && emit('close')
const esc = (e) => e.key === 'Escape' && emit('close')
const listen = (f) => { document[f]('mousedown', outside); document[f]('keydown', esc) }
onMounted(() => listen('addEventListener'))
onBeforeUnmount(() => listen('removeEventListener'))
function go() {
  emit('close')
  jump(`p-${props.win.id}`)
}
</script>

<template>
  <div ref="root" class="gg-panel shadow border rounded bg-body vstack gap-2">
    <div class="fw-semibold">🪟 {{ win.title }}</div>
    <img v-if="shots.length" :src="shots[0]" alt="скриншот" class="rounded border thumb" title="на весь екран" @click="showShot(shots, 0)">
    <div v-if="win.description">{{ win.description }}</div>
    <div v-else class="text-secondary">Опису ще нема.</div>
    <div><button type="button" class="btn btn-link btn-sm p-0 text-decoration-none" @click="go">до опису вікна <Icon name="right" /></button></div>
  </div>
</template>

<style scoped>
.gg-panel { position: absolute; z-index: 40; width: 18rem; max-width: calc(100% - .5rem); padding: .6rem; font-size: .875rem; }
.thumb { max-width: 100%; max-height: 9rem; align-self: flex-start; cursor: zoom-in; }
</style>
