<script setup>
import { computed } from 'vue'

// where to send: first the admin's own chat with the bot — to see the poll before the students do —
// then the groups and forum topics the bot has heard in; places the poll is in already are ticked off
const picked = defineModel({ type: Array, required: true })  // TgChat ids and 'me'
const silent = defineModel('silent', { type: Boolean, default: false })
const props = defineProps({
  chats: { type: Array, default: () => [] },
  me: { type: Number, default: null },  // the admin's chat id; null — the bot is not linked
  sent: { type: Array, default: () => [] },  // sends of this poll: { chat_id, thread_id, status }
})
const places = computed(() => props.chats.filter((c) => !c.hidden && !c.left))
const there = (chatId, threadId) => props.sent.some((s) => s.chat_id === chatId && (s.thread_id ?? null) === (threadId ?? null)
                                                        && s.status !== 'failed')
</script>

<template>
  <div class="vstack gap-1">
    <label v-if="me" class="form-check">
      <input v-model="picked" class="form-check-input" type="checkbox" value="me" :disabled="there(me, null)">
      <span class="form-check-label">🧪 Мені особисто <span class="text-secondary small">— глянути, як виглядає, і проголосувати для проби</span>
        <span v-if="there(me, null)" class="text-success small"> ✔️ уже там</span></span>
    </label>
    <label v-for="c in places" :key="c.id" class="form-check">
      <input v-model="picked" class="form-check-input" type="checkbox" :value="c.id" :disabled="there(c.chat_id, c.thread_id)">
      <span class="form-check-label">📍 {{ c.where }} <span v-if="there(c.chat_id, c.thread_id)" class="text-success small">✔️ уже там</span></span>
    </label>
    <p v-if="!places.length" class="small text-secondary mb-1">
      Бот ще не бачив жодної групи. Додай його в групу чи форум <b>адміністратором</b> і напиши там будь-що — місце зʼявиться тут.
    </p>
    <p v-if="!me" class="small text-secondary mb-1">☝️ Щоб пробувати опитування на собі, привʼяжи бота у <RouterLink to="/my/profile">профілі</RouterLink>.</p>
    <div class="form-check form-switch mt-1">
      <input id="poll-silent" v-model="silent" class="form-check-input" type="checkbox">
      <label class="form-check-label" for="poll-silent">🔕 Тихо — без звуку сповіщення</label>
    </div>
  </div>
</template>
