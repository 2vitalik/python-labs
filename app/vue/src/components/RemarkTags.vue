<script setup>
import { ref } from 'vue'

import Pop from '@core/components/Pop.vue'
import { TONES, vocab, word } from '../defense.js'
import '../remark.css'

// a remark's tags (T328 §2): the first one leads — its colour, its group. The teacher's click opens the whole list with
// what each tag is about; two at most — a third takes the second one's place
const props = defineProps({ tags: { type: Array, default: () => [] }, can: Boolean })
const emit = defineEmits(['set'])
const open = ref(false)
const pick = (key) => emit('set', props.tags.includes(key) ? props.tags.filter((t) => t !== key) : [...props.tags.slice(0, 1), key])
</script>

<template>
  <Pop v-if="can" v-model="open" width="23rem">
    <template #trigger="{ toggle }">
      <button type="button" class="rbare tags" title="Про що зауваження — клік змінює" @click="toggle">
        <span v-for="t in tags" :key="t" class="rtag" :class="TONES[t]">{{ word('tags', t)?.text || t }}</span>
        <span v-if="!tags.length" class="rtag none">＋ тег</span>
      </button>
    </template>
    <div class="rpick">
      <button v-for="t in vocab.tags" :key="t.key" type="button" :class="{ on: tags.includes(t.key) }" @click="pick(t.key)">
        <span><span class="rtag" :class="TONES[t.key]">{{ t.text }}</span></span><span class="hint">{{ t.hint }}</span>
      </button>
    </div>
  </Pop>
  <span v-else class="tags">
    <span v-for="t in tags" :key="t" class="rtag" :class="TONES[t]" :title="word('tags', t)?.hint">{{ word('tags', t)?.text || t }}</span>
  </span>
</template>

<style scoped>
.tags { display: inline-flex; flex-wrap: wrap; gap: .2rem; }
</style>
