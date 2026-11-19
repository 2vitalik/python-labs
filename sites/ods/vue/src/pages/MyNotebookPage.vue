<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import Crumbs from '@core/components/Crumbs.vue'
import Icon from '@core/components/Icon.vue'
import { fmtWhen } from '@core/labs.js'
import { useTitle } from '@core/title.js'

import { getLabFile, getMyLab, labFileRawUrl } from '../api.js'
import LabVersions from '../components/LabVersions.vue'
import LabWide from '../components/LabWide.vue'
import NotebookModes from '../components/NotebookModes.vue'
import NotebookView from '../components/NotebookView.vue'
import { nbMode } from '../labNb.js'
import { fmtSize } from '../labText.js'

// the student's notebook as the teacher sees it (T354): the file read by the site, not run — the outputs are the student's own
const route = useRoute()
const n = computed(() => Number(route.params.n))
const id = computed(() => route.params.id)
const nb = ref(null)
const files = ref([])
const error = ref('')
useTitle(() => nb.value?.file?.name || 'Мій ноутбук')

watch(id, async (v) => {
  error.value = ''
  try {
    nb.value = await getLabFile(v)
  } catch (e) {
    nb.value = null
    error.value = e.message
  }
}, { immediate: true })
onMounted(async () => (files.value = (await getMyLab(n.value).catch(() => null))?.files || []))
</script>

<template>
  <div>
    <Crumbs :items="[['/labs', 'Лаби'], [`/labs/${n}`, `Лаба ${n}`], [`/labs/${n}/my`, 'Моя лаба'], 'Ноутбук']"><LabWide /></Crumbs>
    <p v-if="error" class="text-danger">{{ error }}</p>
    <template v-if="nb">
      <h1 class="h3 mb-1">{{ nb.file?.name || 'Ноутбук' }}</h1>
      <p class="small text-secondary mb-3">
        <template v-if="nb.file">{{ fmtWhen(nb.file.at) }} · {{ fmtSize(nb.file.size) }} · </template>
        <a :href="labFileRawUrl(id)" download><Icon name="download" /> завантажити файл</a>
      </p>
      <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
        <NotebookModes v-model="nbMode" />
        <LabVersions v-if="files.length > 1" :files :current="id" :to="(f) => `/labs/${n}/my/nb/${f.id}`" />
      </div>
      <NotebookView :cells="nb.cells" :mode="nbMode" :tasks="nb.facts?.tasks" />
    </template>
  </div>
</template>
