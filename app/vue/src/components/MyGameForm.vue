<script setup>
import { computed, ref, watch } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { games } from '../catalog.js'
import MdField from './MdField.vue'

// creating the game: base · title · description as three cards, the profile's way (ProfileForm);
// once it exists the same fields fold into one compact card above the description's sections, and «змінити основу» opens
// the choice with its own «Зберегти» / «Скасувати» (T274 §10). The description reads as the others see it, rendered, and
// a click turns it into its Markdown in place (T304, MdField). A changed title or description brings the same pair right
// under them, into a row that is always there — so nothing below moves when the first letter is typed. While a change waits
// for «Зберегти», the card wears the frame of an open form (T291 §4)
const props = defineProps({ dirty: Boolean, changed: { type: Array, default: () => [] }, saved: Boolean, error: String, fresh: Boolean })
const emit = defineEmits(['save', 'reset'])
const form = defineModel({ type: Object, required: true })
const custom = ref(false)
const writing = ref(false)  // the description shows its Markdown source (MdField)
const was = ref(null)  // the base before «змінити основу», while the choice is open
watch(() => form.value.base_custom, (v) => v && !form.value.base_game && (custom.value = true))
watch(() => props.saved, (v) => v && (was.value = null))
// what waits for «Зберегти» — named in the bar that floats over the page, wherever it is scrolled to
const NAMES = { title: 'назва гри', description: 'опис гри', base_game: 'основа', base_custom: 'основа' }
const unsaved = computed(() => [...new Set(props.changed.map((k) => NAMES[k] || k))].join(', '))
const texts = computed(() => props.changed.some((k) => k === 'title' || k === 'description'))
function undo() {
  emit('reset')  // the page puts the saved values back at once
  was.value = null
  custom.value = !form.value.base_game && !!form.value.base_custom
}
const pick = (slug) => { form.value.base_game = slug; custom.value = !slug }
const change = () => (was.value = { base_game: form.value.base_game, base_custom: form.value.base_custom })
function cancel() {
  Object.assign(form.value, was.value)
  custom.value = !was.value.base_game
  was.value = null
}
const moved = computed(() => was.value && (form.value.base_game !== was.value.base_game || form.value.base_custom !== was.value.base_custom))
const chosen = computed(() => games.value.find((g) => g.slug === form.value.base_game))
const showChips = computed(() => props.fresh || !!was.value)
</script>

<template>
  <form @submit.prevent="$emit('save')">
    <div id="about" class="card mb-3" :class="{ editing: !fresh && (was || texts) }" data-dock>
      <div v-if="fresh" class="card-header">Основа<span class="tip-dock ms-1" /></div>
      <div class="card-body" :class="{ 'py-2': !fresh }">
        <div v-if="!fresh && !showChips" class="d-flex align-items-center gap-2 small mb-2">
          <span class="text-secondary">Основа:</span>
          <RouterLink v-if="chosen" :to="`/games/${chosen.slug}`">{{ chosen.icon }} {{ chosen.title }}</RouterLink>
          <span v-else>✨ {{ form.base_custom }}</span>
          <a href="#" class="text-secondary ms-1" title="Обрати іншу гру-основу: описане лишається, міняються еталон і підказки" @click.prevent="change">змінити основу</a>
        </div>
        <template v-if="showChips">
          <div class="d-flex flex-wrap gap-1">
            <button v-for="g in games" :key="g.slug" type="button" class="btn btn-sm chip"
                    :class="form.base_game === g.slug ? 'btn-primary' : 'btn-outline-secondary'" @click="pick(g.slug)">{{ g.icon }} {{ g.title }}</button>
            <button type="button" class="btn btn-sm chip" :class="custom ? 'btn-primary' : 'btn-outline-secondary'" @click="pick('')">✨ своя</button>
          </div>
          <input v-if="custom" v-model="form.base_custom" class="form-control mt-2" placeholder="Кількома словами: що за гра" required>
          <Tip id="game-base" class="mt-2">
            <template v-if="chosen">Про основу — на її сторінці: <RouterLink :to="`/games/${chosen.slug}`">{{ chosen.title }} ↗</RouterLink></template>
            <template v-else-if="custom">Своя — теж на клітинковому полі; викладач подивиться і, може, додасть її в каталог</template>
            <template v-else>Одна з ігор каталогу — або своя</template>
            <template v-if="!fresh"> · Зміна основи нічого не стирає: описане лишається, міняються лише еталон і підказки</template>
          </Tip>
          <div v-if="!fresh" class="d-flex flex-wrap align-items-center gap-2 mt-2 mb-2">
            <button class="btn btn-sm btn-success" :disabled="!moved"><Icon name="check" /> Зберегти</button>
            <button type="button" class="btn btn-sm btn-outline-secondary" @click="cancel">Скасувати</button>
            <span v-if="error" class="text-danger small">{{ error }}</span>
          </div>
        </template>
        <template v-if="!fresh">
          <input v-model="form.title" class="form-control form-control-lg fw-semibold soft-input px-2 mt-1" placeholder="Назва гри" title="Назва гри — можна редагувати" required>
          <MdField v-model="form.description" v-model:open="writing" :dirty="changed.includes('description')"
                   placeholder="Що за гра і чим відрізняється від основи — натисни й пиши" @save="$emit('save')" />
          <!-- the row is there from the moment the source opens, so nothing jumps when the first letter is typed -->
          <div v-if="writing || texts" class="foot">
            <template v-if="texts">
              <button class="btn btn-sm btn-success"><Icon name="check" /> Зберегти</button>
              <button type="button" class="btn btn-sm btn-outline-secondary" @click="undo">Скасувати</button>
              <span v-if="error" class="text-danger small">{{ error }}</span>
            </template>
            <span v-if="writing" class="md" title="Опис розуміє Markdown: **жирний**, *курсив*, списки з «- », [посилання](https://…) · ⌘/Ctrl+Enter — зберегти">Markdown</span>
          </div>
        </template>
      </div>
    </div>

    <template v-if="fresh">
      <div id="title" class="card mb-3" data-dock>
        <div class="card-header">Назва<span class="tip-dock ms-1" /></div>
        <div class="card-body">
          <input v-model="form.title" class="form-control" placeholder="Наприклад: Танчики делюкс" autocomplete="off" required>
          <Tip v-if="!form.title" id="game-title" class="mt-2">Своя назва проєкту, не назва основи</Tip>
        </div>
      </div>
      <div id="description" class="card mb-3" data-dock>
        <div class="card-header">Опис<span class="tip-dock ms-1" /></div>
        <div class="card-body">
          <GrowArea v-model="form.description" class="form-control" placeholder="Що за гра і чим відрізнятиметься від основи" />
          <Tip v-if="!form.description" id="game-desc" class="mt-2">Не обовʼязково зараз — допишеш, коли задум устоїться. Markdown можна</Tip>
        </div>
      </div>
    </template>

    <div v-if="fresh" class="d-flex align-items-center gap-3">
      <button class="btn btn-primary" :disabled="!dirty">Створити гру</button>
      <span v-if="error" class="text-danger small">{{ error }}</span>
    </div>
    <!-- a bar over the page, not a row in it: nothing below jumps when the first letter is typed, and it is in sight
         however far the page is scrolled — «десь є незбережене» always says where -->
    <Transition v-else name="saved">
      <div v-if="dirty || saved" class="unsaved shadow border rounded bg-body">
        <template v-if="dirty">
          <span><span class="dot" /> Не збережено: <b>{{ unsaved }}</b></span>
          <button class="btn btn-sm btn-success"><Icon name="check" /> Зберегти</button>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="undo">Скасувати</button>
          <span v-if="error" class="text-danger w-100">{{ error }}</span>
        </template>
        <span v-else class="text-success">✓ Збережено</span>
      </div>
    </Transition>
  </form>
</template>

<style scoped>
/* the frame of an open edit (T291 §4) is a pixel thicker than the card's: the body gives the pixel back, nothing inside shifts */
.editing > .card-body { margin: -1px; }
/* as tall as its buttons whether they are there or not */
.foot { display: flex; flex-wrap: wrap; align-items: center; gap: .5rem; min-height: calc(1.5 * .875rem + .5rem + 2px); margin-top: .25rem; padding: 0 .5rem; }
/* right under the field's frame, not in the middle of the reserved row */
.md { align-self: flex-start; margin: -.2rem 0 0 auto; font-size: .65rem; color: var(--bs-secondary-color); opacity: .7; cursor: help; }
.unsaved { position: fixed; z-index: 1040; left: 50%; bottom: 1rem; transform: translateX(-50%); display: flex; flex-wrap: wrap; align-items: center;
           gap: .4rem .6rem; max-width: calc(100vw - 1.5rem); padding: .45rem .7rem; font-size: .875rem; }
.dot { display: inline-block; width: .5rem; height: .5rem; margin-right: .15rem; border-radius: 50%; background: var(--bs-warning); }
.saved-enter-active { transition: opacity .2s; }
.saved-leave-active { transition: opacity .6s; }
.saved-enter-from, .saved-leave-to { opacity: 0; }
</style>
