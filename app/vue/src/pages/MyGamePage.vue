<script setup>
import { computed, onMounted, ref } from 'vue'

import { getMyGame, postMyGame, putMyGame } from '../api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GameHead from '../components/GameHead.vue'
import MyGameForm from '../components/MyGameForm.vue'
import MyGameParts from '../components/MyGameParts.vue'
import { loadCatalog } from '../catalog.js'
import { useForm } from '@core/form.js'
import { user } from '@core/user.js'

// a student picks the base, names the game and describes it — the profile's way; the game's insides (windows, menus,
// entities, rules, claims) stay the admin's until the mechanism is ready to show (T216)
const game = ref(null)
const loaded = ref(false)
const admin = computed(() => user.value?.status === 'admin')
const { form, dirty, saved, error, fill, save } = useForm({ title: '', base_game: '', base_custom: '', description: '' })

const submit = () => save(async (f) => (game.value = await (game.value ? putMyGame(f) : postMyGame(f))))

onMounted(async () => {
  loadCatalog()
  game.value = await getMyGame()
  if (game.value) fill(game.value)
  loaded.value = true
})
</script>

<template>
  <div v-if="loaded">
    <Crumbs :items="['Моя гра']">
      <RouterLink to="/students?view=cards" class="btn btn-outline-secondary btn-sm">🎮 Ігри студентів</RouterLink>
    </Crumbs>
    <GameHead :game title="Моя гра" checks>
      <RouterLink v-if="game" :to="`/students/${user.nick}`" class="ms-auto small">Як це бачать інші →</RouterLink>
    </GameHead>
    <p v-if="!game" class="text-secondary">Обери основу з каталогу або опиши свою, дай назву — і гра твоя.</p>
    <MyGameForm v-model="form" :dirty :saved :error :fresh="!game" @save="submit" />
    <MyGameParts v-if="admin && game" :game class="mt-5" />
  </div>
</template>
