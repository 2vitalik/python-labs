<script setup>
import { ref } from 'vue'

import Pop from '@core/components/Pop.vue'

// an entity's own emoji (T270 §7): a narrow field and, on a click, a grid of typical game emojis; empty — the type's icon,
// which the field shows as its placeholder
const icon = defineModel({ type: String, default: '' })
defineProps({ placeholder: String })
const open = ref(false)
const SETS = [
  ['люди й істоти', '🧍 🧙 🥷 🤖 👾 👻 🧟 💀 🐉 🐍 🕷️ 🦇 🐺 🐱 🐸 🐟 👽'],
  ['речі', '🔑 💎 🪙 🍎 🍒 ❤️ ⭐ 💣 🔸 🏹 🗡️ 🛡️ 📦 🧪 🎁'],
  ['клітини й природа', '🧱 🟫 🟩 🟦 ⬛ 🌲 🪨 🌊 🔥 ❄️ 🌵 🚪 🕳️'],
  ['знаки', '🚩 🏁 🎯 ❌ ⭕ ⚡ ✨ 💥 ❓ 🔒'],
].map(([name, list]) => [name, list.split(' ')])
const put = (e) => { icon.value = e; open.value = false }
</script>

<template>
  <Pop v-model="open" width="17rem">
    <template #trigger>
      <input v-model="icon" class="form-control form-control-sm emoji" :placeholder title="своя іконка — емодзі" @focus="open = true" @click="open = true">
    </template>
    <div v-for="[name, list] in SETS" :key="name" class="mb-1">
      <div class="grp">{{ name }}</div>
      <div class="grid">
        <button v-for="e in list" :key="e" type="button" class="em" :class="{ on: e === icon }" @click="put(e)">{{ e }}</button>
      </div>
    </div>
    <button type="button" class="btn btn-link btn-sm p-0 text-secondary text-decoration-none" @click="put('')">без своєї — як у типу</button>
  </Pop>
</template>

<style scoped>
.emoji { width: 2.6rem; padding-inline: .2rem; text-align: center; font-size: 1.05rem; }
.grp { font-size: .65rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
.grid { display: flex; flex-wrap: wrap; }
.em { width: 1.85rem; height: 1.85rem; padding: 0; border: 0; border-radius: .3rem; background: none; font-size: 1.1rem; line-height: 1; }
.em:hover { background: var(--bs-tertiary-bg); }
.em.on { background: var(--bs-secondary-bg); }
</style>
