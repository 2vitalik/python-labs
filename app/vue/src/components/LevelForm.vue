<script setup>
import { computed, onMounted, reactive, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { postPart, putPart } from '../api.js'
import { vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { gameBrushes } from '../momentMap.js'
import FieldProps from './FieldProps.vue'
import MomentMap from './MomentMap.vue'
import OptionCards from './OptionCards.vue'
import StatsEditor from './StatsEditor.vue'

// a level's form (T270 §9, T291 §4): the name, how many and the size in one row, as the card's head; where it comes from and
// its parameters with their captions in the left gutter; the field's properties it overrides sit in the same `props` and
// fold away; the map drawn in cells (T276) — behind the quiet «＋ намалювати рівень», open when there is one; no `part` — a new level
const OWN = ['mode', 'count', 'size', 'map']
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
const drawing = ref(!!form.props.map)
const brushes = computed(() => gameBrushes(ed.entities))
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
  <div class="vstack frm">
    <div class="top">
      <input ref="title" v-model="form.title" class="form-control form-control-sm fw-semibold name" placeholder="Назва: Рівень 1, Печери 5–9…">
      <label v-for="s in [spec('count'), spec('size')]" :key="s.key" class="f">{{ s.label }}
        <input v-model="form.props[s.key]" class="form-control form-control-sm" :class="s.key" :placeholder="hint(s)">
      </label>
    </div>
    <div class="gutter">
      <span class="cap">{{ spec('mode').label }}</span>
      <OptionCards v-model="form.props.mode" :options="spec('mode').options" />
      <span class="cap">Параметри</span>
      <StatsEditor v-model="form.stats" free />
    </div>
    <!-- a description is one paragraph on the card: Enter makes no new line -->
    <GrowArea v-model="form.description" class="form-control form-control-sm" placeholder="Коротко: що тут відбувається, чим рівень особливий…"
              @keydown.enter.prevent />
    <div v-if="drawing">
      <div class="cap mb-1">Мапа рівня — що де стоїть на старті</div>
      <MomentMap v-model="form.props.map" :palette="brushes" />
    </div>
    <button v-else type="button" class="more-field align-self-start" title="рівень клітинками зі значків сутностей — заявляє картку «Мапа рівня на сайті»"
            @click="drawing = true">＋ намалювати рівень</button>
    <div>
      <button type="button" class="fold" @click="differs = !differs"><Icon :name="differs ? 'down' : 'right'" /> Поле цього рівня відрізняється</button>
      <div v-if="differs" class="vstack gap-2 mt-1">
        <Tip id="level-field-differs">Лише те, що тут не так, як у поля загалом: гравітація лише на цьому рівні, гекси на бонусному…</Tip>
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
.frm { gap: .35rem; }
/* name · how many · size in a row, as the card's head; in a narrow card the short two go under the name */
.top { display: flex; flex-wrap: wrap; align-items: flex-end; gap: .35rem; }
.name { flex: 1 1 10rem; max-width: 16rem; }
.f { display: flex; flex-direction: column; gap: .1rem; margin: 0; font-size: .7rem; color: var(--bs-secondary-color); }
.count { width: 8.5rem; }
.size { width: 6.5rem; }
/* the captions in a left gutter, the fields right of them; on a phone — over them */
.gutter { display: grid; grid-template-columns: fit-content(7rem) minmax(0, 1fr); align-items: baseline; gap: .35rem .6rem; }
.cap { font-size: .8rem; color: var(--bs-secondary-color); }
@media (max-width: 575.98px) {
  .gutter { grid-template-columns: minmax(0, 1fr); row-gap: .15rem; }
  .cap:not(:first-child) { margin-top: .35rem; }
}
.fold { display: inline-flex; align-items: center; gap: .3rem; padding: 0; border: 0; background: none; color: inherit; font-size: .875rem; }
.fold:hover { color: var(--bs-emphasis-color); }
</style>
