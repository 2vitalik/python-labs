<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { COINS } from '../catalog.js'
import OptionInfo from './OptionInfo.vue'

// the options of one property as tiles, all in sight (T270 §8: no dropdowns); `multi` — the model is a list
const model = defineModel({ type: [String, Array], default: '' })
const p = defineProps({ options: { type: Object, default: () => ({}) }, multi: Boolean })
// vocab.field options are cards { label, icon, desc, coin, slug }, vocab.level ones are plain labels
const tiles = computed(() => Object.entries(p.options).map(([v, o]) => ({ v, ...(typeof o === 'string' ? { label: o } : o) })))
const list = () => [].concat(model.value || [])
const on = (v) => (p.multi ? list().includes(v) : model.value === v)
function click(v) {
  if (!p.multi) model.value = on(v) ? '' : v
  else model.value = on(v) ? list().filter((x) => x !== v) : [...list(), v]
}
</script>

<template>
  <div class="d-flex flex-wrap gap-1">
    <!-- «ⓘ» is the tile's neighbour laid over its corner, not its child: no button inside a button, and its click selects nothing -->
    <div v-for="t in tiles" :key="t.v" class="cell">
      <button type="button" class="opt" :class="{ on: on(t.v), coined: COINS[t.coin] }" :aria-pressed="on(t.v)"
              :title="t.desc || null" @click="click(t.v)">
        <span class="head"><span v-if="t.icon">{{ t.icon }}</span>{{ t.label }}</span>
        <span v-if="t.desc" class="desc">{{ t.desc }}</span>
        <span class="corner">
          <Icon name="done" class="tick text-success" :class="{ off: !on(t.v) }" />
          <span v-if="COINS[t.coin]">{{ COINS[t.coin] }}</span>
        </span>
      </button>
      <span v-if="t.desc" class="info-at"><OptionInfo :o="t" /></span>
    </div>
  </div>
</template>

<style scoped>
.cell { position: relative; display: flex; flex: 0 1 11rem; min-width: 8rem; }
.opt { position: relative; flex: 1; display: flex; flex-direction: column; align-items: flex-start; gap: .1rem;
       padding: .3rem 1.4rem .35rem .5rem; border: 1px solid var(--bs-border-color); border-radius: .4rem;
       background: var(--bs-body-bg); color: var(--bs-body-color); text-align: start; line-height: 1.25; }
.opt:hover { border-color: var(--bs-secondary-color); background: var(--bs-tertiary-bg); }
/* chosen — the «already taken» look of T270 §1: green, not the site's blue */
.opt.on { border-color: var(--bs-success); background: color-mix(in srgb, var(--bs-success) 8%, var(--bs-body-bg)); }
.head { display: inline-flex; align-items: center; gap: .25rem; font-size: .8rem; font-weight: 600; }
/* the tick's place left of the coin is kept, chosen or not: the title never shifts */
.coined .head { padding-right: .9rem; }
.desc { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-size: .72rem; color: var(--bs-secondary-color); }
.corner { position: absolute; top: .3rem; right: .3rem; display: inline-flex; align-items: center; gap: .15rem; height: 1rem;
          font-size: .75rem; line-height: 1; }
.tick { font-size: .85rem; }
.tick.off { visibility: hidden; }
.info-at { position: absolute; right: .2rem; bottom: .15rem; line-height: 1; }
</style>
