<script setup>
import { computed, nextTick, ref } from 'vue'
import { useRoute } from 'vue-router'

import { flash } from '../anchors.js'
import { getGuidePage } from '../api.js'
import { user } from '../user.js'
import GuideText from './GuideText.vue'

// guide section on top of a catalog page: the whole text for guests and students (the catalog itself
// stays admin-only until it is ready — T116 Q13), a collapsed block for the admin
const props = defineProps({ slug: String, stub: String })
const route = useRoute()
const page = ref(null)
const admin = computed(() => user.value?.status === 'admin')
const text = computed(() => (page.value ? `${page.value.brief}\n\n${page.value.body}` : ''))

getGuidePage(props.slug).then(async (p) => {
  page.value = p
  await nextTick()
  if (route.hash) flash(route.hash.slice(1))
})
</script>

<template>
  <template v-if="page">
    <details v-if="admin" class="mb-3">
      <summary class="text-secondary">{{ page.title }} — текст методички</summary>
      <GuideText :text="text" class="mt-2 mb-4" />
    </details>
    <div v-else class="mx-auto" style="max-width: 52rem">
      <h1 class="h2 mb-3">{{ page.title }}</h1>
      <GuideText :text="text" />
      <div class="alert alert-light border mt-4">🚧 {{ stub }}</div>
    </div>
  </template>
</template>
