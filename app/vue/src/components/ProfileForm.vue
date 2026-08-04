<script setup>
defineProps({ hints: Boolean, admin: Boolean })
defineEmits(['save'])
const form = defineModel({ type: Object, required: true })
</script>

<template>
  <form @submit.prevent="$emit('save')">
    <div class="card mb-3">
      <div class="card-header">ПІБ</div>
      <div class="card-body">
        <div class="row g-3">
          <div class="col-md-4">
            <label class="form-label">Прізвище</label>
            <input v-model="form.last_name" class="form-control" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">Імʼя</label>
            <input v-model="form.first_name" class="form-control" required>
          </div>
          <div class="col-md-4">
            <label class="form-label">По батькові</label>
            <input v-model="form.patronymic" class="form-control">
          </div>
        </div>
        <div v-if="hints" class="form-text mt-2">Українською, як у заліковці.</div>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">GitHub</div>
      <div class="card-body">
        <label class="form-label">Посилання на репозиторій</label>
        <input v-model="form.github" class="form-control" type="url"
               placeholder="https://github.com/username/python-labs">
        <div v-if="hints" class="form-text mt-2">
          <ul class="mb-0 ps-3">
            <li>Репозиторій має бути <b>приватним</b>.</li>
            <li><b>Єдиний</b> на всі лаби — це один великий проєкт, без папок Lab1/Lab2.</li>
            <li>Розшар його на викладача: Settings → Collaborators → <code>2vitalik</code>.</li>
          </ul>
        </div>
      </div>
    </div>

    <div class="card mb-3">
      <div class="card-header">Telegram</div>
      <div class="card-body">
        <label class="form-label">Нікнейм</label>
        <div class="input-group">
          <span class="input-group-text">@</span>
          <input v-model="form.tg_username" class="form-control" placeholder="username">
        </div>
        <div v-if="hints" class="form-text mt-2">
          Свій нік дивись у Telegram: Налаштування → Імʼя користувача (username). Якщо ніка ще нема — створи там само.
        </div>
        <slot name="telegram" />
      </div>
    </div>

    <div v-if="admin" class="card mb-3">
      <div class="card-header">Адмінське</div>
      <div class="card-body row g-3">
        <div class="col-md-6">
          <label class="form-label">Група</label>
          <input v-model="form.group" class="form-control" placeholder="ПЗПІ-25-1">
        </div>
        <div class="col-md-6">
          <label class="form-label">Статус</label>
          <select v-model="form.status" class="form-select">
            <option value="pending">pending</option>
            <option value="student">student</option>
            <option value="admin">admin</option>
          </select>
        </div>
      </div>
    </div>

    <button class="btn btn-primary">Зберегти</button>
  </form>
</template>
