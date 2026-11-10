<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { showShot } from '@core/lightbox.js'
import { deleteShot, uploadShot } from '../api.js'
import { useEd } from '../ed.js'

// the screenshots of a part (T270 §10.3): thumbnails that open over the page; the owner adds through the violet tile,
// always there, and takes one off by the round control in its corner
const props = defineProps({ part: Object })
const ed = useEd()
const error = ref('')
const busy = ref(false)
const urls = computed(() => (props.part.screenshots || []).map((s) => `/api/uploads/${props.part.game}/${s}`))

async function run(fn) {
  error.value = ''
  busy.value = true
  try {
    await fn()
    ed.changed()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
function onFile(e) {
  const file = e.target.files[0]
  e.target.value = ''
  if (file) run(() => uploadShot(props.part.id, file))
}
const remove = (name) => run(() => deleteShot(props.part.id, name))
</script>

<template>
  <div v-if="ed.editable || urls.length">
    <div class="d-flex flex-wrap align-items-center gap-2">
      <div v-for="(s, i) in part.screenshots" :key="s" class="shot">
        <img :src="urls[i]" alt="скриншот" class="rounded border" title="на весь екран" @click="showShot(urls, i)">
        <span v-if="ed.editable" class="rm"><DelButton what="скриншот" @yes="remove(s)" /></span>
      </div>
      <label v-if="ed.editable" class="add" :class="{ busy, lone: !urls.length }" title="png, jpg, webp або gif до 8 МБ">
        <Icon name="plus" /><span v-if="!urls.length">скриншот</span>
        <input type="file" accept="image/png,image/jpeg,image/webp,image/gif" hidden :disabled="busy" @change="onFile">
      </label>
    </div>
    <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
  </div>
</template>

<style scoped>
.shot { position: relative; }
.shot img { height: 64px; cursor: zoom-in; }
.rm { position: absolute; top: -.5rem; right: -.5rem; }
.rm :deep(.iact) { width: 1.35rem; height: 1.35rem; border: 1px solid var(--bs-border-color); border-radius: 50%; background: var(--bs-body-bg); font-size: .75rem; }
.rm :deep(.iact:hover) { background: var(--bs-danger-bg-subtle); }
.add { display: inline-flex; align-items: center; justify-content: center; gap: .3rem; height: 64px; min-width: 64px; padding: 0 .75rem;
       border: 1.5px dashed color-mix(in srgb, var(--act-add) 55%, transparent); border-radius: .375rem; color: var(--act-add);
       font-size: .85rem; cursor: pointer; }
.add.lone { height: 1.9rem; padding: 0 .55rem; font-size: .8rem; }  /* no thumbnails to match yet: a card without screenshots stays short */
.add:hover { border-color: var(--act-add); background: color-mix(in srgb, var(--act-add) 8%, transparent); }
.add.busy { opacity: .5; pointer-events: none; }
</style>
