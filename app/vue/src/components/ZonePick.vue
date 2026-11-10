<script setup>
import { zones } from '../catalog.js'

// category and subcategory as two optional selects; the second lists the chosen category's subcategories
const zone = defineModel('zone', { type: String, default: '' })
const subzone = defineModel('subzone', { type: String, default: '' })
defineProps({ small: Boolean })
const pickZone = (z) => { zone.value = z; subzone.value = '' }
</script>

<template>
  <div class="d-flex flex-wrap gap-2">
    <select :value="zone" class="form-select w-auto mw-100" :class="{ 'form-select-sm': small }" @change="pickZone($event.target.value)">
      <option value="">категорія — за бажанням</option>
      <option v-for="(z, k) in zones" :key="k" :value="k">{{ z.icon }} {{ z.title }}</option>
    </select>
    <select v-if="zones[zone]" v-model="subzone" class="form-select w-auto mw-100" :class="{ 'form-select-sm': small }">
      <option value="">підкатегорія — за бажанням</option>
      <option v-for="([title, icon], k) in zones[zone].subzones" :key="k" :value="k">{{ icon }} {{ title }}</option>
    </select>
  </div>
</template>
