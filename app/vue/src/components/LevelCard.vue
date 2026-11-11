<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deletePart } from '../api.js'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import LevelForm from './LevelForm.vue'
import PartLabel from './PartLabel.vue'
import PropsList from './PropsList.vue'
import ShotStrip from './ShotStrip.vue'

// one level or a group of alike ones (T270 §9): where it comes from and how many, its size, the field's properties it
// overrides, its parameters, screenshots and cards; the pencil turns the card into its form in place
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
  <div :id="'p-' + part.id" class="card">
    <div class="card-body p-2 vstack gap-2">
      <LevelForm v-if="edit" :part @done="edit = false" @cancel="edit = false" />
      <template v-else>
        <div class="d-flex align-items-center gap-2">
          <span>🪜</span>
          <span class="fw-semibold">{{ part.title }}</span>
          <span class="text-secondary small">{{ mode }}<template v-if="values.count"> {{ /^\d+$/.test(values.count) ? '×' : '·' }} {{ values.count }}</template></span>
          <span v-if="ed.editable" class="d-flex ms-auto">
            <button type="button" class="iact" title="Редагувати" @click="edit = true"><Icon name="pencil" /></button>
            <DelButton :what="`рівень «${part.title}»`" note="разом зі скриншотами й картками рівня" @yes="remove" />
          </span>
        </div>
        <PropsList :props="values" :specs />
        <div v-if="part.stats?.length" class="d-flex flex-wrap align-items-center gap-1 small">
          <PartLabel icon="🔢" zone="levels" class="me-1">Параметри</PartLabel>
          <span v-for="s in part.stats" :key="s.key" class="badge rounded-pill fw-normal stat">
            {{ s.label || s.key }} {{ s.value }} <span v-if="s.unit" class="opacity-75">{{ s.unit }}</span>
          </span>
        </div>
        <div v-if="part.description" class="small">{{ part.description }}</div>
        <ShotStrip v-if="ed.editable || part.screenshots?.length" :part />
        <div v-if="claims.length || ed.editable" class="vstack gap-1">
          <PartLabel icon="🃏" zone="levels">Картки рівня</PartLabel>
          <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
          <div v-if="ed.editable"><CardPicker :kinds="['level']" :anchor="{ part: part.id }" label="картка" /></div>
        </div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.stat { background: var(--bs-tertiary-bg); color: var(--bs-body-color); border: 1px solid var(--bs-border-color); }
</style>
