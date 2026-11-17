<script setup>
import { computed, inject } from 'vue'

import { diff } from '../tableDiff.js'
import { editVersion } from '../viewStore.js'
import DateChip from './DateChip.vue'
import Icon from './Icon.vue'
import InlineText from './InlineText.vue'
import ViewLibFork from './ViewLibFork.vue'
import ViewLibRestore from './ViewLibRestore.vue'

// one version in a view's history (T315 §7): its number, when, who; a name and a note given in place; ⭐ keeps it in sight
// when the rest fold; under it — what changed against the one before. Actions: look at it in the table, bring it back on
// top, start a new view from it, mark it for comparing (only inside the library)
const props = defineProps({ view: { type: Object, required: true }, ver: { type: Object, required: true }, prev: Object })
const lib = inject('viewsLib')
const key = computed(() => `${props.view.slug}@${props.ver.n}`)
const now = computed(() => props.ver.n === props.view.version)
const what = computed(() => (!props.prev ? 'початок' : diff(props.prev.query, props.ver.query, lib.cols).brief.join(' · ') || 'склад той самий'))
const edit = (patch) => editVersion(props.view.slug, props.ver.n, patch)
async function star() {
  const v = props.ver
  v.star = !v.star
  try {
    await edit({ star: v.star })
  } catch (e) {
    v.star = !v.star
    lib.error = e.message
  }
}
</script>

<template>
  <li class="vver" :class="{ now }">
    <div class="vver-l1">
      <b class="vver-n">в. {{ ver.n }}</b>
      <DateChip :at="ver.at" />
      <span class="vver-by">{{ ver.by || 'сайт' }}</span>
      <span v-if="now" class="vver-now">поточна</span>
      <InlineText class="vver-name" :value="ver.name" :save="(name) => edit({ name })" can placeholder="Назва версії">
        <template #empty><span class="more-field">＋ назва</span></template>
      </InlineText>
      <span class="vver-acts">
        <button type="button" class="iact vver-star" :class="{ on: ver.star }" :title="ver.star ? 'Важлива — видно завжди; клік — зняти' : 'Важлива версія: не згортати'"
                :aria-pressed="ver.star" @click="star"><Icon :name="ver.star ? 'starfill' : 'star'" /></button>
        <RouterLink :to="`/table?view=${view.slug}&v=${ver.n}`" class="iact" title="Подивитись у таблиці, нічого не змінюючи"><Icon name="eye" /></RouterLink>
        <ViewLibRestore :view :ver />
        <ViewLibFork :view :ver />
        <button v-if="lib.pick" type="button" class="iact" :class="{ lit: lib.picks.includes(key) }" :aria-pressed="lib.picks.includes(key)"
                title="Порівняти — відміть два види чи версії" @click="lib.pick(key)"><Icon name="compare" /></button>
      </span>
    </div>
    <div class="vver-l2">
      <span class="vver-what" :title="what">{{ what }}</span>
      <InlineText class="vver-note" :value="ver.note" :save="(note) => edit({ note })" can multi placeholder="Нотатка">
        <template #empty><span class="more-field">＋ нотатка</span></template>
      </InlineText>
    </div>
  </li>
</template>

<style scoped>
.vver { padding: .2rem .25rem .3rem; border-radius: .3rem; font-size: .82rem; }
.vver:hover { background: var(--bs-tertiary-bg); }
.vver-l1 { display: flex; align-items: center; gap: .4rem; min-width: 0; }
.vver-n { font-weight: 600; white-space: nowrap; }
.vver-by { color: var(--bs-secondary-color); white-space: nowrap; }
.vver-now { padding: 0 .35rem; border-radius: .3rem; background: var(--bs-success-bg-subtle); color: var(--bs-success-text-emphasis); font-size: .72rem; white-space: nowrap; }
.vver-name { min-width: 0; font-weight: 500; }
.vver-acts { display: flex; flex: none; align-items: center; margin-left: auto; }
.vver-acts .iact { width: 1.4rem; height: 1.4rem; }
.vver-star.on, .vver-star.on:hover { color: var(--bs-warning); }
.iact.lit { background: var(--bs-body-bg); color: var(--bs-primary); }
.vver-l2 { display: flex; flex-wrap: wrap; gap: 0 .6rem; color: var(--bs-secondary-color); font-size: .76rem; }
.vver-what { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.vver-note { color: var(--bs-body-color); font-style: italic; }
/* «＋ назва», «＋ нотатка» — only on the version under the mouse */
.vver:not(:hover):not(:focus-within) .more-field { visibility: hidden; }
</style>
