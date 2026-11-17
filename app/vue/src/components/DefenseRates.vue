<script setup>
import { vocab } from '../defense.js'
import RateSteps from './RateSteps.vue'
import '../defense.css'

// the teacher's impressions (T327 §4), a click each, saved at once: scales — steps in words with a point between two,
// facts — what happened, not how good it was, marks — for memory. A second click on what is set takes it back.
// No student and no agent ever gets these
const props = defineProps({ d: Object })
const emit = defineEmits(['set'])
function fact(key, value) {
  const facts = { ...props.d.facts }
  if (facts[key] === value) delete facts[key]
  else facts[key] = value
  emit('set', { facts })
}
function rate(key, value) {
  const rates = { ...props.d.rates }
  if (value) rates[key] = value
  else delete rates[key]
  emit('set', { rates })
}
const mark = (key) => emit('set', { marks: props.d.marks.includes(key) ? props.d.marks.filter((x) => x !== key) : [...props.d.marks, key] })
</script>

<template>
  <div>
    <!-- facts first, «Загалом» last: what was seen is marked before what was felt, so the feeling colours it less -->
    <div class="dsub mt-0">Що було на захисті</div>
    <div v-for="f in vocab.facts" :key="f.key" class="fact">
      <span>{{ f.text }}</span>
      <span class="d-flex gap-1">
        <button v-for="a in vocab.answers" :key="a.key" type="button" class="dchip" :class="[a.key, { on: d.facts[f.key] === a.key }]" @click="fact(f.key, a.key)">{{ a.text }}</button>
      </span>
    </div>
    <div class="dsub">На якому рівні</div>
    <div v-for="r in vocab.rates" :key="r.key" class="drow">
      <span class="dlbl">{{ r.text }}</span>
      <RateSteps :steps="r.steps" :value="d.rates[r.key]" @set="(v) => rate(r.key, v)" />
    </div>
    <div class="dsub">Позначки для памʼяті</div>
    <div class="d-flex flex-wrap gap-1">
      <button v-for="m in vocab.marks" :key="m.key" type="button" class="dchip" :class="{ on: d.marks.includes(m.key) }" @click="mark(m.key)">{{ m.icon }} {{ m.text }}</button>
    </div>
  </div>
</template>

<style scoped>
.fact { display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: .2rem .8rem; padding: .2rem 0;
        border-bottom: 1px solid var(--bs-border-color-translucent); font-size: .88rem; }
</style>
