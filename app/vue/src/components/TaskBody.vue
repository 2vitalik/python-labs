<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { kindOf, vocab } from '../catalog.js'
import { useGameCtx } from '../gameCtx.js'
import { PROOFS } from '../proof.js'
import { saveTask } from '../taskForm.js'
import { addable, addsTo } from '../taskMeta.js'
import { ladder, repeatable } from '../tiers.js'
import { user } from '@core/user.js'
import IdeaPop from './IdeaPop.vue'
import InlineMd from '@core/components/InlineMd.vue'
import RuleShape from './RuleShape.vue'
import TaskAliases from './TaskAliases.vue'
import TaskCorePick from './TaskCorePick.vue'
import TaskEdit from './TaskEdit.vue'
import TaskStatusPick from './TaskStatusPick.vue'

// a card unfolded (T274 §2), a row each at one spacing: its kind and what «＋» does with it, the rule it stands for, the
// description, the claim's params, a family's variants (the slot), the price ladder of repeats (a line a step), games; at the bottom, quiet grey lines
// one under another (T284 §6): the proof it asks for, the other names, a word about the card to the teacher.
// The teacher changes the status and the description where they read (T306); the pencil asks the card to turn into its form
const props = defineProps({ task: Object, family: Boolean, q: String })
defineEmits(['edit'])
const ctx = useGameCtx()
const admin = computed(() => user.value?.status === 'admin')
const kind = computed(() => kindOf(props.task))
const how = computed(() => (admin.value || ctx.has.value) && !props.family && addable(props.task))  // a family's plus is on its variants
const proof = computed(() => PROOFS[props.task.proof])
const slotText = (s) => {
  const more = [s.unit, s.type === 'choice' && s.options?.join(' / '), s.required && 'обовʼязково'].filter(Boolean)
  return more.length ? `${s.label} — ${more.join(', ')}` : s.label
}
const adding = ref(false)  // a new variant's form under the family's ones
const variant = computed(() => ({ zone: props.task.zone, subzone: props.task.subzone, parent: props.task.slug, status: 'draft' }))
</script>

<template>
  <div class="px-2 py-2 border-top rounded-bottom vstack gap-2" :class="family ? 'bg-body' : 'bg-body-tertiary'">
    <div class="d-flex align-items-start gap-2">
      <span class="line me-auto">{{ vocab.kinds[kind] || kind }}<template v-if="how"> · {{ addsTo(task) }}</template><template v-if="admin"> ·
        <TaskStatusPick :task can /><template v-if="!family"> · <TaskCorePick :task /></template></template></span>
      <button v-if="admin" type="button" class="iact" title="Редагувати все разом" @click="$emit('edit')"><Icon name="pencil" /></button>
    </div>
    <RuleShape v-if="kind === 'rule'" :rule="task.rule" />
    <InlineMd v-if="task.description || admin" :value="task.description" :can="admin" :q class="small" placeholder="що зробити і що я перевіряю"
              :save="(description) => saveTask(task, { description })">
      <template #empty><span class="more-field" title="опису ще нема — додай пару слів"><Icon name="plus" /> опис</span></template>
    </InlineMd>
    <div v-if="task.slots?.length" class="line">
      Параметри заявки:
      <div v-for="s in task.slots" :key="s.key" class="ps-2">· {{ slotText(s) }}</div>
    </div>
    <div v-if="family">
      <slot />
      <TaskEdit v-if="adding" :task="variant" class="mb-1" @done="adding = false" />
      <button v-else-if="admin" type="button" class="btn btn-sm btn-add" @click="adding = true"><Icon name="plus" /> варіант</button>
    </div>
    <div v-if="repeatable(task)" class="small text-secondary">
      <div v-for="l in ladder(task)" :key="l"><Icon name="repeat" /> {{ l }}</div>
    </div>
    <div v-if="task.games.length" class="d-flex gap-2 flex-wrap align-items-center small">
      <RouterLink v-for="g in task.games" :key="g" :to="`/games/${g}`"
                  class="badge text-bg-light border fw-normal text-decoration-none game-tag">{{ g }}</RouterLink>
    </div>
    <div class="quiet">
      <div v-if="proof" class="help" title="доказ — порада, не вимога: його додають у заявці">
        <span class="ico">{{ proof.icon }}</span>{{ proof.ask }}
      </div>
      <TaskAliases :task :q />
      <IdeaPop v-slot="{ toggle }" kind="fix" :task="task.slug" :zone="task.zone" :subzone="task.subzone">
        <button type="button" class="idea" title="не там лежить, незрозумілий опис, не та ціна, бракує синоніма" @click="toggle">
          <span class="ico">💡</span><span class="word">є думка про цю картку?</span>
        </button>
      </IdeaPop>
    </div>
  </div>
</template>

<style scoped>
.line { font-size: .8rem; color: var(--bs-secondary-color); }
.game-tag { color: var(--bs-link-color); }
/* the quiet lines: TaskAliases' toggle is drawn the same — size, colour, the emoji's column, the dashed word */
.quiet { font-size: .8rem; line-height: 1.5; color: var(--bs-secondary-color); }
.quiet:empty { display: none; }  /* nothing to say: no gap left at the bottom */
.help { cursor: help; }
.ico { display: inline-block; width: 1.5em; opacity: .8; }
.idea { padding: 0; border: 0; background: none; color: inherit; text-align: start; }
.word { text-decoration: underline dashed; text-decoration-color: color-mix(in srgb, currentColor 50%, transparent); text-underline-offset: .2em; }
.idea:hover { color: var(--bs-body-color); }
</style>
