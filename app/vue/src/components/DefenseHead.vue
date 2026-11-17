<script setup>
import Avatar from '@core/components/Avatar.vue'
import Icon from '@core/components/Icon.vue'
import { vocab } from '../defense.js'
import '../defense.css'

// who defends what (T327 §3): the student, the labs and the kind as chips to switch — and the ways to the game and the
// repo, each in a tab of its own: the defense's page stays where it is
const props = defineProps({ d: Object })
const emit = defineEmits(['set'])
const lab = (n) => emit('set', { labs: props.d.labs.includes(n) ? props.d.labs.filter((x) => x !== n) : [...props.d.labs, n].sort() })
</script>

<template>
  <div>
    <div class="d-flex flex-wrap align-items-center gap-2 mb-2">
      <Avatar :user="d.student" :size="44" />
      <div class="me-auto">
        <h1 class="h4 mb-0">{{ d.student.name }}</h1>
        <div class="small text-secondary">{{ d.student.group }}<template v-if="d.game"> · гра «{{ d.game }}»</template></div>
      </div>
      <a :href="`/students/${d.student.nick}`" target="_blank" class="btn btn-sm btn-outline-secondary" title="Сторінка гри — у сусідній вкладці"><Icon name="gamepad" /> Гра</a>
      <a v-if="d.student.github" :href="d.student.github" target="_blank" rel="noopener" class="btn btn-sm btn-outline-secondary"><Icon name="branch" /> Репозиторій</a>
    </div>
    <div class="drow">
      <span class="dlbl">Лаби</span>
      <span class="d-flex flex-wrap gap-1">
        <button v-for="n in vocab.labs" :key="n" type="button" class="dchip" :class="{ on: d.labs.includes(n) }" @click="lab(n)">{{ n }}</button>
      </span>
    </div>
    <div class="drow">
      <span class="dlbl">Вид захисту</span>
      <span class="d-flex flex-wrap gap-1">
        <button v-for="k in vocab.kinds" :key="k.key" type="button" class="dchip" :class="{ on: d.kind === k.key }" @click="emit('set', { kind: k.key })">{{ k.text }}</button>
      </span>
    </div>
  </div>
</template>
