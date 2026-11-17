<script setup>
import { nextTick, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import { renameState } from '../api.js'
import { useEd } from '../ed.js'

// an entity's states, a pill each (T344). With `can` a click on a pill renames the state right in it — on the card and in
// every rule that names it (my_states.py); «Повернути» takes both back. With `tools` (the card's pencil) every pill has its
// minus, and «＋ стан» is a pill being typed: Enter makes it one and opens the next, a comma adds several at once.
// A state taken away stays as a word in its rules, underlined there as unknown
const props = defineProps({ part: Object, can: Boolean, tools: Boolean })
const ed = useEd()
const adding = ref(false)
let again = false  // Enter goes on to the next pill; a click elsewhere just adds
const set = (list) => ed.save.part(props.part.id, { states: list })

async function rename(i, name) {
  const id = props.part.id, old = props.part.states[i]
  const { part, rules } = await renameState(id, old, name)
  await ed.changed()
  const now = part.states[i]
  ed.last = { what: `стан «${old}» → «${now}»${rules ? ` — і в правилах (${rules})` : ''}`,
    undo: async () => { await renameState(id, now, old); await ed.changed(); ed.last = null } }
}
async function add(line) {
  await set([...(props.part.states || []), ...line.split(',').map((s) => s.trim()).filter(Boolean)])
  adding.value = false
  if (!again) return
  again = false
  await nextTick()
  adding.value = true
}
const start = (on) => { again = false; adding.value = on }
</script>

<template>
  <span class="chips">
    <span v-for="(st, i) in part.states" :key="i" class="state" :class="{ can }">
      <InlineText :value="st" :can required placeholder="стан" :save="(name) => rename(i, name)" />
      <Transition name="tool">
        <button v-if="tools" type="button" class="iact del mini" :title="`Прибрати стан «${st}»`" @click="set(part.states.filter((_, k) => k !== i))"><Icon name="minus" /></button>
      </Transition>
    </span>
    <span v-if="adding" class="state draft" @keydown.enter.capture="again = true">
      <InlineText value="" can fresh required placeholder="новий стан" :save="add" @drop="start(false)" />
    </span>
    <Transition v-else name="tool">
      <button v-if="tools" type="button" class="more-field" title="Enter — ще один, кома — кілька одразу" @click="start(true)">＋ стан</button>
    </Transition>
  </span>
</template>

<style scoped>
.chips { display: inline-flex; flex-wrap: wrap; align-items: center; gap: .25rem; }
.state { display: inline-flex; align-items: center; gap: .1rem; padding: 0 .45rem; border: 1px solid var(--bs-info-border-subtle); border-radius: 1rem;
         background: color-mix(in srgb, var(--bs-info) 14%, var(--bs-body-bg)); font-size: .76rem; }
.state.can:hover { border-color: var(--bs-info); }
.state.draft { border-style: dashed; }
/* the pill itself is the field: the value's own ground and frame (InlineText) would stick out of its round ends */
.state :deep(.inl.can) { background: none !important; box-shadow: none !important; }
.state :deep(.inl-f) { background: none; box-shadow: none; }
.state:has(.inl.open) { border-color: var(--bs-primary-border-subtle); background: var(--bs-body-bg); box-shadow: 0 0 0 .2rem color-mix(in srgb, var(--bs-primary) 16%, transparent); }
.state .mini { margin-right: -.3rem; }
</style>
