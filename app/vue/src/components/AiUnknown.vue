<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vPeek } from '@core/peek.js'
import { kindOf, taskIndex } from '../catalog.js'
import { useEd } from '../ed.js'
import { plusOf } from '../gameAdd.js'
import { jump } from '@core/jump.js'
import CoinBadge from './CoinBadge.vue'
import IdeaPop from './IdeaPop.vue'

// a phrase the helper could not lay (T289 §1): the student's words, what is wrong with them, the cards it might be. A card
// that goes in at once the catalog's way (gameAdd.js: no question first) has its «＋» here; one that asks — a type, a
// parameter, a field option, params — opens in the catalog. Nothing fits — «💡» proposes a card. `data` — {why, candidates}
const props = defineProps({ data: Object, item: Object })
const ed = useEd()
const busy = ref(false)
const error = ref('')
const cands = computed(() => (props.data.candidates || []).map((slug) => {
  const t = ed.info(slug) || taskIndex.value[slug]
  const plus = t && t.status === 'active' && kindOf(t) !== 'fieldopt' ? plusOf(t) : null
  return { slug, t, run: plus && !plus.ask ? plus.run : null, has: ed.claims.some((c) => c.task === slug) }
}))

async function add(c) {
  busy.value = true
  error.value = ''
  try {
    const claim = await c.run()
    await ed.changed()
    if (claim?.id) jump(`c-${claim.id}`)
  } catch (e) {
    error.value = e.message
  } finally {
    busy.value = false
  }
}
</script>

<template>
  <div class="vstack gap-1">
    <div><span class="ai-q">«{{ item.quote }}»</span> — {{ data.why }}</div>
    <div class="d-flex flex-wrap gap-1">
      <span v-for="c in cands" :key="c.slug" v-peek="{ kind: 'task', id: c.slug }" class="cand">
        <CoinBadge :coin="c.t?.coin" :amount="c.t?.amount" /> {{ c.t?.title || c.slug }}
        <Icon v-if="c.has" name="done" class="text-success" title="уже в грі" />
        <button v-else-if="c.run" type="button" class="iact add" :disabled="busy" title="Додати картку в гру" @click="add(c)"><Icon name="plus" /></button>
        <RouterLink v-else :to="`/tasks?q=${c.slug}`" class="iact" title="Відкрити в каталозі"><Icon name="open" /></RouterLink>
      </span>
      <IdeaPop v-slot="{ toggle }" kind="idea" :note="`«${item.quote}» — ${data.why}`">
        <button type="button" class="cand idea" @click="toggle">💡 нема такої — запропонувати</button>
      </IdeaPop>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
  </div>
</template>

<style scoped>
.cand { display: inline-flex; align-items: center; gap: .25rem; padding: 0 .1rem 0 .45rem; border: 1px solid color-mix(in srgb, var(--act-add) 45%, transparent);
        border-radius: 1rem; background: var(--bs-body-bg); font-size: .8rem; }
.cand .iact { width: 1.3rem; height: 1.3rem; }
.cand.idea { padding-right: .45rem; color: var(--act-add); }
.cand.idea:hover { background: color-mix(in srgb, var(--act-add) 8%, transparent); }
</style>
