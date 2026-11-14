<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import Pop from '@core/components/Pop.vue'
import { deleteClaim } from '../api.js'
import { missingParams, paramsText } from '../catalog.js'
import { useEd } from '../ed.js'
import { factorsOf, repeatable } from '../tiers.js'
import ClaimPop from './ClaimPop.vue'
import CoinBadge from './CoinBadge.vue'

// a claim as a table row where the link is the point (T278 §10): card · link · note · status; a click opens the claim's
// panel, as ClaimRow does, and the owner's trash waits in the status cell under the mouse (T291 §6). Its columns are the
// table's (`--cols`, SubzoneRows); on a phone the card takes a line of its own
const props = defineProps({ claim: Object })
const ed = useEd()
const open = ref(false)
const info = computed(() => ed.info(props.claim.task))
const remove = () => deleteClaim(props.claim.id).then(() => ed.changed(), (e) => ed.fail(e.message))
const factor = computed(() => (repeatable(info.value) ? factorsOf(props.claim.task, info.value, ed.claims)[props.claim.id] ?? 1 : 1))
const ptext = computed(() => paramsText(info.value, props.claim.params))
const missing = computed(() => missingParams(info.value, props.claim.params).length > 0)
const tip = computed(() => {
  const t = info.value
  const md = t?.description || (t?.parent && ed.info(t.parent)?.description) || ''
  return md.replace(/\[([^\]]*)\]\([^)]*\)/g, '$1').replace(/[*_`#>]/g, '')
})

const VIDEO = /^(m\.)?(youtube\.com|youtu\.be|vimeo\.com|drive\.google\.com)(\/|$)/
// the link as one reads it: no scheme, no www; a long one keeps its host and its last step, a video gets «▶»
function shortLink(url, max = 32) {
  let s = url.trim().replace(/^[a-z][\w+.-]*:\/\//i, '').replace(/^www\./, '').replace(/\/$/, '')
  const video = VIDEO.test(s)
  if (s.length > max) {
    const host = s.split('/')[0]
    const last = s.slice(s.lastIndexOf('/') + 1)
    s = host.length + last.length + 3 <= max ? `${host}/…/${last}` : `${s.slice(0, max - 13)}…${s.slice(-12)}`
  }
  return video ? `▶ ${s}` : s
}
</script>

<template>
  <div :id="`c-${claim.id}`">
    <Pop v-model="open" block width="26rem">
      <template #trigger="{ toggle }">
        <div class="tr" :class="claim.status" role="button" :title="tip" @click="toggle">
          <span class="card-cell">
            <CoinBadge :coin="info?.coin" :amount="info?.amount" :factor />
            <span class="what">
              {{ info?.title || claim.task }}
              <span v-if="ptext" class="muted">{{ ptext }}</span>
              <span v-if="missing" class="need" title="картка чекає обовʼязкових параметрів">параметри?</span>
            </span>
          </span>
          <span class="link-cell">
            <a v-if="claim.link" :href="claim.link" target="_blank" rel="noopener" :title="claim.link" @click.stop>{{ shortLink(claim.link) }}</a>
            <span v-else-if="ed.editable" class="add" title="додати посилання: файл, коміт чи відео"><Icon name="plus" /> посилання</span>
            <span v-else class="muted">—</span>
          </span>
          <span class="note" :title="claim.note">{{ claim.note }}</span>
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
.link-cell a { display: block; overflow: hidden; text-decoration: none; text-overflow: ellipsis; white-space: nowrap; }
.link-cell a:hover { text-decoration: underline; }
.muted { color: var(--bs-secondary-color); }
.add { color: var(--act-add); white-space: nowrap; }
.add:hover { text-decoration: underline; }
.need { padding: 0 .3rem; border-radius: .25rem; background: var(--bs-warning-bg-subtle); color: var(--bs-warning-text-emphasis); font-size: .72rem; }
.note { display: -webkit-box; overflow: hidden; -webkit-box-orient: vertical; -webkit-line-clamp: 2; font-style: italic; color: var(--bs-secondary-color); }
.state { display: inline-flex; align-items: baseline; justify-content: flex-end; gap: .15rem; }
.del-slot :deep(.trash) { width: 1.2rem; height: 1.2rem; opacity: 0; }
.tr:hover .del-slot :deep(.trash), .del-slot:focus-within :deep(.trash) { opacity: 1; }
@media (hover: none) { .del-slot :deep(.trash) { opacity: .45; } }
.verdict { grid-column: 1 / -1; font-size: .75rem; color: var(--bs-danger-text-emphasis); }
@media (max-width: 575px) {
  .tr { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto; row-gap: .1rem; }
  .card-cell { grid-column: 1 / -1; }
}
</style>
