<script setup>
import { ref } from 'vue'

import Pop from '@core/components/Pop.vue'
import EmojiPanel from './EmojiPanel.vue'

// an own emoji in a form (T270 §7, T309): a narrow button with the icon — or, dimmed, with the type's (`placeholder`) —
// and the picker on a click; an emoji of one's own is typed into the picker's search. `hint` — the words the picker
// offers icons by; `legend` — for a storyboard's legend; `big` — beside full-size fields
const icon = defineModel({ type: String, default: '' })
defineProps({ placeholder: String, hint: String, legend: Boolean, big: Boolean })
const open = ref(false)
const put = (e) => { icon.value = e; open.value = false }
</script>

<template>
  <Pop v-model="open" width="24rem">
    <template #trigger="{ toggle }">
      <button type="button" class="form-control emoji" :class="{ none: !icon, 'form-control-sm': !big, big }" title="своя іконка — емодзі" :aria-expanded="open"
              @click="toggle">{{ icon || placeholder || '＋' }}</button>
    </template>
    <EmojiPanel :icon :fallback="placeholder" :hint :legend @pick="put" />
  </Pop>
</template>

<style scoped>
.emoji { width: 2.6rem; padding-inline: .2rem; overflow: hidden; text-align: center; font-size: 1.05rem; white-space: nowrap; }
.emoji.big { width: 3.4rem; font-size: 1.25rem; line-height: 1.2; }
.emoji.none { color: var(--bs-secondary-color); filter: grayscale(.6); opacity: .6; }
</style>
