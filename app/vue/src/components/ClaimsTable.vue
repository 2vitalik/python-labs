<script setup>
import { computed, ref, watch } from 'vue'

import { CLAIM_STATUSES, zones } from '../catalog.js'
import { useEd } from '../ed.js'
import ClaimRow from './ClaimRow.vue'
import SubzoneRows from './SubzoneRows.vue'

// the «Картки» view (T270 §11): every claim of the game, the automatic ones too, as zone → subzone → card, each row
// saying where it is anchored — the teacher checks here, the student sees what went where
const ed = useEd()
const CHIPS = { '': 'усі', ...CLAIM_STATUSES }
const status = ref('')
const auto = ref(false)  // the claims that made themselves (an entity's type, a stat, a field option) are a long tail: off until asked
const own = computed(() => ed.claims.filter((c) => auto.value || !c.auto))
const autos = computed(() => ed.claims.filter((c) => c.auto).length)
const count = (s) => own.value.filter((c) => !s || c.status === s).length
const zoneKey = (c) => {
  const z = ed.info(c.task)?.zone
  return zones.value[z] ? z : ''
}
const tree = computed(() => {
  const by = {}
  for (const c of own.value) if (!status.value || c.status === status.value) (by[zoneKey(c)] ??= []).push(c)
  const known = Object.entries(zones.value).filter(([z]) => by[z]).map(([z, zone]) => ({ key: z, ...zone, list: by[z] }))
  return by[''] ? [...known, { key: '', icon: '·', title: 'інше', color: '#888', list: by[''] }] : known
})
// the categories on screen are this view's contents (the editor's Toc)
const emit = defineEmits(['toc'])
const idOf = (z) => `cards-${z.key || 'other'}`
watch(tree, (t) => emit('toc', t.map((z) => ({ id: idOf(z), text: `${z.icon} ${z.title} (${z.list.length})`, depth: 2 }))), { immediate: true })
</script>

<template>
  <div class="vstack gap-3">
    <div class="d-flex flex-wrap gap-1">
      <button v-for="(label, s) in CHIPS" :key="s" type="button" class="btn btn-sm chip"
              :class="status === s ? 'btn-secondary' : 'btn-outline-secondary'" @click="status = s">
        {{ label }} <span class="opacity-75">{{ count(s) }}</span>
      </button>
      <label v-if="autos" class="form-check form-switch small m-0 ms-auto align-self-center" title="Типи сутностей, параметри, властивості поля, типи вікон — заявляються самі, коли їх обирають; мапа рівня й ігрові моменти — коли їх намальовано">
        <input v-model="auto" type="checkbox" class="form-check-input"> і ті, що заявились самі ({{ autos }})
      </label>
    </div>
    <div v-if="!tree.length" class="text-secondary small">
      {{ ed.claims.length ? 'Карток з таким статусом нема.' : 'Карток ще нема: вони зʼявляються, коли обираєш тип сутності, вікна чи властивість поля або додаєш картку з каталогу.' }}
    </div>
    <section v-for="z in tree" :id="idOf(z)" :key="z.key" class="vstack gap-1 noflash">
      <div class="zone" :style="{ color: z.color }">{{ z.icon }} {{ z.title }} <span class="count">{{ z.list.length }}</span></div>
      <SubzoneRows v-if="z.key" :claims="z.list" where />
      <template v-else><ClaimRow v-for="c in z.list" :key="c.id" :claim="c" where /></template>
    </section>
  </div>
</template>

<style scoped>
.zone { font-weight: 700; }
.count { font-weight: 400; opacity: .6; }
[data-bs-theme=dark] .zone { filter: brightness(1.5); }
</style>
