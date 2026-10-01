<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'

import { getMyWeek, putMyWeek } from '../api.js'
import { useAutosave } from '../autosave.js'
import Crumbs from '../components/Crumbs.vue'
import GrowArea from '../components/GrowArea.vue'
import WeekDone from '../components/WeekDone.vue'
import WeekPaint from '../components/WeekPaint.vue'
import WeekReasons from '../components/WeekReasons.vue'
import WeekTools from '../components/WeekTools.vue'
import { moment } from '../polls.js'
import { user } from '../user.js'
import { DAYS, daysLabel, hm, span } from '../week.js'
import { bare, reds } from '../weekWhy.js'

// a person's usual week (T177): painted on the grid and saved by itself; «Готово» says the week is whole
const frame = ref(null)
const marks = ref([])
const comment = ref('')
const doneAt = ref(null)
const savedAt = ref(null)
const tool = ref('no')
const readout = ref('')
const problem = ref('')
let loaded = false
let pressed = false  // «Готово» goes with the save under way

const range = computed(() => `${DAYS[0]}–${DAYS[frame.value.days - 1]} ${hm(frame.value.from)}–${hm(frame.value.to)}`)
const unexplained = computed(() => reds(bare(marks.value)).map((g) => `${daysLabel(g.map((m) => m.day))} ${span(g[0])}`).join(', '))
const { state, error, touch, flush } = useAutosave(async () => {
  const w = await putMyWeek({ marks: marks.value, comment: comment.value, done: pressed })
  doneAt.value = w.done_at
  savedAt.value = w.updated_at
})
watch([marks, comment], () => loaded && touch())
// what is left to do, said next to the palette: the grid is tall, and the cards under it are out of sight
const todo = computed(() => (unexplained.value ? '❓ Поясни червоні блоки — нижче ↓' : !doneAt.value && marks.value.length ? '✅ Усе позначено? «Готово» — нижче ↓' : ''))
const go = () => document.getElementById(unexplained.value ? 'week-why' : 'week-done').scrollIntoView({ block: 'center' })
async function finish() {
  pressed = true
  await flush()
  pressed = false
}

onMounted(async () => {
  try {
    const w = await getMyWeek()
    ;[marks.value, comment.value, doneAt.value, savedAt.value, frame.value] = [w.marks, w.comment, w.done_at, w.updated_at, w.frame]
    await nextTick()  // what was loaded is not a change to save
    loaded = true
  } catch (e) {
    problem.value = e.message
  }
})
</script>

<template>
  <div>
    <Crumbs :items="user?.status === 'admin' ? [['/week', 'Тиждень потоку'], 'Мій тиждень'] : ['Мій тиждень']" />
    <div class="d-flex flex-wrap align-items-baseline gap-2 mb-2">
      <h1 class="h3 mb-0 me-auto">Мій тиждень</h1>
      <span v-if="state === 'failed'" class="small text-danger">⚠️ не збереглось: {{ error }} · <a href="#" @click.prevent="flush">ще раз</a></span>
      <span v-else-if="state !== 'saved'" class="small text-secondary">⏳ зберігаю…</span>
      <span v-else-if="savedAt" class="small text-secondary">💾 збережено {{ moment(savedAt) }}</span>
    </div>
    <div v-if="problem" class="alert alert-danger">{{ problem }}</div>

    <template v-if="frame">
      <p class="mb-2">Шукаємо час для спільної пари всього потоку — раз на тиждень, {{ range }}.</p>
      <p class="mb-1">Познач свій звичайний тиждень: коли <b>не можеш</b> (і чому), коли <b>незручно</b>, коли <b>найкраще</b>.
        Решта — «можу». Буває по-різному — став «незручно».</p>
      <WeekTools v-model="tool" :readout :todo @go="go" />
      <WeekPaint v-model="marks" :frame :tool class="mb-3" @drag="readout = $event || ''" />
      <WeekReasons id="week-why" v-model="marks" :frame />

      <div class="card mb-3">
        <div class="card-header">Коментар викладачу <span class="small text-secondary">— якщо є що додати</span></div>
        <div class="card-body">
          <GrowArea v-model="comment" class="form-control" maxlength="1000" placeholder="«можу лише онлайн», «у середу після 20:00 — з телефона»…" />
        </div>
      </div>

      <WeekDone id="week-done" :done-at="doneAt" :unexplained :empty="!marks.length" :range :busy="state === 'saving'" @finish="finish" />
    </template>
  </div>
</template>
