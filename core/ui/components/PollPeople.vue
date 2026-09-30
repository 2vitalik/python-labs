<script setup>
import { moment, whoKey, whoName } from '../polls.js'
import Avatar from './Avatar.vue'

// voters as a row of names: a person of the site links to their activity — every vote and message of theirs;
// a Telegram account the site does not know shows its @username. `list` — { who, at?, where? } or plain persons
defineProps({ list: { type: Array, required: true } })
const who = (e) => e.who || e
const hint = (e) => [who(e).group, moment(e.at), e.where && `📍 ${e.where}`].filter(Boolean).join(' · ')
</script>

<template>
  <div class="d-flex flex-wrap gap-1">
    <span v-for="e in list" :key="whoKey(who(e))" class="person d-inline-flex align-items-center gap-1 border rounded-pill ps-1 pe-2" :title="hint(e)">
      <template v-if="who(e).nick">
        <Avatar :user="who(e)" :size="18" />
        <RouterLink :to="`/activity?user=${who(e).nick}`">{{ whoName(who(e)) }}</RouterLink>
      </template>
      <template v-else>
        <span class="unknown">?</span>
        <a v-if="who(e).username && who(e).tg_id != null" :href="`https://t.me/${who(e).username}`" target="_blank" class="text-secondary">{{ whoName(who(e)) }}</a>
        <span v-else class="text-secondary">{{ whoName(who(e)) }}</span>
      </template>
    </span>
  </div>
</template>

<style scoped>
.person { font-size: .85rem; line-height: 1.6; }
.person a { color: inherit; text-decoration: none; }
.person a:hover { text-decoration: underline; }
.unknown { display: inline-flex; align-items: center; justify-content: center; width: 18px; height: 18px; border-radius: 50%; font-size: .7rem;
           background: var(--bs-secondary-bg); color: var(--bs-secondary-color); }
</style>
