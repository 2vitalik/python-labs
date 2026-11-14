<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { familyPlaces } from '../claimPlace.js'
import { myGame } from '../myGame.js'

// a family's mark in its header on /tasks (T291 §7): an outlined tick with how many places its cards hold in the reader's
// game — not the green tick of «вже в грі»: the family is not picked, its cards are. A click lists them, each card with
// its places under it, one row a place; a row leads into the game
const props = defineProps({ task: Object })
const open = ref(false)
const picked = computed(() => (myGame.value ? familyPlaces(props.task) : []))
const count = computed(() => picked.value.reduce((n, p) => n + p.places.length, 0))
const title = computed(() => {
  const cards = picked.value.length
  return `у твоїй грі — картки звідси: ${cards}${count.value > cards ? `, місць: ${count.value}` : ''}; показати де`
})
</script>

<template>
  <span v-if="count" class="kids" @click.stop>
    <Pop v-model="open" width="18rem">
      <template #trigger="{ toggle }">
        <button type="button" class="kmark" :title @click="toggle"><Icon name="check" /><b>{{ count }}</b></button>
      </template>
      <div class="cap">у твоїй грі</div>
      <template v-for="p in picked" :key="p.task.slug">
        <div class="kid"><span v-if="p.task.icon" class="me-1">{{ p.task.icon }}</span>{{ p.task.title }}</div>
        <RouterLink v-for="pl in p.places" :key="pl.id" :to="{ path: '/my/game', hash: `#${pl.id}` }" class="place">
          <span>{{ pl.text }}</span><Icon name="arrow" />
        </RouterLink>
      </template>
    </Pop>
  </span>
</template>

<style scoped>
.kids { display: inline-flex; }
.kids :deep(.pop) { display: flex; }
/* outlined and grey-green: «something inside is in», not the solid tick of a picked card */
.kmark { display: inline-flex; align-items: center; gap: .1rem; height: 1.4rem; margin: -.05rem 0; padding: 0 .35rem 0 .25rem;
         border: 1px dashed color-mix(in srgb, var(--bs-success) 55%, var(--bs-secondary-color)); border-radius: .7rem; background: none;
         color: color-mix(in srgb, var(--bs-success) 60%, var(--bs-secondary-color)); font-size: .8rem; line-height: 1; }
.kmark b { font-size: .72rem; font-variant-numeric: tabular-nums; }
.kmark:hover { border-style: solid; background: color-mix(in srgb, var(--bs-success) 10%, transparent); color: var(--bs-success); }
.cap { margin-bottom: .2rem; font-size: .7rem; color: var(--bs-secondary-color); }
.kid { margin-top: .25rem; padding: 0 .35rem; font-size: .85rem; font-weight: 600; }
/* a place is a sub-item of its card */
.place { display: flex; align-items: center; justify-content: space-between; gap: .5rem; margin-left: .9rem; padding: .15rem .35rem;
         border-radius: .3rem; color: inherit; font-size: .82rem; text-decoration: none; }
.place:hover { background: var(--bs-tertiary-bg); }
.place .icon { color: var(--bs-secondary-color); }
</style>
