<script setup>
import InlinePop from '@core/components/InlinePop.vue'
import EmojiPanel from './EmojiPanel.vue'

// an entity's own emoji picked on its card (T306, T309): a click on the icon — the picker, a pick is saved at once.
// `icon` — its own, `fallback` — its type's, `hint` — the entity's name and type: the picker offers icons by them
defineProps({ can: Boolean, icon: String, fallback: String, hint: String, save: Function })
</script>

<template>
  <InlinePop :can width="24rem" tip="Клік — інша іконка">
    <span class="ico">{{ icon || fallback }}</span>
    <template #panel="{ choose }">
      <EmojiPanel :icon :fallback :hint @pick="choose(save($event))" />
    </template>
  </InlinePop>
</template>

<style scoped>
.ico { font-size: 1.35rem; line-height: 1; }
</style>
