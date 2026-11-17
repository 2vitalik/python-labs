<script setup>
import { onMounted } from 'vue'

import CopyNicks from '../components/CopyNicks.vue'
import Crumbs from '../components/Crumbs.vue'
import TableGrid from '../components/TableGrid.vue'
import TableSetup from '../components/TableSetup.vue'
import ViewHead from '../components/ViewHead.vue'
import ViewTabs from '../components/ViewTabs.vue'
import { createTable } from '../tableCtx.js'
import { useTitle } from '../title.js'
import { liveViews, load, store } from '../viewStore.js'
import { useViewWork } from '../viewWork.js'

// the table of students (T240, T315): one page, many views. The state lives in the URL, tableCtx.js reads it for every part:
// the tabs of views, the head of the one open, the line that says how it is set, the grid
const t = createTable()
useTitle(() => t.view && `Звід · ${t.view.title}`)
useViewWork(() => (t.view && !t.peek ? t.slug : ''))
onMounted(load)
</script>

<template>
  <div>
    <Crumbs :items="[['/students', 'Студенти'], 'Звід']" />
    <div v-if="store.error" class="alert alert-danger">{{ store.error }}</div>
    <template v-if="t.data">
      <ViewTabs />
      <template v-if="t.view">
        <ViewHead />
        <div class="d-flex align-items-start gap-2">
          <TableSetup class="flex-grow-1" />
          <CopyNicks :people="t.rows" class="flex-shrink-0" />  <!-- whoever the filters left: to call them in a chat -->
        </div>
        <TableGrid />
      </template>
      <p v-else class="text-secondary">Виду «{{ t.slug }}» нема.
        <RouterLink v-if="liveViews().length" :to="{ query: { view: liveViews()[0].slug } }">Відкрити «{{ liveViews()[0].title }}»</RouterLink>
      </p>
    </template>
  </div>
</template>
