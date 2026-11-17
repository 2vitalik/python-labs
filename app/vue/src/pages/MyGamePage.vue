<script setup>
import { computed, onMounted, ref } from 'vue'

import { postMyGame, putMyGame } from '../api.js'
import Crumbs from '@core/components/Crumbs.vue'
import Icon from '@core/components/Icon.vue'
import GameEditor from '../components/GameEditor.vue'
import GameHead from '../components/GameHead.vue'
import MyGameForm from '../components/MyGameForm.vue'
import { loadCatalog, vocab } from '../catalog.js'
import { loadMyGame, myClaims, myCoins, myGame, myParts, myRules, myTasks, reloadInsides } from '../myGame.js'
import { useForm } from '@core/form.js'
import { user } from '@core/user.js'
import { wideOf } from '@core/wide.js'

// the student's game: base, title, description — then its description proper (field, levels, entities, rules, windows, cards)
const loaded = ref(false)
const wide = wideOf('game').on
const { form, dirty, changed, saved, error, fill, save, reset } = useForm({ title: '', base_game: '', base_custom: '', description: '' })
const nick = computed(() => user.value?.nick)
const intro = computed(() => (vocab.value.depth === 'simple' ? 'Далі опишеш, хто й що є на полі та які екрани має гра.' : 'Далі опишеш поле, рівні, сутності, правила, вікна й заявиш картки каталогу.'))

// blank lines before and after the text say nothing and keep an empty row in the field (T301 §7); spaces that start the
// first line stay — Markdown may need them
const tidy = (s) => s.replace(/^\s*\n/, '').trimEnd()
// the tick order lives in «Правила» and is saved from there: the head form must not send its stale copy back
const submit = () => save(async (f) => {
  f = { ...f, title: f.title.trim(), description: tidy(f.description) }
  myGame.value = await (myGame.value ? putMyGame({ ...f, phases: myGame.value.phases }) : postMyGame(f))
  if (!myParts.value.length) await reloadInsides()
  return myGame.value
})

// the name is changed in the big heading and saved at once (T310); a description still being written stays in its field
async function rename(title) {
  const g = myGame.value
  myGame.value = await putMyGame({ title, base_game: g.base_game, base_custom: g.base_custom, description: g.description, phases: g.phases })
  fill({ title: myGame.value.title })
}

onMounted(async () => {
  await Promise.all([loadCatalog(), loadMyGame(true)])
  if (myGame.value) fill(myGame.value)
  loaded.value = true
})
</script>

<template>
  <div v-if="loaded">
    <!-- on the whole window (GameEditor's toggle) only the description widens: the head keeps the page column -->
    <div :class="{ 'in-column': wide }">
    <Crumbs :items="['Моя гра']">
      <RouterLink to="/students?view=cards" class="btn btn-outline-secondary btn-sm"><Icon name="gamepad" /> Ігри студентів</RouterLink>
    </Crumbs>
    <GameHead :game="myGame" title="Моя гра" :checks="!myGame" :rename>
      <RouterLink v-if="myGame" :to="`/students/${nick}`" class="ms-auto small text-nowrap">Як це бачать інші →</RouterLink>
      <RouterLink v-if="myGame" to="/my/game/history" class="small text-nowrap" title="Хто що змінював у грі"><Icon name="clock" /> Історія</RouterLink>
    </GameHead>
    <p v-if="!myGame" class="text-secondary">Обери основу з каталогу або опиши свою, дай назву — і гра твоя. {{ intro }}</p>
    <MyGameForm v-model="form" :dirty :changed :saved :error :fresh="!myGame" @save="submit" @reset="reset" />
    </div>
    <GameEditor v-if="myGame" :game="myGame" :parts="myParts" :claims="myClaims" :rules="myRules" :tasks="myTasks" :coins="myCoins"
                editable :nick :reload="() => loadMyGame(true)" />
  </div>
</template>
