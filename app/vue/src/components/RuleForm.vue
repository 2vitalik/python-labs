<script setup>
import { computed, nextTick, reactive, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { postClaim, postRule, putClaim, putRule } from '../api.js'
import { useEd } from '../ed.js'
import { sidesFor, specOf } from '../rules.js'
import CardPicker from './CardPicker.vue'
import RuleLine from './RuleLine.vue'
import SaveCancel from './SaveCancel.vue'

// the rule's editor (T270 §4.3): КОЛИ, every condition and every effect on a line of its own, the card it stands for; the note
// behind «＋ нотатка» until it has text (T291 §4). `rule` null — a new one, opened from `prefill` { when?, cond?, then?, card?,
// claim? }; its card — from the prefill, from a draft claim that waits for this rule, or picked here (T291 §8) — is claimed
// once the rule is saved
const props = defineProps({ rule: Object, prefill: Object })
const emit = defineEmits(['saved', 'cancel'])
const ed = useEd()
const copy = (list) => (list || []).map((it) => ({ ...it }))
const words = (src) => ({
  when: { ...src?.when, kind: src?.when?.kind || 'contact' },
  cond: copy(src?.cond),
  then: src?.then?.length ? copy(src.then) : [{ kind: '' }],
})
const form = reactive({ ...words(props.rule || props.prefill), note: props.rule?.note || '' })
const said = () => JSON.stringify([form.when, form.cond, form.then])
const opened = said()
const moved = computed(() => !props.rule && ed.claims.find((c) => c.id === props.prefill?.claim))  // a draft claim that waits for this rule
const chosen = ref(null)  // { slug, params } — the card picked in this form
const card = computed(() => !props.rule && (chosen.value?.slug || props.prefill?.card || moved.value?.task))
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
// a card picked before any word is written brings its blank — as a rule card picked from the catalog opens its rule
function choose(task, params) {
  chosen.value = { slug: task.slug, params }
  const blank = task.rule || {}
  if (said() !== opened || !(blank.when?.kind || blank.then?.length)) return
  Object.assign(form, words(blank), blank.when?.kind ? {} : { when: form.when })
}

const noting = ref(!!form.note)
const noteBox = ref()
async function addNote() {
  noting.value = true
  await nextTick()
  noteBox.value?.focus()
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
    const claim = c ? putClaim(c.id, { params: c.params, note: c.note, link: c.link, rule: saved.id })
      : card.value && postClaim({ task: card.value, rule: saved.id, params: chosen.value?.params || {} })
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
    <template v-if="noting">
      <span class="kw note">💬</span>
      <input ref="noteBox" v-model="form.note" class="form-control form-control-sm" placeholder="Нотатка: як саме це зроблено">
    </template>
    <template v-if="!rule">
      <span class="kw note">🪙</span>
      <div v-if="card" class="small d-flex align-items-center gap-1">
        <span>картка «{{ ed.info(card)?.title || card }}» додасться до правила після збереження</span>
        <button v-if="chosen" type="button" class="iact del" title="Не додавати цю картку" @click="chosen = null"><Icon name="minus" /></button>
      </div>
      <div v-else class="vstack gap-1 align-items-start" data-dock>
        <span class="d-flex align-items-center gap-1"><CardPicker :kinds="['rule']" hold label="картка, яку це правило реалізує" :suggest="fits" @choose="choose" /><span class="tip-dock" /></span>
        <Tip id="rule-form-card">Картка каталогу — монетка за це правило. Обрана до слів — заповнить правило своєю заготовкою;
          обрана після — ті, що підходять до написаного, стоять угорі списку</Tip>
      </div>
    </template>
    <template v-if="!noting">
      <span></span>
      <div><button type="button" class="more-field" @click="addNote">＋ нотатка</button></div>
    </template>
    <span></span>
    <SaveCancel :disabled="!ready || busy" @save="save" @cancel="emit('cancel')" />
    <div v-if="error" class="text-danger small">{{ error }}</div>
    <template v-if="rule">
      <span class="kw note">🪙</span><div><CardPicker :kinds="['rule']" :anchor="{ rule: rule.id }" label="картка, яку це правило реалізує" :suggest="fits" /></div>
    </template>
  </div>
</template>

<style scoped>
.rule-form { row-gap: .35rem; }
.more { --bs-btn-padding-y: .05rem; --bs-btn-font-size: .8rem; }
</style>
