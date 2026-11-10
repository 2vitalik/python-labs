<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deletePart, postClaim } from '../api.js'
import { PAIRS } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import CoinBadge from './CoinBadge.vue'
import MenuItems from './MenuItems.vue'
import ShotStrip from './ShotStrip.vue'
import WindowForm from './WindowForm.vue'

// a window of the game (T270 §10.1): its type, screenshots, menu and the elements on it; the pencil turns the card into its form
const props = defineProps({ part: Object })
const ed = useEd()
const edit = ref(false)
const error = ref('')
const type = computed(() => ed.info(props.part.task))
const menu = computed(() => ed.menus.find((m) => m.window === props.part.id))
const claims = computed(() => ed.claimsOf(props.part.id).filter((c) => !c.auto))
// an element implies a function of the whole game (a volume slider → the volume really changes): offer it once
const pairs = computed(() => claims.value.filter((c) => PAIRS[c.task] && !ed.claims.some((x) => x.task === PAIRS[c.task]))
  .map((c) => ({ slug: PAIRS[c.task], element: ed.info(c.task)?.title || c.task, fn: ed.info(PAIRS[c.task])?.title || PAIRS[c.task] })))

async function run(fn) {
  error.value = ''
  try {
    const out = await fn()
    ed.changed()
    return out
  } catch (e) {
    error.value = e.message
  }
}
const remove = () => run(() => deletePart(props.part.id))
async function addPair(slug) {
  const c = await run(() => postClaim({ task: slug, params: {} }))
  if (c) jump(`c-${c.id}`)
}
</script>

<template>
  <div :id="'p-' + part.id" class="card">
    <div class="card-body p-2 vstack gap-2">
      <WindowForm v-if="edit" :part @done="edit = false" @cancel="edit = false" />
      <template v-else>
        <div class="d-flex align-items-start gap-2">
          <span>🪟</span>
          <div class="head flex-grow-1">
            <span class="fw-semibold">{{ part.title }}</span>
            <span class="badge border fw-normal text-secondary bg-body-tertiary text-wrap text-start">
              <CoinBadge :coin="type?.coin" :amount="type?.amount" /> {{ type?.title || part.task }}</span>
          </div>
          <template v-if="ed.editable">
            <button type="button" class="iact" title="Редагувати" @click="edit = true"><Icon name="pencil" /></button>
            <DelButton :what="`вікно «${part.title}»`" @yes="remove" />
          </template>
        </div>
        <div v-if="part.description" class="small text-secondary">{{ part.description }}</div>
        <ShotStrip :part />
        <template v-if="!ed.simple">
          <MenuItems :window="part" :menu />
          <div v-if="claims.length || ed.editable" class="small vstack gap-1">
            <div class="text-secondary fw-semibold">Елементи</div>
            <ClaimRow v-for="c in claims" :key="c.id" :claim="c" />
            <div v-if="ed.editable"><CardPicker :kinds="['element']" :anchor="{ part: part.id }" label="елемент" /></div>
          </div>
          <template v-if="ed.editable">
            <div v-for="p in pairs" :key="p.slug" class="small text-secondary d-flex flex-wrap align-items-center column-gap-2">
              <span>💡 є «{{ p.element }}» — додай і те, що він робить: «{{ p.fn }}»</span>
              <button type="button" class="btn btn-sm btn-add py-0" @click="addPair(p.slug)"><Icon name="plus" /> додати</button>
            </div>
          </template>
        </template>
        <div v-if="error" class="text-danger small">{{ error }}</div>
      </template>
    </div>
  </div>
</template>

<style scoped>
/* the title and the type wrap inside their own block, so the pencil and the trash stay in the card on a phone */
.head { display: flex; flex-wrap: wrap; align-items: center; gap: .25rem .5rem; min-width: 0; overflow-wrap: anywhere; }
</style>
