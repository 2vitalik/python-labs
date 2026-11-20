import { ref } from 'vue'

import { load, save } from '@core/local.js'

// how a lecture looks (T374 §5): with the lecturer's colours (`<c-b>…</c-b>` in the text, lecture.css) or calm — the tags
// say nothing then. Remembered in this browser; the class `lec-author` stands on the text and on the slides
const KEY = 'lec-look'
export const author = ref(load(KEY) !== 'calm')
export function toggleLook() {
  author.value = !author.value
  save(KEY, author.value ? 'author' : 'calm')
}
