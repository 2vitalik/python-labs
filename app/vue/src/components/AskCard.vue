<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { plural } from '@core/plural.js'
import { subzoneTitle, taskIndex, vocab, zoneOf } from '../catalog.js'
import { saveTask } from '../taskForm.js'
import AskRow from './AskRow.vue'
import CardSign from './CardSign.vue'
import CoinBadge from './CoinBadge.vue'

// a card on «Запити» (T319): what it is, how many games ask for it and «Відкрити для всіх» — the card goes into the core,
// its requests become ordinary claims (an edit of the card: the history keeps it); a line in its place then offers it
// back. Under it — the requests with their sentences; those without one (a type, a parameter) — a quiet count of who
const props = defineProps({ ask: Object })
const emit = defineEmits(['changed'])
const t = computed(() => props.ask.task)
const card = computed(() => taskIndex.value[t.value.slug])
const home = computed(() => [zoneOf(t.value).title, subzoneTitle(t.value), vocab.value.kinds[t.value.kind]].filter(Boolean).join(' · '))
const said = computed(() => props.ask.claims.filter((c) => !c.auto))
const auto = computed(() => props.ask.claims.filter((c) => c.auto))
const who = (list) => new Set(list.map((c) => c.nick)).size
const asking = computed(() => {
  const real = who(props.ask.claims.filter((c) => !c.test)), test = who(props.ask.claims.filter((c) => c.test))
  return [real && `${real} ${plural(real, 'гра', 'гри', 'ігор')}`, test && `${test} ${plural(test, 'тестова', 'тестові', 'тестових')}`].filter(Boolean).join(' і ')
})
const opened = ref(false)
const busy = ref(false)
const error = ref('')
async function open(on) {
  busy.value = true
  error.value = ''
  try {
    await saveTask(card.value, { core: on })
    opened.value = on
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div v-if="opened" class="ask-card done d-flex flex-wrap align-items-center gap-2">
    <span><Icon name="check" class="text-success" /> «{{ t.title }}» — в основі для всіх, запити на неї стали заявками</span>
    <button type="button" class="btn btn-sm btn-outline-secondary ms-auto" :disabled="busy" @click="open(false)"><Icon name="back" /> Повернути</button>
    <span v-if="error" class="text-danger small w-100">{{ error }}</span>
  </div>
  <div v-else class="ask-card">
    <div class="head d-flex flex-wrap align-items-center gap-2">
      <span v-peek="{ kind: 'task', id: t.slug }" class="title me-auto">
        <CardSign :task="t" class="sign" />
        <span v-if="t.icon">{{ t.icon }}</span>
        <RouterLink :to="{ path: '/tasks', query: { q: t.slug } }" class="fw-semibold">{{ t.title }}</RouterLink>
        <CoinBadge :coin="t.coin" :amount="t.amount" />
      </span>
      <button type="button" class="btn btn-sm btn-success" :disabled="busy || !card" @click="open(true)"
              title="Покласти картку в основу: студенти заявлятимуть її одразу, а всі запити на неї стануть звичайними заявками">
        <Icon name="check" /> Відкрити для всіх</button>
    </div>
    <div class="sub">{{ home }} · просять: {{ asking }}</div>
    <div v-if="error" class="text-danger small px-2">{{ error }}</div>
    <AskRow v-for="c in said" :key="c.id" :claim="c" :task="t" @changed="emit('changed')" />
    <div v-if="auto.length" class="auto">
      без пояснення: {{ auto.length }} — {{ (vocab.kinds[t.kind] || 'картка').toLowerCase() }} у:
      <template v-for="(c, i) in auto" :key="c.id">{{ i ? ', ' : '' }}<RouterLink :to="`/students/${c.nick}#${c.anchor}`">{{ c.name }}</RouterLink></template>
    </div>
  </div>
</template>

<style scoped>
.ask-card { border: 1px solid var(--bs-border-color); border-radius: .4rem; }
.ask-card.done { padding: .4rem .6rem; font-size: .9rem; color: var(--bs-secondary-color); }
.head { padding: .45rem .6rem 0; }
.title { display: inline-flex; flex-wrap: wrap; align-items: center; gap: .35rem; min-width: 0; }
.sub { padding: 0 .6rem .45rem; font-size: .78rem; color: var(--bs-secondary-color); }
.auto { padding: .35rem .6rem; border-top: 1px solid var(--bs-border-color-translucent); font-size: .78rem; color: var(--bs-secondary-color); }
</style>
