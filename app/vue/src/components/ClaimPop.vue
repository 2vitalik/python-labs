<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import { user } from '@core/user.js'
import { asked, needsWhy } from '../asked.js'
import { kindOf, subzoneTitle, vocab, zoneOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { factorsOf, repeatable } from '../tiers.js'
import CardSign from './CardSign.vue'
import ClaimJudge from './ClaimJudge.vue'
import ClaimOwner from './ClaimOwner.vue'
import ClaimShots from './ClaimShots.vue'
import CoinBadge from './CoinBadge.vue'
import Md from '@core/components/Md.vue'

// a claim's panel (T270 §7): the card it claims — what it is, where it lives, its description — then by who looks:
// the owner edits, moves or drops it, the teacher gives the verdict, anyone else reads the note, the link and the verdict;
// the teacher editing a student's game (T282) is both — the owner's fields, then the verdict. A card «за запитом» (T319):
// the student's sentence — what it does in this game — the owner changes it in place
const props = defineProps({ claim: Object, linkFirst: Boolean })  // linkFirst — the owner's cursor starts in the link
const emit = defineEmits(['close'])
const ed = useEd()
const info = computed(() => ed.info(props.claim.task))
const ask = computed(() => asked(info.value) && props.claim.status !== 'accepted')
const why = computed(() => !!props.claim.why || (ask.value && needsWhy(info.value)))
const factor = computed(() => (repeatable(info.value) ? factorsOf(props.claim.task, info.value, ed.claims)[props.claim.id] ?? 1 : 1))
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
        <CardSign :task="info" class="align-self-center" />
        <span class="fw-semibold">{{ info?.title || claim.task }}</span>
        <CoinBadge :coin="info?.coin" :amount="info?.amount" :factor />
        <RouterLink v-if="user?.status === 'admin'" :to="`/tasks?q=${claim.task}`" class="ms-auto small text-nowrap" title="картка в каталозі">
          <Icon name="open" /> каталог
        </RouterLink>
      </div>
      <div class="text-secondary small">{{ home }}</div>
    </div>
    <Md v-if="desc" :text="desc" class="desc" />
    <div v-if="why" class="why">
      <div class="why-cap">Що це робить у грі<template v-if="ask"> · запит: монетка — коли викладач відкриє картку</template></div>
      <InlineText v-if="ed.editable" :value="claim.why" can multi block placeholder="що саме у твоїй грі це робить і як це побачити"
                  :save="(text) => ed.save.claim(claim.id, { why: text })">
        <template #empty><span class="miss">бракує пояснення — клік, щоб написати</span></template>
      </InlineText>
      <div v-else-if="claim.why">{{ claim.why }}</div>
      <div v-else class="miss">бракує пояснення</div>
    </div>
    <div v-if="claim.verdict && !ed.judge" class="small" :class="claim.status === 'returned' ? 'text-danger' : 'text-secondary'">
      Викладач: {{ claim.verdict }}
    </div>
    <ClaimOwner v-if="ed.editable" :claim :link-first @close="emit('close')" />
    <template v-else>
      <div v-if="claim.note" class="note">{{ claim.note }}</div>
      <a v-if="claim.link" :href="claim.link" target="_blank" rel="noopener" class="small text-break"><Icon name="link" /> {{ claim.link }}</a>
      <ClaimShots :claim />
    </template>
    <ClaimJudge v-if="ed.judge" :claim :class="{ 'pt-2 border-top': ed.editable }" @close="emit('close')" />
  </div>
</template>

<style scoped>
.desc { max-height: 14rem; overflow-y: auto; font-size: .82rem; }
.note { padding: .1rem .35rem; border-radius: .25rem; background: color-mix(in srgb, var(--bs-warning) 16%, var(--bs-body-bg)); font-style: italic; }
.why { padding-left: .5rem; border-left: 2px dashed var(--bs-border-color); font-size: .85rem; }
.why-cap { font-size: .72rem; color: var(--bs-secondary-color); }
.miss { color: var(--act-miss); font-size: .8rem; }
</style>
