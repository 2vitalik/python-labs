<script setup>
import { computed, reactive, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deleteClaim, putClaim } from '../api.js'
import { useEd } from '../ed.js'
import AskTeacher from './AskTeacher.vue'
import MoveTo from './MoveTo.vue'
import SlotFields from './SlotFields.vue'

// the owner's part of a claim's panel: params, note, link; then move it, delete it or tell the teacher the card belongs
// elsewhere. An auto-claim follows its part: only its note and link are the student's
const props = defineProps({ claim: Object })
const emit = defineEmits(['close'])
const ed = useEd()
const info = computed(() => ed.info(props.claim.task))
const title = computed(() => info.value?.title || props.claim.task)
const form = reactive({ params: { ...props.claim.params }, note: props.claim.note || '', link: props.claim.link || '' })
const moving = ref(false)
const error = ref('')

async function run(call) {
  error.value = ''
  try {
    await call()
    ed.changed()
    emit('close')
  } catch (e) {
    error.value = e.message
  }
}
const save = () => run(() => putClaim(props.claim.id, props.claim.auto ? { note: form.note, link: form.link } : form))
const move = (to) => run(() => putClaim(props.claim.id, { ...form, ...to }))
const remove = () => run(() => deleteClaim(props.claim.id))
// a rule card with no rule to sit on: the rule's form opens from the card's blank, and saving it takes this claim along
function newRule() {
  ed.open('rule', { ...info.value?.rule, claim: props.claim.id })
  emit('close')
}
</script>

<template>
  <div class="vstack gap-2">
    <div v-if="!claim.auto && info?.slots?.length" class="d-flex flex-wrap gap-2 align-items-center">
      <SlotFields :specs="info.slots" :params="form.params" />
    </div>
    <input v-model="form.note" class="form-control form-control-sm" placeholder="Нотатка: як саме це зроблено">
    <input v-model="form.link" class="form-control form-control-sm" placeholder="GitHub: файл або коміт — за бажанням">
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('close')">Скасувати</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
    <div class="vstack gap-2 pt-2 border-top">
      <div v-if="claim.auto" class="text-secondary small">тримається сама: зміни тип, параметр чи властивість — зміниться й вона</div>
      <template v-else>
        <div class="d-flex align-items-center">
          <button type="button" class="iact wide" :class="{ on: moving }" @click="moving = !moving"><Icon name="move" /> Перемістити</button>
          <DelButton class="ms-auto" :what="`заявку «${title}»`" @yes="remove" />
        </div>
        <MoveTo v-if="moving" :claim @pick="move" @rule="newRule" />
      </template>
      <AskTeacher :task="claim.task" />
    </div>
  </div>
</template>

<style scoped>
.iact.wide { width: auto; gap: .3rem; padding: 0 .45rem; font-size: .8rem; }
.iact.on { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
</style>
