<script setup>
import { vocab } from '../catalog.js'
import PropsList from './PropsList.vue'

// the field's proposed properties, read as FieldCard reads them (its own PropsList). `data` — the reference node's `field`
defineProps({ data: Object })
</script>

<template>
  <PropsList :props="data" :specs="vocab.field"><span class="text-secondary">Властивості поля не названо.</span></PropsList>
</template>
