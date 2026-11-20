<script setup>
import { computed, nextTick, ref } from 'vue'

import { hasDrafts, textOf } from '../drafts.js'
import { site } from '../site.js'
import { user } from '../user.js'
import DraftsToggle from './DraftsToggle.vue'
import GuideEditor from './GuideEditor.vue'
import GuideText from './GuideText.vue'
import Icon from './Icon.vue'

// guide text with its admin tools: ✏️ on headings (renderMd) and «сторінку» open one inline editor at a time;
// the saved page comes back through v-model:page. The admin's text is with drafts or without (drafts.js)
// `view` — the text as shown (not as edited): a lesson's summary without its h1; `put` — where the editor saves;
// `history` — the address of the text's history: the site's by default, '' = no such page
const props = defineProps({ page: Object, prefix: { type: String, default: '' }, tools: { type: Boolean, default: true }, view: Function,
                            put: Function, history: { type: String, default: null }, placeholder: String })
const emit = defineEmits(['update:page'])
const admin = computed(() => user.value?.status === 'admin')
const past = computed(() => props.history ?? site.history.path)
const text = computed(() => (props.view || ((t) => t))(textOf(props.page)))
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
      <a href="#" @click.prevent="edit('')"><Icon name="pencil" /> редагувати</a>
      <template v-if="past"> · <RouterLink :to="{ path: past, query: { slug: page.slug } }"><Icon name="clock" /> історія</RouterLink></template>
      <slot name="tools" />  <!-- the page's own links after these: « · <a>…</a>» -->
    </div>
    <GuideEditor v-if="editing !== null" ref="editor" :key="editing" :page :id="editing" :prefix :put :notitle="!past" :view
                 @saved="saved" @close="editing = null" />
    <GuideText v-if="text" :text :prefix :editable="admin" @edit="edit" />
    <p v-else class="text-secondary">{{ placeholder || (admin ? 'Без чернеток тут порожньо' : '🚧 Розділ ще готується') }}</p>
  </div>
</template>

<style scoped>
/* optically midway between the heading above and the text: the full-width line below pulls harder than the short heading */
.tools { margin: -.75rem 0 .5rem; }
.tools a, .tools :slotted(a) { color: var(--bs-tertiary-color); text-decoration: none; }  /* a page's own links look the same */
.tools a:hover, .tools :slotted(a:hover) { color: var(--bs-body-color); }
</style>
