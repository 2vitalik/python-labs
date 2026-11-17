<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { fmtWhen } from '@core/labs.js'
import { sendDefense } from '../api.js'
import { vocab } from '../defense.js'
import '../defense.css'

// the word that ends a defense (T329 §4) and the one button that opens it to the student: the result and every remark
// still a draft. Sent once, the button sends what was added since
const props = defineProps({ d: Object })
const emit = defineEmits(['set', 'sent'])
const busy = ref(false)
const error = ref('')
const drafts = computed(() => props.d.remarks.filter((r) => r.state === 'draft').length)
const debts = computed(() => props.d.remarks.filter((r) => r.kind === 'debt' && r.state !== 'accepted').length)
const idle = computed(() => !!props.d.sent_at && !drafts.value)
async function send() {
  busy.value = true
  try {
    await sendDefense(props.d.id)
    error.value = ''
    emit('sent')
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
</script>

<template>
  <div>
    <div class="drow">
      <span class="dlbl">Результат</span>
      <span class="d-flex flex-wrap align-items-center gap-1">
        <button v-for="r in vocab.results" :key="r.key" type="button" class="dchip" :class="{ on: d.result === r.key }"
                @click="emit('set', { result: d.result === r.key ? '' : r.key })">{{ r.icon }} {{ r.text }}</button>
        <span v-if="debts && d.result !== 'again'" class="dhint ms-1">незакритих боргів: {{ debts }} — «зараховано» вони блокують</span>
      </span>
    </div>
    <div class="d-flex flex-wrap align-items-center gap-2 mt-2">
      <button type="button" class="btn btn-success" :disabled="busy || idle" @click="send"><Icon name="send" /> {{ d.sent_at ? 'Надіслати нові' : 'Надіслати студентові' }}</button>
      <span class="dhint">
        <template v-if="idle">надіслано {{ fmtWhen(d.sent_at, true) }} — студент бачить результат і зауваження</template>
        <template v-else>студент побачить результат і нові зауваження ({{ drafts }}); враження й нотатка лишаються твоїми</template>
      </span>
    </div>
    <div v-if="error" class="text-danger small mt-1">{{ error }}</div>
  </div>
</template>
