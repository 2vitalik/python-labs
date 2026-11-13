<script setup>
// the key to how a rule's words look (T270 §4.1, T281): each sample wears the very classes Pieces.vue gives the real thing
</script>

<template>
  <div class="rlegend">
    <span><span class="pc ent">👾 сутність</span> мишка — її картка</span>
    <span><span class="pc state">стан</span></span>
    <span><span class="pc num">20</span> число</span>
    <span><span class="pc choice">варіант</span> зі словника</span>
    <span><span class="pc name">лічильник</span></span>
    <span><span class="pc free">свої слова</span></span>
    <span><span class="pc letter sd-a">А</span> <span class="pc letter sd-b">Б</span> сторони КОЛИ</span>
  </div>
</template>

<style scoped>
.rlegend { display: flex; flex-wrap: wrap; align-items: center; gap: .2rem 1rem; margin-top: .6rem; padding-top: .4rem; border-top: 1px dashed var(--bs-border-color);
           font-size: .7rem; color: var(--bs-secondary-color); }
.rlegend .pc { color: var(--bs-body-color); }
.rlegend .pc.choice { color: var(--pc-choice); }
.rlegend .pc.letter { color: var(--side-ink); }
</style>
