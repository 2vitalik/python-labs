<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import GuideText from '@core/components/GuideText.vue'
import Icon from '@core/components/Icon.vue'
import { getEtalon } from '../api.js'
import GameMoments from '../components/GameMoments.vue'
import GameSample from '../components/GameSample.vue'
import TaskCatalog from '../components/TaskCatalog.vue'
import { AXES, games, KLASSES, loadCatalog, STATUSES } from '../catalog.js'
import { isFolded, toggleFold } from '../fold.js'
import { problem } from '@core/problem.js'
import { useTaskFilter } from '../taskFilter.js'
import { useTitle } from '@core/title.js'
import { user } from '@core/user.js'

const slug = useRoute().params.slug
const game = computed(() => games.value.find((g) => g.slug === slug))
useTitle(() => game.value?.title)
const FRAMED = /```field[^`]*[[(]/  // a grid with a marked cell: only then the frames need explaining
const examples = computed(() => {
  const e = game.value.examples
  return e && [...(FRAMED.test(e) ? ['Синя рамка — хто щойно зробив хід, жовта — що змінилось на полі.'] : []), e].join('\n\n')
})
const { grouped } = useTaskFilter(slug)
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))

const SHOW_TASKS = false  // «Завдання гри» hidden until the catalog has enough per-game cards (T125 п. 44)
const etalon = ref(null)  // the classic version described the way students describe theirs; absent for a base without one

onMounted(async () => {
  await loadCatalog()
  if (!game.value) problem.value = 'lost'
  else getEtalon(slug).then((d) => (etalon.value = d), () => {})
})
</script>

<template>
  <div v-if="game">
    <Crumbs :items="[['/method', 'Методичка'], ['/games', 'Ігри'], game.title]" />
    <div class="d-flex align-items-center gap-2 mb-1">
      <span class="fs-2">{{ game.icon }}</span>
      <h1 class="h3 mb-0">{{ game.title }}</h1>
      <span v-if="game.status !== 'active'" class="badge text-bg-light border text-secondary fw-normal">{{ STATUSES[game.status] }}</span>
      <RouterLink v-if="user?.status === 'admin'" :to="`/games/${game.slug}/edit`"
                  class="ms-auto text-decoration-none" title="Редагувати">✏️</RouterLink>
      <RouterLink v-if="user?.status === 'admin'" :to="`/games/history?slug=${game.slug}`"
                  class="text-decoration-none" title="Історія правок">🕘</RouterLink>
    </div>
    <p class="text-secondary">{{ game.summary }}</p>
    <p class="d-flex gap-2 flex-wrap">
      <span class="badge text-bg-primary">{{ KLASSES[game.klass] }}</span>
      <span v-for="(v, k) in game.axes" :key="k" class="badge text-bg-light border text-dark fw-normal">{{ AXES[k] }}: {{ v }}</span>
    </p>

    <!-- each block folds by its heading, and stays so on the next visit (T274 §8) -->
    <template v-if="game.description">
      <h2 id="about" class="h4 head"><button type="button" class="fold" @click="toggleFold('game:about')">
        <Icon :name="isFolded('game:about') ? 'right' : 'down'" class="chev" /> Про гру</button></h2>
      <GuideText v-show="!isFolded('game:about')" :text="game.description" class="mb-4" />
    </template>

    <template v-if="examples">
      <h2 id="examples" class="h4 head"><button type="button" class="fold" @click="toggleFold('game:examples')">
        <Icon :name="isFolded('game:examples') ? 'right' : 'down'" class="chev" /> Приклади ігрових ситуацій</button></h2>
      <GameMoments v-show="!isFolded('game:examples')" :text="examples" class="mb-4" />
    </template>

    <template v-if="etalon">
      <h2 id="etalon" class="h4 head"><button type="button" class="fold" @click="toggleFold('game:etalon')">
        <Icon :name="isFolded('game:etalon') ? 'right' : 'down'" class="chev" /> Як описати цю гру — зразок</button></h2>
      <div v-show="!isFolded('game:etalon')">
        <p class="text-secondary small">
          Так виглядає опис класичної версії в «Моїй грі»: поле, рівні, сутності, правила, вікна, картки каталогу. Це зразок — тут нічого
          не зберігається. Свій опис робиш у <RouterLink to="/my/game">«Моїй грі»</RouterLink>: на цій основі кнопка «Почати з еталона»
          скопіює зразок тобі, далі викреслюєш зайве й додаєш своє.
        </p>
        <GameSample :slug :etalon />
      </div>
    </template>

    <template v-if="SHOW_TASKS">
      <h2 id="catalog" class="h5">Завдання гри <span class="count fs-6">({{ shown }})</span></h2>
      <p class="text-secondary small">Лише специфічні для цієї гри; універсальні — у <RouterLink to="/tasks?game=universal">каталозі</RouterLink>.</p>
      <TaskCatalog :game="slug" />
    </template>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; }
.head { margin-top: 1.5rem; scroll-margin-top: 1rem; }
.fold { padding: 0; border: 0; background: none; color: inherit; font: inherit; text-align: start; }
.fold .chev { font-size: .8em; opacity: .55; }
.fold:hover .chev { opacity: 1; }
#catalog { scroll-margin-top: 1rem; }
</style>
