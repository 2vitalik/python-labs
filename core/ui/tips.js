import { reactive } from 'vue'

import { load, save } from './local.js'

// the explanations the reader has put away (Tip.vue, T291 §5): by the tip's id, remembered in this browser
const read = () => { try { return JSON.parse(load('tips') || '{}') } catch { return {} } }
const off = reactive(read())

export const isOff = (id) => !!off[id]
export function setOff(id, on) {
  if (on) off[id] = 1
  else delete off[id]
  save('tips', JSON.stringify(off))
}
