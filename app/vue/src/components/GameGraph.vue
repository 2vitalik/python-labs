<script setup>
import { computed, onMounted, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { load, save } from '@core/local.js'
import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { layout } from '../graphLayout.js'
import { forest } from '../graphTree.js'
import { useJumps } from '../windowJumps.js'
import '../windowTone.css'
import GraphOutline from './GraphOutline.vue'
import GraphWide from './GraphWide.vue'

// the map of windows (T270 §10.4, T274 §9, T284 §1): a tree from the root, «вшир» — left to right (GraphWide), «вглиб» —
// top down in rows (GraphOutline). A window's colour says its type: the main menu, the game screen, any other; what leads
// to a window stands over it — «☰ item →» of «Переходи й дії» in a quiet ink, «⚡ rule →» violet. The transitions the tree
// has no arrow for stand by their node as its children: the label over the window in a dashed frame (GraphJump). The view
// switch hangs over the map's empty corner; the legend is the map's key, and the mouse over a sample dims the rest
const ed = useEd()
const jumps = useJumps()
const still = computed(() => {
  const { kids, extras } = forest(ed.windows, ed.menus, jumps.value)
  return ![...Object.values(kids), ...Object.values(extras)].some((list) => list.length)
})
const hues = computed(() => ({ '--gg-win': zones.value.interface?.color, '--gg-game': zones.value.field?.color, '--gg-by-rule': zones.value['game-logic']?.color }))
const root = ref()
const mode = ref(load('graph-mode'))  // 'wide' | 'deep'; not chosen yet — «вшир» if it fits without scrolling sideways
const only = ref('')  // the legend's sample under the mouse: the map shows only its kind

onMounted(() => {
  const room = root.value.clientWidth || window.innerWidth
  mode.value ||= room < 700 || layout(ed.windows, ed.menus, jumps.value).width > room ? 'deep' : 'wide'
})
const choose = (m) => { mode.value = m; save('graph-mode', m) }
const KEY = [
  ['main', 'усі головні меню одного кольору'], ['game', 'ігровий екран — кольором поля'], ['shot', 'вікно зі скриншотом'], ['bare', 'скриншота ще нема'],
  ['item', 'пункт із «Переходів і дій» вікна'], ['rule', 'перехід робить правило: клік — до правила'], ['jump', 'перехід до вікна, що вже є на схемі: клік — до його картки'],
]
</script>

<template>
  <div ref="root" class="gg" :class="mode" :style="hues" :data-only="only || null">
    <div v-if="!still && mode" class="sw btn-group btn-group-sm" role="group" aria-label="вигляд схеми">
      <button type="button" class="btn btn-outline-secondary" :class="{ active: mode === 'wide' }" @click="choose('wide')"><Icon name="right" /> вшир</button>
      <button type="button" class="btn btn-outline-secondary" :class="{ active: mode === 'deep' }" @click="choose('deep')"><Icon name="down" /> вглиб</button>
    </div>
    <GraphOutline v-if="mode === 'deep'" />
    <GraphWide v-else-if="mode" />
    <div v-if="still" class="small text-secondary">Стрілки зʼявляться, коли переходи вестимуть до інших вікон</div>
    <div v-else class="legend" @mouseleave="only = ''">
      <span v-for="[k, tip] in KEY" :key="k" class="key" :title="tip" @mouseenter="only = k">
        <span v-if="k === 'main'" class="chip gg-w tone-main">Головне меню</span>
        <span v-else-if="k === 'game'" class="chip gg-w tone-game">Гра</span>
        <template v-else-if="k === 'shot'"><Icon name="winshot" class="gg-w sign" /> зі скриншотом</template>
        <template v-else-if="k === 'bare'"><Icon name="win" class="gg-w sign" /> без</template>
        <template v-else-if="k === 'item'"><span class="by-item"><Icon name="menu" /> пункт</span></template>
        <template v-else-if="k === 'rule'"><span class="by-rule"><Icon name="bolt" /> правило</span></template>
        <template v-else><span class="chip ghost gg-w">вікно</span> ще раз</template>
      </span>
    </div>
  </div>
</template>

<style>
/* the map's palette, for both views and their pieces; the windows' own colours are windowTone.css */
.gg { position: relative; --gg-line: color-mix(in srgb, var(--bs-body-color) 35%, var(--bs-body-bg)); --gg-by-rule: #8e24aa;
  --gg-item: color-mix(in srgb, #47658c 62%, var(--bs-body-color)); --gg-rule: color-mix(in srgb, var(--gg-by-rule) 78%, var(--bs-body-color)); }
/* the legend's sample under the mouse: everything of another kind fades */
.gg :is(.gnode, .ghost, .by-item, .by-rule, .edge, .arr, .knee, .rail) { transition: opacity .15s; }
.gg[data-only] :is(.gnode, .ghost, .by-item, .by-rule) { opacity: .22; }
.gg[data-only=main] :is(.gnode, .ghost).tone-main, .gg[data-only=game] :is(.gnode, .ghost).tone-game, .gg[data-only=shot] .gnode.shot,
.gg[data-only=bare] .gnode:not(.shot), .gg[data-only=item] .by-item, .gg[data-only=rule] .by-rule, .gg[data-only=jump] .ghost, .gg[data-only] .legend * { opacity: 1; }
</style>

<style scoped>
/* the switch over the corner the tree leaves empty: right for «вглиб», left for «вшир»; it slides when the view changes */
.sw { position: absolute; z-index: 2; top: 0; left: 0; background: var(--bs-body-bg); transition: left .25s ease, transform .25s ease; }
.deep > .sw { left: 100%; transform: translateX(-100%); }
.legend { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem .9rem; margin-top: .6rem; padding-top: .4rem; border-top: 1px dashed var(--bs-border-color);
          font-size: .7rem; color: var(--bs-secondary-color); }
.key { display: inline-flex; align-items: center; gap: .25rem; cursor: default; }
.chip { padding: 0 .35rem; border: 1px solid var(--w-line); border-radius: 5px; background: var(--w-bg); color: var(--bs-body-color); }
.chip.ghost { border-style: dashed; background: none; color: var(--w-ink); }
.sign { color: var(--w-ink); font-size: .85rem; }
.by-item { color: var(--gg-item); font-weight: 500; }
.by-rule { color: var(--gg-rule); font-weight: 500; }
</style>
