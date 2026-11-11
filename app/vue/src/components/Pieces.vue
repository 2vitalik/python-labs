<script setup>
import { jump } from '../jump.js'

// the pieces of one clause (rules.js: pieces), each looking like what it is: an entity in a frame, a number in bold,
// a state as a pill, the student's own words on a yellowish ground (T270 §4.1); `sub` — a side's letter, small (T278 §7)
defineProps({ list: Array })
const TIP = { free: 'написано студентом', state: 'стан сутності', name: 'лічильник або параметр', choice: 'варіант зі словника', side: 'сторона події КОЛИ', not: 'заперечення' }
</script>

<template>
  <span class="pieces">
    <template v-for="(p, i) in list" :key="i">
      <span v-if="p.id" class="pc ent" role="button" :title="p.tip || `показати «${p.v}»`" @click.stop="jump(`p-${p.id}`)">{{ p.icon }} {{ p.v }}<sup v-if="p.sub" class="pc-ix">{{ p.sub }}</sup></span>
      <span v-else class="pc" :class="[p.t, { unknown: p.unknown }]" :title="p.unknown ? 'такого стану в сутності нема — додай його в станах' : p.tip || TIP[p.t]">{{ p.v }}<sup v-if="p.sub" class="pc-ix">{{ p.sub }}</sup></span>
      {{ ' ' }}
    </template>
  </span>
</template>

<style>
:root { --pc-choice: #0b7285; }
[data-bs-theme=dark] { --pc-choice: #66d9e8; }
.pieces { line-height: 1.7; overflow-wrap: anywhere; }
.pc.ent, .pc.side { padding: .05rem .3rem; border: 1px solid var(--bs-border-color); border-radius: .35rem; background: var(--bs-body-bg); white-space: nowrap; }
.pc.ent:hover { border-color: var(--bs-secondary-color); }
.pc.side { border-style: dashed; color: var(--bs-secondary-color); }
.pc.num { font-weight: 700; font-variant-numeric: tabular-nums; }
.pc.choice { color: var(--pc-choice); }
.pc.state { padding: .05rem .4rem; border: 1px solid var(--bs-info-border-subtle); border-radius: .75rem; background: color-mix(in srgb, var(--bs-info) 14%, var(--bs-body-bg)); }
.pc.state.unknown { text-decoration: underline wavy var(--bs-warning); text-underline-offset: .2em; }
.pc.name { border-bottom: 1px dashed var(--bs-secondary-color); }
.pc.free { padding: .05rem .25rem; border-radius: .25rem; background: color-mix(in srgb, var(--bs-warning) 16%, var(--bs-body-bg)); font-style: italic; }
.pc.not { color: var(--bs-danger); font-weight: 600; }
.pc-ix { margin-left: .15em; font-size: .68em; font-weight: 700; line-height: 0; color: var(--bs-secondary-color); }
</style>
