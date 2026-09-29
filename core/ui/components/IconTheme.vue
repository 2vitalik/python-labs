<script setup>
// sun or moon — the theme is pinned; half-filled circle with «A» — automatic, as on the device
// (the letter is from the flash of a phone camera). All three are of one width: the menu fit is computed from widths
defineProps({ mode: String })
</script>

<template>
  <svg width="22" height="16" viewBox="0 0 22 16" fill="none" stroke="currentColor" stroke-width="1.5"
       stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
    <template v-if="mode === 'auto'">
      <circle cx="8" cy="8" r="6" />
      <path d="M8 2a6 6 0 0 1 0 12z" fill="currentColor" />
      <text x="15.5" y="7" font-size="9" font-weight="700" fill="currentColor" stroke="none">A</text>
    </template>
    <g v-else transform="translate(3)">
      <path v-if="mode === 'dark'" d="M14 8.53A6 6 0 1 1 7.47 2 4.67 4.67 0 0 0 14 8.53z" />
      <template v-else>
        <circle cx="8" cy="8" r="3" />
        <path d="M8 1v1.5M8 13.5V15M1 8h1.5M13.5 8H15M3.05 3.05l1.06 1.06M11.89 11.89l1.06 1.06M3.05 12.95l1.06-1.06M11.89 4.11l1.06-1.06" />
      </template>
    </g>
  </svg>
</template>
