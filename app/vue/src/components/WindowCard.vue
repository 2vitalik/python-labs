<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deletePart } from '../api.js'
import { useEd } from '../ed.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import CoinBadge from './CoinBadge.vue'
import MenuItems from './MenuItems.vue'
import PairAdvice from './PairAdvice.vue'
import PartLabel from './PartLabel.vue'
import ShotStrip from './ShotStrip.vue'
import WindowForm from './WindowForm.vue'

// a window of the game (T270 §10.1): its type, screenshots, transitions and actions, the elements on it; the pencil turns
// the card into its form
const props = defineProps({ part: Object })
const ed = useEd()
const edit = ref('')  // '' — the card; otherwise its form, and 'description' puts the cursor there (T278 §2)
const error = ref('')
const type = computed(() => ed.info(props.part.task))
const menu = computed(() => ed.menus.find((m) => m.window === props.part.id))
const claims = computed(() => ed.claimsOf(props.part.id).filter((c) => !c.auto))

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
          <span>🪟</span>
          <div class="head flex-grow-1">
            <span class="fw-semibold">{{ part.title }}</span>
            <span class="badge border fw-normal text-secondary bg-body-tertiary text-wrap text-start" :title="type?.description">
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
        <template v-if="!ed.simple">
          <MenuItems :window="part" :menu />
          <div v-if="claims.length || ed.editable" class="small vstack gap-1">
            <PartLabel icon="🧩" zone="interface">Елементи</PartLabel>
            <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
            <div v-if="ed.editable"><CardPicker :kinds="['element']" :anchor="{ part: part.id }" label="елемент" /></div>
          </div>
          <PairAdvice :part />
        </template>
        <div v-if="error" class="text-danger small">{{ error }}</div>
      </template>
    </div>
  </div>
</template>

<style scoped>
/* the title and the type wrap inside their own block, so the pencil and the trash stay in the card on a phone */
.head { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .5rem; min-width: 0; overflow-wrap: anywhere; }
/* no description yet: an invitation in the colour of adding, framed as the screenshot's «＋» tile (T278 §2) */
.more { display: flex; align-items: center; gap: .3rem; padding: .2rem .55rem; border: 1.5px dashed color-mix(in srgb, var(--act-add) 55%, transparent);
        border-radius: .375rem; background: none; color: var(--act-add); font-size: .8rem; text-align: start; }
.more:hover { border-color: var(--act-add); background: color-mix(in srgb, var(--act-add) 8%, transparent); }
</style>
