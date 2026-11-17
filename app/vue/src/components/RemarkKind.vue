<script setup>
import { computed, ref } from 'vue'

import Pop from '@core/components/Pop.vue'
import { COINS } from '../catalog.js'
import { vocab, word } from '../defense.js'
import '../remark.css'

// what a remark asks of the student (T328 §3): a debt · better · a quest · a tip — and, where the course lets it, the coin
// for the rework (T329 §2). The teacher's click opens both lists, each line with what it means
const props = defineProps({ r: Object, can: Boolean })
const emit = defineEmits(['set'])
const open = ref(false)
const paid = computed(() => vocab.value.coins !== 'off' && vocab.value.paid.includes(props.r.kind))
const set = (patch) => { open.value = false; emit('set', patch) }
</script>

<template>
  <Pop v-if="can" v-model="open" width="24rem">
    <template #trigger="{ toggle }">
      <button type="button" class="rbare rkind" :class="r.kind" title="Що це означає для студента — клік змінює" @click="toggle">
        {{ word('remark_kinds', r.kind)?.text }}<span v-if="r.coin" :title="`за доробку: ${r.amount} × ${COINS[r.coin]}`">{{ COINS[r.coin] }}</span>
      </button>
    </template>
    <div class="rpick">
      <button v-for="k in vocab.remark_kinds" :key="k.key" type="button" :class="{ on: r.kind === k.key }" @click="set({ kind: k.key })">
        <span class="rkind" :class="k.key">{{ k.text }}</span><span class="hint">{{ k.hint }}</span>
      </button>
    </div>
    <template v-if="paid">
      <div class="sub">Монетка за доробку — бачиш лише ти</div>
      <div class="rpick">
        <button v-for="e in vocab.efforts" :key="e.coin" type="button" :class="{ on: r.coin === e.coin }" @click="set({ coin: e.coin })">
          <span>{{ COINS[e.coin] }}</span><span class="hint">{{ e.text }}</span>
        </button>
        <button type="button" :class="{ on: !r.coin }" @click="set({ coin: '' })"><span>—</span><span class="hint">без монетки</span></button>
      </div>
    </template>
  </Pop>
  <span v-else class="rkind" :class="r.kind" :title="word('remark_kinds', r.kind)?.hint">{{ word('remark_kinds', r.kind)?.text }}<span v-if="r.coin">{{ COINS[r.coin] }}</span></span>
</template>

<style scoped>
.sub { margin: .5rem .4rem .15rem; font-size: .72rem; color: var(--bs-secondary-color); }
</style>
