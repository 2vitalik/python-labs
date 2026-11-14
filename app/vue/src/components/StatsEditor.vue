<script setup>
import { computed, nextTick, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { vPeek } from '@core/peek.js'
import { statOf } from '../catalog.js'
import { statItems } from '../items.js'
import Picker from './Picker.vue'
import ProposeCard from './ProposeCard.vue'

// stats as rows «назва = значення одиниця» (T270 §7): a catalog stat brings its label and unit, the student's own one has
// both typed; a name already present is marked and not sent twice; a catalog stat shows its card under the mouse (T291 §6).
// `free` — no catalog, own rows only (a level's)
const stats = defineModel({ type: Array, default: () => [] })
const props = defineProps({ free: Boolean })
const rows = ref([])
const open = ref(false)
const proposing = ref(false)
const root = ref()
let uid = 0
let sent = ''  // what went up last: the same list coming back down is not a reset

const own = (key) => props.free || !statOf(key)
// `withUnit` — the student's own unit field is in the row: a unit is rare, it comes by «＋ од.» (T291 §4)
const toRow = (s) => ({ ...s, uid: ++uid, own: own(s.key), label: s.label || s.key, was: s.label || s.key, withUnit: !!s.unit })
const names = (r) => (r.own ? [r.label.trim().toLowerCase()] : [r.key.toLowerCase(), r.label.toLowerCase()]).filter(Boolean)
const dup = computed(() => rows.value.map((r, i) => names(r).some((n) => rows.value.slice(0, i).some((x) => names(x).includes(n)))))
// an own row keeps its key while its name stays as it came
const out = (r) => (r.own
  ? { key: r.key && r.label.trim() === r.was ? r.key : r.label.trim(), label: r.label.trim(), value: r.value, unit: r.unit }
  : { key: r.key, label: r.label, value: r.value, unit: statOf(r.key)?.unit || r.unit })  // a card without a unit («ціна») takes the student's
const items = computed(() => statItems(new Set(rows.value.filter((r) => !r.own).map((r) => r.key))))

watch(stats, (v) => { if (JSON.stringify(v) !== sent) rows.value = (v || []).map(toRow) }, { immediate: true })
watch(rows, (rs) => {
  const list = rs.filter((r, i) => !dup.value[i] && (r.own ? r.label.trim() : r.key)).map(out)
  sent = JSON.stringify(list)
  stats.value = list
}, { deep: true })

function push(row, field) {
  rows.value.push({ key: '', label: '', value: '', unit: '', was: '', ...row, uid: ++uid })
  open.value = false
  nextTick(() => [...root.value.querySelectorAll('.srow')].at(-1)?.querySelector(field)?.focus())
}
const pick = (it) => (it.taken ? (open.value = false) : push({ key: it.key, label: it.title, unit: it.stat.unit, own: false }, '.val'))
const addOwn = (name = '') => push({ label: name, own: true }, name ? '.val' : '.name-in')
function showUnit(r, i) {
  r.withUnit = true
  nextTick(() => root.value.querySelectorAll('.srow')[i]?.querySelector('.unit-in')?.focus())
}
watch(open, () => (proposing.value = false))
</script>

<template>
  <div ref="root" class="vstack gap-1">
    <div v-for="(r, i) in rows" :key="r.uid" class="srow">
      <span class="ico">{{ r.own ? '•' : statOf(r.key)?.icon }}</span>
      <span v-if="!r.own" v-peek="statOf(r.key)?.slug ? { kind: 'task', id: statOf(r.key).slug } : null" class="name"
            :title="statOf(r.key)?.slug ? null : statOf(r.key)?.desc">{{ statOf(r.key)?.label || r.label }}</span>
      <input v-else v-model="r.label" class="form-control form-control-sm name-in" :class="{ 'is-invalid': dup[i] }" placeholder="назва">
      <span class="eq">=</span>
      <input v-model="r.value" class="form-control form-control-sm val" placeholder="3">
      <span v-if="!r.own && statOf(r.key)?.unit" class="unit" title="одиницю дає картка параметра">{{ statOf(r.key).unit }}</span>
      <input v-else-if="r.withUnit" v-model="r.unit" class="form-control form-control-sm unit-in" placeholder="од.">
      <button v-else type="button" class="more-field" title="одиниця виміру: шт., с, клітинок за тік…" @click="showUnit(r, i)">＋ од.</button>
      <button type="button" class="iact del" title="Прибрати" @click="rows.splice(i, 1)"><Icon name="minus" /></button>
      <div v-if="dup[i]" class="bad">такий параметр уже є</div>
    </div>
    <div v-if="free"><button type="button" class="btn btn-sm btn-add" @click="addOwn()"><Icon name="plus" /> параметр</button></div>
    <Pop v-else v-model="open" width="22rem">
      <template #trigger="{ toggle }">
        <button type="button" class="btn btn-sm btn-add" @click="toggle"><Icon name="plus" /> параметр</button>
      </template>
      <ProposeCard v-if="proposing" what="новий параметр" all-to="/tasks?zone=entities&sub=params" zone="entities" subzone="params"
                   @done="addOwn" @cancel="proposing = false" />
      <Picker v-else inline autofocus :items placeholder="HP, швидкість, шкода…" @pick="pick">
        <template #footer>
          <div class="foot">
            <button type="button" class="btn btn-sm btn-add" @click="addOwn()"><Icon name="plus" /> свій параметр</button>
            <a href="#" @click.prevent="proposing = true">запропонувати в каталог</a>
          </div>
        </template>
      </Picker>
    </Pop>
  </div>
</template>

<style scoped>
/* one line a stat even in a narrow card (T291 §4): the name gives way, the value and the unit keep their size */
.srow { display: flex; flex-wrap: wrap; align-items: center; gap: .3rem; }
.ico { width: 1.1rem; text-align: center; }
.name { flex: 1 1 4.5rem; min-width: 4.5rem; max-width: 9rem; font-size: .85rem; }
.name-in { flex: 1 1 5rem; min-width: 5rem; max-width: 9rem; }
.val { width: 3.8rem; }
.unit-in { width: 3.6rem; }
.eq, .unit { color: var(--bs-secondary-color); }
.unit { font-size: .8rem; white-space: nowrap; }
.bad { width: 100%; padding-left: 1.65rem; font-size: .75rem; color: var(--bs-danger); }
.foot { display: flex; align-items: center; gap: .5rem; margin: .4rem .5rem .1rem; padding-top: .4rem; border-top: 1px solid var(--bs-border-color-translucent); font-size: .78rem; }
.foot a { margin-left: auto; color: var(--bs-secondary-color); }
</style>
