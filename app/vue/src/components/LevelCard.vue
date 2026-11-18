<script setup>
import { computed, ref, watch } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import InlinePop from '@core/components/InlinePop.vue'
import InlineText from '@core/components/InlineText.vue'
import Reveal from '@core/components/Reveal.vue'
import { vToStart } from '@core/toStart.js'
import { deletePart } from '../api.js'
import { vocab, zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { target } from '@core/jump.js'
import { isShut, toggleCard } from '../looks.js'
import { toolsOn } from '../tools.js'
import CardFold from './CardFold.vue'
import CardPicker from './CardPicker.vue'
import CardShut from './CardShut.vue'
import ClaimRow from './ClaimRow.vue'
import LevelMap from './LevelMap.vue'
import OptionCards from './OptionCards.vue'
import PartBlock from './PartBlock.vue'
import PropsList from './PropsList.vue'
import ShotStrip from './ShotStrip.vue'
import StatAdd from './StatAdd.vue'
import StatList from './StatList.vue'
import ToolsButton from './ToolsButton.vue'
import '../partCard.css'

// one level or a group of alike ones (T270 §9): where it comes from and how many, its size, the field's properties it
// overrides, its parameters, its map drawn in cells (T276), screenshots and cards; the head is tinted and sticks while the
// card passes (partCard.css). The owner changes the name, where it comes from, how many, the size and the properties, a
// parameter and the description where they read (T306). The pencil opens no form (T310): it turns the card's tools on —
// what is not said yet (where from, how many, the size, the field's properties a level may change — «як у поля»),
// «＋ параметр» by the caption (T350), the map's editor — while the map is a feature on (T319). Folded (T296 §7) — the
// head, two lines and what is inside
const OVERRIDES = ['size', 'topology', 'view', 'time', 'control', 'gravity', 'wrap']  // what a level is offered to change
const p = defineProps({ part: Object })
const ed = useEd()
const tools = computed(() => ed.editable && toolsOn(p.part.id))
const values = computed(() => p.part.props || {})
const modeSpec = computed(() => vocab.value.level.find((s) => s.key === 'mode'))
const mode = computed(() => {
  const o = modeSpec.value?.options?.[values.value.mode]
  return typeof o === 'string' ? o : o?.label || values.value.mode || ''
})
// the level's own size, then whatever of the field it changes; with the tools — also what it may change and has not
const specs = computed(() => [...vocab.value.level.filter((s) => s.key === 'size'), ...vocab.value.field.filter((s) => s.key !== 'size')]
  .filter((s) => !tools.value || OVERRIDES.includes(s.key) || values.value[s.key] != null))
const claims = computed(() => ed.claimsOf(p.part.id).filter((c) => !c.auto))
const shut = computed(() => !tools.value && isShut(p.part.id, 'levels'))
// «show me where» a claim of this card is: a folded card opens to show it
watch(target, (id) => id && shut.value && claims.value.some((c) => `c-${c.id}` === id) && toggleCard(p.part.id, 'levels'))
const bits = computed(() => [['stats', p.part.stats?.length, 'параметри'], ['grid', values.value.map ? 1 : 0, 'карта рівня'],
  ['image', p.part.screenshots?.length, 'скриншоти'], ['card', claims.value.length, 'картки рівня']])
const save = (patch) => ed.save.part(p.part.id, patch)
const setProp = (key, v) => save((now) => ({ props: { ...now.props, [key]: v } }))
const setStats = (fn) => save((now) => ({ stats: fn(now.stats || []) }))
const statList = ref()

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
  <div :id="'p-' + part.id" class="card pcard" :class="{ 'tools-on': tools }" :style="{ '--z': zones.levels?.color }">
    <div v-to-start="'картки'" class="pcard-head">
      <span>🪜</span>
      <div class="pcard-names">
        <InlineText :value="part.title" :can="ed.editable" required placeholder="Назва рівня" class="fw-semibold" :save="(title) => save({ title })" />
        <span class="text-secondary small">
          <InlinePop v-if="mode || tools" :can="ed.editable" width="15rem" tip="Клік — звідки інакше">
            <template v-if="mode">{{ mode }}</template><span v-else class="inl-none">звідки береться?</span>
            <template #panel="{ choose }">
              <OptionCards :model-value="values.mode" :options="modeSpec.options" compact @update:model-value="(m) => choose(setProp('mode', m))" />
            </template>
          </InlinePop>
          <template v-if="values.count || tools">{{ ` ${/^\d+$/.test(values.count) ? '×' : '·'} ` }}<InlineText :value="String(values.count || '')" :can="ed.editable"
            placeholder="скільки таких: 12, без ліміту…" :save="(c) => setProp('count', c)"><template #empty><span class="inl-none">скільки?</span></template></InlineText></template>
        </span>
      </div>
      <span class="pcard-acts">
        <CardFold :id="part.id" scope="levels" />
        <template v-if="ed.editable">
          <ToolsButton :id="part.id" :all="ed.levels.map((l) => l.id)" />
          <DelButton :what="`рівень «${part.title}»`" note="разом зі скриншотами й картками рівня" @yes="remove" />
        </template>
      </span>
    </div>
    <div v-if="shut" class="card-body"><CardShut :text="part.description" :bits @open="toggleCard(part.id, 'levels', $event)" /></div>
    <div v-else class="card-body vstack gap-2">
      <PropsList :props="values" :specs :can="ed.editable" :save="setProp" :all="tools" inherit />
      <Reveal :show="!!part.stats?.length || tools" gap>
        <PartBlock pic="stats" zone="levels" title="Параметри" inline class="small">
          <template #after><Transition name="tool"><StatAdd v-if="tools" free @pick="statList.begin($event)" /></Transition></template>
          <StatList ref="statList" :stats="part.stats" :can="ed.editable" :tools free pills :save="setStats" />
        </PartBlock>
      </Reveal>
      <InlineText v-if="part.description || ed.editable" :value="part.description" multi block :can="ed.editable" class="small"
                  placeholder="Коротко: що тут відбувається, чим рівень особливий…" :save="(description) => save({ description })">
        <template #empty><span class="more-field"><Icon name="plus" /> опис</span></template>
      </InlineText>
      <LevelMap :text="values.map" :tools="ed.has('map') && (tools || (ed.editable && !values.map))" :save="(map) => setProp('map', map)" />
      <ShotStrip v-if="ed.editable || part.screenshots?.length" :part />
      <PartBlock v-if="claims.length || ed.editable" pic="card" zone="levels" title="Картки рівня">
        <template #after><CardPicker plus :kinds="['level']" :anchor="{ part: part.id }" label="картка рівня" /></template>
        <div v-if="claims.length" class="vstack gap-1">
          <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
        </div>
      </PartBlock>
    </div>
  </div>
</template>
