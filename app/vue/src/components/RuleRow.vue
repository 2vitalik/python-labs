<script setup>
import { computed, reactive, ref, watch } from 'vue'

import { deleteRule, postRule, putRule } from '../api.js'
import { sentence, sidesFor, specOf } from '../rules.js'
import ArgFields from './ArgFields.vue'
import WordPick from './WordPick.vue'

// a rule as a sentence «КОЛИ … → ЯКЩО … → ТО …»; in edit mode each word is a pick from the vocab with its arguments
const props = defineProps({ rule: Object, parts: Array, game: Object, editable: Boolean })
const emit = defineEmits(['changed', 'cancel'])
const edit = ref(!props.rule)
const arm = ref(false)
const error = ref('')
const form = reactive({
  when: { kind: 'contact', ...(props.rule?.when || {}) },
  cond: (props.rule?.cond || []).map((c) => ({ ...c })),
  then: props.rule ? props.rule.then.map((e) => ({ ...e })) : [{ kind: '' }],
  note: props.rule?.note || '',
})
const text = computed(() => props.rule && sentence(props.rule, props.parts))
const sides = computed(() => sidesFor(form.when))
const whenSpec = computed(() => specOf('triggers', form.when.kind))
const complete = (dic, it) => {
  const spec = specOf(dic, it.kind)
  return spec && spec.args.every((a) => !a.required || it[a.name] || it[a.name] === 0)
}
const ready = computed(() => complete('triggers', form.when) && form.then.length &&
  form.then.every((e) => complete('effects', e)) && form.cond.every((c) => complete('conditions', c)))

// a new word keeps only its own args
const reset = (it) => { for (const k of Object.keys(it)) if (k !== 'kind' && k !== 'not') delete it[k] }
watch(() => form.when.kind, () => reset(form.when))

async function save() {
  error.value = ''
  try {
    await (props.rule ? putRule(props.rule.id, form) : postRule(form))
    edit.value = false
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
const cancel = () => (props.rule ? (edit.value = false) : emit('cancel'))
const remove = async () => { await deleteRule(props.rule.id); emit('changed') }
</script>

<template>
  <div v-if="!edit" class="rule d-flex flex-wrap align-items-baseline gap-1 px-2 py-1 border rounded">
    <span class="kw">КОЛИ</span><span>{{ text.when }}</span>
    <template v-if="text.cond"><span class="kw">→ ЯКЩО</span><span>{{ text.cond }}</span></template>
    <span class="kw">→ ТО</span><span>{{ text.then }}</span>
    <span v-if="rule.note" class="text-secondary small" :title="rule.note">💬</span>
    <template v-if="editable">
      <span class="ms-auto act" role="button" title="Редагувати" @click="edit = true">✏️</span>
      <span v-if="!arm" class="act text-secondary" role="button" title="Видалити правило" @click="arm = true">✕</span>
      <button v-else class="btn btn-danger btn-sm py-0" @mouseleave="arm = false" @click="remove">Точно?</button>
    </template>
  </div>

  <div v-else class="border rounded p-2 vstack gap-2 editing">
    <div class="d-flex flex-wrap align-items-center gap-1">
      <span class="kw">КОЛИ</span>
      <WordPick v-model="form.when.kind" dic="triggers" placeholder="подія…" />
      <ArgFields v-if="whenSpec" :spec="whenSpec" :item="form.when" :parts :sides="['*']" :game />
    </div>
    <div class="d-flex flex-wrap align-items-center gap-1">
      <span class="kw">ЯКЩО</span>
      <template v-for="(c, i) in form.cond" :key="i">
        <span v-if="i" class="text-secondary small">і</span>
        <button type="button" class="btn btn-sm py-0 px-1" :class="c.not ? 'btn-dark' : 'btn-outline-secondary'" title="заперечення" @click="c.not = !c.not">не</button>
        <WordPick v-model="c.kind" dic="conditions" placeholder="умова…" @update:model-value="reset(c)" />
        <ArgFields v-if="specOf('conditions', c.kind)" :spec="specOf('conditions', c.kind)" :item="c" :parts :sides :game />
        <span class="act text-secondary" role="button" title="Прибрати умову" @click="form.cond.splice(i, 1)">✕</span>
      </template>
      <button type="button" class="btn btn-link btn-sm p-0 text-decoration-none" @click="form.cond.push({ kind: '' })">＋ умова</button>
      <span v-if="!form.cond.length" class="text-secondary small">(необовʼязково)</span>
    </div>
    <div class="d-flex flex-wrap align-items-center gap-1">
      <span class="kw">ТО</span>
      <template v-for="(e, i) in form.then" :key="i">
        <span v-if="i" class="text-secondary small">·</span>
        <WordPick v-model="e.kind" dic="effects" placeholder="ефект…" @update:model-value="reset(e)" />
        <ArgFields v-if="specOf('effects', e.kind)" :spec="specOf('effects', e.kind)" :item="e" :parts :sides :game />
        <span v-if="form.then.length > 1" class="act text-secondary" role="button" title="Прибрати ефект" @click="form.then.splice(i, 1)">✕</span>
      </template>
      <button type="button" class="btn btn-link btn-sm p-0 text-decoration-none" @click="form.then.push({ kind: '' })">＋ ефект</button>
    </div>
    <div class="d-flex gap-2">
      <input v-model="form.note" class="form-control form-control-sm" placeholder="Нотатка (за бажанням)">
      <button class="btn btn-primary btn-sm text-nowrap" :disabled="!ready" @click="save">💾 Зберегти</button>
      <button class="btn btn-outline-secondary btn-sm" @click="cancel">✕</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.kw { font-size: .72rem; font-weight: 700; color: var(--bs-secondary-color); letter-spacing: .04em; }
.rule { font-size: .9rem; background: var(--bs-body-bg); }
.act { opacity: .6; }
.act:hover { opacity: 1; }
.editing { background: var(--bs-tertiary-bg); }
</style>
