<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Reveal from '@core/components/Reveal.vue'
import { useEd } from '../ed.js'
import { FEATURES } from '../features.js'
import { jump } from '@core/jump.js'

// «Ще можна описати» (T319): after the last section, the sections of features not shown yet — a row each: its sign, name,
// a line of what it holds and «＋ відкрити»; a click opens the section and goes there. One the teacher closed is grey,
// «ще готується», with no button. The owner's only; nothing to list — no block
const ed = useEd()
const list = computed(() => (ed.editable && !ed.sandbox ? FEATURES.filter((f) => f.section && !ed.has(f.id)) : []))
const busy = ref(false)
async function open(f) {
  busy.value = true
  await ed.turn(f.id, true)
  busy.value = false
  if (ed.has(f.id)) jump(f.section)
}
</script>

<template>
  <Reveal :show="list.length > 0">
    <div class="more-box">
      <div class="group-cap mb-1">Ще можна описати</div>
      <div v-for="f in list" :key="f.id" class="line" :class="{ off: !ed.offers(f.id) }">
        <span class="sign">{{ f.icon }}</span>
        <span class="what"><b>{{ f.title }}</b> <span class="text">— {{ f.text }}</span></span>
        <button v-if="ed.offers(f.id)" type="button" class="btn btn-sm btn-add py-0 ms-auto" :disabled="busy" @click="open(f)"><Icon name="plus" /> відкрити</button>
        <span v-else class="soon ms-auto">ще готується</span>
      </div>
    </div>
  </Reveal>
</template>

<style scoped>
.more-box { margin-top: 1rem; padding: .4rem .6rem .5rem; border: 1px dashed var(--bs-border-color); border-radius: .5rem; font-size: .82rem; }
.line { display: flex; flex-wrap: wrap; align-items: baseline; gap: .1rem .5rem; padding: .2rem 0; }
.line + .line { border-top: 1px dotted var(--bs-border-color); }
.what { flex: 1 1 14rem; min-width: 0; }
.text { color: var(--bs-secondary-color); }
.off { opacity: .55; }
.soon { font-size: .74rem; color: var(--bs-secondary-color); white-space: nowrap; }
</style>
