<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { lastOrder } from '@core/studentFilter.js'

// «‹ попередня · 3 з 27 · наступна ›» on a student's game page: through the list /students last showed in this tab, in its
// order and with its filters; a page reached by a direct link, or a student out of that list, has none
const props = defineProps({ nick: String })
const order = lastOrder()  // read once: the list is off screen while its pages are paged
const at = computed(() => order.indexOf(props.nick))
const prev = computed(() => order[at.value - 1])
const next = computed(() => order[at.value + 1])
</script>

<template>
  <nav v-if="at >= 0 && order.length > 1" class="d-flex justify-content-end align-items-center gap-2 small mb-2" aria-label="Інші ігри зі списку">
    <RouterLink v-if="prev" :to="`/students/${prev}`" :title="prev"><Icon name="left" /> попередня</RouterLink>
    <span v-else class="off"><Icon name="left" /> попередня</span>
    <span class="text-secondary">· {{ at + 1 }} з {{ order.length }} ·</span>
    <RouterLink v-if="next" :to="`/students/${next}`" :title="next">наступна <Icon name="right" /></RouterLink>
    <span v-else class="off">наступна <Icon name="right" /></span>
  </nav>
</template>

<style scoped>
a { text-decoration: none; }
.off { color: var(--bs-tertiary-color); }
</style>
