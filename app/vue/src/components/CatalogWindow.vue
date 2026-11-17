<script setup>
import { computed, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'

import Sheet from '@core/components/Sheet.vue'
import { placesOf } from '../claimPlace.js'
import { useEd } from '../ed.js'
import { provideGameCtx } from '../gameCtx.js'
import { jump } from '../jump.js'
import { provideTaskFilter } from '../taskFilter.js'
import TaskCatalog from './TaskCatalog.vue'
import TaskFilters from './TaskFilters.vue'

// the catalog in a window over the game's page (T318): the very cards of «Таски» — search, subcategories, a card unfolded,
// «＋» and the tick — narrowed to what the place is about, so several cards are picked without leaving the game.
// `scope` — { title, only(task), to, anchor? } (sections.js catalogOf, CardPicker): `to` — the same on «Таски», `anchor` —
// the part or rule the cards are claimed on. The window writes into the game being edited (gameCtx.js), not «Моя гра»
const open = defineModel({ type: Boolean, default: false })
const props = defineProps({ scope: Object })
const ed = useEd()
const router = useRouter()
const filter = reactive({ q: '', game: '', algo: '', zone: '', sub: '', only: null })
watch(() => open.value && props.scope, (s) => s && Object.assign(filter, { q: '', game: '', algo: '', zone: s.zone || '', sub: '', only: s.only }))
provideTaskFilter(filter)

const anchor = computed(() => props.scope?.anchor)
const at = (c) => !anchor.value || ((c.part || '') === (anchor.value.part || '') && (c.rule || '') === (anchor.value.rule || ''))
const claims = computed(() => ed.claims.filter(at))
function show(id) {
  open.value = false
  jump(id)
}
provideGameCtx({
  has: computed(() => true), get can() { return ed.editable }, claims, parts: computed(() => ed.parts), slugs: computed(() => new Set(claims.value.map((c) => c.task))),
  places: (slug) => placesOf(slug, { claims: claims.value, parts: ed.parts, rules: ed.rules, info: ed.info }),
  reload: () => ed.changed(), show, get anchor() { return anchor.value },
})
const href = computed(() => (props.scope ? router.resolve(props.scope.to).href : ''))
</script>

<template>
  <Sheet v-model="open" :title="scope?.title">
    <template #head>
      <span v-if="scope?.note" class="small text-secondary">{{ scope.note }}</span>
      <a :href target="_blank" rel="noopener" class="small text-nowrap" title="Ця сама категорія на сторінці «Таски» — у новій вкладці">на сторінці «Таски» ↗</a>
    </template>
    <template #bar><TaskFilters /></template>
    <TaskCatalog v-if="scope" />
  </Sheet>
</template>
