import { onScopeDispose, ref, toValue, watchEffect } from 'vue'

const own = ref('')  // the open page's title from its data; empty → the route's meta.title

// tab title: «<page> · Python Labs»
export function watchTitle(route) {
  watchEffect(() => (document.title = [own.value || route.meta.title, 'Python Labs'].filter(Boolean).join(' · ')))
}

export function useTitle(text) {
  watchEffect(() => (own.value = toValue(text)))
  onScopeDispose(() => (own.value = ''))
}
