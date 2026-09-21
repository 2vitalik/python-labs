<script setup>
import { computed } from 'vue'

import { zones } from '../catalog.js'
import { useTaskFilter } from '../taskFilter.js'
import MasonryGroups from './MasonryGroups.vue'
import ZoneNav from './ZoneNav.vue'

const props = defineProps({ game: { type: String, default: '' } })
const { f, set, counts, grouped } = useTaskFilter(props.game)
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))
</script>

<template>
  <ZoneNav :zones="zones" :counts="counts" :zone="f.zone" :sub="f.sub"
           @select="(z, s) => set({ zone: z, sub: s })" />

  <p v-if="!shown" class="text-secondary mt-3">Нічого не знайдено — спробуй інші слова чи зніми фільтри.</p>
  <section v-for="z in grouped" :id="'zone-' + z.key" :key="z.key" class="zone noflash mb-4">
    <h2 v-if="!f.zone" class="h6 zone-head" :style="{ '--zc': z.color }">
      {{ z.icon }} {{ z.title }} <span class="count">{{ counts[z.key] || 0 }}</span>
    </h2>
    <MasonryGroups :zone="z.key" :color="z.color" :subs="z.subs" />
  </section>
</template>

<style scoped>
.zone { scroll-margin-top: 1rem; }
.zone-head {
  color: var(--zc); font-weight: 700;
  border-bottom: 2px solid color-mix(in srgb, var(--zc) 30%, #fff);
  padding-bottom: .25rem; margin-bottom: .75rem;
}
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
