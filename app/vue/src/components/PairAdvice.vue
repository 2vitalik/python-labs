<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { answersOf, hide, isHidden } from '../advice.js'
import { postClaim } from '../api.js'
import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'

// advice on a window's card (T278 §11): its type or an element hints at a function of the whole game (a volume slider →
// the volume really changes). Asked, not ordered, while none of the answers is claimed; «не про мою гру» hides it for
// this game. Not in the sample's sandbox, the short form or a reader's view. `part` — the window
const props = defineProps({ part: Object })
const ed = useEd()
const error = ref('')
const busy = ref(false)
const title = (slug) => ed.info(slug)?.title || slug
const either = (names) => (names.length > 1 ? `${names.slice(0, -1).join(', ')} або ${names.at(-1)}` : names[0])
// a window type and the function behind it may share a title («Досягнення»): the kind's word tells them apart
const what = (slug) => `${kindOf(ed.info(slug)) === 'window' ? 'вікно' : 'елемент'} «${title(slug)}»`
const fn = (f, slugs) => (slugs.some((s) => title(s) === title(f)) ? `сама функція «${title(f)}»` : `«${title(f)}»`)
const line = (slugs, fns) => `Є ${slugs.map(what).join(' і ')}. Може, у грі є й ${either(fns.map((f) => fn(f, slugs)))}?`

// the window type and an element asking the same make one advice
const advice = computed(() => {
  if (!ed.editable || ed.sandbox || ed.simple) return []
  const out = []
  const own = ed.claimsOf(props.part.id).filter((c) => !c.auto).map((c) => c.task)
  for (const slug of new Set([props.part.task, ...own])) {
    const all = answersOf(slug), fns = all.filter((f) => ed.info(f))  // a card the reader cannot see is not offered
    if (!fns.length || all.some((f) => ed.claims.some((c) => c.task === f)) || isHidden(ed.game.id, `pair:${slug}`)) continue
    const same = out.find((a) => a.fns.join() === fns.join())
    if (same) same.slugs.push(slug)
    else out.push({ slugs: [slug], fns })
  }
  return out
})
const wave = (a) => a.slugs.forEach((s) => hide(ed.game.id, `pair:${s}`, line([s], a.fns)))

async function add(slug) {
  error.value = ''
  busy.value = true
  try {
    const c = await postClaim({ task: slug, params: {} })
    await ed.changed()
    jump(`c-${c.id}`)
  } catch (e) {
    error.value = e.message
  }
  busy.value = false
}
</script>

<template>
  <div v-for="a in advice" :key="a.slugs[0]" class="advice small">
    <span>💡 {{ line(a.slugs, a.fns) }}</span>
    <span class="d-inline-flex flex-wrap align-items-center gap-1">
      <button v-for="f in a.fns" :key="f" type="button" class="btn btn-sm btn-add py-0" :disabled="busy" :title="ed.info(f)?.description"
              @click="add(f)"><Icon name="plus" /> {{ a.fns.length > 1 ? title(f) : 'так, додати' }}</button>
      <button type="button" class="off" title="сховати цю пораду для цієї гри; повернути — під списком «чого бракує» вгорі" @click="wave(a)">не про мою гру</button>
    </span>
  </div>
  <div v-if="error" class="text-danger small">{{ error }}</div>
</template>

<style scoped>
/* a hint's colour — not an error's, not an add's */
.advice { display: flex; flex-wrap: wrap; align-items: baseline; gap: .25rem .5rem; padding: .3rem .5rem; border-radius: .375rem;
          background: var(--bs-warning-bg-subtle); border-left: 3px solid var(--bs-warning-border-subtle); }
.off { padding: 0 .15rem; border: 0; background: none; color: var(--bs-secondary-color); text-decoration: underline dashed; text-underline-offset: .2em; }
.off:hover { color: var(--bs-body-color); }
</style>
