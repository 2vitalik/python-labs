<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { user } from '@core/user.js'
import { kindOf, subzoneTitle, vocab, zoneOf } from '../catalog.js'
import { useEd } from '../ed.js'
import ClaimJudge from './ClaimJudge.vue'
import ClaimOwner from './ClaimOwner.vue'
import CoinBadge from './CoinBadge.vue'
import Md from './Md.vue'

// a claim's panel (T270 §7): the card it claims — what it is, where it lives, its description — then by who looks:
// the owner edits, moves or drops it, the teacher gives the verdict, anyone else reads the note, the link and the verdict
const props = defineProps({ claim: Object })
const emit = defineEmits(['close'])
const ed = useEd()
const info = computed(() => ed.info(props.claim.task))
const desc = computed(() => info.value?.description || (info.value?.parent && ed.info(info.value.parent)?.description) || '')
const home = computed(() => {
  const where = [zoneOf(info.value).title, subzoneTitle(info.value)].filter(Boolean).join(' › ')
  return [vocab.value.kinds[kindOf(info.value)], where].filter(Boolean).join(' · ')
})
</script>

<template>
  <div class="vstack gap-2">
    <div>
      <div class="d-flex align-items-baseline gap-2">
        <CoinBadge :coin="info?.coin" :amount="info?.amount" />
        <span class="fw-semibold">{{ info?.title || claim.task }}</span>
        <RouterLink v-if="user?.status === 'admin'" :to="`/tasks?q=${claim.task}`" class="ms-auto small text-nowrap" title="картка в каталозі">
          <Icon name="open" /> каталог
        </RouterLink>
      </div>
      <div class="text-secondary small">{{ home }}</div>
    </div>
    <Md v-if="desc" :text="desc" class="desc" />
    <div v-if="claim.verdict && !ed.judge" class="small" :class="claim.status === 'returned' ? 'text-danger' : 'text-secondary'">
      Викладач: {{ claim.verdict }}
    </div>
    <ClaimOwner v-if="ed.editable" :claim @close="emit('close')" />
    <template v-else>
      <div v-if="claim.note" class="note">{{ claim.note }}</div>
      <a v-if="claim.link" :href="claim.link" target="_blank" rel="noopener" class="small text-break"><Icon name="link" /> {{ claim.link }}</a>
      <ClaimJudge v-if="ed.judge" :claim @close="emit('close')" />
    </template>
  </div>
</template>

<style scoped>
.desc { max-height: 14rem; overflow-y: auto; font-size: .82rem; }
.note { padding: .1rem .35rem; border-radius: .25rem; background: color-mix(in srgb, var(--bs-warning) 16%, var(--bs-body-bg)); font-style: italic; }
</style>
