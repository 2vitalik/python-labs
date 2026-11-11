<script setup>
import { computed, reactive, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { postClaim, postRule, putClaim, putRule } from '../api.js'
import { useEd } from '../ed.js'
import { sidesFor, specOf } from '../rules.js'
import CardPicker from './CardPicker.vue'
import RuleLine from './RuleLine.vue'

// the rule's editor (T270 §4.3): КОЛИ, every condition and every effect on a line of its own, a note. `rule` null — a new one,
// opened from `prefill` { when?, cond?, then?, card? }; the card is claimed on the new rule once it is saved
const props = defineProps({ rule: Object, prefill: Object })
const emit = defineEmits(['saved', 'cancel'])
const ed = useEd()
const src = props.rule || props.prefill || {}
const copy = (list) => (list || []).map((it) => ({ ...it }))
const form = reactive({
  when: { ...src.when, kind: src.when?.kind || 'contact' },
  cond: copy(src.cond),
  then: src.then?.length ? copy(src.then) : [{ kind: '' }],
  note: props.rule?.note || '',
})
const moved = computed(() => !props.rule && ed.claims.find((c) => c.id === props.prefill?.claim))  // a draft claim that waits for this rule
const card = computed(() => !props.rule && (props.prefill?.card || moved.value?.task))
const sides = computed(() => sidesFor(form.when))
const complete = (dic, it) => specOf(dic, it.kind)?.args.every((a) => !a.required || it[a.name] || it[a.name] === 0)
const ready = computed(() => complete('triggers', form.when) && form.then.length > 0 &&
  form.then.every((e) => complete('effects', e)) && form.cond.every((c) => complete('conditions', c)))
// a card fits when its blank uses only this rule's words: the same trigger (if it names one), its effects among ours
function fits(task) {
  const when = task.rule?.when?.kind
  const then = (task.rule?.then || []).map((e) => e.kind)
  if (!when && !then.length) return false
  return (!when || when === form.when.kind) && then.every((k) => form.then.some((e) => e.kind === k))
}
const error = ref('')
const busy = ref(false)
async function save() {
  error.value = ''
  busy.value = true
  try {
    const saved = await (props.rule ? putRule(props.rule.id, form) : postRule(form))
    let lost = ''  // the rule is in; a card that failed must not make a retry post the rule twice
    const c = moved.value
    const claim = c ? putClaim(c.id, { params: c.params, note: c.note, link: c.link, rule: saved.id }) : card.value && postClaim({ task: card.value, rule: saved.id, params: {} })
    await Promise.resolve(claim).catch((e) => (lost = e.message))
    ed.changed()
    if (lost) ed.fail(`Правило збережено, а картку не додано: ${lost}`)
    emit('saved')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="rule-text rule-form">
    <span class="kw when">КОЛИ</span>
    <RuleLine :item="form.when" dic="triggers" :sides="['*']" placeholder="подія…" />
    <template v-for="(c, i) in form.cond" :key="`c${i}`">
      <span class="kw if">{{ i ? 'ТА' : 'ЯКЩО' }}</span>
      <RuleLine :item="c" dic="conditions" :sides :when="form.when" placeholder="умова…" negatable removable @remove="form.cond.splice(i, 1)" />
    </template>
    <span class="kw if">{{ form.cond.length ? '' : 'ЯКЩО' }}</span>
    <div>
      <button type="button" class="btn btn-sm btn-add more" @click="form.cond.push({ kind: '' })"><Icon name="plus" /> умова</button>
      <span v-if="!form.cond.length" class="text-secondary small ms-2">необовʼязково</span>
    </div>
    <template v-for="(e, i) in form.then" :key="`t${i}`">
      <span class="kw then">{{ i ? '' : 'ТО' }}</span>
      <RuleLine :item="e" dic="effects" :sides :when="form.when" placeholder="ефект…" :removable="form.then.length > 1" @remove="form.then.splice(i, 1)" />
    </template>
    <span></span>
    <div><button type="button" class="btn btn-sm btn-add more" @click="form.then.push({ kind: '' })"><Icon name="plus" /> ефект</button></div>
    <span class="kw note">💬</span>
    <input v-model="form.note" class="form-control form-control-sm" placeholder="Нотатка: як саме це зроблено — за бажанням">
    <template v-if="card">
      <span class="kw note">🪙</span><span class="small">картка «{{ ed.info(card)?.title || card }}» додасться до правила після збереження</span>
    </template>
    <span></span>
    <div class="d-flex flex-wrap gap-2">
      <button type="button" class="btn btn-sm btn-success" :disabled="!ready || busy" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
      <div v-if="error" class="w-100 text-danger small">{{ error }}</div>
    </div>
    <template v-if="rule">
      <span class="kw note">🪙</span><div><CardPicker :kinds="['rule']" :anchor="{ rule: rule.id }" label="картка, яку це правило реалізує" :suggest="fits" /></div>
    </template>
  </div>
</template>

<style scoped>
.rule-form { row-gap: .35rem; }
.more { --bs-btn-padding-y: .05rem; --bs-btn-font-size: .8rem; }
</style>
