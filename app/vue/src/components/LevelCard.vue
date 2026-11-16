<script setup>
import { computed, ref, watch } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import InlinePop from '@core/components/InlinePop.vue'
import InlineText from '@core/components/InlineText.vue'
import { vToStart } from '@core/toStart.js'
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
import OptionCards from './OptionCards.vue'
import PartBlock from './PartBlock.vue'
import PropsList from './PropsList.vue'
import ShotStrip from './ShotStrip.vue'
import '../partCard.css'

// one level or a group of alike ones (T270 §9): where it comes from and how many, its size, the field's properties it
// overrides, its parameters, its map drawn in cells (T276), screenshots and cards; the head is tinted and sticks while the
// card passes (partCard.css). The owner changes the name, where it comes from, how many, the size and the properties, a
// parameter's value and the description where they read (T306); the pencil turns the head and the top of the card into its
// form in place, framed alone (T294 §4) — all at once, and what is not there yet; the level's cards stay under the form,
// each with its trash (T284 §4). Folded (T296 §7) — the head, two lines and what is inside
const p = defineProps({ part: Object })
const ed = useEd()
const edit = ref(false)
const values = computed(() => p.part.props || {})
const modeSpec = computed(() => vocab.value.level.find((s) => s.key === 'mode'))
const mode = computed(() => {
  const o = modeSpec.value?.options?.[values.value.mode]
  return typeof o === 'string' ? o : o?.label || values.value.mode || ''
})
// the level's own size, then whatever of the field it changes
const specs = computed(() => [...vocab.value.level.filter((s) => s.key === 'size'), ...vocab.value.field.filter((s) => s.key !== 'size')])
const claims = computed(() => ed.claimsOf(p.part.id).filter((c) => !c.auto))
const shut = computed(() => !edit.value && isShut(p.part.id, 'levels'))
// «show me where» a claim of this card is: a folded card opens to show it
watch(target, (id) => id && shut.value && claims.value.some((c) => `c-${c.id}` === id) && toggleCard(p.part.id, 'levels'))
const bits = computed(() => [['stats', p.part.stats?.length, 'параметри'], ['grid', values.value.map ? 1 : 0, 'карта рівня'],
  ['image', p.part.screenshots?.length, 'скриншоти'], ['card', claims.value.length, 'картки рівня']])
const save = (patch) => ed.save.part(p.part.id, patch)
const setProp = (key, v) => save((now) => ({ props: { ...now.props, [key]: v } }))
const setStat = (key, value) => save((now) => ({ stats: now.stats.map((s) => (s.key === key ? { ...s, value } : s)) }))

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
    <div v-if="!edit" v-to-start="'картки'" class="pcard-head">
      <span>🪜</span>
      <InlineText :value="part.title" :can="ed.editable" required placeholder="Назва рівня" class="fw-semibold" :save="(title) => save({ title })" />
      <span class="text-secondary small">
        <InlinePop v-if="mode" :can="ed.editable" width="15rem" tip="Клік — звідки інакше">
          {{ mode }}
          <template #panel="{ choose }">
            <OptionCards :model-value="values.mode" :options="modeSpec.options" compact @update:model-value="(m) => choose(setProp('mode', m))" />
          </template>
        </InlinePop>
        <template v-if="values.count">{{ ` ${/^\d+$/.test(values.count) ? '×' : '·'} ` }}<InlineText :value="String(values.count)" :can="ed.editable"
          placeholder="скільки таких" :save="(c) => setProp('count', c)" /></template>
      </span>
      <span class="pcard-acts">
        <CardFold :id="part.id" scope="levels" />
        <template v-if="ed.editable">
          <button type="button" class="iact" title="Редагувати все разом" @click="edit = true"><Icon name="pencil" /></button>
          <DelButton :what="`рівень «${part.title}»`" note="разом зі скриншотами й картками рівня" @yes="remove" />
        </template>
      </span>
    </div>
    <div v-if="shut" class="card-body"><CardShut :text="part.description" :bits @open="toggleCard(part.id, 'levels', $event)" /></div>
    <div v-else class="card-body vstack gap-2">
      <div v-if="edit" class="editing pform"><LevelForm :part @done="edit = false" @cancel="edit = false" /></div>
      <template v-else>
        <PropsList :props="values" :specs :can="ed.editable" :save="setProp" />
        <PartBlock v-if="part.stats?.length" pic="stats" zone="levels" title="Параметри" inline class="small">
          <span class="d-flex flex-wrap gap-1">
            <span v-for="s in part.stats" :key="s.key" class="badge rounded-pill fw-normal stat">
              {{ s.label || s.key }} <InlineText :value="String(s.value)" :can="ed.editable" required :save="(v) => setStat(s.key, v)" />
              <span v-if="s.unit" class="opacity-75">{{ s.unit }}</span>
            </span>
          </span>
        </PartBlock>
        <InlineText v-if="part.description || ed.editable" :value="part.description" multi block :can="ed.editable" class="small"
                    placeholder="Коротко: що тут відбувається, чим рівень особливий…" :save="(description) => save({ description })">
          <template #empty><span class="more-field">＋ опис</span></template>
        </InlineText>
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
