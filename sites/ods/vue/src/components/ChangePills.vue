<script setup>
import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'

// a row of the filters: its word at the left, its values as pills — pressed grey like every filter, the colour only in the
// dot that says what the value is (a group, a level); the number — what the pill would leave, 0 greys it
defineProps({ label: String, pills: Array, on: { type: Array, default: () => [] } })
const emit = defineEmits(['pick'])
</script>

<template>
  <div class="frow">
    <span class="flabel">{{ label }}</span>
    <div class="fpills">
      <button v-for="p in pills" :key="p.v" v-hint="p.hint" type="button" class="btn btn-sm chip"
              :class="[on.includes(p.v) ? 'btn-secondary' : 'btn-outline-secondary', { zero: !p.n && !on.includes(p.v) }]"
              :aria-pressed="on.includes(p.v)" @click="emit('pick', p.v)">
        <span v-if="p.color" class="g-dot" :style="{ '--c': `var(--g-${p.color})` }" /><span v-if="p.sev" class="sev-dot" :class="`s${p.sev}`" />
        <Icon v-if="p.icon" :name="p.icon" />{{ p.text }}<span v-if="p.n !== undefined" class="n">{{ p.n || 0 }}</span>
      </button>
      <slot />
    </div>
  </div>
</template>
