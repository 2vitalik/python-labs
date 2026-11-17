<script setup>
import { computed, ref, watch } from 'vue'

import Pop from '@core/components/Pop.vue'
import { useEd } from '../ed.js'
import { windowTypeItems } from '../items.js'
import CoinBadge from './CoinBadge.vue'
import Picker from './Picker.vue'
import ProposeCard from './ProposeCard.vue'

// a window's type, as RoleField is an entity's: a field-like button with the chosen type → the window types of the catalog;
// none fits — propose one to the teacher, and meanwhile the window is «своє вікно». v-model:open — the list
const task = defineModel({ type: String, default: '' })
const open = defineModel('open', { type: Boolean, default: false })
const ed = useEd()
const proposing = ref(false)
const type = computed(() => ed.info(task.value))
const items = computed(() => windowTypeItems().map((it) => ({ ...it, taken: it.key === task.value })))
watch(open, () => (proposing.value = false))
const pick = (slug) => { task.value = slug; open.value = false }
</script>

<template>
  <Pop v-model="open" width="24rem">
    <template #trigger="{ toggle }">
      <button type="button" class="form-select form-select-sm text-start text-truncate" title="Тип вікна" @click="toggle">
        <template v-if="type"><CoinBadge :coin="type.coin" :amount="type.amount" /> {{ type.title }}</template>
        <span v-else class="text-secondary">обери тип: головне меню, пауза, кінець гри…</span>
      </button>
    </template>
    <ProposeCard v-if="proposing" what="новий тип вікна" all-to="/tasks?zone=interface&sub=menus" zone="interface" subzone="menus"
                 @done="pick('custom-window')" @cancel="proposing = false" />
    <Picker v-else inline autofocus :items placeholder="головне меню, пауза, кінець гри…" @pick="pick($event.key)">
      <template #footer>
        <div class="foot">Нема потрібного типу? <a href="#" @click.prevent="proposing = true">запропонувати</a></div>
      </template>
    </Picker>
  </Pop>
</template>

<style scoped>
.foot { margin: .4rem .5rem .1rem; padding-top: .4rem; border-top: 1px solid var(--bs-border-color-translucent); font-size: .78rem; color: var(--bs-secondary-color); }
</style>
