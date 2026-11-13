import { ref } from 'vue'

import { extra } from '@core/http.js'

// the teacher edits a student's game (T282 Б): while it is on, every «my game» call carries the header and the server works
// on that student's game, writing the teacher into its history. The router switches it off on leaving the page
export const editing = ref('')  // the student's nick while on

export function setEditing(nick) {
  editing.value = nick
  if (nick) extra['X-Game-Of'] = nick
  else delete extra['X-Game-Of']
}
