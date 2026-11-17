<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import Pop from '@core/components/Pop.vue'
import { fmtWhen } from '@core/labs.js'
import { judgeVideo, putVideo } from '../api.js'
import { useEd } from '../ed.js'
import { shortLink } from '../shortLink.js'
import { anchorOf, tagOf, titleOf } from '../videos.js'
import CoinBadge from './CoinBadge.vue'
import VideoWord from './VideoWord.vue'

// a video of «Супровід» (T318) as a row of the links' table: what it is and by when · the link — the last version, when it
// came, how many there were · a note · the teacher's word. The owner pastes the link right in its cell: another link is a
// new version, the earlier ones stay under «версій: N». The teacher marks «треба» / «не треба» in one click and opens the
// rest — why, accepted, returned — by a click on the row. Its columns are the table's (`--cols`, VideoSlots)
const props = defineProps({ v: Object })
const ed = useEd()
const last = computed(() => props.v.versions.at(-1))
const card = computed(() => (props.v.kind === 'gold' ? ed.info(props.v.task) : null))
const tag = computed(() => tagOf(props.v))
const can = computed(() => ed.editable && !ed.sandbox)
const olds = ref(false)
const word = ref(false)
const field = ref()
const fail = (e) => ed.fail(e.message)
const put = (patch) => putVideo(props.v.slot, { link: last.value?.link || '', note: last.value?.note || '', ...patch }).then(() => ed.changed())
const need = (k) => judgeVideo(ed.nick, props.v.slot, { need: props.v.need === k ? '' : k }).then(() => ed.changed(), fail)
// «оновити»: the field opens with the old link selected — paste over it
async function renew() {
  await field.value.edit()
  document.activeElement?.select?.()
}
</script>

<template>
  <div :id="anchorOf(v)">
    <Pop v-model="word" block width="24rem">
      <template #trigger="{ toggle }">
        <div class="tr" :class="[v.status, { skip: v.need === 'skip', judge: ed.judge }]" :role="ed.judge ? 'button' : null"
             :title="ed.judge ? 'Клік — слово викладача: чи потрібне, зараховано, повернуто' : null" @click="ed.judge && toggle()">
          <span class="what">
            <span><CoinBadge v-if="card" :coin="card.coin" :amount="card.amount" /> {{ titleOf(v, ed.info) }}</span>
            <span v-if="tag" class="tag" :class="tag.tone" :title="tag.tip">{{ tag.text }}</span>
          </span>
          <span class="link-cell">
            <InlineText v-if="can" ref="field" :value="last?.link || ''" can required placeholder="посилання: YouTube, Google Drive, Loom" :save="(link) => put({ link, note: '' })">
              <a :href="last.link" target="_blank" rel="noopener" :title="last.link" @click.stop>{{ shortLink(last.link) }}</a>
              <template #empty><span class="add" title="Встав посилання на відео"><Icon name="plus" /> посилання</span></template>
            </InlineText>
            <a v-else-if="last" :href="last.link" target="_blank" rel="noopener" :title="last.link" @click.stop>{{ shortLink(last.link) }}</a>
            <span v-else class="muted">—</span>
            <span v-if="last" class="meta" @click.stop>
              <span :title="`останнє посилання — ${fmtWhen(last.at)}`">{{ fmtWhen(last.at, true) }}</span>
              <button v-if="v.versions.length > 1" type="button" class="more-field" :title="olds ? 'сховати попередні версії' : 'показати всі версії'" @click="olds = !olds">версій: {{ v.versions.length }}</button>
              <button v-if="can" type="button" class="more-field" title="Нове посилання стане новою версією — попередні лишаться" @click="renew">оновити</button>
            </span>
          </span>
          <InlineText v-if="can && last" :value="last.note" can block class="note" placeholder="що у відео, таймкоди" :save="(note) => put({ note })">
            <template #empty><span class="nadd">＋ нотатка</span></template>
          </InlineText>
          <span v-else class="note" :title="last?.note">{{ last?.note }}</span>
          <span class="state">
            <span v-if="ed.judge" class="needs" @click.stop>
              <button type="button" :class="{ on: v.need === 'must' }" title="Від цього студента відео обовʼязкове" @click="need('must')">треба</button>
              <button type="button" :class="{ on: v.need === 'skip' }" title="Від цього студента не потрібне — наприклад, показав на онлайн-захисті" @click="need('skip')">не треба</button>
            </span>
            <span v-if="v.status === 'accepted'" class="text-success" title="зараховано"><Icon name="done" /></span>
            <span v-else-if="v.status === 'returned'" class="text-danger" title="повернуто — доробити"><Icon name="back" /></span>
          </span>
          <div v-if="v.need && v.why" class="line">викладач: {{ v.why }}</div>
          <div v-if="v.status === 'returned' && v.verdict" class="line bad">{{ v.verdict }}</div>
          <div v-else-if="v.verdict" class="line">{{ v.verdict }}</div>
          <ol v-if="olds" class="olds" @click.stop>
            <li v-for="(x, i) in v.versions" :key="i">
              <span class="old">
                <span class="muted">{{ fmtWhen(x.at) }}</span>
                <a :href="x.link" target="_blank" rel="noopener" :title="x.link">{{ shortLink(x.link, 48) }}</a>
                <span v-if="x.note" class="muted">— {{ x.note }}</span>
                <span v-if="i === v.versions.length - 1" class="muted">· поточна</span>
              </span>
            </li>
          </ol>
        </div>
      </template>
      <VideoWord v-if="ed.judge" :v @close="word = false" />
    </Pop>
  </div>
</template>

<style scoped>
/* a row of the links' table (ClaimLinkRow): the same columns, grounds and sizes */
.tr { display: grid; grid-template-columns: var(--cols); column-gap: .6rem; align-items: baseline; padding: .25rem .45rem;
      border-bottom: 1px solid var(--bs-border-color-translucent); font-size: .82rem; }
.tr.judge:hover { background-image: linear-gradient(rgb(127 127 127 / .07), rgb(127 127 127 / .07)); }
.tr.accepted { background-color: color-mix(in srgb, var(--bs-success) 9%, transparent); }
.tr.returned { background-color: color-mix(in srgb, var(--bs-danger) 9%, transparent); }
.tr.skip > .what > :first-child, .tr.skip > .link-cell { opacity: .55; }
.what { display: flex; flex-wrap: wrap; align-items: baseline; gap: .1rem .5rem; min-width: 0; overflow-wrap: anywhere; }
.tag { font-size: .72rem; color: var(--bs-secondary-color); white-space: nowrap; }
.tag.bad { padding: 0 .3rem; border-radius: .25rem; background: var(--bs-danger-bg-subtle); color: var(--bs-danger-text-emphasis); }
.tag.ok { color: var(--bs-success); }
.tag.late { color: var(--bs-warning-text-emphasis); }
.tag.off { font-style: italic; }
.needs { display: inline-flex; gap: .3rem; }
.needs button { padding: 0 .3rem; border: 1px dashed var(--bs-border-color); border-radius: .25rem; background: none; color: var(--bs-secondary-color); font-size: .7rem; white-space: nowrap; }
.needs button:hover { border-color: var(--bs-secondary-color); color: var(--bs-body-color); }
.needs button.on { border-style: solid; border-color: var(--bs-secondary-color); background: var(--bs-secondary-bg); color: var(--bs-body-color); }
.link-cell { display: flex; flex-wrap: wrap; align-items: baseline; gap: 0 .5rem; min-width: 0; overflow-wrap: anywhere; }
.link-cell a { display: inline-block; max-width: 100%; overflow: hidden; vertical-align: top; text-decoration: none; text-overflow: ellipsis; white-space: nowrap; }
.link-cell a:hover { text-decoration: underline; }
.meta { display: inline-flex; flex-wrap: wrap; align-items: baseline; gap: 0 .5rem; font-size: .72rem; color: var(--bs-secondary-color); }
.muted { color: var(--bs-secondary-color); }
.add { color: var(--act-add); white-space: nowrap; }
.add:hover { text-decoration: underline; }
.note { display: -webkit-box; min-width: 0; overflow: hidden; -webkit-box-orient: vertical; -webkit-line-clamp: 2; font-style: italic; color: var(--bs-secondary-color); overflow-wrap: anywhere; }
.note.open { display: block; overflow: visible; }
.nadd { color: var(--act-add); opacity: 0; }
.tr:hover .nadd, .inl:focus-visible .nadd { opacity: .75; }
.state { display: inline-flex; align-self: center; align-items: center; justify-content: flex-end; gap: .4rem; }
.line { grid-column: 1 / -1; font-size: .75rem; color: var(--bs-secondary-color); }
.line.bad { color: var(--bs-danger-text-emphasis); }
.olds { grid-column: 1 / -1; margin: .2rem 0 .1rem; padding-left: 1.4rem; font-size: .76rem; }
.old { display: inline-flex; flex-wrap: wrap; gap: 0 .45rem; vertical-align: top; overflow-wrap: anywhere; }
.old a { text-decoration: none; }
.old a:hover { text-decoration: underline; }
@media (max-width: 575px) {
  .tr { grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) auto; row-gap: .1rem; }
  .what { grid-column: 1 / -1; }
}
</style>
