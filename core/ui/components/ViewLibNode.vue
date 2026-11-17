<script setup>
import { computed, inject, ref } from 'vue'

import { plural } from '../plural.js'
import { workLine, worked } from '../viewStats.js'
import Icon from './Icon.vue'
import IconChevron from './IconChevron.vue'
import Reveal from './Reveal.vue'
import ViewIcon from './ViewIcon.vue'
import ViewLibFlag from './ViewLibFlag.vue'
import ViewVersions from './ViewVersions.vue'

// one view in the origin tree (T315 §8): icon, name, ⭐, how many versions, a word on its use; the name or the versions
// open them under it. Its children hang below on a thin line. While views are picked (`keep`) a view that is only the way
// to a picked one stands paler, and the rest fold into «… N проміжні»; `all` — that fold was opened: everything below shows
const props = defineProps({ view: { type: Object, required: true }, branch: { type: Function, required: true }, keep: Function, only: Boolean, all: Boolean })
const lib = inject('viewsLib')
const more = ref(false)
const b = computed(() => props.branch(props.view.slug, props.all || more.value))
const way = computed(() => !!props.keep && !props.all && !props.keep(props.view))
const times = (n) => `${n} ${plural(n, 'раз', 'рази', 'разів')}`
const use = computed(() => (props.view.uses ? `працював ${times(props.view.uses)}` : props.view.opens ? `відкривав ${times(props.view.opens)}` : 'не відкривав'))
const open = computed(() => !!lib.hist[props.view.slug])
const toggle = () => (lib.hist[props.view.slug] = !open.value)
const picked = () => lib.picks.includes(props.view.slug)
</script>

<template>
  <li :id="`view-${view.slug}`" class="vnode">
    <div class="vnode-line" :class="{ way }">
      <button type="button" class="iact mini" :aria-expanded="open" :title="open ? 'Згорнути версії' : 'Версії'" @click="toggle"><IconChevron :dir="open ? 'down' : 'right'" :size="12" /></button>
      <ViewIcon :view />
      <button type="button" class="vnode-name" :title="view.about || view.title" @click="toggle">{{ view.title }}</button>
      <ViewLibFlag :view field="etalon" />
      <button type="button" class="vnode-vers" @click="toggle">{{ view.version }} {{ plural(view.version, 'версія', 'версії', 'версій') }}</button>
      <span class="vnode-use" :class="{ worked: worked(view) }" :title="workLine(view)">{{ use }}</span>
      <span class="vnode-acts">
        <RouterLink :to="`/table?view=${view.slug}`" class="iact" title="Відкрити в таблиці"><Icon name="open" /></RouterLink>
        <button type="button" class="iact" :class="{ lit: picked() }" :aria-pressed="picked()" title="Порівняти — відміть два види чи версії"
                @click="lib.pick(view.slug)"><Icon name="compare" /></button>
      </span>
    </div>
    <Reveal :show="open"><ViewVersions :view :only class="vnode-versions" /></Reveal>
    <ul v-if="b.shown.length || b.hidden" class="vnode-kids">
      <ViewLibNode v-for="k in b.shown" :key="k.slug" :view="k" :branch :keep :only :all="all || more" />
      <li v-if="b.hidden" class="vnode-more">
        <button type="button" class="more-field" @click="more = true">… {{ b.hidden }} {{ plural(b.hidden, 'проміжний', 'проміжні', 'проміжних') }}</button>
      </li>
    </ul>
  </li>
</template>

<style scoped>
.vnode-line { display: flex; align-items: center; gap: .35rem; min-width: 0; padding: .12rem .25rem; border-radius: .3rem; }
.vnode-line:hover { background: color-mix(in srgb, var(--bs-tertiary-bg) 70%, transparent); }
.vnode-line.way { opacity: .55; }
.vnode-name { min-width: 0; padding: 0; border: 0; background: none; color: inherit; font-weight: 600; text-align: start;
              overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.vnode-vers { flex: none; padding: 0; border: 0; background: none; color: var(--bs-secondary-color); font-size: .78rem; white-space: nowrap; }
.vnode-vers:hover { color: var(--bs-body-color); text-decoration: underline dashed; text-underline-offset: .2em; }
.vnode-use { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: .76rem; color: var(--bs-secondary-color); opacity: .8; }
.vnode-use.worked { color: var(--bs-body-color); opacity: 1; }
.vnode-use::before { content: '·'; margin-right: .35rem; color: var(--bs-secondary-color); }
.vnode-acts { display: flex; flex: none; margin-left: auto; opacity: .6; }
.vnode-line:hover .vnode-acts, .vnode-acts:focus-within { opacity: 1; }
.iact.lit { background: var(--bs-tertiary-bg); color: var(--bs-primary); }
.vnode-versions { margin: .15rem 0 .35rem 1.9rem; }
/* the children on a thin line down from their parent */
.vnode-kids { margin: 0 0 0 .78rem; padding: 0 0 0 .9rem; border-left: 1px solid var(--bs-border-color); list-style: none; }
.vnode-more { padding: .15rem .25rem; }
</style>
