<script setup>
import { computed, ref } from 'vue'

import { useTable } from '../tableCtx.js'
import { createView, liveViews } from '../viewStore.js'
import Icon from './Icon.vue'
import ViewIcon from './ViewIcon.vue'
import ViewName from './ViewName.vue'

// «З чого почати» (T315 §7): a new view is made of what is on screen now, or of an etalon — a view marked as good to start
// from, with its «для чого» under it. A click on a row picks the base; the name under the list makes the view and opens it.
// No emoji typed — the base's icon goes with it
const emit = defineEmits(['close'])
const t = useTable()
const etalons = computed(() => liveViews().filter((v) => v.etalon))
const base = ref('')  // an etalon's slug; '' — what is on screen
const blocked = computed(() => (!base.value && !t.view ? 'Обери, з чого почати' : ''))

async function make({ title, emoji }) {
  const b = etalons.value.find((v) => v.slug === base.value)
  if (!b) await t.fork({ title, emoji: emoji || t.view.emoji })
  else {
    const v = await createView({ title, emoji: emoji || b.emoji, query: b.query, parent: b.slug, parent_version: b.version, folder: b.folder })
    t.open(v.slug)
  }
  emit('close')
}
</script>

<template>
  <div>
    <div class="small text-secondary mb-1">З чого почати</div>
    <div class="bases">
      <button v-if="t.view" type="button" class="base" :class="{ on: !base }" @click="base = ''">
        <span class="ic"><Icon name="cols3" /></span>
        <span class="txt"><span>Те, що зараз на екрані</span>
          <small>{{ t.view.emoji }} {{ t.view.title }}<template v-if="t.dirty"> · зі змінами</template></small></span>
      </button>
      <button v-for="v in etalons" :key="v.slug" type="button" class="base" :class="{ on: base === v.slug }" @click="base = v.slug">
        <span class="ic"><ViewIcon :view="v" /></span>
        <span class="txt"><span class="text-truncate">{{ v.title }}</span><small v-if="v.about" class="about">{{ v.about }}</small></span>
      </button>
    </div>
    <p v-if="!etalons.length" class="small text-secondary mt-1 mb-0">Еталонів ще нема: зірка біля назви виду робить його еталоном</p>
    <ViewName class="mt-2" :go="make" :blocked @cancel="emit('close')" />
  </div>
</template>

<style scoped>
.bases { display: flex; flex-direction: column; gap: .1rem; max-height: 50vh; overflow-y: auto; }
.base { display: flex; align-items: flex-start; gap: .5rem; width: 100%; padding: .3rem .45rem; border: 0; border-radius: .35rem; background: none;
        color: var(--bs-body-color); text-align: start; }
.base:hover { background: var(--bs-tertiary-bg); }
.base.on { background: color-mix(in srgb, var(--act-add) 12%, transparent); box-shadow: inset 2px 0 0 var(--act-add); }
.ic { display: inline-flex; justify-content: center; width: 1.4rem; flex-shrink: 0; font-size: 1.05rem; line-height: 1.3; color: var(--bs-secondary-color); }
.txt { display: flex; flex-direction: column; min-width: 0; }
.txt small { color: var(--bs-secondary-color); font-size: .75rem; }
.about { display: -webkit-box; overflow: hidden; -webkit-box-orient: vertical; -webkit-line-clamp: 2; }
</style>
