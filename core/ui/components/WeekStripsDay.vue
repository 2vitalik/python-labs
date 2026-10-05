<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

import { short } from '../studentFilter.js'
import { DAY_NAMES, DAYS } from '../week.js'
import { dayMarks } from '../weekStrips.js'
import WeekStripsOver from './WeekStripsOver.vue'
import WeekStripsSum from './WeekStripsSum.vue'

// a day of the strips (T186): Σ and the best windows, then a strip a person, group by group, and what lies over them
// (WeekStripsOver). `nick` — the person under the pointer, outlined in every day; `lit` — the reason whose chip is under it
const props = defineProps({
  day: { type: Number, required: true }, frame: { type: Object, required: true }, groups: { type: Array, required: true },
  counts: { type: Array, required: true }, top: { type: Number, required: true }, tops: { type: Array, required: true },
  mine: Array, picked: Object, ruler: Object, nick: String, lit: Number, roomy: Boolean,
})
const route = useRoute()
const shown = computed(() => props.groups.filter((g) => g.list.length))
const width = computed(() => ({ '--all': shown.value.reduce((n, g) => n + g.list.length, 0), '--k': shown.value.length }))
const marks = computed(() => new Map(shown.value.flatMap((g) => g.list).map(({ s }) => [s.nick, dayMarks(s.week.marks, props.day, props.frame, props.roomy)])))
const dim = (x) => props.lit != null && !x.cats.includes(props.lit)  // a reason's chip is under the pointer, and this mark doesn't name it
const tiny = (name) => (name ? short(name).split('-').at(-1) : '—')  // «ПЗПІ-25-3» → «3»: a narrow group has room for little
const group = (g) => `${g.name || 'Без групи'} · ${g.list.length} з ${g.size}`
function caption(s) {
  const [last, first] = (s.name || s.nick).split(' ')
  return [last, first && `${first[0]}.`, s.week.comment && '💬', !s.week.done_at && '✍️'].filter(Boolean).join(' ')
}
</script>

<template>
  <div class="day" :style="width">
    <RouterLink v-if="!roomy" class="name" :to="{ path: `/week/${day + 1}`, query: route.query }" :title="`${DAY_NAMES[day]} окремо: імена й причини`">
      {{ DAYS[day] }} <span class="text-secondary">›</span></RouterLink>
    <div class="cols">
      <WeekStripsSum :day :counts :top :tops />
      <div class="grps"><div class="set">
        <div v-for="g in shown" :key="g.name" class="grp" :style="{ '--n': g.list.length }">
          <div class="label" :title="roomy ? null : group(g)">{{ roomy ? group(g) : tiny(g.name) }}</div>
          <div v-if="roomy" class="names" :data-d="day">
            <span v-for="{ s } in g.list" :key="s.nick" :class="{ me: s.nick === nick }" :data-nick="s.nick">{{ caption(s) }}</span>
          </div>
          <div class="body" :data-day="day">
            <div v-for="{ s } in g.list" :key="s.nick" class="strip" :class="{ me: s.nick === nick }" :data-nick="s.nick">
              <i v-for="(x, k) in marks.get(s.nick)" :key="k" :class="[x.m.kind, { soft: x.m.soft, dim: dim(x) }]" :style="x.style">{{ x.sign }}</i>
            </div>
          </div>
        </div>
        <WeekStripsOver :day :mine :ruler :picked />
      </div></div>
      <div class="lines"></div>
    </div>
  </div>
</template>

<style scoped>
/* a narrow day scrolls sideways rather than squeezes the strips below --strip-min */
.day { flex: 1 1 0; min-width: max(var(--day-min), calc(var(--sum) + var(--gut) + var(--strip-min) * var(--all) + var(--gap) * var(--k))); }
.day + .day { margin-left: var(--day-gap); }
.name { display: block; height: var(--dayname); text-align: center; font-size: .8rem; font-weight: 600; color: var(--bs-body-color); text-decoration: none; }
.name:hover { text-decoration: underline; }
.cols { position: relative; display: flex; }
.grps { flex: 1 1 0; min-width: 0; }
/* every strip gets the same width: a group grows with its people, the whole set — up to --strip-max a strip */
.set { position: relative; display: flex; max-width: 100%; width: calc(var(--strip-max) * var(--all) + var(--gap) * (var(--k) - 1)); }
.grp { display: flex; flex-direction: column; flex: var(--n) 1 0; min-width: 0; }
.grp + .grp { margin-left: var(--gap); }
.label { height: var(--label); font-size: .65rem; line-height: var(--label); text-align: center; color: var(--bs-secondary-color);
         overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.names { display: flex; height: var(--names); }
.names span { flex: 1 1 0; min-width: 0; padding: .25rem 0; writing-mode: vertical-rl; transform: rotate(180deg); font-size: .7rem; line-height: 1;
              overflow: hidden; white-space: nowrap; text-overflow: ellipsis; }
.body { display: flex; height: calc(var(--slot) * var(--rows)); background: color-mix(in srgb, var(--bs-body-color) 5%, var(--bs-body-bg)); }
.strip { position: relative; flex: 1 1 0; min-width: 0; }
.roomy .strip + .strip { box-shadow: inset 1px 0 var(--bs-body-bg); }
.strip i { position: absolute; left: 0; right: 0; overflow: hidden; font-size: .65rem; font-style: normal; line-height: var(--slot); text-align: center; }
.strip .no { background: var(--strip-no); }
.strip .meh { background: var(--strip-meh); }
.strip .ok { background: var(--strip-ok); }
.strip .soft { background: repeating-linear-gradient(135deg, var(--strip-meh) 0 3px, var(--strip-no) 3px 5px); }
.strip .dim { opacity: .15; }
.me { outline: 1.5px solid var(--bs-emphasis-color); outline-offset: -.5px; z-index: 2; }
/* hour lines over the marks, faint enough to read through */
.lines { position: absolute; left: 0; right: 0; top: calc(var(--label) + var(--names)); height: calc(var(--slot) * var(--rows)); z-index: 1; pointer-events: none;
         background: linear-gradient(color-mix(in srgb, var(--bs-body-color) 20%, transparent) 1px, transparent 1px) 0 0 / 100% calc(var(--slot) * var(--hour)); }
</style>
