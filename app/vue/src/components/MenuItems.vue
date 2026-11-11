<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { useEd } from '../ed.js'
import { jump } from '../jump.js'
import { ruleJumps } from '../windowJumps.js'
import MenuForm from './MenuForm.vue'
import PartLabel from './PartLabel.vue'

// «Переходи й дії» of a window (T278 §4), in two columns: what was pressed or what happened → the window it leads to (a click
// goes there) or the action card, then a note. Under the items — the jumps the rules make, to read only: a click goes to the
// rule. The owner edits the items in place (MenuForm); `menu` — the Part of kind menu hosted on this window, if there is one yet
const props = defineProps({ window: Object, menu: Object })
const ed = useEd()
const edit = ref(false)
const items = computed(() => props.menu?.items || [])
const jumps = computed(() => ruleJumps(ed.windows, ed.rules || []).filter((j) => j.from === props.window.id))
const winTitle = (id) => ed.windows.find((w) => w.id === id)?.title
</script>

<template>
  <div v-if="items.length || jumps.length || ed.editable" class="small">
    <MenuForm v-if="edit" :window :menu @done="edit = false" @cancel="edit = false" />
    <div v-else class="vstack gap-1">
      <div v-if="items.length || jumps.length" class="d-flex align-items-start gap-2">
        <div class="flex-grow-1 min-w-0">
          <PartLabel icon="↪" zone="interface">Переходи й дії</PartLabel>
          <div class="moves">
            <div v-for="(it, i) in items" :key="i" class="move">
              <span>{{ it.title }}</span>
              <span>
                <a v-if="winTitle(it.window)" href="#" class="text-decoration-none" @click.prevent="jump('p-' + it.window)">→ 🪟 {{ winTitle(it.window) }}</a>
                <span v-else-if="it.window" class="text-secondary">→ 🪟 вікна вже нема</span>
                <span v-else-if="it.task" :title="ed.info(it.task)?.description">⚙ {{ ed.info(it.task)?.title || it.task }}</span>
                <span v-if="it.note" class="text-secondary"><template v-if="it.window || it.task"> · </template>{{ it.note }}</span>
              </span>
            </div>
            <div v-for="j in jumps" :key="j.rule + j.to" class="move rule" role="button" title="перехід за правилом — змінюється правилом; клік — до правила"
                 @click="jump('r-' + j.rule)">
              <span>⚡ {{ j.title }}</span>
              <span>→ 🪟 {{ winTitle(j.to) }}</span>
            </div>
          </div>
        </div>
        <button v-if="ed.editable && items.length" type="button" class="iact" title="Редагувати переходи й дії" @click="edit = true"><Icon name="pencil" /></button>
      </div>
      <div v-if="ed.editable && !items.length">
        <button type="button" class="btn btn-sm btn-add" @click="edit = true"><Icon name="plus" /> перехід</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.min-w-0 { min-width: 0; }
/* one grid for all the rows of the window, so both columns line up; a long title wraps rather than widens its column */
.moves { display: grid; grid-template-columns: fit-content(55%) minmax(0, 1fr); column-gap: .75rem; margin-top: .25rem; overflow-wrap: anywhere; }
.move { display: grid; grid-column: 1 / -1; grid-template-columns: subgrid; padding: .05rem .25rem; margin: 0 -.25rem; border-radius: .25rem; }
.rule { color: var(--bs-secondary-color); cursor: pointer; }
.rule:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
</style>
