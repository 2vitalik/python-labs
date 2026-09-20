<script setup>
import { onMounted, ref } from 'vue'

import Crumbs from '../components/Crumbs.vue'
import { loadCatalog, zones } from '../catalog.js'

// proposal П1: zone = a RANGE of one color family; neighbour zones get neighbour families,
// border subzones get border hues; gray = code (base craft), fuchsia = support (unlike anything else)
const PLAN = {
  entities: { letter: 'E', family: 'жовтий→зелений→бірюза (46°–172°)', why: 'живе і росте; найємніше сімейство — якраз для 7 підзон', colors: [
    'hsl(46 90% 42%)', 'hsl(66 70% 40%)', 'hsl(88 62% 40%)', 'hsl(112 55% 38%)', 'hsl(135 58% 36%)', 'hsl(158 65% 34%)', 'hsl(172 70% 33%)'] },
  'game-logic': { letter: 'L', family: 'блакитний→синій→індиго (190°–258°)', why: 'найбільша зона (9) — другий за ємністю діапазон; межа з фіолетовими Рівнями', colors: [
    'hsl(190 75% 36%)', 'hsl(200 80% 42%)', 'hsl(209 85% 48%)', 'hsl(218 75% 52%)', 'hsl(226 70% 46%)', 'hsl(234 65% 55%)', 'hsl(242 60% 48%)', 'hsl(250 62% 58%)', 'hsl(258 65% 50%)'] },
  levels: { letter: 'R', family: 'фіолетовий→пурпур (266°–315°)', why: 'сусід Логіки (твоя ідея «синій+фіолетовий поруч»)', colors: [
    'hsl(266 60% 48%)', 'hsl(276 62% 42%)', 'hsl(286 65% 46%)', 'hsl(296 60% 40%)', 'hsl(306 65% 44%)', 'hsl(315 68% 46%)'] },
  interface: { letter: 'I', family: 'червоний→помаранч→беж (350°–40°)', why: 'дизайн = теплий червоний; беж — легальний член цього сімейства (I8)', colors: [
    'hsl(350 72% 46%)', 'hsl(0 75% 50%)', 'hsl(9 78% 47%)', 'hsl(18 80% 45%)', 'hsl(27 84% 44%)', 'hsl(35 75% 46%)', 'hsl(40 62% 50%)', 'hsl(30 40% 56%)'] },
  code: { letter: 'C', family: 'сірий (5 світлостей, легка синь)', why: 'базове ремесло — нейтральний; різноманіття світлістю', colors: [
    'hsl(220 12% 22%)', 'hsl(220 10% 35%)', 'hsl(220 9% 47%)', 'hsl(220 8% 58%)', 'hsl(220 10% 68%)'] },
  support: { letter: 'S', family: 'фуксія/маджента (322°–342°)', why: 'маленька зона — «особливий» колір, якого нема ніде', colors: [
    'hsl(322 70% 45%)', 'hsl(332 75% 50%)', 'hsl(342 70% 55%)'] },
}
const CAPACITY = [
  'зелений (жовтозел→бірюза): 7–8 чітко різних — найємніший',
  'синій (блакить→індиго): 6–7', 'червоний (з помаранчем і бежем): 6–7',
  'фіолетовий: 5–6', 'фуксія/рожевий: 3–4',
  'чистий жовтий: 2–3 (швидко стає оливою/бежем) — тому жовтий не окрема зона, а край зеленого',
  'сірий: 4–5 світлостей',
]
const copied = ref('')
const copy = (label, css) => { navigator.clipboard?.writeText(css); copied.value = label }

onMounted(loadCatalog)
</script>

<template>
  <Crumbs :items="['Кольори v2']" />
  <h1 class="h3">Кольори v2 <span class="text-secondary fs-6">пропозиція П1: зона = діапазон сімейства</span></h1>
  <p class="text-secondary mb-1">Принципи: сусідні зони — сусідні сімейства (Логіка↔Рівні на межі синього/фіолетового);
    межові підзони беруть крайні відтінки; Код — сірий; Супровід — фуксія, якої нема ніде більше.
    Клік копіює css. Відповідь — кодами: «I3 не туди» чи «E: помінять місцями E1 і E4». {{ copied ? `Скопійовано: ${copied}` : '' }}</p>
  <p class="small text-secondary">Ігрова майстерня з усіма варіаціями — на <RouterLink to="/colors">/colors</RouterLink>.</p>

  <h2 class="h6 mt-3">Ємність сімейств (скільки «прям різних» відтінків тримає)</h2>
  <ul class="small text-secondary">
    <li v-for="c in CAPACITY" :key="c">{{ c }}</li>
  </ul>

  <div v-for="(z, zk) in zones" :key="zk" class="mb-4">
    <h2 class="h6 mb-1">{{ z.icon }} {{ z.title }}
      <span class="text-secondary fw-normal small">— {{ PLAN[zk].family }} · {{ PLAN[zk].why }}</span>
    </h2>
    <div class="d-flex flex-wrap gap-2">
      <div v-for="([st, si], sk, i) in z.subzones" :key="sk" class="tile" :style="{ background: PLAN[zk].colors[i] }"
           role="button" :title="PLAN[zk].colors[i]" @click="copy(`${PLAN[zk].letter}${i + 1}`, PLAN[zk].colors[i])">
        <b>{{ PLAN[zk].letter }}{{ i + 1 }}</b> {{ si }} {{ st }}
      </div>
    </div>
  </div>
</template>

<style scoped>
.tile { color: #fff; border-radius: .35rem; padding: .45rem .6rem; font-size: .85rem; user-select: none; }
</style>
