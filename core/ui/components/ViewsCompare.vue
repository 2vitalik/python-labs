<script setup>
import { computed, inject, ref } from 'vue'

import { versionsOf, viewOf } from '../viewStore.js'
import Icon from './Icon.vue'
import ViewDiff from './ViewDiff.vue'

// the comparison at the bottom of the window (T315 §8): two marks — views or versions, from any of the library's looks —
// read «А → Б»; one mark asks for the second. In a few words or in full; sides swapped; closed — the marks go
const lib = inject('viewsLib')
const full = ref(false)
function side(key) {
  const [slug, n] = key.split('@')
  const v = viewOf(slug)
  const ver = n && versionsOf(slug).find((x) => x.n === Number(n))
  if (!v || (n && !ver)) return null
  return { key, title: `${v.emoji} ${v.title}${n ? ` · в. ${n}` : ''}`.trim(), query: (ver || v).query }
}
const sides = computed(() => lib.picks.map(side).filter(Boolean))
</script>

<template>
  <Transition name="vcmp">
    <div v-if="lib.picks.length" class="vcmp border rounded bg-body">
      <div class="vcmp-head">
        <Icon name="compare" class="text-secondary" />
        <b class="vcmp-name" :title="sides[0]?.title">{{ sides[0]?.title }}</b>
        <Icon name="arrow" class="text-secondary" />
        <b v-if="sides[1]" class="vcmp-name" :title="sides[1].title">{{ sides[1].title }}</b>
        <span v-else class="text-secondary">обери другий вид чи версію</span>
        <span class="vcmp-tools">
          <span v-if="sides[1]" class="vcmp-mode" role="group" aria-label="Як показати різницю">
            <button type="button" :class="{ on: !full }" :aria-pressed="!full" @click="full = false">коротко</button>·<button
              type="button" :class="{ on: full }" :aria-pressed="full" @click="full = true">докладно</button>
          </span>
          <button type="button" class="iact" :disabled="sides.length < 2" title="Поміняти місцями" @click="lib.picks.reverse()"><Icon name="repeat" /></button>
          <button type="button" class="iact" title="Закрити порівняння" @click="lib.picks = []"><Icon name="x" /></button>
        </span>
      </div>
      <ViewDiff v-if="sides.length === 2" :a="sides[0]" :b="sides[1]" :cols="lib.cols" :full class="vcmp-body" />
    </div>
  </Transition>
</template>

<style scoped>
.vcmp { padding: .45rem .5rem .55rem .75rem; box-shadow: 0 .25rem 1rem rgb(0 0 0 / .14); }
.vcmp-head { display: flex; align-items: center; gap: .45rem; min-width: 0; }
.vcmp-name { min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.vcmp-tools { display: flex; flex: none; align-items: center; gap: .2rem; margin-left: auto; }
.vcmp-mode { display: inline-flex; gap: .3rem; margin-right: .4rem; font-size: .8rem; color: var(--bs-secondary-color); }
.vcmp-mode button { padding: 0; border: 0; background: none; color: inherit; }
.vcmp-mode button:hover, .vcmp-mode button.on { color: var(--bs-body-color); }
.vcmp-mode button.on { font-weight: 600; }
.iact:disabled { opacity: .35; }
.vcmp-body { max-height: 40vh; margin-top: .35rem; overflow-y: auto; }
.vcmp-enter-active, .vcmp-leave-active { transition: opacity .2s ease, transform .2s ease; }
.vcmp-enter-from, .vcmp-leave-to { opacity: 0; transform: translateY(.75rem); }
@media (prefers-reduced-motion: reduce) { .vcmp-enter-active, .vcmp-leave-active { transition: none; } }
</style>
