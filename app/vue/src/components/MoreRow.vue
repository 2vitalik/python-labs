<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Reveal from '@core/components/Reveal.vue'
import { useEd } from '../ed.js'
import { FEATURE } from '../features.js'

// «ще тут» (T319): under a base section, its features not shown yet — a click turns one on right here. The cards' tools
// come on with it (ed.turnOn), so its empty blocks («＋ параметр», «＋ механіка», «＋ елемент») are there at once.
// `ids` — the section's features; the owner's only, nothing to offer — no row
const p = defineProps({ ids: Array })
const ed = useEd()
const list = computed(() => (ed.editable && !ed.sandbox ? p.ids.filter((id) => !ed.has(id) && ed.offers(id)).map((id) => FEATURE[id]) : []))
const busy = ref(false)
async function open(f) {
  busy.value = true
  await ed.turnOn(f.id)
  busy.value = false
}
</script>

<template>
  <Reveal :show="list.length > 0">
    <div class="more-row">
      <span>ще тут:</span>
      <template v-for="(f, i) in list" :key="f.id">
        <span v-if="i" class="dot">·</span>
        <button type="button" class="more-field" :disabled="busy" :title="f.text" @click="open(f)"><Icon name="plus" /> {{ f.more }}</button>
      </template>
    </div>
  </Reveal>
</template>

<style scoped>
/* a quiet line at the section's end: the dashed rule over it says «more of the same place» */
.more-row { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem .4rem; margin-top: .75rem; padding-top: .4rem;
            border-top: 1px dashed var(--bs-border-color); color: var(--bs-secondary-color); font-size: .76rem; }
.more-row .more-field { white-space: normal; text-align: start; }
.dot { opacity: .6; }
</style>
