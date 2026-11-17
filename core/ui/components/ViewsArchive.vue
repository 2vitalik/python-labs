<script setup>
import { computed, inject } from 'vue'

import { workLine } from '../viewStats.js'
import { archiveView, removeView, store } from '../viewStore.js'
import DateChip from './DateChip.vue'
import DelButton from './DelButton.vue'
import Icon from './Icon.vue'
import IconChevron from './IconChevron.vue'
import Reveal from './Reveal.vue'
import ViewIcon from './ViewIcon.vue'

// the views put away (T315 §7), folded at the bottom of the library, the latest first: each comes back with all its
// history, or goes for good — only from here
const lib = inject('viewsLib')
const list = computed(() => store.data.views.filter((v) => v.archived_at).sort((a, b) => b.archived_at.localeCompare(a.archived_at)))
</script>

<template>
  <section class="varch">
    <button type="button" class="varch-head" :disabled="!list.length" :aria-expanded="lib.archive && !!list.length" @click="lib.archive = !lib.archive">
      <IconChevron :dir="lib.archive && list.length ? 'down' : 'right'" />
      <Icon name="archive" />
      <span>Архів</span>
      <span class="varch-n">{{ list.length || 'порожній' }}</span>
    </button>
    <Reveal :show="lib.archive && list.length > 0">
      <TransitionGroup tag="ul" name="varch" class="varch-list">
        <li v-for="v in list" :id="`view-${v.slug}`" :key="v.slug" class="varch-row">
          <ViewIcon :view="v" />
          <span class="varch-title" :title="v.title">{{ v.title }}</span>
          <span class="varch-when">прибрано <DateChip :at="v.archived_at" /></span>
          <span class="varch-work" :title="workLine(v)">{{ workLine(v) }}</span>
          <button type="button" class="iact" title="Повернути з архіву — з усією історією" @click="lib.act(() => archiveView(v.slug, false))"><Icon name="back" /></button>
          <DelButton :what="`вид «${v.title}»`" note="назавжди, з усіма версіями" title="Видалити назавжди" @yes="lib.act(() => removeView(v.slug))" />
        </li>
      </TransitionGroup>
    </Reveal>
  </section>
</template>

<style scoped>
.varch { margin-top: 1.75rem; }
.varch-head { display: inline-flex; align-items: center; gap: .35rem; padding: .1rem .3rem; border: 0; border-radius: .3rem; background: none;
              color: var(--bs-secondary-color); font-weight: 600; }
.varch-head:not(:disabled):hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
.varch-head:disabled { opacity: .7; }
.varch-n { font-weight: 400; font-size: .85rem; }
.varch-list { margin: .35rem 0 0; padding: 0; list-style: none; }
.varch-row { display: flex; align-items: center; gap: .5rem; padding: .25rem .3rem; border-bottom: 1px solid var(--bs-border-color-translucent); font-size: .88rem; }
.varch-title { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.varch-when { flex: none; font-size: .78rem; color: var(--bs-secondary-color); white-space: nowrap; }
.varch-work { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: .76rem; color: var(--bs-secondary-color); }
.varch-enter-active, .varch-leave-active { transition: opacity .2s ease; }
.varch-enter-from, .varch-leave-to { opacity: 0; }
</style>
