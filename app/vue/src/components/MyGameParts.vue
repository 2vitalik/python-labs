<script setup>
import { computed, onMounted, ref } from 'vue'

import { getStudentGame, postClaim, postPart } from '../api.js'
import ClaimPicker from './ClaimPicker.vue'
import ClaimRow from './ClaimRow.vue'
import EntityCard from './EntityCard.vue'
import GameGraph from './GameGraph.vue'
import MenuCard from './MenuCard.vue'
import RuleRow from './RuleRow.vue'
import WindowCard from './WindowCard.vue'
import { ROLES, tasks } from '../catalog.js'

// the insides of «Моя гра» — windows, menus, the map, entities, rules, game-level claims: the pilot's editor (T93, T101),
// the admin's only while the mechanism is hidden from students (T216)
const props = defineProps({ game: { type: Object, required: true } })
const parts = ref([])
const claims = ref([])
const rules = ref([])
const newWin = ref(null)
const newEnt = ref(null)
const newRule = ref(false)
const error = ref('')

const infoMap = computed(() => Object.fromEntries(tasks.value.map((t) => [t.slug, t])))
const info = (slug) => infoMap.value[slug]
const windows = computed(() => parts.value.filter((p) => p.kind === 'window'))
const menus = computed(() => parts.value.filter((p) => p.kind === 'menu'))
const entities = computed(() => parts.value.filter((p) => p.kind === 'entity'))
const windowTypes = computed(() => tasks.value.filter((t) => t.tags.includes('window')))
const gameClaims = computed(() => claims.value.filter((c) => !c.part))
const claimsOf = (id) => claims.value.filter((c) => c.part === id)
const nick = computed(() => props.game.owner.split('@')[0])

async function reload() {
  const full = await getStudentGame(nick.value)
  parts.value = full.parts
  claims.value = full.claims
  rules.value = full.rules
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
const addGameClaim = (task, params) => run(() => postClaim({ task, params }))
async function addEntity() {
  error.value = ''
  try {
    await postPart({ kind: 'entity', ...newEnt.value })
    newEnt.value = null
    await reload()
  } catch (e) {
    error.value = e.message
  }
}
const onRuleSaved = () => { newRule.value = false; reload() }
const scrollTo = (id) => document.getElementById(`p-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })

onMounted(reload)
</script>

<template>
  <div>
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

    <h2 class="h5 mt-4">Сутності <span class="count">({{ entities.length }})</span></h2>
    <p class="text-secondary small mb-2">Мешканці ігрового поля: гравець, вороги, предмети, стіни. Механіки заявляються прямо на сутності.</p>
    <div class="row g-3">
      <div v-for="p in entities" :id="`p-${p.id}`" :key="p.id" class="col-md-6">
        <EntityCard :part="p" :claims="claimsOf(p.id)" :info="info" @changed="reload" />
      </div>
    </div>
    <div v-if="newEnt" class="card mt-3">
      <div class="card-body d-flex gap-2 flex-wrap align-items-center">
        <select v-model="newEnt.role" class="form-select w-auto">
          <option value="">Роль…</option>
          <option v-for="(r, k) in ROLES" :key="k" :value="k">{{ r.icon }} {{ r.label }}</option>
        </select>
        <input v-model="newEnt.title" class="form-control w-auto flex-grow-1" placeholder="Назва сутності (Гравець, Ворожий танк…)">
        <button class="btn btn-primary" :disabled="!newEnt.role || !newEnt.title.trim()" @click="addEntity">Додати</button>
        <button class="btn btn-outline-secondary" @click="newEnt = null">✕</button>
      </div>
    </div>
    <button v-else class="btn btn-outline-primary btn-sm mt-3" @click="newEnt = { role: '', title: '' }">＋ сутність</button>

    <h2 class="h5 mt-4">Правила <span class="count">({{ rules.length }})</span></h2>
    <p class="text-secondary small mb-2">Правило — речення «КОЛИ → ТО»: контакт сутностей чи таймер, і що стається.</p>
    <div class="vstack gap-1">
      <RuleRow v-for="r in rules" :key="r.id" :rule="r" :parts="parts" editable @changed="reload" />
      <RuleRow v-if="newRule" :rule="null" :parts="parts" editable @changed="onRuleSaved" @cancel="newRule = false" />
    </div>
    <button v-if="!newRule" class="btn btn-outline-primary btn-sm mt-2" :disabled="!entities.length"
            :title="entities.length ? '' : 'Спершу додай сутності'" @click="newRule = true">＋ правило</button>

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
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; font-size: 1rem; }
</style>
