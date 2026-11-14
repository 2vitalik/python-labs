<script setup>
import { onMounted, reactive, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import TagInput from '@core/components/TagInput.vue'
import Tip from '@core/components/Tip.vue'
import { postPart, putPart } from '../api.js'
import { roleOf } from '../catalog.js'
import { useEd } from '../ed.js'
import EmojiField from './EmojiField.vue'
import MoreFields from './MoreFields.vue'
import RoleField from './RoleField.vue'
import SaveCancel from './SaveCancel.vue'
import StatsEditor from './StatsEditor.vue'

// an entity's form, for a new one and in place of its card (T270 §7, T291 §4): own emoji, name and type in one row, as on
// the card, then a line about it; the full form adds stats and — by «＋ стани», or at once when there are some — states.
// `prefill` = { role?, title? } — a new one's start; emits done(saved part); `focus: 'description'` — opened by the card's
// «＋ опис», the cursor waits there
const props = defineProps({ part: Object, prefill: Object, focus: String })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const p = props.part
const start = p || props.prefill || {}
const form = reactive({
  icon: p?.icon || '', title: start.title || '', role: start.role || '', description: p?.description || '',
  stats: (p?.stats || []).map((s) => ({ ...s })), states: [...(p?.states || [])],
})
const shown = reactive({ states: form.states.length > 0 })
const error = ref('')
const title = ref()
const desc = ref()
const STATES = ['звичайний', 'посилений', 'переляканий', 'патрулює', 'переслідує', 'спить', 'відкрито', 'закрито']
onMounted(() => (props.focus === 'description' ? desc.value?.$el.focus() : !p && title.value?.focus()))

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
  <div class="vstack frm">
    <div class="top">
      <span class="d-flex gap-1 name">
        <EmojiField v-model="form.icon" :placeholder="roleOf(form.role).icon" />
        <input ref="title" v-model="form.title" class="form-control form-control-sm" placeholder="Назва: Танк гравця, Привид…">
      </span>
      <span class="kind">
        <span class="label">Тип</span>
        <RoleField v-model="form.role" class="flex-grow-1 min-w-0" />
      </span>
    </div>
    <!-- a description is one paragraph on the card: Enter makes no new line -->
    <GrowArea ref="desc" v-model="form.description" class="form-control form-control-sm" placeholder="Що це і як поводиться — коротко"
              @keydown.enter.prevent />
    <template v-if="!ed.simple">
      <div class="gutter" data-dock>
        <span class="label">Параметри</span>
        <StatsEditor v-model="form.stats" />
        <template v-if="shown.states">
          <span class="label">Стани<span class="tip-dock" /></span>
          <div class="vstack gap-1">
            <TagInput v-model="form.states" :hash="false" placeholder="стани через кому" :known="STATES" />
            <Tip id="entity-states">Переходи між станами — правилами з ефектом «стає…»</Tip>
          </div>
        </template>
      </div>
      <MoreFields :fields="{ states: 'стани' }" :shown @show="shown[$event] = true" />
    </template>
    <SaveCancel :disabled="!form.title.trim()" @save="save" @cancel="emit('cancel')" />
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.frm { gap: .35rem; }
.label { font-size: .7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
/* emoji · name · type in a row, as on the card; in a narrow card the type goes under the name */
.top { display: flex; flex-wrap: wrap; align-items: center; gap: .35rem .6rem; }
.name { flex: 1 1 10rem; max-width: 16rem; }
.kind { display: flex; flex: 1 1 11rem; align-items: center; gap: .4rem; min-width: 0; }
.min-w-0 { min-width: 0; }
/* the captions in a left gutter, the fields right of them: a block costs no row of its own */
.gutter { display: grid; grid-template-columns: auto minmax(0, 1fr); align-items: baseline; gap: .35rem .6rem; }
@media (max-width: 575.98px) {
  .gutter { grid-template-columns: minmax(0, 1fr); row-gap: .15rem; }
  .gutter > .label:not(:first-child) { margin-top: .35rem; }
}
</style>
