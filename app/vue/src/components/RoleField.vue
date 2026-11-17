<script setup>
import { computed, ref, watch } from 'vue'

import Pop from '@core/components/Pop.vue'
import { roleOf } from '../catalog.js'
import { roleItems } from '../items.js'
import Picker from './Picker.vue'
import ProposeCard from './ProposeCard.vue'

// an entity's type (T270 §7): a field-like button with the chosen type → the types with what each one is, by family;
// none fits — propose one to the teacher, and meanwhile the entity is an «object», so nobody is stuck.
// v-model:open — the list, for a page that opens it itself (EntityDraft: Enter before a type)
const role = defineModel({ type: String, default: '' })
const open = defineModel('open', { type: Boolean, default: false })
const proposing = ref(false)
const items = computed(() => roleItems().map((it) => ({ ...it, taken: it.key === role.value })))
watch(open, () => (proposing.value = false))
const pick = (it) => { role.value = it.key; open.value = false }
const proposed = () => { role.value = 'object'; open.value = false }
</script>

<template>
  <Pop v-model="open" width="24rem">
    <template #trigger="{ toggle }">
      <button type="button" class="form-select form-select-sm text-start text-truncate type" title="Тип сутності" @click="toggle">
        <template v-if="role">{{ roleOf(role).icon }} {{ roleOf(role).label }}</template>
        <span v-else class="text-secondary">обери тип: гравець, ворог, стіна…</span>
      </button>
    </template>
    <ProposeCard v-if="proposing" what="новий тип сутності" all-to="/tasks?zone=entities&sub=roles" zone="entities" subzone="roles"
                 @done="proposed" @cancel="proposing = false" />
    <Picker v-else inline autofocus :items placeholder="пошук типу…" @pick="pick">
      <template #footer>
        <div class="foot">Нема потрібного типу? <a href="#" @click.prevent="proposing = true">запропонувати</a></div>
      </template>
    </Picker>
  </Pop>
</template>

<style scoped>
.type { min-width: 10rem; }  /* beside the name in the form's top row (T291 §4) */
.foot { margin: .4rem .5rem .1rem; padding-top: .4rem; border-top: 1px solid var(--bs-border-color-translucent); font-size: .78rem; color: var(--bs-secondary-color); }
</style>
