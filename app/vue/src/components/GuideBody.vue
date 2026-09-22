<script setup>
import { computed, nextTick, ref } from 'vue'

import { user } from '../user.js'
import GuideEditor from './GuideEditor.vue'
import GuideText from './GuideText.vue'

// guide text with its admin tools: ✏️ on headings (renderMd) and «сторінку» open one inline editor at a time;
// the saved page comes back through v-model:page
const props = defineProps({ page: Object, prefix: { type: String, default: '' }, tools: { type: Boolean, default: true } })
const emit = defineEmits(['update:page'])
const admin = computed(() => user.value?.status === 'admin')
const editing = ref(null)  // null · '' = whole page · heading id
const editor = ref()

function edit(id) {
  if (editor.value?.dirty && !confirm('Є незбережені зміни. Покинути їх?')) return
  editing.value = id
}
async function saved(p) {
  editing.value = null  // unmount the teleported editor before v-html replaces its slot
  await nextTick()
  emit('update:page', p)
}
</script>

<template>
  <div>
    <div v-if="admin && tools" class="tools small text-end">
      <a href="#" @click.prevent="edit('')">✏️ редагувати</a> ·
      <RouterLink :to="{ path: '/method/history', query: { slug: page.slug } }">🕘 історія</RouterLink>
    </div>
    <GuideEditor v-if="editing !== null" ref="editor" :key="editing" :page :id="editing" :prefix
                 @saved="saved" @close="editing = null" />
    <GuideText :text="page.body" :prefix :editable="admin" @edit="edit" />
  </div>
</template>

<style scoped>
.tools { margin-bottom: -.25rem; }
.tools a { color: var(--bs-tertiary-color); text-decoration: none; }
.tools a:hover { color: var(--bs-body-color); }
</style>
