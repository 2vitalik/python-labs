<script setup>
import { axisText, KLASSES } from '../ludopedia.js'

// rows of the corpus list: a game per row, the numbers that say how rich the description is
defineProps({ list: Array, family: Boolean })
const axes = (g) => ['time', 'opponent', 'goal'].map((k) => axisText(k, g.axes[k])).filter(Boolean).join(' · ')
</script>

<template>
  <table class="table table-sm align-middle mb-0 ludo">
    <thead class="small text-secondary">
      <tr>
        <th>Гра</th>
        <th v-if="family">Сімʼя</th>
        <th>Клас</th>
        <th>Осі</th>
        <th class="text-end">Рік</th>
        <th title="Стадія опису · частка механіки, що лягла в словники">Опис</th>
        <th class="text-end" title="сутностей · правил · тегів механік">Σ</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="g in list" :key="g.slug">
        <td>
          <RouterLink :to="`/ludopedia/${g.slug}`" class="fw-semibold text-decoration-none">{{ g.title }}</RouterLink>
          <div class="small text-secondary">{{ g.headline }}</div>
        </td>
        <td v-if="family" class="small"><RouterLink :to="{ path: '/ludopedia', query: { fam: g.family } }" class="text-decoration-none">{{ g.family }}</RouterLink></td>
        <td class="small">{{ KLASSES[g.klass] || g.klass }}</td>
        <td class="small text-secondary">{{ axes(g) }}</td>
        <td class="text-end small">{{ g.year }}</td>
        <td class="small text-nowrap"><span class="badge border fw-normal" :class="g.stage === 'v1' ? 'text-secondary' : 'text-bg-success'">{{ g.stage }}</span> {{ g.coverage }}%</td>
        <td class="text-end small text-secondary text-nowrap">{{ g.entities }} · {{ g.rules }} · {{ g.mechanics.length }}</td>
        <td><a v-if="g.url" :href="g.url" target="_blank" rel="noopener" class="text-decoration-none" title="Найкращий вхід у гру">⭐</a></td>
      </tr>
    </tbody>
  </table>
</template>

<style scoped>
.ludo td, .ludo th { padding-block: .35rem; }
</style>
