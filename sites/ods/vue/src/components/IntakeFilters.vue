<script setup>
import { computed } from 'vue'

import { vHint } from '@core/hint.js'

import { count, labsOf, SHOWS, skippedOf } from '../intake.js'

// «Показати»: one of SHOWS and, apart from them, a lab; each count is what its pill would show with the other choice
// kept. The rows set aside hide behind every pill until «показати відкладені»
const props = defineProps({ people: Array, f: Object })
const emit = defineEmits(['set'])
const labs = computed(() => labsOf(props.people))
const skipped = computed(() => skippedOf(props.people))
const n = (patch) => count(props.people, { ...props.f, ...patch })
const chip = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')
</script>

<template>
  <div class="d-flex flex-wrap align-items-center gap-1 mb-3">
    <span class="small text-secondary me-1">Показати</span>
    <button v-for="(s, k) in SHOWS" :key="k" v-hint="s[1]" type="button" class="btn btn-sm chip" :class="chip(f.show === k)"
            :aria-pressed="f.show === k" @click="emit('set', { show: k === 'all' ? undefined : k })">
      {{ s[0] }} <span class="opacity-75">{{ n({ show: k }) }}</span></button>
    <template v-if="labs.length">
      <span class="mx-1 text-secondary">·</span>
      <button v-for="l in labs" :key="l" v-hint="`файли лаби ${l}`" type="button" class="btn btn-sm chip" :class="chip(f.lab === l)"
              :aria-pressed="f.lab === l" @click="emit('set', { lab: f.lab === l ? undefined : String(l) })">
        лаба {{ l }} <span class="opacity-75">{{ n({ lab: l }) }}</span></button>
    </template>
    <button v-if="skipped" type="button" class="dot small ms-2" @click="emit('set', { skipped: f.skipped ? undefined : '1' })">
      {{ f.skipped ? 'сховати' : 'показати' }} відкладені · {{ skipped }}</button>
  </div>
</template>
