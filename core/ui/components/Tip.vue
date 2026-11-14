<script setup>
import { computed } from 'vue'

import { isOff, setOff } from '../tips.js'
import Icon from './Icon.vue'

// an explanation — the same look wherever one is needed (T291 §5): small grey text behind «ⓘ» in a dashed frame.
// With `id` the reader can put it away: the icon stays and brings it back; the choice holds for every place that shows
// this id. <Tip id="rule-when">КОЛИ — що запускає правило…</Tip>
const props = defineProps({ id: String })
const off = computed(() => !!props.id && isOff(props.id))
</script>

<template>
  <button v-if="off" type="button" class="tipbox-ico" title="показати пояснення" @click.stop="setOff(id, false)"><Icon name="info" /></button>
  <div v-else class="tipbox">
    <Icon name="info" class="tipbox-i" />
    <div class="tipbox-body"><slot /></div>
    <button v-if="id" type="button" class="tipbox-x" title="сховати пояснення — значок лишиться, клік по ньому поверне" @click.stop="setOff(id, true)"><Icon name="x" /></button>
  </div>
</template>

<!-- not scoped: a host styles the box through its own classes; the names are the component's own (a plain `.tip` is
     taken by several pages) -->
<style>
.tipbox { display: flex; align-items: flex-start; gap: .35rem; padding: .2rem .25rem .2rem .4rem; border: 1px dashed var(--bs-info-border-subtle); border-radius: .3rem;
          background: color-mix(in srgb, var(--bs-info-bg-subtle) 45%, transparent); color: var(--bs-secondary-color); font-size: .76rem; font-weight: 400; line-height: 1.3; text-align: start; }
.tipbox-i { margin-top: .1rem; color: var(--bs-info-text-emphasis); opacity: .8; }
.tipbox-body { flex: 1 1 0; min-width: 0; }
.tipbox-body > :last-child { margin-bottom: 0; }
.tipbox-x, .tipbox-ico { display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0; padding: 0; border: 0; border-radius: .25rem; background: none; }
.tipbox-x { width: 1.05rem; height: 1.05rem; color: var(--bs-secondary-color); font-size: .7rem; opacity: .45; }
.tipbox-x:hover { background: var(--bs-tertiary-bg); opacity: 1; }
.tipbox-ico { width: 1.25rem; height: 1.25rem; color: var(--bs-info-text-emphasis); font-size: .85rem; opacity: .7; }
.tipbox-ico:hover { background: color-mix(in srgb, var(--bs-info-bg-subtle) 70%, transparent); opacity: 1; }
</style>
