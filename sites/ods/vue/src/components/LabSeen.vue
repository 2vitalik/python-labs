<script setup>
import { computed, onMounted } from 'vue'

import { fmtWhen } from '@core/labs.js'

import { commons, loadLabPages } from '../labPages.js'
import { fmtSize, numbered, sameOf } from '../labText.js'
import LabClip from './LabClip.vue'
import LabLadder from './LabLadder.vue'
import LabVerdict from './LabVerdict.vue'
import LabVersions from './LabVersions.vue'

// «Що бачить сайт»: the latest file, the answers of its line, the levels the work reaches, the versions — MY as is
const props = defineProps({ n: Number, lab: Object })
const file = computed(() => props.lab.file?.id && props.lab.file)
const files = computed(() => numbered(props.lab.files))
const k = computed(() => files.value.find((f) => f.id === file.value?.id)?.k)
const nb = (f) => `/labs/${props.n}/my/nb/${f.id}`
const run = computed(() => file.value?.run)
const steps = computed(() => props.lab.grade?.steps || [])
const marimo = computed(() => file.value?.kind === 'marimo' && !props.lab.attempts)  // marimo keeps no outputs: no line in it
const byTelegram = computed(() => props.lab.handin === 'telegram')  // no hand-in block above: the file and the line go to the teacher
// what the work reaches by itself, or what 12 still lacks; without a file the levels above the answers are unknown
const level = computed(() => {
  const work = props.lab.grade?.work
  if (work) return `Сама робота зараз тягне на рівень ${work}.`
  if (!file.value) return `Решту пунктів сайт побачить у файлі ноутбука — ${byTelegram.value ? 'коли викладач перенесе його сюди' : 'здай його вище'}.`
  const lack = steps.value.find((s) => s.level === 12)?.needs.filter((x) => x.ok === false).map((x) => x.text)
  return lack?.length ? `До рівня 12 бракує: ${lack.join(' · ')}.` : ''
})
const grading = computed(() => commons().some((p) => p.part === 'grading'))
onMounted(() => loadLabPages().catch(() => {}))
</script>

<template>
  <section class="mb-4">
    <h2 class="h5">Що бачить сайт</h2>
    <div v-if="file" class="mb-2">
      <LabClip class="text-secondary" /> <b>{{ file.name }}</b>
      <span class="text-secondary"> · {{ fmtWhen(file.at) }} · {{ fmtSize(file.size) }}<template v-if="k"> · версія {{ k }} із {{ files.length }}</template></span>
      <div><RouterLink :to="nb(file)">Подивитись ноутбук, як його бачить викладач</RouterLink></div>
      <div v-if="run" class="small mt-1">Перезапущено у викладача<template v-if="run.same !== null">:
        <span :class="sameOf(run).cls">{{ sameOf(run).short }}</span></template><template v-if="run.total"> · {{ run.right }} із {{ run.total }} ✅</template><template v-if="run.errors?.length"> · помилок {{ run.errors.length }}</template></div>
    </div>
    <p v-if="lab.attempts" class="mb-1"><b>{{ lab.ok }} із {{ lab.total }} ✅</b> · спроба {{ lab.attempts }}<template v-if="lab.checked_at"> · перевірено {{ fmtWhen(lab.checked_at) }}</template></p>
    <p v-else-if="marimo" class="text-secondary mb-1">marimo не зберігає виводів, тож рядка відповідей у файлі нема —
      {{ byTelegram ? 'надішли його викладачеві тим самим повідомленням, що й файл' : 'встав його через «інший спосіб» вище' }}.</p>
    <p v-else class="text-secondary mb-1">Рядка відповідей у файлі не знайшлося.</p>
    <LabVerdict :verdict="lab.verdict" class="mb-3" />
    <template v-if="steps.length">
      <h3 class="h6 mt-3">Рівні <RouterLink v-if="grading" to="/labs/about/grading" class="small fw-normal ms-1">правила оцінювання</RouterLink></h3>
      <LabLadder :steps />
      <p v-if="level" class="mt-2 mb-0">{{ level }}</p>
    </template>
    <template v-if="files.length">
      <h3 class="h6 mt-3">Версії</h3>
      <LabVersions :files="lab.files" :current="file?.id" :to="nb" />
    </template>
  </section>
</template>
