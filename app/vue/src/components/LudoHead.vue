<script setup>
import { AXES, axisText, FAMILIES, KLASSES, LINK_KINDS, STAGES } from '../ludopedia.js'

// the head of a corpus game: what it is, where it lives in the taxonomy, where to look at it, which mechanics it carries
defineProps({ game: Object })
</script>

<template>
  <div>
    <h1 class="h3 mb-1">{{ game.title }}</h1>
    <p class="text-secondary mb-1">{{ game.headline }}<span v-if="game.aka.length" class="small"> · також: {{ game.aka.join(', ') }}</span></p>
    <p class="d-flex gap-1 flex-wrap mb-2">
      <RouterLink :to="{ path: '/ludopedia', query: { fam: game.family } }" class="badge text-bg-primary text-decoration-none">{{ FAMILIES[game.family]?.[0] || game.family }}</RouterLink>
      <RouterLink v-for="a in game.also" :key="a" :to="{ path: '/ludopedia', query: { fam: a } }" class="badge text-bg-light border text-dark fw-normal text-decoration-none">+ {{ FAMILIES[a]?.[0] || a }}</RouterLink>
      <RouterLink :to="{ path: '/ludopedia', query: { klass: game.klass } }" class="badge text-bg-secondary text-decoration-none">{{ KLASSES[game.klass] || game.klass }}</RouterLink>
      <span v-for="(v, k) in game.axes" :key="k" class="badge text-bg-light border text-dark fw-normal">{{ AXES[k]?.[0] || k }}: {{ axisText(k, v) }}</span>
    </p>
    <p class="small text-secondary mb-2">
      <span v-if="game.year">{{ game.year }} · </span><span v-if="game.platforms.length">{{ game.platforms.join(', ') }} · </span>
      <span :title="STAGES[game.stage]">{{ game.stage }}</span> · покриття словниками {{ game.coverage }}% · {{ game.author }} · {{ game.date }}
    </p>
    <p class="d-flex gap-1 flex-wrap mb-2">
      <a v-for="l in game.links" :key="l.url" :href="l.url" target="_blank" rel="noopener" class="btn btn-sm" :class="l.best ? 'btn-primary' : 'btn-outline-secondary'"
         :title="l.note || l.url">{{ l.best ? '⭐ ' : '' }}{{ LINK_KINDS[l.kind] || l.kind }}</a>
    </p>
    <p class="d-flex gap-1 flex-wrap mb-0">
      <RouterLink v-for="t in game.mechanics" :key="t" :to="{ path: '/ludopedia', query: { mech: t.replace(/^\+/, '') } }"
                  class="badge fw-normal text-decoration-none" :class="t.startsWith('+') ? 'text-secondary border border-secondary-subtle new' : 'text-bg-light border text-dark'"
                  :title="t.startsWith('+') ? 'Нова механіка — картки в каталозі ще нема' : 'Картка каталогу · інші ігри з нею'">{{ t }}</RouterLink>
    </p>
  </div>
</template>

<style scoped>
.new { border-style: dashed !important; }
</style>
