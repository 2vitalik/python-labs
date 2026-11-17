<script setup>
import { onMounted, ref } from 'vue'

import Crumbs from '@core/components/Crumbs.vue'
import { getMyRemarks } from '../api.js'
import MyRemark from '../components/MyRemark.vue'
import { dayOf, labsText, setVocab, span, word } from '../defense.js'
import '../defense.css'

// the student's remarks, a defense after a defense, the newest first (T328 §4): the result, what still waits for an
// answer — and an answer to each remark right in it
const data = ref(null)
const error = ref('')
const RESULTS = { passed: 'Захист зараховано.', cond: 'Зараховано з умовою: закрий усі борги — зауваження з червоною позначкою.',
                  again: 'Потрібен повторний захист.' }
const left = (d) => d.remarks.filter((r) => ['open', 'returned'].includes(r.state) && r.kind !== 'tip').length
const debts = (d) => d.remarks.filter((r) => r.kind === 'debt' && r.state !== 'accepted').length
function changed(r) {
  for (const d of data.value.defenses) {
    const i = d.remarks.findIndex((x) => x.id === r.id)
    if (i >= 0) d.remarks[i] = r
  }
}
onMounted(async () => {
  try {
    const d = await getMyRemarks()
    setVocab(d.vocab)
    data.value = d
  } catch (e) {
    error.value = e.message
  }
})
</script>

<template>
  <div>
    <Crumbs :items="['Зауваження']" />
    <h1 class="h3">Зауваження після захисту</h1>
    <p class="text-secondary">На кожне зауваження потрібна відповідь: виправив — посилання на коміт, не виправляв — рядок чому.
      Викладач перевірить і прийме або поверне.</p>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>

    <template v-if="data">
      <section v-for="d in data.defenses" :key="d.id" class="mb-4">
        <h2 class="h5 mb-1">Захист {{ dayOf(d.started_at) }}
          <span class="dhint">{{ labsText(d.labs) }} · {{ word('kinds', d.kind)?.text }}<template v-if="d.minutes"> · {{ span(d.minutes) }}</template></span></h2>
        <div v-if="d.result" class="result" :class="d.result">{{ word('results', d.result)?.icon }} {{ RESULTS[d.result] }}
          <template v-if="d.result === 'cond'"> Лишилось боргів: {{ debts(d) }}.</template></div>
        <div class="dhint mb-1">
          <template v-if="d.remarks.length">прийнято {{ d.counts.accepted }} із {{ d.counts.all }}<template v-if="left(d)"> · чекають твоєї відповіді: {{ left(d) }}</template></template>
          <template v-else>Зауважень нема</template>
        </div>
        <MyRemark v-for="(r, i) in d.remarks" :key="r.id" :r :n="i + 1" @changed="changed" />
      </section>
      <p v-if="!data.defenses.length" class="text-secondary text-center mt-4">Зауважень поки нема — вони зʼявляться тут після захисту.</p>
    </template>
  </div>
</template>

<style scoped>
.result { margin-bottom: .2rem; font-weight: 600; }
.result.again { color: var(--bs-danger-text-emphasis); }
.result.passed { color: var(--bs-success-text-emphasis); }
</style>
