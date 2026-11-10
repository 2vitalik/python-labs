<script setup>
import Icon from '@core/components/Icon.vue'
import { COINS } from '../catalog.js'

// the options of one property as tiles, all in sight (T270 §8: no dropdowns); `multi` — the model is a list
const model = defineModel({ type: [String, Array], default: '' })
const p = defineProps({ options: { type: Object, default: () => ({}) }, multi: Boolean })
// vocab.field options are cards { label, icon, desc, coin }, vocab.level ones are plain labels
const opt = (o) => (typeof o === 'string' ? { label: o } : o || {})
const list = () => [].concat(model.value || [])
const on = (v) => (p.multi ? list().includes(v) : model.value === v)
function click(v) {
  if (!p.multi) model.value = on(v) ? '' : v
  else model.value = on(v) ? list().filter((x) => x !== v) : [...list(), v]
}
</script>

<template>
  <div class="d-flex flex-wrap gap-1">
    <button v-for="(o, v) in options" :key="v" type="button" class="opt" :class="{ on: on(v) }" :aria-pressed="on(v)"
            :title="opt(o).desc || null" @click="click(v)">
      <span class="head">
        <span v-if="opt(o).icon">{{ opt(o).icon }}</span>{{ opt(o).label }}
        <Icon v-if="on(v)" name="done" class="text-success" />
      </span>
      <span v-if="opt(o).desc" class="desc">{{ opt(o).desc }}</span>
      <span v-if="COINS[opt(o).coin]" class="coin">{{ COINS[opt(o).coin] }}</span>
    </button>
  </div>
</template>

<style scoped>
.opt { position: relative; display: flex; flex-direction: column; align-items: flex-start; gap: .1rem; flex: 0 1 11rem; min-width: 8rem;
       padding: .3rem 1.4rem .35rem .5rem; border: 1px solid var(--bs-border-color); border-radius: .4rem;
       background: var(--bs-body-bg); color: var(--bs-body-color); text-align: start; line-height: 1.25; }
.opt:hover { border-color: var(--bs-secondary-color); background: var(--bs-tertiary-bg); }
/* chosen — the «already taken» look of T270 §1: green, not the site's blue */
.opt.on { border-color: var(--bs-success); background: color-mix(in srgb, var(--bs-success) 8%, var(--bs-body-bg)); }
.head { display: inline-flex; align-items: center; gap: .25rem; font-size: .8rem; font-weight: 600; }
.desc { display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden; font-size: .72rem; color: var(--bs-secondary-color); }
.coin { position: absolute; top: .2rem; right: .3rem; font-size: .75rem; line-height: 1; }
</style>
