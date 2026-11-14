<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { plural } from '@core/plural.js'
import { addable, apply, GROUPS, mark, tally } from '../ai.js'
import { useEd } from '../ed.js'
import AiGroup from './AiGroup.vue'

// one round of «Описати словами» (T289 §1, contract §8): folded — a line of when and what became of its proposals;
// unfolded — the proposals by groups in the description's order, «Додати все» for the open ones. One with proposals still
// waiting opens by itself. Adding writes the named ones and what they need, then the description below is read again
// (ed.changed); the rows stay where they were, in their new state
const props = defineProps({ draft: Object })
const ed = useEd()
const t = computed(() => tally(props.draft))
const open = ref(t.value.open + t.value.unknown > 0)
const words = ref(false)  // the student's text shown
const busy = ref(false)
const error = ref('')
const groups = computed(() => GROUPS.map((g) => ({ ...g, items: props.draft.items.filter((it) => it.group === g.key) })).filter((g) => g.items.length))
const ready = computed(() => props.draft.items.filter((it) => addable(props.draft, it)).map((it) => it.key))
const when = computed(() => new Date(props.draft.at).toLocaleString('uk-UA', { dateStyle: 'medium', timeStyle: 'short' }))
const summary = computed(() => {
  const n = props.draft.items.length, c = t.value
  const parts = [[c.added, 'додано'], [c.rejected, 'відхилено'], [c.exists, 'уже є'], [c.unknown, 'не розпізнано'], [c.open, 'чекають']]
  const said = parts.filter(([k]) => k).map(([k, w]) => `${k} ${w}`).join(' · ')
  return `${n} ${plural(n, 'пропозиція', 'пропозиції', 'пропозицій')}${said ? `: ${said}` : ''}`
})

async function run(job) {
  busy.value = true
  error.value = ''
  try {
    await job()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
const add = (keys) => run(async () => {
  const r = await apply(props.draft, keys)
  await ed.changed()
  if (r.skipped?.length) error.value = `Не додано: ${r.skipped.slice(0, 5).join('; ')}`
})
const setState = (keys, state) => run(() => mark(props.draft, keys, state))
</script>

<template>
  <div class="ai-draft" :class="{ open }">
    <button type="button" class="head" :aria-expanded="open" @click="open = !open">
      <Icon :name="open ? 'down' : 'right'" class="chev" /><Icon name="spark" class="spark" />
      <span>{{ when }}</span><span class="text-secondary">· {{ summary }}</span>
    </button>
    <div v-if="open" class="vstack gap-3 mt-2">
      <div class="vstack gap-1">
        <div class="d-flex flex-wrap align-items-center gap-2">
          <button type="button" class="more-field me-auto" @click="words = !words">{{ words ? 'сховати текст' : 'твій текст' }}</button>
          <button v-if="ready.length" type="button" class="btn btn-sm btn-add" :disabled="busy" @click="add(ready)"><Icon name="plus" /> Додати все ({{ ready.length }})</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="open = false"><Icon name="fold" /> Згорнути</button>
        </div>
        <div v-if="words" class="said">{{ draft.text }}</div>
        <div v-if="draft.error" class="text-danger small">{{ draft.error }}</div>
        <div v-if="error" class="text-danger small">{{ error }}</div>
      </div>
      <AiGroup v-for="g in groups" :key="g.key" :group="g" :draft :busy @add="add" @mark="setState" />
      <div v-if="!groups.length && !draft.error" class="small text-secondary">Пропозицій нема — спробуй описати інакше.</div>
      <div v-if="groups.length" class="small text-secondary">Нічого не додається само. Твій текст і пропозиції лишаються тут: нерозібрані чекають, доки не вирішиш.</div>
    </div>
  </div>
</template>

<style scoped>
.ai-draft { padding: .35rem .6rem; border: 1px solid var(--bs-border-color); border-radius: .5rem; }
.ai-draft.open { padding-bottom: .75rem; }
.head { display: flex; flex-wrap: wrap; align-items: center; gap: .1rem .4rem; width: 100%; padding: 0; border: 0; background: none; color: inherit;
        font-size: .86rem; text-align: start; }
.chev { color: var(--bs-secondary-color); }
.spark { color: var(--act-add); }
.said { padding: .3rem .5rem; border-left: 3px solid var(--bs-border-color); color: var(--bs-secondary-color); font-size: .84rem; white-space: pre-wrap; }
</style>
