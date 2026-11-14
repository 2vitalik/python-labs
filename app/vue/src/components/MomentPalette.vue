<script setup>
import { computed } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { useMomentEd } from '../momentEd.js'
import { iconsOn } from '../momentsEdit.js'
import MomentIconForm from './MomentIconForm.vue'

// the palette is the legend (T276): every icon of a line is a brush — a click takes it and turns the tool back to
// painting; the line's name is renamed in a panel, a line whose icons no frame has can go. Icons drawn on the frames
// but missing from the legend follow it: a brush too, and «＋» names them into the legend. Brushes given from outside (a
// student's game: its entities) come first and are not the text's to rename
const ed = useMomentEd()
const used = computed(() => iconsOn(ed.model))
const plain = (s) => (s.match(/\*\*([^*]+)\*\*/)?.[1] || s.replace(/[*_`]/g, '')).trim()
const on = (icon) => ed.tool === 'paint' && ed.brush === icon
const take = (icon) => { ed.brush = icon; ed.tool = 'paint' }
function add({ icon, name }) {
  if (!ed.model.legend.length && !ed.model.legendTitle) ed.model.legendTitle = '**Приклад ігрових елементів**'
  const icons = icon.split(/[,\s]+/).filter(Boolean)
  ed.model.legend.push({ icons, name })
  take(icons[0])
}
</script>

<template>
  <div>
    <div class="label">{{ ed.given.length ? 'Чим малювати: сутності гри й свої значки' : 'Легенда — обери, чим малювати' }}</div>
    <div class="d-flex flex-wrap align-items-center gap-1">
      <button v-for="p in ed.given" :key="p.icon" type="button" class="item brush" :class="{ on: on(p.icon) }" :title="`малювати: ${p.name}`" @click="take(p.icon)">
        {{ p.icon }} <span class="name">{{ plain(p.name) }}</span></button>
      <span v-for="(l, i) in ed.model.legend" :key="i" class="item">
        <button v-for="icon in l.icons" :key="icon" type="button" class="brush" :class="{ on: on(icon) }" :title="`малювати: ${plain(l.name)}`" @click="take(icon)">{{ icon }}</button>
        <span class="name" :title="l.name.replace(/[*_`]/g, '')">{{ plain(l.name) }}</span>
        <MomentIconForm v-slot="{ toggle }" :icon="l.icons.join(', ')" :name="l.name" @save="(v) => (l.name = v.name)">
          <button type="button" class="iact" title="перейменувати" @click="toggle"><Icon name="pencil" /></button>
        </MomentIconForm>
        <DelButton v-if="!l.icons.some((x) => used.has(x))" :what="`«${plain(l.name)}» з легенди`" @yes="ed.model.legend.splice(i, 1)" />
      </span>
      <MomentIconForm v-slot="{ toggle }" fresh @save="add">
        <button type="button" class="btn btn-sm btn-add" @click="toggle"><Icon name="plus" /> значок</button>
      </MomentIconForm>
    </div>
    <div v-if="ed.stray.length" class="d-flex flex-wrap align-items-center gap-1 mt-1">
      <span class="label mb-0 me-1">ще на кадрах</span>
      <span v-for="icon in ed.stray" :key="icon" class="item">
        <button type="button" class="brush" :class="{ on: on(icon) }" title="малювати" @click="take(icon)">{{ icon }}</button>
        <MomentIconForm v-slot="{ toggle }" :icon @save="(v) => add({ icon, name: v.name })">
          <button type="button" class="iact add" title="назвати й додати в легенду" @click="toggle"><Icon name="plus" /></button>
        </MomentIconForm>
      </span>
    </div>
  </div>
</template>

<style scoped>
.label { font-size: .7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); margin-bottom: .2rem; }
.item { display: inline-flex; align-items: center; gap: .1rem; padding: .05rem .25rem; border: 1px solid var(--bs-border-color); border-radius: .4rem;
        background: var(--bs-body-bg); font-size: .8rem; }
.item .iact { width: 1.3rem; height: 1.3rem; font-size: .75rem; opacity: .45; }
.item:hover .iact { opacity: 1; }
.brush { width: 1.9rem; height: 1.9rem; padding: 0; border: 0; border-radius: .3rem; background: none; font-size: 1.1rem; line-height: 1; }
.brush:hover { background: var(--bs-tertiary-bg); }
.brush.on { box-shadow: inset 0 0 0 2px var(--bs-body-color); background: var(--bs-secondary-bg); }
.item.brush { width: auto; height: auto; padding: .1rem .4rem; }
.name { max-width: 9rem; padding-inline: .15rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
</style>
