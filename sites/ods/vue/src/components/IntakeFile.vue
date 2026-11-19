<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'

import { applyIntakeRow, intakeRawUrl } from '../api.js'
import { factsOf, stateOf } from '../intake.js'
import { fmtSize } from '../labText.js'
import IntakeLab from './IntakeLab.vue'
import LabClip from './LabClip.vue'

// a forwarded file in one line: its name (the file as sent), what the site read in it — the lab correctable till it is
// a version — and in a place at the end what it is to the site now: on the site · «перенести» · «ще раз» after a trouble ·
// the teacher's own file, brought over only by a click · not a notebook · «лаба?» · whose?; the trouble or why it is no
// notebook — under the line
const props = defineProps({ id: String, file: Object, student: Boolean, mine: Boolean, busy: Boolean })
const emit = defineEmits(['act'])
const state = computed(() => stateOf(props.file, props.student, props.mine))
const facts = computed(() => factsOf(props.file))
const reason = computed(() => ({ trouble: props.file.trouble, mine: props.file.trouble, none: props.file.why })[state.value] || '')
const size = computed(() => (props.file.size ? ` · ${fmtSize(props.file.size)}` : ''))
const apply = () => emit('act', () => applyIntakeRow(props.id))
</script>

<template>
  <div class="file">
    <div class="line">
      <div class="what"><div class="flow">
        <span class="piece first">
          <LabClip class="clip" />
          <a v-if="file.kind" v-hint="`${file.name}${size} — скачати, як надіслано`" :href="intakeRawUrl(id)" download class="name">{{ file.name || 'ноутбук' }}</a>
          <a v-else-if="file.link" v-hint="file.link" :href="file.link" target="_blank" rel="noopener" class="name">{{ file.name || 'посилання' }}</a>
          <span v-else v-hint="`${file.name}${size}`" class="name">{{ file.name }}</span>
        </span>
        <span v-for="x in facts" :key="x.text" class="piece" :class="x.cls">
          <IntakeLab v-if="x.lab" :id :lab="file.lab" :busy @act="emit('act', $event)" />
          <span v-else v-hint="x.hint">{{ x.text }}</span>
        </span>
      </div></div>
      <span class="state">
        <RouterLink v-if="state === 'site'" v-hint="'версія «Моєї лаби» — до перевірки'" :to="`/labs/${file.lab}/results/${file.vid}`"
                    class="site"><Icon name="done" /> на сайті</RouterLink>
        <button v-else-if="state === 'move' || state === 'trouble'" type="button" class="btn btn-sm btn-add go" :disabled="busy"
                @click="apply">{{ state === 'move' ? 'перенести' : 'ще раз' }}</button>
        <template v-else-if="state === 'mine'">
          <span v-hint="'ноутбук із твого повідомлення: сам сайт його не переносить'" class="quiet">твій файл</span>
          <button type="button" class="dot" :disabled="busy" @click="apply">{{ file.trouble ? 'ще раз' : 'перенести' }}</button>
        </template>
        <IntakeLab v-else-if="state === 'nolab'" :id :busy @act="emit('act', $event)" />
        <span v-else-if="state === 'nobody'" v-hint="'спершу скажи вгорі картки, чий це студент'" class="quiet">чий?</span>
        <span v-else class="quiet">не ноутбук</span>
      </span>
    </div>
    <div v-if="reason" class="reason" :class="state">{{ reason }}</div>
  </div>
</template>

<style scoped>
.file { font-size: .85rem; }
.line { display: flex; align-items: flex-start; gap: .5rem; line-height: 1.5rem; }
/* whole pieces in a row that wraps between them; each piece's «·» lies in a strip left of the box and is clipped there,
   so a piece that starts a line has none. The name keeps its width up to a cap and gives way only when alone on a line */
.what { flex: 1 1 auto; min-width: 0; overflow: hidden; }
.flow { display: flex; flex-wrap: wrap; margin-left: -1.1em; }
.piece { position: relative; padding-left: 1.1em; white-space: nowrap; }
.piece::before { content: '·'; position: absolute; left: 0; width: 1.1em; text-align: center; color: var(--bs-secondary-color); }
.first { display: inline-flex; align-items: center; min-width: 0; }
.clip { flex-shrink: 0; margin-right: .2rem; color: var(--bs-secondary-color); }
.name { min-width: 0; max-width: 16rem; overflow: hidden; text-overflow: ellipsis; }
.piece.ok { color: var(--bs-success-text-emphasis); }
.piece.late { color: var(--bs-warning-text-emphasis); }
.piece.quiet { color: var(--bs-secondary-color); font-size: inherit; }
.state { flex: 0 0 auto; min-width: 5rem; display: flex; justify-content: flex-end; align-items: center; gap: .4rem; height: 1.5rem; white-space: nowrap; }
/* a phone: the name beside the state, the facts under them across the whole width */
@media (max-width: 575px) {
  .file { overflow: hidden; }
  .line { flex-wrap: wrap; gap: 0; margin-left: -1.1em; }
  .what, .flow { display: contents; }
  .first { flex: 1 1 0; }
  .line::after { content: ''; order: 2; flex-basis: 100%; }
  .piece:not(.first) { order: 3; }
}
.site { text-decoration: none; color: var(--bs-success-text-emphasis); }
.site:hover { text-decoration: underline; }
.go { padding: 0 .5rem; font-size: .8rem; line-height: 1.35; }
.reason { font-size: .8rem; }
.reason.trouble, .reason.mine { color: var(--bs-danger-text-emphasis); }
.reason.none { color: var(--bs-secondary-color); }
</style>
