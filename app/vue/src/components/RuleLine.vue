<script setup>
import { computed } from 'vue'

import Icon from '@core/components/Icon.vue'
import { specOf } from '../rules.js'
import ArgFields from './ArgFields.vue'
import WordPick from './WordPick.vue'

// one word of the rule's form on its own line: «не» · the word · its arguments · take the line off
const props = defineProps({ item: Object, dic: String, sides: Array, when: Object, placeholder: String, negatable: Boolean, removable: Boolean })
defineEmits(['remove'])
const spec = computed(() => specOf(props.dic, props.item.kind))
// another word starts clean: the old one's arguments mean nothing to it
function setWord(kind) {
  for (const k of Object.keys(props.item)) if (k !== 'not') delete props.item[k]
  props.item.kind = kind
}
</script>

<template>
  <div class="rline">
    <button v-if="negatable" type="button" class="btn btn-sm not" :class="item.not ? 'btn-danger' : 'btn-outline-secondary'"
            title="заперечення: умова НЕ виконується" :aria-pressed="!!item.not" @click="item.not = !item.not">не</button>
    <WordPick :model-value="item.kind" :dic :placeholder @update:model-value="setWord" />
    <ArgFields v-if="spec" :spec :item :sides :when />
    <button v-if="removable" type="button" class="iact del" title="Прибрати рядок" @click="$emit('remove')"><Icon name="minus" /></button>
  </div>
</template>

<style scoped>
.rline { display: flex; flex-wrap: wrap; align-items: center; gap: .3rem; min-width: 0; }
.not { --bs-btn-padding-y: .05rem; --bs-btn-padding-x: .35rem; --bs-btn-font-size: .75rem; }
</style>
