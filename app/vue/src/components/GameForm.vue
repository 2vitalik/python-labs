<script setup>
import { AXES, KLASSES, STATUSES } from '../catalog.js'

const form = defineModel({ type: Object })
defineEmits(['save'])
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
          <div class="col-md-4">
            <label class="form-label">Slug</label>
            <input v-model="form.slug" class="form-control font-monospace" required>
          </div>
          <div class="col-md-3">
            <label class="form-label">Іконка</label>
            <input v-model="form.icon" class="form-control" placeholder="емодзі">
          </div>
          <div class="col-md-4">
            <label class="form-label">Клас</label>
            <select v-model="form.klass" class="form-select">
              <option value="">—</option>
              <option v-for="(label, k) in KLASSES" :key="k" :value="k">{{ label }}</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Статус</label>
            <select v-model="form.status" class="form-select">
              <option v-for="(label, k) in STATUSES" :key="k" :value="k">{{ label }}</option>
            </select>
          </div>
          <div class="col-md-4">
            <label class="form-label">Порядок</label>
            <input v-model.number="form.order" type="number" class="form-control">
          </div>
        </div>
        <div class="form-text mt-2">Slug — стабільне EN-імʼя для URL і знімка; чернетки бачить лише викладач.</div>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Осі опису</div>
      <div class="card-body">
        <div class="row g-3">
          <div v-for="(label, k) in AXES" :key="k" class="col-md-4">
            <label class="form-label">{{ label }}</label>
            <input :value="form.axes[k] || ''" class="form-control" @input="form.axes[k] = $event.target.value">
          </div>
        </div>
        <div class="form-text mt-2">Вільні підписи; порожнє — вісь не показується.</div>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Опис</div>
      <div class="card-body">
        <label class="form-label">Один рядок суті (для картки в галереї)</label>
        <input v-model="form.summary" class="form-control mb-3">
        <label class="form-label">Повний опис (markdown)</label>
        <textarea v-model="form.description" class="form-control font-monospace" rows="14"></textarea>
      </div>
    </div>

    <button class="btn btn-primary">Зберегти</button>
  </form>
</template>
