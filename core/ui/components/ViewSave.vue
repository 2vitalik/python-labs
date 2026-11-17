<script setup>
import { computed, onBeforeUnmount, ref, watch } from 'vue'

import { useTable } from '../tableCtx.js'
import { diff } from '../tableDiff.js'
import { toSaved } from '../tableViews.js'
import { editVersion } from '../viewStore.js'
import Icon from './Icon.vue'
import Pop from './Pop.vue'
import Reveal from './Reveal.vue'
import ViewName from './ViewName.vue'

// the view changed and not saved (T315 §2.3, §7): what changed in a few words and three ways on — save it (a version),
// make a new view of it (this one stays as saved), go back to the saved. A save leaves a quiet line for 15 s: the version
// it made, and a note to give it. A past version looked at has its own bar (ViewPeekBar), not this one
const t = useTable()
const LINGER = 15000
const brief = computed(() => (t.dirty ? diff(t.view.query, toSaved(t.state), t.cols).brief.join(' · ') || 'є зміни' : ''))
const busy = ref(false)
const error = ref('')
const forking = ref(false)
const done = ref(0)  // the version just saved
const late = ref(false)  // its time is out: the line goes once the note field is closed
const noting = ref(false)
const note = ref('')
const noted = ref('')
const noteField = ref()
const changed = computed(() => t.dirty && !t.peek)
const show = computed(() => changed.value || (!!done.value && (!late.value || noting.value)))
let timer
onBeforeUnmount(() => clearTimeout(timer))
watch(changed, (on) => on && (done.value = 0))  // changed again: the saved line gives way
watch(() => t.slug, () => (done.value = 0))
watch(noting, (on) => on && noteField.value?.focus(), { flush: 'post' })

async function run(work) {
  busy.value = true
  error.value = ''
  try {
    await work()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const save = () => run(async () => {
  await t.save()
  done.value = t.view.version
  late.value = noting.value = false
  noted.value = note.value = ''
  clearTimeout(timer)
  timer = setTimeout(() => (late.value = true), LINGER)
})
const fork = async (body) => {
  await t.fork({ ...body, emoji: body.emoji || t.view.emoji })
  forking.value = false
}
// Enter or leaving the field; once closed (Esc, saved) a late blur does nothing
async function addNote() {
  const text = note.value.trim()
  if (!noting.value || busy.value) return
  if (!text) return (noting.value = false)
  await run(async () => {
    noted.value = (await editVersion(t.slug, done.value, { note: text })).note
    noting.value = false
  })
}
</script>

<template>
  <Reveal :show>
    <div class="vsave d-flex flex-wrap align-items-center gap-2 small pt-2">
      <template v-if="changed">
        <span class="what text-truncate" :title="brief">змінено: {{ brief }}</span>
        <button type="button" class="btn btn-sm btn-success" :disabled="busy" title="Записати зміни у вид — нова версія" @click="save"><Icon name="check" /> Зберегти</button>
        <Pop v-model="forking" width="22rem">
          <template #trigger="{ toggle }">
            <button type="button" class="btn btn-sm btn-add" :disabled="busy" title="Те, що на екрані, — окремим видом; цей лишиться, як був збережений" @click="toggle">
              <Icon name="plus" /> як новий вид</button>
          </template>
          <ViewName :go="fork" @cancel="forking = false" />
        </Pop>
        <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="busy" title="Повернути вид, як він збережений" @click="t.reset()"><Icon name="back" /> скинути</button>
      </template>
      <template v-else>
        <span class="what"><Icon name="check" class="text-success" /> збережено · версія {{ done }}</span>
        <span v-if="noted" class="what fst-italic text-truncate" :title="noted">{{ noted }}</span>
        <input v-else-if="noting" ref="noteField" v-model="note" class="form-control form-control-sm note" placeholder="що змінилось — Enter" aria-label="Нотатка версії"
               :readonly="busy" @keydown.enter.prevent="addNote" @keydown.esc="noting = false" @blur="addNote">
        <button v-else type="button" class="more-field" @click="noting = true">＋ нотатка</button>
      </template>
      <span v-if="error" class="text-danger">{{ error }}</span>
    </div>
  </Reveal>
</template>

<style scoped>
.what { min-width: 0; color: var(--bs-secondary-color); }
.note { width: 16rem; max-width: 100%; }
</style>
