<script setup>
import Icon from '@core/components/Icon.vue'
import { ai } from '../ai.js'
import AiDraft from './AiDraft.vue'
import AiInput from './AiInput.vue'

// «✨ Описати словами» of «＋ Додати» (T291 §14, T289 §1): the field to write in — or why there is none now — and under it
// every round of this game, the newest first
const WHY = { nokey: 'ШІ-помічник ще не підключено', budget: 'На цей місяць бюджет ШІ-помічника вичерпано — спробуй наступного місяця' }
</script>

<template>
  <div class="vstack gap-2">
    <AiInput v-if="ai.mode === 'on'" />
    <div v-else class="d-flex align-items-center gap-2 border rounded px-2 py-1 small text-secondary"><Icon name="spark" /> {{ WHY[ai.why] || 'ШІ-помічник зараз недоступний' }}</div>
    <AiDraft v-for="d in ai.drafts" :key="d.id" :draft="d" />
  </div>
</template>
