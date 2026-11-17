<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import Pop from '@core/components/Pop.vue'
import { deleteClaim } from '../api.js'
import { asked, needsWhy } from '../asked.js'
import { missingParams, paramsText } from '../catalog.js'
import { useEd } from '../ed.js'
import { shortLink } from '../shortLink.js'
import { factorsOf, repeatable } from '../tiers.js'
import ClaimPop from './ClaimPop.vue'
import CoinBadge from './CoinBadge.vue'

// a claim as a table row where the link is the point (T278 §10): card · link · note · status; a click opens the claim's
// panel, as ClaimRow does, and the owner's trash ends the row — always there, quieter until the mouse is over it (T301 §2).
// The owner writes the link and the note right in their cells (T306): a click beside the link — its address in place, a
// click on the link itself still leads there. Its columns are the table's (`--cols`, SubzoneRows); on a phone the card
// takes a line of its own. A card «за запитом» (T319) says «запит», as ClaimRow does
const props = defineProps({ claim: Object })
const ed = useEd()
const open = ref(false)
const info = computed(() => ed.info(props.claim.task))
const ask = computed(() => asked(info.value) && props.claim.status !== 'accepted')
const noWhy = computed(() => ask.value && needsWhy(info.value) && !props.claim.why?.trim())
const remove = () => deleteClaim(props.claim.id).then(() => ed.changed(), (e) => ed.fail(e.message))
const save = (patch) => ed.save.claim(props.claim.id, patch)
const factor = computed(() => (repeatable(info.value) ? factorsOf(props.claim.task, info.value, ed.claims)[props.claim.id] ?? 1 : 1))
const ptext = computed(() => paramsText(info.value, props.claim.params))
const missing = computed(() => missingParams(info.value, props.claim.params).length > 0)
const tip = computed(() => {
  const t = info.value
  const md = t?.description || (t?.parent && ed.info(t.parent)?.description) || ''
  return md.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_`#>]/g, '')
})

</script>

<template>
  <div :id="`c-${claim.id}`">
    <Pop v-model="open" block width="26rem">
      <template #trigger="{ toggle }">
        <div class="tr" :class="claim.status" role="button" :title="tip" @click="toggle">
          <span class="card-cell">
            <CoinBadge :coin="info?.coin" :amount="info?.amount" :factor :class="{ waits: ask }" />
            <span class="what">
              {{ info?.title || claim.task }}
              <span v-if="ptext" class="muted">{{ ptext }}</span>
              <span v-if="missing" class="need" title="картка чекає обовʼязкових параметрів">параметри?</span>
              <span v-if="ask" class="ask" title="картка за запитом: монетка зарахується, коли викладач відкриє картку">запит</span>
              <span v-if="noWhy" class="miss" title="картка за запитом чекає речення: що саме у грі це робить — клік по рядку">бракує пояснення</span>
            </span>
          </span>
          <span class="link-cell">
            <InlineText v-if="ed.editable" :value="claim.link" can block :save="(link) => save({ link })"
                        :placeholder="info?.zone === 'support' ? 'відео, сторінка гри, документ' : 'файл або коміт на GitHub'">
              <a :href="claim.link" target="_blank" rel="noopener" :title="claim.link" @click.stop>{{ shortLink(claim.link) }}</a>
              <template #empty><span class="add" title="додати посилання: файл, коміт чи відео"><Icon name="plus" /> посилання</span></template>
            </InlineText>
            <a v-else-if="claim.link" :href="claim.link" target="_blank" rel="noopener" :title="claim.link" @click.stop>{{ shortLink(claim.link) }}</a>
            <span v-else class="muted">—</span>
          </span>
          <InlineText v-if="ed.editable" :value="claim.note" can block class="note" placeholder="як саме це зроблено" :save="(note) => save({ note })">
            <template #empty><span class="nadd"><Icon name="plus" /> нотатка</span></template>
          </InlineText>
          <span v-else class="note" :title="claim.note">{{ claim.note }}</span>
          <span class="state">
            <span v-if="claim.status === 'accepted'" class="text-success" title="зараховано"><Icon name="done" /></span>
            <span v-else-if="claim.status === 'returned'" class="text-danger" title="повернуто — доробити"><Icon name="back" /></span>
            <span v-if="ed.editable && !claim.auto" class="del-slot" @click.stop>
              <DelButton :what="`заявку «${info?.title || claim.task}»`" title="Видалити заявку" @yes="remove" />
            </span>
          </span>
          <div v-if="claim.status === 'returned' && claim.verdict" class="verdict">{{ claim.verdict }}</div>
        </div>
      </template>
      <ClaimPop :claim :link-first="!claim.link" @close="open = false" />
    </Pop>
  </div>
</template>

<style scoped>
/* translucent grounds: the flash of a jump (on the wrapper) shows through */
.tr { display: grid; grid-template-columns: var(--cols); column-gap: .6rem; align-items: baseline; padding: .25rem .45rem;
      border-bottom: 1px solid var(--bs-border-color-translucent); font-size: .82rem; }
.tr:hover { background-image: linear-gradient(rgb(127 127 127 / .07), rgb(127 127 127 / .07)); }
.tr.accepted { background-color: color-mix(in srgb, var(--bs-success) 9%, transparent); }
.tr.returned { background-color: color-mix(in srgb, var(--bs-danger) 9%, transparent); }
/* the coin, then the title in a column of its own: a long title wraps under itself */
.card-cell { display: flex; align-items: baseline; gap: .4rem; min-width: 0; }
.what { min-width: 0; overflow-wrap: anywhere; }
.link-cell, .note { min-width: 0; overflow-wrap: anywhere; }
/* one line: a link cut in the middle of a word reads worse than one cut at the end — the whole is in the title */
.link-cell a { display: inline-block; max-width: 100%; overflow: hidden; vertical-align: top; text-decoration: none; text-overflow: ellipsis; white-space: nowrap; }
.link-cell a:hover { text-decoration: underline; }
.muted { color: var(--bs-secondary-color); }
.add { color: var(--act-add); white-space: nowrap; }
.add:hover { text-decoration: underline; }
.need { padding: 0 .3rem; border-radius: .25rem; background: var(--bs-warning-bg-subtle); color: var(--bs-warning-text-emphasis); font-size: .72rem; }
.miss { color: var(--act-miss); font-size: .72rem; white-space: nowrap; }
.ask { padding: 0 .25rem; border: 1px dashed var(--bs-border-color); border-radius: .25rem; color: var(--bs-secondary-color); font-size: .68rem; }
.waits { opacity: .5; }  /* the coin of a request is not counted yet */
.note { display: -webkit-box; overflow: hidden; -webkit-box-orient: vertical; -webkit-line-clamp: 2; font-style: italic; color: var(--bs-secondary-color); }
.note.open { display: block; overflow: visible; }  /* the field in place shows the whole note */
/* an empty note's way in: pale at rest, clear under the mouse — as in the videos' table (T344, T350) */
.nadd { color: var(--act-add); font-style: normal; opacity: .6; }
.tr:hover .nadd, .inl:focus-visible .nadd { opacity: 1; }
.state { display: inline-flex; align-self: center; align-items: center; justify-content: flex-end; gap: .15rem; }
/* the trash of every list (ClaimRow): full size, its height given back so the row keeps the text's */
.del-slot :deep(.trash) { margin-block: -.25rem; font-size: 1rem; opacity: .5; }
.tr:hover .del-slot :deep(.trash), .del-slot:focus-within :deep(.trash) { opacity: 1; }
.verdict { grid-column: 1 / -1; font-size: .75rem; color: var(--bs-danger-text-emphasis); }
@media (max-width: 575px) {
  .tr { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto; row-gap: .1rem; }
  .card-cell { grid-column: 1 / -1; }
}
</style>
