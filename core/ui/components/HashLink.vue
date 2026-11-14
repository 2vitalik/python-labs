<script setup>
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import Icon from './Icon.vue'

// a link to this place of the page (T291 §11): a quiet «#» by a block's heading. A click puts #id into the address and
// the whole link into the clipboard; whoever arrives by it is scrolled to the block, and it lights up (App.vue, anchors.js)
const props = defineProps({ id: String })
const route = useRoute()
const router = useRouter()
const done = ref(false)

async function take() {
  await router.replace({ query: route.query, hash: `#${props.id}` })
  try { await navigator.clipboard.writeText(location.href) } catch { /* the address bar has it anyway */ }
  done.value = true
  setTimeout(() => (done.value = false), 1500)
}
</script>

<template>
  <a :href="`#${id}`" class="hlink" :class="{ done }" :title="done ? 'посилання скопійовано' : 'посилання на це місце: клік — в адресу й у буфер'"
     @click.prevent.stop="take"><Icon :name="done ? 'check' : 'hash'" /></a>
</template>

<style>
.hlink { display: inline-flex; align-items: center; justify-content: center; width: 1.3rem; height: 1.3rem; flex-shrink: 0; border-radius: .25rem;
         color: var(--bs-secondary-color); font-size: .8rem; font-weight: 400; opacity: .4; }
.hlink:hover { background: var(--bs-tertiary-bg); color: var(--bs-body-color); opacity: 1; }
.hlink.done { color: var(--bs-success); opacity: 1; }
</style>
