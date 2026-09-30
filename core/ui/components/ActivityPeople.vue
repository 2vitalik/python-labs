<script setup>
import { computed, ref, watch } from 'vue'

import { PERIODS, ago, online, usePolling } from '../activity.js'
import { getActivityPeople } from '../api.js'
import Avatar from './Avatar.vue'
import Spark from './Spark.vue'

// who showed up and how much they do: the latest first, counts over the chosen period, a bar per day for two weeks
const props = defineProps({ days: Number, staff: Boolean })
const data = ref(null)
const error = ref('')
const COLS = [['login', '🔑', 'Входи'], ['view', '👁', 'Перегляди сторінок'], ['edit', '✏️', 'Зміни даних'],
              ['tg', '💬', 'Повідомлення, реакції, вступи в Telegram'], ['vote', '🗳', 'Голоси в опитуваннях'], ['api', '⚙️', 'API-виклики']]
const max = computed(() => Math.max(1, ...data.value.rows.flatMap((p) => p.days)))
const tiles = computed(() => {
  const t = data.value.total
  return [['Студентів', t.students], ['Заходили', t.seen, t.students], ['Привʼязали бота', t.linked, t.students],
          ['Зараз на сайті', data.value.rows.filter((p) => online(p.last)).length]]
})

async function load() {
  try {
    data.value = await getActivityPeople({ days: props.days, staff: props.staff })
    error.value = ''
  } catch (e) {
    error.value = e.message
  }
}
watch(() => [props.days, props.staff], load, { immediate: true })
usePolling(load, 60)
</script>

<template>
  <div v-if="error" class="alert alert-danger">{{ error }}</div>
  <template v-if="data">
    <div class="d-flex flex-wrap gap-2 mb-3">
      <div v-for="[label, n, of] in tiles" :key="label" class="tile border rounded px-3 py-2">
        <div class="small text-secondary">{{ label }}</div>
        <div class="fs-4 fw-semibold lh-sm">{{ n }} <span v-if="of" class="fs-6 fw-normal text-secondary">з {{ of }}</span></div>
      </div>
    </div>
    <div class="d-flex align-items-center gap-2 mb-2">
      <span class="small text-secondary">Лічильники за:</span>
      <div class="btn-group btn-group-sm">
        <RouterLink v-for="[n, text] in PERIODS" :key="n" :to="{ query: { ...$route.query, days: n === 7 ? undefined : n } }" replace
                    class="btn" :class="n === days ? 'btn-primary' : 'btn-outline-secondary'">{{ text }}</RouterLink>
      </div>
    </div>
    <table class="table table-sm align-middle">
      <thead>
        <tr>
          <th>Хто</th><th>Востаннє</th>
          <th title="Дій за день: входи, перегляди, зміни, Telegram. Висота — корінь від кількості, шкала спільна для всіх">14 днів</th>
          <th v-for="[key, icon, title] in COLS" :key="key" class="text-end" :title="title">{{ icon }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="p in data.rows" :key="p.nick" :class="{ 'table-info': p.status === 'admin', 'table-warning': p.status === 'pending' }">
          <td>
            <div class="d-flex align-items-center gap-2">
              <Avatar :user="p" :size="24" />
              <div>
                <RouterLink :to="{ query: { user: p.nick } }" class="name">{{ p.name || p.nick }}</RouterLink>
                <span v-if="!p.tg_linked" title="Бот не привʼязаний"> 🚫</span>
                <div class="small text-body-tertiary lh-1">{{ p.group }}</div>
              </div>
            </div>
          </td>
          <td class="text-nowrap"><span v-if="online(p.last)" class="dot" title="Зараз на сайті"></span>{{ ago(p.last) }}</td>
          <td><Spark :values="p.days" :days="data.spark" :max /></td>
          <td v-for="[key] in COLS" :key="key" class="text-end num">{{ p.n[key] || '' }}</td>
        </tr>
      </tbody>
    </table>
    <p v-if="!data.rows.length" class="text-secondary text-center mt-4">Ще ніхто не заходив.</p>
  </template>
</template>

<style scoped>
.tile { min-width: 8.5rem; }
.name { color: inherit; text-decoration: none; }
.name:hover { text-decoration: underline; }
.num { font-variant-numeric: tabular-nums; }
.dot { display: inline-block; width: .5rem; height: .5rem; border-radius: 50%; background: var(--bs-success); margin-right: .35rem; }
</style>
