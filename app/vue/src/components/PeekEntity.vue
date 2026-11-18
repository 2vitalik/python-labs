<script setup>
import { computed, ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import { showShot } from '@core/lightbox.js'
import { close, vPeek } from '@core/peek.js'
import { iconOf, roleOf } from '../catalog.js'
import { useEd } from '../ed.js'
import { jump } from '@core/jump.js'
import { mentions } from '../rules.js'
import CardSign from './CardSign.vue'
import EntityStats from './EntityStats.vue'
import PartLabel from './PartLabel.vue'
import RuleText from './RuleText.vue'

// an entity's card under the mouse (T284 §2): what it is, its numbers and states; its mechanics and the rules that name
// it unfold right here, and each is a way on
const props = defineProps({ id: String })
const ed = useEd()
const part = computed(() => ed.entities.find((p) => p.id === props.id))
const role = computed(() => roleOf(part.value?.role))
const claims = computed(() => ed.claimsOf(props.id))
const mechanics = computed(() => claims.value.filter((c) => !c.auto))
const rules = computed(() => ed.rules.filter((r) => mentions(r, props.id)))
const shots = computed(() => (part.value?.screenshots || []).map((s) => `/api/uploads/${part.value.game}/${s}`))
const open = ref('')  // '' | mechanics | rules
const show = () => { close(); jump(`p-${props.id}`) }
</script>

<template>
  <div v-if="part" class="vstack gap-2">
    <div class="pk-head">
      <span class="ico">{{ iconOf(part) }}</span>
      <span class="fw-semibold">{{ part.title }}</span>
      <span v-if="role.slug" v-peek="{ kind: 'task', id: role.slug }" class="pk-type">{{ (role.label || '').toLowerCase() }}</span>
      <span v-else class="pk-type">{{ (role.label || '').toLowerCase() }}</span>
    </div>
    <div v-if="part.description">{{ part.description }}</div>
    <div v-else class="text-secondary">Опису ще нема.</div>
    <img v-if="shots.length" :src="shots[0]" alt="скриншот" class="rounded border pk-shot" title="на весь екран" @click.stop="showShot(shots, 0)">
    <EntityStats :part :auto="claims.filter((c) => c.auto)" />
    <div v-if="mechanics.length">
      <button type="button" class="pk-fold" @click.stop="open = open === 'mechanics' ? '' : 'mechanics'">
        <PartLabel pic="cog" zone="entities">Механіки</PartLabel> {{ mechanics.length }} <Icon :name="open === 'mechanics' ? 'down' : 'right'" />
      </button>
      <template v-if="open === 'mechanics'">
        <div v-for="c in mechanics" :key="c.id" class="pk-row"><span><CardSign :task="ed.info(c.task)" /> <span v-peek="{ kind: 'task', id: c.task }">{{ ed.info(c.task)?.title || c.task }}</span></span></div>
      </template>
    </div>
    <div v-if="rules.length">
      <button type="button" class="pk-fold" @click.stop="open = open === 'rules' ? '' : 'rules'">
        <PartLabel pic="bolt" zone="game-logic">Правила</PartLabel> {{ rules.length }} <Icon :name="open === 'rules' ? 'down' : 'right'" />
      </button>
      <div v-if="open === 'rules'" class="vstack gap-1 mt-1">
        <div v-for="r in rules" :key="r.id" v-peek="{ kind: 'rule', id: r.id }" class="pk-rule"><RuleText :rule="r" :parts="ed.parts" /></div>
      </div>
    </div>
    <button type="button" class="pk-go" @click.stop="show">до сутності на сторінці <Icon name="arrow" /></button>
  </div>
</template>

<style scoped>
.ico { font-size: 1.3rem; line-height: 1; }
.pk-rule { padding: .15rem .3rem; border: 1px solid var(--bs-border-color-translucent); border-radius: .3rem; cursor: pointer; }
.pk-rule:hover { background: var(--bs-tertiary-bg); }
.pk-rule :deep(.rule-text) { font-size: .78rem; pointer-events: none; }
</style>
