<script setup>
import { subStyle } from '../catalog.js'

defineProps({ zones: Object, counts: Object, zone: String, sub: String })
defineEmits(['select'])
</script>

<template>
  <nav class="mb-3">
    <div class="d-flex flex-wrap gap-2">
      <button type="button" class="btn btn-sm zone-btn" :class="{ active: !zone }"
              @click="$emit('select', '', '')">
        Всі <span class="count">{{ counts[''] || 0 }}</span>
      </button>
      <button v-for="(z, zk) in zones" :key="zk" type="button" class="btn btn-sm zone-btn"
              :style="{ '--zc': z.color }" :class="{ active: zone === zk, 'opacity-50': !counts[zk] }"
              @click="$emit('select', zone === zk ? '' : zk, '')">
        {{ z.icon }} {{ z.title }} <span class="count">{{ counts[zk] || 0 }}</span>
      </button>
    </div>
    <div v-if="zone" class="d-flex flex-wrap gap-1 mt-2">
      <button v-for="([st, si], sk, i) in zones[zone].subzones" :key="sk" type="button"
              class="btn btn-sm sub-btn" :style="subStyle(zones[zone].color, i)"
              :class="{ active: sub === sk, 'opacity-50': !counts[`${zone}/${sk}`] }"
              @click="$emit('select', zone, sub === sk ? '' : sk)">
        {{ si }} {{ st }} <span class="count">{{ counts[`${zone}/${sk}`] || 0 }}</span>
      </button>
    </div>
  </nav>
</template>

<style scoped>
.zone-btn {
  --zc: #6c757d;
  font-weight: 600; color: var(--zc);
  background: color-mix(in srgb, var(--zc) 8%, #fff);
  border: 1px solid color-mix(in srgb, var(--zc) 40%, #fff);
}
.zone-btn.active { color: #fff; background: var(--zc); border-color: var(--zc); }
.sub-btn {
  color: var(--sc); background: var(--st);
  border: 1px solid color-mix(in srgb, var(--sc) 35%, #fff);
}
.sub-btn.active { color: #fff; background: var(--sc); border-color: var(--sc); }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
