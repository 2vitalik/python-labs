import { onScopeDispose, ref, toValue, watchEffect } from 'vue'

import { site } from './site.js'

const own = ref('')  // the open page's title from its data; empty → the route's meta.title

// tab title: «<page> · <the site's name>»
export function watchTitle(route) {
  watchEffect(() => (document.title = [own.value || route.meta.title, site.name].filter(Boolean).join(' · ')))
}

export function useTitle(text) {
  watchEffect(() => (own.value = toValue(text)))
  onScopeDispose(() => (own.value = ''))
}
