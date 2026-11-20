<script setup>
import { computed } from 'vue'

import { fmtWhen } from '@core/labs.js'

// a lab among the student's own, in a few quiet words (BRIEF of GET /api/variants): where it is handed in, the deadline,
// what the site has, the mark. A lab handed in by Telegram says nothing of «not yet» nor of a missed deadline: the
// site cannot know. Red — as on «Моя лаба»: past the deadline with no version in time
const props = defineProps({ m: Object })
const words = computed(() => {
  const m = props.m, out = []
  if (m.handin === 'telegram') out.push('здаємо в Telegram')
  if (m.due) out.push(`до ${fmtWhen(m.due)}`)
  if (m.handed) out.push(m.ok ? `здано: ${m.ok} із ${m.total} ✅` : 'здано')
  else if (m.handin === 'site') out.push('ще не здано')
  if (m.points !== null && m.points !== undefined) out.push(`оцінка ${m.points}`)
  return out
})
const late = computed(() => {
  const m = props.m
  if (!m.late || m.in_time) return ''
  return m.handed ? 'після дедлайну' : m.handin === 'site' ? 'дедлайн минув' : ''
})
</script>

<template>
  <span class="text-secondary">{{ words.join(' · ') }}<span v-if="late" class="text-danger"> · {{ late }}</span></span>
</template>
