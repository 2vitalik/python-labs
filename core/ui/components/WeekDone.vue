<script setup>
import { moment } from '../polls.js'

// the end of «Мій тиждень»: «Готово» says the week is whole. It waits for a reason to each «не можу» (`unexplained` names them);
// once pressed it stays pressed, and what is painted later only asks for its reasons. `empty` — nothing is marked at all
defineProps({ doneAt: String, unexplained: String, empty: Boolean, range: String, busy: Boolean })
defineEmits(['finish'])
</script>

<template>
  <div class="card mb-3" :class="{ 'border-success': doneAt && !unexplained }">
    <div class="card-body">
      <template v-if="doneAt">
        <div v-if="unexplained" class="text-danger">⚠️ Поясни нові червоні блоки: {{ unexplained }}</div>
        <template v-else>
          <b>✅ Готово</b> <span class="text-secondary">· {{ moment(doneAt) }}</span>
          <div class="small text-secondary mt-1">Можеш міняти будь-коли — зміни зберігаються самі</div>
        </template>
      </template>
      <template v-else>
        <button type="button" class="btn btn-success" :disabled="!!unexplained || busy" @click="$emit('finish')">✅ Готово — тиждень позначено</button>
        <div class="small mt-2" :class="unexplained ? 'text-danger' : 'text-secondary'">
          <template v-if="unexplained">Спершу поясни червоні блоки: {{ unexplained }}</template>
          <template v-else-if="empty">Жодної позначки — отже, можеш будь-коли {{ range }}? Якщо так — тисни «Готово»</template>
          <template v-else>Перевір тиждень і тисни: викладач побачить, що він готовий</template>
        </div>
      </template>
    </div>
  </div>
</template>
