<script setup>
import { computed } from 'vue'

import '../defense.css'

// a scale of steps in words (T327 §4): a click sets a step, a click on the dot between two — «між ними»; what the step
// means stands beside — a number alone would mean whatever the mood was. A second click takes the step back
const props = defineProps({ steps: Array, value: Number })
const emit = defineEmits(['set'])
const set = (v) => emit('set', props.value === v ? 0 : v)
const hint = computed(() => {
  const v = props.value
  if (!v) return ''
  return Number.isInteger(v) ? props.steps[v - 1].hint : `між «${props.steps[v - 1.5].text}» і «${props.steps[v - 0.5].text}»`
})
</script>

<template>
  <span class="steps">
    <template v-for="(s, i) in steps" :key="i">
      <button v-if="i" type="button" class="mid" :class="{ on: value === i + 0.5 }" :title="`між «${steps[i - 1].text}» і «${s.text}»`" @click="set(i + 0.5)"></button>
      <button type="button" class="dchip" :class="{ on: value === i + 1, near: value === i + 0.5 || value === i + 1.5 }" :title="s.hint" @click="set(i + 1)">{{ s.text }}</button>
    </template>
    <span class="dhint ms-1">{{ hint }}</span>
  </span>
</template>

<style scoped>
.steps { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem 0; }
.mid { position: relative; width: .9rem; height: 1.5rem; padding: 0; border: 0; background: none; }
.mid::before { content: ''; position: absolute; inset: 50% auto auto 50%; width: .34rem; height: .34rem; border-radius: 50%; translate: -50% -50%;
               background: var(--bs-border-color); }
.mid:hover::before { background: var(--bs-secondary-color); }
.mid.on::before { width: .6rem; height: .6rem; background: var(--bs-primary); }
</style>
