<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import { useJumps } from '../windowJumps.js'
import CardSign from './CardSign.vue'
import MenuForm from './MenuForm.vue'
import PartBlock from './PartBlock.vue'

// «Переходи й дії» of a window (T278 §4), in two columns: what was pressed or what happened → the window it leads to (a click
// goes there) or the action card, then a note. Under the items — the jumps the rules make, to read only: named by the
// rule's reason, a click goes to the rule. A window, a card or a rule named here shows its card under the mouse.
// The owner edits the items in place (MenuForm, framed as an open form — the new-thing frame while there is no menu); `menu` — the Part of kind menu hosted on this window, if there is one yet
const props = defineProps({ window: Object, menu: Object })
const ed = useEd()
const edit = ref(false)
const items = computed(() => props.menu?.items || [])
const all = useJumps()
const jumps = computed(() => all.value.filter((j) => j.from === props.window.id))
const winTitle = (id) => ed.windows.find((w) => w.id === id)?.title
</script>

<template>
  <div v-if="items.length || jumps.length || ed.editable" class="small">
    <MenuForm v-if="edit" :window :menu class="editing open-form" :class="{ new: !menu }" @done="edit = false" @cancel="edit = false" />
    <PartBlock v-else pic="goto" zone="interface" title="Переходи й дії">
      <!-- by the caption (T294 §8): «＋» while there are none, the pencil once there are -->
      <template v-if="ed.editable" #after>
        <button v-if="items.length" type="button" class="iact qtip" data-tip="Редагувати переходи й дії" aria-label="Редагувати переходи й дії" @click="edit = true"><Icon name="pencil" /></button>
        <button v-else type="button" class="iact add qtip" data-tip="＋ перехід" aria-label="додати перехід" @click="edit = true"><Icon name="plus" /></button>
      </template>
      <div v-if="items.length || jumps.length" class="moves">
        <div v-for="(it, i) in items" :key="i" class="move">
          <span>{{ it.title }}</span>
          <span>
            <a v-if="winTitle(it.window)" v-peek="{ kind: 'window', id: it.window }" href="#" class="text-decoration-none" @click.prevent="jump('p-' + it.window)">→ <Icon name="win" /> {{ winTitle(it.window) }}</a>
            <span v-else-if="it.window" class="text-secondary">→ вікна вже нема</span>
            <span v-else-if="it.task">→ <CardSign :task="ed.info(it.task)" /> <span v-peek="{ kind: 'task', id: it.task }">{{ ed.info(it.task)?.title || it.task }}</span></span>
            <span v-if="it.note" class="text-secondary"><template v-if="it.window || it.task"> · </template>{{ it.note }}</span>
          </span>
        </div>
        <div v-for="j in jumps" :key="j.rule + j.to" v-peek="{ kind: 'rule', id: j.rule }" class="move rule" role="button" @click="jump('r-' + j.rule)">
          <span><Icon name="bolt" /> {{ j.title }}</span>
          <span>→ <Icon name="win" /> {{ winTitle(j.to) }}</span>
        </div>
      </div>
    </PartBlock>
  </div>
</template>

<style scoped>
.open-form { padding: .45rem; }  /* the form's frame (T291 §4) keeps off its fields */
/* one grid for all the rows of the window, so both columns line up; a long title wraps rather than widens its column */
.moves { display: grid; grid-template-columns: fit-content(55%) minmax(0, 1fr); column-gap: .75rem; overflow-wrap: anywhere; }
.move { display: grid; grid-column: 1 / -1; grid-template-columns: subgrid; padding: .05rem .25rem; margin: 0 -.25rem; border-radius: .25rem; }
/* a jump a rule makes wears the rules' violet, as on the map */
.rule { color: color-mix(in srgb, #8e24aa 70%, var(--bs-body-color)); cursor: pointer; }
.rule:hover { background: var(--bs-tertiary-bg); }
</style>
