<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { showShot } from '@core/lightbox.js'
import { close, vPeek } from '@core/peek.js'
import { useEd } from '../ed.js'
import { toneOf } from '../graphTree.js'
import { jump } from '../jump.js'
import { useJumps } from '../windowJumps.js'
import '../windowTone.css'
import CardSign from './CardSign.vue'
import PartLabel from './PartLabel.vue'

// a window's card under the mouse (T284 §2): its screenshot, description, where it leads and what is on it; every
// mention inside is a way on — to another window, a rule, a catalog card
const props = defineProps({ id: String })
const ed = useEd()
const win = computed(() => ed.windows.find((w) => w.id === props.id))
const type = computed(() => ed.info(win.value?.task))
const shots = computed(() => (win.value?.screenshots || []).map((s) => `/api/uploads/${win.value.game}/${s}`))
const items = computed(() => ed.menus.find((m) => m.window === props.id)?.items || [])
const all = useJumps()
const jumps = computed(() => all.value.filter((j) => j.from === props.id))
const claims = computed(() => ed.claimsOf(props.id).filter((c) => !c.auto))
const title = (id) => ed.windows.find((w) => w.id === id)?.title
// a window named here wears its sign and its type's colour, as on the map (T296 §12)
const winOf = (id) => ed.windows.find((w) => w.id === id)
const sign = (id) => (winOf(id)?.screenshots?.length ? 'winshot' : 'win')
const tone = (id) => (toneOf(winOf(id)) ? `tone-${toneOf(winOf(id))}` : '')
const card = (slug) => ed.info(slug)?.title || slug
const show = () => { close(); jump(`p-${props.id}`) }
</script>

<template>
  <div v-if="win" class="vstack gap-2">
    <div class="pk-head">
      <Icon :name="shots.length ? 'winshot' : 'win'" class="gg-w sign" :class="toneOf(win) && `tone-${toneOf(win)}`" />
      <span class="fw-semibold">{{ win.title }}</span>
      <span v-if="type" v-peek="{ kind: 'task', id: win.task }" class="pk-type">{{ type.title }}</span>
    </div>
    <img v-if="shots.length" :src="shots[0]" alt="скриншот" class="rounded border pk-shot" title="на весь екран" @click.stop="showShot(shots, 0)">
    <div v-if="win.description">{{ win.description }}</div>
    <div v-else class="text-secondary">Опису ще нема.</div>
    <div v-if="items.length || jumps.length">
      <PartLabel pic="goto" zone="interface">Переходи й дії</PartLabel>
      <div v-for="(it, i) in items" :key="i" class="pk-row">
        <span :class="{ 'text-secondary fst-italic': !it.title }">{{ it.title || 'як?' }}</span>
        <span v-if="title(it.window)">→ <Icon :name="sign(it.window)" class="gg-w" :class="tone(it.window)" /> <span v-peek="{ kind: 'window', id: it.window }">{{ title(it.window) }}</span></span>
        <span v-else-if="it.task">→ <CardSign :task="ed.info(it.task)" /> <span v-peek="{ kind: 'task', id: it.task }">{{ card(it.task) }}</span></span>
        <span v-if="it.note" class="text-secondary">· {{ it.note }}</span>
      </div>
      <div v-for="j in jumps" :key="j.rule + j.to" class="pk-row">
        <span v-peek="{ kind: 'rule', id: j.rule }" class="by-rule"><Icon name="bolt" /> {{ j.title }}</span>
        <span>→ <Icon :name="sign(j.to)" class="gg-w" :class="tone(j.to)" /> <span v-peek="{ kind: 'window', id: j.to }">{{ title(j.to) }}</span></span>
      </div>
    </div>
    <div v-if="claims.length">
      <PartLabel pic="widgets" zone="interface">Елементи</PartLabel>
      <div v-for="c in claims" :key="c.id" class="pk-row"><span><CardSign :task="ed.info(c.task)" /> <span v-peek="{ kind: 'task', id: c.task }">{{ card(c.task) }}</span></span></div>
    </div>
    <button type="button" class="pk-go" @click.stop="show">до вікна на сторінці <Icon name="arrow" /></button>
  </div>
</template>

<style scoped>
.sign, .pk-row .gg-w { color: var(--w-ink); }
.by-rule { color: color-mix(in srgb, #8e24aa 78%, var(--bs-body-color)); }
</style>
