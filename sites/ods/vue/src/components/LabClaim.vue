<script setup>
import { onMounted, ref } from 'vue'

import { claimLab, getLabFree } from '../api.js'
import LabDrop from './LabDrop.vue'

// no card yet (T354 §5): the student names their number — the same in every lab — or hands in the notebook and the
// site reads the variant out of it; `why` — the API's words for the missing card, `got` — MY once there is one
const props = defineProps({ n: Number, why: String })
const emit = defineEmits(['got'])
const free = ref(null)  // {group, free: [n…], same}
const pick = ref('')
const busy = ref(false)
const error = ref('')

onMounted(async () => {
  try {
    free.value = await getLabFree(props.n)
    pick.value = free.value.same ?? ''
  } catch (e) {
    error.value = e.message
  }
})

async function claim() {
  busy.value = true
  error.value = ''
  try {
    emit('got', await claimLab(props.n, Number(pick.value)))
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <section>
    <h2 class="h5">Який у тебе варіант?</h2>
    <p v-if="why" class="small text-secondary mb-1">{{ why }}</p>
    <p>Номер варіанта — це твій номер у списку потоку; він той самий у кожній лабі.</p>
    <div v-if="free?.free.length" class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <select v-model="pick" class="form-select w-auto" :aria-label="`Вільні номери потоку ${free.group}`">
        <option value="" disabled>мій номер</option>
        <option v-for="k in free.free" :key="k" :value="k">{{ k }}<template v-if="k === free.same"> — як в іншій лабі</template></option>
      </select>
      <button type="button" class="btn btn-primary" :disabled="pick === '' || busy" @click="claim">Це мій варіант</button>
      <span class="small text-secondary">вільні номери потоку {{ free.group }}</span>
    </div>
    <p v-else-if="free" class="text-secondary">Вільних номерів у потоці {{ free.group }} нема — скажи викладачеві.</p>
    <p v-if="error" class="text-danger">{{ error }}</p>
    <p class="mt-3 mb-2">…або просто завантаж свій ноутбук — сайт прочитає варіант із нього:</p>
    <LabDrop :n @got="emit('got', $event)" />
  </section>
</template>
