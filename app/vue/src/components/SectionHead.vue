<script setup>
import Icon from '@core/components/Icon.vue'
import { zones } from '../catalog.js'
import { isFolded, isShort, setShort, toggleFold } from '../fold.js'

// a section's heading in the editor: icon and title, a count, a muted note, and the section's own actions on the right;
// with `fold` (the key it is remembered by, fold.js) a chevron leads the title and a click on either folds the section,
// and a quiet button at the end shows the section in short or in full (T284 §3);
// `zone` — the catalog category the section belongs to: a bar of its colour before the title (T278 §9).
// The heading sticks under the menu while its section is on screen: the reader sees where they are and can fold it away
defineProps({ icon: String, title: String, count: [Number, String], note: String, fold: String, zone: String })
</script>

<template>
  <h2 class="h6 head d-flex flex-wrap align-items-center gap-2">
    <span v-if="zones[zone]" class="bar" :style="{ background: zones[zone].color }" :title="`категорія каталогу: ${zones[zone].title}`" />
    <component :is="fold ? 'button' : 'span'" :type="fold ? 'button' : null" class="name" :class="{ fold }"
               :aria-expanded="fold ? !isFolded(fold) : null" @click="fold && toggleFold(fold)">
      <Icon v-if="fold" :name="isFolded(fold) ? 'right' : 'down'" class="chev" />
      {{ icon }} {{ title }} <span v-if="count !== undefined" class="count">({{ count }})</span>
    </component>
    <span v-if="note" class="note">{{ note }}</span>
    <span class="ms-auto d-flex align-items-center gap-1">
      <slot />
      <button v-if="fold && !isFolded(fold)" type="button" class="iact" :class="{ on: isShort(fold) }"
              :title="isShort(fold) ? 'Показано коротко — показати секцію повністю' : 'Коротко: лише початок секції'" @click="setShort(fold, !isShort(fold))">
        <Icon name="short" />
      </button>
    </span>
  </h2>
</template>

<style scoped>
/* stuck under the menu, over the section's own content; wider than the column by its padding, so nothing shows beside it */
.head { position: sticky; top: var(--nav-h, 0px); z-index: 20; min-height: 2.35rem; margin: 0 -.5rem .5rem; padding: .25rem .5rem; border-bottom: 1px solid var(--bs-border-color);
        background: var(--bs-body-bg); font-weight: 700; }
.bar { width: 4px; height: 1.2em; margin-right: -.2rem; border-radius: 2px; }
.name.fold { padding: 0; border: 0; background: none; color: inherit; font: inherit; text-align: start; }
.chev { font-size: .85em; opacity: .55; }
.name.fold:hover .chev { opacity: 1; }
.count { font-weight: 400; opacity: .55; }
.note { font-size: .8rem; font-weight: 400; color: var(--bs-secondary-color); }
.iact.on { background: var(--bs-secondary-bg); color: var(--bs-body-color); }
</style>
