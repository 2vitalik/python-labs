<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { deletePart } from '../api.js'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import FieldForm from './FieldForm.vue'
import PartBlock from './PartBlock.vue'
import PropsList from './PropsList.vue'
import ShotStrip from './ShotStrip.vue'

// the «Поле» section's body (T270 §8): the field's properties to read, its screenshots and the cards about it;
// the pencil turns the card into its form in place, framed alone (T294 §4): the cards about the field stay under it
const ed = useEd()
const edit = ref(false)
const claims = computed(() => (ed.field ? ed.claimsOf(ed.field.id).filter((c) => !c.auto) : []))

async function remove() {
  try {
    await deletePart(ed.field.id)
    await ed.changed()
  } catch (e) {
    ed.fail(e.message)
  }
}
defineExpose({ add: () => (edit.value = true) })
</script>

<template>
  <div :id="ed.field ? `p-${ed.field.id}` : null" class="card">
    <div class="card-body p-2 vstack gap-2">
      <div v-if="edit" class="editing form-box" :class="{ new: !ed.field }"><FieldForm :part="ed.field" @done="edit = false" @cancel="edit = false" /></div>
      <template v-else-if="!ed.field">
        <Tip>Поле — де йде гра: яка сітка, як на неї дивимось, як іде час (покроково чи в реальному часі),
          як керує гравець і що може лежати в одній клітині.</Tip>
        <button v-if="ed.editable" type="button" class="btn btn-sm btn-add align-self-start" @click="edit = true"><Icon name="plus" /> Описати поле</button>
      </template>
      <template v-else>
        <div class="d-flex align-items-start gap-2">
          <PropsList :props="ed.field.props" :specs="vocab.field" class="flex-grow-1">
            <span class="text-secondary">Властивості поля ще не вказані.</span>
          </PropsList>
          <span v-if="ed.editable" class="d-flex ms-auto">
            <button type="button" class="iact" title="Редагувати" @click="edit = true"><Icon name="pencil" /></button>
            <DelButton what="опис поля" note="разом зі скриншотами й картками про поле" @yes="remove" />
          </span>
        </div>
        <div v-if="ed.field.description" class="small">{{ ed.field.description }}</div>
        <ShotStrip v-if="ed.editable || ed.field.screenshots?.length" :part="ed.field" />
      </template>
      <PartBlock v-if="ed.field && (claims.length || ed.editable)" pic="card" zone="field" title="Картки про поле">
        <template #after><CardPicker plus :kinds="['field']" :anchor="{ part: ed.field.id }" label="картка про поле" /></template>
        <div v-if="claims.length" class="vstack gap-1">
          <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
        </div>
      </PartBlock>
    </div>
  </div>
</template>

<style scoped>
.form-box { padding: .45rem; }
</style>
