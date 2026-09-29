<script setup>
import { usePolling } from '../activity.js'
import { getMe } from '../api.js'
import { user } from '../user.js'

const reload = () => location.reload()
// the API does not answer (http.js `down`); a deploy restarts it in seconds, so the page keeps knocking.
// Whoever was signed in goes on with the open page, the rest start over: the guard has not seen who they are
usePolling(() => getMe().then(() => user.value || reload(), () => {}), 5)
</script>

<template>
  <div class="alert alert-warning d-flex flex-wrap align-items-center gap-2 mb-4">
    <div class="me-auto">
      <b>⚠️ Сайт тимчасово недоступний</b>
      <div class="small">Сервер не відповідає. Сторінка оживе сама, щойно він повернеться.</div>
    </div>
    <button class="btn btn-outline-secondary btn-sm" @click="reload">Оновити</button>
  </div>
</template>
