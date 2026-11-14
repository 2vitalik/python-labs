<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { showShot } from '@core/lightbox.js'
import { useEd } from '../ed.js'

// pictures uploaded to a game (a part's screenshots, a claim's proof): thumbnails that open over the page, a gif plays;
// `adds` — the violet tile, `word` on it while there is nothing yet; `drops` — the round control in a thumbnail's corner.
// `add(file)` / `drop(name)` — the calls; the editor reloads after each; `need` — none yet is a gap: the lone tile is red
const props = defineProps({ game: String, names: Array, adds: Boolean, drops: Boolean, word: String, what: String, add: Function, drop: Function, need: Boolean })
const ed = useEd()
const error = ref('')
const busy = ref(false)
const urls = computed(() => props.names.map((s) => `/api/uploads/${props.game}/${s}`))

async function run(fn) {
  error.value = ''
  busy.value = true
  try {
    await fn()
    await ed.changed()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
function onFile(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (file) run(() => props.add(file))
}
</script>

<template>
  <div v-if="adds || urls.length">
    <div class="d-flex flex-wrap align-items-center gap-2">
      <div v-for="(s, i) in names" :key="s" class="shot">
        <img :src="urls[i]" :alt="what" class="rounded border" title="на весь екран" @click="showShot(urls, i)">
        <span v-if="drops" class="rm"><DelButton :what @yes="run(() => drop(s))" /></span>
      </div>
      <label v-if="adds" class="add" :class="{ busy, lone: !urls.length, miss: need && !urls.length }"
             :title="need && !urls.length ? `${word} ще нема — png, jpg, webp або gif до 8 МБ` : 'png, jpg, webp або gif до 8 МБ'">
        <Icon name="plus" /><span v-if="!urls.length">{{ word }}</span>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" hidden :disabled="busy" @change="onFile">
      </label>
    </div>
    <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
  </div>
</template>

<style scoped>
.shot { position: relative; }
.shot img { height: 64px; max-width: 12rem; object-fit: cover; cursor: zoom-in; }  /* a panorama stays inside a phone's sheet */
.rm { position: absolute; top: -.5rem; right: -.5rem; }
.rm :deep(.iact) { width: 1.35rem; height: 1.35rem; border: 1px solid var(--bs-border-color); border-radius: 50%; background: var(--bs-body-bg); font-size: .75rem; }
.rm :deep(.iact:hover) { background: var(--bs-danger-bg-subtle); }
.add { display: inline-flex; align-items: center; justify-content: center; gap: .3rem; height: 64px; min-width: 64px; padding: 0 .75rem;
       border: 1.5px dashed color-mix(in srgb, var(--act-add) 55%, transparent); border-radius: .375rem; color: var(--act-add);
       font-size: .85rem; cursor: pointer; }
.add.lone { height: 1.9rem; padding: 0 .55rem; font-size: .8rem; }  /* no thumbnails to match yet: a card without pictures stays short */
.add:hover { border-color: var(--act-add); background: color-mix(in srgb, var(--act-add) 8%, transparent); }
.add.busy { opacity: .5; pointer-events: none; }
.add.miss { --act-add: var(--act-miss); }
</style>
