<script setup>
import { ref } from 'vue'

import Pop from '@core/components/Pop.vue'
import CoinBadge from './CoinBadge.vue'
import Md from '@core/components/Md.vue'

// «ⓘ» of an option tile (T278 §3): the whole description in a floating panel — on a phone the only way to read it
defineProps({ o: Object })
const open = ref(false)
</script>

<template>
  <Pop v-model="open" width="20rem">
    <template #trigger="{ toggle }">
      <button type="button" class="info" :class="{ on: open }" :aria-expanded="open" :aria-label="`Повний опис: ${o.label}`"
              title="Повний опис" @click="toggle">
        <svg class="icon" viewBox="0 0 16 16" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="1.5"
             stroke-linecap="round" aria-hidden="true">
          <circle cx="8" cy="8" r="6.5" /><path d="M8 7.4v3.8" /><path d="M8 4.9h.01" stroke-width="2" />
        </svg>
      </button>
    </template>
    <div class="vstack gap-2">
      <div class="d-flex align-items-baseline gap-2">
        <span class="fw-semibold">{{ o.icon }} {{ o.label }}</span>
        <CoinBadge :coin="o.coin" class="ms-auto" />
      </div>
      <Md :text="o.desc" class="desc" />
      <!-- a new tab: the form under the panel is not saved yet -->
      <RouterLink v-if="o.slug" :to="{ path: '/tasks', query: { q: o.slug } }" target="_blank" class="small align-self-start"
                  title="Картка в каталозі — у новій вкладці">у каталозі →</RouterLink>
    </div>
  </Pop>
</template>

<style scoped>
.info { display: inline-flex; align-items: center; justify-content: center; width: 1.1rem; height: 1.1rem; padding: 0;
        border: 0; border-radius: 50%; background: none; color: var(--bs-secondary-color); font-size: .85rem; }
.info:hover, .info.on { color: var(--bs-body-color); background: color-mix(in srgb, var(--bs-body-color) 10%, transparent); }
.desc { font-size: .85rem; }
</style>
