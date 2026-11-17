<script setup>
import { computed, nextTick, onMounted, reactive, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import Tip from '@core/components/Tip.vue'
import { deleteClaim, putClaim } from '../api.js'
import { kindOf } from '../catalog.js'
import { useEd } from '../ed.js'
import AskTeacher from './AskTeacher.vue'
import ClaimShots from './ClaimShots.vue'
import MoveTo from './MoveTo.vue'
import SlotFields from './SlotFields.vue'

// the owner's part of a claim's panel: params, proof, note and link (rare — behind «＋ нотатка · ＋ посилання» until filled,
// T291 §4); then move it, delete it or tell the teacher the card belongs elsewhere. An auto-claim follows its part: only its
// note, link and proof are the student's. A rule card not yet on a rule has both ways out on top (T291 §8). `linkFirst` —
// opened for the link («＋ посилання» in a table of links): the cursor starts there
const props = defineProps({ claim: Object, linkFirst: Boolean })
const emit = defineEmits(['close'])
const ed = useEd()
const info = computed(() => ed.info(props.claim.task))
const title = computed(() => info.value?.title || props.claim.task)
const ruleDraft = computed(() => !props.claim.auto && !props.claim.rule && kindOf(info.value) === 'rule')
const form = reactive({ params: { ...props.claim.params }, note: props.claim.note || '', link: props.claim.link || '' })
const shown = reactive({ note: !!form.note, link: !!form.link || props.linkFirst })
const moving = ref(false)
const error = ref('')
const noteBox = ref()
const linkBox = ref()
const boxes = { note: noteBox, link: linkBox }
onMounted(() => props.linkFirst && linkBox.value?.focus())
async function more(field) {
  shown[field] = true
  await nextTick()
  boxes[field].value?.focus()
}

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
// the rule's form opens from the card's blank, and saving it takes this claim along
function newRule() {
  ed.open('rule', { ...info.value?.rule, claim: props.claim.id })
  emit('close')
}
</script>

<template>
  <div class="vstack gap-2">
    <div v-if="ruleDraft" class="vstack gap-1">
      <Tip id="claim-rule-draft">Картка чекає на правило: почни нове з її заготовки або привʼяжи до правила, що вже є</Tip>
      <div class="d-flex flex-wrap align-items-center gap-2">
        <button type="button" class="btn btn-sm btn-add" @click="newRule"><Icon name="plus" /> нове правило з цієї картки</button>
        <button type="button" class="iact wide" :class="{ on: moving }" @click="moving = !moving">
          привʼязати до наявного <Icon :name="moving ? 'down' : 'right'" />
        </button>
      </div>
      <MoveTo v-if="moving" :claim no-new @pick="move" />
    </div>
    <div v-if="!claim.auto && info?.slots?.length" class="d-flex flex-wrap gap-2 align-items-center">
      <SlotFields :specs="info.slots" :params="form.params" />
    </div>
    <input v-if="shown.note" ref="noteBox" v-model="form.note" class="form-control form-control-sm" placeholder="Нотатка: як саме це зроблено" @keydown.enter="save">
    <input v-if="shown.link" ref="linkBox" v-model="form.link" class="form-control form-control-sm" @keydown.enter="save"
           :placeholder="info?.zone === 'support' ? 'Посилання: відео, сторінка гри, документ' : 'GitHub: файл або коміт — за бажанням'">
    <ClaimShots :claim editable />
    <div v-if="!shown.note || !shown.link" class="d-flex gap-3">
      <button v-if="!shown.note" type="button" class="more-field" @click="more('note')"><Icon name="plus" /> нотатка</button>
      <button v-if="!shown.link" type="button" class="more-field" @click="more('link')"><Icon name="plus" /> посилання</button>
    </div>
    <div class="d-flex gap-2">
      <button type="button" class="btn btn-sm btn-success" @click="save"><Icon name="check" /> Зберегти</button>
      <button type="button" class="btn btn-sm btn-outline-secondary" @click="emit('close')">Скасувати</button>
    </div>
    <div v-if="error" class="text-danger small">{{ error }}</div>
    <div class="vstack gap-2 pt-2 border-top">
      <Tip v-if="claim.auto" id="claim-auto">Тримається сама: зміни тип, параметр чи властивість — зміниться й вона</Tip>
      <template v-else>
        <div class="d-flex align-items-center">
          <button v-if="!ruleDraft" type="button" class="iact wide" :class="{ on: moving }" @click="moving = !moving"><Icon name="move" /> Перемістити</button>
          <DelButton class="ms-auto" :what="`заявку «${title}»`" @yes="remove" />
        </div>
        <MoveTo v-if="moving && !ruleDraft" :claim @pick="move" @rule="newRule" />
      </template>
      <AskTeacher :task="claim.task" />
    </div>
  </div>
</template>

<style scoped>
.iact.wide { width: auto; gap: .3rem; padding: 0 .45rem; font-size: .8rem; }
.iact.on { background: var(--bs-tertiary-bg); color: var(--bs-body-color); }
</style>
