<script setup>
import { computed } from 'vue'

import { deleteClaimShot, uploadClaimShot } from '../api.js'
import { useEd } from '../ed.js'
import { PROOFS } from '../proof.js'
import ShotTiles from './ShotTiles.vue'

// the proof of a claim (T284 §7): up to three screenshots or gifs of what was done, opened over the page by a click.
// `editable` — the owner's panel: the violet tile (not in the sample's sandbox) and the round control on a thumbnail, each
// saved at once; while there is nothing yet, a quiet line says what the card asks to show — a hint, never a must
const props = defineProps({ claim: Object, editable: Boolean })
const MAX = 3  // as routes/my_claim_shots.py
const ed = useEd()
const shots = computed(() => props.claim.shots || [])
const proof = computed(() => PROOFS[ed.info(props.claim.task)?.proof])
const adds = computed(() => props.editable && !ed.sandbox && shots.value.length < MAX)
const ask = computed(() => {
  const p = proof.value
  if (!props.editable || !p || shots.value.length) return ''
  if (p.link) return props.claim.link ? '' : p.link  // a video, the code: the link field above is the place, the tile is a spare
  return adds.value ? p.ask : ''
})
</script>

<template>
  <div v-if="ask || adds || shots.length" class="vstack gap-1">
    <div v-if="ask" class="small text-secondary">{{ proof.icon }} {{ ask }}</div>
    <ShotTiles :game="claim.game" :names="shots" :adds :drops="editable" word="скриншот або гіфка" what="доказ"
               :add="(file) => uploadClaimShot(claim.id, file)" :drop="(name) => deleteClaimShot(claim.id, name)" />
  </div>
</template>
