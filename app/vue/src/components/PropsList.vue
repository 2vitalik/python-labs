<script setup>
import { computed } from 'vue'

import InlinePop from '@core/components/InlinePop.vue'
import InlineText from '@core/components/InlineText.vue'
import { vPeek } from '@core/peek.js'
import OptionCards from './OptionCards.vue'

// properties to read (T270 §8): «Сітка: 🔲 квадратна» in two columns, only the filled ones; `specs` — rows of vocab.field /
// vocab.level; the default slot is what to say when nothing is filled. A chosen option that is a catalog card shows the
// card under the mouse (T291 §6). With `can` the owner changes a property where it reads (T306): a choice — in a floating
// panel of its tiles, saved on a click (several in a row where the property takes several); a text or words — in place.
// `all` (the card's tools, T310) — the unset ones stand there too, as a quiet word to click: «не вказано», or, `inherit`
// (a level's), «як у поля». `save(key, value)` is awaited
const p = defineProps({ props: { type: Object, default: () => ({}) }, specs: { type: Array, default: () => [] }, can: Boolean, save: Function,
  all: Boolean, inherit: Boolean })
// `none` — how v2 stored «no gravity»: now an unset property says the same
const empty = (v) => v == null || v === '' || v === false || v === 'none' || (Array.isArray(v) && !v.length)
// an option the vocab no longer knows is shown as it is stored
const option = (s, v) => {
  const o = s.options?.[v]
  return { text: !o ? v : typeof o === 'string' ? o : [o.icon, o.label].filter(Boolean).join(' '), slug: o?.slug, desc: o?.desc }
}
const values = (s, v) => (s.type === 'bool' ? [{ text: 'так' }] : s.type === 'choice' ? [].concat(v).map((x) => option(s, x))
  : [{ text: Array.isArray(v) ? v.join(' · ') : String(v) }])
const none = (s) => (p.inherit ? 'як у поля' : s.type === 'bool' ? 'ні' : 'не вказано')
const rows = computed(() => p.specs.filter((s) => p.all || !empty(p.props?.[s.key])).map((s) => {
  const set = !empty(p.props?.[s.key])
  return { spec: s, key: s.key, label: s.label.split(/[:(]/)[0].trim(), full: s.label, set, values: set ? values(s, p.props[s.key]) : [], none: none(s) }
}))
const words = (v) => [].concat(v || []).join(', ')
const split = (line) => line.split(',').map((x) => x.trim()).filter(Boolean)
</script>

<template>
  <div v-if="rows.length || $slots.default" class="plist small">
    <TransitionGroup name="toolrow">
      <div v-for="r in rows" :key="r.key" class="prop">
        <span class="text-secondary" :title="r.full">{{ r.label }}:</span>{{ ' ' }}
        <InlineText v-if="r.spec.type === 'text'" :value="r.set ? String(props[r.key]) : ''" :can :placeholder="r.spec.hint" :save="(v) => save(r.key, v)">
          <template #empty><span class="inl-none">{{ r.none }}</span></template>
        </InlineText>
        <InlineText v-else-if="r.spec.type === 'tags'" :value="words(props[r.key])" :can placeholder="слова через кому" :save="(v) => save(r.key, split(v))">
          {{ r.values[0]?.text }}
          <template #empty><span class="inl-none">{{ r.none }}</span></template>
        </InlineText>
        <InlinePop v-else :can width="20rem">
          <template #default="{ open }">
            <span v-if="!r.set" class="inl-none">{{ r.none }}</span>
            <template v-for="(o, i) in r.values" :key="i">{{ i ? ' · ' : '' }}<span v-peek="open || !o.slug ? null : { kind: 'task', id: o.slug }"
              :title="o.slug ? null : o.desc">{{ o.text }}</span></template>
          </template>
          <template #panel="{ choose }">
            <div class="cap">{{ r.full }}</div>
            <label v-if="r.spec.type === 'bool'" class="form-check m-0">
              <input type="checkbox" class="form-check-input" :checked="r.set" @change="choose(save(r.key, $event.target.checked))"> так
            </label>
            <OptionCards v-else :model-value="props[r.key]" :options="r.spec.options" :multi="r.spec.multi" compact
                         @update:model-value="(v) => choose(save(r.key, v), { keep: r.spec.multi })" />
          </template>
        </InlinePop>
      </div>
    </TransitionGroup>
    <slot v-if="!rows.length" />
  </div>
</template>

<style scoped>
.plist { columns: 2 12rem; column-gap: 1.5rem; }
.prop { break-inside: avoid; padding: .05rem 0; }
.cap { margin-bottom: .35rem; font-size: .8rem; color: var(--bs-secondary-color); }
</style>
