<script setup>
import { computed, ref } from 'vue'

import { vHint } from '@core/hint.js'

import { prevOf, WAYS } from '../labText.js'
import LabAnswers from './LabAnswers.vue'
import LabLadder from './LabLadder.vue'
import LabVersions from './LabVersions.vue'
import ReviewFile from './ReviewFile.vue'
import ReviewMarks from './ReviewMarks.vue'
import ReviewRun from './ReviewRun.vue'

// the right side of the review desk, in the order the teacher goes: hint and points, answers, levels, defence, rerun,
// versions, the file. `shown` — the version on the left; `compare` — mark what changed since the one before it
const props = defineProps({ n: Number, doc: Object, shown: String })
const compare = defineModel('compare', { type: Boolean, default: false })
defineEmits(['show', 'saved', 'freed'])
const marks = ref()
const hasPrev = computed(() => !!props.shown && !!prevOf(props.doc.files, props.shown))
defineExpose({ dirty: () => !!marks.value?.dirty() })
</script>

<template>
  <div class="rv-panel">
    <ReviewMarks ref="marks" :n :doc @saved="$emit('saved', $event)" />
    <div class="group-box">
      <div class="group-cap">Відповіді</div>
      <LabAnswers :answers="doc.answers" :values="doc.values" :verdict="doc.verdict" />
      <code v-if="doc.line" class="d-block small text-secondary text-break mt-1">{{ doc.line }}</code>
    </div>
    <div v-if="doc.grade?.steps?.length" class="group-box">
      <div class="group-cap">Рівні</div>
      <LabLadder :steps="doc.grade.steps" />
    </div>
    <div class="group-box small">
      <div class="group-cap">Захист</div>
      <div>Студент: <b>{{ WAYS[doc.way] || 'ще не обрав' }}</b>
        <a v-if="doc.video" :href="doc.video" target="_blank" rel="noopener" class="ms-1">запис ↗</a></div>
      <ol v-if="doc.ask?.length" class="mb-0 mt-1 ps-3"><li v-for="q in doc.ask" :key="q">{{ q }}</li></ol>
    </div>
    <div class="group-box">
      <div class="group-cap">Перезапуск</div>
      <ReviewRun :run="doc.file?.run" :shown @show="$emit('show', $event)" />
    </div>
    <div v-if="doc.files?.length" class="group-box">
      <div class="group-cap">Версії</div>
      <LabVersions :files="doc.files" :current="shown" @pick="$emit('show', $event)" />
      <div v-hint="hasPrev ? '' : 'це перша версія — нема з чим порівнювати'" class="form-check form-switch small mt-1 mb-0">
        <input id="rv-compare" v-model="compare" class="form-check-input" type="checkbox" :disabled="!hasPrev">
        <label class="form-check-label" for="rv-compare">порівняти з попередньою</label>
      </div>
    </div>
    <div class="group-box">
      <div class="group-cap">Файл</div>
      <ReviewFile :n :doc :shown @freed="$emit('freed')" />
    </div>
  </div>
</template>

<style scoped>
.rv-panel { display: flex; flex-direction: column; gap: .6rem; }
.rv-panel :deep(.group-box) { background: var(--bs-body-bg); }
</style>
