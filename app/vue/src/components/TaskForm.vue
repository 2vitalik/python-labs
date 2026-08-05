<script setup>
import { computed } from 'vue'

import { COIN_NAMES, COINS, STATUSES, zones } from '../catalog.js'

const form = defineModel({ type: Object })
defineEmits(['save'])

const subzones = computed(() => zones.value[form.value.zone]?.subzones || {})
</script>

<template>
  <form @submit.prevent="$emit('save')">
    <div class="card mb-3">
      <div class="card-header">Основне</div>
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-5">
            <label class="form-label">Назва</label>
            <input v-model="form.title" class="form-control" required>
          </div>
          <div class="col-md-3">
            <label class="form-label">Slug</label>
            <input v-model="form.slug" class="form-control font-monospace" required>
          </div>
          <div class="col-md-2">
            <label class="form-label">Статус</label>
            <select v-model="form.status" class="form-select">
              <option v-for="(label, k) in STATUSES" :key="k" :value="k">{{ label }}</option>
            </select>
          </div>
          <div class="col-md-2">
            <label class="form-label">Порядок</label>
            <input v-model.number="form.order" type="number" class="form-control">
          </div>
          <div class="col-md-4">
            <label class="form-label">Зона</label>
            <select v-model="form.zone" class="form-select" required @change="form.subzone = ''">
              <option v-for="(z, k) in zones" :key="k" :value="k">{{ z.title }}</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Підзона</label>
            <select v-model="form.subzone" class="form-select" required>
              <option v-for="(label, k) in subzones" :key="k" :value="k">{{ label }}</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Ігри (slug через кому)</label>
            <input v-model="form.games" class="form-control font-monospace" placeholder="порожнє = універсальне">
          </div>
        </div>
        <label class="form-label mt-3">Опис (markdown): що зробити і що я перевіряю</label>
        <textarea v-model="form.description" class="form-control" rows="4"></textarea>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Ціна і повторюваність</div>
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Монетка</label>
            <select v-model="form.coin" class="form-select">
              <option value="">—</option>
              <option v-for="(e, k) in COINS" :key="k" :value="k">{{ e }} {{ COIN_NAMES[k] }}</option>
            </select>
          </div>
          <div class="col-md-3">
            <label class="form-label">Кількість</label>
            <input v-model.number="form.amount" type="number" step="0.5" min="0" class="form-control">
          </div>
          <div class="col-md-3">
            <label class="form-label">Макс. зарахувань</label>
            <input v-model.number="form.max_count" type="number" min="0" class="form-control">
          </div>
          <div class="col-md-2">
            <label class="form-label">Теги</label>
            <input v-model="form.tags" class="form-control font-monospace" placeholder="algo, …">
          </div>
        </div>
        <div class="form-text mt-2">Макс. зарахувань: 1 — одноразове · N — стільки разів · 0 — без ліміту (кожен рівень окремо).</div>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Варіанти (сімʼя)</div>
      <div class="card-body">
        <div v-for="(v, i) in form.variants" :key="i" class="row g-2 mb-2">
          <div class="col-md-3"><input v-model="v.slug" class="form-control form-control-sm font-monospace" placeholder="slug"></div>
          <div class="col-md-5"><input v-model="v.title" class="form-control form-control-sm" placeholder="назва варіанта"></div>
          <div class="col-md-2">
            <select v-model="v.coin" class="form-select form-select-sm">
              <option value="">—</option>
              <option v-for="(e, k) in COINS" :key="k" :value="k">{{ e }}</option>
            </select>
          </div>
          <div class="col-md-1"><input v-model.number="v.amount" type="number" step="0.5" min="0" class="form-control form-control-sm"></div>
          <div class="col-md-1"><button type="button" class="btn btn-sm btn-outline-danger" @click="form.variants.splice(i, 1)">✕</button></div>
        </div>
        <button type="button" class="btn btn-outline-secondary btn-sm"
                @click="form.variants.push({ slug: '', title: '', coin: '', amount: 1 })">➕ Варіант</button>
        <div class="form-text mt-2">Порожньо — просте завдання. Перший варіант — базовий; його ціну дублюй у картці.</div>
      </div>
    </div>

    <button class="btn btn-primary">Зберегти</button>
  </form>
</template>
