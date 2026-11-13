<script setup>
// line icons of one style on a 16×16 grid, drawn by hand — no icon package; a new icon is a new line here
defineProps({ name: String })
const PATHS = {
  plus: '<circle cx="8" cy="8" r="6.5"/><path d="M8 5v6M5 8h6"/>',
  minus: '<circle cx="8" cy="8" r="6.5"/><path d="M5 8h6"/>',
  done: '<circle cx="8" cy="8" r="6.5"/><path d="M5 8.3l2.1 2.1L11 6"/>',
  check: '<path d="M3 8.5l3.2 3.2L13 4.8"/>',
  x: '<path d="M4 4l8 8M12 4l-8 8"/>',
  pencil: '<path d="M11.2 2.3l2.5 2.5L5.5 13H3v-2.5z"/><path d="M9.7 3.8l2.5 2.5"/>',
  trash: '<path d="M2.5 4.5h11M6 4.5V3h4v1.5M4 4.5l.7 8.5h6.6l.7-8.5M6.7 7v4M9.3 7v4"/>',
  move: '<path d="M2 8h8M7 5l3 3-3 3M13.5 3v10"/>',
  image: '<rect x="2" y="3" width="12" height="10" rx="1.5"/><circle cx="5.6" cy="6.4" r="1"/><path d="M2.5 11.5l3.5-3 2.5 2 2-1.5 3 2.5"/>',
  down: '<path d="M4 6l4 4 4-4"/>',
  right: '<path d="M6 4l4 4-4 4"/>',
  left: '<path d="M10 4L6 8l4 4"/>',
  link: '<path d="M6.8 9.2a2.5 2.5 0 0 0 3.5 0l2-2a2.5 2.5 0 0 0-3.5-3.5l-.8.8"/><path d="M9.2 6.8a2.5 2.5 0 0 0-3.5 0l-2 2a2.5 2.5 0 0 0 3.5 3.5l.8-.8"/>',
  note: '<path d="M2.5 3.5h11v7h-6l-3 2.5v-2.5h-2z"/>',
  eye: '<path d="M1.5 8S4 3.5 8 3.5 14.5 8 14.5 8 12 12.5 8 12.5 1.5 8 1.5 8z"/><circle cx="8" cy="8" r="2"/>',
  back: '<path d="M5.5 3.5l-3 3 3 3"/><path d="M3 6.5h6a3.5 3.5 0 0 1 0 7H7"/>',
  table: '<rect x="2.5" y="2.5" width="11" height="11" rx="1"/><path d="M2.5 6.5h11M2.5 10h11M6.5 2.5v11"/>',
  menu: '<path d="M3 4.5h10M3 8h10M3 11.5h10"/>',
  list: '<path d="M5.5 4h8M5.5 8h8M5.5 12h8"/><path d="M2.5 4h.01M2.5 8h.01M2.5 12h.01" stroke-width="2"/>',
  search: '<circle cx="7" cy="7" r="4.5"/><path d="M10.5 10.5L14 14"/>',
  open: '<path d="M9 3h4v4M13 3L7.5 8.5"/><path d="M11 9.5V13H3V5h3.5"/>',
  unfold: '<path d="M4.5 6L8 3l3.5 3M4.5 10L8 13l3.5-3"/>',
  fold: '<path d="M4.5 3L8 6l3.5-3M4.5 13L8 10l3.5 3"/>',
  help: '<circle cx="8" cy="8" r="6.5"/><path d="M6.2 6.3a1.9 1.9 0 1 1 2.6 1.8c-.5.3-.8.6-.8 1.3"/><path d="M8 11.6h.01" stroke-width="2"/>',
  keys: '<rect x="1.5" y="4" width="13" height="8.5" rx="1.5"/><path d="M5 10h6"/><path d="M4.3 7h.01M6.8 7h.01M9.2 7h.01M11.7 7h.01" stroke-width="2"/>',
  clock: '<circle cx="8" cy="8" r="6.5"/><path d="M8 4.5V8l2.3 1.5"/>',
}
</script>

<template>
  <svg class="icon" viewBox="0 0 16 16" width="1em" height="1em" fill="none" stroke="currentColor" stroke-width="1.5"
       stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" v-html="PATHS[name]" />
</template>

<style>
.icon { flex-shrink: 0; vertical-align: -.125em; }
</style>
