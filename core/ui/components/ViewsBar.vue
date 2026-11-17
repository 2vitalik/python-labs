<script setup>
import Icon from './Icon.vue'

// the library's switches (T315 §8), all of them in the URL: a search over the name, «для чого» and the tags; the views
// in folders or by origin; ⭐ only; the order; the tags as chips — a click keeps the views with that one
defineProps({ f: { type: Object, required: true }, tags: { type: Array, default: () => [] } })
const emit = defineEmits(['set'])
const MODES = [['folders', 'folder', 'папками', 'Папки: вид перетягується між ними й усередині'],
               ['tree', 'branch', 'походженням', 'Дерево «з чого зроблено», під видом — його версії']]
const ORDERS = [['own', 'свій', 'Як переставлено руками — і на вкладках таблиці'], ['used', 'останнє використання', 'Спершу ті, з якими працювали недавно'],
                ['name', 'назва', 'За абеткою']]
const chip = (on) => (on ? 'btn-secondary' : 'btn-outline-secondary')
</script>

<template>
  <div class="vbar d-flex flex-wrap align-items-center gap-2 mb-2">
    <label class="vbar-q">
      <Icon name="search" />
      <input type="search" class="form-control form-control-sm" :value="f.q" placeholder="назва, для чого, тег" aria-label="Пошук видів"
             @input="emit('set', { q: $event.target.value || undefined })">
    </label>
    <div class="btn-group btn-group-sm" role="group" aria-label="Як показати види">
      <button v-for="[id, icon, text, tip] in MODES" :key="id" type="button" class="btn" :class="chip(f.mode === id)" :title="tip"
              @click="emit('set', { mode: id === 'folders' ? undefined : id })"><Icon :name="icon" /> {{ text }}</button>
    </div>
    <button type="button" class="btn btn-sm chip" :class="chip(f.etalon)" :title="f.mode === 'tree' ? 'Еталони й шлях до них; решта згорнута' : 'Лише види-еталони'"
            @click="emit('set', { etalon: f.etalon ? undefined : '1' })"><Icon :name="f.etalon ? 'starfill' : 'star'" /> лише еталони</button>
    <span class="vbar-order ms-auto" role="group" aria-label="Порядок">
      <Icon name="sort" />
      <template v-for="([id, text, tip], i) in ORDERS" :key="id">
        <span v-if="i" aria-hidden="true">·</span>
        <button type="button" :class="{ on: f.order === id }" :title="tip" :aria-pressed="f.order === id"
                @click="emit('set', { order: id === 'own' ? undefined : id })">{{ text }}</button>
      </template>
    </span>
  </div>
  <div v-if="tags.length" class="vbar-tags d-flex flex-wrap gap-1 mb-3">
    <button v-for="t in tags" :key="t" type="button" class="btn btn-sm chip" :class="chip(f.tag === t)" :aria-pressed="f.tag === t"
            @click="emit('set', { tag: f.tag === t ? undefined : t })">#{{ t }}</button>
  </div>
  <div v-else class="mb-3" />
</template>

<style scoped>
.vbar-q { position: relative; flex: 1 1 11rem; max-width: 18rem; margin: 0; }
.vbar-q .icon { position: absolute; top: 50%; left: .55rem; transform: translateY(-50%); color: var(--bs-secondary-color); pointer-events: none; }
.vbar-q input { padding-left: 1.75rem; }
.btn .icon, .chip .icon { margin-right: .15rem; }
.vbar-order { display: inline-flex; align-items: center; gap: .35rem; font-size: .8rem; color: var(--bs-secondary-color); white-space: nowrap; }
.vbar-order button { padding: 0; border: 0; background: none; color: inherit; }
.vbar-order button:hover { color: var(--bs-body-color); }
.vbar-order button.on { color: var(--bs-body-color); font-weight: 600; }
.vbar-tags .btn { --bs-btn-padding-y: 0; --bs-btn-font-size: .78rem; }
</style>
