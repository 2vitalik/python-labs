<script setup>
import { onMounted, ref } from 'vue'

import { getStudentLabs } from '../api.js'
import { STATES, fmtWhen, labName, labPath } from '../labs.js'
import LabEdit from './LabEdit.vue'

// the «Лаби» card of a student (T235): a row per lab with its state and deadline; ✏️ opens the same editor as the matrix
const props = defineProps({ nick: { type: String, required: true } })
const data = ref(null)
const open = ref(null)
const facts = (c) => (c.facts.before || c.facts.after ? `${c.facts.before} до · ${c.facts.after} після` : 'комітів нема')
onMounted(async () => (data.value = await getStudentLabs(props.nick)))
</script>

<template>
  <div v-if="data" class="card">
    <div class="card-body">
      <h2 class="h5 d-flex align-items-center gap-2">Лаби <RouterLink to="/deadlines" class="small fw-normal ms-auto">усі дедлайни →</RouterLink></h2>
      <p class="small text-secondary mb-2">
        🐙 <template v-if="data.repo"><a :href="data.repo.url" target="_blank">{{ data.repo.url.replace('https://github.com/', '') }}</a>
          · <template v-if="data.repo.ok">{{ data.repo.commits }} комітів · {{ data.repo.branch }}<template v-if="data.repo.last"> · останній {{ fmtWhen(data.repo.last) }}</template></template>
          <span v-else class="text-danger">{{ data.repo.error }}</span> · pull {{ fmtWhen(data.repo.pulled_at) }}</template>
        <template v-else-if="data.github"><a :href="data.github" target="_blank">{{ data.github.replace('https://github.com/', '') }}</a> · ще не клоновано</template>
        <template v-else>репозиторію нема</template>
      </p>
      <table class="table table-sm align-middle mb-0">
        <tbody>
          <template v-for="c in data.labs" :key="c.n">
            <tr>
              <th class="fw-normal"><RouterLink v-if="labPath(c.n)" :to="labPath(c.n)">{{ labName(c.n) }}</RouterLink><template v-else>{{ labName(c.n) }}</template></th>
              <td>{{ STATES[c.state].emoji }} {{ STATES[c.state].text }}<span v-if="c.mark?.met === true || c.mark?.met === false" class="text-secondary" title="слово викладача"> ✍</span></td>
              <td class="text-secondary small">
                <template v-if="c.due">до {{ fmtWhen(c.due) }}<span v-if="c.mark?.until" title="подовжено"> ⏳</span><span v-if="c.mark?.reason"> · {{ c.mark.reason }}</span></template>
              </td>
              <td class="text-secondary small">{{ facts(c) }}</td>
              <td class="text-end"><a href="#" class="ibtn" title="Подовження, вердикт, звіт" @click.prevent="open = open === c.n ? null : c.n">{{ open === c.n ? '▴' : '✏️' }}</a></td>
            </tr>
            <tr v-if="open === c.n">
              <td colspan="5" class="p-0 pb-2"><LabEdit :nick :lab="c.n" :cell="c" @saved="data.labs[c.n - 1] = { n: c.n, ...$event }" @close="open = null" /></td>
            </tr>
          </template>
        </tbody>
      </table>
    </div>
  </div>
</template>
