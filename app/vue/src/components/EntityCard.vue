<script setup>
import { computed, ref } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import { deletePart } from '../api.js'
import { iconOf, roleOf } from '../catalog.js'
import { useEd } from '../ed.js'
import CardPicker from './CardPicker.vue'
import ClaimRow from './ClaimRow.vue'
import EntityForm from './EntityForm.vue'
import EntityRules from './EntityRules.vue'
import EntityStats from './EntityStats.vue'
import JudgeMark from './JudgeMark.vue'
import ShotStrip from './ShotStrip.vue'

// an inhabitant of the field (T270 §7): icon, name, type; the description, stats and states, screenshots, the mechanics
// claimed on it and the rules that name it. The pencil turns the card into its form in place
const props = defineProps({ part: Object })
const ed = useEd()
const edit = ref(false)
const error = ref('')
const role = computed(() => roleOf(props.part.role))
const claims = computed(() => ed.claimsOf(props.part.id))
const auto = computed(() => claims.value.filter((c) => c.auto))
const mechanics = computed(() => claims.value.filter((c) => !c.auto))
const roleClaim = computed(() => (role.value.slug ? auto.value.find((c) => c.task === role.value.slug) : null))
const bare = computed(() => ed.editable && !edit.value && !props.part.description && !props.part.screenshots?.length)

async function remove() {
  error.value = ''
  try {
    await deletePart(props.part.id)
    ed.changed()
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div :id="`p-${part.id}`" class="card" :class="{ bare }">
    <div class="card-body p-2 vstack gap-2">
      <EntityForm v-if="edit" :part @done="edit = false" @cancel="edit = false" />
      <template v-else>
        <div class="d-flex align-items-center gap-2">
          <span class="ico">{{ iconOf(part) }}</span>
          <span class="fw-semibold">{{ part.title }}</span>
          <span class="type" :title="role.desc">{{ (role.label || '').toLowerCase() }}<JudgeMark :claim="roleClaim" /></span>
          <span v-if="ed.editable" class="ms-auto d-flex">
            <button type="button" class="iact" title="Редагувати" @click="edit = true"><Icon name="pencil" /></button>
            <DelButton :what="`сутність «${part.title}»`" note="разом з її правилами й заявками" @yes="remove" />
          </span>
        </div>
        <div v-if="bare" class="unsaid">ще не описано — олівець: назва, опис, скриншот</div>
        <div v-if="part.description" class="desc">{{ part.description }}</div>
        <EntityStats v-if="!ed.simple" :part :auto />
        <ShotStrip :part />
        <template v-if="!ed.simple">
          <div v-if="mechanics.length || ed.editable" class="vstack gap-1">
            <div class="label">Механіки</div>
            <ClaimRow v-for="c in mechanics" :key="c.id" :claim="c" />
            <div><CardPicker :kinds="['mechanic']" :anchor="{ part: part.id }" label="механіка" /></div>
          </div>
          <EntityRules :part />
        </template>
        <div v-if="error" class="text-danger small">{{ error }}</div>
      </template>
    </div>
  </div>
</template>

<style scoped>
.ico { font-size: 1.5rem; line-height: 1; }
.type { font-size: .8rem; color: var(--bs-secondary-color); }
.desc { font-size: .85rem; }
/* fresh from the catalog's «＋» and not yet told about (T274 §3): the owner sees what is still to fill */
.card.bare { border-style: dashed; border-color: color-mix(in srgb, var(--bs-danger) 40%, var(--bs-border-color)); }
.unsaid { font-size: .75rem; color: color-mix(in srgb, var(--bs-danger-text-emphasis) 75%, var(--bs-secondary-color)); }
.label { font-size: .7rem; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; color: var(--bs-secondary-color); }
</style>
