<script setup>
import { computed } from 'vue'

import { CHATS, COLLS, ICONS, TG_KINDS, clock, device, plain } from '../activity.js'

// one feed row: time · whom it is about · icon of the journal · what happened; `one` — email of a one-person feed, which needs no name column
const props = defineProps({ row: { type: Object, required: true }, people: { type: Object, required: true }, one: String })
const r = computed(() => props.row)
const about = computed(() => r.value.about || r.value.user)  // a profile edit is about its owner, whoever made it
const who = computed(() => props.people[about.value])
const stranger = computed(() => (r.value.username ? `@${r.value.username}` : r.value.from_id || r.value.tg_id ? `tg ${r.value.from_id || r.value.tg_id}` : about.value || '—'))
const name = (email) => props.people[email]?.name || (email === 'tgbot' ? 'бот' : email.split('@')[0])
const icon = computed(() => ICONS[r.value.src] || (r.value.src === 'note' ? (r.value.hidden ? '🙈' : '📝') : r.value.dir === 'out' ? '🤖' : '💬'))
const status = computed(() => (r.value.status >= 500 ? 'text-bg-danger' : r.value.status >= 400 ? 'text-bg-warning' : 'text-bg-light border'))
</script>

<template>
  <div class="arow d-flex gap-2 py-1 border-bottom">
    <span class="time text-secondary">{{ clock(r.at) }}</span>
    <span v-if="!one" class="who text-truncate">
      <RouterLink v-if="who" :to="{ query: { user: who.nick } }" :title="`Лише ${who.name || who.nick}`">{{ who.name || who.nick }}</RouterLink>
      <span v-else class="text-secondary">{{ stranger }}</span>
    </span>
    <span class="icon">{{ icon }}</span>
    <div class="what">
      <template v-if="r.src === 'login'">вхід <small class="text-secondary">{{ device(r.ua) }} · {{ r.ip }}</small></template>
      <template v-else-if="r.src === 'view'">
        <RouterLink :to="r.path">{{ r.path }}</RouterLink> <small class="text-secondary" :title="`${r.ua}\n${r.ip}`">{{ device(r.ua) }}</small>
      </template>
      <template v-else-if="r.src === 'api' || r.src === 'fail'">
        <code>{{ r.method }} {{ r.path }}</code> <span class="badge fw-normal" :class="status">{{ r.status }}</span>
        <small class="text-secondary"> {{ r.ms }} мс</small>
      </template>
      <template v-else-if="r.src === 'edit'">
        {{ COLLS[r.coll] || r.coll }}
        <small v-if="r.user !== about" class="text-secondary">· змінив {{ name(r.user) }}</small> <i v-if="r.note" class="text-secondary">{{ r.note }}</i>
        <component :is="r.changes.length > 3 ? 'details' : 'div'" class="small text-secondary">
          <summary v-if="r.changes.length > 3">{{ r.changes.map((c) => c.field).join(', ') }}</summary>
          <div v-for="c in r.changes" :key="c.field" class="text-break">
            {{ c.field }}: <template v-if="c.old"><s>{{ c.old }}</s> → </template>{{ c.new || '✖️' }}
          </div>
        </component>
      </template>
      <template v-else-if="r.src === 'tg'">
        <span class="badge text-bg-light border fw-normal">{{ CHATS[r.chat_type] || r.chat_type }}</span>
        <span v-if="TG_KINDS[r.kind]" class="badge text-bg-light border fw-normal ms-1">{{ TG_KINDS[r.kind] }}</span>
        <span v-if="one && r.user && r.user !== one" class="small text-secondary ms-1">{{ name(r.user) }}:</span>
        <span class="text ms-1">{{ r.text || (r.content_type === 'text' ? '' : `[${r.content_type}]`) }}</span>
      </template>
      <template v-else-if="r.src === 'event'">
        <span class="text">{{ plain(r.text) }}</span>
        <span v-if="!r.sent" class="badge text-bg-warning fw-normal ms-1" title="Вид вимкнено, нема токена або Telegram не прийняв">не в Telegram</span>
      </template>
      <template v-else><span class="text">{{ r.text }}</span> <small class="text-secondary">— {{ name(r.by) }}</small></template>
    </div>
  </div>
</template>

<style scoped>
.arow { font-size: .9rem; line-height: 1.35; }
.time { flex: 0 0 4.2rem; font-variant-numeric: tabular-nums; font-size: .8rem; padding-top: .1rem; }
.who { flex: 0 0 9.5rem; }
.who a { color: inherit; text-decoration: none; }
.who a:hover { text-decoration: underline; }
.icon { flex: 0 0 1.3rem; text-align: center; }
.what { flex: 1 1 0; min-width: 0; overflow-wrap: anywhere; }
.text { white-space: pre-wrap; }
code { color: inherit; }
</style>
