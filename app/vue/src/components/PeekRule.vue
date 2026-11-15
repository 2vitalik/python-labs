<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { close, vPeek } from '@core/peek.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import CardSign from './CardSign.vue'
import PartLabel from './PartLabel.vue'
import RuleText from './RuleText.vue'

// a rule's card under the mouse (T284 §2): the whole sentence — its entities and windows are ways on — and the catalog
// cards claimed on it
const props = defineProps({ id: String })
const ed = useEd()
const rule = computed(() => ed.rules.find((r) => r.id === props.id))
const claims = computed(() => ed.ruleClaims(props.id))
const show = () => { close(); jump(`r-${props.id}`) }
</script>

<template>
  <div v-if="rule" class="vstack gap-2">
    <div class="pk-head"><PartLabel icon="⚡" zone="game-logic">Правило</PartLabel></div>
    <RuleText :rule :parts="ed.parts" />
    <div v-if="claims.length">
      <PartLabel icon="🃏">Картки на правилі</PartLabel>
      <div v-for="c in claims" :key="c.id" class="pk-row"><span><CardSign :task="ed.info(c.task)" /> <span v-peek="{ kind: 'task', id: c.task }">{{ ed.info(c.task)?.title || c.task }}</span></span></div>
    </div>
    <button type="button" class="pk-go" @click.stop="show">до правила на сторінці <Icon name="arrow" /></button>
  </div>
</template>
