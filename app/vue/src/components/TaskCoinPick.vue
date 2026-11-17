<script setup>
import { ref, watch } from 'vue'

import InlinePop from '@core/components/InlinePop.vue'
import { COIN_NAMES, COINS } from '../catalog.js'
import { saveTask } from '../taskForm.js'
import { TIPS } from '../taskTips.js'
import CoinBadge from './CoinBadge.vue'
import TaskChoices from './TaskChoices.vue'

// a card's price where it reads, for the teacher (T306): a click on the coin — the coins with the time each stands for,
// the current one ticked, and how many of it; a coin is saved at once, the amount on Enter or leaving the field. Price
// steps, when the card has them, stay as they are
const p = defineProps({ task: Object, can: Boolean })
const open = ref(false)
const amount = ref(1)
watch(open, (on) => on && (amount.value = p.task.amount))
// the form's hint «ціна — час …: 🌱 до пів години · 📎 близько години · …» — its words over the list, the times by the emoji
const [cap, times] = TIPS.coin.split(': ')
const time = Object.fromEntries(times.split(' · ').map((s) => [s.slice(0, s.indexOf(' ')), s.slice(s.indexOf(' ') + 1)]))
const coins = [{ key: '', icon: '—', title: 'без монетки' },
  ...Object.entries(COINS).map(([k, e]) => ({ key: k, icon: e, title: COIN_NAMES[k], desc: time[e] }))]
const pick = (coin, choose, close) => (coin === p.task.coin ? close() : choose(saveTask(p.task, { coin })))
// leaving the field may come with the panel closing: a failed save opens it again to show why
function setAmount(choose, keep) {
  const a = amount.value === '' ? 1 : amount.value
  if (a === p.task.amount) return
  const work = saveTask(p.task, { amount: a })
  choose(work, { keep })
  work.catch(() => (open.value = true))
}
</script>

<template>
  <InlinePop v-model:open="open" :can width="17rem" :tip="`${COIN_NAMES[task.coin]}${task.amount !== 1 ? ` ×${task.amount}` : ''}\nКлік — змінити`">
    <span class="badge-in"><CoinBadge :coin="task.coin" :amount="task.amount" /></span>
    <template #panel="{ choose, close }">
      <div class="cap">{{ cap }}</div>
      <TaskChoices :items="coins" :current="task.coin" @pick="pick($event, choose, close)" />
      <label class="amt">скільки
        <input v-model.number="amount" type="number" step="0.5" min="0" class="form-control form-control-sm"
               @keydown.enter.prevent="setAmount(choose, false)" @keydown.esc="amount = task.amount" @blur="setAmount(choose, true)">
        <span>{{ COINS[task.coin] }}</span>
      </label>
    </template>
  </InlinePop>
</template>

<style scoped>
/* the badge's own tip («бронзова») would hide «Клік — змінити»: the trigger takes the mouse */
.badge-in > * { pointer-events: none; }
.cap { margin: 0 .5rem .3rem; font-size: .75rem; color: var(--bs-secondary-color); }
.amt { display: flex; align-items: center; gap: .4rem; margin: .4rem .5rem 0; padding-top: .45rem; border-top: 1px solid var(--bs-border-color-translucent);
       font-size: .8rem; color: var(--bs-secondary-color); }
.amt input { width: 4.5rem; }
</style>
