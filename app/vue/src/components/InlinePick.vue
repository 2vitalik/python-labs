<script setup>
import { computed, ref, watch } from 'vue'

import InlinePop from '@core/components/InlinePop.vue'
import Picker from './Picker.vue'
import ProposeCard from './ProposeCard.vue'

// a value chosen from a list right where it reads (T306) — a type of an entity or a window: InlinePop with the list of
// Picker, every option with its line, the current one ticked; a pick is saved at once. `items` — a function, run only
// when the panel opens (the window types are the whole catalog); `propose` — { what, allTo, zone, subzone, then }: none
// fits — the idea goes to the teacher (ProposeCard) and meanwhile the value is `then`, as the forms do
const p = defineProps({ can: Boolean, items: Function, current: String, save: Function, placeholder: String, propose: Object, tip: String,
  width: { type: String, default: '24rem' } })
const open = ref(false)
const proposing = ref(false)
watch(open, () => (proposing.value = false))
const rows = computed(() => (open.value ? p.items().map((it) => ({ ...it, taken: it.key === p.current })) : []))
const pick = (it, choose, close) => (it.key === p.current ? close() : choose(p.save(it.key)))
</script>

<template>
  <InlinePop v-model:open="open" :can :width :tip>
    <template #default="{ open: on }"><slot :open="on" /></template>
    <template #panel="{ choose, close }">
      <template v-if="proposing">
        <ProposeCard :what="propose.what" :all-to="propose.allTo" :zone="propose.zone" :subzone="propose.subzone"
                     @done="choose(save(propose.then))" @cancel="proposing = false" />
        <button type="button" class="btn btn-link btn-sm p-0 mt-1 text-decoration-none" @click="proposing = false">← до списку</button>
      </template>
      <Picker v-else inline autofocus :items="rows" :placeholder @pick="pick($event, choose, close)">
        <template v-if="propose" #footer>
          <div class="foot">Нема потрібного? <a href="#" @click.prevent="proposing = true">запропонувати</a></div>
        </template>
      </Picker>
    </template>
  </InlinePop>
</template>

<style scoped>
.foot { margin: .4rem .5rem .1rem; padding-top: .4rem; border-top: 1px solid var(--bs-border-color-translucent); font-size: .78rem; color: var(--bs-secondary-color); }
</style>
