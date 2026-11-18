<script setup>
import { ref } from 'vue'

import { postPart } from '../api.js'
import { useEd } from '../ed.js'
import { landed } from '@core/jump.js'
import { setTools } from '../tools.js'
import SaveCancel from '@core/components/SaveCancel.vue'

// a new entity, window or level begins as the head of its card (T310): the sign, the name typed where it will stand, the
// type by it, «✕ / ✓» — in the frame of «add», tinted as the card's head (`zone` — the category's colour). Enter or ✓ —
// `enter`, Esc or ✕ — `cancel`. create(data) makes the part; the card is born in the list with its tools on, where the rest
// is added, and flashes there
defineProps({ zone: String, placeholder: String })
const title = defineModel({ type: String, default: '' })
const emit = defineEmits(['enter', 'cancel', 'done'])
const ed = useEd()
const input = ref()
const busy = ref(false)
const error = ref('')

async function create(data) {
  if (busy.value) return
  busy.value = true
  error.value = ''
  try {
    const saved = await postPart({ ...data, title: title.value.trim() })
    await ed.changed()
    setTools(saved.id, true)
    emit('done')  // in the same render as the card: the list does not show both
    landed(`p-${saved.id}`)
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
function key(e) {
  if (e.key === 'Escape') emit('cancel')
  else if (e.key === 'Enter' && !e.isComposing) {
    e.preventDefault()
    emit('enter')
  }
}
defineExpose({ create, focus: (o) => input.value?.focus(o) })
</script>

<template>
  <div class="card editing new draft" :style="{ '--z': zone }">
    <div class="head">
      <slot name="sign" />
      <div class="names">
        <input ref="input" v-model="title" class="form-control form-control-sm fw-semibold name" :placeholder :aria-label="placeholder"
               :readonly="busy" autocomplete="off" @keydown="key">
        <span v-if="$slots.type" class="kind"><slot name="type" /></span>
      </div>
      <SaveCancel class="acts" :disabled="busy || !title.trim()" @save="emit('enter')" @cancel="emit('cancel')" />
    </div>
    <div v-if="error" class="err text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.draft { background: color-mix(in srgb, var(--z, var(--bs-secondary-color)) 11%, var(--bs-body-bg)); }
.head { display: flex; align-items: center; gap: .5rem; padding: .3rem .4rem .3rem .65rem; }
/* the name and the type on one line while both fit, else the type goes under the name — as in the card's head */
.names { display: flex; flex: 1 1 0; flex-wrap: wrap; align-items: center; gap: .3rem .5rem; min-width: 0; }
.name { flex: 1 1 10rem; max-width: 18rem; }
.kind { display: grid; grid-template-columns: minmax(0, 1fr); flex: 1 1 10rem; max-width: 18rem; }
/* by the name's row — the first one when the type goes under it: as tall as the field, the buttons in its middle */
.acts { flex-shrink: 0; align-self: flex-start; min-height: calc(1.5em + .5rem + 2 * var(--bs-border-width)); font-size: .875rem; }
.err { padding: 0 .65rem .35rem; }
</style>
