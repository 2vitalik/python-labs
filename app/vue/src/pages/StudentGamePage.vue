<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import { getStudentGame } from '../api.js'
import CoinBadge from '../components/CoinBadge.vue'
import Crumbs from '@core/components/Crumbs.vue'
import GameGraph from '../components/GameGraph.vue'
import GameHead from '../components/GameHead.vue'
import Md from '../components/Md.vue'
import RuleRow from '../components/RuleRow.vue'
import { COINS, ROLES, loadCatalog, paramsText } from '../catalog.js'
import { studentsCrumbs } from '@core/students.js'
import { useTitle } from '@core/title.js'
import { lookAs, user } from '@core/user.js'

// a student's game as others see it: the head and the description for everyone; the insides — map, windows, menus,
// entities, rules, claims — the admin's only while the mechanism is hidden from students (T216)
const nick = useRoute().params.nick
const data = ref(null)
useTitle(() => data.value?.student.name)
const full = computed(() => user.value?.status === 'admin')
const COIN_ORDER = ['crown', 'gold', 'silver', 'bronze', 'tin', 'wood']

const windows = computed(() => data.value.parts.filter((p) => p.kind === 'window'))
const menus = computed(() => data.value.parts.filter((p) => p.kind === 'menu'))
const entities = computed(() => data.value.parts.filter((p) => p.kind === 'entity'))
const claimsOf = (id) => data.value.claims.filter((c) => c.part === id && c.task !== partById(id)?.task)
const gameClaims = computed(() => data.value.claims.filter((c) => !c.part))
const partById = (id) => data.value.parts.find((p) => p.id === id)
const card = (slug) => data.value.tasks[slug]
const ptext = (c) => paramsText(card(c.task), c.params)
// claimed coins by type — informational, no grading math yet
const coinSum = computed(() => {
  const n = {}
  for (const c of data.value.claims) {
    const t = card(c.task)
    if (t?.coin) n[t.coin] = (n[t.coin] || 0) + (t.amount || 1)
  }
  return COIN_ORDER.filter((k) => n[k]).map((k) => ({ coin: k, n: n[k] }))
})
const scrollTo = (id) => document.getElementById(`p-${id}`)?.scrollIntoView({ behavior: 'smooth', block: 'center' })

onMounted(async () => {
  loadCatalog()
  data.value = await getStudentGame(nick)
})
</script>

<template>
  <div>
    <Crumbs :items="studentsCrumbs(data?.student.name || nick)">
      <button v-if="full && data && data.student.status !== 'admin'" class="btn btn-outline-secondary btn-sm ms-auto"
              :title="data.student.test ? null : 'Лише перегляд'" @click="lookAs(nick)">👁 Очима студента</button>
      <RouterLink v-if="full" :to="{ path: '/activity', query: { user: nick } }" class="btn btn-outline-secondary btn-sm">📈 Активність</RouterLink>
    </Crumbs>
    <p v-if="data && !data.game" class="text-center mt-5 text-secondary">Гру ще не обрано.</p>

    <template v-else-if="data">
      <GameHead :game="data.game" :student="data.student">
        <RouterLink v-if="data.mine" to="/my/game" class="ms-auto small">✏️ Редагувати в «Моїй грі»</RouterLink>
      </GameHead>
      <Md v-if="data.game.description" :text="data.game.description" class="mb-4" />
    </template>

    <template v-if="data?.game && full">
      <p class="text-secondary small">
        вікон: {{ windows.length }} · меню: {{ menus.length }} · сутностей: {{ entities.length }} ·
        правил: {{ data.rules.length }} · заявок: {{ data.claims.length }}
        <span v-if="coinSum.length" title="Заявлено монеток — довідково, без зарахування">
          · <span v-for="c in coinSum" :key="c.coin" class="text-nowrap"> {{ COINS[c.coin] }}×{{ c.n }}</span>
        </span>
      </p>

      <template v-if="windows.length">
        <h2 class="h5">Карта переходів</h2>
        <div class="card mb-4">
          <div class="card-body p-2">
            <GameGraph :windows="windows" :menus="menus" @pick="scrollTo" />
          </div>
        </div>
      </template>

      <h2 v-if="windows.length" class="h5">Вікна</h2>
      <div class="row g-3 mb-4">
        <div v-for="p in windows" :id="`p-${p.id}`" :key="p.id" class="col-md-6">
          <div class="card h-100">
            <div class="card-body vstack gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fw-semibold">{{ p.title }}</span>
                <span class="badge text-bg-light border text-secondary fw-normal">
                  <CoinBadge :coin="card(p.task)?.coin" :amount="card(p.task)?.amount" /> {{ card(p.task)?.title || p.task }}
                </span>
              </div>
              <div v-if="p.description" class="text-secondary small">{{ p.description }}</div>
              <div v-if="p.screenshots.length" class="d-flex flex-wrap gap-2">
                <a v-for="s in p.screenshots" :key="s" :href="`/api/uploads/${p.game}/${s}`" target="_blank">
                  <img :src="`/api/uploads/${p.game}/${s}`" class="rounded border shot">
                </a>
              </div>
              <div v-if="claimsOf(p.id).length" class="d-flex flex-wrap gap-1">
                <span v-for="c in claimsOf(p.id)" :key="c.id" :title="c.note"
                      class="badge rounded-pill text-bg-light border text-dark fw-normal">
                  <CoinBadge :coin="card(c.task)?.coin" :amount="card(c.task)?.amount" /> {{ card(c.task)?.title || c.task }}
                  <span v-if="ptext(c)" class="text-secondary">· {{ ptext(c) }}</span>
                  <a v-if="c.link" :href="c.link" target="_blank" class="text-decoration-none">🔗</a>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <h2 v-if="menus.length" class="h5">Меню</h2>
      <div class="row g-3 mb-4">
        <div v-for="p in menus" :key="p.id" class="col-md-6">
          <div class="card h-100">
            <div class="card-body vstack gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fw-semibold">{{ p.title }}</span>
                <span v-if="p.window" class="text-secondary small">на вікні «{{ partById(p.window)?.title }}»</span>
              </div>
              <ul class="mb-0 ps-4">
                <li v-for="(it, i) in p.items" :key="i">
                  {{ it.title }}
                  <span v-if="it.window" class="text-secondary">→ вікно «{{ partById(it.window)?.title }}»</span>
                  <span v-else-if="it.task" class="text-secondary">→ {{ card(it.task)?.title || it.task }}</span>
                  <span v-if="it.note" class="text-secondary small">· {{ it.note }}</span>
                </li>
              </ul>
              <div v-if="p.screenshots.length" class="d-flex flex-wrap gap-2">
                <a v-for="s in p.screenshots" :key="s" :href="`/api/uploads/${p.game}/${s}`" target="_blank">
                  <img :src="`/api/uploads/${p.game}/${s}`" class="rounded border shot">
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>

      <h2 v-if="entities.length" class="h5">Сутності</h2>
      <div v-if="entities.length" class="row g-3 mb-4">
        <div v-for="p in entities" :key="p.id" class="col-md-6">
          <div class="card h-100">
            <div class="card-body vstack gap-2">
              <div class="d-flex align-items-center gap-2">
                <span class="fw-semibold">{{ ROLES[p.role]?.icon }} {{ p.title }}</span>
                <span class="badge text-bg-light border text-secondary fw-normal">{{ ROLES[p.role]?.label || p.role }}</span>
              </div>
              <div v-if="p.description" class="text-secondary small">{{ p.description }}</div>
              <div v-if="p.screenshots.length" class="d-flex flex-wrap gap-2">
                <a v-for="s in p.screenshots" :key="s" :href="`/api/uploads/${p.game}/${s}`" target="_blank">
                  <img :src="`/api/uploads/${p.game}/${s}`" class="rounded border shot">
                </a>
              </div>
              <div v-if="claimsOf(p.id).length" class="d-flex flex-wrap gap-1">
                <span v-for="c in claimsOf(p.id)" :key="c.id" :title="c.note"
                      class="badge rounded-pill text-bg-light border text-dark fw-normal">
                  <CoinBadge :coin="card(c.task)?.coin" :amount="card(c.task)?.amount" /> {{ card(c.task)?.title || c.task }}
                  <span v-if="ptext(c)" class="text-secondary">· {{ ptext(c) }}</span>
                  <a v-if="c.link" :href="c.link" target="_blank" class="text-decoration-none">🔗</a>
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <h2 v-if="data.rules.length" class="h5">Правила</h2>
      <div v-if="data.rules.length" class="vstack gap-1 mb-4">
        <RuleRow v-for="r in data.rules" :key="r.id" :rule="r" :parts="data.parts" />
      </div>

      <h2 v-if="gameClaims.length" class="h5">Заявки рівня гри</h2>
      <div class="d-flex flex-wrap gap-1">
        <span v-for="c in gameClaims" :key="c.id" :title="c.note"
              class="badge rounded-pill text-bg-light border text-dark fw-normal">
          <CoinBadge :coin="card(c.task)?.coin" :amount="card(c.task)?.amount" /> {{ card(c.task)?.title || c.task }}
          <span v-if="ptext(c)" class="text-secondary">· {{ ptext(c) }}</span>
          <a v-if="c.link" :href="c.link" target="_blank" class="text-decoration-none">🔗</a>
        </span>
      </div>
    </template>
  </div>
</template>

<style scoped>
.shot { height: 110px; }
</style>
