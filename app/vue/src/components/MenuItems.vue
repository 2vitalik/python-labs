<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import MenuForm from './MenuForm.vue'

// the menu of a window to read: each item and where it leads — another window (a click goes there) or an action card;
// the owner edits it in place (MenuForm). `menu` — the Part of kind menu hosted on this window, if there is one yet
const props = defineProps({ window: Object, menu: Object })
const ed = useEd()
const edit = ref(false)
const items = computed(() => props.menu?.items || [])
const winTitle = (id) => ed.windows.find((w) => w.id === id)?.title
</script>

<template>
  <div v-if="items.length || ed.editable" class="small">
    <MenuForm v-if="edit" :window :menu @done="edit = false" @cancel="edit = false" />
    <div v-else-if="items.length" class="d-flex align-items-start gap-2">
      <div class="list">
        <div class="text-secondary fw-semibold">Меню</div>
        <div v-for="(it, i) in items" :key="i">
          {{ it.title }}
          <a v-if="winTitle(it.window)" href="#" class="text-decoration-none ms-1" @click.prevent="jump('p-' + it.window)">→ 🪟 {{ winTitle(it.window) }}</a>
          <span v-else-if="it.window" class="text-secondary ms-1">→ 🪟 вікна вже нема</span>
          <span v-else-if="it.task" class="ms-1" :title="ed.info(it.task)?.description">⚙ {{ ed.info(it.task)?.title || it.task }}</span>
          <span v-if="it.note" class="text-secondary ms-1">· {{ it.note }}</span>
        </div>
      </div>
      <button v-if="ed.editable" type="button" class="iact" title="Редагувати меню" @click="edit = true"><Icon name="pencil" /></button>
    </div>
    <button v-else type="button" class="btn btn-sm btn-add" @click="edit = true"><Icon name="plus" /> пункти меню</button>
  </div>
</template>

<style scoped>
.list { flex-grow: 1; min-width: 0; overflow-wrap: anywhere; }
</style>
