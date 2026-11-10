<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deleteRule } from '../api.js'
import { useEd } from '../ed.js'
import ClaimRow from './ClaimRow.vue'
import RuleForm from './RuleForm.vue'
import RuleText from './RuleText.vue'

// one rule of «Правила»: the sentence and the cards claimed on it; the pencil turns the sentence into the form in place
const props = defineProps({ rule: Object })
const ed = useEd()
const edit = ref(false)
const claims = computed(() => ed.ruleClaims(props.rule.id))
const note = computed(() => {
  const n = claims.value.length
  return n > 1 ? 'разом із картками на ньому' : n ? 'разом із карткою на ньому' : ''
})
async function remove() {
  try {
    await deleteRule(props.rule.id)
    ed.changed()
  } catch (e) {
    ed.fail(e.message)
  }
}
</script>

<template>
  <div :id="`r-${rule.id}`" class="rule-row" :class="{ editing: edit }">
    <RuleForm v-if="edit" :rule @saved="edit = false" @cancel="edit = false" />
    <div v-else class="d-flex align-items-start gap-1">
      <RuleText :rule :parts="ed.parts" class="text" />
      <template v-if="ed.editable">
        <button type="button" class="iact" title="Редагувати правило" @click="edit = true"><Icon name="pencil" /></button>
        <DelButton what="правило" :note @yes="remove" />
      </template>
    </div>
    <div v-if="claims.length" class="claims">
      <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
    </div>
  </div>
</template>

<style scoped>
.rule-row { padding: .3rem .4rem .3rem .5rem; border: 1px solid var(--bs-border-color); border-radius: .375rem; background: var(--bs-body-bg); }
.rule-row.editing { padding: .5rem; background: var(--bs-tertiary-bg); }
.text { flex: 1 1 auto; min-width: 0; }
.claims { margin-top: .3rem; padding-top: .3rem; border-top: 1px dashed var(--bs-border-color); }
</style>
