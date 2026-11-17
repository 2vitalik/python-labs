<script setup>
import Icon from './Icon.vue'

// a choice's answers in rows (FieldForm): «🟢 добре» — the emoji at the start becomes the icon in the cell — a colour each
// from the palette, a minus to drop one. The list is the form's own: the rows change it in place
defineProps({ options: { type: Array, required: true } })
const COLORS = { '': 'без кольору', gray: 'сірий', red: 'червоний', orange: 'помаранчевий', yellow: 'жовтий', green: 'зелений', teal: 'бірюзовий',
                 blue: 'синій', purple: 'фіолетовий', pink: 'рожевий' }
</script>

<template>
  <div>
    <div class="so-cap">Варіанти · емодзі на початку стане значком у клітинці</div>
    <div v-for="(o, i) in options" :key="i" class="d-flex align-items-center gap-1 mb-1">
      <input v-model="o.line" class="form-control form-control-sm" placeholder="🟢 добре" aria-label="Варіант">
      <span class="so-tones">
        <button v-for="(word, c) in COLORS" :key="c" type="button" class="so-tone" :class="[c ? `tone-${c}` : 'tone-none', { on: o.color === c }]" :title="word" @click="o.color = c" />
      </span>
      <button type="button" class="iact mini del" title="Прибрати варіант" @click="options.splice(i, 1)"><Icon name="minus" /></button>
    </div>
    <button type="button" class="btn btn-sm btn-add py-0" @click="options.push({ id: '', line: '', color: '' })"><Icon name="plus" /> варіант</button>
  </div>
</template>

<style scoped>
.so-cap { margin-bottom: .2rem; color: var(--bs-secondary-color); font-size: .72rem; }
.so-tones { display: inline-flex; flex-shrink: 0; gap: .12rem; }
.so-tone { width: .85rem; height: .85rem; padding: 0; border: 1px solid var(--bs-border-color); border-radius: .2rem; }
.so-tone.on { outline: 2px solid var(--bs-body-color); outline-offset: 1px; }
.tone-none { background: transparent; }
</style>
