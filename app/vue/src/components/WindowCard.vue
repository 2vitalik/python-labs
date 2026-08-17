<script setup>
import { computed, reactive, ref } from 'vue'

import { deletePart, postClaim, putPart } from '../api.js'
import { PAIRS } from '../catalog.js'
import ClaimPicker from './ClaimPicker.vue'
import ClaimRow from './ClaimRow.vue'
import CoinBadge from './CoinBadge.vue'
import ShotStrip from './ShotStrip.vue'

const props = defineProps({ part: Object, claims: Array, gameClaims: Array, info: Function })
const emit = defineEmits(['changed'])
const edit = ref(false)
const arm = ref(false)
const error = ref('')
const form = reactive({ title: props.part.title, description: props.part.description })

const own = computed(() => props.claims.filter((c) => c.task !== props.part.task))
const typeInfo = computed(() => props.info(props.part.task))
// claimed element implies a game-level function (volume control → volume actually works)
const hints = computed(() => props.claims.map((c) => PAIRS[c.task])
  .filter((slug) => slug && !props.gameClaims.some((c) => c.task === slug)))

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
const addClaim = (task, part = props.part.id) => run(() => postClaim({ task, part }))
</script>

<template>
  <div class="card h-100">
    <div class="card-body vstack gap-2">
      <div class="d-flex align-items-center gap-2">
        <template v-if="!edit">
          <span class="fw-semibold">{{ part.title }}</span>
          <span class="badge text-bg-light border text-secondary fw-normal">
            <CoinBadge :coin="typeInfo?.coin" :amount="typeInfo?.amount" /> {{ typeInfo?.title || part.task }}
          </span>
          <span class="ms-auto" role="button" title="Редагувати" @click="edit = true">✏️</span>
          <span v-if="!arm" role="button" title="Видалити вікно" @click="arm = true">🗑️</span>
          <button v-else class="btn btn-danger btn-sm" @mouseleave="arm = false" @click="remove">Точно видалити?</button>
        </template>
        <template v-else>
          <input v-model="form.title" class="form-control form-control-sm">
          <button class="btn btn-primary btn-sm" @click="save">💾</button>
          <button class="btn btn-outline-secondary btn-sm" @click="edit = false">✕</button>
        </template>
      </div>
      <textarea v-if="edit" v-model="form.description" class="form-control form-control-sm" rows="2"
                placeholder="Опис вікна"></textarea>
      <div v-else-if="part.description" class="text-secondary small">{{ part.description }}</div>
      <ShotStrip :part="part" @changed="emit('changed')" />
      <div v-if="own.length" class="d-flex flex-wrap gap-1 align-items-start">
        <ClaimRow v-for="c in own" :key="c.id" :claim="c" :info="info(c.task)" @changed="emit('changed')" />
      </div>
      <ClaimPicker placeholder="＋ елемент чи заявка на цьому вікні…" @pick="addClaim" />
      <div v-for="slug in hints" :key="slug" class="small text-secondary">
        💡 Є елемент — заяви й функцію
        <a href="#" @click.prevent="addClaim(slug, '')">«{{ info(slug)?.title || slug }}»</a> (рівень гри)
      </div>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>
