<script setup>
import { computed, ref } from 'vue'

import { view } from '../table.js'
import TableEdit from './TableEdit.vue'

// one cell: the text, a line under it, the hover (table.js view()). A lab cell asks the grid for the editor; an editable cell
// toggles (bool) or opens its small editor (TableEdit) right here
const props = defineProps({ col: { type: Object, required: true }, row: { type: Object, required: true } })
const emit = defineEmits(['pick', 'save'])
const editing = ref(false)
const v = computed(() => view(props.col, props.row))
const editable = computed(() => !!props.col.edit)
const inner = computed(() => v.value.link && v.value.link.startsWith('/'))
function click() {
  if (props.col.type === 'lab') emit('pick')
  else if (!editable.value) return
  else if (props.col.type === 'bool') emit('save', props.col.get(props.row) === true ? (props.col.edit === 'mark' ? false : null) : true)
  else editing.value = !editing.value
}
function save(value) {
  editing.value = false
  emit('save', value)
}
</script>

<template>
  <div class="c" :class="[v.cls, { act: editable || col.type === 'lab' }]" :title="v.title" @click="click">
    <RouterLink v-if="inner" :to="v.link" class="lnk" @click.stop>{{ v.text }}</RouterLink>
    <a v-else-if="v.link" :href="v.link" target="_blank" class="lnk" @click.stop>{{ v.text }}</a>
    <span v-else-if="v.parts" class="t"><span v-for="(p, i) in v.parts" :key="i" :class="p.cls">{{ p.text }}</span></span>
    <span v-else class="t">{{ v.text }}</span>
    <small v-if="v.sub" class="sub">{{ v.sub }}</small>
    <TableEdit v-if="editing" :col :row @save="save" @close="editing = false" />
  </div>
</template>

<style scoped>
.c { position: relative; display: block; min-width: 2.4rem; max-width: 11rem; padding: .15rem .3rem; border: 1px solid transparent; border-radius: .35rem; line-height: 1.15;
     font-size: .95rem; overflow: hidden; text-overflow: ellipsis; }
.c.act { cursor: pointer; }
.c.act:hover { border-color: var(--bs-border-color); background: var(--bs-tertiary-bg); }
.t { display: block; overflow: hidden; text-overflow: ellipsis; }
.sub { display: block; font-size: .66rem; color: var(--bs-secondary-color); white-space: nowrap; }
.none .t { color: var(--bs-tertiary-color); }
.zero .t { color: var(--bs-tertiary-color); }
.num .t { font-variant-numeric: tabular-nums; }
.t > span { margin-right: .15rem; }
.t > .doubt { text-decoration: line-through; text-decoration-color: var(--bs-danger); text-decoration-thickness: 2px; opacity: .7; }
.lnk { text-decoration: none; }
.lnk:hover { text-decoration: underline; }
</style>
