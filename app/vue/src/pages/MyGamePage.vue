<script setup>
import { computed, onMounted, ref } from 'vue'

import { postMyGame, putMyGame } from '../api.js'
import Crumbs from '@core/components/Crumbs.vue'
import GameEditor from '../components/GameEditor.vue'
import GameHead from '../components/GameHead.vue'
import MyGameForm from '../components/MyGameForm.vue'
import { loadCatalog } from '../catalog.js'
import { loadMyGame, myClaims, myGame, myParts, myRules, reloadInsides } from '../myGame.js'
import { useForm } from '@core/form.js'
import { user } from '@core/user.js'

// the student's game: base, title, description — then its description proper (field, entities, rules, windows, claims)
const loaded = ref(false)
const { form, dirty, saved, error, fill, save } = useForm({ title: '', base_game: '', base_custom: '', description: '', phases: [] })
const nick = computed(() => user.value?.nick)

const submit = () => save(async (f) => {
  myGame.value = await (myGame.value ? putMyGame(f) : postMyGame(f))
  if (!myParts.value.length) await reloadInsides()
  return myGame.value
})

onMounted(async () => {
  await Promise.all([loadCatalog(), loadMyGame(true)])
  if (myGame.value) fill(myGame.value)
  loaded.value = true
})
</script>

<template>
  <div v-if="loaded">
    <Crumbs :items="['Моя гра']">
      <RouterLink to="/students?view=cards" class="btn btn-outline-secondary btn-sm">🎮 Ігри студентів</RouterLink>
    </Crumbs>
    <GameHead :game="myGame" title="Моя гра" :checks="!myGame">
      <RouterLink v-if="myGame" :to="`/students/${nick}`" class="ms-auto small text-nowrap">Як це бачать інші →</RouterLink>
    </GameHead>
    <p v-if="!myGame" class="text-secondary">Обери основу з каталогу або опиши свою, дай назву — і гра твоя. Далі опишеш поле, сутності, правила, вікна й заявиш картки каталогу.</p>
    <MyGameForm v-model="form" :dirty :saved :error :fresh="!myGame" @save="submit" />
    <GameEditor v-if="myGame" :game="myGame" :parts="myParts" :claims="myClaims" :rules="myRules" :tasks="{}" editable :nick @changed="reloadInsides" />
  </div>
</template>
