<script setup>
import { computed, ref } from 'vue'

import { vHint } from '@core/hint.js'
import { fmtWhen } from '@core/labs.js'

import IntakeRow from './IntakeRow.vue'
import IntakeWho from './IntakeWho.vue'

// one person's talk as forwarded (T368 §2.7): who it is on Telegram → whose on the site, then the lines oldest first.
// `seen` — the rows the filters took; «уся розмова» in the head shows the rest. Every action answers with the whole
// INTAKE (`got`); while it runs the card's buttons are grey, its error takes the card's last line, kept for it
const props = defineProps({ p: Object, seen: Set })
const emit = defineEmits(['got'])
const all = ref(false)
const busy = ref(false)
const error = ref('')
const taken = computed(() => props.p.rows.filter((r) => props.seen.has(r.id)))
const rows = computed(() => (all.value ? props.p.rows : taken.value))
const rest = computed(() => props.p.rows.length - taken.value.length)

async function run(job) {
  busy.value = true
  error.value = ''
  try {
    emit('got', await job())
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <article class="card person">
    <div class="card-body">
      <header class="head">
        <b class="text-break">{{ p.name || 'без імені' }}</b>
        <a v-if="p.username" :href="`https://t.me/${p.username}`" target="_blank" rel="noopener" class="nick">@{{ p.username }}</a>
        <span v-else-if="!p.tg_id" v-hint="'Telegram ховає цей акаунт за пересиланням: видно лише імʼя'" class="nick">акаунт сховано</span>
        <span class="end">
          <button v-if="rest" type="button" class="dot" @click="all = !all">{{ all ? 'лише відібрані' : `уся розмова · ще ${rest}` }}</button>
          <span v-hint="'останнє повідомлення'">{{ fmtWhen(p.last) }}</span>
        </span>
      </header>
      <IntakeWho :p :busy @act="run" />
      <ul class="list-unstyled mb-0 mt-1">
        <IntakeRow v-for="r in rows" :key="r.id" :r :student="!!p.student" :busy @act="run" />
      </ul>
      <p v-hint="error.length > 60 ? error : ''" class="say" role="status">{{ error }}</p>
    </div>
  </article>
</template>

<style scoped>
.person .card-body { padding: .6rem .9rem .1rem; }
.head { display: flex; flex-wrap: wrap; align-items: baseline; column-gap: .5rem; }
.nick { color: var(--bs-secondary-color); font-size: .85rem; text-decoration: none; }
a.nick:hover { color: var(--bs-body-color); }
.end { display: flex; gap: .75rem; margin-left: auto; color: var(--bs-secondary-color); font-size: .78rem; white-space: nowrap; }
.end .dot { min-width: 8rem; text-align: right; }  /* its two words differ in length: the click stays under the mouse */
.say { height: 1.3rem; margin: 0; overflow: hidden; color: var(--bs-danger-text-emphasis); font-size: .78rem; line-height: 1.3rem;
       text-overflow: ellipsis; white-space: nowrap; }
</style>
