<script setup>
import { computed, reactive, ref } from 'vue'

import TagInput from '@core/components/TagInput.vue'
import { deletePart, postClaim, putPart } from '../api.js'
import { roleGroups, roleOf, vocab } from '../catalog.js'
import { mentions, sentence } from '../rules.js'
import CardPicker from './CardPicker.vue'
import ClaimChip from './ClaimChip.vue'
import ShotStrip from './ShotStrip.vue'
import StatsEditor from './StatsEditor.vue'

// an inhabitant of the field: role, stats (HP, швидкість…), states, mechanics claimed on it, the rules that name it
const props = defineProps({ part: Object, claims: Array, rules: Array, parts: Array, info: Function, editable: Boolean, judge: Boolean, nick: String })
const emit = defineEmits(['changed', 'go'])
const edit = ref(false)
const arm = ref(false)
const error = ref('')
const form = reactive({ title: '', role: '', description: '', stats: [], states: [] })
const role = computed(() => roleOf(props.part.role))
const statIcon = (s) => vocab.value.stats.find((x) => x.key === s.key)?.icon || '•'
const mine = computed(() => props.rules.filter((r) => mentions(r, props.part.id)))
const line = (r) => { const t = sentence(r, props.parts); return `${t.when}${t.cond ? ` → якщо ${t.cond}` : ''} → ${t.then}` }

async function run(fn) {
  error.value = ''
  try {
    await fn()
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
function start() {
  Object.assign(form, { title: props.part.title, role: props.part.role, description: props.part.description,
                        stats: props.part.stats.map((s) => ({ ...s })), states: [...props.part.states] })
  edit.value = true
}
const save = () => run(async () => { await putPart(props.part.id, form); edit.value = false })
const remove = () => run(() => deletePart(props.part.id))
const addClaim = (task, params) => run(() => postClaim({ task, part: props.part.id, params }))
</script>

<template>
  <div class="card h-100">
    <div class="card-body p-2 vstack gap-2">
      <div v-if="!edit" class="d-flex align-items-center gap-2">
        <span class="fs-5 lh-1">{{ role.icon }}</span>
        <span class="fw-semibold">{{ part.title }}</span>
        <span class="text-secondary small">{{ role.label }}</span>
        <template v-if="editable">
          <span class="ms-auto act" role="button" title="Редагувати" @click="start">✏️</span>
          <span v-if="!arm" class="act" role="button" title="Видалити сутність (разом з її правилами й заявками)" @click="arm = true">🗑️</span>
          <button v-else class="btn btn-danger btn-sm py-0" @mouseleave="arm = false" @click="remove">Точно видалити?</button>
        </template>
      </div>
      <template v-else>
        <div class="d-flex gap-1">
          <select v-model="form.role" class="form-select form-select-sm w-auto">
            <optgroup v-for="(list, g) in roleGroups" :key="g" :label="g">
              <option v-for="r in list" :key="r.key" :value="r.key">{{ r.icon }} {{ r.label }}</option>
            </optgroup>
          </select>
          <input v-model="form.title" class="form-control form-control-sm" placeholder="Назва">
        </div>
        <input v-model="form.description" class="form-control form-control-sm" placeholder="Що це і як поводиться — коротко">
        <div class="small text-secondary">Параметри</div>
        <StatsEditor v-model="form.stats" />
        <div class="small text-secondary">Стани <span class="opacity-75">(переходи між ними — правилами «увімкнути стан»)</span></div>
        <TagInput v-model="form.states" :hash="false" :known="['звичайний', 'посилений', 'переляк', 'патрулює', 'переслідує', 'спить', 'відкрито', 'закрито']" />
        <div class="d-flex gap-2">
          <button class="btn btn-primary btn-sm" @click="save">💾 Зберегти</button>
          <button class="btn btn-outline-secondary btn-sm" @click="edit = false">✕</button>
        </div>
      </template>

      <template v-if="!edit">
        <div v-if="part.description" class="text-secondary small">{{ part.description }}</div>
        <div v-if="part.stats.length || part.states.length" class="d-flex flex-wrap gap-1 small">
          <span v-for="s in part.stats" :key="s.key" class="badge rounded-pill fw-normal stat" :title="s.key">{{ statIcon(s) }} {{ s.label || s.key }} {{ s.value }}<span v-if="s.unit" class="opacity-75"> {{ s.unit }}</span></span>
          <span v-if="part.states.length" class="badge rounded-pill fw-normal state" title="стани">🔁 {{ part.states.join(' · ') }}</span>
        </div>
        <ShotStrip v-if="editable || part.screenshots.length" :part :editable @changed="emit('changed')" />
        <div v-if="claims.length" class="d-flex flex-wrap gap-1 align-items-start">
          <ClaimChip v-for="c in claims" :key="c.id" :claim="c" :info="info(c.task)" :parts :editable :judge :nick @changed="emit('changed')" />
        </div>
        <CardPicker v-if="editable" placeholder="＋ механіка: рух, поява, бій, інвентар, стан…" :claimed="new Set(claims.map((c) => c.task))" @pick="addClaim" />
        <ul v-if="mine.length" class="rules list-unstyled mb-0 small">
          <li v-for="r in mine.slice(0, 4)" :key="r.id" role="button" class="text-secondary" title="до правила" @click="emit('go', `r-${r.id}`)">📜 {{ line(r) }}</li>
          <li v-if="mine.length > 4" role="button" class="text-secondary" @click="emit('go', 'rules')">… ще {{ mine.length - 4 }} у «Правилах»</li>
        </ul>
      </template>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.act { opacity: .6; }
.act:hover { opacity: 1; }
.stat { background: var(--bs-tertiary-bg); color: var(--bs-body-color); border: 1px solid var(--bs-border-color); }
.state { background: color-mix(in srgb, var(--bs-info) 14%, var(--bs-body-bg)); color: var(--bs-body-color); border: 1px solid var(--bs-info-border-subtle); }
.rules li { padding: .1rem 0; }
.rules li:hover { color: var(--bs-body-color) !important; }
</style>
