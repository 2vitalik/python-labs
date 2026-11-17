<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { useAutosave } from '@core/autosave.js'
import Crumbs from '@core/components/Crumbs.vue'
import DelButton from '@core/components/DelButton.vue'
import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import { useTitle } from '@core/title.js'
import { lookAs } from '@core/user.js'
import { deleteDefense, getDefense, putDefense } from '../api.js'
import { COINS } from '../catalog.js'
import DefenseClock from '../components/DefenseClock.vue'
import DefenseHead from '../components/DefenseHead.vue'
import DefenseRates from '../components/DefenseRates.vue'
import DefenseResult from '../components/DefenseResult.vue'
import RemarkInput from '../components/RemarkInput.vue'
import RemarkRow from '../components/RemarkRow.vue'
import { loadVocab, vocab } from '../defense.js'
import '../defense.css'

// the teacher's desk for one defense (T327 §3), narrow enough to stand beside the game's tab: who and when · what is owed
// from the defenses before · the remarks, dictated at the bottom of their list as in a chat · impressions in clicks ·
// a note · the result and «send». Every click is saved at once
const route = useRoute()
const router = useRouter()
const d = ref(null)
const error = ref('')
useTitle(() => d.value?.student.name)
const load = async () => { d.value = await getDefense(route.params.id) }
async function set(patch) {
  Object.assign(d.value, patch)  // at once: a click does not wait for the server
  try {
    Object.assign(d.value, await putDefense(d.value.id, patch))
    error.value = ''
  } catch (e) {
    error.value = e.message
    load()
  }
}
const note = useAutosave(() => putDefense(d.value.id, { note: d.value.note }))
function changed(r) {
  for (const list of [d.value.remarks, d.value.debts]) {
    const i = list.findIndex((x) => x.id === r.id)
    if (i >= 0) list[i] = r
  }
}
const removed = (id) => (d.value.remarks = d.value.remarks.filter((r) => r.id !== id))
// a model sorts the new lines a moment after they are added (remark_ai.py): the list is read again, the rest of the page stays
async function added(rows) {
  d.value.remarks.push(...rows)
  if (!vocab.value.ai) return
  for (const ms of [4000, 10000]) setTimeout(async () => { if (d.value) d.value.remarks = (await getDefense(d.value.id)).remarks }, ms)
}
const numberOf = (id) => d.value.remarks.findIndex((r) => r.id === id) + 1
const coins = computed(() => {  // {coin: n} the remarks promise for the rework
  const sum = {}
  for (const r of d.value.remarks) if (r.coin) sum[r.coin] = (sum[r.coin] || 0) + r.amount
  return Object.entries(sum).map(([c, n]) => `${COINS[c]}${n === 1 ? '' : `×${n}`}`).join(' ')
})
const drop = () => deleteDefense(d.value.id).then(() => router.push('/defenses'), (e) => (error.value = e.message))

onMounted(async () => {
  try {
    await Promise.all([loadVocab(), load()])
  } catch (e) {
    error.value = e.message
  }
})
</script>

<template>
  <div class="desk">
    <Crumbs :items="[['/defenses', 'Захисти'], d?.student.name || '…']">
      <button v-if="d" type="button" class="btn btn-outline-secondary btn-sm ms-auto" title="Сторінка зауважень, як її бачить студент"
              @click="lookAs(d.student.nick, '/my/remarks')"><Icon name="eye" /> Очима студента</button>
      <DelButton v-if="d && !d.sent_at" what="захист із його зауваженнями" @yes="drop" />
    </Crumbs>
    <div v-if="error" class="alert alert-danger py-2">{{ error }}</div>
    <template v-if="d && vocab">
      <DefenseHead :d @set="set" />
      <DefenseClock :d @set="set" />

      <details v-if="d.debts.length" class="debts" open>
        <summary>З минулих захистів не закрито: {{ d.debts.length }}</summary>
        <RemarkRow v-for="(r, i) in d.debts" :key="r.id" :r :n="i + 1" can @changed="changed" />
      </details>

      <h2 class="h6 mt-4 mb-1">Зауваження <span class="dhint">{{ d.remarks.length || '' }}</span></h2>
      <RemarkRow v-for="(r, i) in d.remarks" :key="r.id" :r :n="i + 1" :start="d.started_at" :like="numberOf(r.hint?.like)" can @changed="changed" @removed="removed" />
      <p v-if="!d.remarks.length" class="dhint my-2">Поки жодного — перше зʼявиться тут, щойно додаси.</p>
      <RemarkInput :id="d.id" class="mt-2" @added="added" />
      <div v-if="coins" class="dhint mt-1">Монетки за доробку, якщо прийняти все: {{ coins }} — у гаманець поки не входять</div>

      <h2 class="h6 mt-4 mb-1">Враження <span class="dhint">бачиш лише ти</span></h2>
      <DefenseRates :d @set="set" />
      <div class="dsub">Нотатка для себе
        <span class="saved">{{ { dirty: '…', saving: 'зберігаю', failed: 'не збереглось' }[note.state.value] }}</span></div>
      <GrowArea v-model="d.note" class="form-control" placeholder="своїми словами: що запамʼятати про цей захист" @input="note.touch()" />

      <h2 class="h6 mt-4 mb-1">Підсумок</h2>
      <DefenseResult :d @set="set" @sent="load" />
    </template>
  </div>
</template>

<style scoped>
.desk { max-width: 44rem; }
.debts { margin-top: .8rem; padding: .3rem .6rem; border: 1px solid var(--bs-warning-border-subtle); border-radius: .45rem;
         background: color-mix(in srgb, var(--bs-warning-bg-subtle) 45%, var(--bs-body-bg)); }
.debts summary { font-size: .86rem; font-weight: 600; }
.saved { margin-left: .5rem; letter-spacing: 0; text-transform: none; }
</style>
