<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getPoll, getPollChats, getPollTemplates, postPoll, putPoll, sendPoll } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import PollForm from '../components/PollForm.vue'
import PollTargets from '../components/PollTargets.vue'
import { useForm } from '../form.js'
import { emptyForm, fromPoll, keepTargets, lastTargets, review, toPayload, today } from '../polls.js'
import { useTitle } from '../title.js'

// a new poll — from a template (?template=), again after another one (?from=), or from scratch — and an edit (/polls/:id/edit).
// «Надіслати» saves the poll first: if Telegram refuses, nothing typed is lost, the poll page shows what went where
const route = useRoute()
const router = useRouter()
const { form, dirty, fill } = useForm(emptyForm())
const poll = ref(null)
const sends = ref([])
const templates = ref([])
const known = ref([])
const chats = ref([])
const me = ref(null)
const targets = ref([])
const silent = ref(false)
const busy = ref(false)
const error = ref('')
const draft = computed(() => !poll.value || poll.value.status === 'draft')
const r = computed(() => review(form))
const title = computed(() => (poll.value ? `Опитування: ${poll.value.title}` : 'Нове опитування'))
useTitle(title)

function fromTemplate(t) {
  fill(fromPoll(t))
  Object.assign(form, { title: `${t.title} ${today()}`, template: t.id })
}

onMounted(async () => {
  const [tpl, places] = await Promise.all([getPollTemplates(), getPollChats()])
  templates.value = tpl.templates
  known.value = tpl.tags
  chats.value = places.chats
  me.value = places.me
  if (route.params.id) {
    const res = await getPoll(route.params.id)
    poll.value = res.poll
    sends.value = res.sends
    fill(fromPoll(res.poll))
  } else if (route.query.from) {
    const res = await getPoll(route.query.from)
    fill({ ...fromPoll(res.poll), title: res.poll.title.replace(/\d{2}\.\d{2}$/, today()) })  // «Пара 24.09» → today's
  } else {
    const t = templates.value.find((x) => x.id === route.query.template)
    if (t) fromTemplate(t)
  }
  if (draft.value) targets.value = lastTargets(places)
})

async function run(step) {
  busy.value = true
  error.value = ''
  try {
    await step()
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
async function store() {
  const saved = poll.value ? await putPoll(poll.value.id, toPayload(form)) : await postPoll(toPayload(form))
  poll.value = saved
  fill(fromPoll(saved))
  return saved
}
const keep = () => run(async () => router.push(`/polls/${(await store()).id}`))
const send = () => run(async () => {
  const p = await store()
  keepTargets(targets.value)
  await sendPoll(p.id, { targets: targets.value, silent: silent.value })
  router.push(`/polls/${p.id}`)
})
</script>

<template>
  <div>
    <Crumbs :items="[['/polls', 'Опитування'], poll ? [`/polls/${poll.id}`, poll.title] : 'Нове', ...(poll ? ['Редагування'] : [])]" />
    <h1 class="h3 mb-3">{{ poll ? 'Редагування' : 'Нове опитування' }}</h1>

    <div v-if="!poll" class="d-flex flex-wrap align-items-center gap-1 mb-3">
      <span class="small text-secondary me-1">Шаблон:</span>
      <button v-for="t in templates" :key="t.id" type="button" class="btn btn-sm chip" :class="form.template === t.id ? 'btn-secondary' : 'btn-outline-secondary'"
              :title="t.question" @click="fromTemplate(t)">{{ t.title }}</button>
      <button type="button" class="btn btn-sm chip" :class="form.template ? 'btn-outline-secondary' : 'btn-secondary'" @click="fill(emptyForm())">з нуля</button>
      <RouterLink to="/polls/templates" class="small text-secondary ms-2">{{ templates.length ? 'усі шаблони' : 'зробити шаблон' }}</RouterLink>
    </div>

    <div class="card card-body mb-3">
      <PollForm v-model="form" :known :frozen="!draft" />
    </div>

    <div v-if="draft" class="card card-body mb-3">
      <div class="fw-semibold mb-2">Куди надіслати</div>
      <PollTargets v-model="targets" v-model:silent="silent" :chats :me :sent="sends" />
    </div>

    <div class="d-flex flex-wrap align-items-center gap-2">
      <button v-if="draft" type="button" class="btn btn-primary" :disabled="busy || !r.ready || !targets.length" @click="send">🚀 Надіслати</button>
      <button type="button" class="btn" :class="draft ? 'btn-outline-secondary' : 'btn-primary'" :disabled="busy || !r.ready || (!dirty && !!poll)"
              @click="keep">{{ draft ? '💾 Зберегти чернетку' : '💾 Зберегти' }}</button>
      <RouterLink :to="poll ? `/polls/${poll.id}` : '/polls'" class="btn btn-link text-secondary">Скасувати</RouterLink>
      <span v-if="draft && r.ready && !targets.length" class="small text-secondary">☝️ Обери, куди надіслати</span>
      <span v-if="busy" class="small text-secondary">Надсилаю…</span>
    </div>
    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>
