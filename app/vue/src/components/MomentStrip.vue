<script setup>
import { ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { useMomentEd } from '../momentEd.js'

// the strip of a scenario's frames (T276): thumbnails — a click takes a frame into work, dragging puts it elsewhere, the
// round trash in the corner of the frame in work deletes it; «＋ кадр» puts a copy of the frame in work right after it
const ed = useMomentEd()
const from = ref(-1)
const over = ref(-1)
// a click inside the trash's panel bubbles up here after the frame is gone: it must not pick a frame
const pick = (e, i) => !e.target.closest('.rm') && (ed.at = i)
function drop(i) {
  if (from.value >= 0 && from.value !== i) ed.moveFrame(from.value, i)
  from.value = over.value = -1
}
</script>

<template>
  <div class="d-flex flex-wrap align-items-start gap-2">
    <div v-for="(f, i) in ed.scenario?.frames || []" :key="i" class="thumb" :class="{ on: i === ed.at, over: i === over && from !== i }"
         draggable="true" :title="`кадр ${i + 1}: клік — правити, перетягни — переставити`" @click="pick($event, i)"
         @dragstart="from = i" @dragover.prevent="over = i" @drop.prevent="drop(i)" @dragend="from = over = -1">
      <div class="mini"><div v-for="(row, r) in f.grid" :key="r"><span v-for="(c, k) in row" :key="k" :class="c.mark">{{ c.icon }}</span></div></div>
      <span class="num">{{ i + 1 }}</span>
      <span v-if="i === ed.at" class="rm"><DelButton :what="`кадр ${i + 1}`" @yes="ed.dropFrame(i)" /></span>
    </div>
    <button type="button" class="add" :title="ed.frame ? `копія кадру ${ed.at + 1} — зміни в ній клітину-дві` : 'порожнє поле'" @click="ed.addFrame()">
      <Icon name="plus" /> кадр</button>
  </div>
</template>

<style scoped>
.thumb { position: relative; padding: .2rem; border: 1px solid var(--bs-border-color); border-radius: .375rem; background: var(--bs-tertiary-bg); cursor: pointer; }
.thumb.on { border-color: var(--bs-body-color); box-shadow: 0 0 0 1px var(--bs-body-color); }
.thumb.over { box-shadow: -3px 0 0 var(--act-add); }  /* where the dragged frame lands: before this one */
.mini { max-width: 9rem; max-height: 4.5rem; overflow: hidden; font-size: .42rem; line-height: 1; pointer-events: none; }
.mini > div { display: flex; }
.mini span { display: inline-flex; align-items: center; justify-content: center; width: .55rem; height: .55rem; flex-shrink: 0; }
.mini .who { box-shadow: inset 0 0 0 1px var(--bs-primary); }
.mini .new { box-shadow: inset 0 0 0 1px var(--bs-warning); }
.num { position: absolute; bottom: .1rem; left: .2rem; padding: 0 .2rem; border-radius: .2rem; background: var(--bs-body-bg); font-size: .65rem; opacity: .8; }
.rm { position: absolute; top: -.5rem; right: -.5rem; }
.rm :deep(.iact) { width: 1.35rem; height: 1.35rem; border: 1px solid var(--bs-border-color); border-radius: 50%; background: var(--bs-body-bg); font-size: .75rem; }
.add { display: inline-flex; align-items: center; gap: .3rem; align-self: stretch; min-height: 2.2rem; padding: 0 .65rem; border: 1.5px dashed color-mix(in srgb, var(--act-add) 55%, transparent);
       border-radius: .375rem; background: none; color: var(--act-add); font-size: .8rem; }
.add:hover { border-color: var(--act-add); background: color-mix(in srgb, var(--act-add) 8%, transparent); }
</style>
