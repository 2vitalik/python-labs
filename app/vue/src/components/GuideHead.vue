<script setup>
import { computed, nextTick, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

import { flash } from '@core/anchors.js'
import { getGuidePage } from '@core/api.js'
import GuideBody from '@core/components/GuideBody.vue'
import GuideFoot from '@core/components/GuideFoot.vue'
import GuideText from '@core/components/GuideText.vue'
import IconChevron from '@core/components/IconChevron.vue'
import { textOf } from '@core/drafts.js'
import { load, save } from '@core/local.js'
import { tocOf } from '@core/md.js'
import { user } from '@core/user.js'

// guide section on top of a catalog page: the whole text for guests and students (the catalog itself
// stays admin-only until it is ready — T116 Q13); above the catalog — a framed block that folds and remembers it,
// or, moved down, sits under the catalog in the page's #guide-low (remembered too).
// `toc` = the text's headings while it is on screen, for the page's side contents; `low` = the block is under the catalog
const props = defineProps({ slug: String, stub: String })
const emit = defineEmits(['toc', 'low'])
const page = ref(null)
const admin = computed(() => user.value?.status === 'admin')
const text = computed(() => textOf(page.value))

const key = `guide-head:${props.slug}`
const open = ref(load(key) !== '0')
function remember(e) {
  open.value = e.target.open
  save(key, open.value ? '1' : '0')
}
watch([text, open, admin], () => emit('toc', open.value || !admin.value ? tocOf(text.value) : []), { immediate: true })

const low = ref(load(`${key}:low`) === '1')
const link = ref()
const moved = ref(false)
// the view follows the block: the link just clicked stays on screen, ready to take the move back
async function move() {
  low.value = !low.value
  save(`${key}:low`, low.value ? '1' : '0')
  moved.value = true
  await nextTick()
  link.value.scrollIntoView({ block: 'center' })
}
watch(low, () => emit('low', low.value), { immediate: true })

// #catalog is the page's own target under this text (its closing link, also followed from /method):
// the place it will keep is known only once the text is drawn
const route = useRoute()
getGuidePage(props.slug).then(async (p) => {
  page.value = p
  await nextTick()
  if (route.hash === '#catalog') flash('catalog')
})
</script>

<template>
  <template v-if="page">
    <!-- Teleport moves the block without remounting it: an open editor survives the move -->
    <Teleport v-if="admin" defer to="#guide-low" :disabled="!low">
      <details class="rounded px-3 py-2" :class="[low ? 'mt-4' : open ? 'mb-4' : 'mb-3', { moved }]" :open="open"
               @toggle="remember" @animationend.self="moved = false">
        <summary class="d-flex align-items-center gap-2 text-secondary">
          <span>{{ page.title }} — текст методички</span>
          <span class="ms-auto small d-flex align-items-center gap-1" :class="open ? 'text-primary' : 'text-secondary'">
            {{ open ? 'згорнути' : 'розгорнути' }} <IconChevron :dir="open ? 'up' : 'down'" />
          </span>
        </summary>
        <GuideBody v-model:page="page" class="mt-3 mb-2" />
        <div class="move small text-end mb-1">
          <a ref="link" href="#" @click.prevent="move">{{ low ? '↑ перенести вгору' : '↓ перенести вниз' }}</a>
        </div>
      </details>
    </Teleport>
    <div v-else>
      <h1 class="h2 mb-3">{{ page.title }}</h1>
      <GuideText :text="text" />
      <div id="catalog" class="alert alert-light border mt-4">🚧 {{ stub }}</div>
      <GuideFoot />
    </div>
  </template>
</template>

<style scoped>
details { border: 1px solid var(--bs-border-color); }  /* not .border: its !important would beat the glow */
/* just moved: lights up like a flashed card (style.css) — a pale fill and a ring */
.moved { animation: moved 2.5s ease-out; }
@keyframes moved {
  0%, 45% { background-color: color-mix(in srgb, var(--bs-warning-bg-subtle) 50%, var(--bs-body-bg));
            border-color: var(--bs-warning-border-subtle); box-shadow: 0 0 0 .25rem var(--bs-warning-bg-subtle); }
}
summary { cursor: pointer; list-style: none; }
summary::-webkit-details-marker { display: none; }
.move a { color: var(--bs-tertiary-color); text-decoration: none; }
.move a:hover { color: var(--bs-body-color); }
</style>
