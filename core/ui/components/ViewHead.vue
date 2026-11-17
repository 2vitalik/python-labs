<script setup>
import { ref } from 'vue'

import { useTable } from '../tableCtx.js'
import { originLine } from '../viewStats.js'
import { saveView } from '../viewStore.js'
import { toggleWide, wide } from '../wide.js'
import Icon from './Icon.vue'
import IconArrows from './IconArrows.vue'
import InlineText from './InlineText.vue'
import ViewIcon from './ViewIcon.vue'
import ViewMore from './ViewMore.vue'
import ViewPeekBar from './ViewPeekBar.vue'
import ViewSave from './ViewSave.vue'

// the head of the view open (T315 §2.2–3): its icon and name, changed right where they stand, the search and «на всю
// ширину». Under them «для чого», and small after it: the version (its history in the library), where the view comes from,
// the etalon star, «⋯». A past version on screen says so over that line; a change not saved — under it (ViewSave)
const t = useTable()
const error = ref('')
const save = (patch) => saveView(t.slug, patch)
const flipEtalon = () => save({ etalon: !t.view.etalon }).then(() => (error.value = ''), (e) => (error.value = e.message))
</script>

<template>
  <div class="mb-2">
    <div class="d-flex flex-wrap align-items-center gap-2">
      <span class="big"><ViewIcon :view="t.view" can /></span>
      <h1 class="h3 mb-0 me-auto"><InlineText :value="t.view.title" can required placeholder="Назва виду" :save="(title) => save({ title })" /></h1>
      <input type="search" :value="t.state.q" class="form-control form-control-sm w-auto" placeholder="Пошук: ПІБ, нік…"
             title="За початком слова: прізвище, імʼя, нік, Telegram" @input="t.set({ q: $event.target.value })">
      <button type="button" class="btn btn-outline-secondary btn-sm px-2" :title="wide ? 'Назад у колонку сторінки' : 'Таблиця на всю ширину'"
              @click="toggleWide"><IconArrows :out="!wide" /></button>
    </div>
    <ViewPeekBar />
    <div class="about mt-1">
      <InlineText :value="t.view.about" can multi placeholder="Для чого цей вид" :save="(about) => save({ about })">
        <template #empty><span class="inl-none">＋ для чого цей вид</span></template>
      </InlineText>
      <span class="meta">
        <RouterLink :to="{ path: '/table/views', query: { view: t.slug } }" title="Історія версій у бібліотеці видів">версія {{ t.view.version }}</RouterLink>
        <span v-if="originLine(t.view)">{{ originLine(t.view) }}</span>
        <button type="button" class="star" :class="{ on: t.view.etalon }" title="Еталон — з цього виду зручно починати нові" @click="flipEtalon">
          <Icon :name="t.view.etalon ? 'starfill' : 'star'" /><template v-if="t.view.etalon"> еталон</template></button>
        <ViewMore />
        <span v-if="error" class="text-danger">{{ error }}</span>
      </span>
    </div>
    <ViewSave />
  </div>
</template>

<style scoped>
.big { font-size: 1.6rem; line-height: 1; }
.meta { margin-left: .6rem; font-size: .8rem; color: var(--bs-secondary-color); }
.meta > * { white-space: nowrap; }
.meta > * + *::before { content: '·'; margin: 0 .4rem; color: var(--bs-secondary-color); }
.meta a { color: inherit; text-decoration: underline dotted; text-underline-offset: .2em; }
.meta a:hover { color: var(--bs-body-color); }
.star { padding: 0; border: 0; background: none; color: inherit; }
.star:hover { color: var(--bs-body-color); }
.star.on .icon { color: var(--bs-warning); }
</style>
