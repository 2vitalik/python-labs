<script setup>
import InlinePop from '@core/components/InlinePop.vue'
import { STATUSES } from '../catalog.js'
import { saveTask } from '../taskForm.js'
import TaskChoices from './TaskChoices.vue'

// a card's status where it reads, for the teacher (T306): each with what it means for the students; a pick is saved at once
const p = defineProps({ task: Object, can: Boolean })
// what the API does with each (routes/tasks.py, my_claims.py, options.py)
const MEANS = {
  draft: 'бачиш лише ти: студенти її не бачать і не заявляють',
  active: 'у каталозі для всіх, студенти заявляють',
  archived: 'прибрана з каталогу: нових заявок нема, старі лишаються',
}
const items = Object.entries(STATUSES).map(([k, title]) => ({ key: k, title, desc: MEANS[k] }))
const pick = (status, choose, close) => (status === p.task.status ? close() : choose(saveTask(p.task, { status })))
</script>

<template>
  <InlinePop :can width="19rem" :tip="`${MEANS[task.status]}\nКлік — змінити`">
    {{ STATUSES[task.status] }}
    <template #panel="{ choose, close }">
      <TaskChoices :items :current="task.status" @pick="pick($event, choose, close)" />
    </template>
  </InlinePop>
</template>
