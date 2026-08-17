<script setup>
import { computed } from 'vue'

const props = defineProps({ windows: Array, menus: Array })
const emit = defineEmits(['pick'])

const W = 160, H = 92, THUMB = 56, COL = 240, ROW = 118

const trim = (s, n = 20) => (s.length > n ? s.slice(0, n - 1) + '…' : s)

const graph = computed(() => {
  const ids = props.windows.map((w) => w.id)
  const byPair = {} // parallel menu items merge into one labeled arrow
  for (const m of props.menus) {
    if (!m.window) continue
    for (const it of m.items) {
      if (!it.window || it.window === m.window || !ids.includes(it.window)) continue
      const key = `${m.window}>${it.window}`
      byPair[key] ??= { from: m.window, to: it.window, labels: [] }
      if (it.title) byPair[key].labels.push(it.title)
    }
  }
  const edges = Object.values(byPair)
  const adj = {}
  edges.forEach((e) => (adj[e.from] ??= []).push(e.to))

  // BFS layers left → right; unreachable windows start new roots
  const layerOf = {}
  for (const root of ids) {
    if (root in layerOf) continue
    layerOf[root] = 0
    const q = [root]
    while (q.length) {
      const v = q.shift()
      for (const t of adj[v] || []) {
        if (!(t in layerOf)) {
          layerOf[t] = layerOf[v] + 1
          q.push(t)
        }
      }
    }
  }
  const rows = {}
  const pos = {}
  for (const w of props.windows) {
    const l = layerOf[w.id]
    rows[l] ??= 0
    pos[w.id] = { x: 20 + l * COL, y: 16 + rows[l] * ROW, win: w }
    rows[l]++
  }
  const lines = edges.map((e) => {
    const a = pos[e.from], b = pos[e.to]
    const [x1, y1, x2, y2] = [a.x + W, a.y + H / 2, b.x, b.y + H / 2]
    const dx = Math.max(40, Math.abs(x2 - x1) / 2)
    return {
      d: `M ${x1} ${y1} C ${x1 + dx} ${y1}, ${x2 - dx} ${y2}, ${x2} ${y2}`,
      lx: (x1 + x2) / 2, ly: (y1 + y2) / 2 - 7, label: trim(e.labels.join(', '), 28),
    }
  })
  return {
    pos, lines,
    width: 40 + (Math.max(0, ...Object.keys(rows).map(Number)) + 1) * COL - (COL - W),
    height: 32 + Math.max(1, ...Object.values(rows)) * ROW - (ROW - H),
  }
})
</script>

<template>
  <div>
    <div class="overflow-x-auto">
      <svg :width="graph.width" :height="graph.height" class="d-block">
        <defs>
          <marker id="arrow" viewBox="0 0 8 8" refX="7" refY="4" markerWidth="7" markerHeight="7" orient="auto">
            <path d="M 0 0 L 8 4 L 0 8 z" fill="#868e96" />
          </marker>
        </defs>
        <g v-for="(e, i) in graph.lines" :key="i">
          <path :d="e.d" fill="none" stroke="#adb5bd" stroke-width="1.5" marker-end="url(#arrow)" />
          <text :x="e.lx" :y="e.ly" text-anchor="middle" class="lbl">{{ e.label }}</text>
        </g>
        <g v-for="(p, id) in graph.pos" :key="id" role="button" @click="emit('pick', id)">
          <rect :x="p.x" :y="p.y" :width="W" :height="H" rx="8" fill="#fff" stroke="#ced4da" />
          <image v-if="p.win.screenshots[0]" :href="`/api/uploads/${p.win.game}/${p.win.screenshots[0]}`"
                 :x="p.x + 5" :y="p.y + 5" :width="W - 10" :height="THUMB" preserveAspectRatio="xMidYMid slice" />
          <text :x="p.x + W / 2" :y="p.y + (p.win.screenshots[0] ? H - 12 : H / 2 + 4)"
                text-anchor="middle" class="ttl">{{ trim(p.win.title) }}</text>
        </g>
      </svg>
    </div>
    <p v-if="!graph.lines.length" class="text-secondary small mb-0">
      Стрілки зʼявляться, коли меню матимуть вікно-хост, а їхні пункти — цілі-вікна.
    </p>
  </div>
</template>

<style scoped>
.ttl { font-size: .8rem; font-weight: 600; fill: #212529; }
.lbl { font-size: .7rem; fill: #868e96; paint-order: stroke; stroke: #fff; stroke-width: 3px; }
</style>
