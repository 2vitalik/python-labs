<script setup>
import Icon from './Icon.vue'

// a line of a list in the setup panels that is put in order by dragging: the grip, what it holds, ✕ to take it off.
// The drag comes from the owner: v-bind="drag.item(i)" lands on this line
defineProps({ off: { type: String, default: 'Прибрати' } })
const emit = defineEmits(['off'])
</script>

<template>
  <div class="srow">
    <Icon name="grip" class="srow-grip" />
    <slot />
    <button type="button" class="iact mini srow-x" :title="off" @click="emit('off')"><Icon name="x" /></button>
  </div>
</template>

<style scoped>
.srow { display: flex; align-items: center; gap: .35rem; min-width: 0; padding: .2rem .1rem; border-bottom: 1px solid var(--bs-border-color-translucent); cursor: grab; }
.srow-grip { color: var(--bs-secondary-color); opacity: .55; }
.srow:hover .srow-grip { opacity: 1; }
.srow-x { margin-left: auto; }
</style>
