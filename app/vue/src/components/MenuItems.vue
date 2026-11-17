<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import Reveal from '@core/components/Reveal.vue'
import Tip from '@core/components/Tip.vue'
import { vPeek } from '@core/peek.js'
import { deletePart, postPart } from '../api.js'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import { setTools, toolsOn } from '../tools.js'
import { useJumps } from '../windowJumps.js'
import CardSign from './CardSign.vue'
import MenuTarget from './MenuTarget.vue'
import PartBlock from './PartBlock.vue'
import ToolsButton from './ToolsButton.vue'

// «Переходи й дії» of a window (T278 §4), in two columns: what was pressed or what happened → the window it leads to (a click
// goes there) or the action card, then a note. Under the items — the jumps the rules make, to read only: named by the
// rule's reason, a click goes to the rule. A window, a card or a rule named here shows its card under the mouse.
// The owner changes an item's words and its note where they read (T306). No form (T310): the pencil by the caption — or
// the card's own (`tools`) — turns the rows' tools on: a click on where a row leads changes it instead of going there,
// «＋ нотатка», a minus by every row, «＋ перехід або дія» under them. A new row is typed where it will stand; Enter saves
// it and the next one waits under it. `menu` — the Part of kind menu hosted on this window, made with its first row —
// its title stays «Меню «…»»: the samples find it by that; an item is { title, window, task, note }
const props = defineProps({ window: Object, menu: Object, tools: Boolean })
const ed = useEd()
const own = computed(() => `${props.window.id}:menu`)
const on = computed(() => ed.editable && (props.tools || toolsOn(own.value)))
const adding = ref(false)
const n = ref(0)  // every saved row brings a fresh one to type
const items = computed(() => props.menu?.items || [])
const all = useJumps()
const jumps = computed(() => all.value.filter((j) => j.from === props.window.id))
const winTitle = (id) => ed.windows.find((w) => w.id === id)?.title
const setItems = (fn) => ed.save.part(props.menu.id, (m) => ({ items: fn(m.items) }))
const setItem = (i, patch) => setItems((list) => list.map((it, j) => (j === i ? { ...it, ...patch } : it)))
async function addItem(title) {
  const item = { title, window: '', task: '', note: '' }
  if (props.menu) await setItems((list) => [...list, item])
  else {
    await postPart({ kind: 'menu', title: `Меню «${props.window.title}»`, window: props.window.id, items: [item] })
    await ed.changed()
  }
  n.value++
}
function begin() {
  setTools(own.value, true)
  adding.value = true
}
async function removeAll() {
  try {
    await deletePart(props.menu.id)
    await ed.changed()
  } catch (e) {
    ed.fail(e.message)
  }
}
</script>

<template>
  <div v-if="items.length || jumps.length || ed.editable" class="small">
    <PartBlock pic="goto" zone="interface" title="Переходи й дії">
      <!-- by the caption (T294 §8): «＋» while there are none, the pencil once there are — unless the card's own is on -->
      <template v-if="ed.editable" #after>
        <ToolsButton v-if="items.length && !tools" :id="own" what="переходах і діях" />
        <button v-else-if="!items.length && !adding" type="button" class="iact add qtip" data-tip="＋ перехід" aria-label="додати перехід" @click="begin"><Icon name="plus" /></button>
      </template>
      <Reveal :show="on">
        <Tip id="menu-form-rows" class="mb-1">Рядок — що натиснули чи що сталось, і куди це веде: інше вікно або дія — картка, що щось робить
          (рестарт рівня, гучність, збереження). Перехід за подією гри (перемога → вікно) задає правило.</Tip>
      </Reveal>
      <div v-if="items.length || jumps.length || adding" class="moves" :class="{ on }">
        <div v-for="(it, i) in items" :key="i" class="move">
          <InlineText :value="it.title" :can="ed.editable" required placeholder="пункт, кнопка, клавіша" :save="(title) => setItem(i, { title })" />
          <span>
            <MenuTarget v-if="on" :item="it" :host="window.id" :save="(to) => setItem(i, to)" />
            <a v-else-if="winTitle(it.window)" v-peek="{ kind: 'window', id: it.window }" href="#" class="text-decoration-none" @click.prevent="jump('p-' + it.window)">→ <Icon name="win" /> {{ winTitle(it.window) }}</a>
            <span v-else-if="it.window" class="text-secondary">→ вікна вже нема</span>
            <span v-else-if="it.task">→ <CardSign :task="ed.info(it.task)" /> <span v-peek="{ kind: 'task', id: it.task }">{{ ed.info(it.task)?.title || it.task }}</span></span>
            <span v-if="it.note || on" class="text-secondary"><template v-if="it.window || it.task || on"> · </template><InlineText :value="it.note || ''" :can="ed.editable"
              placeholder="нотатка — як: клавіша, сам через 3 с…" :save="(note) => setItem(i, { note })"><template #empty><span class="more-field">＋ нотатка</span></template></InlineText></span>
          </span>
          <Transition name="tool">
            <button v-if="on" type="button" class="iact del mini" :title="`Прибрати рядок «${it.title}»`" @click="setItems((list) => list.filter((_, j) => j !== i))"><Icon name="minus" /></button>
          </Transition>
        </div>
        <!-- outside the columns: a long placeholder must not push the rows' second column away -->
        <div v-if="adding" :key="`new-${n}`" class="move new">
          <InlineText value="" can fresh required placeholder="пункт, кнопка, клавіша: «Нова гра», Esc…" :save="addItem" @drop="adding = false" />
        </div>
        <div v-for="j in jumps" :key="j.rule + j.to" v-peek="{ kind: 'rule', id: j.rule }" class="move rule" role="button" @click="jump('r-' + j.rule)">
          <span><Icon name="bolt" /> {{ j.title }}</span>
          <span>→ <Icon name="win" /> {{ winTitle(j.to) }}</span>
        </div>
      </div>
      <Reveal :show="on && !adding">
        <div class="d-flex align-items-center mt-1">
          <button type="button" class="more-field" @click="adding = true">＋ перехід або дія</button>
          <DelButton v-if="menu && items.length" class="ms-auto" what="усі переходи й дії цього вікна" title="Видалити всі переходи й дії" @yes="removeAll" />
        </div>
      </Reveal>
    </PartBlock>
  </div>
</template>

<style scoped>
/* one grid for all the rows of the window, so both columns line up; a long title wraps rather than widens its column */
.moves { display: grid; grid-template-columns: fit-content(55%) minmax(0, 1fr); column-gap: .75rem; overflow-wrap: anywhere; }
.moves.on { grid-template-columns: fit-content(55%) minmax(0, 1fr) auto; }  /* the minuses' column */
.move { display: grid; grid-column: 1 / -1; grid-template-columns: subgrid; align-items: baseline; padding: .05rem .25rem; margin: 0 -.25rem; border-radius: .25rem; }
.move.new { display: block; }
.mini { align-self: center; }
/* a jump a rule makes wears the rules' violet, as on the map */
.rule { color: color-mix(in srgb, #8e24aa 70%, var(--bs-body-color)); cursor: pointer; }
.rule:hover { background: var(--bs-tertiary-bg); }
</style>
