<script setup>
import { computed, ref, watch } from 'vue'

import { diffEdits } from '../lectureChangeDiff.js'
import { markupOnly } from '../lectureChangeMarks.js'
import { hunksOf, raw, setRaw } from '../lectureChanges.js'
import ChangeBlock from './ChangeBlock.vue'
import ChangeLinks from './ChangeLinks.vue'
import ChangeWhy from './ChangeWhy.vue'

// a change opened under its row: «Було» | «Стало» side by side — the whole block, this change's edits lit, the other
// changes of the same block pale — with the blocks around it, quieter, above and below; a record with no pair (a doubt,
// the layout) — the one block. Then why, what it is, where to look
const props = defineProps({ it: Object, items: Array })
const emit = defineEmits(['ready'])
const hunk = ref(null)
const error = ref('')
const NONE = { before: '', after: '', prev: '', next: '' }
watch(() => props.it.id, async () => {
  hunk.value = null
  error.value = ''
  try {
    hunk.value = (await hunksOf(props.it.slug))[props.it.hunk] || NONE
    emit('ready')
  } catch (e) {
    error.value = e.message
  }
}, { immediate: true })

const pair = computed(() => hunk.value && hunk.value.before !== hunk.value.after)
const others = computed(() => props.items.filter((x) => x.slug === props.it.slug && x.hunk === props.it.hunk && x !== props.it))
// the catalogue gives no edits where only the markup differs (the look's automatic items): a diff of our own then
const editsOf = (x) => (x.edits.length || x !== props.it ? x.edits : diffEdits(hunk.value.before, hunk.value.after))
function ranges(side) {
  const one = (x, pale) => editsOf(x).filter((e) => e[side] || (side === 'a' ? e.del : e.ins)).map((e) => ({
    s: e[side]?.[0] ?? 0, e: e[side]?.[1] ?? 0, frag: side === 'a' ? e.del : e.ins, other: side === 'a' ? e.ins : e.del, js: e.js,
    cls: (side === 'a' ? 'del' : 'ins') + (pale ? ' pale' : ''),
  }))
  return [...one(props.it, false), ...others.value.flatMap((x) => one(x, true))]
}
const wide = ref(false)  // the blocks around in full, not just their edges
// a colour's tag or `**` only: as on the site there is nothing to light — the raw view shows it
const markup = computed(() => pair.value && editsOf(props.it).every(markupOnly))
</script>

<template>
  <div class="chg-open">
    <div class="chg-bar">
      <div class="btn-group btn-group-sm" role="group" aria-label="Як показати блок">
        <button type="button" class="btn chip" :class="raw ? 'btn-outline-secondary' : 'btn-secondary'" :aria-pressed="!raw" @click="setRaw(false)">вигляд</button>
        <button type="button" class="btn chip" :class="raw ? 'btn-secondary' : 'btn-outline-secondary'" :aria-pressed="raw" @click="setRaw(true)">розмітка</button>
      </div>
      <button v-if="hunk && (hunk.prev || hunk.next)" type="button" class="dot small" @click="wide = !wide">
        {{ wide ? 'менше довкола' : 'більше довкола' }}</button>
      <span v-if="markup && !raw" class="quiet">змінено лише розмітку — її видно в «розмітці»</span>
    </div>
    <p v-if="error" class="text-danger small mb-2">{{ error }}</p>
    <p v-else-if="!hunk" class="quiet chg-wait">Беру блок…</p>
    <div v-else class="chg-cols" :class="{ one: !pair, wide }">
      <template v-if="pair">
        <h3 class="side-b">Було</h3>
        <h3 class="side-a">Стало</h3>
      </template>
      <ChangeBlock v-if="hunk.prev" class="ctx prev" :text="hunk.prev" :raw :slug="it.slug" />
      <ChangeBlock v-if="hunk.prev && pair" class="ctx prev dup" :text="hunk.prev" :raw :slug="it.slug" />
      <template v-if="pair">
        <ChangeBlock class="blk side-b" :text="hunk.before" :ranges="ranges('a')" :raw :slug="it.slug" empty="не було" />
        <ChangeBlock class="blk side-a" :text="hunk.after" :ranges="ranges('b')" :raw :slug="it.slug" empty="прибрано" />
      </template>
      <ChangeBlock v-else class="blk" :text="hunk.after" :raw :slug="it.slug" empty="запис про слайд загалом" />
      <ChangeBlock v-if="hunk.next" class="ctx next" :text="hunk.next" :raw :slug="it.slug" />
      <ChangeBlock v-if="hunk.next && pair" class="ctx next dup" :text="hunk.next" :raw :slug="it.slug" />
    </div>
    <ChangeWhy :it />
    <ChangeLinks :it />
  </div>
</template>
