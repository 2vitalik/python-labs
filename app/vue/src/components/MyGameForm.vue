<script setup>
import { computed, ref, watch } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import TagInput from '@core/components/TagInput.vue'
import { games } from '../catalog.js'

// creating the game: base · title · description as three cards, the profile's way (ProfileForm);
// once it exists the same fields fold into one compact card above the description's sections, plus the tick order
const props = defineProps({ dirty: Boolean, saved: Boolean, error: String, fresh: Boolean })
defineEmits(['save'])
const form = defineModel({ type: Object, required: true })
const custom = ref(false)
const changing = ref(false)
watch(() => form.value.base_custom, (v) => v && !form.value.base_game && (custom.value = true))
const pick = (slug) => { form.value.base_game = slug; custom.value = !slug; changing.value = false }
const chosen = computed(() => games.value.find((g) => g.slug === form.value.base_game))
const showChips = computed(() => props.fresh || changing.value)
</script>

<template>
  <form @submit.prevent="$emit('save')">
    <div id="about" class="card mb-3">
      <div v-if="fresh" class="card-header">Основа</div>
      <div class="card-body" :class="{ 'py-2': !fresh }">
        <div v-if="!fresh && !showChips" class="d-flex align-items-center gap-2 small mb-2">
          <span class="text-secondary">Основа:</span>
          <RouterLink v-if="chosen" :to="`/games/${chosen.slug}`">{{ chosen.icon }} {{ chosen.title }}</RouterLink>
          <span v-else>✨ {{ form.base_custom }}</span>
          <a href="#" class="text-secondary text-decoration-none ms-1" @click.prevent="changing = true">змінити</a>
        </div>
        <template v-if="showChips">
          <div class="d-flex flex-wrap gap-1">
            <button v-for="g in games" :key="g.slug" type="button" class="btn btn-sm chip"
                    :class="form.base_game === g.slug ? 'btn-primary' : 'btn-outline-secondary'" @click="pick(g.slug)">{{ g.icon }} {{ g.title }}</button>
            <button type="button" class="btn btn-sm chip" :class="custom ? 'btn-primary' : 'btn-outline-secondary'" @click="pick('')">✨ своя</button>
          </div>
          <input v-if="custom" v-model="form.base_custom" class="form-control mt-2" placeholder="Кількома словами: що за гра" required>
          <div class="form-text mt-2">
            <template v-if="chosen">Про основу — на її сторінці: <RouterLink :to="`/games/${chosen.slug}`">{{ chosen.title }} ↗</RouterLink></template>
            <template v-else-if="custom">Своя — теж на клітинковому полі; викладач подивиться і, може, додасть її в каталог</template>
            <template v-else>Одна з ігор каталогу — або своя</template>
          </div>
        </template>
        <template v-if="!fresh">
          <input v-model="form.title" class="form-control form-control-lg fw-semibold border-0 px-0 shadow-none" placeholder="Назва гри" required>
          <GrowArea v-model="form.description" class="form-control border-0 px-0 shadow-none" placeholder="Що за гра і чим відрізняється від основи (Markdown можна)" />
          <div class="d-flex flex-wrap align-items-center gap-2 small mt-1">
            <span class="text-secondary text-nowrap" title="Порядок кроків одного тіку або ходу: знімає спір «хто ходить першим»">🔁 Порядок тіку:</span>
            <TagInput v-model="form.phases" :hash="false" class="flex-grow-1 form-control-sm phases" placeholder="ввід → гравець → вороги → … (слово і Enter)"
                      :known="['ввід', 'гравець', 'вороги', 'снаряди', 'середовище', 'спавн', 'перевірка перемоги', 'рендер']" />
          </div>
        </template>
      </div>
    </div>

    <template v-if="fresh">
      <div id="title" class="card mb-3">
        <div class="card-header">Назва</div>
        <div class="card-body">
          <input v-model="form.title" class="form-control" placeholder="Наприклад: Танчики делюкс" autocomplete="off" required>
          <div v-if="!form.title" class="form-text mt-2">Своя назва проєкту, не назва основи</div>
        </div>
      </div>
      <div id="description" class="card mb-3">
        <div class="card-header">Опис</div>
        <div class="card-body">
          <GrowArea v-model="form.description" class="form-control" placeholder="Що за гра і чим відрізнятиметься від основи" />
          <div v-if="!form.description" class="form-text mt-2">Не обовʼязково зараз — допишеш, коли задум устоїться. Markdown можна</div>
        </div>
      </div>
    </template>

    <div v-if="fresh || dirty || saved || error" class="d-flex align-items-center gap-3" :class="{ 'mb-3': !fresh }">
      <button class="btn btn-primary" :class="{ 'btn-sm': !fresh }" :disabled="!dirty">{{ fresh ? 'Створити гру' : 'Зберегти' }}</button>
      <Transition name="saved">
        <span v-if="saved" class="text-success small">✓ Збережено</span>
      </Transition>
      <span v-if="error" class="text-danger small">{{ error }}</span>
    </div>
  </form>
</template>

<style scoped>
.saved-enter-active { transition: opacity .2s; }
.saved-leave-active { transition: opacity .6s; }
.saved-enter-from, .saved-leave-to { opacity: 0; }
.phases { font-size: .85rem; }
</style>
