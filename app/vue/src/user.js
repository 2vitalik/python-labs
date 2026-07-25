import { ref } from 'vue'

import { getMe } from './api.js'

export const user = ref(null)

export async function loadUser() {
  user.value = await getMe()
}
