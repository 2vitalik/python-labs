<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { viaText } from '../graphTree.js'
import { jump } from '../jump.js'

// what makes a transition on the map of windows, and the arrow after it: «☰ items» of «Переходи й дії» in a quiet ink,
// «⚡ reason» of a rule in the rules' violet — a click on a reason goes to its rule, the mouse over it brings the rule's card.
// The arrow points down (T296 §11): the window it leads to stands under the caption — two captions side by side must not
// read as one leading to the other
const props = defineProps({ via: Array })
const items = computed(() => props.via.filter((v) => v.kind === 'item').map((v) => v.title).join(', '))
const rules = computed(() => props.via.filter((v) => v.kind === 'rule'))
</script>

<template>
  <span class="gvia" :title="viaText(via)">
    <span class="words">
      <span v-if="items" class="by-item"><Icon name="menu" /> {{ items }}</span>
      <template v-for="(r, i) in rules" :key="r.title">
        <span v-peek="{ kind: 'rule', id: r.rule }" class="by-rule" role="button" @click.stop="jump(`r-${r.rule}`)"><Icon v-if="!i" name="bolt" /> {{ r.title }}</span><span v-if="i < rules.length - 1" class="by-rule">,</span>
      </template>
    </span>
    <Icon name="arrowdown" class="arr" />
  </span>
</template>

<style scoped>
.gvia { display: inline-flex; align-items: center; gap: .3em; max-width: 100%; font-weight: 500; white-space: nowrap; }
.words { min-width: 0; overflow: hidden; text-overflow: ellipsis; }
.by-item { color: var(--gg-item); }
.by-rule { color: var(--gg-rule); }
.by-rule[role=button]:hover { text-decoration: underline; }
.by-item + .by-rule, .by-rule + .by-rule[role=button] { margin-left: .4em; }
.arr { color: var(--gg-line); font-size: .85em; }
</style>
