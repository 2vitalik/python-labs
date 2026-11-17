<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import Tip from '@core/components/Tip.vue'
import { deletePart, postPart } from '../api.js'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { setTools, toolsOn } from '../tools.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import PartBlock from './PartBlock.vue'
import PropsList from './PropsList.vue'
import ShotStrip from './ShotStrip.vue'
import ToolsButton from './ToolsButton.vue'
import '../partCard.css'

// the «Поле» section's body (T270 §8): the field's properties to read, its screenshots and the cards about it. The owner
// changes a property and the description where they read (T306). The pencil opens no form (T310): it turns the tools on —
// every property stands there, the unset ones too, each a click away. «Описати поле» makes the field at once, its tools on
const ed = useEd()
const busy = ref(false)
const tools = computed(() => ed.editable && !!ed.field && toolsOn(ed.field.id))
const claims = computed(() => (ed.field ? ed.claimsOf(ed.field.id).filter((c) => !c.auto) : []))
const save = (patch) => ed.save.part(ed.field.id, patch)
const setProp = (key, v) => save((now) => ({ props: { ...now.props, [key]: v } }))

async function run(fn) {
  busy.value = true
  try {
    await fn()
  } catch (e) {
    ed.fail(e.message)
  } finally {
    busy.value = false
  }
}
const add = () => !ed.field && !busy.value && run(async () => {
  const made = await postPart({ kind: 'field', title: 'Поле', props: {} })
  await ed.changed()
  setTools(made.id, true)
})
const remove = () => run(async () => {
  await deletePart(ed.field.id)
  await ed.changed()
})
defineExpose({ add })
</script>

<template>
  <div :id="ed.field ? `p-${ed.field.id}` : null" class="card" :class="{ 'tools-on': tools }">
    <div class="card-body p-2 vstack gap-2">
      <template v-if="!ed.field">
        <Tip>Поле — де йде гра: яка сітка, як на неї дивимось, як іде час (покроково чи в реальному часі),
          як керує гравець і що може лежати в одній клітині.</Tip>
        <button v-if="ed.editable" type="button" class="btn btn-sm btn-add align-self-start" :disabled="busy" @click="add"><Icon name="plus" /> Описати поле</button>
      </template>
      <template v-else>
        <div class="d-flex align-items-start gap-2">
          <PropsList :props="ed.field.props" :specs="vocab.field" class="flex-grow-1" :can="ed.editable" :save="setProp" :all="tools">
            <span class="text-secondary">Властивості поля ще не вказані.</span>
          </PropsList>
          <span v-if="ed.editable" class="d-flex ms-auto">
            <ToolsButton :id="ed.field.id" what="полі — і ще не вказане" />
            <DelButton what="опис поля" note="разом зі скриншотами й картками про поле" @yes="remove" />
          </span>
        </div>
        <InlineText v-if="ed.field.description || ed.editable" :value="ed.field.description" multi block :can="ed.editable" class="small"
                    placeholder="Коротко про поле: як генерується, камера…" :save="(description) => save({ description })">
          <template #empty><span class="more-field">＋ опис</span></template>
        </InlineText>
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
