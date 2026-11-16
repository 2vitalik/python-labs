<script setup>
import { ref } from 'vue'

import InlinePop from '@core/components/InlinePop.vue'
import { EMOJI_SETS } from '../emojis.js'

// an entity's own emoji picked on its card (T306): a click on the icon — the grid of typical ones, a field for any other,
// and «as its type» to drop it; each is saved at once. `icon` — its own, `fallback` — its type's
const p = defineProps({ can: Boolean, icon: String, fallback: String, save: Function })
const own = ref('')
const put = (e, choose) => choose(p.save(e))
</script>

<template>
  <InlinePop :can width="17rem" tip="Клік — інша іконка" @update:open="own = ''">
    <span class="ico">{{ icon || fallback }}</span>
    <template #panel="{ choose }">
      <input v-model="own" class="form-control form-control-sm mb-2" placeholder="своє емодзі — і Enter" @keydown.enter.prevent="own.trim() && put(own.trim(), choose)">
      <div v-for="[name, list] in EMOJI_SETS" :key="name" class="mb-1">
        <div class="grp">{{ name }}</div>
        <div class="d-flex flex-wrap">
          <button v-for="e in list" :key="e" type="button" class="em" :class="{ on: e === icon }" @click="put(e, choose)">{{ e }}</button>
        </div>
      </div>
      <button type="button" class="btn btn-link btn-sm p-0 text-secondary text-decoration-none" @click="put('', choose)">без своєї — як у типу {{ fallback }}</button>
    </template>
  </InlinePop>
</template>

<style scoped>
.ico { font-size: 1.35rem; line-height: 1; }
.grp { font-size: .65rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
.em { width: 1.85rem; height: 1.85rem; padding: 0; border: 0; border-radius: .3rem; background: none; font-size: 1.1rem; line-height: 1; }
.em:hover { background: var(--bs-tertiary-bg); }
.em.on { background: var(--bs-secondary-bg); }
</style>
