<script setup>
import { computed, ref, watch } from 'vue'

import GrowArea from '@core/components/GrowArea.vue'
import { games } from '../catalog.js'

// the profile's way (ProfileForm): a card per field, hints while it is empty, «Зберегти» only once something changed.
// The base is a row of chips — the catalog's games and «своя»; the latter is pressed by hand, not by an empty base_game,
// so a new game starts with nothing pressed
defineProps({ dirty: Boolean, saved: Boolean, error: String, fresh: Boolean })
defineEmits(['save'])
const form = defineModel({ type: Object, required: true })
const custom = ref(false)
watch(() => form.value.base_custom, (v) => v && !form.value.base_game && (custom.value = true))
const pick = (slug) => { form.value.base_game = slug; custom.value = !slug }
const chosen = computed(() => games.value.find((g) => g.slug === form.value.base_game))
</script>

<template>
  <form @submit.prevent="$emit('save')">
    <div id="base" class="card mb-3">
      <div class="card-header">Основа</div>
      <div class="card-body">
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
      </div>
    </div>

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

    <div class="d-flex align-items-center gap-3">
      <button class="btn btn-primary" :disabled="!dirty">{{ fresh ? 'Створити гру' : 'Зберегти' }}</button>
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
</style>
