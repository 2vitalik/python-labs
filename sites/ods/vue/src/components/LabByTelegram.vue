<script setup>
import LabDue from './LabDue.vue'

// «Здати» of a lab handed in by Telegram (lab_gates.py): no file goes through the site — the teacher brings the files
// over, each with the time of the student's message. «Після дедлайну» shows once a file is here: before that the site
// cannot know when it was sent
defineProps({ lab: Object })
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Здати</h2>
    <p v-if="lab.due" class="small text-secondary mb-2"><LabDue :lab :quiet="!lab.file?.id" /></p>
    <p class="mb-1">Цю лабу здаємо, як і раніше: файл ноутбука — викладачеві в особисті повідомлення Telegram.</p>
    <p v-if="lab.file?.id" class="small text-secondary mb-0">Твій файл уже тут, із часом твого повідомлення, — нижче «Що бачить сайт». Нову версію теж надсилай викладачеві.</p>
    <p v-else class="small text-secondary mb-0">Час здачі — час твого повідомлення. Викладач перенесе файл сюди, і нижче зʼявиться «Що бачить сайт».</p>
  </section>
</template>
