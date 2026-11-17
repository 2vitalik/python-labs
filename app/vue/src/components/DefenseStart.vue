<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { getStudents } from '@core/api.js'
import Avatar from '@core/components/Avatar.vue'
import Icon from '@core/components/Icon.vue'
import { matches } from '@core/studentSearch.js'
import { postDefense } from '../api.js'
import { vocab } from '../defense.js'
import '../defense.css'

// «Почати захист» (T327 §5): a few letters find the student, a click picks them, the labs and the kind are chips —
// and the defense starts now, on its own page
const emit = defineEmits(['cancel'])
const router = useRouter()
const students = ref([])
const q = ref('')
const who = ref(null)
const labs = ref([])
const kind = ref('online')
const error = ref('')
const vFocus = { mounted: (el) => el.focus() }
const found = computed(() => (q.value.trim() ? students.value.filter((s) => matches(s, q.value)).slice(0, 7) : []))
const lab = (n) => (labs.value = labs.value.includes(n) ? labs.value.filter((x) => x !== n) : [...labs.value, n])
async function start() {
  try {
    const d = await postDefense({ nick: who.value.nick, labs: labs.value, kind: kind.value })
    router.push(`/defenses/${d.id}`)
  } catch (e) {
    error.value = e.message
  }
}
onMounted(async () => { students.value = (await getStudents()).filter((s) => s.status === 'student') })
</script>

<template>
  <div class="card editing new mb-3"><div class="card-body py-2">
    <template v-if="!who">
      <input v-model="q" v-focus class="form-control" placeholder="Хто захищається: прізвище, імʼя або нік" @keydown.esc="emit('cancel')"
             @keydown.enter="found.length === 1 && (who = found[0])">
      <button v-for="s in found" :key="s.nick" type="button" class="pick" @click="who = s">
        <Avatar :user="s" :size="24" /> <span>{{ s.name }}</span> <span class="dhint">{{ s.group }}</span>
      </button>
      <div v-if="q.trim() && !found.length" class="dhint mt-1">Нікого не знайдено</div>
    </template>
    <template v-else>
      <div class="d-flex align-items-center gap-2 mb-1">
        <Avatar :user="who" :size="28" /> <b>{{ who.name }}</b> <span class="dhint">{{ who.group }}</span>
        <button type="button" class="more-field ms-1" @click="who = null">інший студент</button>
      </div>
      <div class="drow"><span class="dlbl">Лаби</span><span class="d-flex flex-wrap gap-1">
        <button v-for="n in vocab.labs" :key="n" type="button" class="dchip" :class="{ on: labs.includes(n) }" @click="lab(n)">{{ n }}</button></span></div>
      <div class="drow"><span class="dlbl">Вид захисту</span><span class="d-flex flex-wrap gap-1">
        <button v-for="k in vocab.kinds" :key="k.key" type="button" class="dchip" :class="{ on: kind === k.key }" @click="kind = k.key">{{ k.text }}</button></span></div>
    </template>
    <div class="d-flex gap-2 mt-2">
      <button type="button" class="btn btn-sm btn-add" :disabled="!who" @click="start"><Icon name="play" /> Почати зараз</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
    </div>
    <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
  </div></div>
</template>

<style scoped>
.pick { display: flex; align-items: center; gap: .5rem; width: 100%; padding: .25rem .4rem; border: 0; border-radius: .3rem; background: none; color: inherit; text-align: left; }
.pick:hover { background: var(--bs-tertiary-bg); }
</style>
