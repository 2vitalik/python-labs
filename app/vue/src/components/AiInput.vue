<script setup>
import { computed, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { ai, ask, text } from '../ai.js'

// the student's words (T289 §1, contract §8): a field that grows, how to write, how many asks are left and where the text
// goes, «Розібрати». While the server reads, the button waits with a spinner; an error stays under the field, and so does
// the text — it is cleared only once its proposals are here
const busy = ref(false)
const error = ref('')
const len = computed(() => text.value.length)
const over = computed(() => len.value > ai.max_chars)
const ready = computed(() => !!text.value.trim() && !over.value && !busy.value)
// «з 10» — when the server tells the day's limit (`per_day`); an admin has no limit and no line
const left = computed(() => (ai.left_today == null ? '' : `лишилось ${ai.left_today}${ai.per_day ? ` з ${ai.per_day}` : ''} на сьогодні`
  + (ai.left_total == null ? '' : ` · ${ai.left_total} на семестр`)))

async function send() {
  if (!ready.value) return
  busy.value = true
  error.value = ''
  try {
    await ask(text.value.trim())
    text.value = ''
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="vstack gap-2">
    <Tip id="ai-how">Пиши, як розповів би другові: хто є на полі, що відбувається, які вікна, що вже зроблено. Можна шматками — потім
      допишеш ще. На телефоні зручно диктувати: мікрофон на клавіатурі. Нічого не додається само: ШІ лише пропонує, додаєш ти.</Tip>
    <GrowArea v-model="text" class="form-control words" placeholder="У мене танчики. Є танк гравця, він їздить у 4 боки і стріляє…"
              @keydown.enter="(e) => (e.metaKey || e.ctrlKey) && send()" />
    <div class="d-flex flex-wrap align-items-center gap-1 column-gap-3 small text-secondary">
      <span :class="{ 'text-danger': over }">{{ len }} / {{ ai.max_chars }} знаків</span>
      <span v-if="left">{{ left }}</span>
      <span>текст піде на розбір в API Anthropic</span>
      <button type="button" class="btn btn-sm btn-add ms-auto" :disabled="!ready" title="⌘/Ctrl+Enter" @click="send">
        <span v-if="busy" class="spinner-border spinner-border-sm" aria-hidden="true"></span><Icon v-else name="spark" />
        {{ busy ? 'Розбираю…' : 'Розібрати' }}
      </button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
/* four lines to start with, then it grows with the text */
.words { min-height: 6.6rem; }
</style>
