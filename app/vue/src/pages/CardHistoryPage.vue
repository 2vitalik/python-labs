<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { getCardHistory, revertCard } from '../api.js'
import { FIELDS } from '../cardFields.js'
import { loadCatalog } from '../catalog.js'
import CardChange from '../components/CardChange.vue'
import Crumbs from '@core/components/Crumbs.vue'

// every edit of every task or game, newest first (?slug= narrows to one); ↩ puts the old values back as a new edit
const KINDS = {
  tasks: { nav: 'Таски', title: 'Історія завдань', to: (slug) => `/tasks/${slug}/edit` },
  games: { nav: 'Ігри', title: 'Історія ігор', to: (slug) => `/games/${slug}` },
}
const route = useRoute()
const kind = computed(() => route.meta.kind)
const slug = computed(() => route.query.slug || '')
const items = ref(null)  // null — not loaded yet: «Правок ще не було» is not said before the answer
const open = ref({})
const error = ref('')
const when = (iso) => new Date(iso).toLocaleString('uk-UA', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
const fields = (e) => Object.keys(e.changes).map((k) => (FIELDS[k] || k).toLowerCase()).join(', ')

async function load() {
  items.value = await getCardHistory(kind.value, slug.value)
}
async function revert(e) {
  if (!confirm(`Повернути «${e.title}» до стану перед правкою від ${when(e.at)}? Це нова правка, історія лишається.`)) return
  error.value = ''
  try {
    await revertCard(kind.value, e.id)
    await Promise.all([load(), loadCatalog()])
  } catch (err) {
    error.value = err.message
  }
}
watch([kind, slug], load, { immediate: true })
loadCatalog()
</script>

<template>
  <div>
    <Crumbs :items="[['/method', 'Методичка'], [`/${kind}`, KINDS[kind].nav], 'Історія']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h2 mb-0 me-auto">{{ KINDS[kind].title }}<span v-if="slug" class="text-secondary fs-5"> · {{ items?.[0]?.title || slug }}</span></h1>
      <RouterLink v-if="slug" :to="route.path" class="small">усі правки</RouterLink>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-for="e in items" :key="e.id" class="border rounded mb-2">
      <div class="d-flex flex-wrap align-items-center gap-2 px-3 py-2">
        <span class="text-secondary small">{{ when(e.at) }}</span>
        <span class="small">{{ e.actor }}</span>
        <RouterLink :to="KINDS[kind].to(e.slug)">{{ e.title }}</RouterLink>
        <RouterLink v-if="!slug" :to="{ query: { slug: e.slug } }" class="text-decoration-none small" title="Лише правки цього запису">🕘</RouterLink>
        <i v-if="e.note" class="text-secondary">{{ e.note }}</i>
        <span v-else class="small text-secondary">{{ e.created ? 'створено' : fields(e) }}</span>
        <span class="ms-auto d-flex align-items-center gap-2">
          <a href="#" class="small" @click.prevent="open[e.id] = !open[e.id]">{{ open[e.id] ? 'сховати' : 'зміни' }}</a>
          <button v-if="!e.created" class="btn btn-outline-secondary btn-sm py-0" @click="revert(e)"
                  title="Повернути ці поля до стану перед цією правкою (як нова правка)">↩</button>
        </span>
      </div>
      <CardChange v-if="open[e.id]" :changes="e.changes" class="border-top px-3 py-2" />
    </div>
    <p v-if="items && !items.length" class="text-secondary text-center mt-4">Правок ще не було.</p>
  </div>
</template>
