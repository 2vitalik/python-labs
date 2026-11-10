import { ref } from 'vue'

import { extra } from '@core/http.js'

// the sample's sandbox (T274 §7): while it is on, every «my game» call carries the header and the server works on the
// reader's scratch copy of the sample instead of their game. The router switches it off on leaving the page
export const sandbox = ref('')  // the base game's slug while on

export function setSandbox(slug) {
  sandbox.value = slug
  if (slug) extra['X-Sandbox'] = slug
  else delete extra['X-Sandbox']
}
