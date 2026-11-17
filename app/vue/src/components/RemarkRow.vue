<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import { deleteRemark, putRemark } from '../api.js'
import { STATES, mins } from '../defense.js'
import RemarkCheck from './RemarkCheck.vue'
import RemarkKind from './RemarkKind.vue'
import RemarkTags from './RemarkTags.vue'

// a remark as the teacher works with it (T328): the text is edited where it reads, a click changes the kind and the tags,
// a cleaner text proposed by a model or an agent waits under the line for one click; once it is sent — the student's
// answer and the word on it
const props = defineProps({ r: Object, n: Number, start: String, can: Boolean, like: Number })  // `like` — the number of a remark that says the same
const emit = defineEmits(['changed', 'removed'])
const error = ref('')
const minute = computed(() => (props.start && new Date(props.r.at) >= new Date(props.start) ? mins(props.start, props.r.at) : null))
function put(patch) {
  return putRemark(props.r.id, patch).then((r) => { error.value = ''; emit('changed', r) })
}
const click = (patch) => put(patch).catch((e) => (error.value = e.message))
const drop = () => deleteRemark(props.r.id).then(() => emit('removed', props.r.id), (e) => (error.value = e.message))
</script>

<template>
  <div class="remark" :class="r.state">
    <span class="n">{{ n }}</span>
    <div class="body">
      <InlineText v-if="can" :value="r.text" can multi block required :save="(text) => put({ text })" />
      <div v-else>{{ r.text }}</div>
      <div v-if="can && r.hint?.text" class="hint">
        <span title="Чистіший текст — пропозиція; твій рядок збережеться"><Icon name="spark" /> {{ r.hint.text }}</span>
        <button type="button" class="more-field" @click="click({ text: r.hint.text })">прийняти</button>
      </div>
      <div class="meta">
        <RemarkKind :r :can @set="click" />
        <RemarkTags :tags="r.tags" :can @set="(tags) => click({ tags })" />
        <span v-if="r.kind === 'tip' && r.state === 'open'" class="state">до відома</span>
        <span v-else-if="r.state !== 'draft'" class="state" :class="r.state">{{ STATES[r.state] }}</span>
        <span v-if="minute !== null" class="dim" title="Хвилина захисту — місце в записі розмови">{{ minute }}′</span>
        <span v-if="r.raw" class="dim" :title="`Як було надиктовано: ${r.raw}`">змінено</span>
        <span v-if="can && like" class="dim" title="Пропозиція: ці два зауваження кажуть те саме — одне можна видалити">схоже на №{{ like }}</span>
      </div>
      <RemarkCheck v-if="r.state !== 'draft'" :r :can @changed="emit('changed', $event)" />
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
    <DelButton v-if="can && !r.reply.state" what="зауваження" @yes="drop" />
  </div>
</template>

<style scoped>
.remark { display: grid; grid-template-columns: 1.4rem minmax(0, 1fr) auto; gap: .4rem; align-items: start; padding: .4rem .2rem;
          border-bottom: 1px solid var(--bs-border-color-translucent); }
.remark.accepted { background: color-mix(in srgb, var(--bs-success) 6%, transparent); }
.remark.returned { background: color-mix(in srgb, var(--bs-danger) 6%, transparent); }
.n { padding-top: .1rem; font-size: .76rem; text-align: right; color: var(--bs-secondary-color); font-variant-numeric: tabular-nums; }
.body { min-width: 0; overflow-wrap: anywhere; }
.meta { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem .6rem; margin-top: .2rem; }
.hint { display: flex; flex-wrap: wrap; align-items: baseline; gap: .1rem .5rem; margin-top: .15rem; font-size: .8rem; color: var(--act-add); }
.state { font-size: .72rem; color: var(--bs-secondary-color); }
.state.answered { color: var(--bs-warning-text-emphasis); font-weight: 600; }
.state.accepted { color: var(--bs-success-text-emphasis); }
.state.returned { color: var(--bs-danger-text-emphasis); }
.dim { font-size: .72rem; color: var(--bs-secondary-color); }
</style>
