<script setup>
import { computed, ref } from 'vue'

import { parseOption } from '../polls.js'
import { site } from '../site.js'
import { saveView } from '../viewStore.js'
import Icon from './Icon.vue'
import InlinePop from './InlinePop.vue'

// a view's icon (T315 §2.2): its emoji, or a grey drawn table while it has none. With `can` a click opens a picker under it —
// the site's own panel when it gives one (site.table.emojiPanel: props icon, hint, event pick), else a small palette and a
// field for any other emoji. A pick is saved at once; «без значка» takes the icon away
const p = defineProps({ view: { type: Object, required: true }, can: Boolean })
const PALETTE = '📋 🚀 📅 ⏰ 🔥 ⚠️ ✅ ❌ 🙋 🤖 🐙 🎮 🧪 📊 🧮 📝 🎯 👀 😴 🆘 ⭐ 🏁 🎓 💬 🧩 📦 🔍 ⏳ 🚫 🎬'.split(' ')
const panel = site.table?.emojiPanel
const own = ref('')
const typed = computed(() => parseOption(own.value).emoji)
const save = (emoji) => saveView(p.view.slug, { emoji })
</script>

<template>
  <InlinePop :can :width="panel ? '24rem' : '16.5rem'" tip="Клік — інший значок">
    <span class="vicon"><template v-if="view.emoji">{{ view.emoji }}</template><Icon v-else name="table" class="none" /></span>
    <template #panel="{ choose }">
      <component :is="panel" v-if="panel" :icon="view.emoji" :hint="view.title" @pick="choose(save($event))" />
      <template v-else>
        <div class="pal">
          <button v-for="e in PALETTE" :key="e" type="button" :class="{ on: e === view.emoji }" @click="choose(save(e))">{{ e }}</button>
        </div>
        <input v-model="own" class="form-control form-control-sm mt-2" placeholder="свій: встав емодзі й Enter" aria-label="Свій значок"
               @keydown.enter.prevent="typed && choose(save(typed))">
      </template>
      <button v-if="view.emoji" type="button" class="more-field mt-2" @click="choose(save(''))">без значка</button>
    </template>
  </InlinePop>
</template>

<style scoped>
.vicon { display: inline-flex; align-items: center; justify-content: center; min-width: 1.25em; line-height: 1; }
.none { color: var(--bs-secondary-color); opacity: .7; }
.pal { display: grid; grid-template-columns: repeat(6, 1fr); gap: .15rem; }
.pal button { height: 2.2rem; padding: 0; border: 0; border-radius: .35rem; background: none; font-size: 1.2rem; line-height: 1; }
.pal button:hover { background: var(--bs-tertiary-bg); }
.pal button.on { box-shadow: inset 0 0 0 2px var(--bs-primary-border-subtle); }
</style>
