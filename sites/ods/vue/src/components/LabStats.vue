<script setup>
import { ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import Reveal from '@core/components/Reveal.vue'
import { vHint } from '@core/hint.js'
import { load, save } from '@core/local.js'

import { getLabStats } from '../api.js'
import { MISSING } from '../labText.js'

// «Де помиляються» (T354 §1.7): per answer of the line — how many right and wrong, and under it the causes the site
// named, with who (routes/lab_stats.py). Folded or open as the teacher left it; fetched the first time it opens
const props = defineProps({ n: Number })
const open = ref(load('ods-lab-stats') === '1')
const stats = ref(null)  // [{name, ok, bad, why: [{text, n, who: [{vid, nick, name}]}]}]
const error = ref('')

watch(open, async (on) => {
  save('ods-lab-stats', on ? '1' : '0')
  if (!on || stats.value) return
  try {
    stats.value = await getLabStats(props.n)
  } catch (e) {
    error.value = e.message
  }
}, { immediate: true })
const pc = (s, k) => `${(100 * s[k]) / ((s.ok + s.bad) || 1)}%`
const cause = (w) => w.text || 'невідома причина'
const who = (w) => w.who?.map((x) => `${x.name || x.nick} (${x.vid})`).join('\n')
</script>

<template>
  <section class="mb-3">
    <button type="button" class="st-head" :aria-expanded="open" @click="open = !open">
      <Icon :name="open ? 'down' : 'right'" /> Де помиляються
    </button>
    <Reveal :show="open">
      <div class="st-body">
        <p v-if="error" class="text-danger small mb-0">{{ error }}</p>
        <p v-else-if="!stats" class="text-secondary small mb-0">Рахую…</p>
        <p v-else-if="!stats.length" class="text-secondary small mb-0">Рядків відповідей ще нема.</p>
        <div v-for="s in stats || []" :key="s.name" class="st-row">
          <code class="st-name">{{ s.name }}</code>
          <span class="st-bar"><i class="ok" :style="{ width: pc(s, 'ok') }" /><i class="bad" :style="{ width: pc(s, 'bad') }" /></span>
          <span class="st-n">✅ {{ s.ok }} · ❌ {{ s.bad }}</span>
          <ul v-if="s.why?.length" class="st-why list-unstyled mb-0">
            <li v-for="w in s.why" :key="w.text" :class="{ quiet: !w.text || w.text === MISSING }">
              <span v-hint="who(w)"><b>{{ w.n }}</b> × {{ cause(w) }}</span>
            </li>
          </ul>
        </div>
      </div>
    </Reveal>
  </section>
</template>

<style scoped>
.st-head { display: inline-flex; align-items: center; gap: .3rem; padding: 0; border: 0; background: none; font-weight: 600; }
.st-body { display: flex; flex-direction: column; gap: .4rem; padding: .5rem 0 0 1.3rem; max-width: 46rem; }
.st-row { display: grid; grid-template-columns: 8rem minmax(6rem, 1fr) auto; align-items: center; column-gap: .75rem; font-size: .85rem; }
.st-name { overflow: hidden; text-overflow: ellipsis; }
.st-bar { display: flex; height: .45rem; border-radius: .25rem; overflow: hidden; background: var(--bs-tertiary-bg); }
.st-bar .ok { background: var(--bs-success); }
.st-bar .bad { background: var(--bs-danger); }
.st-n { color: var(--bs-secondary-color); font-size: .78rem; white-space: nowrap; }
.st-why { grid-column: 2 / -1; color: var(--bs-danger-text-emphasis); font-size: .8rem; }
.st-why .quiet { color: var(--bs-secondary-color); }
</style>
