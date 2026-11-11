<script setup>
import { onMounted, reactive, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import TagInput from '@core/components/TagInput.vue'
import { postPart, putPart } from '../api.js'
import { roleOf } from '../catalog.js'
import { useEd } from '../ed.js'
import EmojiField from './EmojiField.vue'
import RoleField from './RoleField.vue'
import StatsEditor from './StatsEditor.vue'

// an entity's form, for a new one and in place of its card (T270 §7): the name first (own emoji + title), then the type and
// a line about it; the full form adds stats and states. `prefill` = { role?, title? } — a new one's start; emits done(saved part);
// `focus: 'description'` — opened by the card's «＋ опис», the cursor waits there
const props = defineProps({ part: Object, prefill: Object, focus: String })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const p = props.part
const start = p || props.prefill || {}
const form = reactive({
  icon: p?.icon || '', title: start.title || '', role: start.role || '', description: p?.description || '',
  stats: (p?.stats || []).map((s) => ({ ...s })), states: [...(p?.states || [])],
})
const error = ref('')
const title = ref()
const desc = ref()
const STATES = ['звичайний', 'посилений', 'переляканий', 'патрулює', 'переслідує', 'спить', 'відкрито', 'закрито']
onMounted(() => (props.focus === 'description' ? desc.value?.focus() : !p && title.value?.focus()))

async function save() {
  error.value = form.role ? '' : 'Обери тип сутності'
  if (error.value) return
  try {
    const saved = p ? await putPart(p.id, { ...form, order: p.order }) : await postPart({ kind: 'entity', ...form })
    ed.changed()
    emit('done', saved)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="vstack gap-2">
    <div class="d-flex gap-2">
      <EmojiField v-model="form.icon" :placeholder="roleOf(form.role).icon" />
      <input ref="title" v-model="form.title" class="form-control form-control-sm" placeholder="Назва: Танк гравця, Привид, Стіна…">
    </div>
    <div class="d-flex align-items-center gap-2">
      <span class="label">Тип</span>
      <RoleField v-model="form.role" class="flex-grow-1" />
    </div>
    <input ref="desc" v-model="form.description" class="form-control form-control-sm" placeholder="Що це і як поводиться — коротко">
    <template v-if="!ed.simple">
      <div class="label">Параметри</div>
      <StatsEditor v-model="form.stats" />
      <div class="label">Стани</div>
      <TagInput v-model="form.states" :hash="false" placeholder="стани через кому" :known="STATES" />
      <div class="hint">переходи між станами — правилами з ефектом «стає…»</div>
    </template>
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" :disabled="!form.title.trim()" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.label { font-size: .7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
.hint { margin-top: -.3rem; font-size: .75rem; color: var(--bs-secondary-color); }
</style>
