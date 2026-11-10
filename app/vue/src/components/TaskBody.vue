<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { kindOf, ruShown, vocab } from '../catalog.js'
import { myGame } from '../myGame.js'
import { hl } from '../taskFilter.js'
import { autoNote, byLang, LANGS } from '../taskMeta.js'
import { user } from '@core/user.js'
import Md from './Md.vue'
import RuleShape from './RuleShape.vue'
import TaskEdit from './TaskEdit.vue'

// a card unfolded: where it lives, the rule it stands for, the description, the claim's params, the synonyms by language;
// a family's variants come in the slot. The pencil asks the card to turn into its form
const props = defineProps({ task: Object, family: Boolean, q: String })
defineEmits(['edit'])
const admin = computed(() => user.value?.status === 'admin')
const kind = computed(() => kindOf(props.task))
const names = computed(() => {
  const a = byLang(props.task.aliases)
  return Object.keys(LANGS).filter((k) => a[k]?.length && (k !== 'ru' || ruShown.value)).map((k) => [k, a[k]])
})
const slotText = (s) => {
  const more = [s.unit, s.type === 'choice' && s.options?.join(' / '), s.required && 'обовʼязково'].filter(Boolean)
  return more.length ? `${s.label} (${more.join(', ')})` : s.label
}
const adding = ref(false)  // a new variant's form under the family's ones
const variant = computed(() => ({ zone: props.task.zone, subzone: props.task.subzone, parent: props.task.slug, status: 'draft' }))
</script>

<template>
  <div class="px-2 py-2 border-top rounded-bottom" :class="family ? 'bg-body' : 'bg-body-tertiary'">
    <div class="d-flex align-items-start gap-2 mb-1">
      <span class="line me-auto" title="тип картки: де вона живе в описі гри">{{ vocab.kinds[kind] || kind }}</span>
      <button v-if="admin" type="button" class="iact" title="Редагувати картку" @click="$emit('edit')"><Icon name="pencil" /></button>
    </div>
    <RuleShape v-if="kind === 'rule'" :rule="task.rule" class="mb-2" />
    <Md v-if="task.description" :text="task.description" :q class="small mb-2" />
    <div v-if="task.slots?.length" class="line mb-2">Параметри заявки: {{ task.slots.map(slotText).join(' · ') }}</div>
    <div v-if="names.length" class="line mb-2" title="інші назви, за якими картку знаходить пошук">
      <span v-for="[k, words] in names" :key="k" class="me-2">
        <span class="lang">{{ LANGS[k] }}</span> <span v-html="words.map((w) => hl(w, q)).join(' · ')"></span>
      </span>
    </div>
    <div v-if="myGame && vocab.depth !== 'simple' && autoNote(kind)" class="line mb-2">{{ autoNote(kind) }}</div>
    <slot />
    <TaskEdit v-if="adding" :task="variant" class="mb-1" @done="adding = false" />
    <button v-else-if="admin && family" type="button" class="btn btn-sm btn-add mt-1" @click="adding = true">
      <Icon name="plus" /> варіант
    </button>
    <div v-if="task.max_count !== 1 || task.games.length" class="d-flex gap-2 flex-wrap align-items-center small mt-2">
      <span v-if="task.max_count === 0" class="text-secondary">без ліміту повторів</span>
      <span v-else-if="task.max_count > 1" class="text-secondary">до {{ task.max_count }} разів</span>
      <RouterLink v-for="g in task.games" :key="g" :to="`/games/${g}`"
                  class="badge text-bg-light border fw-normal text-decoration-none game-tag">{{ g }}</RouterLink>
    </div>
  </div>
</template>

<style scoped>
.line { font-size: .8rem; color: var(--bs-secondary-color); }
.lang { font-size: .68rem; text-transform: uppercase; letter-spacing: .03em; opacity: .75; }
.game-tag { color: var(--bs-link-color); }
</style>
