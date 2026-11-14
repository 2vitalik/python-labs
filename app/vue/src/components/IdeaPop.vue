<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import Pop from '@core/components/Pop.vue'
import { canAccess } from '@core/user.js'
import IdeaForm from './IdeaForm.vue'

// «💡» of /tasks (T274 §4): the idea form in a panel, its subject already filled; only for those who may open /ideas.
// The trigger is the slot: <IdeaPop v-slot="{ toggle }"><button @click="toggle">…</button></IdeaPop>
defineProps({ kind: String, zone: String, subzone: String, task: String, note: String })  // note — the text the form starts with
const router = useRouter()
const allowed = computed(() => canAccess(router.resolve('/ideas').meta.access))
const open = ref(false)
</script>

<template>
  <Pop v-if="allowed" v-model="open" width="24rem">
    <template #trigger="{ toggle }"><slot :toggle /></template>
    <IdeaForm :kind :zone :subzone :task :note compact @done="open = false" @cancel="open = false" />
  </Pop>
</template>
