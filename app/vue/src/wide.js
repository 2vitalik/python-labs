import { computed, ref } from 'vue'

import { load, save } from './local.js'
import { user } from './user.js'

// /tasks catalog on the whole window instead of the page column — the admin's choice, remembered in this browser
const KEY = 'tasks-wide'
export const wide = ref(load(KEY) === '1')
export const wideOn = computed(() => wide.value && user.value?.status === 'admin')
export function toggleWide() {
  wide.value = !wide.value
  save(KEY, wide.value ? '1' : '0')
}
