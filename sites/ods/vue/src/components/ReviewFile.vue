<script setup>
import { ref } from 'vue'

import Icon from '@core/components/Icon.vue'
import Reveal from '@core/components/Reveal.vue'

import { labFileRawUrl, putLabResult } from '../api.js'

// the file as it came, the Colab link, and the card itself: «звільнити» unpins it — the teacher pins cards on «Результати»
const props = defineProps({ n: Number, doc: Object, shown: String })
const emit = defineEmits(['freed'])
const sure = ref(false)
const error = ref('')

async function free() {
  error.value = ''
  try {
    await putLabResult(props.n, props.doc.vid, { student: '' })
    sure.value = false
    emit('freed')
  } catch (e) {
    error.value = e.message
  }
}
</script>

<template>
  <div class="small d-flex flex-column gap-1">
    <a v-if="shown" :href="labFileRawUrl(shown)" download><Icon name="download" /> завантажити файл, що ліворуч</a>
    <a v-if="doc.notebook" :href="doc.notebook" target="_blank" rel="noopener"><Icon name="open" /> ноутбук у Colab</a>
    <template v-if="doc.student">
      <a href="#" class="rv-dot text-secondary" @click.prevent="sure = !sure">звільнити картку</a>
      <Reveal :show="sure">
        <div class="d-flex flex-wrap align-items-center gap-2">
          <span>Картка {{ doc.vid }} стане вільною, а студент лишиться без варіанта цієї лаби, доки не закріпиш йому картку на «Результатах».</span>
          <button type="button" class="btn btn-sm btn-outline-secondary" @click="sure = false">Скасувати</button>
          <button type="button" class="btn btn-sm btn-danger" @click="free">Звільнити</button>
        </div>
      </Reveal>
      <span v-if="error" class="text-danger">{{ error }}</span>
    </template>
    <span v-else class="text-secondary">Картка вільна.</span>
  </div>
</template>

<style scoped>
.rv-dot { align-self: flex-start; text-decoration: underline dotted; text-underline-offset: .2em; }
</style>
