<script setup>
import { computed, reactive, ref } from 'vue'

import { deletePart, postClaim, putPart } from '../api.js'
import { PAIRS } from '../catalog.js'
import CardPicker from './CardPicker.vue'
import ClaimChip from './ClaimChip.vue'
import CoinBadge from './CoinBadge.vue'
import MenuItems from './MenuItems.vue'
import ShotStrip from './ShotStrip.vue'

// a window of the game: its type from the catalog, a screenshot, the elements on it (claims), its menu
const props = defineProps({ part: Object, menus: Array, windows: Array, claims: Array, gameClaims: Array, parts: Array, info: Function, editable: Boolean, judge: Boolean, nick: String })
const emit = defineEmits(['changed'])
const edit = ref(false)
const arm = ref(false)
const error = ref('')
const form = reactive({ title: props.part.title, description: props.part.description })
const own = computed(() => props.claims.filter((c) => c.task !== props.part.task))
const typeInfo = computed(() => props.info(props.part.task))
// claimed element implies a game-level function (volume control → volume actually works)
const hints = computed(() => props.claims.map((c) => PAIRS[c.task]).filter((slug) => slug && !props.gameClaims.some((c) => c.task === slug)))
const ui = (t) => t.zone === 'interface' || t.zone === 'game-logic'

async function run(fn) {
  error.value = ''
  try {
    await fn()
    emit('changed')
  } catch (e) {
    error.value = e.message
  }
}
const save = () => run(async () => { await putPart(props.part.id, form); edit.value = false })
const remove = () => run(() => deletePart(props.part.id))
const addClaim = (task, params) => run(() => postClaim({ task, part: props.part.id, params }))
const addHint = (task) => run(() => postClaim({ task }))  // game-level, no params
</script>

<template>
  <div :id="`p-${part.id}`" class="card h-100">
    <div class="card-body p-2 vstack gap-2">
      <div class="d-flex align-items-start gap-2">
        <template v-if="!edit">
          <span>🪟</span>
          <div class="head d-flex flex-wrap align-items-center column-gap-2 row-gap-1 flex-grow-1">
            <span class="fw-semibold">{{ part.title }}</span>
            <span class="badge text-bg-light border text-secondary fw-normal text-wrap text-start"><CoinBadge :coin="typeInfo?.coin" :amount="typeInfo?.amount" /> {{ typeInfo?.title || part.task }}</span>
          </div>
          <template v-if="editable">
            <span class="act" role="button" title="Редагувати" @click="edit = true">✏️</span>
            <span v-if="!arm" class="act" role="button" title="Видалити вікно" @click="arm = true">🗑️</span>
            <button v-else class="btn btn-danger btn-sm py-0" @mouseleave="arm = false" @click="remove">Точно видалити?</button>
          </template>
        </template>
        <template v-else>
          <input v-model="form.title" class="form-control form-control-sm">
          <button class="btn btn-primary btn-sm" @click="save">💾</button>
          <button class="btn btn-outline-secondary btn-sm" @click="edit = false">✕</button>
        </template>
      </div>
      <input v-if="edit" v-model="form.description" class="form-control form-control-sm" placeholder="Що на цьому вікні">
      <div v-else-if="part.description" class="text-secondary small">{{ part.description }}</div>
      <ShotStrip v-if="editable || part.screenshots.length" :part :editable @changed="emit('changed')" />
      <MenuItems :window="part" :menu="menus[0]" :windows :info :editable @changed="emit('changed')" />
      <div v-if="own.length" class="d-flex flex-wrap gap-1 align-items-start">
        <ClaimChip v-for="c in own" :key="c.id" :claim="c" :info="info(c.task)" :parts :editable :judge :nick @changed="emit('changed')" />
      </div>
      <CardPicker v-if="editable" placeholder="＋ елемент на вікні: лічильник, слайдер, кнопка, підсвітка…" :filter="ui"
                  :claimed="new Set(claims.map((c) => c.task))" @pick="addClaim" />
      <div v-for="slug in hints" :key="slug" class="small text-secondary">
        💡 Є елемент — заяви й функцію <a href="#" @click.prevent="addHint(slug)">«{{ info(slug)?.title || slug }}»</a> (рівень гри)
      </div>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
/* the title and the window type wrap inside their own block — on a phone ✏️ 🗑️ stay in the card */
.head { min-width: 0; overflow-wrap: anywhere; }
.act { opacity: .6; }
.act:hover { opacity: 1; }
</style>
