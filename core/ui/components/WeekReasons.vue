<script setup>
import { computed, ref, shallowRef, watch } from 'vue'

import { daysLabel, settle, span } from '../week.js'
import { REASONS, emojiOf, reds, toggleReason } from '../weekWhy.js'

// why each «не можу»: chips for the usual reasons and a field for one's own. Red marks that share hours and reason
// make one line — a rectangle painted over Monday–Friday is explained once
const props = defineProps({ frame: { type: Object, required: true } })
const marks = defineModel({ type: Array, required: true })
const id = (m) => `${m.day}:${m.start}`
const group = (list) => reds(list).map((g) => g.map(id))
const typing = ref(false)
const groups = shallowRef(group(marks.value))
const shape = computed(() => marks.value.filter((m) => m.kind === 'no').map((m) => `${id(m)}:${m.end}`).join())
// while a reason is typed the lines stay as they are: two of them joining would take the field from under the cursor
watch(shape, () => typing.value || (groups.value = group(marks.value)))
const rows = computed(() => groups.value.map((ids) => marks.value.filter((m) => m.kind === 'no' && ids.includes(id(m)))).filter((list) => list.length)
  .map((list) => ({ key: id(list[0]), list, why: list[0].why, label: `${daysLabel(list.map((m) => m.day))} ${span(list[0])}` })))

const put = (row, why) => marks.value.map((m) => (row.list.includes(m) ? { ...m, why } : m))
// what is typed settles when the field is left, a chip — at once: neighbours with one reason become one mark
function settled(list) {
  const next = settle(list.map((m) => ({ ...m, why: m.why.trim() })), props.frame)
  if (JSON.stringify(next) !== JSON.stringify(marks.value)) marks.value = next  // a field left as it was is no change to save
  groups.value = group(next)
}
const leave = () => { typing.value = false; settled(marks.value) }
</script>

<template>
  <div v-if="rows.length" class="card mb-3">
    <div class="card-header">Чому не можеш <span class="small text-secondary">— для кожного червоного блока</span></div>
    <ul class="list-group list-group-flush">
      <li v-for="row in rows" :key="row.key" class="list-group-item">
        <div class="d-flex flex-wrap align-items-center gap-2">
          <b class="text-nowrap">{{ row.label }}</b>
          <input class="why form-control form-control-sm" :class="{ 'is-invalid': !row.why.trim() }" :value="row.why" maxlength="200"
                 placeholder="обери нижче або напиши своє" @focus="typing = true" @blur="leave" @input="marks = put(row, $event.target.value)">
        </div>
        <div class="d-flex flex-wrap gap-1 mt-2">
          <button v-for="r in REASONS" :key="r" type="button" class="btn btn-sm chip" :class="row.why.includes(emojiOf(r)) ? 'btn-secondary' : 'btn-outline-secondary'"
                  @click="settled(put(row, toggleReason(row.why, r)))">{{ r }}</button>
        </div>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.why { flex: 1 1 12rem; width: auto; }
</style>
