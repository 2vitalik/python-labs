<script setup>
import { fmtWhen } from '@core/labs.js'

// a lab's deadline against what is handed in (lab_my.py `times`): a version that came in time keeps its word when a
// newer one comes after the deadline — that is a redo, not a late hand-in. `quiet` — nothing is here yet and the site
// cannot know when it was sent (a lab the teacher brings the files of): no «late» before a file
defineProps({ lab: Object, quiet: Boolean })
</script>

<template>
  <span v-if="lab.due">Дедлайн {{ fmtWhen(lab.due) }}<template v-if="lab.late && !quiet"> ·
    <span v-if="lab.in_time">є версія, здана вчасно; остання — після дедлайну</span>
    <span v-else class="text-danger">після дедлайну</span></template></span>
</template>
