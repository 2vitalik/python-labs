<script setup>
import { computed, ref, watch } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deletePart } from '../api.js'
import { vocab, zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { target } from '../jump.js'
import { isShut, toggleCard } from '../looks.js'
import CardFold from './CardFold.vue'
import CardPicker from './CardPicker.vue'
import CardShut from './CardShut.vue'
import ClaimRow from './ClaimRow.vue'
import LevelForm from './LevelForm.vue'
import MomentField from './MomentField.vue'
import PartBlock from './PartBlock.vue'
import PropsList from './PropsList.vue'
import ShotStrip from './ShotStrip.vue'
import '../partCard.css'

// one level or a group of alike ones (T270 §9): where it comes from and how many, its size, the field's properties it
// overrides, its parameters, its map drawn in cells (T276), screenshots and cards; the head is tinted and sticks while the
// card passes (partCard.css); the pencil turns the head and the top of the card into its form in place, framed alone
// (T294 §4) — the level's cards stay under the form, each with its trash (T284 §4). Folded (T296 §7) — the head, two lines
// and what is inside
const p = defineProps({ part: Object })
const ed = useEd()
const edit = ref(false)
const values = computed(() => p.part.props || {})
const mode = computed(() => {
  const o = vocab.value.level.find((s) => s.key === 'mode')?.options?.[values.value.mode]
  return typeof o === 'string' ? o : o?.label || values.value.mode || ''
})
// the level's own size, then whatever of the field it changes
const specs = computed(() => [...vocab.value.level.filter((s) => s.key === 'size'), ...vocab.value.field.filter((s) => s.key !== 'size')])
const claims = computed(() => ed.claimsOf(p.part.id).filter((c) => !c.auto))
const shut = computed(() => !edit.value && isShut(p.part.id, 'levels'))
// «show me where» a claim of this card is: a folded card opens to show it
watch(target, (id) => id && shut.value && claims.value.some((c) => `c-${c.id}` === id) && toggleCard(p.part.id, 'levels'))
const bits = computed(() => [['gauge', p.part.stats?.length, 'параметри'], ['grid', values.value.map ? 1 : 0, 'карта рівня'],
  ['image', p.part.screenshots?.length, 'скриншоти'], ['card', claims.value.length, 'картки рівня']])

async function remove() {
  try {
    await deletePart(p.part.id)
    await ed.changed()
  } catch (e) {
    ed.fail(e.message)
  }
}
</script>

<template>
  <div :id="'p-' + part.id" class="card pcard" :style="{ '--z': zones.levels?.color }">
    <div v-if="!edit" class="pcard-head">
      <span>🪜</span>
      <span class="fw-semibold">{{ part.title }}</span>
      <span class="text-secondary small">{{ mode }}<template v-if="values.count">{{ ` ${/^\d+$/.test(values.count) ? '×' : '·'} ${values.count}` }}</template></span>
      <span class="pcard-acts">
        <CardFold :id="part.id" scope="levels" />
        <template v-if="ed.editable">
          <button type="button" class="iact" title="Редагувати" @click="edit = true"><Icon name="pencil" /></button>
          <DelButton :what="`рівень «${part.title}»`" note="разом зі скриншотами й картками рівня" @yes="remove" />
        </template>
      </span>
    </div>
    <div v-if="shut" class="card-body"><CardShut :text="part.description" :bits @open="toggleCard(part.id, 'levels', $event)" /></div>
    <div v-else class="card-body vstack gap-2">
      <div v-if="edit" class="editing pform"><LevelForm :part @done="edit = false" @cancel="edit = false" /></div>
      <template v-else>
        <PropsList :props="values" :specs />
        <PartBlock v-if="part.stats?.length" pic="gauge" zone="levels" title="Параметри" inline class="small">
          <span class="d-flex flex-wrap gap-1">
            <span v-for="s in part.stats" :key="s.key" class="badge rounded-pill fw-normal stat">
              {{ s.label || s.key }} {{ s.value }} <span v-if="s.unit" class="opacity-75">{{ s.unit }}</span>
            </span>
          </span>
        </PartBlock>
        <div v-if="part.description" class="small">{{ part.description }}</div>
        <MomentField v-if="values.map" :text="values.map" />
        <ShotStrip v-if="ed.editable || part.screenshots?.length" :part />
      </template>
      <PartBlock v-if="claims.length || ed.editable" pic="card" zone="levels" title="Картки рівня">
        <template #after><CardPicker plus :kinds="['level']" :anchor="{ part: part.id }" label="картка рівня" /></template>
        <div v-if="claims.length" class="vstack gap-1">
          <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
        </div>
      </PartBlock>
    </div>
  </div>
</template>

<style scoped>
.stat { background: var(--bs-tertiary-bg); color: var(--bs-body-color); border: 1px solid var(--bs-border-color); }
</style>
