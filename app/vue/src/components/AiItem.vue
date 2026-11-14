<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { itemName, needsOf } from '../ai.js'
import { jump } from '../jump.js'
import AiClaim from './AiClaim.vue'
import AiEntity from './AiEntity.vue'
import AiField from './AiField.vue'
import AiLevel from './AiLevel.vue'
import AiRule from './AiRule.vue'
import AiUnknown from './AiUnknown.vue'
import AiWindow from './AiWindow.vue'

// one proposal (T289 §1, contract §8): the thing as it would look in the description, dashed and paler while it is not in
// the game; the student's words under it. Its state changes in place — the row neither goes nor moves: added — a solid
// frame, the tick and «показати →»; rejected — struck through, «повернути»; already in the game — grey «уже є».
// A proposal that needs one rejected (T289 §4) greys and says which. Emits add(keys) · mark(keys, state)
const props = defineProps({ item: Object, draft: Object, busy: Boolean })
const emit = defineEmits(['add', 'mark'])
const BODY = { field: AiField, entity: AiEntity, rule: AiRule, window: AiWindow, level: AiLevel, claim: AiClaim, unknown: AiUnknown }
const needs = computed(() => needsOf(props.draft, props.item))
const waiting = computed(() => needs.value.filter((x) => x.state === 'open'))
const stopped = computed(() => needs.value.filter((x) => x.state === 'rejected'))
const open = computed(() => props.item.state === 'open')
const look = computed(() => ({ open: open.value && props.item.group === 'unknown' ? 'ask' : 'new', added: 'added', rejected: 'no', exists: 'has' }[props.item.state]))
const names = (list) => list.map(itemName).join(', ')
// a rule looks up the titles proposed beside it, an unknown shows the words it came from
const body = computed(() => ({ data: props.item.data, ...(props.item.group === 'rule' && { draft: props.draft }), ...(props.item.group === 'unknown' && { item: props.item }) }))
</script>

<template>
  <div class="ai-item" :class="[look, { dim: open && stopped.length }]">
    <div class="body">
      <component :is="BODY[item.group]" v-bind="body" />
      <div v-if="item.hint" class="ai-sub">{{ item.hint }}</div>
      <div v-if="open && stopped.length" class="ai-sub need">потрібне відхилене: {{ names(stopped) }} — поверни, щоб додати</div>
      <div v-else-if="open && waiting.length" class="ai-sub need">разом додасться: {{ names(waiting) }}</div>
      <div v-else-if="item.state === 'added' && needs.length" class="ai-sub">разом з нею: {{ names(needs) }}</div>
      <div v-if="item.quote && item.group !== 'unknown'" class="ai-q small">«{{ item.quote }}»</div>
    </div>
    <div class="acts">
      <template v-if="open">
        <button v-if="item.group !== 'unknown'" type="button" class="iact add" :disabled="busy || stopped.length > 0" @click="emit('add', [item.key])">
          <Icon name="plus" /> Додати</button>
        <button type="button" class="iact" :disabled="busy" title="Відхилити: у гру не піде, рядок лишиться" @click="emit('mark', [item.key], 'rejected')">
          <Icon name="x" /> відхилити</button>
      </template>
      <span v-else-if="item.state === 'added'" class="state text-success"><Icon name="done" /> додано
        <button v-if="item.made" type="button" class="link" @click="jump(item.made)">показати <Icon name="arrow" /></button></span>
      <span v-else-if="item.state === 'rejected'" class="state">відхилено ·
        <button type="button" class="link" :disabled="busy" @click="emit('mark', [item.key], 'open')">повернути</button></span>
      <span v-else class="state">уже є в грі<button v-if="item.made" type="button" class="link ms-1" @click="jump(item.made)">показати <Icon name="arrow" /></button></span>
    </div>
  </div>
</template>

<style>
/* the look shared by the proposals' bodies (Ai*.vue): a line of icon · title · type, the description, a quiet sub-line */
.ai-item .ai-line { display: flex; flex-wrap: wrap; align-items: baseline; gap: .1rem .4rem; min-width: 0; overflow-wrap: anywhere; }
.ai-item .ai-ico { font-size: 1.1rem; line-height: 1; }
.ai-item .ai-t { font-weight: 600; }
.ai-item .ai-ty { font-size: .78rem; color: var(--bs-secondary-color); }
.ai-item .ai-d { font-size: .84rem; }
.ai-item .ai-sub { font-size: .78rem; color: var(--bs-secondary-color); }
.ai-item .ai-q { font-style: italic; color: var(--bs-secondary-color); }
.ai-item .ai-sub.need { color: var(--bs-warning-text-emphasis); }
</style>

<style scoped>
.ai-item { display: flex; align-items: flex-start; gap: .6rem; padding: .4rem .55rem; border: 1.5px solid var(--bs-border-color); border-radius: .4rem; }
.body { flex: 1; min-width: 0; display: flex; flex-direction: column; gap: .2rem; }
.new { border-style: dashed; border-color: color-mix(in srgb, var(--act-add) 55%, transparent); background: color-mix(in srgb, var(--act-add) 3%, transparent); }
.new > .body, .dim > .body { opacity: .78; }
.dim { border-color: var(--bs-border-color); background: none; }
.added { border-color: color-mix(in srgb, var(--bs-success) 50%, transparent); background: color-mix(in srgb, var(--bs-success) 7%, transparent); }
.has, .no { color: var(--bs-secondary-color); }
.no :deep(.ai-t), .no :deep(.pieces) { text-decoration: line-through; }
.ask { border-style: dashed; border-color: color-mix(in srgb, var(--bs-warning) 80%, transparent); background: color-mix(in srgb, var(--bs-warning) 8%, transparent); }
.acts { display: flex; align-items: center; gap: .15rem; flex-shrink: 0; }
/* an action with its word: the quiet icon button, as wide as the word needs */
.acts .iact { width: auto; gap: .2rem; padding: 0 .4rem; font-size: .78rem; }
.state { font-size: .78rem; white-space: nowrap; }
.link { padding: 0; border: 0; background: none; color: var(--bs-link-color); font-size: inherit; }
.link:hover { text-decoration: underline; }
/* a phone: the actions go under the text, to the right — they never sit on it */
@media (max-width: 575px) {
  .ai-item { flex-wrap: wrap; }
  .acts { width: 100%; justify-content: flex-end; }
}
</style>
