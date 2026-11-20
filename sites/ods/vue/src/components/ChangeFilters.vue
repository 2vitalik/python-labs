<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { pages } from '@core/guide.js'
import { vHint } from '@core/hint.js'

import { busy, lookAuto, PRESETS, presetOn, presetQuery, ROWS, tally, toggled, valueOf } from '../lectureChangeFilter.js'
import { GROUPS, KINDS, ORIGINS, SEVS, SIZES, STATUSES, WHERES } from '../lectureChanges.js'
import { shortTitle } from '../lectures.js'
import ChangePills from './ChangePills.vue'

// the filters in rows, each with its word: ready sets, then a pill per value that is in the catalogue at all; «Тип» —
// the kinds of the groups chosen (all of them at once are seven lines). The words looked for go to the address a moment
// after the typing stops
const props = defineProps({ items: Array, f: Object, query: Object })
const emit = defineEmits(['set'])
const has = computed(() => Object.fromEntries(ROWS.map((k) => [k, new Set(props.items.map((it) => valueOf(it, k)))])))
const n = computed(() => Object.fromEntries(ROWS.map((k) => [k, tally(props.items, props.f, k)])))
const slugs = computed(() => Object.fromEntries(props.items.map((it) => [it.lec, it.slug])))
const autos = computed(() => props.items.filter(lookAuto).length)
const lookOn = computed(() => props.f.group.includes('look'))
const words = (dict, key, more = () => ({})) => Object.keys(dict).filter((v) => has.value[key].has(v))
  .map((v) => ({ v, text: dict[v][0], hint: dict[v][1], n: n.value[key][v], ...more(v) }))
const rows = computed(() => {
  const g = props.f.group
  const kinds = Object.keys(KINDS).filter((k) => has.value.kind.has(k) && (g.includes(KINDS[k][1]) || props.f.kind.includes(k)))
  return [
    ['lec', 'Лекція', [...has.value.lec].sort((a, b) => a - b)
      .map((l) => ({ v: l, text: l, hint: shortTitle(pages.value[slugs.value[l]]?.title || ''), n: n.value.lec[l] }))],
    ['group', 'Група', words(GROUPS, 'group', (v) => ({ color: v }))],
    ['kind', 'Тип', kinds.map((k) => ({ v: k, text: KINDS[k][0], color: KINDS[k][1], n: n.value.kind[k] }))],
    ['sev', 'Критичність', words(SEVS, 'sev', (v) => ({ sev: v })).reverse()],
    ['status', 'Стан', words(STATUSES, 'status')],
    ['where', 'Де', words(WHERES, 'where', (v) => ({ icon: WHERES[v][1], hint: undefined }))],
    ['origin', 'Звідки', words(ORIGINS, 'origin')],
    ['size', 'Розмір', words(SIZES, 'size')],
  ]
})
const reset = () => emit('set', Object.fromEntries([...ROWS, 'q', 'auto', 'for'].map((k) => [k, undefined])))

const text = ref(props.query.q || '')
let timer
watch(text, (v) => {
  clearTimeout(timer)
  timer = setTimeout(() => emit('set', { q: v.trim() || undefined }), 250)
})
watch(() => props.query.q, (v) => (v || '') !== text.value.trim() && (text.value = v || ''))
</script>

<template>
  <div class="chg-filters">
    <div class="frow">
      <span class="flabel">Набори</span>
      <div class="fpills">
        <button v-for="(p, k) in PRESETS" :key="k" v-hint="p.hint" type="button" class="btn btn-sm chip"
                :class="presetOn(query, k) ? 'btn-secondary' : 'btn-outline-secondary'" :aria-pressed="presetOn(query, k)"
                @click="emit('set', presetQuery(k, presetOn(query, k)))">{{ p.word }}</button>
        <button v-if="busy(query)" type="button" class="dot small ms-1" @click="reset">скинути все</button>
      </div>
    </div>
    <ChangePills v-for="[key, label, pills] in rows" :key :label :pills :on="f[key]" @pick="emit('set', toggled(f, key, $event))">
      <button v-if="key === 'group' && autos" v-hint="lookOn ? 'оформлення вибрано — автоматичні записи вже видно' : 'автоматичні записи оформлення — їх багато, тому типово сховані'"
              type="button" class="btn btn-sm chip" :class="[f.auto ? 'btn-secondary' : 'btn-outline-secondary', { zero: lookOn }]"
              :aria-pressed="f.auto" @click="emit('set', { auto: f.auto ? undefined : '1' })">
        з оформленням<span class="n">{{ autos }}</span></button>
      <span v-if="key === 'kind' && !f.group.length" class="quiet fnote">типи зʼявляться, коли вибереш групу</span>
    </ChangePills>
    <div class="frow">
      <label class="flabel" for="chg-q">Шукати</label>
      <div class="fsearch">
        <Icon name="search" />
        <input id="chg-q" v-model="text" type="search" class="form-control form-control-sm" placeholder="слова правки, заголовка, пояснення…"
               autocomplete="off" @keydown.esc="text = ''">
      </div>
    </div>
  </div>
</template>
