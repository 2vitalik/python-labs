<script setup>
import { computed, nextTick, onMounted, provide, reactive, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash } from '../anchors.js'
import Crumbs from '../components/Crumbs.vue'
import Icon from '../components/Icon.vue'
import ViewsArchive from '../components/ViewsArchive.vue'
import ViewsBar from '../components/ViewsBar.vue'
import ViewsCompare from '../components/ViewsCompare.vue'
import ViewsFolders from '../components/ViewsFolders.vue'
import ViewTree from '../components/ViewTree.vue'
import { plural } from '../plural.js'
import { columns } from '../tableCols.js'
import { useTitle } from '../title.js'
import { lastTouch } from '../viewStats.js'
import { liveViews, load, loadVersions, store, viewOf } from '../viewStore.js'

// the library of the views of /table (T315 §8): here they are put in order — in folders or by what each was made from —
// and found by a word, a tag, ⭐. The switches live in the URL; what is open and what is marked for comparing — in `lib`,
// which the rows below share; an action's error stands at the bottom of the window
const route = useRoute()
const router = useRouter()
useTitle('Види')
const lib = reactive({
  cols: computed(() => (store.data ? columns(store.data) : [])),
  picks: [],  // marked for comparing: 'slug' — a view, 'slug@n' — its version
  hist: {},  // slug → its versions are open
  archive: false,
  error: '',
  pick: (key) => (lib.picks = lib.picks.includes(key) ? lib.picks.filter((k) => k !== key) : [...lib.picks, key].slice(-2)),
  act: async (work) => { try { return await work() } catch (e) { lib.error = e.message } },
})
provide('viewsLib', lib)

const ORDERS = ['own', 'used', 'name']
const f = computed(() => ({ q: String(route.query.q || ''), mode: route.query.mode === 'tree' ? 'tree' : 'folders', etalon: route.query.etalon === '1',
                            tag: String(route.query.tag || ''), order: ORDERS.includes(route.query.order) ? route.query.order : 'own' }))
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
const filtering = computed(() => !!(f.value.q.trim() || f.value.tag || f.value.etalon))
const low = (s) => s.toLocaleLowerCase('uk')
const matches = (v) => (!f.value.q.trim() || [v.title, v.about, ...v.tags].some((s) => low(s).includes(low(f.value.q.trim()))))
  && (!f.value.etalon || v.etalon) && (!f.value.tag || v.tags.includes(f.value.tag))
const SORT = { used: (a, b) => lastTouch(b).localeCompare(lastTouch(a)), name: (a, b) => a.title.localeCompare(b.title, 'uk') }
const ordered = computed(() => (SORT[f.value.order] ? [...liveViews()].sort(SORT[f.value.order]) : liveViews()))
const shown = computed(() => ordered.value.filter(matches))
const tags = computed(() => [...new Set(liveViews().flatMap((v) => v.tags))].sort((a, b) => a.localeCompare(b, 'uk')))
const count = computed(() => {
  const n = liveViews().length
  return `${filtering.value ? `${shown.value.length} з ` : ''}${n} ${plural(n, 'вид', 'види', 'видів')}`
})

onMounted(load)  // fresh even when /table has read it: the use counts grow while a view is open there
watch(() => store.versions, (v) => v === null && lib.act(loadVersions), { immediate: true })  // a save drops them: read again
// ?view=<slug> — the way here from a view's «версія 3»: its history open, its row lit
watch([() => !!store.data, () => route.query.view], async ([data, slug]) => {
  const v = data && slug && viewOf(String(slug))
  if (!v) return
  if (v.archived_at) lib.archive = true
  else lib.hist[v.slug] = true
  await nextTick()
  flash(`view-${v.slug}`)
}, { immediate: true })
</script>

<template>
  <div>
    <Crumbs :items="[['/students', 'Студенти'], ['/table', 'Звід'], 'Види']" />
    <div class="d-flex flex-wrap align-items-baseline gap-2 mb-3">
      <h1 class="h3 mb-0">Види</h1>
      <span v-if="store.data" class="text-secondary">{{ count }}</span>
    </div>
    <div v-if="store.error" class="alert alert-danger">{{ store.error }}</div>
    <template v-if="store.data">
      <ViewsBar :f :tags @set="set" />
      <ViewsFolders v-if="f.mode === 'folders'" :views="shown" :filtering :can-drag="f.order === 'own'" />
      <ViewTree v-else :views="ordered" :keep="filtering ? matches : null" :only="f.etalon" />
      <p v-if="filtering && !shown.length" class="text-secondary my-3">
        Нічого не знайдено · <a href="#" @click.prevent="set({ q: undefined, tag: undefined, etalon: undefined })">скинути пошук</a>
      </p>
      <ViewsArchive />
      <div class="vlib-foot">
        <Transition name="vlib-err">
          <div v-if="lib.error" class="vlib-err alert alert-danger small mb-0" role="alert">
            <span>{{ lib.error }}</span>
            <button type="button" class="iact" title="Закрити" @click="lib.error = ''"><Icon name="x" /></button>
          </div>
        </Transition>
        <ViewsCompare />
      </div>
    </template>
    <p v-else-if="!store.error" class="text-secondary">Завантажую…</p>
  </div>
</template>

<style scoped>
/* the comparison and an error hang at the bottom of the window over the list, and rest after it when it ends */
.vlib-foot { position: sticky; bottom: .75rem; z-index: 30; display: grid; gap: .5rem; margin-top: 1rem; }
.vlib-err { display: flex; align-items: center; gap: .5rem; padding: .35rem .5rem .35rem .75rem; box-shadow: 0 .2rem .8rem rgb(0 0 0 / .12); }
.vlib-err .iact { margin-left: auto; }
.vlib-err-enter-active, .vlib-err-leave-active { transition: opacity .2s ease, transform .2s ease; }
.vlib-err-enter-from, .vlib-err-leave-to { opacity: 0; transform: translateY(.5rem); }
@media (prefers-reduced-motion: reduce) { .vlib-err-enter-active, .vlib-err-leave-active { transition: none; } }
</style>
