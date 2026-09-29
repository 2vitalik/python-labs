<script setup>
import { computed, nextTick, ref } from 'vue'

import { hasDrafts, textOf } from '../drafts.js'
import { user } from '../user.js'
import DraftsToggle from './DraftsToggle.vue'
import GuideEditor from './GuideEditor.vue'
import GuideText from './GuideText.vue'

// guide text with its admin tools: ✏️ on headings (renderMd) and «сторінку» open one inline editor at a time;
// the saved page comes back through v-model:page. The admin's text is with drafts or without (drafts.js)
const props = defineProps({ page: Object, prefix: { type: String, default: '' }, tools: { type: Boolean, default: true } })
const emit = defineEmits(['update:page'])
const admin = computed(() => user.value?.status === 'admin')
const text = computed(() => textOf(props.page))
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
      <template v-if="hasDrafts(page)"><DraftsToggle /> · </template>
      <a href="#" @click.prevent="edit('')">✏️ редагувати</a> ·
      <RouterLink :to="{ path: '/method/history', query: { slug: page.slug } }">🕘 історія</RouterLink>
    </div>
    <GuideEditor v-if="editing !== null" ref="editor" :key="editing" :page :id="editing" :prefix
                 @saved="saved" @close="editing = null" />
    <GuideText v-if="text" :text :prefix :editable="admin" @edit="edit" />
    <p v-else class="text-secondary">Без чернеток тут порожньо</p>
  </div>
</template>

<style scoped>
/* optically midway between the heading above and the text: the full-width line below pulls harder than the short heading */
.tools { margin: -.75rem 0 .5rem; }
.tools a { color: var(--bs-tertiary-color); text-decoration: none; }
.tools a:hover { color: var(--bs-body-color); }
</style>
