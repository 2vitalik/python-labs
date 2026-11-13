<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getGameHistory, getStudentGame } from '../api.js'
import GameHistoryRow from '../components/GameHistoryRow.vue'
import { PAGE, WHO } from '../gameHistory.js'
import Crumbs from '@core/components/Crumbs.vue'
import { studentsCrumbs } from '@core/students.js'
import { useTitle } from '@core/title.js'
import { user } from '@core/user.js'

// a game's history (T278 §12): every change of the game, its parts, rules and claims — who made it (the student, the teacher,
// an agent), what, how; read-only. /my/game/history — the owner's, /students/:nick/history — the teacher's look at it
const route = useRoute()
const own = computed(() => !route.params.nick)
const nick = computed(() => route.params.nick || user.value?.nick)
const mine = computed(() => nick.value === user.value?.nick)
const back = computed(() => (own.value ? '/my/game' : `/students/${nick.value}`))
const head = ref(null)  // the passport: whose game, its title
const rows = ref(null)  // null — not loaded yet: «Змін ще нема» is not said before the answer
const more = ref(false)
const busy = ref(false)
const error = ref('')
const who = ref('')
const filters = computed(() => WHO.map((w) => ({ ...w, label: (mine.value && w.mine) || w.label })))
const name = computed(() => head.value?.student.name || nick.value)
const crumbs = computed(() => (own.value ? [['/my/game', 'Моя гра'], 'Історія'] : studentsCrumbs([back.value, name.value], 'Історія')))
useTitle(() => head.value?.game && `Історія · ${head.value.game.title}`)

async function load(before) {
  busy.value = true
  try {
    const asked = who.value
    const page = await getGameHistory(nick.value, { limit: PAGE, ...(asked && { who: asked }), ...(before && { before }) })
    if (asked !== who.value) return  // the filter changed meanwhile: its own answer is on the way
    rows.value = before ? [...rows.value, ...page] : page
    more.value = page.length >= PAGE
    error.value = ''
  } catch (e) {
    error.value = e.message
    rows.value ??= []
  }
  busy.value = false
}

watch(nick, (n) => {
  if (!n) return
  rows.value = head.value = null
  load()
  getStudentGame(n).then((d) => (head.value = d), () => {})
}, { immediate: true })
watch(who, () => load())  // the server filters: a rare teacher's row is found at once, not pages down
</script>

<template>
  <div>
    <Crumbs :items="crumbs">
      <RouterLink :to="back" class="btn btn-outline-secondary btn-sm">← до гри</RouterLink>
    </Crumbs>
    <h1 class="h2 mb-3">🕘 Історія гри<span v-if="head?.game" class="text-secondary fs-5"> · {{ head.game.title }}</span></h1>
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <span class="small text-secondary">хто:</span>
      <div class="btn-group btn-group-sm" role="group" aria-label="хто змінював">
        <button v-for="w in filters" :key="w.key" type="button" class="btn btn-outline-secondary" :class="{ active: who === w.key }"
                @click="who = w.key">{{ w.label }}</button>
      </div>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <GameHistoryRow v-for="r in rows || []" :key="r.id" :row="r" />
    <p v-if="rows && !rows.length && !error" class="text-secondary text-center mt-4">{{ who ? 'Таких змін нема.' : 'Змін ще нема.' }}</p>
    <div v-if="more" class="text-center">
      <button class="btn btn-outline-secondary btn-sm" :disabled="busy" @click="load(rows.at(-1).at)">Показати ще</button>
    </div>
  </div>
</template>
