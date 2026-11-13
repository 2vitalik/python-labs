<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { zones } from '../catalog.js'
import { TIPS } from '../taskTips.js'
import PartLabel from './PartLabel.vue'

// «Де лежить» of the card form: category (zone), subcategory (subzone), family, order, slug. Folded, it is the caption and
// one muted line of what is set (a card that exists starts so); unfolded, its fields stand in a light frame under the caption.
// `f` is TaskEdit's form, written in place
const props = defineProps({ f: Object, open: Boolean })
const shown = ref(props.open)
const zone = computed(() => zones.value[props.f.zone])
const firstSub = (z) => Object.keys(zones.value[z]?.subzones || {})[0] || ''
</script>

<template>
  <div class="vstack gap-1">
    <button type="button" class="head" :aria-expanded="shown" @click="shown = !shown">
      <PartLabel>Де лежить</PartLabel><Icon :name="shown ? 'down' : 'right'" class="chev" />
      <span v-if="!shown" class="hint">
        {{ zone?.icon }} {{ zone?.title }} · {{ zone?.subzones[f.subzone]?.[0] || '—' }}<template v-if="f.parent">
        · у сімʼї {{ f.parent }}</template> · <span class="font-monospace">{{ f.slug || 'без slug' }}</span>
      </span>
    </button>
    <div v-if="shown" class="row-f frame">
      <label class="f w9">категорія
        <select v-model="f.zone" class="form-select form-select-sm" @change="f.subzone = firstSub(f.zone)">
          <option v-for="(z, k) in zones" :key="k" :value="k">{{ z.icon }} {{ z.title }}</option>
        </select>
      </label>
      <label class="f w9" :title="TIPS.subzone"><span class="tip">підкатегорія</span>
        <select v-model="f.subzone" class="form-select form-select-sm">
          <option v-for="(s, k) in zone?.subzones" :key="k" :value="k">{{ s[1] }} {{ s[0] }}</option>
        </select>
      </label>
      <label class="f w8" :title="TIPS.parent"><span class="tip">сімʼя</span>
        <input v-model="f.parent" class="form-control form-control-sm font-monospace" placeholder="slug батька">
      </label>
      <label class="f w4" :title="TIPS.order"><span class="tip">порядок</span>
        <input v-model.number="f.order" type="number" class="form-control form-control-sm">
      </label>
      <label class="f grow" :title="TIPS.slug"><span class="tip">slug</span>
        <input v-model="f.slug" class="form-control form-control-sm font-monospace">
      </label>
    </div>
  </div>
</template>

<style scoped>
/* the summary runs on after the caption and wraps under it, as text */
.head { padding: 0; border: 0; background: none; color: inherit; text-align: start; }
.chev { margin: 0 .35rem 0 .2rem; font-size: .75rem; color: var(--bs-secondary-color); opacity: .7; }
.head:hover .chev { opacity: 1; }
.frame { padding: .4rem .5rem .5rem; border: 1px solid var(--bs-border-color); border-radius: var(--bs-border-radius);
         background: var(--bs-tertiary-bg); }
</style>
