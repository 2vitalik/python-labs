<script setup>
import { computed, ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { putMyGame } from '../api.js'
import { useEd } from '../ed.js'
import { gameBrushes } from '../momentMap.js'
import GameMoments from './GameMoments.vue'
import MomentEditor from './MomentEditor.vue'

// «Як це грається» (T276 «Те саме студентам», T291 §15): the owner draws the game's moments — scenarios of frames with the
// game's entities for brushes — and saves them with the game; everyone else sees them step by step. A scenario of three
// frames claims «Ігровий момент по кадрах» by itself (auto_claims.py). Unsaved changes frame the block; the row of
// «Зберегти / Скасувати» keeps its room, so nothing jumps when it shows
const ed = useEd()
const saved = computed(() => ed.game?.moments || '')
const text = ref(saved.value)
watch(saved, (now, was) => text.value === was && (text.value = now))  // a reload after another form keeps a draft in work
const dirty = computed(() => text.value !== saved.value)
const palette = computed(() => gameBrushes(ed.entities))
const busy = ref(false)
const error = ref('')

async function save() {
  error.value = ''
  busy.value = true
  try {
    const { title, base_game, base_custom, description, phases } = ed.game
    await putMyGame({ title, base_game, base_custom, description, phases, moments: text.value })
    await ed.changed()
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div v-if="ed.editable" class="box vstack gap-2" :class="{ editing: dirty }">
    <Tip v-if="!saved" id="moments-how">
      Покажи по кадрах, як грається твоя гра: звичайний хід, особлива ситуація, перемога. Малюй значками сутностей, «＋ кадр»
      копіює попередній. Сценарій із трьох кадрів сам заявляє картку «Ігровий момент по кадрах».
    </Tip>
    <MomentEditor v-model="text" :palette empty="▫️" />
    <div class="d-flex flex-wrap align-items-center gap-2" :class="{ idle: !dirty }">
      <button type="button" class="btn btn-sm btn-success" :disabled="busy" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="text = saved">Скасувати</button>
      <span v-if="error" class="text-danger small">{{ error }}</span>
    </div>
  </div>
  <GameMoments v-else-if="saved" :text="saved" />
  <div v-else class="text-secondary small">Ще не показано, як грається.</div>
</template>

<style scoped>
/* the frame of unsaved changes (T291 §4) is always there, unseen: it showing does not shift the editor */
.box { padding: .5rem; border: 2px solid transparent; border-radius: .45rem; }
.idle { visibility: hidden; }
</style>
