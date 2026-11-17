<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import { vPeek } from '@core/peek.js'
import { statOf } from '../catalog.js'
import JudgeMark from './JudgeMark.vue'

// stats where they read: the name on the left, the value and the unit on the right — or, `pills`, in a row of pills (a
// level's). With `can` a value, an own stat's name and its unit open on a click (T306). With `tools` (the card's pencil,
// T310) every row gets its minus and an own stat without a unit — «＋ од.». «＋ параметр» is by the block's caption
// (StatAdd, T350), and the stat picked there comes here — begin(): it stands as the last row with its value open and is
// saved once it has one — the server takes no stat without a value; an own one asks for its name first. `free` — no
// catalog, own names only; `auto` — the part's auto-claims (the teacher's marks); `save(fn)` — fn(list as it is now) →
// the new list, awaited
const p = defineProps({ stats: { type: Array, default: () => [] }, auto: { type: Array, default: () => [] }, can: Boolean, tools: Boolean,
  free: Boolean, pills: Boolean, save: Function })
const writing = ref('')  // the stat whose value is open: its card under the mouse would cover the field
const draft = ref(null)  // { key, label, unit, own } — a new stat that waits for its value
defineExpose({ begin: (d) => (draft.value = d) })
const card = (s) => (p.free ? null : statOf(s.key))
const sign = (s) => (p.free ? '' : `${card(s)?.icon || '•'} `)
const claimOf = (s) => (card(s)?.slug ? p.auto.find((c) => c.task === card(s).slug) : null)
// with the tools on a row's card under the mouse would cover the row below
const peek = (s) => (!p.tools && writing.value !== s.key && card(s)?.slug ? { kind: 'task', id: card(s).slug } : null)
const set = (key, patch) => p.save((list) => list.map((s) => (s.key === key ? { ...s, ...patch } : s)))
const drop = (key) => p.save((list) => list.filter((s) => s.key !== key))
const named = (label) => { draft.value.label = label }
async function add(value) {
  const d = draft.value
  await p.save((list) => [...list, { key: d.own ? d.label : d.key, label: d.label, value, unit: d.unit }])
  draft.value = null
}
</script>

<template>
  <div class="stats" :class="{ pills }">
    <div v-for="s in stats" :key="s.key" v-peek="peek(s)" class="stat" :title="card(s) || free ? null : 'свій параметр'">
      <span class="name">{{ sign(s) }}<template v-if="card(s)">{{ s.label || s.key }}</template>
        <InlineText v-else :value="s.label || s.key" :can required placeholder="назва" :save="(label) => set(s.key, { key: label, label })" /></span>
      <span class="val"><InlineText :value="String(s.value)" :can required class="v" :save="(value) => set(s.key, { value })"
                                    @update:open="(o) => (writing = o ? s.key : '')" /><span v-if="card(s)?.unit" class="unit">{{ s.unit }}</span>
        <InlineText v-else-if="s.unit || tools" :value="s.unit || ''" :can class="unit" placeholder="од." :save="(unit) => set(s.key, { unit })">
          <template #empty><span class="more-field" title="одиниця виміру: шт., с, клітинок за тік…"><Icon name="plus" /> од.</span></template>
        </InlineText>{{ ' ' }}<JudgeMark :claim="claimOf(s)" /></span>
      <Transition name="tool">
        <button v-if="tools" type="button" class="iact del mini" :title="`Прибрати «${s.label || s.key}»`" @click="drop(s.key)"><Icon name="minus" /></button>
      </Transition>
    </div>
    <div v-if="draft" class="stat">
      <span class="name">{{ sign(draft) }}<template v-if="!draft.own">{{ draft.label }}</template>
        <InlineText v-else :value="draft.label" can fresh required placeholder="назва параметра" :save="named" @drop="draft.label || (draft = null)" /></span>
      <span v-if="draft.label" class="val"><InlineText value="" can fresh required class="v" placeholder="значення" :save="add" @drop="draft = null" /><span
        v-if="draft.unit" class="unit">{{ draft.unit }}</span></span>
    </div>
  </div>
</template>

<style scoped>
.stats { display: grid; grid-template-columns: repeat(auto-fill, minmax(10.5rem, 1fr)); column-gap: 1.25rem; font-size: .8rem; }
/* a long value («≤ 4 (20 на рівень) шт.») wraps under itself instead of squeezing the name into a column of letters */
.stat { display: flex; flex-wrap: wrap; justify-content: space-between; align-items: baseline; gap: 0 .5rem; padding: .1rem 0; border-bottom: 1px dotted var(--bs-border-color); }
.name { color: var(--bs-secondary-color); }
.val { margin-left: auto; text-align: end; }
.v { font-weight: 600; font-variant-numeric: tabular-nums; }
.unit { margin-left: .35em; color: var(--bs-secondary-color); }
.mini { align-self: center; }
/* a level's: pills in a row, as they always were */
.pills { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem; font-size: .75rem; }
.pills .stat { flex-wrap: nowrap; gap: 0 .3rem; padding: .1rem .5rem; border: 1px solid var(--bs-border-color); border-radius: 1rem; background: var(--bs-tertiary-bg); }
.pills .name { color: inherit; }
.pills .val { margin: 0; }
.pills .v { font-weight: 400; }
.pills .unit { opacity: .75; }
</style>
