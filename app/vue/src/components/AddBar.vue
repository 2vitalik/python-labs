<script setup>
import { computed, ref } from 'vue'

import { postClaim } from '../api.js'
import { kindOf, vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { cardItems, roleItems, statItems, windowTypeItems } from '../items.js'
import { jump } from '../jump.js'
import AddStep from './AddStep.vue'
import Picker from './Picker.vue'

// one «＋ Додати» over the whole description (T270 §11): type what the game has — a type of entity, a type of window,
// a parameter, a card — and it lands where its kind says. The «＋» of each section does the same within the section.
const emit = defineEmits(['open'])  // open(block, prefill): the form of a new entity | window | level | rule
const ed = useEd()
const step = ref(null)
const error = ref('')

const FORMS = [
  { key: 'form:rule', title: 'Правило', icon: '📜', desc: 'КОЛИ подія — ЯКЩО умова — ТО ефект', words: ['коли', 'якщо', 'взаємодія', 'подія', 'rule'], open: 'rule' },
  { key: 'form:level', title: 'Рівень', icon: '🪜', desc: 'звідки береться, розмір, параметри, скриншот', words: ['мапа', 'карта', 'level'], open: 'level' },
  { key: 'form:field', title: 'Поле', icon: '🗺️', desc: 'сітка, вид, час, керування', words: ['сітка', 'grid', 'field'], go: 'field' },
]
const tag = (list, group, more = () => ({})) => list.map((it) => ({ ...it, key: `${group}:${it.key}`, group, ...more(it) }))
const kindName = (t) => vocab.value.kinds[kindOf(t)] || 'картка'
const items = computed(() => [
  ...tag(roleItems(), 'Нова сутність — обери тип', (it) => ({ open: 'entity', prefill: { role: it.key } })),
  ...tag(windowTypeItems(), 'Нове вікно — обери тип', (it) => ({ open: 'window', prefill: { task: it.key } })),
  ...(ed.simple ? [] : [
    ...tag(FORMS, 'Розділи опису'),
    ...tag(statItems(), 'Параметр сутності'),
    ...cardItems(['mechanic', 'rule', 'element', 'field', 'level', 'game']).map((it) => ({ ...it, hint: kindName(it.task), group: `${kindName(it.task)} · ${it.group}` })),
  ]),
])

async function pick(it) {
  error.value = ''
  if (it.open) return emit('open', it.open, it.prefill)
  if (it.go) return jump(it.go)
  if (it.stat) return (step.value = { stat: it.stat, part: ed.entities.length === 1 ? ed.entities[0].id : '', value: '' })
  const kind = kindOf(it.task)
  if (kind === 'rule') return emit('open', 'rule', { ...it.task.rule, card: it.task.slug })  // the card's template starts the rule
  if (kind === 'mechanic' || kind === 'element') {
    const hosts = kind === 'element' ? ed.windows : ed.entities
    return (step.value = { task: it.task, part: hosts.length === 1 ? hosts[0].id : '', params: {} })
  }
  try {
    const c = await postClaim({ task: it.task.slug, part: kind === 'field' && ed.field ? ed.field.id : '', params: {} })
    ed.changed()
    jump(kind === 'field' && !ed.field ? 'drafts' : `c-${c.id}`)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div>
    <AddStep v-if="step" :step @done="step = null" />
    <template v-else>
      <Picker :items placeholder="＋ Додати: що є в грі — «ворог», «життя», «пауза», «телепорт», «правило»…" @pick="pick" />
      <div class="form-text">
        Швидке додавання: напиши своїми словами, що є в грі, — знайде тип сутності, тип вікна{{ ed.simple ? '' : ', параметр чи картку каталогу' }}
        і покладе на місце. Те саме роблять «＋» у секціях нижче.
      </div>
    </template>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>
