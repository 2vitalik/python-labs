<script setup>
import { useTable } from '../tableCtx.js'
import Icon from './Icon.vue'
import SetupWord from './SetupWord.vue'

// a family of like columns on one line of the catalog (T315 §3): the first leads, the others smaller. One's own column has
// a pencil at the end: its form takes the catalog's place
defineProps({ cols: { type: Array, required: true } })
const t = useTable()
</script>

<template>
  <div class="sfam">
    <SetupWord v-for="(c, i) in cols" :key="c.key" :col="c" :small="i > 0" />
    <button v-if="cols[0].own" type="button" class="iact mini ms-auto" :title="`Змінити колонку «${cols[0].name}»`" @click="t.ui.field = cols[0].field">
      <Icon name="pencil" /></button>
  </div>
</template>

<style scoped>
.sfam { display: flex; flex-wrap: wrap; align-items: center; gap: .35rem .35rem; padding: .18rem 0; }
</style>
