<script setup>
import { computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { getGuideHistory, getGuidePage, putGuidePage } from '../api.js'
import Crumbs from '../components/Crumbs.vue'
import Diff from '../components/Diff.vue'
import { diffLines } from '../diff.js'
import { ALL, loadGuide, pages } from '../guide.js'

// every save of every guide page, newest first (?slug= narrows to one page); ↩ brings the text back as a new save
const route = useRoute()
const router = useRouter()
const items = ref([])
const open = ref({})
const error = ref('')
const slug = computed(() => route.query.slug || '')
const options = computed(() => [{ slug: 'home' }, ...ALL].map((s) => [s.slug, pages.value[s.slug]?.title || s.slug]))
const rows = computed(() => items.value.map((e) => {
  const d = diffLines(e.old || '', e.new || '')
  return { ...e, add: d.filter((r) => r.t === '+').length, del: d.filter((r) => r.t === '-').length }
}))
const when = (iso) => new Date(iso).toLocaleString('uk-UA', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' })
const path = (s) => (s === 'home' ? '/' : s === 'changes-draft' ? '/changes' : ALL.find((a) => a.slug === s)?.path || '/method')
const pick = (s) => router.replace({ query: s ? { slug: s } : {} })

async function load() {
  items.value = await getGuideHistory(slug.value)
}
async function revert(e) {
  if (!confirm(`Зробити «${e.title}» таким, як до правки від ${when(e.at)}? Це нова правка, історія лишається.`)) return
  error.value = ''
  try {
    const p = await getGuidePage(e.slug)
    await putGuidePage(e.slug, { title: p.title, body: e.old, rev: p.rev, note: `відкат до ${when(e.at)}` })
    await load()
  } catch (err) {
    error.value = err.message
  }
}
watch(slug, load, { immediate: true })
loadGuide()
</script>

<template>
  <div>
    <Crumbs :items="[['/method', 'Методичка'], 'Історія']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h2 mb-0 me-auto">Історія правок</h1>
      <select class="form-select form-select-sm w-auto" :value="slug" @change="pick($event.target.value)">
        <option value="">усі сторінки</option>
        <option v-for="[s, t] in options" :key="s" :value="s">{{ t }}</option>
      </select>
    </div>
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <div v-for="e in rows" :key="e.id" class="border rounded mb-2">
      <div class="d-flex flex-wrap align-items-center gap-2 px-3 py-2">
        <span class="text-secondary small">{{ when(e.at) }}</span>
        <span class="small">{{ e.actor }}</span>
        <RouterLink :to="path(e.slug)">{{ e.title }}</RouterLink>
        <i v-if="e.note" class="text-secondary">{{ e.note }}</i>
        <span v-if="e.old_title != null" class="small text-secondary">назва: {{ e.old_title }} → {{ e.new_title }}</span>
        <span class="ms-auto small font-monospace"><span class="text-success">+{{ e.add }}</span> <span class="text-danger">−{{ e.del }}</span></span>
        <a v-if="e.new != null" href="#" class="small" @click.prevent="open[e.id] = !open[e.id]">{{ open[e.id] ? 'сховати' : 'зміни' }}</a>
        <button v-if="e.old != null" class="btn btn-outline-secondary btn-sm py-0" @click="revert(e)"
                title="Повернути текст до стану перед цією правкою (як нова правка)">↩</button>
      </div>
      <Diff v-if="open[e.id]" :old="e.old" :new="e.new" class="border-top px-3 py-2" />
    </div>
    <p v-if="!rows.length" class="text-secondary text-center mt-4">Правок ще не було.</p>
  </div>
</template>
