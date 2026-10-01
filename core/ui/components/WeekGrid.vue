<script setup>
import { computed, ref } from 'vue'

import { DAYS, hm, slots, startOf } from '../week.js'

// the week as a grid: a column a day, a row a slot, the hours on the left. Whoever uses it says how a cell looks —
// `look(day, row)` gives its class and style — and what is in it (the default slot); `over` lies above the cells
const props = defineProps({ frame: { type: Object, required: true }, look: { type: Function, default: () => null } })
defineEmits(['pick'])
const cells = ref()
defineExpose({ cells })
const rows = computed(() => slots(props.frame))
const hours = computed(() => Array.from({ length: (props.frame.to - props.frame.from) / 60 + 1 }, (_, i) => hm(props.frame.from + i * 60)))
function line(row) {
  const min = startOf(props.frame, row) % 60
  return row && (min === 0 ? 'hour' : min === 30 ? 'half' : '')
}
</script>

<template>
  <div class="week" :style="{ '--days': frame.days }">
    <div class="days"><span v-for="d in frame.days" :key="d">{{ DAYS[d - 1] }}</span></div>
    <div class="d-flex">
      <div class="hours"><span v-for="h in hours" :key="h">{{ h }}</span></div>
      <div ref="cells" class="cells">
        <template v-for="r in rows" :key="r">
          <div v-for="d in frame.days" :key="d" class="cell" :class="[line(r - 1), { first: d === 1 }]" v-bind="look(d - 1, r - 1)"
               @click="$emit('pick', d - 1, r - 1)"><slot :day="d - 1" :row="r - 1" /></div>
        </template>
        <slot name="over" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.week { --slot: 1rem; --hours: 2.6rem; user-select: none; -webkit-user-select: none; -webkit-touch-callout: none; }
.days { display: grid; grid-template-columns: repeat(var(--days), 1fr); margin-left: var(--hours); padding-bottom: .25rem;
        text-align: center; font-size: .8rem; font-weight: 600; color: var(--bs-secondary-color); }
.hours { flex: 0 0 var(--hours); padding-right: .4rem; text-align: right; font-size: .7rem; color: var(--bs-secondary-color); }
/* an hour's label sits on its line, not under it */
.hours span { display: block; height: calc(var(--slot) * 4); line-height: 1; transform: translateY(-.35rem); }
.hours span:last-child { height: 0; }  /* the hour the grid ends at: a label with no rows of its own */
/* pan-y: a swipe scrolls the page, the browser leaves the rest of the touch to us */
.cells { position: relative; flex: 1 1 0; display: grid; grid-template-columns: repeat(var(--days), 1fr); grid-auto-rows: var(--slot);
         border: 1px solid var(--bs-border-color); border-radius: var(--bs-border-radius); overflow: hidden; touch-action: pan-y; cursor: pointer; }
.cell { display: flex; align-items: center; justify-content: center; min-width: 0; font-size: .65rem; line-height: 1;
        border-top: 1px solid transparent; border-left: 1px solid var(--bs-border-color); }
.cell.first { border-left: 0; }
.cell.hour { border-top-color: var(--bs-border-color); }
.cell.half { border-top-color: var(--bs-border-color-translucent); }
.cell.no { background: var(--week-no); }
.cell.meh { background: var(--week-meh); }
.cell.ok { background: var(--week-ok); }
@media (hover: hover) { .cell:hover { box-shadow: inset 0 0 0 1px var(--bs-secondary-color); } }
</style>
