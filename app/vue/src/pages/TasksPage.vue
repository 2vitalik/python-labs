<script setup>
import { computed, onMounted } from 'vue'

import TaskCard from '../components/TaskCard.vue'
import ZoneNav from '../components/ZoneNav.vue'
import { games, loadCatalog, subStyle, zones } from '../catalog.js'
import { useTaskFilter } from '../taskFilter.js'
import { user } from '../user.js'

const { f, set, counts, grouped } = useTaskFilter()
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))

onMounted(loadCatalog)
</script>

<template>
  <div v-if="user && user.status !== 'pending'">
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0 me-2">Завдання <span class="text-secondary fs-6">({{ shown }})</span></h1>
      <input :value="f.q" class="form-control form-control-sm w-auto flex-grow-1" style="max-width: 22rem"
             placeholder="Пошук: назва, опис, теги…" @input="set({ q: $event.target.value })">
      <select :value="f.game" class="form-select form-select-sm w-auto" @change="set({ game: $event.target.value })">
        <option value="">Всі ігри</option>
        <option v-for="g in games" :key="g.slug" :value="g.slug">{{ g.icon }} {{ g.title }}</option>
      </select>
      <div class="form-check">
        <input id="algo" class="form-check-input" type="checkbox" :checked="f.algo"
               @change="set({ algo: $event.target.checked ? '1' : '' })">
        <label class="form-check-label" for="algo">⭐ алгоритмічні</label>
      </div>
      <RouterLink v-if="user.status === 'admin'" to="/tasks/new" class="btn btn-outline-primary btn-sm ms-auto">➕ Нове завдання</RouterLink>
    </div>

    <ZoneNav :zones="zones" :counts="counts" :zone="f.zone" :sub="f.sub"
             @select="(z, s) => set({ zone: z, sub: s })" />

    <p v-if="!shown" class="text-secondary mt-3">Нічого не знайдено — спробуй інші слова чи зніми фільтри.</p>
    <section v-for="z in grouped" :key="z.key" class="mb-4">
      <h2 v-if="!f.zone" class="h6 zone-head" :style="{ '--zc': z.color }">{{ z.icon }} {{ z.title }}</h2>
      <div class="task-cols">
        <div v-for="s in z.subs" :key="s.key" class="task-group" :style="subStyle(z.color, s.i)">
          <div class="group-head">{{ s.icon }} {{ s.title }} <span class="opacity-50">{{ s.list.length }}</span></div>
          <TaskCard v-for="t in s.list" :key="t.id" :task="t" />
        </div>
      </div>
    </section>
  </div>
  <p v-else class="text-center mt-5">Каталог доступний після входу і підтвердження.</p>
</template>

<style scoped>
.zone-head {
  color: var(--zc); font-weight: 700;
  border-bottom: 2px solid color-mix(in srgb, var(--zc) 30%, #fff);
  padding-bottom: .25rem; margin-bottom: .75rem;
}
.task-cols { columns: 20rem; column-gap: 1.5rem; }
.task-group {
  break-inside: avoid; margin-bottom: 1rem; padding-left: .5rem;
  border-left: 3px solid color-mix(in srgb, var(--sc) 55%, #fff);
}
.group-head { font-size: .85rem; font-weight: 600; color: var(--sc); margin-bottom: .25rem; }
</style>
