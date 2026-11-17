<script setup>
import { computed, ref } from 'vue'

import { plural } from '../plural.js'
import { useTable } from '../tableCtx.js'
import Reveal from './Reveal.vue'
import SetupFamily from './SetupFamily.vue'

// one section of the column catalog (T315 §3): its columns in families, a line each; the minor ones wait at its tail
// behind a quiet link that opens them in place. A search shows everything it finds. The slot — what stands under the caption
const props = defineProps({ cat: String, cols: Array, searching: Boolean })
const t = useTable()
const more = ref(false)
function families(list) {
  const rows = []
  const at = {}
  for (const c of list) {
    if (c.fam && c.fam in at) rows[at[c.fam]].push(c)
    else {
      if (c.fam) at[c.fam] = rows.length
      rows.push([c])
    }
  }
  return rows
}
const minor = computed(() => (props.searching ? [] : props.cols.filter((c) => t.quiet(c))))
const lead = computed(() => families(props.cols.filter((c) => !minor.value.includes(c))))
const tail = computed(() => families(minor.value))
</script>

<template>
  <section class="ssec">
    <div class="group-cap">{{ cat }}</div>
    <slot />
    <SetupFamily v-for="f in lead" :key="f[0].key" :cols="f" />
    <template v-if="tail.length">
      <button type="button" class="more-field" :aria-expanded="more" @click="more = !more">
        {{ more ? 'згорнути' : 'ще' }} {{ minor.length }} {{ plural(minor.length, 'другорядна', 'другорядні', 'другорядних') }}</button>
      <Reveal :show="more"><SetupFamily v-for="f in tail" :key="f[0].key" :cols="f" /></Reveal>
    </template>
  </section>
</template>

<style scoped>
.ssec + .ssec { margin-top: .45rem; }
</style>
