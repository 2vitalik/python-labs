<script setup>
import { computed, nextTick, ref, watch } from 'vue'

import { filterText } from '../tableFilter.js'
import { useTable } from '../tableCtx.js'
import { sortOf } from '../tableViews.js'
import Icon from './Icon.vue'
import Pop from './Pop.vue'
import SetupChip from './SetupChip.vue'
import SetupCols from './SetupCols.vue'
import SetupFilters from './SetupFilters.vue'
import SetupGroups from './SetupGroups.vue'
import SetupLab from './SetupLab.vue'
import SetupSort from './SetupSort.vue'

// the line that says how the view is set (T315 §2.4): Лаба · Колонки · Фільтри · Групи · Сортування. Each word shows what
// is set — grey while nothing is — and opens its small panel over the page. Which one is open is t.ui.panel: a column's
// header menu opens «Колонки» too. One line on a laptop, the words cut with «…»; a narrow window wraps them whole
const t = useTable()
const line = ref()
const pop = (name) => ({ modelValue: t.ui.panel === name, 'onUpdate:modelValue': (on) => turn(name, on) })
function turn(name, on) {
  if (on) t.ui.panel = name
  else if (t.ui.panel === name) t.ui.panel = ''
  if (!on && name === 'cols') t.ui.field = null
}
// opened from far down the table (a header's menu): the line comes into sight with its panel
watch(() => t.ui.panel, (p) => p && nextTick(() => {
  const top = line.value?.getBoundingClientRect().top
  if (top < 60 || top > innerHeight * 0.6) line.value.scrollIntoView({ block: 'start', behavior: 'smooth' })
}))
const sorts = computed(() => t.state.sort.map(sortOf).map((s) => ({ ...s, col: t.col(s.id) })).filter((s) => s.col))
const filterWords = computed(() => t.filters.map((f) => `${f.col.short} ${filterText(f.col, f.spec)}`))
const titles = computed(() => ({
  lab: `Колонки «цієї лаби» показують лабу ${t.state.lab} — клік: інша лаба`,
  cols: t.shown.map((c) => c.title).join('\n') || 'Колонок нема',
  filters: t.filters.map((f) => `${f.col.title}: ${filterText(f.col, f.spec)}`).join('\n') || 'Без фільтрів',
  groups: t.groupCols.map((c) => c.title).join(' › ') || 'Без груп',
  sort: sorts.value.map((s) => `${s.col.title} ${s.desc ? '↓' : '↑'}`).join('\n') || 'Як у списку: за групою й прізвищем',
}))
</script>

<template>
  <div ref="line" class="setup">
    <Pop v-if="t.usesLab" v-bind="pop('lab')" class="setup-item fixed" width="16rem">
      <template #trigger="{ toggle, open }">
        <SetupChip icon="flask" word="Лаба" set bare :open :title="titles.lab" @click="toggle">{{ t.state.lab }}</SetupChip>
      </template>
      <SetupLab @done="t.ui.panel = ''" />
    </Pop>
    <Pop v-bind="pop('cols')" class="setup-item fixed" width="47rem">
      <template #trigger="{ toggle, open }">
        <SetupChip icon="cols3" word="Колонки" :set="!!t.shown.length" bare :open :title="titles.cols" @click="toggle">{{ t.shown.length }}</SetupChip>
      </template>
      <SetupCols />
    </Pop>
    <Pop v-bind="pop('filters')" class="setup-item" width="28rem">
      <template #trigger="{ toggle, open }">
        <SetupChip icon="filter" word="Фільтри" :set="!!t.filters.length" :open :title="titles.filters" @click="toggle">
          {{ filterWords.slice(0, 3).join(' · ') }}<template v-if="filterWords.length > 3"> ＋{{ filterWords.length - 3 }}</template></SetupChip>
      </template>
      <SetupFilters />
    </Pop>
    <Pop v-bind="pop('groups')" class="setup-item" width="22rem">
      <template #trigger="{ toggle, open }">
        <SetupChip icon="layers" word="Групи" :set="!!t.groupCols.length" :open :title="titles.groups" @click="toggle">{{ t.groupCols.map((c) => c.short).join(' › ') }}</SetupChip>
      </template>
      <SetupGroups />
    </Pop>
    <Pop v-bind="pop('sort')" class="setup-item" width="25rem">
      <template #trigger="{ toggle, open }">
        <SetupChip icon="sort" word="Сортування" :set="!!sorts.length" :open :title="titles.sort" @click="toggle">
          <template v-for="(s, i) in sorts" :key="s.id">{{ i ? ' · ' : '' }}{{ s.col.short }} <Icon :name="s.desc ? 'down' : 'up'" /></template></SetupChip>
      </template>
      <SetupSort />
    </Pop>
  </div>
</template>

<style scoped>
.setup { display: flex; align-items: center; gap: .35rem; min-width: 0; margin-bottom: .5rem; }
/* a number says it all: those words keep their width, the long ones give theirs */
.setup-item { flex: 0 1 auto; min-width: 2.5rem; }
.setup-item.fixed { flex-shrink: 0; }
@media (max-width: 767px) { .setup { flex-wrap: wrap; } }
</style>
