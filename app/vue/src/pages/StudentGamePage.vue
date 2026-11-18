<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getStudentGame } from '../api.js'
import Crumbs from '@core/components/Crumbs.vue'
import Icon from '@core/components/Icon.vue'
import GameEditor from '../components/GameEditor.vue'
import GameHead from '../components/GameHead.vue'
import Md from '@core/components/Md.vue'
import StudentPager from '../components/StudentPager.vue'
import { loadCatalog } from '../catalog.js'
import { studentsCrumbs } from '@core/students.js'
import { editing, setEditing } from '../teacher.js'
import { useTitle } from '@core/title.js'
import { lookAs, user } from '@core/user.js'
import { wideOf } from '@core/wide.js'

// a student's game as others see it — the passport: head, description, then the same sections as the editor, read-only;
// the teacher accepts or returns claims right here, edits the game in the student's stead («Редагувати», T282 Б: the
// history signs it with the teacher's name) and pages through the list they came from
const route = useRoute()
const nick = computed(() => route.params.nick)  // paging keeps the page and changes the nick
const data = ref(null)
const wide = wideOf('game').on
useTitle(() => data.value?.student.name)
const admin = computed(() => user.value?.status === 'admin')
// one's own game is edited in «Моя гра», a fellow teacher's is theirs
const canEdit = computed(() => admin.value && data.value?.game && !data.value.mine && data.value.student.status !== 'admin')
const editor = computed(() => !!data.value?.game && editing.value === nick.value)
const reload = async () => {
  const n = nick.value
  const d = await getStudentGame(n)
  if (n === nick.value) data.value = d  // paged on meanwhile: the answer is about the page before
}

watch(nick, (n) => {
  if (!n) return  // on the way out of the page
  data.value = null
  reload()
})
onMounted(async () => {
  loadCatalog()
  await reload()
})
</script>

<template>
  <div>
    <!-- on the whole window (GameEditor's toggle) only the description widens: the head keeps the page column -->
    <div :class="{ 'in-column': wide }">
    <Crumbs :items="studentsCrumbs(data?.student.name || nick)">
      <button v-if="admin && data && data.student.status !== 'admin'" class="btn btn-outline-secondary btn-sm ms-auto"
              :title="data.student.test ? 'Його «Моя гра» — з редагуванням' : 'Його «Моя гра» — лише перегляд'" @click="lookAs(nick, '/my/game')"><Icon name="eye" /> Очима студента</button>
      <RouterLink v-if="admin" :to="{ path: '/activity', query: { user: nick } }" class="btn btn-outline-secondary btn-sm"><Icon name="chart" /> Активність</RouterLink>
    </Crumbs>
    <StudentPager v-if="admin" :nick />
    <p v-if="data && !data.game" class="text-center mt-5 text-secondary">Гру ще не обрано.</p>
    </div>

    <template v-if="data?.game">
      <div :class="{ 'in-column': wide }">
      <GameHead :game="data.game" :student="data.student">
        <RouterLink v-if="data.mine" to="/my/game" class="ms-auto small text-nowrap"><Icon name="pencil" /> Редагувати в «Моїй грі»</RouterLink>
        <button v-if="canEdit && !editor" type="button" class="btn btn-sm btn-outline-secondary text-nowrap"
                title="Правити гру за студента: в історії зміни підписані твоїм іменем" @click="setEditing(nick)"><Icon name="pencil" /> Редагувати</button>
        <RouterLink v-if="admin || data.mine" :to="`/students/${nick}/history`" class="small text-nowrap" :class="{ 'ms-auto': !data.mine }"
                    title="Хто що змінював у грі"><Icon name="clock" /> Історія</RouterLink>
      </GameHead>
      <Md v-if="data.game.description" :text="data.game.description" class="mb-3" />
      <div v-if="editor" class="alert box d-flex flex-wrap align-items-center gap-2 py-2 small">
        <span><Icon name="pencil" /> Ти редагуєш гру студента <b>{{ data.student.name }}</b> — правки записуються від твого імені</span>
        <button type="button" class="btn btn-sm btn-outline-secondary ms-auto" @click="setEditing('')">Вийти</button>
      </div>
      </div>
      <GameEditor :key="nick" :game="data.game" :parts="data.parts" :claims="data.claims" :rules="data.rules" :tasks="data.tasks"
                  :coins="data.coins" :videos="data.videos" :editable="editor" :judge="admin && !data.mine" :nick :reload />
    </template>
  </div>
</template>

<style scoped>
.box { border-color: var(--bs-warning-border-subtle); background: color-mix(in srgb, var(--bs-warning-bg-subtle) 55%, var(--bs-body-bg)); }
</style>
