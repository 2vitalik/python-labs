<script setup>
import { computed, ref } from 'vue'

// «@нік @нік …» of these people to the clipboard: to call them in the group's chat. Who has no nick is left out, and counted
const props = defineProps({ people: { type: Array, required: true } })
const nicks = computed(() => props.people.filter((p) => p.tg_username).map((p) => `@${p.tg_username}`))
const copied = ref(false)
async function copy() {
  await navigator.clipboard.writeText(nicks.value.join(' '))
  copied.value = true
  setTimeout(() => (copied.value = false), 2000)
}
</script>

<template>
  <button v-if="nicks.length" type="button" class="btn btn-outline-secondary btn-sm py-0" :title="`${nicks.length} з ${people.length} мають нік`" @click="copy">
    {{ copied ? `✓ скопійовано ${nicks.length}` : '📋 @ніки' }}
  </button>
</template>
