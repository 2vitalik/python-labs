<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { kindOf, vocab } from '../catalog.js'
import { myGame } from '../myGame.js'
import { addable, addsTo } from '../taskMeta.js'
import { user } from '@core/user.js'
import IdeaPop from './IdeaPop.vue'
import Md from './Md.vue'
import RuleShape from './RuleShape.vue'
import TaskAliases from './TaskAliases.vue'
import TaskEdit from './TaskEdit.vue'

// a card unfolded (T274 §2), a row each: its kind and what «＋» does with it, the rule it stands for, the description, the
// claim's params, the other names, a family's variants (the slot), games and the limit, a word about the card to the teacher.
// The pencil asks the card to turn into its form
const props = defineProps({ task: Object, family: Boolean, q: String })
defineEmits(['edit'])
const admin = computed(() => user.value?.status === 'admin')
const kind = computed(() => kindOf(props.task))
const how = computed(() => (admin.value || myGame.value) && !props.family && addable(props.task))  // a family's plus is on its variants
const slotText = (s) => {
  const more = [s.unit, s.type === 'choice' && s.options?.join(' / '), s.required && 'обовʼязково'].filter(Boolean)
  return more.length ? `${s.label} — ${more.join(', ')}` : s.label
}
const adding = ref(false)  // a new variant's form under the family's ones
const variant = computed(() => ({ zone: props.task.zone, subzone: props.task.subzone, parent: props.task.slug, status: 'draft' }))
</script>

<template>
  <div class="px-2 py-2 border-top rounded-bottom" :class="family ? 'bg-body' : 'bg-body-tertiary'">
    <div class="d-flex align-items-start gap-2 mb-1">
      <span class="line me-auto">{{ vocab.kinds[kind] || kind }}<template v-if="how"> · {{ addsTo(task) }}</template></span>
      <button v-if="admin" type="button" class="iact" title="Редагувати картку" @click="$emit('edit')"><Icon name="pencil" /></button>
    </div>
    <RuleShape v-if="kind === 'rule'" :rule="task.rule" class="mb-2" />
    <Md v-if="task.description" :text="task.description" :q class="small mb-2" />
    <div v-if="task.slots?.length" class="line mb-2">
      Параметри заявки:
      <div v-for="s in task.slots" :key="s.key" class="ps-2">· {{ slotText(s) }}</div>
    </div>
    <TaskAliases :task :q class="mb-2" />
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
    <IdeaPop v-slot="{ toggle }" kind="fix" :task="task.slug" :zone="task.zone" :subzone="task.subzone" class="mt-2">
      <button type="button" class="quiet" title="не там лежить, незрозумілий опис, не та ціна, бракує синоніма" @click="toggle">
        💡 є думка про цю картку
      </button>
    </IdeaPop>
  </div>
</template>

<style scoped>
.line { font-size: .8rem; color: var(--bs-secondary-color); }
.game-tag { color: var(--bs-link-color); }
.quiet { padding: 0; border: 0; background: none; font-size: .75rem; color: var(--bs-secondary-color); opacity: .8; }
.quiet:hover { opacity: 1; text-decoration: underline; }
</style>
