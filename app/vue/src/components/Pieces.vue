<script setup>
import { vPeek } from '@core/peek.js'
import { jump } from '../jump.js'

// the pieces of one clause (rules.js: pieces), each looking like what it is: an entity in a frame, a number in bold,
// a state as a pill, the student's own words on a yellowish ground (T270 §4.1); `sub` — a side's letter, a small badge in
// the side's own colour (`sd`: a | b), so «Міна ᴮ» in ТО is found in КОЛИ by the colour (T278 §7). An entity or a window
// named in the clause shows its card under the mouse (T284 §2); a click goes to it on the page
defineProps({ list: Array })
const TIP = { free: 'написано студентом', state: 'стан сутності', name: 'лічильник або параметр', choice: 'варіант зі словника', side: 'сторона події КОЛИ', letter: 'сторона події КОЛИ', not: 'заперечення' }
</script>

<template>
  <span class="pieces">
    <template v-for="(p, i) in list" :key="i">
      <span v-if="p.id" v-peek="{ kind: p.t === 'window' ? 'window' : 'entity', id: p.id }" class="pc ent" role="button" :title="p.tip" @click.stop="jump(`p-${p.id}`)">{{ p.icon }} {{ p.v }}<sup v-if="p.sub" class="pc-ix" :class="`sd-${p.sd}`">{{ p.sub }}</sup></span>
      <span v-else class="pc" :class="[p.t, p.sd && `sd-${p.sd}`, { unknown: p.unknown }]" :title="p.unknown ? 'такого стану в сутності нема — додай його в станах' : p.tip || TIP[p.t]">{{ p.v }}<sup v-if="p.sub" class="pc-ix" :class="`sd-${p.sd}`">{{ p.sub }}</sup></span>
      {{ ' ' }}
    </template>
  </span>
</template>

<style>
:root { --pc-choice: #0b7285; --side-a: #e8590c; --side-b: #7048e8; --side-ink: #fff; }
[data-bs-theme=dark] { --pc-choice: #66d9e8; --side-a: #ff922b; --side-b: #9f86ff; --side-ink: #16181b; }
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
/* a side of КОЛИ: А and Б each of its own colour, the letter a filled badge — small next to its entity, full size alone
   (the side is «будь-хто») */
.sd-a { --sd: var(--side-a); }
.sd-b { --sd: var(--side-b); }
.pc.letter, .pc-ix { border-radius: .6em; background: var(--sd, var(--bs-secondary-color)); color: var(--side-ink); font-weight: 700; }
.pc.letter { padding: .08rem .42rem; font-size: .8em; }
.pc-ix { top: -.45em; margin-left: .2em; padding: .05em .32em; font-size: .62em; line-height: 1.2; }
</style>
