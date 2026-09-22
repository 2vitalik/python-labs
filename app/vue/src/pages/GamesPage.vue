<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import GameCard from '../components/GameCard.vue'
import Crumbs from '../components/Crumbs.vue'
import GuideHead from '../components/GuideHead.vue'
import Toc from '../components/Toc.vue'
import { games, KLASSES, loadCatalog } from '../catalog.js'
import { canAccess, user } from '../user.js'

const router = useRouter()
const admin = computed(() => user.value?.status === 'admin')
const myGame = computed(() => canAccess(router.resolve('/my/game').meta.access))  // at hand: on a phone the menu hides it in «Ще»
const klass = ref('')
const shown = computed(() => games.value.filter((g) => !klass.value || g.klass === klass.value))
const toc = ref([])

onMounted(() => admin.value && loadCatalog())
</script>

<template>
  <div>
    <Crumbs :items="[['/method', 'Методичка'], 'Ігри']">
      <RouterLink v-if="myGame" to="/my/game" class="btn btn-outline-primary btn-sm">Моя гра</RouterLink>
    </Crumbs>
    <GuideHead slug="game" stub="Каталог базових ігор відкриється тут незабаром. Поки що — варіанти перелічені вище; вибір обговорюємо на парі або в чаті."
               @toc="toc = $event" />
    <template v-if="admin">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h1 class="h3 mb-0">Ігри <span class="text-secondary fs-6">({{ shown.length }})</span></h1>
        <div class="d-flex gap-2">
          <RouterLink to="/ideas" class="btn btn-outline-secondary btn-sm">💡 Знахідки</RouterLink>
          <RouterLink to="/games/new" class="btn btn-outline-primary btn-sm">➕ Нова гра</RouterLink>
        </div>
      </div>

      <div class="mb-3 d-flex gap-2 flex-wrap">
        <button class="btn btn-sm" :class="klass === '' ? 'btn-primary' : 'btn-outline-secondary'" @click="klass = ''">всі</button>
        <button v-for="(label, k) in KLASSES" :key="k" class="btn btn-sm"
                :class="klass === k ? 'btn-primary' : 'btn-outline-secondary'" @click="klass = k">{{ label }}</button>
      </div>

      <div class="row g-3">
        <div v-for="g in shown" :key="g.id" class="col-md-6 col-lg-4"><GameCard :game="g" /></div>
      </div>
    </template>
    <Toc :items="toc" />
  </div>
</template>
