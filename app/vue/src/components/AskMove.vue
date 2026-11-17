<script setup>
import { computed, ref } from 'vue'

import Pop from '@core/components/Pop.vue'
import { cardItems } from '../items.js'
import Picker from './Picker.vue'

// «перенести на іншу картку» of a request (T319): a card of the same kind that already covers it — «це вже „Збирання“»;
// emits pick(slug). The default slot is the trigger: it gets `toggle`
const props = defineProps({ task: Object })
const emit = defineEmits(['pick'])
const open = ref(false)
const items = computed(() => (open.value ? cardItems([props.task.kind]).filter((it) => it.key !== props.task.slug) : []))
function pick(it) {
  open.value = false
  emit('pick', it.key)
}
</script>

<template>
  <Pop v-model="open" width="24rem">
    <template #trigger="{ toggle }"><slot :toggle /></template>
    <div class="small text-secondary">Картка того самого типу, яка це вже покриває</div>
    <Picker inline autofocus :items placeholder="пошук картки…" @pick="pick" />
  </Pop>
</template>
