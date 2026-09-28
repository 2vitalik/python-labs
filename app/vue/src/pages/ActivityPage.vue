<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { CHIPS } from '../activity.js'
import ActivityFeed from '../components/ActivityFeed.vue'
import ActivityPeople from '../components/ActivityPeople.vue'
import Crumbs from '../components/Crumbs.vue'
import { useTitle } from '../title.js'

// everything the site and the bot track, for the teacher (T146). The state lives in the URL, so a view can be bookmarked:
// ?tab=people · ?user=<nick> · ?show=site,tg (chips, when not the default set; `none` — all off) · ?days=30 · ?staff=1
const route = useRoute()
const router = useRouter()
useTitle(() => route.query.user && `Активність: ${route.query.user}`)
const DEFAULT = CHIPS.filter((c) => c.on).map((c) => c.key)
const tab = computed(() => (route.query.tab === 'people' && !route.query.user ? 'people' : 'feed'))
const staff = computed(() => route.query.staff === '1')
const shown = computed(() => (route.query.show ? route.query.show.split(',') : DEFAULT))
const src = computed(() => CHIPS.filter((c) => shown.value.includes(c.key)).flatMap((c) => c.src).join(','))
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })

// `none` — every chip is off: an empty `show` would read as the default set
const show = (keys) => set({ show: keys.join() === DEFAULT.join() ? undefined : keys.join() || 'none' })
const toggle = (key) => show(CHIPS.map((c) => c.key).filter((k) => shown.value.includes(k) !== (k === key)))
</script>

<template>
  <div>
    <Crumbs :items="route.query.user ? [['/activity', 'Активність'], route.query.user] : ['Активність']" />
    <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
      <h1 class="h3 mb-0 me-2">Активність</h1>
      <div v-if="!route.query.user" class="btn-group btn-group-sm">
        <button class="btn" :class="tab === 'feed' ? 'btn-primary' : 'btn-outline-secondary'" @click="set({ tab: undefined })">Стрічка</button>
        <button class="btn" :class="tab === 'people' ? 'btn-primary' : 'btn-outline-secondary'" @click="set({ tab: 'people' })">Люди</button>
      </div>
      <label v-if="!route.query.user" class="form-check form-switch small ms-auto mb-0" title="Рядки викладачів і службові">
        <input class="form-check-input" type="checkbox" :checked="staff" @change="set({ staff: staff ? undefined : '1' })">
        і викладачі
      </label>
    </div>
    <ActivityPeople v-if="tab === 'people'" :days="Number(route.query.days ?? 7)" :staff />
    <template v-else>
      <div class="d-flex flex-wrap align-items-center gap-1 mb-3">
        <button v-for="c in CHIPS" :key="c.key" class="btn btn-sm" :class="shown.includes(c.key) ? 'btn-secondary' : 'btn-outline-secondary'"
                :title="c.title" @click="toggle(c.key)">{{ c.icon }} {{ c.text }}</button>
        <a v-if="src" href="#" class="small text-secondary ms-1" @click.prevent="show([])">скинути</a>
      </div>
      <ActivityFeed :nick="route.query.user" :src :staff />
    </template>
  </div>
</template>
