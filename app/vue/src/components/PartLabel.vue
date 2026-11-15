<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { zones } from '../catalog.js'

// the caption of a block inside a card (T278 §5): a small sign and a word in capitals, in the colour of the catalog
// category the block belongs to. `pic` — a drawn icon's name (T301 §5: the editor's own things wear the site's drawings,
// a little taller than the capitals), `icon` — a text sign (a category's emoji); `zone` — its key in `zones` (entities,
// game-logic, interface, field, levels)
const props = defineProps({ pic: String, icon: String, zone: String })
const color = computed(() => zones.value[props.zone]?.color)
</script>

<template>
  <span class="plabel" :style="color ? { '--z': color } : null"><Icon v-if="pic" :name="pic" class="pic" /><span v-else-if="icon" class="ico">{{ icon }}</span><slot /></span>
</template>

<style scoped>
/* mixed with the text's own colour, as RuleGroup's names: darker on the light theme, lighter on the dark one */
.plabel { display: inline-flex; align-items: center; gap: .3rem; font-size: .7rem; font-weight: 700; letter-spacing: .05em;
          text-transform: uppercase; color: color-mix(in srgb, var(--z, var(--bs-secondary-color)) 78%, var(--bs-body-color)); }
.pic { font-size: .95rem; }
.ico { font-size: .8rem; line-height: 1; letter-spacing: 0; }
</style>
