<script setup>
import { computed } from 'vue'

import { vPeek } from '@core/peek.js'
import { paramsText, taskIndex, zoneOf } from '../catalog.js'
import { useEd } from '../ed.js'
import CoinBadge from './CoinBadge.vue'

// the catalog cards a proposal claims (T289 §1), a row each as a claim looks in the description — coin, title, params,
// the category's colour on the left — and the card under the mouse. `list` — the reference node's `claims`: slug | {slug, params}
const props = defineProps({ list: Array })
const ed = useEd()
const rows = computed(() => (props.list || []).map((c) => (typeof c === 'string' ? { slug: c, params: {} } : { slug: c.slug, params: c.params || {} }))
  .map((c) => {
    const t = ed?.info(c.slug) || taskIndex.value[c.slug]
    return { ...c, t, ptext: paramsText(t, c.params) }
  }))
</script>

<template>
  <div v-if="rows.length" class="ai-cards">
    <span v-for="c in rows" :key="c.slug" v-peek="{ kind: 'task', id: c.slug }" class="ai-card" :style="{ '--zc': zoneOf(c.t).color }">
      <CoinBadge :coin="c.t?.coin" :amount="c.t?.amount" /> {{ c.t?.title || c.slug }}<span v-if="c.ptext" class="p"> · {{ c.ptext }}</span>
    </span>
  </div>
</template>

<style scoped>
.ai-cards { display: flex; flex-wrap: wrap; gap: .25rem; }
.ai-card { padding: 0 .4rem; border: 1px solid var(--bs-border-color); border-left: 3px solid var(--zc); border-radius: .3rem;
           background: var(--bs-body-bg); font-size: .8rem; overflow-wrap: anywhere; }
.p { color: var(--bs-secondary-color); }
</style>
