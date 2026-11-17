<script setup>
import { computed } from 'vue'

import Avatar from '@core/components/Avatar.vue'
import Icon from '@core/components/Icon.vue'
import { clock, dayOf, labsText, mins, span, word } from '../defense.js'

// a defense in the list (T327 §5): who · what and when · the result · how the remarks stand — the whole row leads to its page
const props = defineProps({ d: Object })
const face = computed(() => { const v = props.d.rates?.all; return v ? word('rates', 'all').steps[Math.round(v) - 1].text : '' })
const result = computed(() => word('results', props.d.result))
const length = computed(() => (props.d.started_at ? span(props.d.minutes ?? mins(props.d.started_at)) : ''))
</script>

<template>
  <RouterLink :to="`/defenses/${d.id}`" class="row1" :class="{ live: !d.ended_at }">
    <Avatar :user="d.student" :size="28" />
    <span class="who"><b>{{ d.student.name }}</b> <span class="dim">{{ d.student.group }}</span><span v-if="d.marks?.includes('star')" title="еталон"> ⭐</span></span>
    <span class="dim">{{ labsText(d.labs) }}</span>
    <span class="dim when">{{ dayOf(d.started_at) }}, {{ clock(d.started_at) }} · {{ d.ended_at ? length : `триває ${length}` }}</span>
    <span class="res" :title="result ? `${result.text}` : 'результат ще не сказано'">{{ result?.icon || '·' }}<span v-if="face" title="загальне враження"> {{ face }}</span></span>
    <span class="cnt" :title="`зауважень прийнято ${d.counts.accepted} із ${d.counts.all}`">
      <template v-if="d.counts.all">{{ d.counts.accepted }}/{{ d.counts.all }}</template>
      <span v-if="d.counts.answered" class="wait" title="відповіді чекають перевірки"><Icon name="clock" /> {{ d.counts.answered }}</span>
      <span v-if="d.counts.draft" class="dim" title="чернетки: ще не надіслано студентові"><Icon name="pencil" /> {{ d.counts.draft }}</span>
    </span>
  </RouterLink>
</template>

<style scoped>
.row1 { display: grid; grid-template-columns: auto minmax(9rem, 1.4fr) minmax(4rem, .6fr) minmax(10rem, 1.2fr) 3.6rem minmax(4.5rem, auto); gap: .2rem .7rem;
        align-items: center; padding: .35rem .4rem; border-bottom: 1px solid var(--bs-border-color-translucent); color: inherit; text-decoration: none; font-size: .88rem; }
.row1:hover { background: var(--bs-tertiary-bg); }
.row1.live { background: color-mix(in srgb, var(--bs-success) 7%, transparent); }
.who { min-width: 0; overflow-wrap: anywhere; }
.dim { font-size: .78rem; color: var(--bs-secondary-color); }
.cnt { display: inline-flex; align-items: center; justify-content: flex-end; gap: .5rem; font-variant-numeric: tabular-nums; }
.wait { color: var(--bs-warning-text-emphasis); font-weight: 600; }
@media (max-width: 767px) {
  .row1 { grid-template-columns: auto minmax(0, 1fr) auto; }
  .when { grid-column: 2 / -1; }
}
</style>
