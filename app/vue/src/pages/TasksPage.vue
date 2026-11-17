<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import Icon from '@core/components/Icon.vue'
import GuideHead from '../components/GuideHead.vue'
import IconArrows from '@core/components/IconArrows.vue'
import TaskCatalog from '../components/TaskCatalog.vue'
import TaskFilters from '../components/TaskFilters.vue'
import Toc from '@core/components/Toc.vue'
import { getAsks } from '../api.js'
import { loadCatalog } from '../catalog.js'
import { loadMyGame } from '../myGame.js'
import { useTaskFilter } from '../taskFilter.js'
import { canAccess, user } from '@core/user.js'
import { toggleWide, wide } from '@core/wide.js'

const router = useRouter()
const admin = computed(() => user.value?.status === 'admin')
const myGame = computed(() => canAccess(router.resolve('/my/game').meta.access))
const ideas = computed(() => canAccess(router.resolve('/ideas').meta.access))
const { f, grouped, coreOnly, total } = useTaskFilter()
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))
const asks = ref(null)  // the teacher's: how many cards «за запитом» students added (T319)
watch(admin, (a) => a && asks.value === null && getAsks().then((r) => (asks.value = r.length), () => {}), { immediate: true })
// side contents in page order: the guide text's headings while it is open and the categories on screen — a category chosen
// in the filter gives its subcategories instead; with all of them shown the subcategories stay off the list (`quiet`),
// only the row under the menu names the one being read
const guideToc = ref([])
const low = ref(false)
const toc = computed(() => {
  const one = !!f.value.zone
  const zones = grouped.value.flatMap((z) => [
    ...(one ? [] : [{ id: `zone-${z.key}`, text: `${z.icon} ${z.title}`, depth: 2 }]),
    ...z.subs.map((s) => ({ id: `sub-${z.key}-${s.key}`, text: `${s.icon} ${s.title}`, depth: one ? 2 : 3, quiet: !one })),
  ])
  const both = guideToc.value.length && zones.length
  return low.value
    ? [...zones, ...(both ? [{ label: 'Методичка' }] : []), ...guideToc.value]
    : [...guideToc.value, ...(both ? [{ label: 'Завдання' }] : []), ...zones]
})

onMounted(() => { loadCatalog(); loadMyGame() })  // the student's game lets a card be added from here («＋ у гру»)
</script>

<template>
  <div>
    <!-- wide mode widens the catalog only: crumbs and the guide block keep the page column -->
    <div :class="{ 'in-column': wide }">
      <Crumbs :items="[['/method', 'Методичка'], 'Таски']">
        <RouterLink v-if="myGame" to="/my/game" class="btn btn-outline-primary btn-sm">Моя гра</RouterLink>
      </Crumbs>
      <GuideHead slug="tasks" @toc="guideToc = $event" @low="low = $event" />
    </div>
    <!-- min-height: a zone click scrolls the head to the top even when the filtered list is short -->
    <div class="catalog-area">
      <div id="catalog" class="d-flex flex-wrap align-items-center gap-2 mb-2">
        <h1 class="h3 mb-0 me-auto">Завдання
          <span v-if="coreOnly && total > shown" class="count fs-6" :title="`Основа: ${shown}; ще ${total - shown} — за запитом, під рядком у кінці підкатегорії`">({{ shown }} з {{ total }})</span>
          <span v-else class="count fs-6">({{ shown }})</span>
        </h1>
        <RouterLink v-if="ideas" to="/ideas" class="btn btn-outline-secondary btn-sm">💡 Знахідки</RouterLink>
        <RouterLink v-if="admin" to="/tasks/asks" class="btn btn-outline-secondary btn-sm" title="Картки за запитом, які студенти додали в ігри: найчастіші зверху">
          <Icon name="bell" /> Запити<template v-if="asks !== null"> ({{ asks }})</template></RouterLink>
        <RouterLink v-if="admin" to="/tasks/history" class="btn btn-outline-secondary btn-sm"><Icon name="clock" /> Історія</RouterLink>
        <button type="button" class="btn btn-outline-secondary btn-sm d-inline-flex align-items-center px-2"
                :title="wide ? 'Назад у колонку сторінки' : 'Каталог на всю ширину'" @click="toggleWide">
          <IconArrows :out="!wide" />
        </button>
      </div>
      <TaskFilters />
      <TaskCatalog />
    </div>
    <div id="guide-low" :class="{ 'in-column': wide }"></div>
    <Toc :items="toc" :side="!wide" />
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; }
#catalog { scroll-margin-top: 1rem; }
.catalog-area { min-height: 100vh; }
</style>
