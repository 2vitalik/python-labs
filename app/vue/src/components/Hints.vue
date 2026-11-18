<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { hiddenOf, hide, unhide } from '../advice.js'
import { useEd } from '../ed.js'
import { jump } from '@core/jump.js'

// «чого бракує» — a few gentle lines; a click shows the place: the page scrolls there and it flashes.
// An advice line (`advice`, T278 §11) can be hidden for this game; the hidden ones wait under the list with «повернути».
// No advice in the sample's sandbox, as on the window cards. A framed group with its caption (T301 §3):
// it must not read as the explanation of the «＋ Додати» field above it
const props = defineProps({ items: Array })
const ed = useEd()
const asks = computed(() => ed.editable && !ed.sandbox)
const lines = computed(() => props.items.filter((h) => !h.advice || asks.value))
const hidden = computed(() => (asks.value ? hiddenOf(ed.game.id) : []))
const open = ref(false)
</script>

<template>
  <div v-if="lines.length || hidden.length" class="group-box small">
    <div class="group-cap mb-1">Підказки</div>
    <ul v-if="lines.length" class="lines list-unstyled mb-0 vstack gap-1">
      <li v-for="h in lines" :key="h.key || h.text" role="button" class="d-flex gap-1 align-items-baseline" title="показати, де це" @click="jump(h.to)">
        <span>💡</span><span class="text">{{ h.text }}</span><span class="go text-nowrap">показати <Icon name="right" /></span>
        <button v-if="h.advice" type="button" class="quiet off text-nowrap" title="сховати цю пораду для цієї гри"
                @click.stop="hide(ed.game.id, h.key, h.text)"><Icon name="x" /> не про мою гру</button>
      </li>
    </ul>
    <div v-if="hidden.length" :class="{ 'mt-1': lines.length }">
      <button type="button" class="quiet" :aria-expanded="open" @click="open = !open">сховані поради ({{ hidden.length }})</button>
      <ul v-if="open" class="list-unstyled mb-0 mt-1 vstack gap-1">
        <li v-for="a in hidden" :key="a.key" class="d-flex gap-2 align-items-baseline">
          <span class="text">{{ a.text }}</span>
          <button type="button" class="quiet text-nowrap" @click="unhide(ed.game.id, a.key)">повернути</button>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.text { color: var(--bs-secondary-color); }
.go { margin-left: .25rem; font-size: .75rem; color: var(--bs-secondary-color); opacity: 0; }
.lines li:hover .text { color: var(--bs-body-color); }
.lines li:hover .go { opacity: 1; }
.quiet { padding: 0; border: 0; background: none; color: var(--bs-secondary-color); text-decoration: underline dashed; text-underline-offset: .2em; }
.quiet:hover { color: var(--bs-body-color); }
.off { margin-left: .25rem; font-size: .75rem; }
</style>
