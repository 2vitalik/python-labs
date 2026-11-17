<script setup>
// the picker's groups as a strip of their signs (T309): a click brings the group up, the one in view is lit, a group with
// nothing under the colour filter is dim. `live` — the keys of the groups that have something
defineProps({ groups: Array, at: String, live: Set })
defineEmits(['go'])
</script>

<template>
  <div class="tabs" :style="{ '--n': groups.length || 1 }">
    <button v-for="(g, i) in groups" :key="g.key" type="button" class="tab qtip" :class="{ on: g.key === at, 'qtip-end': i > groups.length - 5 }"
            :data-tip="g.title" :aria-label="g.title" :disabled="!live.has(g.key)" tabindex="-1" @click="$emit('go', g.key)">{{ g.sign }}</button>
  </div>
</template>

<style scoped>
.tabs { display: grid; grid-template-columns: repeat(var(--n), minmax(0, 1fr)); height: 1.7rem; border-bottom: 1px solid var(--bs-border-color-translucent); }
.tab { padding: 0; border: 0; border-bottom: 2px solid transparent; background: none; color: inherit; font-size: .95rem; line-height: 1; filter: grayscale(.7); opacity: .75; }
.tab:hover, .tab.on { filter: none; opacity: 1; }
.tab.on { border-bottom-color: var(--bs-primary); }
.tab:disabled { opacity: .2; }
@media (max-width: 575px) {
  .tabs { grid-template-columns: repeat(calc((var(--n) + 1) / 2), minmax(0, 1fr)); height: 3.4rem; }
}
</style>
