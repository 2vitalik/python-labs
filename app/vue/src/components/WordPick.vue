<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { wordItems } from '../items.js'
import { specOf } from '../rules.js'
import Picker from '@core/components/Picker.vue'

// a word of the sentence (trigger · condition · effect): a button with the chosen word, the searchable list in a panel over the page
const props = defineProps({ dic: String, placeholder: { type: String, default: 'слово…' } })
const model = defineModel({ type: String, default: '' })
const open = ref(false)
const label = computed(() => specOf(props.dic, model.value)?.label)
const items = computed(() => wordItems(props.dic).map((it) => ({ ...it, taken: it.key === model.value })))
function pick(it) {
  model.value = it.key
  open.value = false
}
</script>

<template>
  <Pop v-model="open" width="20rem">
    <template #trigger="{ toggle }">
      <button type="button" class="btn btn-sm btn-outline-secondary word" :class="{ empty: !label }" @click="toggle">
        {{ label || placeholder }}<Icon name="down" class="chev" />
      </button>
    </template>
    <Picker inline autofocus small :items placeholder="пошук слова…" @pick="pick" />
  </Pop>
</template>

<style scoped>
.word { --bs-btn-color: var(--bs-body-color); --bs-btn-padding-y: .1rem; white-space: nowrap; }
.word.empty { --bs-btn-color: var(--bs-secondary-color); font-style: italic; }
.chev { opacity: .55; }
</style>
