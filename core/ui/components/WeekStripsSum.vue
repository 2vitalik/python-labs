<script setup>
import { computed } from 'vue'

import { place } from '../weekStrips.js'

// the left edge of a day on the strips (T186): Σ — how many can't come in a slot, the deeper the more, the number where
// a run of equal counts begins; ①–⑤ — the best windows, right next to the people they are about
const props = defineProps({ day: { type: Number, required: true }, counts: { type: Array, required: true }, top: { type: Number, required: true },
                            tops: { type: Array, required: true } })
const sums = computed(() => props.counts[props.day].map((c, r, col) => ({ n: c.no, show: c.no > 0 && c.no !== col[r - 1]?.no })))
const best = computed(() => props.tops.map((w, k) => ({ w, k })).filter(({ w }) => w.day === props.day))
const tone = (n) => n && { background: `color-mix(in srgb, var(--strip-no) ${Math.round(12 + (88 * n) / props.top)}%, var(--bs-body-bg))` }
</script>

<template>
  <div class="side">
    <div class="head">Σ</div>
    <div class="body" :data-day="day">
      <div class="sum"><b v-for="(c, r) in sums" :key="r" :style="tone(c.n)">{{ c.show ? c.n : '' }}</b></div>
      <div class="tops">
        <i v-for="{ w, k } in best" :key="k" :style="place(w.r0, w.n)"><span>{{ k + 1 }}</span></i>
      </div>
    </div>
  </div>
</template>

<style scoped>
.side { flex: 0 0 auto; }
.head { height: calc(var(--label) + var(--names)); display: flex; align-items: flex-end; font-size: .65rem; line-height: var(--label);
        color: var(--bs-secondary-color); padding-left: .3rem; }
.body { display: flex; height: calc(var(--slot) * var(--rows)); }
.sum { width: var(--sum); }
.sum b { display: block; height: var(--slot); font-size: .6rem; font-weight: 400; line-height: var(--slot); text-align: center; font-variant-numeric: tabular-nums; }
.tops { position: relative; width: var(--gut); }
.tops i { position: absolute; left: calc(50% - 1.5px); width: 3px; border-radius: 2px; background: var(--bs-primary); }
/* the number sits on the top of its bar */
.tops span { position: absolute; top: 0; left: 50%; transform: translateX(-50%); width: .8rem; height: .8rem; border-radius: 50%;
             background: var(--bs-primary); color: #fff; font: normal 600 .55rem/.8rem var(--bs-font-sans-serif); text-align: center; }
</style>
