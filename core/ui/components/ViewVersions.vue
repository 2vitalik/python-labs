<script setup>
import { computed, inject, provide, reactive, ref } from 'vue'

import { plural } from '../plural.js'
import { columns } from '../tableCols.js'
import { store, versionsOf } from '../viewStore.js'
import ViewLibVersion from './ViewLibVersion.vue'

// the history of one view (T315 §7), newest first. `only` — the first, the current and the starred stand, each run of the
// rest folds into «… 4 проміжні» that a click opens in place. The host reads the versions (loadVersions); out of the
// library — no marks for comparing — it brings its own columns and its own line for an error
const props = defineProps({ view: { type: Object, required: true }, only: Boolean })
const outer = inject('viewsLib', null)
const lib = outer || reactive({ cols: computed(() => (store.data ? columns(store.data) : [])), error: '',
                                act: async (work) => { try { return await work() } catch (e) { lib.error = e.message } } })
if (!outer) provide('viewsLib', lib)

const list = computed(() => [...versionsOf(props.view.slug)].sort((a, b) => b.n - a.n))
const opened = ref({})
const stays = (x) => !props.only || x.star || x.n === 1 || x.n === props.view.version
const rows = computed(() => {
  const out = []
  list.value.forEach((ver, i) => {
    const row = { key: ver.n, ver, prev: list.value[i + 1] }
    const last = out.at(-1)
    if (stays(ver)) out.push(row)
    else if (last?.run) last.run.push(row)
    else out.push({ key: `run${ver.n}`, run: [row] })
  })
  return out.flatMap((r) => (r.run && opened.value[r.key] ? r.run : [r]))
})
</script>

<template>
  <div class="vvers">
    <p v-if="!store.versions" class="vvers-wait">версії…</p>
    <ul v-else class="vvers-list">
      <template v-for="r in rows" :key="r.key">
        <li v-if="r.run" class="vvers-run">
          <button type="button" class="more-field" @click="opened[r.key] = true">… {{ r.run.length }} {{ plural(r.run.length, 'проміжна', 'проміжні', 'проміжних') }}</button>
        </li>
        <ViewLibVersion v-else :view :ver="r.ver" :prev="r.prev" />
      </template>
    </ul>
    <div v-if="!outer && lib.error" class="small text-danger">{{ lib.error }}</div>
  </div>
</template>

<style scoped>
.vvers { padding-left: .75rem; border-left: 2px solid var(--bs-border-color-translucent); }
.vvers-list { margin: 0; padding: 0; list-style: none; }
.vvers-wait { margin: 0; font-size: .8rem; color: var(--bs-secondary-color); }
.vvers-run { padding: .1rem 0 .15rem; }
</style>
