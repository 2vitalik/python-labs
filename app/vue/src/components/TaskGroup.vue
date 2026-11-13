<script setup>
import PartLabel from './PartLabel.vue'

// a group of the card form (T284 §6): a small caption in capitals — its hint under the mouse, if any — over the fields
defineProps({ label: String, tip: String })
</script>

<template>
  <div class="vstack gap-1">
    <div><PartLabel :class="{ tip }" :title="tip">{{ label }}</PartLabel></div>
    <slot />
  </div>
</template>
