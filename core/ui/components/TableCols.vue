<script setup>
import { computed, ref } from 'vue'

// which columns the table shows and in what order: the picked ones on the left (↑ ↓ ✕), every column there is on the right, by its group
const props = defineProps({ cols: { type: Array, required: true }, picked: { type: Array, required: true } })
const emit = defineEmits(['change', 'close'])
const byKey = computed(() => Object.fromEntries(props.cols.map((c) => [c.key, c])))
const groups = computed(() => {
  const out = new Map()
  for (const c of props.cols) out.set(c.group, [...(out.get(c.group) || []), c])
  return [...out].map(([name, list]) => ({ name, list, n: list.filter((c) => props.picked.includes(c.key)).length }))
})
const open = ref(new Set(groups.value.filter((g) => g.n).map((g) => g.name)))
const toggleGroup = (name) => (open.value.has(name) ? open.value.delete(name) : open.value.add(name))
const toggle = (key) => emit('change', props.picked.includes(key) ? props.picked.filter((k) => k !== key) : [...props.picked, key])
function move(key, by) {
  const list = [...props.picked]
  const i = list.indexOf(key)
  const j = i + by
  if (j < 0 || j >= list.length) return
  ;[list[i], list[j]] = [list[j], list[i]]
  emit('change', list)
}
</script>

<template>
  <div class="card mb-3">
    <div class="card-body py-2">
      <div class="d-flex align-items-center gap-2 mb-2">
        <b>▦ Колонки</b>
        <button type="button" class="btn-close btn-sm ms-auto" title="Згорнути" @click="emit('close')"></button>
      </div>
      <div class="row g-3 small">
        <div class="col-md-4">
          <div class="text-secondary mb-1">Показані · {{ picked.length }}</div>
          <div v-for="(k, i) in picked" :key="k" class="d-flex align-items-center gap-1 py-1 border-bottom">
            <span class="text-truncate" :title="byKey[k]?.title">{{ byKey[k]?.short }}<template v-if="byKey[k]?.short !== byKey[k]?.title"> {{ byKey[k]?.title }}</template></span>
            <a href="#" class="ibtn ms-auto" :class="{ invisible: !i }" title="Вище" @click.prevent="move(k, -1)">↑</a>
            <a href="#" class="ibtn" :class="{ invisible: i === picked.length - 1 }" title="Нижче" @click.prevent="move(k, 1)">↓</a>
            <a href="#" class="ibtn" title="Сховати" @click.prevent="toggle(k)">✕</a>
          </div>
        </div>
        <div class="col-md-8">
          <div v-for="g in groups" :key="g.name" class="mb-1">
            <a href="#" class="text-body text-decoration-none fw-semibold" @click.prevent="toggleGroup(g.name)">{{ open.has(g.name) ? '▾' : '▸' }} {{ g.name }}
              <span class="text-secondary fw-normal">{{ g.n }} / {{ g.list.length }}</span></a>
            <div v-if="open.has(g.name)" class="d-flex flex-wrap gap-1 mt-1 mb-2">
              <button v-for="c in g.list" :key="c.key" type="button" class="btn btn-sm chip" :class="picked.includes(c.key) ? 'btn-secondary' : 'btn-outline-secondary'"
                      :title="c.title" @click="toggle(c.key)">{{ c.short }} <span v-if="c.short !== c.title" class="opacity-75">{{ c.title.replace(/^Лаба \d+: /, '') }}</span></button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
