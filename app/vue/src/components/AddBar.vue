<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { aiShown, loadAi, setTab, tab } from '../ai.js'
import { postClaim } from '../api.js'
import { needsWhy } from '../asked.js'
import { kindOf, vocab } from '../catalog.js'
import { useEd } from '../ed.js'
import { homeOf } from '../features.js'
import { cardItems, roleItems, statItems, windowTypeItems } from '../items.js'
import { jump } from '@core/jump.js'
import AddStep from './AddStep.vue'
import AiPanel from './AiPanel.vue'
import Picker from '@core/components/Picker.vue'

// one «＋ Додати» over the whole description (T270 §11): type what the game has — a type of entity, a type of window,
// a parameter, a card — and it lands where its kind says. The «＋» of each section does the same within the section.
// Everything this reader may be offered is here (T319): a thing of a feature not shown yet makes it appear, a closed
// feature's things are not offered; a card «за запитом» asks its sentence in the second step (AddStep).
// Beside it — «✨ Описати словами» (T291 §14): the switch shows only while the server offers the helper, and only on the
// student's own game (not the sample's sandbox, not the teacher's edit of someone's game). Its caption names it (T301 §3):
// one field that adds anything — and finds where it goes
const emit = defineEmits(['open'])  // open(block, prefill): the form of a new entity | window | level | rule
const ed = useEd()
const step = ref(null)
const error = ref('')
const own = computed(() => !ed.teacher && !ed.sandbox)
const words = computed(() => own.value && aiShown.value && tab.value === 'words')
onMounted(() => own.value && loadAi())

const FORMS = [
  { key: 'form:rule', title: 'Правило', icon: '⚡', desc: 'КОЛИ подія — ЯКЩО умова — ТО ефект', words: ['коли', 'якщо', 'взаємодія', 'подія', 'rule'], open: 'rule' },
  { key: 'form:level', title: 'Рівень', icon: '🪜', desc: 'звідки береться, розмір, параметри, скриншот', words: ['мапа', 'карта', 'level'], open: 'level', feature: 'levels' },
  { key: 'form:field', title: 'Поле', icon: '🗺️', desc: 'сітка, вид, час, керування', words: ['сітка', 'grid', 'field'], go: 'field', feature: 'field' },
]
const tag = (list, group, more = () => ({})) => list.map((it) => ({ ...it, key: `${group}:${it.key}`, group, ...more(it) }))
const kindName = (t) => vocab.value.kinds[kindOf(t)] || 'картка'
const offered = (feature) => !feature || ed.offers(feature)
const items = computed(() => [
  ...tag(roleItems(), 'Нова сутність — обери тип', (it) => ({ open: 'entity', prefill: { role: it.key } })),
  ...tag(windowTypeItems(), 'Нове вікно — обери тип', (it) => ({ open: 'window', prefill: { task: it.key } })),
  ...tag(FORMS.filter((f) => offered(f.feature)), 'Розділи опису'),
  ...(offered('stats') ? tag(statItems(), 'Параметр сутності') : []),
  ...cardItems(['mechanic', 'rule', 'element', 'field', 'level', 'game'], null, (t) => offered(homeOf(t)))
    .map((it) => ({ ...it, hint: kindName(it.task), group: `${kindName(it.task)} · ${it.group}` })),
])
const asks = (t) => needsWhy(t, !own.value)

async function pick(it) {
  error.value = ''
  if (it.feature && !ed.has(it.feature)) {  // the section comes first, then the form opens or the page goes there
    await ed.turn(it.feature, true)
    await nextTick()
  }
  if (it.open) return emit('open', it.open, it.prefill)
  if (it.go) return jump(it.go)
  if (it.stat) return (step.value = { stat: it.stat, part: ed.entities.length === 1 ? ed.entities[0].id : '', value: '' })
  const kind = kindOf(it.task)
  const why = asks(it.task)
  if (kind === 'rule' && !why) return emit('open', 'rule', { ...it.task.rule, card: it.task.slug })  // the card's template starts the rule
  if (why || kind === 'mechanic' || kind === 'element') {
    const hosts = kind === 'element' ? ed.windows : kind === 'mechanic' ? ed.entities : []
    return (step.value = { task: it.task, part: hosts.length === 1 ? hosts[0].id : '', params: {}, why: why ? '' : null })
  }
  try {
    const c = await postClaim({ task: it.task.slug, part: kind === 'field' && ed.field ? ed.field.id : '', params: {} })
    ed.changed()
    jump(`c-${c.id}`)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div>
    <div class="group-cap mb-1">Додати в гру</div>
    <div v-if="own && aiShown" class="btn-group btn-group-sm mb-2" role="group" aria-label="як додати">
      <button type="button" class="btn" :class="words ? 'btn-outline-secondary' : 'btn-secondary'" :aria-pressed="!words" @click="setTab('list')">
        <Icon name="plus" /> Додати зі списку</button>
      <button type="button" class="btn" :class="words ? 'btn-secondary' : 'btn-outline-secondary'" :aria-pressed="words" @click="setTab('words')">
        <Icon name="spark" /> Описати словами</button>
    </div>
    <AiPanel v-if="words" />
    <AddStep v-else-if="step" :step @done="step = null" />
    <template v-else>
      <Picker :items placeholder="＋ Додати: що є в грі — «ворог», «життя», «пауза», «телепорт», «правило»…" @pick="pick" />
      <div class="form-text">
        Швидке додавання: напиши своїми словами, що є в грі, — знайде тип сутності, тип вікна, параметр чи картку каталогу
        і покладе на місце. Те саме роблять «＋» у секціях нижче.
      </div>
    </template>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>
