<script setup>
import { computed, nextTick, reactive, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump, target } from '../jump.js'
import { RULE_GROUP_ORDER, ruleGroup } from '../rules.js'
import { isContact } from '../ruleViews.js'
import PhasesStrip from './PhasesStrip.vue'
import RuleForm from './RuleForm.vue'
import RuleGroup from './RuleGroup.vue'
import RulesControls from './RulesControls.vue'
import RulesMatrix from './RulesMatrix.vue'
import RulesSwitch from './RulesSwitch.vue'
import RulesTime from './RulesTime.vue'

// the body of «Правила» (T270 §4.2, T274 §6): the tick's order, then the rules grouped by what starts them — or one of the
// tables: contacts, controls, time. add(prefill?) opens the new rule's form: prefill = { when?, cond?, then?, card? }
const ed = useEd()
const view = ref('list')
const folded = reactive({})  // group → folded
const adding = ref(null)  // the new rule's prefill while its form is open
const opened = ref(0)  // every add() starts a fresh form
const contacts = computed(() => ed.rules.filter(isContact))
const grouped = computed(() => {
  const m = {}
  for (const r of ed.rules) (m[ruleGroup(r)] ??= []).push(r)
  return [...new Set([...RULE_GROUP_ORDER, ...Object.keys(m)])].filter((g) => m[g]).map((g) => ({ g, list: m[g] }))
})
const firstWord = (g) => Object.keys(vocab.value.triggers).find((k) => vocab.value.triggers[k].group === g)

async function add(prefill) {
  adding.value = prefill || {}
  opened.value++
  await nextTick()
  document.getElementById('rule-new')?.scrollIntoView({ block: 'center', behavior: 'smooth' })
}
defineExpose({ add })
function show(id) {
  view.value = 'list'
  jump(`r-${id}`)
}
// «show me where» lands on a rule here or on a card claimed on one: back to the list, the rule's group open
watch(target, (id) => {
  const claim = ed.claims.find((c) => `c-${c.id}` === id)
  const rule = ed.rules.find((r) => `r-${r.id}` === id || r.id === claim?.rule)
  if (!rule) return
  view.value = 'list'
  folded[ruleGroup(rule)] = false
})
</script>

<template>
  <div>
    <PhasesStrip class="mb-3" />
    <RulesSwitch v-model="view" class="mb-2" />
    <RulesMatrix v-if="view === 'contacts'" :rules="contacts" @show="show" @add="add" />
    <RulesControls v-else-if="view === 'controls'" @show="show" @add="add" />
    <RulesTime v-else-if="view === 'time'" @show="show" @add="add" />
    <div v-else class="vstack gap-2">
      <RuleGroup v-for="{ g, list } in grouped" :key="g" v-model:folded="folded[g]" :name="g" :rules="list"
                 @add="add({ when: { kind: firstWord(g) } })" />
    </div>
    <div v-if="adding" id="rule-new" class="new mt-2">
      <RuleForm :key="opened" :rule="null" :prefill="adding" @saved="adding = null" @cancel="adding = null" />
    </div>
    <template v-else>
      <p v-if="!ed.rules.length && ed.editable" class="small text-secondary mb-0">
        Правило — речення з трьох частин: <b class="kw-when">КОЛИ</b> щось сталося, <b class="kw-if">ЯКЩО</b> виконано умову (можна без неї),
        <b class="kw-then">ТО</b> ось що відбувається. Наприклад: «<b class="kw-when">КОЛИ</b> куля × танк <b class="kw-then">ТО</b> танк отримує шкоду 1»
        або «<b class="kw-when">КОЛИ</b> кожні 20 тіків <b class="kw-if">ЯКЩО</b> ворогів на полі &lt; 4 <b class="kw-then">ТО</b> зʼявляється ворог».
      </p>
      <p v-else-if="!ed.rules.length" class="small text-secondary mb-0">Правил поки нема.</p>
      <!-- «Керування» and «Час» have a plus of their own under the table -->
      <button v-if="ed.editable && (view === 'list' || view === 'contacts')" type="button" class="btn btn-sm btn-add mt-2" @click="add()">
        <Icon name="plus" /> правило
      </button>
    </template>
  </div>
</template>

<style scoped>
.new { padding: .5rem; border: 1px solid var(--bs-border-color); border-radius: .375rem; background: var(--bs-tertiary-bg); scroll-margin-top: 1rem; }
.kw-when { color: var(--kw-when); }
.kw-if { color: var(--kw-if); }
.kw-then { color: var(--kw-then); }
</style>
