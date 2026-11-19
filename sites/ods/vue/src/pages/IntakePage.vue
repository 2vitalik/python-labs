<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

import { flash } from '@core/anchors.js'
import Crumbs from '@core/components/Crumbs.vue'

import { getIntake } from '../api.js'
import IntakeFilters from '../components/IntakeFilters.vue'
import IntakeHow from '../components/IntakeHow.vue'
import IntakePerson from '../components/IntakePerson.vue'
import IntakeStrips from '../components/IntakeStrips.vue'
import { filterOf, pickRows } from '../intake.js'

// «Вхідні» (T368 §2.7): what the teacher forwarded to the bot from students' chats — the cards' numbers of each lab with
// a file, then people, the freshest talk first. The filters live in the address; the rows they took stay while the
// teacher works on them — an action answers with the whole INTAKE, and a row that no longer fits does not vanish under
// the mouse — and are taken anew when a filter changes
const route = useRoute()
const router = useRouter()
const data = ref(null)
const error = ref('')
const seen = ref(new Set())
const f = computed(() => filterOf(route.query))
const people = computed(() => data.value?.people.filter((p) => p.rows.some((r) => seen.value.has(r.id))) || [])
const set = (patch) => router.replace({ query: { ...route.query, ...patch } })
const take = () => data.value && (seen.value = pickRows(data.value.people, f.value))
watch(f, take)

onMounted(async () => {
  try {
    data.value = await getIntake()
    take()
  } catch (e) {
    error.value = e.message
  }
})
// a number of a strip → its file's row, shown even if the filters hid it
async function go(id) {
  if (!seen.value.has(id)) seen.value = new Set([...seen.value, id])
  await nextTick()
  flash(`in-${id}`)
}
</script>

<template>
  <div class="intake">
    <Crumbs :items="['Вхідні']" />
    <h1 class="h2 mb-1">Вхідні з Telegram</h1>
    <IntakeHow :force="!!data && !data.people.length" />
    <div v-if="error" class="alert alert-danger">{{ error }}</div>
    <p v-else-if="!data" class="text-secondary">Завантажую…</p>
    <p v-else-if="!data.people.length" class="text-secondary my-4">Поки порожньо.</p>
    <template v-else>
      <IntakeStrips v-if="data.strips.length" :strips="data.strips" @go="go" />
      <IntakeFilters :people="data.people" :f @set="set" />
      <div class="vstack gap-2">
        <IntakePerson v-for="p in people" :key="p.key" :p :seen @got="data = $event" />
      </div>
      <p v-if="!people.length" class="text-secondary">Під цей вибір нічого нема.</p>
    </template>
  </div>
</template>

<style>
/* the page's quiet words and links, shared by its parts: grey at rest, a dotted line under what can be clicked */
.intake .dot { padding: 0; border: 0; background: none; color: var(--bs-secondary-color); text-decoration: underline dotted; text-underline-offset: .2em; }
.intake .dot:hover:not(:disabled) { color: var(--bs-body-color); }
.intake .dot:disabled { opacity: .5; }
.intake .quiet { color: var(--bs-secondary-color); font-size: .8rem; }
</style>
