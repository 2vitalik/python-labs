<script setup>
import { ref, watch } from 'vue'

import Icon from '@core/components/Icon.vue'
import { vHint } from '@core/hint.js'
import { showShot } from '@core/lightbox.js'

import { slideLink, slidePic } from '../lectureChanges.js'

// where to look at the change: the lecturer's slide (its picture over the page; none on the site yet — the button greys
// and says why), our slide, the place in the text (the slide's for now: a finer anchor is to come)
const props = defineProps({ it: Object })
const pic = ref('wait')  // wait · yes · no
watch(() => slidePic(props.it), (url) => {
  pic.value = 'wait'
  const img = new Image()
  const got = (v) => () => slidePic(props.it) === url && (pic.value = v)  // an answer for a slide left behind is no answer
  img.onload = got('yes')
  img.onerror = got('no')
  img.src = url
}, { immediate: true })
const PIC = { wait: 'беру знімок…', yes: 'знімок слайда лектора поверх сторінки', no: 'знімка цього слайда лектора на сайті ще нема' }
const look = () => pic.value === 'yes' && showShot([slidePic(props.it)])
</script>

<template>
  <div class="chg-links">
    <button v-hint="PIC[pic]" type="button" class="btn btn-sm btn-outline-secondary" :class="{ off: pic !== 'yes' }"
            :aria-disabled="pic !== 'yes'" @click="look"><Icon name="image" /> слайд лектора</button>
    <RouterLink v-hint="`слайд ${it.slide} лекції ${it.lec} на сайті`" :to="slideLink(it)" class="btn btn-sm btn-outline-secondary">
      <Icon name="win" /> наш слайд</RouterLink>
    <RouterLink v-hint="'місце в тексті лекції — поки що через слайд'" :to="slideLink(it)" class="btn btn-sm btn-outline-secondary">
      <Icon name="book" /> у тексті</RouterLink>
  </div>
</template>
