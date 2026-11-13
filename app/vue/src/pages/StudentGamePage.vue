<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudentGame } from '../api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GameEditor from '../components/GameEditor.vue'
import GameHead from '../components/GameHead.vue'
import Md from '../components/Md.vue'
import { loadCatalog } from '../catalog.js'
import { studentsCrumbs } from '@core/students.js'
import { useTitle } from '@core/title.js'
import { lookAs, user } from '@core/user.js'

// a student's game as others see it — the passport: head, description, then the same sections as the editor, read-only;
// the teacher accepts or returns claims right here
const nick = useRoute().params.nick
const data = ref(null)
useTitle(() => data.value?.student.name)
const admin = computed(() => user.value?.status === 'admin')
const reload = async () => (data.value = await getStudentGame(nick))

onMounted(async () => {
  loadCatalog()
  await reload()
})
</script>

<template>
  <div>
    <Crumbs :items="studentsCrumbs(data?.student.name || nick)">
      <button v-if="admin && data && data.student.status !== 'admin'" class="btn btn-outline-secondary btn-sm ms-auto"
              :title="data.student.test ? 'Його «Моя гра» — з редагуванням' : 'Його «Моя гра» — лише перегляд'" @click="lookAs(nick, '/my/game')">👁 Очима студента</button>
      <RouterLink v-if="admin" :to="{ path: '/activity', query: { user: nick } }" class="btn btn-outline-secondary btn-sm">📈 Активність</RouterLink>
    </Crumbs>
    <p v-if="data && !data.game" class="text-center mt-5 text-secondary">Гру ще не обрано.</p>

    <template v-else-if="data">
      <GameHead :game="data.game" :student="data.student">
        <RouterLink v-if="data.mine" to="/my/game" class="ms-auto small text-nowrap">✏️ Редагувати в «Моїй грі»</RouterLink>
        <RouterLink v-if="admin || data.mine" :to="`/students/${nick}/history`" class="small text-nowrap" :class="{ 'ms-auto': !data.mine }"
                    title="Хто що змінював у грі">🕘 Історія</RouterLink>
      </GameHead>
      <Md v-if="data.game.description" :text="data.game.description" class="mb-3" />
      <GameEditor :game="data.game" :parts="data.parts" :claims="data.claims" :rules="data.rules" :tasks="data.tasks" :coins="data.coins"
                  :judge="admin && !data.mine" :nick :reload />
    </template>
  </div>
</template>
