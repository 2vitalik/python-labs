<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { load, save } from '@core/local.js'
import { useMomentEd } from '../momentEd.js'
import { iconsOn } from '../momentsEdit.js'
import MomentIconForm from './MomentIconForm.vue'

// the brushes right over the field (T276, T294 §19): a row of icons — the game's entities, then the legend's own icons,
// then icons drawn on the frames that no line names yet — a click takes one and turns the tool back to painting, its
// name comes under the mouse. «Aa» shows the names (remembered in this browser): then a legend's line can be renamed
// or, once no frame has its icons, taken away; «＋» names a new icon into the legend
const ed = useMomentEd()
const used = computed(() => iconsOn(ed.model))
const names = ref(load('moment-names') === '1')
const flip = () => save('moment-names', (names.value = !names.value) ? '1' : '')
const plain = (s) => (s.match(/\*\*([^*]+)\*\*/)?.[1] || s.replace(/[*_`]/g, '')).trim()
const on = (icon) => (ed.tool === 'paint' || ed.tool === 'fill') && ed.brush === icon
const take = (icon) => { ed.brush = icon; if (ed.tool !== 'fill') ed.tool = 'paint' }
function add({ icon, name }) {
  ed.snap()
  if (!ed.model.legend.length && !ed.model.legendTitle) ed.model.legendTitle = '**Приклад ігрових елементів**'
  const icons = icon.split(/[,\s]+/).filter(Boolean)
  ed.model.legend.push({ icons, name })
  take(icons[0])
}
</script>

<template>
  <div class="pal" :class="{ names }">
    <template v-if="ed.given.length">
      <button v-for="p in ed.given" :key="p.icon" type="button" class="brush qtip" :class="{ on: on(p.icon) }" :data-tip="names ? null : plain(p.name)"
              :aria-label="`малювати: ${plain(p.name)}`" @click="take(p.icon)">{{ p.icon }}<span v-if="names" class="name">{{ plain(p.name) }}</span></button>
      <span v-if="ed.model.legend.length || ed.stray.length" class="sep" />
    </template>
    <span v-for="(l, i) in ed.model.legend" :key="i" class="line">
      <button v-for="icon in l.icons" :key="icon" type="button" class="brush qtip" :class="{ on: on(icon) }" :data-tip="names ? null : plain(l.name)"
              :aria-label="`малювати: ${plain(l.name)}`" @click="take(icon)">{{ icon }}</button>
      <template v-if="names">
        <span class="name" :title="l.name.replace(/[*_`]/g, '')">{{ plain(l.name) }}</span>
        <MomentIconForm v-slot="{ toggle }" :icon="l.icons.join(', ')" :name="l.name" @save="(v) => (l.name = v.name)">
          <button type="button" class="iact" title="перейменувати" @click="toggle"><Icon name="pencil" /></button>
        </MomentIconForm>
        <DelButton v-if="!l.icons.some((x) => used.has(x))" :what="`«${plain(l.name)}» з легенди`" @yes="ed.snap(); ed.model.legend.splice(i, 1)" />
      </template>
    </span>
    <span v-for="icon in ed.stray" :key="icon" class="line stray">
      <button type="button" class="brush qtip" :class="{ on: on(icon) }" data-tip="є на кадрах, у легенді нема" @click="take(icon)">{{ icon }}</button>
      <MomentIconForm v-if="names" v-slot="{ toggle }" :icon @save="(v) => add({ icon, name: v.name })">
        <button type="button" class="iact add" title="назвати й додати в легенду" @click="toggle"><Icon name="plus" /></button>
      </MomentIconForm>
    </span>
    <MomentIconForm v-slot="{ toggle }" fresh @save="add">
      <button type="button" class="iact add qtip" data-tip="＋ свій значок" aria-label="свій значок" @click="toggle"><Icon name="plus" /></button>
    </MomentIconForm>
    <button type="button" class="iact look qtip" :class="{ on: names }" :aria-pressed="names" :data-tip="names ? 'сховати назви' : 'показати назви'" @click="flip">Aa</button>
  </div>
</template>

<style scoped>
.pal { display: flex; flex-wrap: wrap; align-items: center; gap: .15rem; }
.line { display: inline-flex; align-items: center; gap: .1rem; }
.names .line { padding-right: .35rem; }
/* a brush is its icon on a quiet tile; the one in hand wears a ring of the site's blue */
.brush { display: inline-flex; align-items: center; gap: .3rem; min-width: 1.9rem; height: 1.9rem; padding: 0 .3rem; justify-content: center; border: 0;
         border-radius: .35rem; background: none; font-size: 1.1rem; line-height: 1; }
.brush:hover { background: var(--bs-tertiary-bg); }
.brush.on { background: color-mix(in srgb, var(--bs-primary) 12%, transparent); box-shadow: inset 0 0 0 2px color-mix(in srgb, var(--bs-primary) 70%, transparent); }
.name { max-width: 8rem; overflow: hidden; color: var(--bs-body-color); font-size: .78rem; text-overflow: ellipsis; white-space: nowrap; }
.stray .brush { outline: 1px dashed var(--bs-border-color); outline-offset: -3px; }
.sep { width: 1px; height: 1.3rem; margin: 0 .3rem; background: var(--bs-border-color); }
.line .iact { width: 1.3rem; height: 1.3rem; font-size: .75rem; opacity: .5; }
.line:hover .iact { opacity: 1; }
.look { width: auto; padding: 0 .35rem; margin-left: .2rem; font-size: .75rem; font-weight: 600; }
.look.on { background: color-mix(in srgb, var(--bs-link-color) 12%, transparent); color: var(--bs-link-color); }
</style>
