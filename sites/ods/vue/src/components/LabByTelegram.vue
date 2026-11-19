<script setup>
import { fmtWhen } from '@core/labs.js'

// «Здати» of a lab handed in by Telegram (lab_gates.py): no file goes through the site — the teacher brings the files
// over, each with the time of the student's message
defineProps({ lab: Object })
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Здати</h2>
    <p v-if="lab.due" class="small text-secondary mb-2">Дедлайн {{ fmtWhen(lab.due) }}</p>
    <p class="mb-1">Цю лабу здаємо, як і раніше: файл ноутбука — викладачеві в особисті повідомлення Telegram.</p>
    <p class="small text-secondary mb-0">Час здачі — час твого повідомлення. Викладач перенесе файл сюди, і нижче зʼявиться «Що бачить сайт».</p>
  </section>
</template>
