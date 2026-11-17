<script setup>
import { computed } from 'vue'

import Tip from '@core/components/Tip.vue'
import { useEd } from '../ed.js'
import { GROUPS } from '../videos.js'
import VideoRow from './VideoRow.vue'

// the videos every game is asked for (T318), on top of «Супровід»: rows that are there already — nobody adds them as
// cards. By who needs them: demos — everyone, by a lab's deadline; async defenses — from 70; a row per gold card — from 85.
// The same table of links as the section's cards (SubzoneRows, `table`); without them (T319) the section is these rows alone
const ed = useEd()
const groups = computed(() => GROUPS.map((g) => ({ ...g, list: ed.videos.filter((v) => v.kind === g.kind) })).filter((g) => g.list.length))
</script>

<template>
  <div class="videos" :class="{ judge: ed.judge }" :data-dock="ed.has('support') ? '' : null">
    <div v-if="ed.has('support')" class="cap"><span class="fw-semibold">Відео</span> <span class="muted">— ці рядки є в кожній грі, картки додавати не треба</span><span class="tip-dock" /></div>
    <Tip v-if="ed.editable" id="videos-how" class="mb-1">Встав посилання на відео: YouTube («доступ за посиланням»), Google Drive (відкрий доступ усім, хто має посилання) чи Loom.
      Перезаписав — дай нове посилання кнопкою «оновити»: попередні версії лишаються, а «вчасно» рахується за першим.</Tip>
    <div class="thead"><span>відео</span><span>посилання</span><span>нотатка</span></div>
    <div v-for="g in groups" :key="g.kind" class="vstack noflash">
      <div class="sub" :title="g.hint">{{ g.icon }} {{ g.title }} <span class="who">{{ g.who }}</span></div>
      <VideoRow v-for="v in g.list" :key="v.slot" :v />
    </div>
  </div>
</template>

<style scoped>
/* the columns of the section's own table of links (SubzoneRows .links), so the two read as one */
.videos { --cols: minmax(0, 2fr) minmax(0, 1.4fr) minmax(0, 1.4fr) 3rem; max-width: 62rem; }
.videos.judge { --cols: minmax(0, 2fr) minmax(0, 1.4fr) minmax(0, 1fr) 9rem; }  /* the teacher's «треба · не треба» in the last column */
.cap { display: flex; flex-wrap: wrap; align-items: center; gap: .1rem .4rem; margin-bottom: .3rem; font-size: .85rem; }
.muted { font-size: .76rem; color: var(--bs-secondary-color); }
.thead { display: grid; grid-template-columns: var(--cols); column-gap: .6rem; padding: 0 .45rem; border-bottom: 1px solid var(--bs-border-color);
         font-size: .7rem; color: var(--bs-secondary-color); }
.sub { margin-top: .5rem; padding-bottom: .1rem; border-bottom: 1px solid var(--bs-border-color-translucent); font-size: .8rem; font-weight: 600; color: var(--bs-secondary-color); }
.who { margin-left: .3rem; font-size: .72rem; font-weight: 400; }
@media (max-width: 575px) { .thead { display: none; } }
</style>
