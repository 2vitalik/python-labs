<script setup>
import { computed, reactive, ref } from 'vue'

import { deleteClaim, putClaim } from '../api.js'
import { paramsText } from '../catalog.js'
import CoinBadge from './CoinBadge.vue'
import SlotFields from './SlotFields.vue'

const props = defineProps({ claim: Object, info: Object })
const emit = defineEmits(['changed'])
const open = ref(false)
const form = reactive({ params: { ...props.claim.params }, note: props.claim.note, link: props.claim.link })
const ptext = computed(() => paramsText(props.info, props.claim.params))

async function save() {
  await putClaim(props.claim.id, form)
  open.value = false
  emit('changed')
}

async function remove() {
  await deleteClaim(props.claim.id)
  emit('changed')
}
</script>

<template>
  <div>
    <span class="badge rounded-pill text-bg-light border text-dark fw-normal" role="button"
          :title="claim.note" @click="open = !open">
      <CoinBadge :coin="info?.coin" :amount="info?.amount" /> {{ info?.title || claim.task }}
      <span v-if="ptext" class="text-secondary">· {{ ptext }}</span>
      <a v-if="claim.link" :href="claim.link" target="_blank" class="text-decoration-none" @click.stop>🔗</a>
      <span v-if="claim.note">💬</span>
      <span class="ms-1 text-secondary" role="button" title="Прибрати заявку" @click.stop="remove">✕</span>
    </span>
    <div v-if="open" class="d-flex gap-1 flex-wrap my-1">
      <SlotFields v-if="info?.slots?.length" :specs="info.slots" :params="form.params" />
      <div class="input-group input-group-sm w-auto flex-grow-1">
        <input v-model="form.note" class="form-control" placeholder="Нотатка">
        <input v-model="form.link" class="form-control" placeholder="GitHub-посилання">
        <button class="btn btn-outline-primary" @click="save">💾</button>
      </div>
    </div>
  </div>
</template>
