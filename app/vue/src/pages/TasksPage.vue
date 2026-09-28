<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import Crumbs from '../components/Crumbs.vue'
import GuideHead from '../components/GuideHead.vue'
import IconArrows from '../components/IconArrows.vue'
import TaskCatalog from '../components/TaskCatalog.vue'
import Toc from '../components/Toc.vue'
import { games, loadCatalog } from '../catalog.js'
import { useTaskFilter } from '../taskFilter.js'
import { canAccess, user } from '../user.js'
import { toggleWide, wide, wideOn } from '../wide.js'

const router = useRouter()
const admin = computed(() => user.value?.status === 'admin')
const myGame = computed(() => canAccess(router.resolve('/my/game').meta.access))
const { f, set, grouped } = useTaskFilter()
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))
// side contents in page order: the guide text's headings while it is open and the zones on screen
const guideToc = ref([])
const low = ref(false)
const toc = computed(() => {
  const zones = grouped.value.map((z) => ({ id: `zone-${z.key}`, text: `${z.icon} ${z.title}`, depth: 2 }))
  const both = guideToc.value.length && zones.length
  return low.value
    ? [...zones, ...(both ? [{ label: 'Методичка' }] : []), ...guideToc.value]
    : [...guideToc.value, ...(both ? [{ label: 'Завдання' }] : []), ...zones]
})

onMounted(() => admin.value && loadCatalog())
</script>

<template>
  <div>
    <!-- wide mode widens the catalog only: crumbs and the guide block keep the page column -->
    <div :class="{ column: wideOn }">
      <Crumbs :items="[['/method', 'Методичка'], 'Таски']">
        <RouterLink v-if="myGame" to="/my/game" class="btn btn-outline-primary btn-sm">Моя гра</RouterLink>
      </Crumbs>
      <GuideHead slug="tasks" stub="Каталог завдань із цінами відкриється тут незабаром — до першої лаби."
                 @toc="guideToc = $event" @low="low = $event" />
    </div>
    <template v-if="admin">
      <!-- min-height: a zone click scrolls the head to the top even when the filtered list is short -->
      <div class="catalog-area">
        <div id="catalog" class="d-flex flex-wrap align-items-center gap-2 mb-2">
          <h1 class="h3 mb-0 me-auto">Завдання <span class="count fs-6">({{ shown }})</span></h1>
          <RouterLink to="/ideas" class="btn btn-outline-secondary btn-sm">💡 Знахідки</RouterLink>
          <RouterLink to="/tasks/new" class="btn btn-outline-primary btn-sm">➕ Нове завдання</RouterLink>
          <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2"
                  :title="wide ? 'Назад у колонку сторінки' : 'Каталог на всю ширину'" @click="toggleWide">
            <IconArrows :out="!wide" />
          </button>
        </div>
        <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
          <input :value="f.q" class="form-control form-control-sm w-auto flex-grow-1" style="max-width: 28rem"
                 placeholder="Пошук: назва, опис, теги…" @input="set({ q: $event.target.value })">
          <select :value="f.game" class="form-select form-select-sm w-auto" @change="set({ game: $event.target.value })">
            <option value="">Всі ігри</option>
            <option value="universal">🌍 Універсальні</option>
            <option v-for="g in games" :key="g.slug" :value="g.slug">{{ g.icon }} {{ g.title }}</option>
          </select>
          <div class="form-check">
            <input id="algo" class="form-check-input" type="checkbox" :checked="f.algo"
                   @change="set({ algo: $event.target.checked ? '1' : '' })">
            <label class="form-check-label" for="algo">⭐ алгоритмічні</label>
          </div>
        </div>
        <TaskCatalog />
      </div>
    </template>
    <div id="guide-low" :class="{ column: wideOn }"></div>
    <Toc v-if="!wideOn" :items="toc" />
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; }
#catalog { scroll-margin-top: 1rem; }
.catalog-area { min-height: 100vh; }
/* the page column without its side padding (the wide container has its own) */
.column { max-width: calc(var(--page-max) - 2rem); margin: 0 auto; }
</style>
