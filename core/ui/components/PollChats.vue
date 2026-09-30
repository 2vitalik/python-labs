<script setup>
import { onMounted, ref } from 'vue'

import { ago } from '../activity.js'
import { getPollChats, putPollChat } from '../api.js'

// the places the bot has heard in: a group, a forum topic; the admin names them as they like and hides the ones not for polls
const chats = ref([])
const error = ref('')
const load = async () => (chats.value = (await getPollChats()).chats)

async function save(c, patch) {
  error.value = ''
  try {
    Object.assign(c, await putPollChat(c.id, patch))
  } catch (e) {
    error.value = e.message
  }
}
const rename = (c, e) => e.target.value.trim() !== c.name && save(c, { name: e.target.value })
onMounted(load)
</script>

<template>
  <div>
    <p class="small text-secondary">
      Бот запамʼятовує групу чи гілку форуму, щойно бачить там повідомлення, — він має бути в групі <b>адміністратором</b>.
      Нове місце — напиши в ньому будь-що. Назва тут — лише для тебе; у Telegram нічого не міняється.
    </p>
    <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
    <div v-for="c in chats" :key="c.id" class="d-flex flex-wrap align-items-center gap-2 py-1 border-bottom" :class="{ 'opacity-50': c.hidden || c.left }">
      <input class="form-control form-control-sm name" :value="c.name" :placeholder="[c.title, c.topic || (c.thread_id ? `#${c.thread_id}` : '')].filter(Boolean).join(' › ')"
             :title="`${c.title} · chat ${c.chat_id}${c.thread_id ? ` · гілка ${c.thread_id}` : ''}`" @change="rename(c, $event)" @keydown.enter="$event.target.blur()">
      <span class="small text-secondary">{{ c.thread_id ? 'гілка' : c.type === 'supergroup' ? 'форум' : 'група' }} · {{ ago(c.seen_at) }}</span>
      <span v-if="c.left" class="badge text-bg-warning fw-normal">бота там нема</span>
      <div class="form-check form-switch mb-0 ms-auto" title="Показувати серед місць, куди слати">
        <input :id="`chat-${c.id}`" class="form-check-input" type="checkbox" :checked="!c.hidden" @change="save(c, { hidden: !c.hidden })">
        <label class="form-check-label small" :for="`chat-${c.id}`">у списку</label>
      </div>
    </div>
    <p v-if="!chats.length" class="small text-secondary mb-0">Поки жодного місця.</p>
  </div>
</template>

<style scoped>
.name { flex: 1 1 14rem; max-width: 24rem; }
</style>
