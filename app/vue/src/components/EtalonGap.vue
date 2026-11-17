<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { hide, isHidden } from '../advice.js'
import { getEtalon } from '../api.js'
import { games, taskIndex, zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { addsTo } from '../taskMeta.js'
import CoinBadge from './CoinBadge.vue'
import PartLabel from './PartLabel.vue'
import TaskAdd from './TaskAdd.vue'

// «в еталоні є, у тебе нема» (T280 Q7): the cards the base game's reference description claims and this game does not.
// A quiet line under «чого бракує» opens the list by category; a card has the catalog's own plus and «не про мою гру»,
// which hides it for this game as an advice is hidden (advice.js, back from «сховані поради»). The owner's, with «Еталон основи» on (T319)
const ed = useEd()
const etalon = ref(null)
const open = ref(false)
const base = computed(() => games.value.find((g) => g.slug === ed.game.base_game))
watch(() => ed.game.base_game, async (slug) => {
  etalon.value = null
  const d = slug ? await getEtalon(slug).catch(() => null) : null  // a base without a reference description answers 404
  if (slug === ed.game.base_game) etalon.value = d
}, { immediate: true })

const key = (slug) => `etalon:${slug}`
const groups = computed(() => {
  const mine = new Set(ed.claims.map((c) => c.task))
  const lacking = [...new Set((etalon.value?.claims || []).map((c) => c.task))]
    .filter((s) => !mine.has(s) && !isHidden(ed.game.id, key(s)))
    .map((s) => taskIndex.value[s]).filter((t) => t?.status === 'active')
  return Object.entries(zones.value).map(([id, z]) => ({ id, z, list: lacking.filter((t) => t.zone === id) })).filter((g) => g.list.length)
})
const count = computed(() => groups.value.reduce((n, g) => n + g.list.length, 0))
const cards = (n) => (n % 10 === 1 && n % 100 !== 11 ? 'картка' : n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 12 || n % 100 > 14) ? 'картки' : 'карток')
const wave = (t) => hide(ed.game.id, key(t.slug), `В еталоні є «${t.title}»`)
</script>

<template>
  <div v-if="count" class="small">
    <button type="button" class="quiet" :aria-expanded="open" @click="open = !open">
      в еталоні «{{ base?.title }}» є ще {{ count }} {{ cards(count) }}, яких нема в тебе <Icon :name="open ? 'down' : 'right'" />
    </button>
    <div v-if="open" class="gap mt-2">
      <div class="text-secondary mb-2">Може, це є й у твоїй грі, а ти не заявив? «＋» додає картку так само, як у каталозі; чого в грі нема — «не про мою гру».</div>
      <div v-for="g in groups" :key="g.id" class="mb-2">
        <PartLabel :icon="g.z.icon" :zone="g.id">{{ g.z.title }}</PartLabel>
        <div v-for="t in g.list" :key="t.slug" class="line">
          <TaskAdd :task="t" />
          <span v-peek="{ kind: 'task', id: t.slug }" class="name" :title="addsTo(t)">{{ t.icon }} {{ t.title }}</span>
          <CoinBadge :coin="t.coin" :amount="t.amount" />
          <button type="button" class="quiet off text-nowrap" title="сховати для цієї гри; повернути — «сховані поради» вище" @click="wave(t)">не про мою гру</button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.quiet { padding: 0; border: 0; background: none; color: var(--bs-secondary-color); text-decoration: underline dashed; text-underline-offset: .2em; }
.quiet:hover { color: var(--bs-body-color); }
.gap { padding: .5rem .6rem; border: 1px solid var(--bs-border-color); border-radius: .375rem; }
.line { display: flex; align-items: center; gap: .45rem; min-height: 1.7rem; padding: 0 .15rem; border-radius: .25rem; }
.line:hover { background: var(--bs-tertiary-bg); }
.name { min-width: 0; overflow-wrap: anywhere; }
.off { margin-left: auto; font-size: .75rem; }
</style>
