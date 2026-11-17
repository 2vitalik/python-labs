<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import InlinePop from '@core/components/InlinePop.vue'
import { useEd } from '../ed.js'
import { cardItems } from '../items.js'
import CardSign from './CardSign.vue'
import Picker from './Picker.vue'

// where a transition leads (T270 §10.1, T278 §4), picked where it reads (T310): nowhere, another window of the game, or a
// card — an action that opens no window. `item` — the menu item ({ window, task }); `host` — the item's own window;
// `save({ window, task })` is awaited. Shown while the tools are on: at rest the same place is a link that leads there.
// v-model:open — a row not saved yet lives while its target is being picked (MenuItems, T318)
const props = defineProps({ item: Object, host: String, save: Function })
const ed = useEd()
const open = defineModel('open', { type: Boolean, default: false })
const ACTIONS = ['element', 'game', 'level', 'rule', 'mechanic', 'field']
const items = computed(() => (open.value ? [
  { key: '', title: 'нікуди — просто рядок', icon: '·', taken: !props.item.window && !props.item.task },
  ...ed.windows.filter((w) => w.id !== props.host)
    .map((w) => ({ key: `w:${w.id}`, title: w.title, icon: '🪟', desc: w.description, group: 'Вікна', taken: w.id === props.item.window })),
  ...cardItems(ACTIONS).map((it) => ({ ...it, key: `t:${it.key}`, group: 'Дія — картка каталогу', taken: it.key === props.item.task })),
] : []))
const winTitle = computed(() => ed.windows.find((w) => w.id === props.item.window)?.title)
const part = (key, mark) => (key.startsWith(mark) ? key.slice(2) : '')
const pick = (it, choose, close) => (it.taken ? close() : choose(props.save({ window: part(it.key, 'w:'), task: part(it.key, 't:') })))
</script>

<template>
  <InlinePop v-model:open="open" can width="24rem" tip="Клік — куди веде або що робить">
    <template v-if="winTitle">→ <Icon name="win" /> {{ winTitle }}</template>
    <span v-else-if="item.window" class="text-secondary">→ вікна вже нема</span>
    <template v-else-if="item.task">→ <CardSign :task="ed.info(item.task)" /> {{ ed.info(item.task)?.title || item.task }}</template>
    <span v-else class="inl-none">→ куди?</span>
    <template #panel="{ choose, close }"><Picker inline autofocus :items placeholder="вікно або картка-дія…" @pick="pick($event, choose, close)" /></template>
  </InlinePop>
</template>
