<script setup>
import { computed, ref } from 'vue'

import { COINS, missingParams, subzoneTitle } from '../catalog.js'
import { searchTasks } from '../search.js'
import SlotFields from './SlotFields.vue'

// «＋ картка…» on an entity, a window or the game: search by title, synonyms, slug, tags; a card with required
// slots asks for them first (unless `loose` — the game level may wait); emits pick(slug, params)
const props = defineProps({
  placeholder: { type: String, default: '＋ картка з каталогу…' }, filter: { type: Function, default: () => true },
  claimed: { type: Set, default: () => new Set() }, loose: Boolean,
})
const emit = defineEmits(['pick'])
const q = ref('')
const open = ref(false)
const picked = ref(null)
const params = ref({})
const found = computed(() => (q.value.trim().length < 2 ? [] : searchTasks(q.value, 8, props.filter)))
const ready = computed(() => props.loose || !missingParams(picked.value, params.value).length)

function pick(t) {
  q.value = ''
  open.value = false
  if (t.slots?.length) {
    picked.value = t
    params.value = {}
  } else {
    emit('pick', t.slug, {})
  }
}
function send() {
  emit('pick', picked.value.slug, params.value)
  picked.value = null
}
</script>

<template>
  <div v-if="picked" class="d-flex gap-1 flex-wrap align-items-center small">
    <span class="text-nowrap">{{ COINS[picked.coin] || '·' }} {{ picked.title }}:</span>
    <SlotFields :specs="picked.slots" :params="params" />
    <button class="btn btn-primary btn-sm" :disabled="!ready" @click="send">Додати</button>
    <button class="btn btn-outline-secondary btn-sm" @click="picked = null">✕</button>
  </div>
  <div v-else class="position-relative">
    <input v-model="q" class="form-control form-control-sm picker" :placeholder="placeholder"
           @focus="open = true" @blur="open = false" @keydown.enter.prevent="found[0] && pick(found[0])">
    <div v-if="open && found.length" class="list-group position-absolute w-100 shadow" style="z-index: 20">
      <button v-for="t in found" :key="t.slug" type="button" class="list-group-item list-group-item-action py-1 small d-flex gap-2"
              :class="{ 'text-secondary': claimed.has(t.slug) }" @mousedown.prevent="pick(t)">
        <span>{{ COINS[t.coin] || '·' }}</span>
        <span class="me-auto">{{ t.title }} <span v-if="claimed.has(t.slug)" title="уже є в грі">✓</span></span>
        <span class="text-secondary text-nowrap">{{ subzoneTitle(t) }}</span>
      </button>
    </div>
    <div v-else-if="open && q.trim().length >= 2" class="list-group position-absolute w-100 shadow" style="z-index: 20">
      <div class="list-group-item py-1 small text-secondary">Нічого — спробуй інше слово або <RouterLink to="/ideas">запропонуй картку</RouterLink></div>
    </div>
  </div>
</template>

<style scoped>
.picker { border-style: dashed; }
</style>
