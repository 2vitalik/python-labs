<script setup>
import { inject } from 'vue'

import { saveView, viewOf } from '../viewStore.js'
import Icon from './Icon.vue'

// a view's yes/no switch in the library (T315 §7–§8): ⭐ etalon — «start a new view from this one», 📌 pinned — on the tabs
// of /table. On — in colour, off — grey; a click answers at once, a failure puts it back and says why
const props = defineProps({ view: { type: Object, required: true }, field: { type: String, required: true } })
const lib = inject('viewsLib')
const LOOK = {
  etalon: { on: 'starfill', off: 'star', yes: 'Еталон — з нього варто починати новий вид; клік — зняти', no: 'Зробити еталоном' },
  pinned: { on: 'pin', off: 'pin', yes: 'На вкладках таблиці; клік — прибрати з вкладок', no: 'Не на вкладках; клік — поставити' },
}
async function flip() {
  const v = viewOf(props.view.slug)
  const k = props.field
  v[k] = !v[k]
  try {
    await saveView(v.slug, { [k]: v[k] })
  } catch (e) {
    v[k] = !v[k]
    lib.error = e.message
  }
}
</script>

<template>
  <button type="button" class="iact vflag" :class="[field, { on: view[field] }]" :title="view[field] ? LOOK[field].yes : LOOK[field].no" :aria-pressed="!!view[field]"
          @click="flip"><Icon :name="view[field] ? LOOK[field].on : LOOK[field].off" /></button>
</template>

<style scoped>
.vflag.etalon.on, .vflag.etalon.on:hover { color: var(--bs-warning); }
.vflag.pinned.on, .vflag.pinned.on:hover { color: var(--bs-primary); }
</style>
