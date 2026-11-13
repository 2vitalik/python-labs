<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { deletePart } from '../api.js'
import { useEd } from '../ed.js'
import { toneOf } from '../graphTree.js'
import '../windowTone.css'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import CoinBadge from './CoinBadge.vue'
import MenuItems from './MenuItems.vue'
import PairAdvice from './PairAdvice.vue'
import PartBlock from './PartBlock.vue'
import ShotStrip from './ShotStrip.vue'
import WindowForm from './WindowForm.vue'

// a window of the game (T270 §10.1): its type, screenshots, transitions and actions, the elements on it. Its sign is the
// map's: filled when there is a screenshot, in the colour of the window's type (T284 §1). The pencil turns the top of the
// card into its form; the elements stay under the form, each with its trash (T284 §4)
const props = defineProps({ part: Object })
const ed = useEd()
const edit = ref('')  // '' — the card; otherwise its form, and 'description' puts the cursor there (T278 §2)
const error = ref('')
const type = computed(() => ed.info(props.part.task))
const menu = computed(() => ed.menus.find((m) => m.window === props.part.id))
const claims = computed(() => ed.claimsOf(props.part.id).filter((c) => !c.auto))
const tone = computed(() => toneOf(props.part))

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
  <div :id="'p-' + part.id" class="card">
    <div class="card-body p-2 vstack gap-2">
      <WindowForm v-if="edit" :part :focus="edit" @done="edit = ''" @cancel="edit = ''" />
      <template v-else>
        <div class="d-flex align-items-start gap-2">
          <Icon :name="part.screenshots?.length ? 'winshot' : 'win'" class="gg-w sign" :class="tone && `tone-${tone}`" />
          <div class="head flex-grow-1">
            <span class="fw-semibold">{{ part.title }}</span>
            <span v-peek="type ? { kind: 'task', id: part.task } : null" class="badge border fw-normal text-secondary bg-body-tertiary text-wrap text-start">
              <CoinBadge :coin="type?.coin" :amount="type?.amount" /> {{ type?.title || part.task }}</span>
          </div>
          <template v-if="ed.editable">
            <button type="button" class="iact" title="Редагувати" @click="edit = 'all'"><Icon name="pencil" /></button>
            <DelButton :what="`вікно «${part.title}»`" @yes="remove" />
          </template>
        </div>
        <div v-if="part.description" class="small text-secondary">{{ part.description }}</div>
        <button v-else-if="ed.editable" type="button" class="more" @click="edit = 'description'"><Icon name="plus" /> опис</button>
        <ShotStrip :part />
      </template>
      <template v-if="!ed.simple">
        <MenuItems :window="part" :menu />
        <PartBlock v-if="claims.length || ed.editable" icon="🧩" zone="interface" title="Елементи" class="small">
          <div class="vstack gap-1">
            <ClaimRow v-for="c in claims" :key="c.id" :claim="c" :tools="!!edit" />
            <div v-if="ed.editable"><CardPicker :kinds="['element']" :anchor="{ part: part.id }" label="елемент" /></div>
          </div>
        </PartBlock>
        <PairAdvice v-if="!edit" :part />
      </template>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.sign { margin-top: .2rem; color: var(--w-ink); font-size: 1.1rem; }
/* the title and the type wrap inside their own block, so the pencil and the trash stay in the card on a phone */
.head { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .5rem; min-width: 0; overflow-wrap: anywhere; }
/* no description yet: an invitation in the colour of adding, framed as the screenshot's «＋» tile (T278 §2) */
.more { display: flex; align-items: center; gap: .3rem; padding: .2rem .55rem; border: 1.5px dashed color-mix(in srgb, var(--act-add) 55%, transparent);
        border-radius: .375rem; background: none; color: var(--act-add); font-size: .8rem; text-align: start; }
.more:hover { border-color: var(--act-add); background: color-mix(in srgb, var(--act-add) 8%, transparent); }
</style>
