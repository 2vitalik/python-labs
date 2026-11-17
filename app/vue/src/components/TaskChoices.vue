<script setup>
import Icon from '@core/components/Icon.vue'

// a short list to pick one from in a panel — a coin, a status: no search, every option in sight, a row each with its sign,
// its name and a line of what it means, the current one ticked; rows drawn as Picker's. items: [{ key, icon?, title, desc? }]
defineProps({ items: Array, current: String })
defineEmits(['pick'])
</script>

<template>
  <div>
    <button v-for="it in items" :key="it.key" type="button" class="pick" @click="$emit('pick', it.key)">
      <span v-if="it.icon" class="ico">{{ it.icon }}</span>
      <span class="body">
        {{ it.title }}<span v-if="it.key === current" class="text-success ms-1" title="зараз"><Icon name="done" /></span>
        <span v-if="it.desc" class="sub">{{ it.desc }}</span>
      </span>
    </button>
  </div>
</template>

<style scoped>
.pick { display: flex; align-items: baseline; gap: .45rem; width: 100%; padding: .22rem .5rem; border: 0; border-radius: .25rem; background: none;
        color: inherit; text-align: start; font-size: .85rem; }
.pick:hover, .pick:focus-visible { background: var(--bs-tertiary-bg); outline: 0; }
.ico { flex-shrink: 0; min-width: 1.25rem; text-align: center; }
.body { flex-grow: 1; min-width: 0; }
.sub { display: block; font-size: .75rem; color: var(--bs-secondary-color); }
</style>
