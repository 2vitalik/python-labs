<script setup>
import { computed, reactive, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import { postTask, putTask } from '../api.js'
import { PROOFS } from '../proof.js'
import { csv, place, toForm, toPayload } from '../taskForm.js'
import { subzoneKind } from '../taskMeta.js'
import { TIPS } from '../taskTips.js'
import RuleBlank from './RuleBlank.vue'
import SlotsEditor from './SlotsEditor.vue'
import TaskGroup from './TaskGroup.vue'
import TaskMain from './TaskMain.vue'
import TaskNames from './TaskNames.vue'
import TaskWhere from './TaskWhere.vue'

// the teacher's form of a catalog card, in the card's own place: groups of dense rows under small captions (T284 §6), no page.
// A task without `id` is a new card; the saved one goes straight into the loaded catalog
const props = defineProps({ task: Object })
const emit = defineEmits(['done'])
const f = reactive(toForm(props.task))
const subKind = computed(() => subzoneKind(f.zone, f.subzone, csv(f.tags)))
const kind = computed(() => f.kind || subKind.value)
const busy = ref(false)
const error = ref('')

async function save() {
  busy.value = true
  error.value = ''
  try {
    const p = toPayload(f, kind.value)
    place(props.task.id ? await putTask(props.task.id, p) : await postTask(p))
    emit('done')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <form class="task-edit border rounded p-2 vstack" @submit.prevent="save">
    <TaskGroup label="Основне"><TaskMain :f :kind :sub-kind="subKind" /></TaskGroup>
    <TaskWhere :f :open="!task.id" />
    <TaskGroup label="Опис" :tip="TIPS.description">
      <GrowArea v-model="f.description" class="form-control form-control-sm" placeholder="що зробити і що я перевіряю" />
    </TaskGroup>
    <TaskGroup label="Параметри заявки" :tip="TIPS.slots"><SlotsEditor v-model="f.slots" /></TaskGroup>
    <TaskGroup label="Доказ" :tip="TIPS.proof">
      <div class="row-f align-items-center">
        <select v-model="f.proof" class="form-select form-select-sm w-auto">
          <option value="">— нічого особливого</option>
          <option v-for="(p, k) in PROOFS" :key="k" :value="k">{{ p.icon }} {{ p.label }}</option>
        </select>
        <span v-if="PROOFS[f.proof]" class="hint">на картці: «{{ PROOFS[f.proof].ask }}»</span>
      </div>
    </TaskGroup>
    <TaskGroup label="Інші назви" :tip="TIPS.aliases"><TaskNames v-model="f.aliases" /></TaskGroup>
    <TaskGroup v-if="kind === 'rule'" label="Заготовка правила" :tip="TIPS.blank"><RuleBlank v-model="f.rule" /></TaskGroup>
    <div class="d-flex align-items-center gap-2">
      <button class="btn btn-sm btn-success" :disabled="busy"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('done')">Скасувати</button>
      <RouterLink v-if="task.id" :to="`/tasks/history?slug=${task.slug}`" class="ms-auto small text-decoration-none">🕘 історія</RouterLink>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </form>
</template>

<style>
/* the dense rows of the form and its parts (TaskMain, TaskWhere, SlotsEditor, TaskNames, RuleBlank): a tiny caption over each field;
   a caption with a dotted line has a hint under the mouse (taskTips.js) */
.task-edit { gap: .8rem; background: var(--bs-body-bg); font-size: .85rem; }
.task-edit .row-f { display: flex; flex-wrap: wrap; gap: .35rem; align-items: flex-end; }
.task-edit .f { display: flex; flex-direction: column; gap: .1rem; margin: 0; font-size: .7rem; color: var(--bs-secondary-color); }
.task-edit .grow { flex: 1 1 8rem; min-width: 0; }
.task-edit .w3 { width: 3rem; } .task-edit .w4 { width: 4.5rem; } .task-edit .w7 { width: 7rem; }
.task-edit .w8 { width: 8.5rem; } .task-edit .w9 { width: 10rem; }
.task-edit .hint { font-size: .72rem; color: var(--bs-secondary-color); }
.task-edit .lang { width: 2rem; flex-shrink: 0; font-size: .68rem; text-transform: uppercase; color: var(--bs-secondary-color); }
.task-edit .tip { text-decoration: underline dotted; text-decoration-color: color-mix(in srgb, currentColor 60%, transparent);
                  text-underline-offset: .2em; cursor: help; }
</style>
