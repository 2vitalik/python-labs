<script setup>
import { hm } from '../week.js'
import { LAYERS } from '../weekView.js'

// how /week looks (T186): strips or numbers, how long a class is, the order of strips in a group; the legend says what is what.
// `roomy` — a day's page: strips only; `busy` — the teacher has hours they can't, hatched on the grid
const props = defineProps({ roomy: Boolean, busy: Boolean })
const view = defineModel('view', { type: String, required: true })
const len = defineModel('len', { type: Number, required: true })
const sort = defineModel('sort', { type: String, required: true })
const layer = defineModel('layer', { type: String, required: true })
const LENS = [80, 90, 120, 160]
const on = (yes) => (yes ? 'btn-secondary' : 'btn-outline-secondary')
const strips = () => props.roomy || view.value === 'strips'
</script>

<template>
  <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
    <div v-if="!roomy" class="btn-group btn-group-sm">
      <button type="button" class="btn" :class="on(view === 'strips')" title="Кожен студент — окрема смужка" @click="view = 'strips'">Смужки</button>
      <button type="button" class="btn" :class="on(view === 'heat')" title="У клітинці — скільки людей" @click="view = 'heat'">Числа</button>
    </div>
    <div class="btn-group btn-group-sm" title="Скільки триває пара">
      <button v-for="l in LENS" :key="l" type="button" class="btn" :class="on(l === len)" @click="len = l">{{ hm(l) }}</button>
    </div>
    <div v-if="strips()" class="btn-group btn-group-sm" title="Порядок смужок у групі">
      <button type="button" class="btn" :class="on(sort === 'busy')" @click="sort = 'busy'">за зайнятістю</button>
      <button type="button" class="btn" :class="on(sort === 'name')" @click="sort = 'name'">за абеткою</button>
    </div>
    <div v-else class="btn-group btn-group-sm">
      <button v-for="(text, key) in LAYERS" :key="key" type="button" class="btn" :class="on(key === layer)" @click="layer = key">{{ text }}</button>
    </div>
    <span class="small text-secondary">
      <template v-if="strips()">
        <i class="key no"></i> не можу <i class="key meh"></i> незручно <i class="key ok"></i> найкраще <i class="key"></i> можу ·
        <span class="dot">1</span>…<span class="dot">5</span> найкращі вікна ·
      </template>
      <template v-else>у клітинці — скільки людей ·</template>
      <template v-if="busy"><i class="key busy"></i> ти не можеш</template>
      <template v-else>свої години познач у «Мій тиждень» — їх заштрихує</template>
    </span>
  </div>
</template>

<style scoped>
.key { display: inline-block; width: .75rem; height: .75rem; vertical-align: -.1rem; border-radius: 2px;
       background: color-mix(in srgb, var(--bs-body-color) 5%, var(--bs-body-bg)); border: 1px solid var(--bs-border-color-translucent); }
.key.no { background: var(--strip-no); }
.key.meh { background: var(--strip-meh); }
.key.ok { background: var(--strip-ok); }
.key.busy { background: repeating-linear-gradient(135deg, transparent 0 3px, color-mix(in srgb, var(--bs-body-color) 40%, transparent) 3px 4px); }
.dot { display: inline-block; width: .8rem; height: .8rem; border-radius: 50%; background: var(--bs-primary); color: #fff;
       font: 600 .55rem/.8rem var(--bs-font-sans-serif); text-align: center; vertical-align: .05rem; }
</style>
