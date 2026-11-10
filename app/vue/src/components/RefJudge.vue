<script setup>
import { ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { judgeRef } from '../api.js'

// the teacher on a record of /ideas: a line to its author, then its state — taken, dropped, or back to the new ones
const props = defineProps({ r: Object })
const emit = defineEmits(['changed'])
const BUTTONS = { linked: ['взято', 'btn-success'], dropped: ['відхилено', 'btn-secondary'], inbox: ['у нові', 'btn-outline-secondary'] }
const open = ref(false)
const reply = ref('')
const error = ref('')
watch(open, (on) => {
  if (!on) return
  reply.value = props.r.reply || ''
  error.value = ''
})

async function judge(status) {
  error.value = ''
  try {
    await judgeRef(props.r.id, { status, reply: reply.value.trim() })
    open.value = false
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <Pop v-model="open" width="20rem">
    <template #trigger="{ toggle }">
      <button type="button" class="iact wide" title="Відповісти автору й позначити стан" @click="toggle"><Icon name="note" /> відповісти</button>
    </template>
    <div class="vstack gap-2">
      <input v-model="reply" class="form-control form-control-sm" placeholder="Відповідь автору — за бажанням"
             @keydown.enter="judge(r.status || 'inbox')">
      <div class="d-flex flex-wrap gap-2">
        <button v-for="([label, tone], s) in BUTTONS" :key="s" type="button" class="btn btn-sm" :class="tone" @click="judge(s)">
          <Icon v-if="(r.status || 'inbox') === s" name="check" /> {{ label }}</button>
      </div>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </Pop>
</template>

<style scoped>
.iact.wide { width: auto; gap: .3rem; padding: 0 .45rem; font-size: .8rem; }
</style>
