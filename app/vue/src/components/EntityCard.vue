<script setup>
import { computed, ref, watch } from 'vue'

import DelButton from '@core/components/DelButton.vue'
import Icon from '@core/components/Icon.vue'
import InlineText from '@core/components/InlineText.vue'
import { vPeek } from '@core/peek.js'
import { vToStart } from '@core/toStart.js'
import { deletePart } from '../api.js'
import { roleOf, zones } from '../catalog.js'
import { useEd } from '../ed.js'
import { roleItems } from '../items.js'
import { target } from '../jump.js'
import { isShut, toggleCard } from '../looks.js'
import { mentions } from '../rules.js'
import CardFold from './CardFold.vue'
import CardPicker from './CardPicker.vue'
import CardShut from './CardShut.vue'
import ClaimRow from './ClaimRow.vue'
import EmojiPick from './EmojiPick.vue'
import EntityForm from './EntityForm.vue'
import EntityRules from './EntityRules.vue'
import EntityStats from './EntityStats.vue'
import InlinePick from './InlinePick.vue'
import JudgeMark from './JudgeMark.vue'
import PartBlock from './PartBlock.vue'
import ShotStrip from './ShotStrip.vue'
import '../partCard.css'

// an inhabitant of the field (T270 §7): icon, name, type in the card's head (partCard.css: tinted, sticks while the card
// passes); the description, stats and states, screenshots, the mechanics claimed on it and the rules that name it.
// The owner changes each of them where it reads (T306): the icon, the name, the type, the description, a stat's value, the
// states; the pencil turns the head and the top of the card into its form — all at once, and what is not there yet (a new
// stat). The mechanics stay under the form, each with its trash, and the rules too (T284 §4). Folded (T296 §7) — the head,
// two lines and what is inside
const props = defineProps({ part: Object })
const ed = useEd()
const edit = ref(false)
const error = ref('')
const role = computed(() => roleOf(props.part.role))
const claims = computed(() => ed.claimsOf(props.part.id))
const auto = computed(() => claims.value.filter((c) => c.auto))
const mechanics = computed(() => claims.value.filter((c) => !c.auto))
const roleClaim = computed(() => (role.value.slug ? auto.value.find((c) => c.task === role.value.slug) : null))
const shut = computed(() => !edit.value && isShut(props.part.id, 'entities'))
// «show me where» a claim of this card is: a folded card opens to show it
watch(target, (id) => id && shut.value && claims.value.some((c) => `c-${c.id}` === id) && toggleCard(props.part.id, 'entities'))
const bits = computed(() => [['stats', props.part.stats?.length, 'параметри'], ['half', props.part.states?.length, 'стани'],
  ['image', props.part.screenshots?.length, 'скриншоти'], ['cog', mechanics.value.length, 'механіки'],
  ['⚡', ed.rules.filter((r) => mentions(r, props.part.id)).length, 'правила']])
const save = (patch) => ed.save.part(props.part.id, patch)
// none fits — the idea goes to the teacher, and meanwhile the entity is an «object», as in the form (RoleField)
const PROPOSE = { what: 'новий тип сутності', allTo: '/tasks?zone=entities&sub=roles', zone: 'entities', subzone: 'roles', then: 'object' }

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
  <div :id="`p-${part.id}`" class="card pcard" :style="{ '--z': zones.entities?.color }">
    <div v-if="!edit" v-to-start="'картки'" class="pcard-head">
      <EmojiPick :can="ed.editable" :icon="part.icon" :fallback="role.icon" :save="(icon) => save({ icon })" />
      <InlineText :value="part.title" :can="ed.editable" required placeholder="Назва" class="fw-semibold" :save="(title) => save({ title })" />
      <InlinePick :can="ed.editable" :items="roleItems" :current="part.role" placeholder="пошук типу…" tip="Клік — інший тип" :propose="PROPOSE"
                  :save="(r) => save({ role: r })">
        <template #default="{ open }">
          <span v-peek="open || !role.slug ? null : { kind: 'task', id: role.slug }" class="type" :title="role.slug ? null : role.desc">{{ (role.label || '').toLowerCase() }}<JudgeMark :claim="roleClaim" /></span>
        </template>
      </InlinePick>
      <span class="pcard-acts">
        <CardFold :id="part.id" scope="entities" />
        <template v-if="ed.editable">
          <button type="button" class="iact" title="Редагувати все разом" @click="edit = true"><Icon name="pencil" /></button>
          <DelButton :what="`сутність «${part.title}»`" note="разом з її правилами й заявками" @yes="remove" />
        </template>
      </span>
    </div>
    <div v-if="shut" class="card-body"><CardShut :text="part.description" :bits @open="toggleCard(part.id, 'entities', $event)" /></div>
    <div v-else class="card-body vstack gap-2">
      <div v-if="edit" class="editing pform"><EntityForm :part @done="edit = false" @cancel="edit = false" /></div>
      <template v-else>
        <InlineText v-if="part.description || ed.editable" :value="part.description" multi block :can="ed.editable" class="desc"
                    placeholder="Що це і як поводиться — коротко" :save="(description) => save({ description })">
          <template #empty><span class="more" title="опису ще нема — додай пару слів"><Icon name="plus" /> опис</span></template>
        </InlineText>
        <EntityStats v-if="!ed.simple" :part :auto :can="ed.editable" />
        <ShotStrip :part need />
      </template>
      <template v-if="!ed.simple">
        <PartBlock v-if="mechanics.length || ed.editable" pic="cog" zone="entities" title="Механіки">
          <template #after><CardPicker plus :kinds="['mechanic']" :anchor="{ part: part.id }" label="механіка" /></template>
          <div v-if="mechanics.length" class="vstack gap-1">
            <ClaimRow v-for="c in mechanics" :key="c.id" :claim="c" />
          </div>
        </PartBlock>
        <EntityRules :part />
      </template>
      <div v-if="error" class="text-danger small">{{ error }}</div>
    </div>
  </div>
</template>

<style scoped>
.type { font-size: .8rem; color: var(--bs-secondary-color); }
.desc { font-size: .85rem; }
</style>
