<script setup>
import { onMounted, reactive, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { postPart, putPart } from '../api.js'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import FieldProps from './FieldProps.vue'
import OptionCards from './OptionCards.vue'
import StatsEditor from './StatsEditor.vue'

// a level's form (T270 §9): where it comes from, how many, its size and parameters; the field's properties it overrides
// sit in the same `props` and fold away; no `part` — a new level
const OWN = ['mode', 'count', 'size']
const OVERRIDES = ['topology', 'view', 'time', 'control', 'gravity', 'wrap']
const p = defineProps({ part: Object })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const spec = (key) => vocab.value.level.find((s) => s.key === key) || { key, label: key }
// the level's size has no hint of its own: the field's default size is the one to differ from
const hint = (s) => s.hint || (ed.field?.props?.size ? `як у поля: ${ed.field.props.size}` : 'напр. 20×15')
const form = reactive({ title: p.part?.title || '', props: { ...(p.part?.props || {}) }, description: p.part?.description || '',
                        stats: (p.part?.stats || []).map((s) => ({ ...s })) })
const differs = ref(Object.keys(form.props).some((k) => !OWN.includes(k)))
const title = ref()
const error = ref('')
const busy = ref(false)
onMounted(() => !p.part && title.value?.focus())

async function save() {
  error.value = ''
  busy.value = true
  try {
    const data = { title: form.title.trim(), props: form.props, stats: form.stats, description: form.description.trim() }
    if (p.part) await putPart(p.part.id, { ...data, order: p.part.order })
    else await postPart({ kind: 'level', ...data })
    await ed.changed()
    emit('done')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="vstack gap-2">
    <input ref="title" v-model="form.title" class="form-control form-control-sm fw-semibold" placeholder="Назва: Рівень 1, Печери 5–9, Генератор лабіринтів…">
    <div>
      <div class="small text-secondary mb-1">{{ spec('mode').label }}</div>
      <OptionCards v-model="form.props.mode" :options="spec('mode').options" />
    </div>
    <div class="row g-2">
      <div v-for="s in [spec('count'), spec('size')]" :key="s.key" class="col-6">
        <div class="small text-secondary mb-1">{{ s.label }}</div>
        <input v-model="form.props[s.key]" class="form-control form-control-sm" :placeholder="hint(s)">
      </div>
    </div>
    <div>
      <div class="small text-secondary mb-1">Параметри</div>
      <StatsEditor v-model="form.stats" free />
    </div>
    <input v-model="form.description" class="form-control form-control-sm" placeholder="Коротко: що тут відбувається, чим рівень особливий…">
    <div>
      <button type="button" class="fold" @click="differs = !differs"><Icon :name="differs ? 'down' : 'right'" /> Поле цього рівня відрізняється</button>
      <div v-if="differs" class="mt-2">
        <div class="form-text mt-0 mb-2">Лише те, що тут не так, як у поля загалом: гравітація лише на цьому рівні, гекси на бонусному…</div>
        <FieldProps v-model="form.props" :only="OVERRIDES" />
      </div>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" :disabled="busy || !form.title.trim()" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
    </div>
  </div>
</template>

<style scoped>
.fold { display: inline-flex; align-items: center; gap: .3rem; padding: 0; border: 0; background: none; color: inherit; font-size: .875rem; }
.fold:hover { color: var(--bs-emphasis-color); }
</style>
