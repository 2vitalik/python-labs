<script setup>
import { computed, nextTick, onMounted, ref } from 'vue'

import Icon from './Icon.vue'
import { mark, search, words } from '../pick.js'

// one list to choose anything from (T270 §5): it opens with every option at once, typing filters it and each row says
// why it matched. items: [{ key, title, icon?, hint?, desc?, group?, words?: [synonyms], taken?, tag?: { text, title } }]
// → emits pick(item); `tag` — a quiet word by the title, its row dimmed.
// `inline` — the list is part of the flow (inside a Pop); otherwise it drops under the field while the field has focus.
const props = defineProps({ items: Array, placeholder: { type: String, default: 'пошук…' }, inline: Boolean, autofocus: Boolean, small: Boolean })
const emit = defineEmits(['pick'])
const q = ref('')
const open = ref(false)
const cursor = ref(0)
const input = ref()
const list = ref()
const qs = computed(() => words(q.value))
const rows = computed(() => search(props.items, qs.value))

function pick(it) {
  q.value = ''
  cursor.value = 0
  if (!props.inline) input.value.blur()
  emit('pick', it)
}
function key(e) {
  if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
    open.value = true
    cursor.value = Math.max(0, Math.min(rows.value.length - 1, cursor.value + (e.key === 'ArrowDown' ? 1 : -1)))
    nextTick(() => list.value?.querySelector('.active')?.scrollIntoView({ block: 'nearest' }))
    e.preventDefault()
  } else if (e.key === 'Enter') {
    if (rows.value[cursor.value]) pick(rows.value[cursor.value])
    e.preventDefault()
  } else if (e.key === 'Escape' && !props.inline) input.value.blur()
}
onMounted(() => props.autofocus && nextTick(() => input.value?.focus()))
defineExpose({ focus: () => input.value?.focus() })
</script>

<template>
  <div class="picker" :class="{ inline }">
    <input ref="input" v-model="q" class="form-control" :class="{ 'form-control-sm': small }" :placeholder autocomplete="off"
           @focus="open = true" @blur="open = false" @input="cursor = 0; open = true" @keydown="key">
    <div v-if="inline || open" ref="list" class="rows" :class="{ 'shadow border rounded bg-body': !inline }" @mousedown.prevent>
      <template v-for="(it, i) in rows" :key="it.key">
        <div v-if="!qs.length && it.group && it.group !== rows[i - 1]?.group" class="group">{{ it.group }}</div>
        <button type="button" class="pick" :class="{ active: i === cursor, tagged: it.tag }" @click="pick(it)" @mousemove="cursor = i">
          <span v-if="it.icon" class="ico">{{ it.icon }}</span>
          <span class="body">
            <span class="ttl" v-html="mark(it.title, qs)"></span>
            <span v-if="it.tag" class="tag" :title="it.tag.title">{{ it.tag.text }}</span>
            <span v-if="it.taken" class="text-success ms-1" title="уже є"><Icon name="done" /></span>
            <span v-if="it.why || it.desc" class="sub" v-html="mark(it.why || it.desc, qs)"></span>
          </span>
          <span v-if="it.hint || (qs.length && it.group)" class="hint">{{ it.hint || it.group }}</span>
        </button>
      </template>
      <div v-if="!rows.length" class="none">Нічого не знайшлось — спробуй інше слово.</div>
      <slot name="footer" :q="q" />
    </div>
  </div>
</template>

<style scoped>
.picker { position: relative; }
.rows { max-height: 20rem; overflow-y: auto; }
.picker:not(.inline) .rows { position: absolute; z-index: 30; top: calc(100% + .2rem); left: 0; right: 0; min-width: 17rem; }
.inline .rows { margin-top: .35rem; max-height: 17rem; }
.group { margin: .4rem .5rem .1rem; font-size: .65rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
.pick { display: flex; align-items: baseline; gap: .45rem; width: 100%; padding: .22rem .5rem; border: 0; background: none; color: inherit; text-align: start; font-size: .85rem; }
.pick.active { background: var(--bs-tertiary-bg); }
.ico { flex-shrink: 0; min-width: 1.25rem; text-align: center; }
.body { flex-grow: 1; min-width: 0; }
.sub { display: block; overflow: hidden; font-size: .75rem; color: var(--bs-secondary-color); text-overflow: ellipsis; white-space: nowrap; }
.hint { flex-shrink: 0; font-size: .72rem; color: var(--bs-secondary-color); white-space: nowrap; }
.tagged .ico, .tagged .ttl { opacity: .7; }
.tag { margin-left: .35rem; padding: 0 .25rem; border: 1px dashed var(--bs-border-color); border-radius: .25rem; font-size: .66rem;
       color: var(--bs-secondary-color); white-space: nowrap; }
.none { padding: .35rem .5rem; font-size: .8rem; color: var(--bs-secondary-color); }
</style>
