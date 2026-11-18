<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { statItems } from '../items.js'
import Picker from '@core/components/Picker.vue'
import ProposeCard from './ProposeCard.vue'

// «＋ параметр» of a card with its tools on (T310) — a violet «＋» by the caption «Параметри» (T350): the catalog's stats
// to pick from, each with its line, the ones the card has ticked; «свій параметр» — a name of the student's own; none
// fits — the idea goes to the teacher and the stat is the student's own meanwhile. Emits pick({ key, label, unit, own }) —
// the list gives it a row with the value open (StatList.begin). `free` — no catalog (a level's): the «＋» asks for an own name at once
const p = defineProps({ taken: { type: Array, default: () => [] }, free: Boolean })
const emit = defineEmits(['pick'])
const open = ref(false)
const proposing = ref(false)
watch(open, () => (proposing.value = false))
const items = computed(() => (open.value ? statItems(new Set(p.taken)) : []))
function own(label = '') {
  open.value = false
  emit('pick', { key: '', label, unit: '', own: true })
}
function pick(it) {
  open.value = false
  if (!it.taken) emit('pick', { key: it.key, label: it.title, unit: it.stat.unit || '', own: false })
}
</script>

<template>
  <button v-if="free" type="button" class="iact add qtip" data-tip="＋ параметр" aria-label="додати параметр" @click="own()"><Icon name="plus" /></button>
  <Pop v-else v-model="open" width="22rem">
    <template #trigger="{ toggle }">
      <button type="button" class="iact add qtip" data-tip="＋ параметр" aria-label="додати параметр" @click="toggle"><Icon name="plus" /></button>
    </template>
    <ProposeCard v-if="proposing" what="новий параметр" all-to="/tasks?zone=entities&sub=params" zone="entities" subzone="params"
                 @done="own" @cancel="proposing = false" />
    <Picker v-else inline autofocus :items placeholder="HP, швидкість, шкода…" @pick="pick">
      <template #footer>
        <div class="foot">
          <button type="button" class="more-field" @click="own()"><Icon name="plus" /> свій параметр</button>
          <a href="#" @click.prevent="proposing = true">запропонувати в каталог</a>
        </div>
      </template>
    </Picker>
  </Pop>
</template>

<style scoped>
.foot { display: flex; align-items: center; gap: .5rem; margin: .4rem .5rem .1rem; padding-top: .4rem; border-top: 1px solid var(--bs-border-color-translucent); font-size: .78rem; }
.foot a { margin-left: auto; color: var(--bs-secondary-color); }
</style>
