<script setup>
import { nextTick, ref, watch } from 'vue'

import { hitLink, snippetHtml } from '../lectureFindKinds.js'

// the results (sectionsOf): a section per kind in its colour, inside it the lectures, inside them the places — each a
// link to its spot in the lecture; why it was found (`via`) — once for the rows of a lecture that share it.
// `active` — the row the arrows stand on: it is kept in sight
const props = defineProps({ sections: Array, counts: Object, active: Number })
const root = ref()
watch(() => props.active, async () => {
  await nextTick()
  root.value?.querySelector('.hit.on')?.scrollIntoView({ block: 'nearest' })
})
const shown = (s) => s.groups.reduce((n, g) => n + g.rows.length, 0)
</script>

<template>
  <div ref="root" class="hits">
    <section v-for="s in sections" :key="s.key" class="kind" :class="`k-${s.key}`">
      <h2 class="head"><span class="kdot" />{{ s.head }}
        <span class="n">{{ shown(s) < (counts[s.key] || 0) ? `${shown(s)} з ${counts[s.key]}` : shown(s) }}</span></h2>
      <div v-for="g in s.groups" :key="g.lec" class="group">
        <RouterLink :to="`/lectures/${g.lec}`" class="lec small text-secondary">Лекція {{ g.lec }} · {{ g.title }}</RouterLink>
        <RouterLink v-for="(h, j) in g.rows" :key="h.i" :to="hitLink(h)" class="hit" :class="{ on: h.i === active }" :data-i="h.i">
          <span class="where">{{ h.heading || 'Початок лекції' }}<span class="at">слайд {{ h.slide }}</span></span>
          <span v-if="h.snippet" class="snip" v-html="snippetHtml(h.snippet, h.marks)" />
          <span v-if="h.via && h.via !== g.rows[j - 1]?.via" class="via">{{ h.via }}</span>
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hits { margin-top: .75rem; }
.kind + .kind { margin-top: 1.25rem; }
.head { display: flex; align-items: center; gap: .45rem; margin: 0 0 .15rem; font-size: .8rem; font-weight: 600;
        text-transform: uppercase; letter-spacing: .03em; color: var(--bs-secondary-color); }
.head .n { font-weight: 400; color: var(--bs-tertiary-color); text-transform: none; }
.group { padding: .35rem 0; border-bottom: 1px solid var(--bs-border-color-translucent); }
.lec { display: block; text-decoration: none; margin-bottom: .15rem; }
.lec:hover { color: var(--bs-body-color) !important; }
/* a thin edge of the kind's colour on the left; the arrows' row is filled */
.hit { display: block; margin: .3rem 0 .3rem .5rem; padding: .2rem .6rem; border-left: 3px solid var(--k);
       border-radius: 0 .3rem .3rem 0; color: inherit; text-decoration: none; scroll-margin: 5rem 0 1rem; }
.hit:hover .where, .hit.on .where { text-decoration: underline; }
.hit.on { background: var(--bs-tertiary-bg); }
.where { display: block; color: var(--bs-link-color); }
.at { display: inline-block; margin-left: .5rem; font-size: .75rem; color: var(--bs-tertiary-color); }
.snip { display: block; font-size: .875rem; color: var(--bs-secondary-color); }
.via { display: block; font-size: .75rem; color: var(--bs-tertiary-color); }
.via::before { content: '↳ '; }
</style>
