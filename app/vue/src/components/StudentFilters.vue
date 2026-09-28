<script setup>
import { useStudentFilter } from '../studentFilter.js'

// filter buttons of /students: group chips (none pressed = every group) and a «has it / doesn't» pair per column;
// the number on a button — how many rows it leaves with the other filters kept
const props = defineProps({ students: Array })
const { active, groups, facets, toggleGroup, toggleFacet, reset } = useStudentFilter(() => props.students)
const look = (on, n) => (on ? 'btn-secondary' : ['btn-outline-secondary', { 'opacity-50': !n }])
</script>

<template>
  <div class="d-flex flex-wrap gap-1 mb-2">
    <button v-for="g in groups" :key="g.name" type="button" class="btn btn-sm" :class="look(g.on, g.n)" :title="g.name"
            @click="toggleGroup(g)">{{ g.text }} <span class="count">{{ g.n }}</span></button>
  </div>
  <div class="d-flex flex-wrap align-items-center gap-2 mb-3">
    <div v-for="f in facets" :key="f.key" class="btn-group btn-group-sm" :title="f.title">
      <button v-for="v in ['1', '0']" :key="v" type="button" class="btn" :class="look(f.value === v, f.n[v])"
              @click="toggleFacet(f.key, v)">{{ v === '1' ? f.text : 'ні' }} <span class="count">{{ f.n[v] }}</span></button>
    </div>
    <a v-if="active" href="#" class="small text-secondary" @click.prevent="reset">скинути</a>
  </div>
</template>

<style scoped>
/* Bootstrap fills an outline button on hover: one just switched off would still look pressed */
.btn-outline-secondary { --bs-btn-hover-color: var(--bs-btn-color); --bs-btn-hover-bg: var(--bs-tertiary-bg); }
.count { font-weight: 400; opacity: .55; font-size: .85em; }
</style>
