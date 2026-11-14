<script setup>
import { reactive, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { deletePart, postPart, putPart } from '../api.js'
import { useEd } from '../ed.js'
import MenuTarget from './MenuTarget.vue'
import MoreFields from './MoreFields.vue'
import PartLabel from './PartLabel.vue'
import SaveCancel from './SaveCancel.vue'

// the transitions and actions of a window (T278 §4), edited in place: a row per item — what was pressed or what happened
// and where it leads, side by side as on the card (T291 §4); the notes are rare and come by «＋ нотатки». They are a Part
// of its own (kind menu) hosted on the window, made on the first save — its title stays «Меню «…»»: the samples find it
// by that; an item is { title, window, task, note }
const props = defineProps({ window: Object, menu: Object })
const emit = defineEmits(['done', 'cancel'])
const ed = useEd()
const blank = () => ({ title: '', window: '', task: '', note: '' })
// `noted` — the row came with a note: its field is in sight, the others wait for «＋ нотатки»
const rows = reactive((props.menu?.items || []).map((it) => ({ ...blank(), ...it, noted: !!it.note })))
if (!rows.length) rows.push(blank())
const shown = reactive({ notes: false })
const items = () => rows.map(({ noted, ...it }) => it)
const busy = ref(false)
const error = ref('')

async function run(fn) {
  error.value = ''
  busy.value = true
  try {
    await fn()
    ed.changed()
    emit('done')
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const save = () => run(() => (props.menu
  ? putPart(props.menu.id, { title: props.menu.title, description: props.menu.description, window: props.window.id, items: items() })
  : postPart({ kind: 'menu', title: `Меню «${props.window.title}»`, window: props.window.id, items: items() })))
const remove = () => run(() => deletePart(props.menu.id))
</script>

<template>
  <div class="vstack frm" :class="{ notes: shown.notes }" data-dock>
    <span class="d-flex align-items-center gap-1"><PartLabel icon="↪" zone="interface">Переходи й дії</PartLabel><span class="tip-dock" /></span>
    <Tip id="menu-form-rows">Рядок — що натиснули чи що сталось, і куди це веде: інше вікно або дія — картка, що щось робить
      (рестарт рівня, гучність, збереження). Перехід за подією гри (перемога → вікно) задає правило.</Tip>
    <div v-for="(it, i) in rows" :key="i" class="item">
      <input v-model="it.title" class="form-control form-control-sm what" placeholder="пункт, кнопка, клавіша: «Нова гра», Esc…">
      <MenuTarget v-model:window="it.window" v-model:task="it.task" :host="window.id" />
      <button type="button" class="iact del" title="Прибрати рядок" @click="rows.splice(i, 1)"><Icon name="minus" /></button>
      <input v-if="shown.notes || it.noted" v-model="it.note" class="form-control form-control-sm note" placeholder="нотатка — як: клавіша, сам через 3 с…">
    </div>
    <MoreFields :fields="{ notes: 'нотатки' }" :shown @show="shown[$event] = true" />
    <SaveCancel :disabled="busy" @save="save" @cancel="emit('cancel')">
      <button type="button" class="iact add qtip" data-tip="＋ рядок" aria-label="ще рядок" @click="rows.push(blank())"><Icon name="plus" /></button>
      <DelButton v-if="menu" what="усі переходи й дії цього вікна" @yes="remove" />
    </SaveCancel>
    <div v-if="error" class="text-danger">{{ error }}</div>
  </div>
</template>

<style scoped>
.frm { gap: .35rem; }
/* what · where side by side, as the card's two columns; in a narrow card the target goes under, the note — always under */
.item { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem; }
.what { flex: 1 1 8rem; min-width: 0; max-width: 16rem; }
.note { flex: 1 1 100%; margin-right: 1.6rem; }  /* under the row, short of the minus's column */
.notes .item + .item { padding-top: .35rem; border-top: 1px dashed var(--bs-border-color); }  /* two lines an item: where one ends */
</style>
