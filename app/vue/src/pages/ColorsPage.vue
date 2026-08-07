<script setup>
import { ref } from 'vue'

// palette workshop: pick zone base colors and a subzone-variation principle by code (e.g. "G h2")
const FAMILIES = [
  { code: 'R', name: 'червоний', h: 4 }, { code: 'O', name: 'помаранчевий', h: 27 },
  { code: 'Y', name: 'бурштиновий', h: 42 }, { code: 'G', name: 'зелений', h: 130 },
  { code: 'T', name: 'бірюзовий', h: 174 }, { code: 'C', name: 'блакитний', h: 200 },
  { code: 'B', name: 'синій', h: 226 }, { code: 'V', name: 'фіолетовий', h: 275 },
  { code: 'M', name: 'малиновий', h: 335 },
]
// three variation principles inside one family (what subzones could use)
const PRINCIPLES = [
  { key: 'h', name: 'сусідні хʼю (відтінок повзе по колу)', make: (h, i) => `hsl(${(h + (i - 3) * 12 + 360) % 360} 62% 44%)` },
  { key: 'l', name: 'яскравість (той самий тон, темніше→світліше)', make: (h, i) => `hsl(${h} 62% ${26 + i * 7}%)` },
  { key: 's', name: 'насиченість (соковитий→приглушений)', make: (h, i) => `hsl(${h} ${92 - i * 12}% 44%)` },
]
const STEPS = [0, 1, 2, 3, 4, 5, 6]
// ready-made 6-zone combos to say "беремо К2"
const COMBOS = [
  { code: 'К1', note: 'поточна', items: ['G', 'V', 'O', 'C', 'B', 'M'] },
  { code: 'К2', note: 'тепло/холод через один', items: ['O', 'T', 'M', 'B', 'Y', 'V'] },
  { code: 'К3', note: 'без синьої пари, максимальний розліт', items: ['G', 'B', 'Y', 'M', 'T', 'V'] },
]
const base = (f) => `hsl(${f.h} 62% 44%)`
const copied = ref('')
const copy = (label, css) => { navigator.clipboard?.writeText(css); copied.value = label }
</script>

<template>
  <h1 class="h3">Кольори <span class="text-secondary fs-6">майстерня палітри зон і підзон</span></h1>
  <p class="text-secondary">Клік по плитці копіює css-значення. У відповідях достатньо коду: сімейство — буква (<b>G</b>),
    варіація — буква+номер (<b>G h2</b>), готовий набір — <b>К2</b>. {{ copied ? `Скопійовано: ${copied}` : '' }}</p>
  <p class="small text-secondary">Конкретна пропозиція розкладки зон/підзон — на <RouterLink to="/colors2">/colors2</RouterLink>.</p>

  <h2 class="h5 mt-4">Готові набори для 6 зон</h2>
  <div v-for="c in COMBOS" :key="c.code" class="d-flex align-items-center gap-2 mb-2">
    <b class="combo-code">{{ c.code }}</b>
    <div v-for="f in c.items" :key="f" class="swatch lg" :style="{ background: base(FAMILIES.find((x) => x.code === f)) }"
         role="button" :title="f" @click="copy(`${c.code}/${f}`, base(FAMILIES.find((x) => x.code === f)))">{{ f }}</div>
    <span class="text-secondary small">{{ c.note }}</span>
  </div>

  <h2 class="h5 mt-4">Сімейства і принципи варіацій підзон</h2>
  <div v-for="f in FAMILIES" :key="f.code" class="mb-3">
    <div class="d-flex align-items-center gap-2 mb-1">
      <div class="swatch lg" :style="{ background: base(f) }" role="button" @click="copy(f.code, base(f))">{{ f.code }}</div>
      <b>{{ f.name }}</b> <span class="text-secondary small">база: hue {{ f.h }}°</span>
    </div>
    <div v-for="p in PRINCIPLES" :key="p.key" class="d-flex align-items-center gap-1 mb-1 ms-4">
      <div v-for="i in STEPS" :key="i" class="swatch" :style="{ background: p.make(f.h, i) }"
           role="button" :title="p.make(f.h, i)" @click="copy(`${f.code} ${p.key}${i}`, p.make(f.h, i))">{{ p.key }}{{ i }}</div>
      <span class="text-secondary small ms-2">{{ p.name }}</span>
    </div>
  </div>
</template>

<style scoped>
.swatch {
  width: 3.2rem; height: 2rem; border-radius: .3rem; color: #fff; font-size: .7rem;
  display: flex; align-items: center; justify-content: center; user-select: none;
}
.swatch.lg { width: 3.6rem; height: 2.4rem; font-weight: 700; }
.combo-code { width: 2rem; }
</style>
