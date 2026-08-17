<script setup>
import { computed, onMounted, ref } from 'vue'

import { getMyGame, getStudentGame, postClaim, postPart } from '../api.js'
import ClaimPicker from '../components/ClaimPicker.vue'
import ClaimRow from '../components/ClaimRow.vue'
import GameGraph from '../components/GameGraph.vue'
import Md from '../components/Md.vue'
import MenuCard from '../components/MenuCard.vue'
import MyGameForm from '../components/MyGameForm.vue'
import WindowCard from '../components/WindowCard.vue'
import { games, loadCatalog, tasks } from '../catalog.js'

const game = ref(null)
const parts = ref([])
const claims = ref([])
const loaded = ref(false)
const denied = ref(false)
const editGame = ref(false)
const newWin = ref(null)
const error = ref('')

const infoMap = computed(() => Object.fromEntries(tasks.value.map((t) => [t.slug, t])))
const info = (slug) => infoMap.value[slug]
const windows = computed(() => parts.value.filter((p) => p.kind === 'window'))
const menus = computed(() => parts.value.filter((p) => p.kind === 'menu'))
const windowTypes = computed(() => tasks.value.filter((t) => t.tags.includes('window')))
const gameClaims = computed(() => claims.value.filter((c) => !c.part))
const claimsOf = (id) => claims.value.filter((c) => c.part === id)
const nick = computed(() => game.value?.owner.split('@')[0])
const baseTitle = computed(() => games.value.find((g) => g.slug === game.value?.base_game)?.title)

async function reload() {
  try {
    game.value = await getMyGame()
  } catch {
    denied.value = true
    loaded.value = true
    return
  }
  if (game.value) {
    const full = await getStudentGame(nick.value)
    parts.value = full.parts
    claims.value = full.claims
  }
  loaded.value = true
}

function onSaved(g) {
  game.value = g
  editGame.value = false
}

async function run(fn) {
  error.value = ''
  try {
    await fn()
    await reload()
  } catch (e) {
    error.value = e.message
  }
}

async function addWindow() {
  error.value = ''
  try {
    await postPart({ kind: 'window', ...newWin.value })
    newWin.value = null
    await reload()
  } catch (e) {
    error.value = e.message
  }
}
const addMenu = () => run(() => postPart({ kind: 'menu', title: 'Нове меню' }))
const addGameClaim = (task) => run(() => postClaim({ task }))
const scrollTo = (id) => document.getElementById(`p-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })

onMounted(() => Promise.all([loadCatalog(), reload()]))
</script>

<template>
  <div class="col-lg-10 mx-auto">
    <p v-if="denied" class="text-center mt-5">Сторінка для учасників курсу — увійди з поштою @nure.ua.</p>

    <template v-else-if="loaded && !game">
      <h1 class="h3 mb-2">Моя гра</h1>
      <p class="text-secondary">Створи свою гру — а далі описуй її вікна, меню і заявляй виконані картки з каталогу.</p>
      <MyGameForm @saved="onSaved" />
    </template>

    <template v-else-if="game">
      <div class="d-flex align-items-center gap-2 mb-1">
        <h1 class="h3 mb-0">{{ game.title }}</h1>
        <span class="badge text-bg-light border text-secondary fw-normal">
          основа:
          <RouterLink v-if="game.base_game" :to="`/games/${game.base_game}`">{{ baseTitle || game.base_game }}</RouterLink>
          <template v-else>{{ game.base_custom }}</template>
        </span>
        <span role="button" title="Редагувати гру" @click="editGame = !editGame">✏️</span>
        <RouterLink :to="`/students/${nick}`" class="ms-auto small">Як це бачать інші →</RouterLink>
      </div>
      <MyGameForm v-if="editGame" :game="game" class="mb-3" @saved="onSaved" />
      <Md v-else-if="game.description" :text="game.description" class="text-secondary mb-3" />

      <h2 class="h5 mt-4">Вікна <span class="count">({{ windows.length }})</span></h2>
      <div class="row g-3">
        <div v-for="p in windows" :id="`p-${p.id}`" :key="p.id" class="col-md-6">
          <WindowCard :part="p" :claims="claimsOf(p.id)" :game-claims="gameClaims" :info="info" @changed="reload" />
        </div>
      </div>
      <div v-if="newWin" class="card mt-3">
        <div class="card-body d-flex gap-2 flex-wrap align-items-center">
          <select v-model="newWin.task" class="form-select w-auto">
            <option value="">Тип вікна…</option>
            <option v-for="t in windowTypes" :key="t.slug" :value="t.slug">{{ t.title }}</option>
          </select>
          <input v-model="newWin.title" class="form-control w-auto flex-grow-1" placeholder="Назва вікна у твоїй грі">
          <button class="btn btn-primary" :disabled="!newWin.task || !newWin.title.trim()" @click="addWindow">Додати</button>
          <button class="btn btn-outline-secondary" @click="newWin = null">✕</button>
        </div>
      </div>
      <button v-else class="btn btn-outline-primary btn-sm mt-3" @click="newWin = { task: '', title: '' }">＋ вікно</button>

      <h2 class="h5 mt-4">Меню <span class="count">({{ menus.length }})</span></h2>
      <p class="text-secondary small mb-2">Пункт меню може вести на вікно або на картку-функцію; порожні цілі — просто текст.</p>
      <div class="vstack gap-3">
        <MenuCard v-for="p in menus" :key="p.id" :part="p" :windows="windows"
                  :claims="claimsOf(p.id)" :info="info" @changed="reload" />
      </div>
      <button class="btn btn-outline-primary btn-sm mt-2" @click="addMenu">＋ меню</button>

      <template v-if="windows.length">
        <h2 class="h5 mt-4">Карта переходів</h2>
        <div class="card">
          <div class="card-body p-2">
            <GameGraph :windows="windows" :menus="menus" @pick="scrollTo" />
          </div>
        </div>
      </template>

      <h2 class="h5 mt-4">Заявки рівня гри <span class="count">({{ gameClaims.length }})</span></h2>
      <p class="text-secondary small mb-2">Механіки й функції, не привʼязані до конкретного вікна.</p>
      <div v-if="gameClaims.length" class="d-flex flex-wrap gap-1 align-items-start mb-2">
        <ClaimRow v-for="c in gameClaims" :key="c.id" :claim="c" :info="info(c.task)" @changed="reload" />
      </div>
      <div class="col-md-6"><ClaimPicker @pick="addGameClaim" /></div>

      <datalist id="task-cards">
        <option v-for="t in tasks" :key="t.slug" :value="t.slug">{{ t.title }}</option>
      </datalist>
      <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    </template>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; font-size: 1rem; }
</style>
