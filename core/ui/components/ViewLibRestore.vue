<script setup>
import { inject, ref } from 'vue'

import { restoreVersion } from '../viewStore.js'
import Icon from './Icon.vue'
import Pop from './Pop.vue'

// «повернути» a version (T315 §7): asked in a small panel; the old look becomes a new version on top, nothing is lost.
// The current version has nothing to come back to: the button stays, grey, and says so
const props = defineProps({ view: { type: Object, required: true }, ver: { type: Object, required: true } })
const lib = inject('viewsLib')
const open = ref(false)
const now = () => props.ver.n === props.view.version
const restore = () => lib.act(async () => {
  open.value = false
  await restoreVersion(props.view.slug, props.ver.n)
})
</script>

<template>
  <Pop v-model="open" width="17rem">
    <template #trigger="{ toggle }">
      <button type="button" class="iact" :disabled="now()" :title="now() ? 'Це й так поточна версія' : 'Повернути цю версію'" @click="toggle"><Icon name="back" /></button>
    </template>
    <div class="mb-2">Повернути версію {{ ver.n }}?<div class="small text-secondary">Вона стане новою версією зверху — нічого не загубиться</div></div>
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" @click="restore">Повернути</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
    </div>
  </Pop>
</template>

<style scoped>
.iact { width: 1.4rem; height: 1.4rem; }
.iact:disabled { opacity: .35; }
</style>
