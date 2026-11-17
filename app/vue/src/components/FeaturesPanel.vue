<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { useEd } from '../ed.js'
import { BASE, FEATURES, GROUPS } from '../features.js'
import FeatureRow from './FeatureRow.vue'

// «Можливості» (T319): what the game page holds beyond its base — all at once («Усе»), back to the base, or one by one.
// Turning off takes away only the empty: what has data stays, so nothing filled is ever hidden. The owner's only (GameEditor)
const ed = useEd()
const open = ref(false)
const busy = ref(false)
const groups = GROUPS.map(([id, title]) => ({ id, title, list: FEATURES.filter((f) => f.group === id) }))
const count = computed(() => FEATURES.filter((f) => ed.has(f.id)).length)
const ids = (fn) => FEATURES.filter(fn).map((f) => f.id)
const more = computed(() => ids((f) => !ed.has(f.id) && ed.offers(f.id)))
const less = computed(() => ids((f) => ed.has(f.id) && !ed.filled(f.id)))
async function run(fn) {
  busy.value = true
  await fn()
  busy.value = false
}
</script>

<template>
  <Pop v-model="open" width="26rem">
    <template #trigger="{ toggle }">
      <button type="button" class="btn btn-sm btn-outline-secondary" :aria-expanded="open" title="Що ще описати в грі: усе одразу чи галочками" @click="toggle">
        <Icon name="layers" /> Можливості <span class="cnt">{{ count ? `основа + ${count}` : 'основа' }}</span>
      </button>
    </template>
    <div class="fp vstack gap-2">
      <div class="d-flex flex-wrap gap-2">
        <button type="button" class="btn btn-sm btn-add py-0" :disabled="busy || !more.length" title="Увімкнути все, що відкрито"
                @click="run(() => ed.turn(more, true))"><Icon name="plus" /> Усе</button>
        <button type="button" class="btn btn-sm btn-outline-secondary py-0" :disabled="busy || !less.length" title="Прибрати все порожнє — заповнене лишається"
                @click="run(() => ed.turn(ids((f) => !ed.filled(f.id)), false))">Лише основа</button>
      </div>
      <div class="base">
        <div class="group-cap">Основа — є завжди</div>
        <div v-for="[name, what] in BASE" :key="name"><b>{{ name }}</b> — {{ what }}</div>
      </div>
      <div v-for="g in groups" :key="g.id">
        <div class="group-cap">{{ g.title }}</div>
        <FeatureRow v-for="f in g.list" :key="f.id" :f :busy :run />
      </div>
    </div>
  </Pop>
</template>

<style scoped>
.cnt { font-size: .75rem; opacity: .7; }
/* on a phone the panel is a sheet at the bottom (Pop): the list scrolls inside either way */
.fp { max-height: min(32rem, 65vh); overflow-y: auto; font-size: .82rem; }
.base { padding: .3rem .5rem .4rem; border-radius: .375rem; background: var(--bs-tertiary-bg); color: var(--bs-secondary-color); font-size: .78rem; }
.base b { font-weight: 600; color: var(--bs-body-color); }
</style>
