<script setup>
import Icon from '@core/components/Icon.vue'
import { useEd } from '../ed.js'
import RuleRow from './RuleRow.vue'
import StableColumns from './StableColumns.vue'

// one group of rules by what starts them: a header in the group's colour with the count — a click folds it — and the rules
// in steady columns; the header's plus starts a new rule of this group. The header sticks under the section's heading
// while its rules pass (T294 §17): «where am I» and its «＋» stay at hand
defineProps({ name: String, rules: Array })
defineEmits(['add'])
const folded = defineModel('folded', { type: Boolean, default: false })
const ed = useEd()
// calm hues, one per group (rules.js: RULE_GROUP_ORDER); the text mixes them with the page's own colour, so both themes read
const COLORS = { контакт: '#d9603b', 'ввід і час': '#3b82c4', 'стан і лічильники': '#2a9d8f', 'життєвий цикл': '#c2557a', пазли: '#b08a1e', інше: '#7a8594' }
// a group is «what starts the rule» — said in words next to its name
const WHEN = {
  контакт: 'коли сутності зіткнулись, стали поруч чи побачили одна одну', 'ввід і час': 'коли гравець щось зробив або минув час',
  'стан і лічильники': 'коли змінився стан чи число дійшло до межі', 'життєвий цикл': 'коли щось зʼявилось, зникло, почався чи скінчився рівень',
  пазли: 'коли виконано чи порушено умови розвʼязку', інше: 'подія, описана словами',
}
</script>

<template>
  <section class="rgroup" :style="{ '--g': COLORS[name] || COLORS.інше }">
    <div class="ghead">
      <button type="button" class="fold" :aria-expanded="!folded" :title="folded ? 'Розгорнути' : 'Згорнути'" @click="folded = !folded">
        <span class="gname">{{ name }}</span><span class="count">{{ rules.length }}</span><Icon :name="folded ? 'right' : 'down'" class="chev" />
        <span v-if="WHEN[name]" class="gwhen">{{ WHEN[name] }}</span>
      </button>
      <button v-if="ed.editable" type="button" class="iact add" :title="`Нове правило: ${name}`" @click="$emit('add')"><Icon name="plus" /></button>
    </div>
    <StableColumns v-if="!folded" v-slot="{ item }" :items="rules" scope="rules">
      <RuleRow :rule="item" />
    </StableColumns>
  </section>
</template>

<style scoped>
.ghead { position: sticky; z-index: 10; top: calc(var(--nav-h, 0px) + var(--stick-h, 0px)); display: flex; align-items: center; gap: .25rem;
         margin-bottom: .4rem; padding: .1rem .2rem .1rem .55rem; border-left: 3px solid var(--g); border-radius: .25rem;
         background: color-mix(in srgb, var(--g) 9%, var(--bs-body-bg)); }
.fold { display: inline-flex; flex-grow: 1; align-items: center; gap: .45rem; padding: .15rem 0; border: 0; background: none; color: inherit; text-align: start; }
.gname { font-size: .74rem; font-weight: 700; letter-spacing: .05em; text-transform: uppercase; color: color-mix(in srgb, var(--g) 78%, var(--bs-body-color)); }
.count { font-size: .75rem; color: var(--bs-secondary-color); font-variant-numeric: tabular-nums; }
.chev { color: var(--bs-secondary-color); }
.gwhen { font-size: .75rem; color: var(--bs-secondary-color); }
</style>
