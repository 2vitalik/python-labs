<script setup>
import { computed } from 'vue'

import { postClaim } from '../api.js'
import { zones } from '../catalog.js'
import { anchorKind } from '../myGame.js'
import CardPicker from './CardPicker.vue'
import ClaimChip from './ClaimChip.vue'

// claims that belong to the game itself, by zone (логіка · рівні · інтерфейс · код · супровід); the ones that
// want an entity or a window but have none yet are the drafts — shown apart with a nudge to anchor them
const props = defineProps({ claims: Array, parts: Array, info: Function, editable: Boolean, judge: Boolean, nick: String, drafts: Boolean })
const emit = defineEmits(['changed', 'error'])
const mine = computed(() => props.claims.filter((c) => !c.part && (anchorKind(props.info(c.task)) !== 'game') === props.drafts))
const byZone = computed(() => {
  const m = {}
  for (const c of mine.value) (m[props.info(c.task)?.zone || '?'] ??= []).push(c)
  return Object.keys(zones.value).filter((z) => m[z]).map((z) => ({ z, ...zones.value[z], list: m[z] })).concat(m['?'] ? [{ z: '?', title: 'інше', icon: '·', color: '#888', list: m['?'] }] : [])
})
const notGame = (t) => anchorKind(t) === 'game'
async function add(task, params) {
  try {
    await postClaim({ task, params })
    emit('changed')
  } catch (e) {
    emit('error', e.message)
  }
}
</script>

<template>
  <div class="vstack gap-2">
    <div v-for="g in byZone" :key="g.z" class="d-flex flex-wrap align-items-start gap-1">
      <span v-if="byZone.length > 1 || !drafts" class="zone small text-nowrap me-1" :style="{ color: g.color }">{{ g.icon }} {{ g.title }}</span>
      <ClaimChip v-for="c in g.list" :key="c.id" :claim="c" :info="info(c.task)" :parts :editable :judge :nick @changed="emit('changed')" />
    </div>
    <p v-if="!mine.length && !drafts" class="text-secondary small mb-0">Що в грі є загалом: перемога й поразка, рівні, збереження, рекорди, код і тести, відео — картки без привʼязки до сутності чи вікна.</p>
    <CardPicker v-if="editable && !drafts" placeholder="＋ картка рівня гри: рівні, рахунок, збереження, код, тести, відео…" :filter="notGame" loose
                :claimed="new Set(claims.filter((c) => !c.part).map((c) => c.task))" @pick="add" />
  </div>
</template>

<style scoped>
.zone { font-weight: 600; line-height: 1.9; }
[data-bs-theme=dark] .zone { filter: brightness(1.5); }
</style>
