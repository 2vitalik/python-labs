<script setup>
import { computed } from 'vue'

import { LIMITS, chars, optionLabel, review } from '../polls.js'
import GrowArea from './GrowArea.vue'
import TagInput from './TagInput.vue'

// the question and its answers — a line each, emoji first, so a list can be pasted in one go — with a preview as Telegram
// will show it; `frozen`: the poll is in Telegram already, only the title and the tags can change; `template` — the form of a template
const form = defineModel({ type: Object, required: true })
defineProps({ known: { type: Array, default: () => [] }, frozen: Boolean, template: Boolean })
const r = computed(() => review(form.value))
const rows = computed(() => Math.max(3, form.value.lines.split('\n').length + 1))
const over = (n, max) => (n > max ? 'text-danger fw-semibold' : 'text-body-tertiary')
</script>

<template>
  <div class="vstack gap-3">
    <div>
      <label class="form-label fw-semibold" for="poll-question">Питання</label>
      <GrowArea id="poll-question" v-model="form.question" class="form-control" :disabled="frozen" placeholder="Хто сьогодні на парі?" />
      <div class="small text-end" :class="over(chars(form.question), LIMITS.question)">{{ chars(form.question) }} / {{ LIMITS.question }}</div>
    </div>

    <div class="row g-3">
      <div class="col-md-6">
        <label class="form-label fw-semibold" for="poll-lines">Варіанти <span class="fw-normal text-secondary small">— кожен з нового рядка, емодзі на початку</span></label>
        <textarea id="poll-lines" v-model="form.lines" class="form-control" :rows :disabled="frozen" :placeholder="'✅ так\n🤒 хворію\n❌ ні'"></textarea>
        <div class="small text-body-tertiary mt-1">{{ r.options.length }} з {{ LIMITS.most }} · до {{ LIMITS.option }} символів у варіанті</div>
      </div>
      <div class="col-md-6">
        <div class="form-label fw-semibold">Як побачать у Telegram</div>
        <div class="preview border rounded p-3">
          <div class="fw-semibold text-break">{{ form.question.trim() || 'Питання' }}</div>
          <div class="small text-secondary mb-2">Публічне опитування · {{ form.multiple ? 'кілька відповідей' : 'одна відповідь' }}</div>
          <div v-for="(o, i) in r.options" :key="i" class="d-flex gap-2 py-1 text-break">
            <span class="dot" :class="{ square: form.multiple }"></span><span :class="{ 'text-danger': chars(optionLabel(o)) > LIMITS.option }">{{ optionLabel(o) }}</span>
          </div>
          <div v-if="!r.options.length" class="small text-body-tertiary">Варіанти зʼявляться тут</div>
          <div v-if="r.options.length" class="small text-secondary border-top mt-2 pt-2">
            У таблиці: <span v-for="(o, i) in r.options" :key="i" class="me-2" :title="optionLabel(o)">{{ o.emoji || i + 1 }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="row g-3 align-items-start">
      <div class="col-md-5">
        <label class="form-label fw-semibold" for="poll-title">{{ template ? 'Назва шаблону' : 'Заголовок' }}</label>
        <input id="poll-title" v-model="form.title" class="form-control" :placeholder="template ? 'Хто на парі' : 'Пара 01.10'">
        <div class="form-text">{{ template ? 'Нове опитування отримає її з датою: «Хто на парі 01.10»' : 'Назва колонки в таблиці; порожній — початок питання' }}</div>
      </div>
      <div class="col-md-7">
        <div class="form-label fw-semibold">Теги</div>
        <TagInput v-model="form.tags" :known />
        <div class="form-text">Щоб знаходити й порівнювати: «відвідуваність», «лаба-3»</div>
      </div>
    </div>

    <div class="form-check form-switch">
      <input id="poll-multiple" v-model="form.multiple" class="form-check-input" type="checkbox" :disabled="frozen">
      <label class="form-check-label" for="poll-multiple">Можна обрати кілька варіантів</label>
    </div>

    <div v-if="frozen" class="small text-secondary">🔒 Опитування вже в Telegram — питання й варіанти там не змінити. «Повторити» створить нове з правками.</div>
    <ul v-if="r.errors.length || r.warnings.length" class="list-unstyled small mb-0">
      <li v-for="e in r.errors" :key="e" class="text-danger">❌ {{ e }}</li>
      <li v-for="w in r.warnings" :key="w" class="text-warning-emphasis">☝️ {{ w }}</li>
    </ul>
  </div>
</template>

<style scoped>
.preview { background: var(--bs-tertiary-bg); }
.dot { flex: 0 0 1rem; height: 1rem; margin-top: .2rem; border: 2px solid var(--bs-secondary-color); border-radius: 50%; }
.dot.square { border-radius: .25rem; }
</style>
