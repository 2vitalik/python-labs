<script setup>
import { seek } from '../lesson.js'
import Avatar from './Avatar.vue'

// the merged transcript as a chat: a section per topic (its time is the anchor), lines with the speaker's avatar and a link
// to the student; a run of one speaker shows the name once; a time opens the video at that moment when the host can
const props = defineProps({ sections: Array, people: Object, video: Object, start: String })
const person = (who) => props.people[who]
const to = (who) => (person(who)?.nick ? `/students/${person(who).nick}` : '')
const teacher = (who) => person(who)?.status === 'admin'
const at = (t) => {
  const s = props.video?.at && seek(t, props.start)
  return s == null ? '' : props.video.at(s)
}
const same = (items, i) => i > 0 && items[i - 1].who === items[i].who
</script>

<template>
  <div class="transcript">
    <section v-for="s in sections" :id="s.id" :key="s.id">
      <h3 v-if="s.title" class="h5 d-flex align-items-baseline gap-2 mt-4 mb-2">
        <span>{{ s.title }}</span><small class="text-body-tertiary fw-normal">{{ s.time }}</small>
      </h3>
      <template v-for="(it, i) in s.items" :key="i">
        <p v-if="it.note" class="note text-body-tertiary fst-italic small text-center my-2">{{ it.note }}</p>
        <div v-else-if="it.who" class="line" :class="{ same: same(s.items, i), teacher: teacher(it.who) }">
          <Avatar v-if="!same(s.items, i)" :user="person(it.who) || { name: it.who }" :size="28" class="ms-auto" />
          <div v-else class="gutter small text-body-tertiary">{{ it.time !== s.items[i - 1].time ? it.time : '' }}</div>
          <div>
            <div v-if="!same(s.items, i)" class="head small">
              <RouterLink v-if="to(it.who)" :to="to(it.who)" class="name">{{ it.who }}</RouterLink>
              <span v-else class="name">{{ it.who }}</span>
              <a v-if="at(it.time)" :href="at(it.time)" target="_blank" rel="noopener" class="time" title="Відео з цього місця">{{ it.time }}</a>
              <span v-else class="time">{{ it.time }}</span>
            </div>
            <div class="text">{{ it.text }}</div>
          </div>
        </div>
        <p v-else class="text-secondary small">{{ it.text }}</p>
      </template>
    </section>
  </div>
</template>

<style scoped>
section { scroll-margin-top: 1rem; }
/* a #t-… link lights the heading, not the whole section (flash() in anchors.js lights the target) */
section.flash { animation: none; }
section.flash > h3 { animation: guide-flash 2.5s ease-out; border-radius: .25rem; }
.line { display: grid; grid-template-columns: 2.4rem 1fr; gap: .25rem .5rem; margin-top: .6rem; }
.line.same { margin-top: .15rem; }
.gutter { text-align: right; padding-top: .15rem; font-size: .72rem; white-space: nowrap; font-variant-numeric: tabular-nums; }
.head { display: flex; gap: .5rem; align-items: baseline; line-height: 1.2; }
.name { font-weight: 600; text-decoration: none; color: inherit; }
a.name:hover { text-decoration: underline; }
.teacher .name { color: var(--bs-primary); }
.time { color: var(--bs-tertiary-color); text-decoration: none; font-variant-numeric: tabular-nums; }
a.time:hover { color: var(--bs-body-color); text-decoration: underline; }
.text { line-height: 1.45; }
</style>
