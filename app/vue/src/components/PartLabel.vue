<script setup>
import { computed } from 'vue'

import { zones } from '../catalog.js'

// the caption of a block inside a card (T278 §5): a small icon and a word in capitals, in the colour of the catalog
// category the block belongs to. `zone` — its key in `zones` (entities, game-logic, interface, field, levels)
const props = defineProps({ icon: String, zone: String })
const color = computed(() => zones.value[props.zone]?.color)
</script>

<template>
  <span class="plabel" :style="color ? { '--z': color } : null"><span v-if="icon" class="ico">{{ icon }}</span><slot /></span>
</template>

<style scoped>
/* mixed with the text's own colour, as RuleGroup's names: darker on the light theme, lighter on the dark one */
.plabel { display: inline-flex; align-items: center; gap: .3rem; font-size: .7rem; font-weight: 700; letter-spacing: .05em;
          text-transform: uppercase; color: color-mix(in srgb, var(--z, var(--bs-secondary-color)) 78%, var(--bs-body-color)); }
/* a symbol that has a text form (⚙ ↪ ⚡) is drawn as one, in the caption's colour — not as a colour emoji */
.ico { font-size: .8rem; line-height: 1; letter-spacing: 0; font-variant-emoji: text; }
</style>
