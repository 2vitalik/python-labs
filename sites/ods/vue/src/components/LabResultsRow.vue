<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'
import { fmtWhen } from '@core/labs.js'

import { putLabResult } from '../api.js'
import { sameOf, WAYS } from '../labText.js'
import LabClip from './LabClip.vue'
import LabPieces from './LabPieces.vue'

// a student's line of the stream's table (T354 §6); the mark and the note are saved as soon as they change;
// `runs` — the table has the rerun column (somebody's file was rerun)
const props = defineProps({ n: Number, r: Object, runs: Boolean })
const saved = ref('')  // '' · 'ok' · the API's words
const files = computed(() => (Array.isArray(props.r.files) ? props.r.files.length : props.r.files || 0))
const run = computed(() => props.r.file?.run)
const g = computed(() => props.r.grade || {})

async function save() {
  const r = props.r
  const points = r.points === '' || r.points === null || r.points === undefined ? null : Number(r.points)
  try {
    const back = await putLabResult(props.n, r.vid, { points, note: r.note })
    r.points = back.points
    r.note = back.note
    saved.value = 'ok'
  } catch (e) {
    saved.value = e.message
  }
}
</script>

<template>
  <tr>
    <td class="text-nowrap">
      <RouterLink :to="`/labs/${n}/results/${r.vid}`">{{ r.who?.name || r.student }}</RouterLink>
      <div class="sub">{{ r.who?.nick }}</div>
    </td>
    <td class="text-nowrap"><code>{{ r.vid }}</code></td>
    <td class="text-nowrap">
      <template v-if="r.attempts">{{ r.ok }} / {{ r.total }}<div v-hint="'спроб рядка'" class="sub">спроб {{ r.attempts }}</div></template>
      <span v-else class="text-secondary">—</span>
    </td>
    <td class="text-nowrap">
      <template v-if="files"><LabClip /> {{ files }}<div class="sub">{{ fmtWhen(r.file?.at) }}</div></template>
      <span v-else class="text-secondary">—</span>
    </td>
    <td class="pcs-cell"><LabPieces :count="r.count" /></td>
    <td v-if="runs" class="text-nowrap">
      <span v-if="!run" class="text-secondary">—</span>
      <span v-else v-hint="sameOf(run).text" :class="sameOf(run).cls">{{ sameOf(run).short }}</span>
    </td>
    <td class="text-nowrap small">
      <template v-if="r.way !== r.defended || !WAYS[r.defended]"><span :class="{ 'text-secondary': r.defended }">{{ WAYS[r.way] || '—' }}</span></template>
      <template v-if="WAYS[r.defended]"><template v-if="r.way !== r.defended"> → </template><b v-hint="'захист прийнято'" class="text-success">{{ WAYS[r.defended] }}</b></template>
    </td>
    <td class="text-nowrap">
      <b>{{ g.hint ?? '—' }}</b><div v-if="g.work && g.work !== g.hint" v-hint="'рівень самої роботи'" class="sub">робота {{ g.work }}</div>
    </td>
    <td><input v-model="r.points" type="number" min="0" max="20" class="form-control form-control-sm pts" @change="save"></td>
    <td><input v-model="r.note" class="form-control form-control-sm note" @change="save"></td>
    <td class="small text-nowrap">
      <Icon v-if="saved === 'ok'" name="check" class="text-success" />
      <span v-else-if="saved" class="text-danger">{{ saved }}</span>
    </td>
  </tr>
</template>

<style scoped>
.sub { color: var(--bs-secondary-color); font-size: .75rem; }
.pts { width: 4.5rem; }
.note { min-width: 9rem; }
.pcs-cell { min-width: 11rem; }
</style>
