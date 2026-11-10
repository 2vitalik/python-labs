<script setup>
import { computed, onBeforeUnmount, ref } from 'vue'
import { useRoute } from 'vue-router'

import Icon from '@core/components/Icon.vue'
import { canAccess, user } from '@core/user.js'
import { getSandbox, resetSandbox } from '../api.js'
import { sandbox, setSandbox } from '../sandbox.js'
import GameEditor from './GameEditor.vue'

// the base game's reference description: read-only, or — «Спробувати редагувати» — the sandbox (T274 §7): the same editor
// over the reader's own server-side copy of it, real calls and all; nothing of it reaches their game
const props = defineProps({ slug: String, etalon: Object })
const route = useRoute()
const box = ref(null)  // the copy while the sandbox is on
const round = ref(0)  // a reset makes a new copy with new ids: the editor starts afresh
const busy = ref(false)
const error = ref('')
// the header is what keeps writes off the reader's game: no header, no editing
const on = computed(() => box.value && sandbox.value === props.slug)

async function run(fn) {
  error.value = ''
  busy.value = true
  try {
    await fn()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const reload = () => getSandbox(props.slug).then((d) => (box.value = d))
const enter = () => run(async () => {
  const d = await getSandbox(props.slug).catch((e) => (e.status === 404 ? resetSandbox(props.slug) : Promise.reject(e)))
  setSandbox(props.slug)
  box.value = d
})
const reset = () => run(async () => {
  box.value = await resetSandbox(props.slug)
  round.value++
})
function leave() {
  setSandbox('')
  box.value = null
}
onBeforeUnmount(() => setSandbox(''))
</script>

<template>
  <div>
    <template v-if="on">
      <div class="alert box d-flex flex-wrap align-items-center gap-2 py-2 small">
        <span>🧪 Пісочниця — це твоя копія зразка. Міняй що завгодно: у твою гру нічого не потрапляє</span>
        <span class="ms-auto d-flex gap-2">
          <button type="button" class="btn btn-sm btn-outline-secondary" :disabled="busy" title="Знову чистий зразок" @click="reset">Скинути</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="leave">Вийти</button>
        </span>
      </div>
      <div v-if="error" class="text-danger small mb-2">{{ error }}</div>
      <GameEditor :key="round" full editable :game="box.game" :parts="box.parts" :claims="box.claims" :rules="box.rules" :tasks="box.tasks"
                  :coins="box.coins" :reload />
    </template>
    <template v-else>
      <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
        <button v-if="canAccess('active')" type="button" class="btn btn-sm btn-outline-secondary" :disabled="busy" @click="enter">
          <Icon name="pencil" /> Спробувати редагувати</button>
        <span v-else-if="!user" class="small text-secondary">
          <RouterLink :to="{ path: '/login', query: { next: route.fullPath } }">Увійди</RouterLink>, щоб спробувати редагувати</span>
        <span v-if="error" class="text-danger small">{{ error }}</span>
      </div>
      <GameEditor full :game="etalon.game" :parts="etalon.parts" :claims="etalon.claims" :rules="etalon.rules" :tasks="etalon.tasks" :coins="etalon.coins" />
    </template>
  </div>
</template>

<style scoped>
.box { border-color: var(--bs-warning-border-subtle); background: color-mix(in srgb, var(--bs-warning-bg-subtle) 55%, var(--bs-body-bg)); }
</style>
