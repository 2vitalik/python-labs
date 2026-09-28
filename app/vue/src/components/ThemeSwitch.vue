<script setup>
import { onMounted, onUnmounted, ref } from 'vue'

import { MODES, mode, setMode } from '../theme.js'
import IconTheme from './IconTheme.vue'

// the button shows the current mode, the list names all three: a click that changes nothing on the page
// (dark → «as on the device» on a dark device) still reads as a change
const root = ref()
const open = ref(false)
const close = (e) => root.value.contains(e.target) || (open.value = false)
onMounted(() => document.addEventListener('click', close))
onUnmounted(() => document.removeEventListener('click', close))

function pick(m) {
  setMode(m)
  open.value = false
}
</script>

<template>
  <div ref="root" class="dropdown">
    <button type="button" class="btn btn-sm border-0 p-1 d-inline-flex text-body-secondary"
            :title="`Тема: ${MODES[mode].toLowerCase()}`" @click="open = !open">
      <IconTheme :mode />
    </button>
    <!-- data-bs-popper: Bootstrap's own rules for a menu placed without Popper (under the button, right edges aligned) -->
    <ul class="dropdown-menu dropdown-menu-end" :class="{ show: open }" data-bs-popper="static">
      <li v-for="(text, m) in MODES" :key="m">
        <button type="button" class="dropdown-item d-flex align-items-center gap-2" :class="{ active: mode === m }" @click="pick(m)">
          <IconTheme :mode="m" /> {{ text }}
        </button>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.btn:hover { color: var(--bs-body-color) !important; }
</style>
