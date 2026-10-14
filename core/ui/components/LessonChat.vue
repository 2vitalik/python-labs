<script setup>
import { computed, ref } from 'vue'

import { parseChat } from '../lesson.js'
import IconChevron from './IconChevron.vue'

// Zoom's chat of the meeting, folded: links and questions typed during the class
const props = defineProps({ text: String })
const open = ref(false)
const rows = computed(() => parseChat(props.text))
</script>

<template>
  <div class="mt-4">
    <a href="#" class="fold text-decoration-none text-reset d-inline-flex align-items-center gap-1" @click.prevent="open = !open">
      <IconChevron :dir="open ? 'down' : 'right'" :size="12" /><span class="fw-semibold">💬 Чат Zoom</span>
      <span class="text-secondary small">· {{ rows.length }} повідомлень</span>
    </a>
    <table v-if="open" class="table table-sm small mt-2 mb-0">
      <tbody>
        <tr v-for="(r, i) in rows" :key="i">
          <td class="text-body-tertiary text-nowrap">{{ r.time }}</td>
          <td class="text-nowrap fw-semibold">{{ r.who }}<span v-if="r.to" class="fw-normal text-body-tertiary"> → {{ r.to }}</span></td>
          <td class="text-break" style="white-space: pre-line">{{ r.text }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style scoped>
.fold:hover .fw-semibold { text-decoration: underline; }
td { border-color: var(--bs-border-color-translucent); }
</style>
