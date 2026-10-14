<script setup>
import { computed, onMounted, ref, watch } from 'vue'

import { getAttendance, getStudents, postLessonAlias } from '../api.js'
import { fmtDur } from '../lesson.js'
import { byGroup } from '../studentFilter.js'
import Avatar from './Avatar.vue'
import ZoomPull from './ZoomPull.vue'

// «👥 Були»: who was in the Zoom meeting and for how long — avatars by group, minutes under each, pale under the threshold (T222);
// the admin also sees the unknown names («хто це?» → an alias, as for speakers), the teacher's own time and the pull button
const props = defineProps({ lesson: Object, admin: Boolean })
const emit = defineEmits(['changed'])
const data = ref(null)
const students = ref([])
const error = ref('')
const load = async () => (data.value = props.lesson.zoom.uuid ? await getAttendance(props.lesson.slug) : null)
watch(() => props.lesson.zoom.pulled, load, { immediate: true })
onMounted(async () => props.admin && (students.value = (await getStudents()).filter((s) => s.status === 'student')))

const groups = computed(() => byGroup((data.value?.people || []).map((p) => ({ ...p, group: p.person.group, test: p.person.test }))))
const present = computed(() => new Set(data.value.people.filter((p) => p.present).map((p) => p.person.nick)).size)
const average = computed(() => data.value.people.reduce((n, p) => n + p.seconds, 0) / (data.value.people.length || 1))
const when = computed(() => data.value.meeting.start && new Date(data.value.meeting.start).toLocaleString('uk-UA', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' }))
const hint = (p) => [p.person?.name || p.name, p.person?.group, fmtDur(p.seconds), p.late >= 300 && `спізнився на ${Math.round(p.late / 60)} хв`, !p.present && 'менше чверті заняття']
  .filter(Boolean).join(' · ')
async function assign(name, nick) {
  if (!nick) return
  error.value = ''
  try {
    await postLessonAlias(props.lesson.slug, { name, nick })
    await load()
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <section class="mt-4">
    <div v-if="data" class="d-flex flex-wrap align-items-baseline gap-2">
      <span class="fw-semibold">👥 Були · {{ present }} із {{ data.of }}</span>
      <span class="text-secondary small">· у середньому {{ fmtDur(average) }} · зустріч {{ fmtDur(data.seconds) }}<template v-if="when">, {{ when }}</template></span>
    </div>
    <p v-else-if="admin" class="text-secondary small mb-2">👥 Відвідування ще не забрано із Zoom</p>
    <div v-for="g in groups" :key="g.name" class="d-flex flex-wrap align-items-start gap-2 mt-2">
      <span class="group small text-body-tertiary">{{ g.name || 'без групи' }}</span>
      <RouterLink v-for="p in g.list" :key="p.name" :to="`/students/${p.person.nick}`" class="who text-center text-decoration-none" :class="{ pale: !p.present }" :title="hint(p)">
        <Avatar :user="p.person" :size="36" />
        <div class="min small text-secondary">{{ Math.round(p.seconds / 60) }}</div>
      </RouterLink>
    </div>
    <div v-if="data && admin" class="small mt-2">
      <span v-for="t in data.teachers" :key="t.name" class="text-body-tertiary me-3">🧑‍🏫 {{ t.person.name }} · {{ fmtDur(t.seconds) }}</span>
      <div v-for="u in data.unknown" :key="u.name" class="unknown mt-1" :class="{ pale: !u.present }">
        <span><span class="badge text-bg-warning fw-normal me-2">?</span>{{ u.name }} <span class="text-body-tertiary">· {{ fmtDur(u.seconds) }}<template v-if="u.email"> · {{ u.email }}</template></span></span>
        <select class="form-select form-select-sm" @change="assign(u.name, $event.target.value)">
          <option value="">хто це?</option>
          <option v-for="s in students" :key="s.nick" :value="s.nick">{{ s.name }} {{ s.group }}</option>
        </select>
      </div>
      <span v-if="error" class="text-danger">{{ error }}</span>
    </div>
    <div v-else-if="data && data.others" class="small text-body-tertiary mt-1">ще {{ data.others }} — імена, яких реєстр не знає</div>
    <ZoomPull v-if="admin" :lesson class="mt-2" @pulled="$emit('changed')" />
  </section>
</template>

<style scoped>
.group { width: 100%; }
.who { width: 2.6rem; }
.min { line-height: 1.1; margin-top: .15rem; font-variant-numeric: tabular-nums; }
.pale { opacity: .4; }
.unknown { display: grid; grid-template-columns: 1fr auto; gap: .5rem; align-items: center; max-width: 36rem; }
</style>
