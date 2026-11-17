<script setup>
import { subStyle } from '../catalog.js'

// the filter of /tasks: a row of categories, under the chosen one — a row of its subcategories, each with how many cards match;
// with one category to show (the catalog's window of a section, T318) its row says nothing — the subcategories alone,
// and of them only `subs` (a Set of `zone/sub`), when given: the ones the place has cards of
defineProps({ zones: Object, subs: Object, counts: Object, zone: String, sub: String })
defineEmits(['select'])
</script>

<template>
  <nav class="mb-3">
    <div v-if="Object.keys(zones).length > 1" class="cap">категорія</div>
    <div v-if="Object.keys(zones).length > 1" class="d-flex flex-wrap gap-1">
      <button type="button" class="btn btn-sm zone-btn" :class="{ active: !zone }"
              @click="$emit('select', '', '')">
        Всі<sup class="count">{{ counts[''] || 0 }}</sup>
      </button>
      <button v-for="(z, zk) in zones" :key="zk" type="button" class="btn btn-sm zone-btn"
              :style="{ '--zc': z.color }" :class="{ active: zone === zk, 'opacity-50': !counts[zk] }"
              @click="$emit('select', zone === zk ? '' : zk, '')">
        {{ z.icon }} {{ z.title }}<sup class="count">{{ counts[zk] || 0 }}</sup>
      </button>
    </div>
    <template v-if="zones[zone]">  <!-- ?zone= in the URL comes before the zones load -->
      <div class="cap" :class="{ 'mt-2': Object.keys(zones).length > 1 }">підкатегорія</div>
      <div class="d-flex flex-wrap gap-1">
        <button v-for="([st, si], sk, i) in zones[zone].subzones" v-show="!subs || subs.has(`${zone}/${sk}`)" :key="sk" type="button"
                class="btn btn-sm sub-btn" :style="subStyle(zones[zone].color, i)"
                :class="{ active: sub === sk, 'opacity-50': !counts[`${zone}/${sk}`] }"
                @click="$emit('select', zone, sub === sk ? '' : sk)">
          {{ si }} {{ st }}<sup class="count">{{ counts[`${zone}/${sk}`] || 0 }}</sup>
        </button>
      </div>
    </template>
  </nav>
</template>

<style scoped>
.cap { margin-bottom: .2rem; font-size: .7rem; color: var(--bs-secondary-color); }
.zone-btn {
  --zc: #6c757d;
  font-weight: 600; color: var(--zc);
  background: color-mix(in srgb, var(--zc) 8%, var(--bs-body-bg));
  border: 1px solid color-mix(in srgb, var(--zc) 40%, var(--bs-body-bg));
}
.sub-btn {
  color: var(--sc); background: var(--st);
  border: 1px solid color-mix(in srgb, var(--sc) 35%, var(--bs-body-bg));
}
/* the zone colours are picked for a white page: on a dark one the text goes lighter, the tint darker */
[data-bs-theme=dark] .zone-btn { color: color-mix(in srgb, var(--zc) 60%, #fff); }
[data-bs-theme=dark] .sub-btn { color: color-mix(in srgb, var(--sc) 60%, #fff);
                                background: color-mix(in srgb, var(--sc) 12%, var(--bs-body-bg)); }
.zone-btn.active { color: #fff; background: var(--zc); border-color: var(--zc); }
.sub-btn.active { color: #fff; background: var(--sc); border-color: var(--sc); }
/* the whole row of categories fits the page column: the count is an index at the word, the buttons stand closer */
.zone-btn { --bs-btn-padding-x: .45rem; }
.count { top: -.55em; margin-left: .15em; font-size: .68em; font-weight: 400; opacity: .7; }
</style>
