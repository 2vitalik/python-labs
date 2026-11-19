<script setup>
import { computed, ref, watch } from 'vue'

import Reveal from '@core/components/Reveal.vue'
import SaveCancel from '@core/components/SaveCancel.vue'

import { putMyLab } from '../api.js'
import { WAYS } from '../labText.js'

// «Захист»: how the student means to defend (T228) — saved on the click itself; a record wants its link
const props = defineProps({ n: Number, lab: Object })
const emit = defineEmits(['got'])
const CHOICES = [['none', 'Без захисту', 'до 12 балів'], ['record', 'Записом', 'відкриває 14 і 16'], ['live', 'Наживо', 'відкриває 18 і 20']]
const way = ref(props.lab.way || '')
const video = ref(props.lab.video || '')
const busy = ref(false)
const error = ref('')
const changed = computed(() => video.value.trim() !== (props.lab.video || ''))
watch(() => props.lab.video, (v) => (video.value = v || ''))
watch(() => props.lab.way, (w) => (way.value = w || ''))

async function put(data, undo) {
  busy.value = true
  error.value = ''
  try {
    emit('got', await putMyLab(props.n, data))
  } catch (e) {
    error.value = e.message
    undo()
  } finally {
    busy.value = false
  }
}
function choose(k) {
  const was = way.value
  way.value = k
  put({ way: k }, () => (way.value = was))
}
const saveVideo = () => put({ video: video.value.trim() }, () => {})
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Захист</h2>
    <div class="row g-2" role="radiogroup" aria-label="Як захищатимешся">
      <div v-for="[k, title, sub] in CHOICES" :key="k" class="col-sm-4">
        <label class="way-c" :class="{ on: way === k }">
          <input type="radio" name="lab-way" class="form-check-input" :value="k" :checked="way === k" :disabled="busy" @change="choose(k)">
          <span><b>{{ title }}</b><span class="d-block small text-secondary">{{ sub }}</span></span>
        </label>
      </div>
    </div>
    <Reveal :show="way === 'record'">
      <div class="pt-2">
        <label class="form-label mb-1" for="lab-video">Посилання на запис</label>
        <input id="lab-video" v-model="video" class="form-control" maxlength="300" placeholder="https://…">
        <SaveCancel class="mt-1" :class="{ invisible: !changed }" :disabled="busy" @save="saveVideo" @cancel="video = lab.video || ''" />
      </div>
    </Reveal>
    <p v-if="error" class="text-danger small mt-1 mb-0">{{ error }}</p>
    <p v-if="WAYS[lab.defended]" class="mt-2 mb-0">Викладач зарахував захист: <b>{{ WAYS[lab.defended] }}</b></p>
    <p class="small text-secondary mt-2 mb-0">Бали ставить викладач після захисту; це підказка за правилами лаби.<template
      v-if="typeof lab.grade?.hint === 'number'"> За цими правилами зараз виходить до <b>{{ lab.grade.hint }}</b>.</template></p>
  </section>
</template>

<style scoped>
.way-c { display: flex; align-items: flex-start; gap: .5rem; height: 100%; padding: .5rem .75rem; border: 1px solid var(--bs-border-color);
         border-radius: .5rem; cursor: pointer; transition: border-color .15s, background .15s; }
.way-c:hover { background: var(--bs-tertiary-bg); }
.way-c.on { border-color: var(--bs-primary); background: var(--bs-primary-bg-subtle); }
.way-c .form-check-input { margin-top: .25rem; flex-shrink: 0; }
</style>
