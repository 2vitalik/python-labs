<script setup>
// a block that comes and goes with a switch (T310): it opens downwards and fades in — the eye sees where the new thing
// came from, and what is under it glides instead of jumping. `gap` — it stands in a stack with gaps (.5rem): the gap
// comes and goes with it
defineProps({ show: Boolean, gap: Boolean })
</script>

<template>
  <Transition name="reveal">
    <div v-if="show" class="reveal" :class="{ gap }"><div class="reveal-in"><slot /></div></div>
  </Transition>
</template>

<style>
.reveal { display: grid; grid-template-rows: 1fr; }
.reveal-in { min-width: 0; min-height: 0; }
.reveal-enter-active, .reveal-leave-active { transition: grid-template-rows .22s ease, opacity .22s ease, margin .22s ease; }
.reveal-enter-active > .reveal-in, .reveal-leave-active > .reveal-in { overflow: hidden; }
.reveal-enter-from, .reveal-leave-to { grid-template-rows: 0fr; opacity: 0; }
.reveal.gap.reveal-enter-from, .reveal.gap.reveal-leave-to { margin-bottom: -.5rem; }
@media (prefers-reduced-motion: reduce) { .reveal-enter-active, .reveal-leave-active { transition: none; } }
</style>
