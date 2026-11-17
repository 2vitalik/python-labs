<script setup>
import { reactive, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import EmojiField from './EmojiField.vue'

// a legend's line in a panel over the palette (T276): its name for a known icon, or the icon and the name of a new one
// (`fresh`). The name is the legend's Markdown as it stands in the text: «**ключ** *(відчиняє двері)*». Enter saves —
// and does not send the game's form around it
const props = defineProps({ icon: String, name: String, fresh: Boolean })
const emit = defineEmits(['save'])
const open = ref(false)
const f = reactive({ icon: '', name: '' })
watch(open, (on) => on && Object.assign(f, { icon: props.icon || '', name: props.name || '' }))
function save() {
  if (!f.icon.trim() || !f.name.trim()) return
  emit('save', { icon: f.icon.trim(), name: f.name.trim() })
  open.value = false
}
</script>

<template>
  <Pop v-model="open" width="21rem">
    <template #trigger="{ toggle }"><slot :toggle /></template>
    <div class="vstack gap-2" @keydown.enter.prevent="save">
      <div class="d-flex align-items-center gap-2">
        <EmojiField v-if="fresh" v-model="f.icon" :hint="f.name" legend />
        <span v-else class="fs-5">{{ icon }}</span>
        <input v-model="f.name" class="form-control form-control-sm" placeholder="**ключ** *(відчиняє двері)*">
      </div>
      <div class="d-flex gap-2">
        <button type="button" class="btn btn-sm btn-success" :disabled="!f.icon.trim() || !f.name.trim()" @click="save"><Icon name="check" /> Зберегти</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false">Скасувати</button>
      </div>
    </div>
  </Pop>
</template>
