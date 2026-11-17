<script setup>
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'

import { groupable } from '../table.js'
import { useTable } from '../tableCtx.js'
import { sortOf } from '../tableViews.js'
import FilterControl from './FilterControl.vue'
import Icon from './Icon.vue'

// a column's menu under its header (T315 §3): its full name; sort either way, or one more level of sort; group by it; its
// filter; «другорядна»; hide; an own column — its field. On the body and fixed to the header: the table scrolls and would
// clip it, so it follows the header as the page scrolls or the table changes; Esc or a press outside closes it
const props = defineProps({ c: { type: Object, required: true }, anchor: { type: Object, required: true } })
const emit = defineEmits(['close'])
const t = useTable()
const box = ref()
const at = ref({})
const error = ref('')
const id = props.c.id
const levels = computed(() => t.state.sort.map(sortOf))
const mine = computed(() => levels.value.find((l) => l.id === id))
const grouped = computed(() => t.state.group.includes(id))
const canGroup = groupable(props.c)

function sort(desc) {
  if (mine.value?.desc === desc) t.set({ sort: t.state.sort.filter((s) => sortOf(s).id !== id) })  // the active way again — off
  else if (mine.value) t.set({ sort: t.state.sort.map((s) => (sortOf(s).id === id ? (desc ? '-' : '') + id : s)) })  // its level kept
  else t.sortBy(id, desc)
}
const group = () => t.set({ group: grouped.value ? t.state.group.filter((g) => g !== id) : [...t.state.group, id] })
const quiet = () => t.toggleQuiet(props.c).then(() => (error.value = ''), (e) => (error.value = e.message))
function hide() {
  t.hide(id)
  emit('close')
}
function field() {  // the setup line opens its catalog of columns on this field
  t.ui.field = props.c.field
  t.ui.panel = 'cols'
  emit('close')
}

function place() {
  const r = props.anchor.getBoundingClientRect()
  at.value = { left: `${Math.max(4, Math.min(r.left, innerWidth - 300))}px`, top: `${r.bottom + 2}px`, maxHeight: `${Math.max(220, innerHeight - r.bottom - 12)}px` }
}
const away = (e) => !box.value?.contains(e.target) && !props.anchor.contains(e.target) && emit('close')  // its header toggles it itself
const key = (e) => e.key === 'Escape' && emit('close')
function listen(f) {
  document[f]('mousedown', away)
  document[f]('keydown', key)
  window[f]('scroll', place, true)  // any scroll: the page's or the table's own
  window[f]('resize', place)
}
onMounted(() => {
  place()
  listen('addEventListener')
})
onUnmounted(() => listen('removeEventListener'))
watch(() => t.state, place, { flush: 'post' })
</script>

<template>
  <Teleport to="body">
    <div ref="box" class="hmenu card shadow" :style="at">
      <div class="ttl text-truncate" :title="c.title">{{ c.title }}</div>
      <div v-for="desc in [false, true]" :key="String(desc)" class="d-flex align-items-center">
        <button type="button" class="it" :class="{ on: mine?.desc === desc }" :title="mine?.desc === desc ? 'Ще клік — без цього сортування' : ''" @click="sort(desc)">
          <Icon :name="desc ? 'down' : 'up'" /> Сортувати {{ desc ? 'за спаданням' : 'за зростанням' }}</button>
        <button v-if="!mine && levels.length" type="button" class="lvl" title="Лишити те сортування й додати це наступним рівнем" @click="t.sortBy(id, desc, true)">＋ рівнем</button>
      </div>
      <button v-if="canGroup" type="button" class="it" :class="{ on: grouped }" @click="group">
        <Icon name="layers" /> Групувати за цим<Icon v-if="grouped" name="check" class="ms-auto" /></button>
      <div class="sec">
        <div class="cap"><Icon name="filter" /> Фільтр</div>
        <FilterControl :col="c" :spec="t.state.filters[id] || ''" :rows="t.pool(id)" @set="(s) => t.setFilter(id, s)" />
      </div>
      <div class="sec">
        <button type="button" class="it" :class="{ on: t.quiet(c) }" title="Блідіша в таблиці й нижче в каталозі — в усіх видах" @click="quiet">
          <Icon name="short" /> Другорядна<Icon v-if="t.quiet(c)" name="check" class="ms-auto" /></button>
        <button type="button" class="it" @click="hide"><Icon name="eyeoff" /> Сховати</button>
        <button v-if="c.own" type="button" class="it" @click="field"><Icon name="pencil" /> Налаштувати поле</button>
        <div v-if="error" class="text-danger px-2 small">{{ error }}</div>
      </div>
    </div>
  </Teleport>
</template>

<style scoped>
.hmenu { position: fixed; z-index: 1030; width: 18.5rem; padding: .35rem; overflow-y: auto; font-size: .85rem; text-align: start; white-space: normal; }
.ttl { padding: .15rem .5rem .35rem; font-weight: 600; }
.it { display: flex; align-items: center; gap: .5rem; flex: 1; width: 100%; min-width: 0; padding: .25rem .5rem; border: 0; border-radius: .3rem;
      background: none; color: var(--bs-body-color); text-align: start; white-space: nowrap; }
.it:hover { background: var(--bs-tertiary-bg); }
.it.on { background: var(--bs-secondary-bg); font-weight: 500; }
.it > .icon:first-child { color: var(--bs-secondary-color); }
.lvl { flex-shrink: 0; padding: .1rem .4rem; border: 0; border-radius: .3rem; background: none; color: var(--act-add); font-size: .78rem; white-space: nowrap; opacity: .75; }
.lvl:hover { opacity: 1; background: color-mix(in srgb, var(--act-add) 10%, transparent); }
.sec { margin-top: .35rem; padding-top: .35rem; border-top: 1px solid var(--bs-border-color-translucent); }
.sec > .fc, .sec > .cap { padding: 0 .5rem; }
.cap { display: flex; align-items: center; gap: .35rem; margin-bottom: .25rem; font-size: .72rem; color: var(--bs-secondary-color); }
@media (max-width: 575px) {
  .hmenu { inset: auto .5rem .5rem .5rem !important; width: auto; max-height: 70vh !important; }
}
</style>
