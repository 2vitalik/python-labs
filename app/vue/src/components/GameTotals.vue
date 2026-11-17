<script setup>
import { computed } from 'vue'

import { plural } from '@core/plural.js'
import { COIN_NAMES, COIN_ORDER, COINS, vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { gradeOf, woodOf } from '../grade.js'

// a game in numbers (T284 §4): what is described — a tile each, the number over its word — and the wallet: a line per
// kind of coin, claimed and accepted, their sum in 🌱 under them; the slot under the tiles is the editor's controls.
// The grade the accepted coins would give shows only to whom the API hands the scale (the teacher, while it is a draft).
// A tile per section that is shown (T319); the coins of cards asked for wait apart, under the sums — they are in none
const props = defineProps({ counts: Object, coins: Object })
const ed = useEd()
defineEmits(['go'])  // a tile is the way to its section; «картки» — to everything claimed as a tree
const WORDS = {
  entities: ['сутність', 'сутності', 'сутностей'], windows: ['вікно', 'вікна', 'вікон'], rules: ['правило', 'правила', 'правил'],
  levels: ['рівень', 'рівні', 'рівнів'], cards: ['картка', 'картки', 'карток'],
}
const FEATURES = ['levels', 'cards']  // the tiles that are features of their own name
const tiles = computed(() => Object.keys(WORDS).filter((k) => !FEATURES.includes(k) || ed.has(k))
  .map((k) => ({ k, n: props.counts[k] || 0, word: plural(props.counts[k] || 0, ...WORDS[k]) })))
const rows = computed(() => COIN_ORDER.filter((c) => props.coins?.claimed?.[c] || props.coins?.accepted?.[c]))
const sum = computed(() => ({ claimed: woodOf(props.coins?.claimed), accepted: woodOf(props.coins?.accepted), asked: woodOf(props.coins?.asked) }))
const grade = computed(() => ({ claimed: gradeOf(sum.value.claimed), accepted: gradeOf(sum.value.accepted) }))
const fmt = (n) => (n ? String(+n.toFixed(1)).replace('.', ',') : '—')
</script>

<template>
  <div class="totals">
    <div class="left">
      <div class="tiles">
        <button v-for="t in tiles" :key="t.k" type="button" class="tile" :title="t.k === 'cards' ? 'усе заявлене — деревом' : 'до секції'" @click="$emit('go', t.k)"><b>{{ t.n }}</b><span>{{ t.word }}</span></button>
      </div>
      <slot />
    </div>
    <div v-if="rows.length || sum.asked" class="wallet-box group-box">
    <table class="wallet">
      <thead><tr><th>монетки</th><th title="картка рахується не більше разів, ніж дозволяє">заявлено</th><th title="після перевірки викладачем">зараховано</th></tr></thead>
      <tbody>
        <tr v-for="c in rows" :key="c"><td>{{ COINS[c] }} {{ COIN_NAMES[c] }}</td><td>{{ fmt(coins.claimed?.[c]) }}</td><td class="ok">{{ fmt(coins.accepted?.[c]) }}</td></tr>
      </tbody>
      <tfoot>
        <tr title="кожна наступна монетка вдвічі дорожча: 📎 = 2 🌱, 🥉 = 4, 🥈 = 8, 🥇 = 16, 👑 = 32"><td>разом у 🌱</td><td>{{ fmt(sum.claimed) }}</td><td class="ok">{{ fmt(sum.accepted) }}</td></tr>
        <tr v-if="grade.claimed !== null" class="grade" :title="vocab.grade.draft ? 'чернетка шкали: бачить лише викладач, поки шкалу не затверджено' : 'за шкалою курсу'">
          <td>оцінка<span v-if="vocab.grade.draft" class="draft"> · чернетка шкали</span></td><td>≈ {{ grade.claimed }}</td><td class="ok">≈ {{ grade.accepted }}</td>
        </tr>
        <tr v-if="sum.asked" class="asked" title="картки за запитом: зарахуються, коли викладач відкриє картку"><td>за запитом</td><td>{{ fmt(sum.asked) }}</td><td /></tr>
      </tfoot>
    </table>
    </div>
  </div>
</template>

<style scoped>
.totals { display: flex; flex-wrap: wrap; align-items: flex-start; justify-content: space-between; gap: .75rem 1.5rem; }
.left { display: flex; flex-direction: column; gap: .6rem; min-width: 0; flex: 1 1 18rem; }
.tiles { display: flex; flex-wrap: wrap; gap: .4rem; }
.tile { display: flex; flex-direction: column; align-items: center; min-width: 4.6rem; padding: .3rem .6rem .35rem; border: 1px solid var(--bs-border-color); border-radius: .5rem;
        background: none; color: inherit; line-height: 1.15; }
.tile:hover { border-color: var(--bs-secondary-color); background: var(--bs-tertiary-bg); }
.tile b { font-size: 1.35rem; font-weight: 600; font-variant-numeric: tabular-nums; }
.tile span { font-size: .72rem; color: var(--bs-secondary-color); }
.wallet-box { flex: 0 0 auto; padding-top: .35rem; }
.wallet { font-size: .8rem; font-variant-numeric: tabular-nums; }
.wallet th { padding: 0 0 .15rem .9rem; font-size: .68rem; font-weight: 600; letter-spacing: .03em; color: var(--bs-secondary-color); text-align: end; }
.wallet th:first-child, .wallet td:first-child { padding-left: 0; text-align: start; }
.wallet td { padding: .05rem 0 .05rem .9rem; text-align: end; }
.wallet tbody tr + tr td { border-top: 1px dotted var(--bs-border-color); }
.wallet tfoot td { border-top: 1px solid var(--bs-border-color); font-weight: 600; }
.wallet .ok { color: var(--bs-success-text-emphasis); }
.wallet .grade td { border-top: 0; font-weight: 400; color: var(--bs-secondary-color); }
.wallet .grade .ok { color: var(--bs-success-text-emphasis); font-weight: 600; }
.wallet .asked td { border-top: 1px dotted var(--bs-border-color); font-weight: 400; color: var(--bs-secondary-color); }
.draft { font-size: .68rem; }
</style>
