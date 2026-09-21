<script setup>
import { computed, ref, watch } from 'vue'

import { getGuidePage } from '../api.js'
import { load, save } from '../local.js'
import { tocOf } from '../md.js'
import { user } from '../user.js'
import GuideFoot from './GuideFoot.vue'
import GuideText from './GuideText.vue'
import IconChevron from './IconChevron.vue'

// guide section on top of a catalog page: the whole text for guests and students (the catalog itself
// stays admin-only until it is ready — T116 Q13); above the catalog — a framed block that folds and remembers it.
// `toc` = the text's headings while it is on screen, for the page's side contents
const props = defineProps({ slug: String, stub: String })
const emit = defineEmits(['toc'])
const page = ref(null)
const admin = computed(() => user.value?.status === 'admin')
const text = computed(() => (page.value ? `${page.value.brief}\n\n${page.value.body}` : ''))

const key = `guide-head:${props.slug}`
const open = ref(load(key) !== '0')
function remember(e) {
  open.value = e.target.open
  save(key, open.value ? '1' : '0')
}
watch([text, open, admin], () => emit('toc', open.value || !admin.value ? tocOf(text.value) : []), { immediate: true })

getGuidePage(props.slug).then((p) => (page.value = p))
</script>

<template>
  <template v-if="page">
    <details v-if="admin" class="border rounded px-3 py-2 mb-4" :open="open" @toggle="remember">
      <summary class="d-flex align-items-center gap-2 text-secondary">
        <span>{{ page.title }} — текст методички</span>
        <span class="ms-auto small d-flex align-items-center gap-1" :class="open ? 'text-primary' : 'text-secondary'">
          {{ open ? 'згорнути' : 'розгорнути' }} <IconChevron :dir="open ? 'up' : 'down'" />
        </span>
      </summary>
      <GuideText :text="text" class="mt-3 mb-2" />
    </details>
    <div v-else>
      <h1 class="h2 mb-3">{{ page.title }}</h1>
      <GuideText :text="text" />
      <div class="alert alert-light border mt-4">🚧 {{ stub }}</div>
      <GuideFoot />
    </div>
  </template>
</template>

<style scoped>
summary { cursor: pointer; list-style: none; }
summary::-webkit-details-marker { display: none; }
</style>
