<script setup>
import { STATUS, moment, optionLabel } from '../polls.js'

// a poll in the list: what it asks, where it went, how many answer now; the warnings lead to the details on its page
defineProps({ p: { type: Object, required: true } })
// «ПЗПІ-25 Python › 25-1 пари, 25-2 пари»: the topics of one forum under its name once
function places(p) {
  const by = new Map()
  for (const s of p.sends.filter((x) => x.status !== 'failed')) {
    const [chat, topic] = s.where.split(' › ')
    by.set(chat, new Set([...(by.get(chat) || []), ...(topic ? [topic] : [])]))
  }
  return [...by].map(([chat, topics]) => [chat, [...topics].join(', ')].filter(Boolean).join(' › ')).join(' · ')
}
const failed = (p) => p.sends.some((s) => s.status === 'failed')
</script>

<template>
  <RouterLink :to="`/polls/${p.id}`" class="poll card card-body py-2 px-3 text-reset text-decoration-none">
    <div class="d-flex align-items-baseline gap-2">
      <span :title="STATUS[p.status].text">{{ STATUS[p.status].icon }}</span>
      <span class="fw-semibold text-break">{{ p.title }}</span>
      <span v-if="p.mismatch" class="small text-warning-emphasis" title="Telegram рахує інакше, ніж дійшло до нас — деталі всередині">⚠️ не всі голоси</span>
      <span v-if="failed(p)" class="small text-danger" title="Telegram не прийняв опитування в якомусь чаті — деталі всередині">❌ не всюди надіслано</span>
      <span v-if="p.status !== 'draft'" class="ms-auto text-nowrap" title="Скільки людей відповіли зараз, без спроб викладачів">👥 {{ p.voters }}</span>
    </div>
    <div class="small text-break">{{ p.question }}</div>
    <div class="small text-secondary d-flex flex-wrap column-gap-2">
      <span>{{ p.options.map(optionLabel).join(' · ') }}</span>
      <span v-for="t in p.tags" :key="t">#{{ t }}</span>
    </div>
    <div class="small text-secondary">
      <template v-if="p.status === 'draft'">📝 чернетка · {{ moment(p.created_at) }}</template>
      <template v-else>📍 {{ places(p) || '—' }} · {{ moment(p.sent_at) }}<template v-if="p.closed_at"> · закрито {{ moment(p.closed_at) }}</template></template>
    </div>
  </RouterLink>
</template>

<style scoped>
.poll:hover { border-color: var(--bs-secondary-color); }
</style>
