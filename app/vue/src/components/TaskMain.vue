<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'

import { COIN_NAMES, COINS, STATUSES, vocab } from '../catalog.js'
import { OPT_HINT } from '../taskMeta.js'
import { TIPS } from '../taskTips.js'
import TierEditor from './TierEditor.vue'

// «Основне» of the card form: name, icon, price, how many times — or, by «＋ спадна ціна», price steps that say it instead
// (T291 §13); kind, what it means, status, games, tags. `f` is TaskEdit's form, written in place; `kind` — the one in force,
// `subKind` — the subzone's
const props = defineProps({ f: Object, kind: String, subKind: String })
const tiered = computed(() => !!props.f.tiers?.length)
</script>

<template>
  <div class="vstack main">
    <div class="row-f">
      <label class="f grow">назва<input v-model="f.title" class="form-control form-control-sm" required></label>
      <label class="f w3" :title="TIPS.icon"><span class="tip">іконка</span>
        <input v-model="f.icon" class="form-control form-control-sm text-center">
      </label>
      <label class="f w8" :title="TIPS.coin"><span class="tip">монетка</span>
        <select v-model="f.coin" class="form-select form-select-sm">
          <option value="">—</option>
          <option v-for="(e, k) in COINS" :key="k" :value="k">{{ e }} {{ COIN_NAMES[k] }}</option>
        </select>
      </label>
      <label class="f w4" :title="TIPS.amount"><span class="tip">скільки</span>
        <input v-model.number="f.amount" type="number" step="0.5" min="0" class="form-control form-control-sm">
      </label>
      <label class="f max" :class="{ tiered }" :title="TIPS.max"><span class="tip">разів</span>
        <span class="position-relative">
          <input v-if="tiered" disabled class="form-control form-control-sm">
          <input v-else v-model.number="f.max_count" type="number" min="0" class="form-control form-control-sm">
          <span v-if="tiered" class="unlim">за сходинками</span>
          <span v-else-if="f.max_count === 0" class="unlim">без ліміту</span>
        </span>
      </label>
      <button v-if="!tiered" type="button" class="more-field mb-1" @click="f.tiers = [[3, 1], [0, 0.5]]"><Icon name="plus" /> спадна ціна за повтори</button>
    </div>
    <TierEditor v-if="tiered" v-model="f.tiers" :amount="f.amount" class="tiers" />
    <div class="row-f">
      <label class="f w9" :title="TIPS.kind"><span class="tip">тип</span>
        <select v-model="f.kind" class="form-select form-select-sm">
          <option value="">за підкатегорією: {{ vocab.kinds[subKind] || subKind }}</option>
          <option v-for="(label, k) in vocab.kinds" :key="k" :value="k">{{ label }}</option>
        </select>
      </label>
      <label v-if="OPT_HINT[kind]" class="f w9" :title="TIPS.opt"><span class="tip">що означає</span>
        <input v-model="f.opt" class="form-control form-control-sm font-monospace" :placeholder="OPT_HINT[kind]">
      </label>
      <label class="f w7" :title="TIPS.status"><span class="tip">статус</span>
        <select v-model="f.status" class="form-select form-select-sm">
          <option v-for="(label, k) in STATUSES" :key="k" :value="k">{{ label }}</option>
        </select>
      </label>
      <label class="f grow" :title="TIPS.games"><span class="tip">ігри</span>
        <input v-model="f.games" class="form-control form-control-sm font-monospace" placeholder="усі ігри">
      </label>
      <label class="f grow" :title="TIPS.tags"><span class="tip">теги</span>
        <input v-model="f.tags" class="form-control form-control-sm font-monospace" placeholder="algo, lab1, …">
      </label>
    </div>
  </div>
</template>

<style scoped>
.main { gap: .4rem; }
/* as narrow as «скільки»: the meaning of 0 sits inside the field, so nothing beside it moves */
.max { width: 5.25rem; }
.max.tiered { width: 6.5rem; }  /* the steps decide: the words take the field */
.tiers { max-width: 30rem; padding-left: .5rem; border-left: 2px solid var(--bs-border-color); }
.max input { appearance: textfield; }
.max input::-webkit-inner-spin-button, .max input::-webkit-outer-spin-button { appearance: none; margin: 0; }
.unlim { position: absolute; top: 50%; right: .45rem; transform: translateY(-50%); font-size: .68rem; white-space: nowrap;
         color: var(--bs-secondary-color); pointer-events: none; }
</style>
