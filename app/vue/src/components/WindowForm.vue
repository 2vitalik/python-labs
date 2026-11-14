<script setup>
import { computed, nextTick, onMounted, reactive, ref } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { postPart, putPart } from '../api.js'
import { useEd } from '../ed.js'
import { windowTypeItems } from '../items.js'
import { jump } from '../jump.js'
import CoinBadge from './CoinBadge.vue'
import Picker from './Picker.vue'
import ProposeCard from './ProposeCard.vue'

// a window's form (T270 §10.1, T278 §6, T291 §4): the title and the type from the list of window types side by side, as on
// the card, then what is on it. `part` — the window being edited; without it a new one, `prefill.task` — its type already
// chosen; `focus: 'description'` — opened by the card's «＋ опис», the cursor waits there
const props = defineProps({ part: Object, prefill: Object, focus: String })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const form = reactive({ task: props.part?.task || props.prefill?.task || '', title: props.part?.title || '', description: props.part?.description || '' })
const own = ref(!!props.part)  // the student wrote a title of their own: another type no longer replaces it
const open = ref(false)
const proposing = ref(false)
const busy = ref(false)
const error = ref('')
const titleInput = ref()
const descInput = ref()
const type = computed(() => ed.info(form.task))
const types = computed(() => windowTypeItems().map((it) => ({ ...it, taken: it.key === form.task })))

function choose(slug) {
  form.task = slug
  if (!own.value) form.title = ed.info(slug)?.title || ''
  open.value = proposing.value = false
  nextTick(() => titleInput.value?.focus())
}
if (!props.part && form.task) form.title = type.value?.title || ''
// opened after mount: Pop starts listening for Esc and outside clicks only when its model changes
onMounted(() => {
  if (!form.task) open.value = true
  else if (props.focus === 'description') descInput.value?.$el.focus()
  else titleInput.value?.focus()
})

async function save() {
  error.value = !form.task ? 'Обери тип вікна.' : !form.title.trim() ? 'Напиши назву вікна.' : ''
  if (error.value) return
  busy.value = true
  try {
    const p = props.part
    const saved = p ? await putPart(p.id, { ...form, order: p.order }) : await postPart({ kind: 'window', ...form })
    ed.changed()
    emit('done')
    if (!p) jump(`p-${saved.id}`)
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
      <input ref="titleInput" v-model="form.title" class="form-control form-control-sm name" placeholder="Назва вікна"
             @input="own = !!form.title.trim()" @keydown.enter="save">
      <span class="kind">
        <span class="label">Тип</span>
        <Pop v-model="open" width="24rem" class="flex-grow-1 min-w-0">
          <template #trigger="{ toggle }">
            <button type="button" class="form-select form-select-sm text-start text-truncate" title="Тип вікна" @click="toggle">
              <template v-if="type"><CoinBadge :coin="type.coin" :amount="type.amount" /> {{ type.title }}</template>
              <span v-else class="text-secondary">обери тип: головне меню, пауза, кінець гри…</span>
            </button>
          </template>
          <template v-if="proposing">
            <ProposeCard what="новий тип вікна" all-to="/tasks?zone=interface&sub=menus" zone="interface" subzone="menus" @done="choose('custom-window')" />
            <button type="button" class="btn btn-link btn-sm p-0 mt-1 text-decoration-none" @click="proposing = false">← до списку типів</button>
          </template>
          <Picker v-else inline autofocus :items="types" placeholder="головне меню, пауза, кінець гри…" @pick="choose($event.key)">
            <template #footer>
              <div class="foot">Нема потрібного типу? → <a href="#" @click.prevent="proposing = true">запропонувати</a></div>
            </template>
          </Picker>
        </Pop>
      </span>
    </div>
    <!-- one paragraph, as the card shows it: a long one wraps into more rows, Enter still saves -->
    <GrowArea ref="descInput" v-model="form.description" class="form-control form-control-sm" placeholder="Що на цьому вікні"
              @keydown.enter.prevent="save" />
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" :disabled="busy" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('cancel')">Скасувати</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.frm { gap: .35rem; }
/* the title and the type side by side, as on the card; in a narrow card the type goes under the title */
.top { display: flex; flex-wrap: wrap; align-items: center; gap: .35rem .6rem; }
.name { flex: 1 1 9rem; max-width: 16rem; }
.kind { display: flex; flex: 1 1 12rem; align-items: center; gap: .4rem; min-width: 0; }
.min-w-0 { min-width: 0; }
.foot { margin: .35rem .5rem .1rem; font-size: .8rem; color: var(--bs-secondary-color); }
.label { font-size: .7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
</style>
