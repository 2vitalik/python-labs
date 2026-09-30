<script setup>
import { SENDS, moment, stuck } from '../polls.js'

// where the poll went: a line per chat or topic, with the link to the message, Telegram's error, and a warning
// when Telegram counts more voters than reached us — votes lost while the bot was down
defineProps({ sends: { type: Array, required: true }, open: Boolean })
defineEmits(['retry'])
const cls = { queued: 'text-secondary', sent: 'text-success', failed: 'text-danger', closed: 'text-secondary' }
const lost = (m) => `Telegram рахує ${m.telegram}, до нас дійшло ${m.ours}. Голоси губляться, коли бот не працює довше доби:`
  + ' Telegram тримає їх лише добу. Хто саме — не відновити; решта голосів збережена.'
</script>

<template>
  <div>
    <div v-for="s in sends" :key="s.id" class="send d-flex flex-wrap align-items-baseline gap-2 py-2 border-bottom">
      <span class="fw-semibold">📍 {{ s.where }}</span>
      <span class="small" :class="cls[s.status]">{{ SENDS[s.status] }} {{ moment(s.closed_at || s.sent_at || s.at) }}</span>
      <span v-if="s.silent" class="small" title="Надіслано без звуку сповіщення">🔕</span>
      <a v-if="s.url" :href="s.url" target="_blank" class="small">повідомлення ↗</a>
      <span v-if="s.state?.total != null" class="small text-secondary" title="Скільки голосують зараз — за лічильником Telegram">👥 {{ s.state.total }}</span>
      <span v-if="s.mismatch" class="badge text-bg-warning fw-normal" :title="lost(s.mismatch)">⚠️ Telegram: {{ s.mismatch.telegram }} · у нас: {{ s.mismatch.ours }}</span>
      <button v-if="open && stuck(s)" type="button" class="btn btn-outline-primary btn-sm py-0 ms-auto" @click="$emit('retry', s)">🔁 Повторити</button>
      <div v-if="s.error" class="w-100 small text-danger">{{ s.error }}</div>
    </div>
  </div>
</template>
