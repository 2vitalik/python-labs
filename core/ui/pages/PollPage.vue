<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { usePolling } from '../activity.js'
import { closePoll, deletePoll, getPoll, getPollChats, pollToTemplate, retrySend, sendPoll } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import PollHead from '../components/PollHead.vue'
import PollResults from '../components/PollResults.vue'
import PollSends from '../components/PollSends.vue'
import PollTargets from '../components/PollTargets.vue'
import { keepTargets, lastTargets } from '../polls.js'
import { useTitle } from '../title.js'

// one poll: where it went and who answered what; refreshes itself while it is open. A draft asks where to send it
const route = useRoute()
const router = useRouter()
const res = ref(null)
const places = ref(null)  // { chats, me } — loaded once there is something to send
const more = ref(false)
const targets = ref([])
const silent = ref(false)
const busy = ref(false)
const error = ref('')
const done = ref('')
const poll = computed(() => res.value?.poll)
const draft = computed(() => poll.value?.status === 'draft')
useTitle(() => poll.value?.title)

async function load() {
  res.value = await getPoll(route.params.id)
  if (draft.value && !places.value) {
    places.value = await getPollChats()
    targets.value = lastTargets(places.value)
  }
}
watch(() => route.params.id, (id) => id && load(), { immediate: true })
usePolling(() => poll.value?.status === 'open' && load().catch(() => {}), 10)  // a missed refresh is made up by the next one

async function act(step) {
  busy.value = true
  error.value = done.value = ''
  try {
    await step()
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
async function sendMore() {
  more.value = !more.value
  if (!places.value) places.value = await getPollChats()
}
const send = () => act(async () => {
  if (draft.value) keepTargets(targets.value)  // «ще кудись» is a one-off, the draft's first send is the usual one
  await sendPoll(poll.value.id, { targets: targets.value, silent: silent.value })
  targets.value = []
  more.value = false
  await load()
})
const retry = (s) => act(async () => {
  await retrySend(poll.value.id, s.id)
  await load()
})
const close = () => confirm('Закрити опитування? Telegram зупинить його в усіх чатах — голосувати більше не можна буде.')
  && act(async () => (res.value = await closePoll(poll.value.id)))
const toTemplate = () => act(async () => (done.value = `📋 Шаблон «${(await pollToTemplate(poll.value.id)).title}» створено`))
const remove = () => confirm('Видалити опитування? Голоси студентів тут не пропадуть — лише твої спроби.')
  && act(async () => {
    await deletePoll(poll.value.id)
    router.push('/polls')
  })
</script>

<template>
  <div v-if="poll">
    <Crumbs :items="[['/polls', 'Опитування'], poll.title]" />
    <PollHead :poll :can-delete="res.can_delete" :busy @template="toTemplate" @remove="remove" />
    <div v-if="done" class="alert alert-success py-2">{{ done }} — <RouterLink to="/polls/templates">до шаблонів</RouterLink></div>
    <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>

    <div v-if="res.sends.length || !draft" class="mb-4">
      <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
        <h2 class="h5 mb-0 me-auto">Де опитування</h2>
        <button v-if="poll.status === 'open'" type="button" class="btn btn-outline-secondary btn-sm" @click="sendMore">➕ Ще кудись</button>
        <button v-if="poll.status === 'open'" type="button" class="btn btn-outline-danger btn-sm" :disabled="busy" @click="close">⏹ Закрити</button>
      </div>
      <PollSends :sends="res.sends" :open="poll.status !== 'closed'" @retry="retry" />
    </div>

    <div v-if="(draft || more) && places" class="card card-body mb-4">
      <div class="fw-semibold mb-2">{{ draft ? 'Куди надіслати' : 'Куди ще' }}</div>
      <PollTargets v-model="targets" v-model:silent="silent" :chats="places.chats" :me="places.me" :sent="res.sends" />
      <div class="mt-2">
        <button type="button" class="btn btn-primary" :disabled="busy || !targets.length" @click="send">🚀 Надіслати</button>
        <span v-if="busy" class="small text-secondary ms-2">Надсилаю…</span>
      </div>
    </div>

    <PollResults v-if="!draft" :res />
  </div>
</template>
