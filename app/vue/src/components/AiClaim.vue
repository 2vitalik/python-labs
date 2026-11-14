<script setup>
import AiCards from './AiCards.vue'

// a card about the game as a whole (the reference node's top `claims`): it lands in its category's section, a coin after
// the teacher's check. `data` — slug | {slug, params}
defineProps({ data: [Object, String] })
</script>

<template>
  <div class="vstack gap-1">
    <AiCards :list="[data]" />
    <div class="ai-sub">картка каталогу — монетка після перевірки викладачем</div>
  </div>
</template>
