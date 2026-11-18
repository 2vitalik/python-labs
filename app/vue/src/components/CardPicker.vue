<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { postClaim } from '../api.js'
import { needsWhy, whyOk } from '../asked.js'
import { kindOf, missingParams } from '../catalog.js'
import { useEd } from '../ed.js'
import { cardItems } from '../items.js'
import { landed } from '@core/jump.js'
import Picker from '@core/components/Picker.vue'
import ProposeCard from './ProposeCard.vue'
import SlotFields from './SlotFields.vue'
import WhyField from './WhyField.vue'

// «＋ механіка» and the like: the catalog's cards of these kinds in a panel; a picked one is claimed at `anchor`
// ({ part } · { rule } · {}), its required params asked first, and the sentence of a card «за запитом» (T319).
// `suggest(task)` lifts a card under «підходять сюди».
// `hold` — the anchor does not exist yet (a new rule's form, T291 §8): the card is only chosen — choose(task, params, why) —
// and the caller claims it once the anchor is saved. `plus` — the trigger is a small violet «＋» by a block's caption (T294 §8),
// the label under the mouse. Under the list — the way to the same cards with room to read them: the catalog's window
// (T318, CatalogWindow), where several are added one after another; `catalog` — the section's own scope of it
const props = defineProps({ kinds: Array, anchor: { type: Object, default: () => ({}) }, label: String, suggest: Function, filter: Function,
                            hold: Boolean, plus: Boolean, catalog: Object })
const emit = defineEmits(['choose'])
const ed = useEd()
const open = ref(false)
const picked = ref(null)  // a row of the list waiting for its params or its sentence
const params = ref({})
const why = ref('')
const asks = (t) => needsWhy(t, ed.teacher || ed.sandbox)
const proposing = ref(false)
const error = ref('')
const here = (c) => (c.part || '') === (props.anchor.part || '') && (c.rule || '') === (props.anchor.rule || '')
const items = computed(() => {
  const all = cardItems(props.kinds, new Set(props.hold ? [] : ed.claims.filter(here).map((c) => c.task)), props.filter)
  const fit = (it) => props.suggest?.(it.task)
  return [...all.filter(fit).map((it) => ({ ...it, group: 'підходять сюди' })), ...all.filter((it) => !fit(it))]
})
const anchored = computed(() => props.hold || !!(props.anchor.part || props.anchor.rule))
const ready = computed(() => !missingParams(picked.value?.task, params.value).length && (!asks(picked.value?.task) || whyOk(why.value)))
const plain = (md) => (md || '').replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_`#>]/g, '')
// the same cards in the catalog's window: claimed at this picker's anchor
const ZONE = { mechanic: 'entities', element: 'interface', field: 'interface', level: 'levels', rule: 'game-logic' }
const host = computed(() => ed.parts.find((p) => p.id === props.anchor.part)?.title)
function roomy() {
  open.value = false
  ed.catalog(props.catalog || {
    title: `Каталог · ${props.label}`, note: host.value ? `додається до «${host.value}»` : props.anchor.rule ? 'додається до правила' : '',
    only: (t) => props.kinds.includes(kindOf(t)) && (!props.filter || props.filter(t)), anchor: anchored.value ? props.anchor : null,
    to: { path: '/tasks', query: ZONE[props.kinds[0]] ? { zone: ZONE[props.kinds[0]] } : {} },
  })
}

watch(open, () => { picked.value = null; proposing.value = false; error.value = '' })

function pick(it) {
  if (asks(it.task) || (anchored.value && missingParams(it.task, {}).length)) {
    picked.value = it
    params.value = {}
    why.value = ''
  } else send(it.task, {})
}
async function send(task, p, w = '') {
  error.value = ''
  if (props.hold) {
    emit('choose', task, p, w)
    open.value = false
    return
  }
  try {
    const c = await postClaim({ task: task.slug, ...props.anchor, params: p, why: w })
    open.value = false
    ed.changed()
    landed(`c-${c.id}`)
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <Pop v-if="ed.editable" v-model="open" width="24rem">
    <template #trigger="{ toggle }">
      <button v-if="plus" type="button" class="iact add qtip" :data-tip="`＋ ${label}`" :aria-label="`додати: ${label}`" @click.stop="toggle"><Icon name="plus" /></button>
      <button v-else type="button" class="btn btn-sm btn-add" @click="toggle"><Icon name="plus" /> {{ label }}</button>
    </template>
    <ProposeCard v-if="proposing" what="нову картку" @done="open = false" @cancel="proposing = false"
                 :zone="ZONE[kinds[0]]"
                 :subzone="{ element: 'hud', field: 'render' }[kinds[0]]" />
    <div v-else-if="picked" class="vstack gap-2">
      <div class="fw-semibold">{{ picked.icon }} {{ picked.title }}</div>
      <div v-if="picked.desc" class="desc">{{ plain(picked.desc) }}</div>
      <WhyField v-if="asks(picked.task)" v-model="why" />
      <div v-if="picked.task.slots?.length" class="d-flex flex-wrap gap-2 align-items-center"><SlotFields :specs="picked.task.slots" :params /></div>
      <div class="d-flex gap-2">
        <button type="button" class="btn btn-sm btn-add" :disabled="!ready" @click="send(picked.task, params, asks(picked.task) ? why.trim() : '')"><Icon name="plus" /> Додати</button>
        <button type="button" class="btn btn-sm btn-outline-secondary" @click="picked = null">Скасувати</button>
      </div>
    </div>
    <Picker v-else inline autofocus :items placeholder="пошук картки…" @pick="pick">
      <template #footer>
        <div class="foot">
          <a v-if="!hold" href="#" title="Ці самі картки у вікні над сторінкою: з описами, підкатегоріями — і додавати можна кілька поспіль" @click.prevent="roomy">Переглянути всі просторо</a>
          <RouterLink v-else to="/tasks" target="_blank">Увесь каталог ↗</RouterLink>
          · нема потрібного — <a href="#" @click.prevent="proposing = true">запропонуй картку</a>
        </div>
      </template>
    </Picker>
    <div v-if="error" class="text-danger small mt-2">{{ error }}</div>
  </Pop>
</template>

<style scoped>
.desc { display: -webkit-box; overflow: hidden; -webkit-line-clamp: 2; -webkit-box-orient: vertical; font-size: .8rem; color: var(--bs-secondary-color); }
.foot { margin: .4rem .5rem .1rem; padding-top: .4rem; border-top: 1px solid var(--bs-border-color-translucent); font-size: .78rem; color: var(--bs-secondary-color); }
</style>
