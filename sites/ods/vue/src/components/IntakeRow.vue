<script setup>
import { vHint } from '@core/hint.js'
import { fmtWhen } from '@core/labs.js'

import { putIntakeRow } from '../api.js'
import IntakeFile from './IntakeFile.vue'
import IntakeText from './IntakeText.vue'

// a line of the talk: when, the words (the teacher's own — «ти:» and quieter), the file; at the right, in places kept
// for them — 🙋 on a student's words (asks for more time) and «відкласти»: a row set aside goes grey
const props = defineProps({ r: Object, student: Boolean, busy: Boolean })
const emit = defineEmits(['act'])
const put = (data) => emit('act', () => putIntakeRow(props.r.id, data))
const ASK = { true: 'просить більше часу — клік знімає', false: 'клік — просить більше часу' }
</script>

<template>
  <li :id="`in-${r.id}`" class="msg" :class="{ mine: r.mine, skip: r.skip }">
    <time class="when" :datetime="r.sent_at">{{ fmtWhen(r.sent_at) }}</time>
    <div class="body">
      <IntakeText v-if="r.text" :text="r.text" :mine="r.mine" />
      <IntakeFile v-if="r.file" :id="r.id" :file="r.file" :student :mine="r.mine" :busy @act="emit('act', $event)" />
      <span v-if="!r.text && !r.file" class="quiet">без тексту</span>
    </div>
    <div class="tools">
      <button v-if="!r.mine && r.text" v-hint="ASK[!!r.asks]" type="button" class="ask" :class="{ on: r.asks }" aria-label="просить час" :aria-pressed="!!r.asks"
              :disabled="busy" @click="put({ asks: !r.asks })">🙋</button>
      <span v-else class="ask" />
      <button type="button" class="dot small" :disabled="busy" @click="put({ skip: !r.skip })">{{ r.skip ? 'повернути' : 'відкласти' }}</button>
    </div>
  </li>
</template>

<style scoped>
/* the side columns as wide as what they hold: the file's line in the middle needs every rem */
.msg { display: grid; grid-template-columns: 6rem minmax(0, 1fr) 6rem; grid-template-areas: 'when body tools'; column-gap: .6rem;
       padding: .35rem 0; border-top: 1px solid var(--bs-border-color-translucent); }
.when { grid-area: when; color: var(--bs-secondary-color); font-size: .78rem; line-height: 1.5rem; white-space: nowrap; }
.body { grid-area: body; min-width: 0; }
.tools { grid-area: tools; display: flex; justify-content: flex-end; align-items: center; gap: .4rem; height: 1.5rem; }
.mine .body { color: var(--bs-secondary-color); }
.skip .when, .skip .body { opacity: .45; }
.ask { width: 1.6rem; height: 1.4rem; padding: 0; border: 1px solid transparent; border-radius: .3rem; background: none; line-height: 1;
       filter: grayscale(1); opacity: .35; }
.ask:hover:not(:disabled) { opacity: .8; }
.ask.on { filter: none; opacity: 1; border-color: var(--bs-warning-border-subtle); background: var(--bs-warning-bg-subtle); }
span.ask { visibility: hidden; }
@media (max-width: 575px) {
  .msg { grid-template-columns: minmax(0, 1fr) auto; grid-template-areas: 'when tools' 'body body'; }
}
</style>
