<script setup>
import { computed } from 'vue'

import { byGroup } from '../studentFilter.js'
import { stateOf } from '../weekSum.js'
import CopyNicks from './CopyNicks.vue'

// how the stream gets on with its weeks: who has finished, who has started, whom to remind; and what people wrote
const props = defineProps({ students: { type: Array, required: true } })
const n = computed(() => Object.fromEntries(['done', 'draft', 'none'].map((k) => [k, props.students.filter((s) => stateOf(s) === k).length])))
const late = computed(() => byGroup(props.students.filter((s) => stateOf(s) !== 'done')))
const comments = computed(() => props.students.filter((s) => s.week?.comment))
</script>

<template>
  <div class="mb-3">
    <div class="mb-2">
      ✅ заповнили <b>{{ n.done }}</b> з {{ students.length }} ·
      <span title="Позначили щось, але «Готово» не натиснули: їхні позначки враховано">✍️ почали {{ n.draft }}</span> · ще ні {{ n.none }}
    </div>
    <details v-if="late.length" class="small mb-1">
      <summary>Хто ще не закінчив — {{ n.draft + n.none }}</summary>
      <div v-for="g in late" :key="g.name" class="mt-2">
        <b>{{ g.name || 'Без групи' }}</b> <span class="text-secondary me-1">{{ g.list.length }}</span> <CopyNicks :people="g.list" />
        <div>
          <template v-for="(s, i) in g.list" :key="s.nick">{{ i ? ', ' : '' }}<RouterLink :to="`/activity?user=${s.nick}`">{{ s.name || s.nick }}</RouterLink>{{ stateOf(s) === 'draft' ? ' ✍️' : '' }}</template>
        </div>
      </div>
    </details>
    <details v-if="comments.length" class="small">
      <summary>Коментарі студентів — {{ comments.length }}</summary>
      <div v-for="s in comments" :key="s.nick" class="mt-1">
        <RouterLink :to="`/activity?user=${s.nick}`">{{ s.name || s.nick }}</RouterLink> <span class="text-secondary">{{ s.group }}</span>: {{ s.week.comment }}
      </div>
    </details>
  </div>
</template>
