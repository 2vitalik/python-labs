<script setup>
import { computed, ref } from 'vue'

import { ACTIONS, ROLES } from '../gameHistory.js'
import { ago } from '@core/activity.js'
import Diff from '@core/components/Diff.vue'
import IconChevron from '@core/components/IconChevron.vue'

// one change of a game: when · who · what · done · which fields; a click unfolds «було → стало», a field a line
const props = defineProps({ row: { type: Object, required: true } })
const open = ref(false)
const act = computed(() => ACTIONS[props.row.action] || ACTIONS.changed)
const role = computed(() => ROLES[props.row.actor.role] || ROLES.system)
const exact = computed(() => new Date(props.row.at).toLocaleString('uk-UA', { dateStyle: 'long', timeStyle: 'short' }))
const both = computed(() => !['added', 'deleted'].includes(props.row.action))  // a new or a gone object has one side only
const rule = computed(() => props.row.coll === 'rules')
const markdown = (f) => f.key === 'description'  // a line diff reads better than two walls of text
</script>

<template>
  <div class="border rounded mb-2">
    <div class="head d-flex flex-wrap align-items-center column-gap-2 px-3 py-2" role="button" tabindex="0" :aria-expanded="open"
         @click="open = !open" @keydown.enter.space.prevent="open = !open">
      <span class="small text-secondary text-nowrap" :title="exact">{{ ago(row.at) }}</span>
      <span class="small text-nowrap" :title="role.name">{{ role.icon }} {{ row.actor.name }}</span>
      <span>{{ row.what }}<template v-if="row.title && !rule"> «{{ row.title }}»</template></span>
      <span v-if="rule" class="sentence small text-secondary text-truncate">{{ row.title }}</span>
      <span class="small fw-semibold text-nowrap" :class="act.cls">{{ act.word }}</span>
      <span v-if="both && row.fields.length" class="small text-secondary">{{ row.fields.map((f) => f.label).join(', ') }}</span>
      <IconChevron :dir="open ? 'up' : 'down'" class="ms-auto text-secondary flex-shrink-0" />
    </div>
    <div v-if="open" class="border-top px-3 py-2 small">
      <div v-for="f in row.fields" :key="f.key" class="field">
        <span class="text-secondary">{{ f.label }}:</span>
        <Diff v-if="markdown(f)" :old="f.old || ''" :new="f.new || ''" class="mt-1" />
        <template v-else>
          <span v-if="row.action !== 'added'" :class="f.old == null ? 'text-secondary' : 'was'">{{ f.old ?? '—' }}</span>
          <span v-if="both" class="text-secondary"> → </span>
          <span v-if="row.action !== 'deleted'">{{ f.new ?? '—' }}</span>
        </template>
      </div>
      <p v-if="!row.fields.length" class="text-secondary mb-0">Без подробиць.</p>
    </div>
  </div>
</template>

<style scoped>
.head { cursor: pointer; row-gap: .15rem; }
.sentence { min-width: 0; max-width: 100%; }
.field + .field { margin-top: .25rem; }
.field > span:first-child { margin-right: .35rem; }
.was { text-decoration: line-through; color: var(--bs-secondary-color); }
</style>
