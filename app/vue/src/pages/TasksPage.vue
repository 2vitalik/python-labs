<script setup>
import { computed, onMounted } from 'vue'

import GuideHead from '../components/GuideHead.vue'
import TaskCatalog from '../components/TaskCatalog.vue'
import { games, loadCatalog } from '../catalog.js'
import { useTaskFilter } from '../taskFilter.js'
import { user } from '../user.js'

const admin = computed(() => user.value?.status === 'admin')
const { f, set, grouped } = useTaskFilter()
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))

onMounted(() => admin.value && loadCatalog())
</script>

<template>
  <div>
    <GuideHead slug="tasks" stub="Каталог завдань із цінами відкриється тут незабаром — до першої лаби." />
    <template v-if="admin">
      <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
        <h1 class="h3 mb-0 me-2">Завдання <span class="count fs-6">({{ shown }})</span></h1>
        <input :value="f.q" class="form-control form-control-sm w-auto flex-grow-1" style="max-width: 22rem"
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
        <RouterLink to="/tasks/new" class="btn btn-outline-primary btn-sm ms-auto">➕ Нове завдання</RouterLink>
      </div>

      <TaskCatalog />
    </template>
  </div>
</template>

<style scoped>
.count { font-weight: 400; opacity: .55; }
</style>
