<script setup>
import { isMore, toggleMore } from '../coreMode.js'
import { useCardsMode } from '../taskFilter.js'

// the quiet row at the end of a subcategory or a family under «Основа» (T319): how many cards «за запитом» wait here;
// a click shows them in place, among the others, and the row turns to hide them back. `scope` — `zone/sub` or a family's slug
defineProps({ scope: String, n: Number })
const { s } = useCardsMode()
</script>

<template>
  <button v-if="n" type="button" class="more-asked" @click.stop="toggleMore(s, scope)"
          title="Картки за запитом: додати можна з одним реченням — що саме у твоїй грі це робить; монетка — коли викладач відкриє картку">
    {{ isMore(s, scope) ? `сховати ${n} за запитом` : `＋ ще ${n} за запитом` }}
  </button>
</template>

<style scoped>
.more-asked { display: block; width: 100%; padding: .15rem .5rem; border: 1px dashed var(--bs-border-color); border-radius: .3rem;
              background: none; color: var(--bs-secondary-color); font-size: .78rem; text-align: start; }
.more-asked:hover { border-color: var(--bs-secondary-color); color: var(--bs-body-color); }
</style>
