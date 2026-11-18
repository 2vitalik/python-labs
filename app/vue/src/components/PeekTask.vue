<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { close } from '@core/peek.js'
import { user } from '@core/user.js'
import { kindOf, subzoneTitle, taskIndex, vocab, zoneOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { PROOFS } from '../proof.js'
import CardSign from './CardSign.vue'
import CoinBadge from './CoinBadge.vue'
import Md from '@core/components/Md.vue'

// a catalog card under the mouse (T284 §2): its sign and name with the price at the end (T296 §10, §14), what kind of card
// it is and where it lives, its description, what a claim states and shows. `id` — the card's slug; `hint` — what a click
// on the mention does (a claim's row: its panel)
const props = defineProps({ id: String, hint: String })
const ed = useEd()
const info = computed(() => ed?.info(props.id) || taskIndex.value[props.id])
const parent = computed(() => info.value?.parent && (ed?.info(info.value.parent) || taskIndex.value[info.value.parent]))
const desc = computed(() => info.value?.description || parent.value?.description || '')
const home = computed(() => {
  const where = [zoneOf(info.value).title, subzoneTitle(info.value)].filter(Boolean).join(' › ')
  return [vocab.value.kinds[kindOf(info.value)], where].filter(Boolean).join(' · ')
})
const proof = computed(() => PROOFS[info.value?.proof])
</script>

<template>
  <div v-if="info" class="vstack gap-2">
    <div>
      <div class="pk-head pk-one">
        <CardSign :task="info" class="pk-sign" />
        <span class="fw-semibold">{{ info.icon }} {{ info.title }}</span>
        <CoinBadge :coin="info.coin" :amount="info.amount" />
      </div>
      <div class="text-secondary small">{{ home }}<template v-if="parent"> · у сімʼї «{{ parent.title }}»</template></div>
    </div>
    <Md v-if="desc" :text="desc" class="desc" />
    <div v-else class="text-secondary">Опису ще нема.</div>
    <div v-if="info.slots?.length" class="small text-secondary">
      У заявці вказують: <span v-for="(s, i) in info.slots" :key="s.key">{{ i ? ', ' : '' }}{{ s.label.toLowerCase() }}</span>
    </div>
    <div v-if="proof" class="small text-secondary">{{ proof.icon }} {{ proof.ask }}</div>
    <div v-if="hint" class="pk-hint"><Icon name="pencil" /> {{ hint }}</div>
    <RouterLink v-if="user?.status === 'admin'" :to="`/tasks?q=${id}`" class="pk-go" @click="close"><Icon name="open" /> картка в каталозі</RouterLink>
  </div>
  <div v-else class="text-secondary">Картки «{{ id }}» в каталозі нема.</div>
</template>

<style scoped>
.desc { font-size: .84rem; }
</style>
