<script setup>
import { computed, ref, watch } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { deletePart } from '../api.js'
import { zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { toneOf } from '../graphTree.js'
import { target } from '../jump.js'
import { isShut, toggleCard } from '../looks.js'
import { useJumps } from '../windowJumps.js'
import '../partCard.css'
import '../windowTone.css'
import CardFold from './CardFold.vue'
import CardPicker from './CardPicker.vue'
import CardShut from './CardShut.vue'
import CardSign from './CardSign.vue'
import ClaimRow from './ClaimRow.vue'
import CoinBadge from './CoinBadge.vue'
import MenuItems from './MenuItems.vue'
import PairAdvice from './PairAdvice.vue'
import PartBlock from './PartBlock.vue'
import ShotStrip from './ShotStrip.vue'
import WindowForm from './WindowForm.vue'

// a window of the game (T270 §10.1): its type, screenshots, transitions and actions, the elements on it. Its sign is the
// map's: filled when there is a screenshot, in the colour of the window's type (T284 §1). The head is tinted and sticks
// while the card passes (partCard.css). The pencil turns the head and the top of the card into its form, framed alone
// (T291 §4, T294 §4); the elements stay under the form, each with its trash (T284 §4). Folded (T296 §7) — the head, two
// lines and what is inside
const props = defineProps({ part: Object })
const ed = useEd()
const edit = ref('')  // '' — the card; otherwise its form, and 'description' puts the cursor there (T278 §2)
const error = ref('')
const type = computed(() => ed.info(props.part.task))
const menu = computed(() => ed.menus.find((m) => m.window === props.part.id))
const claims = computed(() => ed.claimsOf(props.part.id).filter((c) => !c.auto))
const tone = computed(() => toneOf(props.part))
const jumps = useJumps()
const shut = computed(() => !edit.value && isShut(props.part.id, 'windows'))
// «show me where» a claim of this card is: a folded card opens to show it
watch(target, (id) => id && shut.value && claims.value.some((c) => `c-${c.id}` === id) && toggleCard(props.part.id, 'windows'))
const bits = computed(() => [['image', props.part.screenshots?.length, 'скриншоти'],
  ['goto', (menu.value?.items?.length || 0) + jumps.value.filter((j) => j.from === props.part.id).length, 'переходи й дії'],
  ['widgets', claims.value.length, 'елементи']])

async function remove() {
  error.value = ''
  try {
    await deletePart(props.part.id)
    ed.changed()
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div :id="'p-' + part.id" class="card pcard" :style="{ '--z': zones.interface?.color }">
    <div v-if="!edit" class="pcard-head">
      <Icon :name="part.screenshots?.length ? 'winshot' : 'win'" class="gg-w sign" :class="tone && `tone-${tone}`" />
      <div class="head flex-grow-1">
        <span class="fw-semibold">{{ part.title }}</span>
        <span v-peek="type ? { kind: 'task', id: part.task } : null" class="badge border fw-normal text-secondary wtype">
          <CardSign v-if="type" :task="type" /><span class="t">{{ type?.title || part.task }}</span><CoinBadge :coin="type?.coin" :amount="type?.amount" /></span>
      </div>
      <span class="pcard-acts">
        <CardFold :id="part.id" scope="windows" />
        <template v-if="ed.editable">
          <button type="button" class="iact" title="Редагувати" @click="edit = 'all'"><Icon name="pencil" /></button>
          <DelButton :what="`вікно «${part.title}»`" @yes="remove" />
        </template>
      </span>
    </div>
    <div v-if="shut" class="card-body"><CardShut :text="part.description" :bits @open="toggleCard(part.id, 'windows', $event)" /></div>
    <div v-else class="card-body vstack gap-2">
      <div v-if="edit" class="editing pform"><WindowForm :part :focus="edit" @done="edit = ''" @cancel="edit = ''" /></div>
      <template v-else>
        <div v-if="part.description" class="small text-secondary">{{ part.description }}</div>
        <button v-else-if="ed.editable" type="button" class="more" title="опису ще нема — додай пару слів" @click="edit = 'description'"><Icon name="plus" /> опис</button>
        <ShotStrip :part need />
      </template>
      <template v-if="!ed.simple">
        <MenuItems :window="part" :menu />
        <PartBlock v-if="claims.length || ed.editable" pic="widgets" zone="interface" title="Елементи" class="small">
          <template #after><CardPicker plus :kinds="['element']" :anchor="{ part: part.id }" label="елемент" /></template>
          <div v-if="claims.length" class="vstack gap-1">
            <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
          </div>
        </PartBlock>
        <PairAdvice v-if="!edit" :part />
      </template>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.sign { color: var(--w-ink); font-size: 1.1rem; }
/* the title and the type wrap inside their own block, so the pencil and the trash stay in the card on a phone */
.head { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .5rem; min-width: 0; overflow-wrap: anywhere; }
/* the window's type: its sign, name and coin on one line — a long name ends in «…», the card under the mouse has it whole;
   on the head's own tint, framed by the head's line */
.wtype { display: inline-flex; align-items: center; gap: .3rem; max-width: 100%; border-color: color-mix(in srgb, var(--z) 35%, var(--bs-border-color)) !important; }
.wtype .t { min-width: 0; overflow: hidden; text-overflow: ellipsis; }
</style>
