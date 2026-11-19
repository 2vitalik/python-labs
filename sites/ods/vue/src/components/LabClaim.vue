<script setup>
import { computed, onMounted, ref } from 'vue'

import { claimLab, getLabFree } from '../api.js'
import LabDrop from './LabDrop.vue'

// no card yet (T354 §5): the student names their number — the same in every lab — or hands in the notebook and the
// site reads the variant out of it. Nothing to pick: the demo for the teacher and test students, else what is missing
// (a group in the profile, the group's cards). `why` — the API's words, shown only if /free cannot be read
const props = defineProps({ n: Number, why: String })
const emit = defineEmits(['got'])
const free = ref(null)  // {group, own, free: [n…], same, demo: vid | null}
const pick = ref('')
const busy = ref(false)
const error = ref('')
const stuck = computed(() => free.value && !free.value.free.length && !free.value.demo)  // a file would not help either

onMounted(async () => {
  try {
    free.value = await getLabFree(props.n)
    pick.value = free.value.same ?? ''
  } catch (e) {
    error.value = e.message
  }
})

async function claim(num) {
  busy.value = true
  error.value = ''
  try {
    emit('got', await claimLab(props.n, num))
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
    <p v-if="!free && why" class="small text-secondary mb-1">{{ why }}</p>
    <p>Номер варіанта — це твій номер у списку потоку; він той самий у кожній лабі.</p>
    <template v-if="free">
      <div v-if="free.free.length" class="d-flex flex-wrap align-items-center gap-2 mb-2">
        <select v-model="pick" class="form-select w-auto" :aria-label="`Вільні номери потоку ${free.group}`">
          <option value="" disabled>мій номер</option>
          <option v-for="k in free.free" :key="k" :value="k">{{ k }}<template v-if="k === free.same"> — як в іншій лабі</template></option>
        </select>
        <button type="button" class="btn btn-primary" :disabled="pick === '' || busy" @click="claim(Number(pick))">Це мій варіант</button>
        <span class="small text-secondary">вільні номери потоку {{ free.group }}</span>
      </div>
      <div v-else-if="free.demo" class="mb-2">
        <button type="button" class="btn btn-primary" :disabled="busy" @click="claim(0)">Взяти демо-варіант {{ free.demo }}</button>
        <div class="small text-secondary mt-1">для перевірки сторінки: справжні студенти беруть свій номер</div>
      </div>
      <p v-else-if="!free.own">У профілі немає групи — <RouterLink to="/my/profile">впиши її в профілі</RouterLink>, і тут зʼявляться
        номери твого потоку.</p>
      <p v-else-if="!free.group">Для групи {{ free.own }} карток ще нема — напиши викладачеві.</p>
      <p v-else>Вільних номерів у потоці {{ free.group }} нема — напиши викладачеві.</p>
    </template>
    <p v-if="error" class="text-danger">{{ error }}</p>
    <template v-if="!stuck">
      <p class="mt-3 mb-2">…або просто завантаж свій ноутбук — сайт прочитає варіант із нього:</p>
      <LabDrop :n @got="emit('got', $event)" />
    </template>
  </section>
</template>
