<script setup>
import { fmtWhen } from '@core/labs.js'

// the teacher's rerun of the file (bin/nbrun, RUN): when, in what, how long, whether its line says what the student's
// did, the errors; `show` — the executed copy into the left column
defineProps({ run: Object, shown: String })
defineEmits(['show'])
</script>

<template>
  <p v-if="!run" class="small text-secondary mb-0">Ще не перезапускали: <code>bin/nbrun</code> на ноутбуці викладача.</p>
  <div v-else class="small">
    <div>{{ fmtWhen(run.at) }}<template v-if="run.engine"> · {{ run.engine }}</template><template v-if="run.seconds"> · {{ run.seconds }} с</template></div>
    <div>
      <span :class="run.same ? 'text-success' : 'text-danger'">{{ run.same ? '✅ рядок збігся з рядком студента' : '≠ рядок не збігся з рядком студента' }}</span>
      <template v-if="run.total"> · {{ run.right }} / {{ run.total }} ✅</template>
    </div>
    <code v-if="run.line" class="d-block text-break mt-1">{{ run.line }}</code>
    <ul v-if="run.errors?.length" class="list-unstyled mb-0 mt-1 text-danger">
      <li v-for="(e, i) in run.errors" :key="i"><b>{{ e.key }}</b> {{ e.name }}<template v-if="e.text">: {{ e.text }}</template></li>
    </ul>
    <template v-if="run.file">
      <span v-if="shown === run.file" class="d-inline-block mt-1 text-secondary">ліворуч — виконана копія</span>
      <a v-else href="#" class="rv-dot d-inline-block mt-1" @click.prevent="$emit('show', run.file)">показати виконану копію ліворуч</a>
    </template>
  </div>
</template>

<style scoped>
.rv-dot { text-decoration: underline dotted; text-underline-offset: .2em; }
</style>
