<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import EntityCard from './EntityCard.vue'
import EntityForm from './EntityForm.vue'
import StableColumns from './StableColumns.vue'

// the body of «Сутності» (T270 §7): a new entity's form on top, the cards in two stable columns, one toggle for all their
// rule lists. add(prefill?) opens the form, the type (and the name) already chosen: { role?, title? }
const ed = useEd()
const adding = ref(null)  // the new form's prefill; null — no form
const formKey = ref(0)
function add(prefill = {}) {
  adding.value = { ...prefill }
  formKey.value++
}
defineExpose({ add })
function created(part) {
  adding.value = null
  if (part?.id) jump(`p-${part.id}`)
}
</script>

<template>
  <div>
    <div v-if="!ed.simple && ed.entities.length" class="d-flex justify-content-end mb-1">
      <button type="button" class="toggle" @click="ed.showRules = !ed.showRules">
        <Icon :name="ed.showRules ? 'fold' : 'unfold'" /> {{ ed.showRules ? 'згорнути правила' : 'розгорнути правила' }}
      </button>
    </div>
    <div v-if="ed.editable && adding" class="card mb-2 editing new">
      <div class="card-body p-2">
        <EntityForm :key="formKey" :prefill="adding" @done="created" @cancel="adding = null" />
      </div>
    </div>
    <StableColumns v-if="ed.entities.length" v-slot="{ item }" :items="ed.entities" scope="entities">
      <EntityCard :part="item" />
    </StableColumns>
    <Tip v-else-if="!adding">
      <div>Мешканці поля: гравець, вороги, предмети, стіни, підлога.</div>
      <div v-if="ed.simple">У кожної — тип, короткий опис і скриншот.</div>
      <div v-else>У кожної — тип, параметри, стани, механіки й правила.</div>
    </Tip>
  </div>
</template>

<style scoped>
.toggle { display: inline-flex; align-items: center; gap: .25rem; padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .78rem; }
.toggle:hover { color: var(--bs-body-color); }
</style>
