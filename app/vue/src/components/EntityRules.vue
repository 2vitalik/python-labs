<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import { mentions } from '../rules.js'
import RuleText from './RuleText.vue'

// the rules that name an entity, folded under «Правила (N)» (T270 §7); the section's toggle opens or folds every card's at once
const props = defineProps({ part: Object })
const ed = useEd()
const open = ref(ed.showRules)
watch(() => ed.showRules, (on) => (open.value = on))
const mine = computed(() => ed.rules.filter((r) => mentions(r, props.part.id)))
</script>

<template>
  <div v-if="mine.length">
    <button type="button" class="head" @click="open = !open"><Icon :name="open ? 'down' : 'right'" /> Правила ({{ mine.length }})</button>
    <div v-if="open" class="vstack gap-1 mt-1">
      <div v-for="r in mine" :key="r.id" class="rule" role="button" title="до правила" @click="jump(`r-${r.id}`)">
        <RuleText :rule="r" :parts="ed.parts" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.head { display: inline-flex; align-items: center; gap: .25rem; padding: 0; border: 0; background: none; color: var(--bs-secondary-color);
        font-size: .78rem; font-weight: 600; }
.head:hover { color: var(--bs-body-color); }
.rule { padding: .2rem .35rem; border: 1px solid var(--bs-border-color-translucent); border-radius: .3rem; }
.rule:hover { border-color: var(--bs-border-color); background: var(--bs-tertiary-bg); }
.rule :deep(.rule-text) { font-size: .8rem; }
</style>
