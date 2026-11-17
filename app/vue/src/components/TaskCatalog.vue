<script setup>
import { computed } from 'vue'

import { useTaskFilter } from '../taskFilter.js'
import TaskGroups from './TaskGroups.vue'
import ZoneNav from './ZoneNav.vue'

// the catalog itself: the row of categories, then the cards by category and subcategory. On /tasks the filter is the
// address; in a window over a game's page (T318) it is the window's own, the categories are the place's, and the sections
// carry no ids — the page under the window has sections of the same names
const props = defineProps({ game: { type: String, default: '' } })
const { f, set, counts, grouped, zonesIn, subsIn, local } = useTaskFilter(props.game)
// a place with one category has it chosen from the start: its subcategories are the row to pick from
const only = computed(() => (local && Object.keys(zonesIn.value).length === 1 ? Object.keys(zonesIn.value)[0] : ''))
const zone = computed(() => f.value.zone || only.value)
</script>

<template>
  <ZoneNav :zones="zonesIn" :subs="subsIn" :counts="counts" :zone :sub="f.sub"
           @select="(z, s) => set({ zone: z, sub: s })" />

  <p v-if="!grouped.length" class="text-secondary mt-3">Нічого не знайдено — спробуй інші слова чи зніми фільтри.</p>
  <section v-for="z in grouped" :id="local ? null : 'zone-' + z.key" :key="z.key" class="zone noflash mb-4">
    <h2 v-if="!zone" class="h6 zone-head" :style="{ '--zc': z.color }">
      {{ z.icon }} {{ z.title }} <span class="count">{{ counts[z.key] || 0 }}</span>
    </h2>
    <TaskGroups :zone="z.key" :color="z.color" :subs="z.subs" :bare="local" />
  </section>
</template>

<style scoped>
.zone { scroll-margin-top: 1rem; }
.zone-head {
  color: var(--zc); font-weight: 700;
  border-bottom: 2px solid color-mix(in srgb, var(--zc) 30%, var(--bs-body-bg));
  padding-bottom: .25rem; margin-bottom: .75rem;
}
[data-bs-theme=dark] .zone-head { color: color-mix(in srgb, var(--zc) 60%, #fff); }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
