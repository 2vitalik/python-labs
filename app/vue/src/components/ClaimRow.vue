<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { vPeek } from '@core/peek.js'
import { deleteClaim } from '../api.js'
import { iconOf, kindOf, missingParams, paramsText, zoneOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import { sentence } from '../rules.js'
import ClaimPop from './ClaimPop.vue'
import CoinBadge from './CoinBadge.vue'

// one claim as a row (T270 §7): coin · title · params · the student's note · link · status; the mouse over it brings the
// card's description (T284 §2), a click opens the panel with the actions — «⋯» at the end tells the owner so.
// `where` — name the anchor too, a click on it jumps there; `tools` — the row's host is being edited: a trash beside it
const props = defineProps({ claim: Object, where: Boolean, tools: Boolean })
const ed = useEd()
const open = ref(false)
const info = computed(() => ed.info(props.claim.task))
const ptext = computed(() => paramsText(info.value, props.claim.params))
const missing = computed(() => missingParams(info.value, props.claim.params).length > 0)
const remove = () => deleteClaim(props.claim.id).then(() => ed.changed(), (e) => ed.fail(e.message))
const cut = (s, n) => (s.length > n ? `${s.slice(0, n - 1)}…` : s)
const place = computed(() => {
  const c = props.claim
  const p = c.part && ed.parts.find((x) => x.id === c.part)
  if (p) return { id: `p-${p.id}`, text: `${iconOf(p)} ${p.title}` }
  const r = c.rule && ed.rules.find((x) => x.id === c.rule)
  if (r) return { id: `r-${r.id}`, text: `правило: ${cut(sentence(r, ed.parts).when, 28)}` }
  const kind = kindOf(info.value)  // unanchored: a level card lives in «Рівні», a game card in its zone, the rest wait in their section's strip
  return kind === 'level' ? { id: 'levels', text: '🪜 рівні' } : kind === 'game' ? null : { id: `c-${c.id}`, text: 'ще без місця' }
})
</script>

<template>
  <div :id="`c-${claim.id}`" class="crow">
    <Pop v-model="open" block width="26rem" class="flex-grow-1">
      <template #trigger="{ toggle }">
        <div v-peek="open ? null : { kind: 'task', id: claim.task }" class="claim" :class="claim.status" :style="{ '--zc': zoneOf(info).color }" role="button" @click="toggle">
          <div class="line">
            <CoinBadge :coin="info?.coin" :amount="info?.amount" />
            <span class="title">{{ info?.title || claim.task }}</span>
            <span v-if="ptext" class="params">{{ ptext }}</span>
            <span v-if="missing" class="need" title="картка чекає обовʼязкових параметрів">параметри?</span>
            <span v-if="claim.note" class="note">{{ claim.note }}</span>
            <span v-if="claim.auto" class="auto" title="тримається сама — з типу, параметра чи властивості">авто</span>
            <span v-if="claim.shots?.length" class="text-secondary" :title="`є доказ: ${claim.shots.length}`"><Icon name="image" /></span>
            <a v-if="claim.link" :href="claim.link" target="_blank" rel="noopener" class="lnk" title="код" @click.stop><Icon name="link" /></a>
            <span class="end">
              <span v-if="where && place" class="where" role="button" title="показати" @click.stop="jump(place.id)">{{ place.text }}</span>
              <span v-if="claim.status === 'accepted'" class="text-success" title="зараховано"><Icon name="done" /></span>
              <span v-else-if="claim.status === 'returned'" class="text-danger" title="повернуто — доробити"><Icon name="back" /></span>
              <Icon v-if="ed.editable" name="more" class="dots" />
            </span>
          </div>
          <div v-if="claim.status === 'returned' && claim.verdict" class="verdict">{{ claim.verdict }}</div>
        </div>
      </template>
      <ClaimPop :claim @close="open = false" />
    </Pop>
    <DelButton v-if="tools && ed.editable && !claim.auto" :what="`заявку «${info?.title || claim.task}»`" @yes="remove" />
  </div>
</template>

<style scoped>
.crow { display: flex; align-items: flex-start; gap: .15rem; }
.crow > :first-child { min-width: 0; }
.dots { align-self: center; color: var(--bs-secondary-color); opacity: .55; }
.claim:hover .dots { opacity: 1; }
/* translucent grounds: the flash of a jump (on the wrapper) shows through */
.claim { padding: .2rem .45rem; border: 1px solid var(--bs-border-color); border-left: 3px solid var(--zc); border-radius: .3rem; font-size: .82rem; }
.claim:hover { background-image: linear-gradient(rgb(127 127 127 / .07), rgb(127 127 127 / .07)); }
.claim.accepted { background-color: color-mix(in srgb, var(--bs-success) 9%, transparent); }
.claim.returned { background-color: color-mix(in srgb, var(--bs-danger) 9%, transparent); }
.line { display: flex; flex-wrap: wrap; align-items: baseline; column-gap: .4rem; }
.title { min-width: 0; overflow-wrap: anywhere; }
.params, .lnk, .where { color: var(--bs-secondary-color); }
.need { padding: 0 .3rem; border-radius: .25rem; background: var(--bs-warning-bg-subtle); color: var(--bs-warning-text-emphasis); font-size: .72rem; }
.note { min-width: 3rem; overflow: hidden; padding: 0 .25rem; border-radius: .25rem; background: color-mix(in srgb, var(--bs-warning) 16%, var(--bs-body-bg));
        font-style: italic; text-overflow: ellipsis; white-space: nowrap; }
.auto { padding: 0 .25rem; border: 1px solid var(--bs-border-color); border-radius: .25rem; color: var(--bs-secondary-color); font-size: .68rem; }
.lnk:hover, .where:hover { color: var(--bs-body-color); }
.end { display: inline-flex; align-items: baseline; gap: .4rem; margin-left: auto; }
.where { max-width: 14rem; overflow: hidden; font-size: .74rem; text-overflow: ellipsis; white-space: nowrap; }
.where:hover { text-decoration: underline; }
.verdict { font-size: .75rem; color: var(--bs-danger-text-emphasis); }
</style>
