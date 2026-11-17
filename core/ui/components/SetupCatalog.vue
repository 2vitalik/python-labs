<script setup>
import { computed, onMounted, ref } from 'vue'

import { useTable } from '../tableCtx.js'
import { rel } from '../tableViews.js'
import { bySection, hit } from './ColPick.vue'
import FieldForm from './FieldForm.vue'
import Icon from './Icon.vue'
import SetupSection from './SetupSection.vue'

// the catalog of columns (T315 §3): a search, then the sections — a lab's columns once, for «this lab» (they go in by a
// relative id, the view then serves every lab) or for a lab picked by its number — and one's own columns, made and changed
// right here: their form takes the catalog's place. t.ui.field is the field in the form ({} — a new one): the header's
// menu of a column opens it too
const t = useTable()
const q = ref('')
const lab = ref(0)  // 0 — «ця лаба»; N — lab N itself
const find = ref()
const sections = computed(() => bySection(t.cols.filter((c) => (!c.lab || c.lab === (lab.value || t.state.lab)) && hit(c, q.value))
  .map((c) => ({ ...c, id: c.lab && !lab.value ? rel(c.key, c.lab) : c.key }))))
// a field with values written keeps its type and what it is on — the API would say 409
const locked = (f) => !!f.key && t.data.rows.some((r) => Object.keys(r.fields || {}).some((k) => k === f.key || k.startsWith(`${f.key}.`)))
const idOf = (f) => (f.scope === 'lab' ? `f.${f.key}.lab` : `f.${f.key}`)
// a new column goes into the view at once; one turned from «на студента» to «на лабу» (or back) keeps its place there
async function saved(f) {
  const was = t.ui.field
  t.ui.field = null
  await t.reload()
  if (!was.key) t.shown.some((c) => c.field?.key === f.key) || t.setCols([...t.state.cols, idOf(f)])  // a family may have taken it in already
  else if (was.scope !== f.scope) t.setCols(t.state.cols.map((id) => (id === idOf(was) ? idOf(f) : id)))
}
async function dropped() {
  const { key } = t.ui.field
  t.ui.field = null
  await t.reload()
  const left = t.state.cols.filter((id) => id !== `f.${key}` && !id.startsWith(`f.${key}.`))
  if (left.length < t.state.cols.length) t.setCols(left)
}
onMounted(() => find.value?.focus({ preventScroll: true }))
</script>

<template>
  <div class="cat">
    <Transition name="cat-swap" mode="out-in">
      <FieldForm v-if="t.ui.field" :key="t.ui.field.key || '+'" :field="t.ui.field" :locked="locked(t.ui.field)" @saved="saved" @deleted="dropped" @close="t.ui.field = null" />
      <div v-else>
        <input ref="find" v-model="q" type="search" class="form-control form-control-sm" placeholder="Знайти колонку: назва чи значок">
        <div class="cat-list">
          <SetupSection v-for="s in sections" :key="s.cat" :cat="s.cat" :cols="s.cols" :searching="!!q.trim()">
            <div v-if="s.cat === 'Лаба'" class="cat-labs">
              <button type="button" :class="{ on: !lab }" title="Колонки «цієї лаби»: вид покаже їх для тієї лаби, на яку повернутий" @click="lab = 0">ця лаба ({{ t.state.lab }})</button>
              <button v-for="l in t.data.labs" :key="l.n" type="button" :class="{ on: lab === l.n }" :title="`Колонки саме лаби ${l.n} — щоб поставити поруч дві лаби`"
                      @click="lab = l.n">{{ l.n }}</button>
            </div>
          </SetupSection>
          <div v-if="!sections.length" class="small text-secondary mt-2">Нічого не знайдено</div>
        </div>
        <button type="button" class="btn btn-sm btn-add mt-2" @click="t.ui.field = {}"><Icon name="plus" /> своя колонка</button>
      </div>
    </Transition>
  </div>
</template>

<style scoped>
.cat { min-width: 0; }
/* the badges on the words' corners stick out a little: room for them on top and on the right */
.cat-list { max-height: min(58vh, 30rem); margin-top: .35rem; padding: .3rem .55rem 0 0; overflow-y: auto; }
.cat-labs { display: flex; flex-wrap: wrap; gap: .2rem; margin: .1rem 0 .25rem; font-size: .75rem; }
.cat-labs button { padding: 0 .4rem; border: 1px solid transparent; border-radius: .3rem; background: none; color: var(--bs-secondary-color); }
.cat-labs button:hover { background: var(--bs-tertiary-bg); }
.cat-labs button.on { border-color: var(--bs-border-color); background: var(--bs-secondary-bg); color: var(--bs-body-color); }
.cat-swap-enter-active, .cat-swap-leave-active { transition: opacity .15s ease; }
.cat-swap-enter-from, .cat-swap-leave-to { opacity: 0; }
</style>
