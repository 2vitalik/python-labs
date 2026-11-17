<script setup>
import { inject, ref } from 'vue'

import { setFolders } from '../viewStore.js'
import DelButton from './DelButton.vue'
import Icon from './Icon.vue'
import InlineText from './InlineText.vue'
import ViewRow from './ViewRow.vue'

// one folder of the library (T315 §8): its name renamed in place with all its views, the count; an empty one can go.
// `name` '' — the views in no folder: no head. The whole section takes a drop (`drag` — the folders' one useDragSort);
// a row is draggable only while its grip is held, so its words can still be selected and edited
const props = defineProps({ name: { type: String, default: '' }, list: { type: Array, required: true }, total: Number, drag: { type: Object, required: true }, canDrag: Boolean })
const lib = inject('viewsLib')
const armed = ref('')  // the row whose grip is down
function grab(slug) {
  armed.value = slug
  addEventListener('mouseup', () => (armed.value = ''), { once: true })
}
// a link or selected words dragged out of a row would start moving the row: only the grip does
function guard(e) {
  if (armed.value) return
  e.preventDefault()
  e.stopPropagation()
}
const rename = (to) => setFolders({ rename: [props.name, to] })
const remove = () => lib.act(() => setFolders({ rename: [props.name, ''] }))
</script>

<template>
  <section class="vfold" v-bind="drag.zone(name, list.length)" @dragstart.capture="guard">
    <h2 v-if="name" :id="`folder-${name}`" class="vfold-head">
      <Icon name="folder" />
      <InlineText :value="name" :save="rename" can required />
      <span class="vfold-n">{{ total }}</span>
      <DelButton v-if="!total" :what="`папку «${name}»`" note="у ній нема жодного виду" title="Прибрати порожню папку" @yes="remove" />
    </h2>
    <TransitionGroup tag="ul" name="vrows" class="vfold-list">
      <ViewRow v-for="(v, i) in list" :key="v.slug" :view="v" :can-drag v-bind="drag.item(i, name)" :draggable="armed === v.slug"
               @grab="grab(v.slug)" @dragend="armed = ''" />
    </TransitionGroup>
    <p v-if="!list.length" class="vfold-empty">{{ name ? 'перетягни сюди вид' : 'перетягни сюди вид, щоб вийняти його з папки' }}</p>
  </section>
</template>

<style scoped>
.vfold { padding-bottom: .25rem; border-radius: .4rem; }
.vfold + .vfold { margin-top: 1.1rem; }
.vfold-head { display: flex; align-items: center; gap: .4rem; margin: 0 0 .15rem; font-size: 1rem; font-weight: 600; }
.vfold-head > .icon { color: var(--bs-secondary-color); }
.vfold-n { font-size: .8rem; font-weight: 400; color: var(--bs-secondary-color); }
.vfold-list { margin: 0; padding: 0; list-style: none; }
.vfold-empty { margin: 0; padding: .55rem .75rem; border: 1px dashed var(--bs-border-color); border-radius: .4rem; font-size: .8rem; color: var(--bs-secondary-color); }
/* rows come, go and change places gliding */
.vrows-enter-active, .vrows-leave-active, .vrows-move { transition: opacity .2s ease, transform .2s ease; }
.vrows-enter-from, .vrows-leave-to { opacity: 0; transform: translateY(-.35rem); }
@media (prefers-reduced-motion: reduce) { .vrows-enter-active, .vrows-leave-active, .vrows-move { transition: none; } }
</style>
