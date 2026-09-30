<script setup>
import { STATUS, moment } from '../polls.js'

// the poll itself: its title and state, what can be done with it, and the question as it was asked.
// «Повторити» opens a new poll with the same question; the delete button shows only while nobody but teachers has voted
defineProps({ poll: { type: Object, required: true }, canDelete: Boolean, busy: Boolean })
defineEmits(['template', 'remove'])
</script>

<template>
  <div class="d-flex flex-wrap align-items-center gap-2 mb-1">
    <h1 class="h3 mb-0 text-break">{{ poll.title }}</h1>
    <span class="badge fw-normal" :class="STATUS[poll.status].cls">{{ STATUS[poll.status].icon }} {{ STATUS[poll.status].text }}</span>
    <div class="ms-auto d-flex flex-wrap gap-1">
      <RouterLink :to="`/polls/${poll.id}/edit`" class="btn btn-outline-secondary btn-sm" title="Редагувати">✏️</RouterLink>
      <RouterLink :to="`/polls/new?from=${poll.id}`" class="btn btn-outline-secondary btn-sm" title="Нове опитування з тим самим питанням">🔁 Повторити</RouterLink>
      <button type="button" class="btn btn-outline-secondary btn-sm" :disabled="busy" title="Зберегти питання й варіанти як шаблон"
              @click="$emit('template')">📋 У шаблони</button>
      <button v-if="canDelete" type="button" class="btn btn-outline-danger btn-sm" :disabled="busy" title="Видалити" @click="$emit('remove')">🗑</button>
    </div>
  </div>
  <div class="small text-secondary mb-3 d-flex flex-wrap column-gap-2">
    <span v-for="t in poll.tags" :key="t"><RouterLink :to="`/polls?tag=${encodeURIComponent(t)}`" class="text-secondary">#{{ t }}</RouterLink></span>
    <span>створив {{ poll.by }} · {{ moment(poll.created_at) }}</span>
    <span v-if="poll.sent_at">· надіслано {{ moment(poll.sent_at) }}</span>
    <span v-if="poll.closed_at">· закрито {{ moment(poll.closed_at) }}</span>
  </div>
  <div class="card card-body mb-3">
    <div class="fw-semibold text-break">{{ poll.question }}</div>
    <div class="small text-secondary">{{ poll.multiple ? 'можна обрати кілька варіантів' : 'один варіант' }}</div>
  </div>
</template>
