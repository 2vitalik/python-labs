<script setup>
import { computed, ref } from 'vue'

import { plural } from '../plural.js'
import ViewLibNode from './ViewLibNode.vue'

// the library by origin (T315 §8): a tree of «made from» — the roots are the views made of nothing or of a view no longer
// among the live ones; under each view its versions open. `keep` — while a search, a tag or ⭐ picks views: the ones it
// picks stand with the way to them, the rest fold into «… 3 проміжні» that a click opens in place. `only` — the
// versions too keep only the first, the current and the starred
const props = defineProps({ views: { type: Array, required: true }, keep: Function, only: Boolean })
const live = computed(() => new Set(props.views.map((v) => v.slug)))
const kids = computed(() => {
  const by = {}
  for (const v of props.views) (by[live.value.has(v.parent) ? v.parent : ''] ||= []).push(v)
  return by
})
const kidsOf = (slug) => kids.value[slug] || []
const has = (v) => props.keep(v) || kidsOf(v.slug).some(has)
const size = (v) => 1 + kidsOf(v.slug).reduce((n, k) => n + size(k), 0)
// the children a node shows, and how many views fold under «… N»
function branch(slug, all) {
  const list = kidsOf(slug)
  if (all || !props.keep) return { shown: list, hidden: 0 }
  return { shown: list.filter(has), hidden: list.filter((v) => !has(v)).reduce((n, v) => n + size(v), 0) }
}
const more = ref(false)
const top = computed(() => branch('', more.value))
</script>

<template>
  <ul class="vtree">
    <ViewLibNode v-for="v in top.shown" :key="v.slug" :view="v" :branch :keep :only :all="more" />
    <li v-if="top.hidden" class="vtree-more">
      <button type="button" class="more-field" @click="more = true">… ще {{ top.hidden }} {{ plural(top.hidden, 'вид', 'види', 'видів') }}</button>
    </li>
  </ul>
</template>

<style scoped>
.vtree { margin: 0; padding: 0; list-style: none; }
.vtree-more { padding: .2rem 0 .2rem 1.6rem; }
</style>
