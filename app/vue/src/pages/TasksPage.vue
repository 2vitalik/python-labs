<script setup>
import { computed, onMounted } from 'vue'

import TaskCard from '../components/TaskCard.vue'
import ZoneTree from '../components/ZoneTree.vue'
import { games, loadCatalog, zones } from '../catalog.js'
import { useTaskFilter } from '../taskFilter.js'
import { user } from '../user.js'

const { f, set, counts, grouped } = useTaskFilter()
const shown = computed(() => grouped.value.reduce((n, z) => n + z.subs.reduce((m, s) => m + s.list.length, 0), 0))

onMounted(loadCatalog)
</script>

<template>
  <div v-if="user && user.status !== 'pending'">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h1 class="h3 mb-0">Завдання <span class="text-secondary fs-6">({{ shown }})</span></h1>
      <RouterLink v-if="user.status === 'admin'" to="/tasks/new" class="btn btn-outline-primary btn-sm">➕ Нове завдання</RouterLink>
    </div>

    <div class="row g-2 mb-3">
      <div class="col-md-5">
        <input :value="f.q" class="form-control" placeholder="Пошук: назва, опис, теги…"
               @input="set({ q: $event.target.value })">
      </div>
      <div class="col-md-4">
        <select :value="f.game" class="form-select" @change="set({ game: $event.target.value })">
          <option value="">Всі ігри</option>
          <option v-for="g in games" :key="g.slug" :value="g.slug">{{ g.icon }} {{ g.title }}</option>
        </select>
      </div>
      <div class="col-md-3 d-flex align-items-center">
        <div class="form-check">
          <input id="algo" class="form-check-input" type="checkbox" :checked="f.algo"
                 @change="set({ algo: $event.target.checked ? '1' : '' })">
          <label class="form-check-label" for="algo">⭐ алгоритмічні</label>
        </div>
      </div>
    </div>

    <div class="row g-3">
      <div class="col-md-4 col-lg-3">
        <ZoneTree :zones="zones" :counts="counts" :zone="f.zone" :sub="f.sub"
                  @select="(z, s) => set({ zone: z, sub: s })" />
      </div>
      <div class="col-md-8 col-lg-9">
        <p v-if="!shown" class="text-secondary mt-3">Нічого не знайдено — спробуй інші слова чи зніми фільтри.</p>
        <section v-for="z in grouped" :key="z.key" class="mb-3">
          <h2 class="h5">{{ z.title }}</h2>
          <div v-for="s in z.subs" :key="s.key" class="mb-3">
            <div class="text-secondary small fw-semibold mb-1">{{ s.title }}</div>
            <TaskCard v-for="t in s.list" :key="t.id" :task="t" />
          </div>
        </section>
      </div>
    </div>
  </div>
  <p v-else class="text-center mt-5">Каталог доступний після входу і підтвердження.</p>
</template>
