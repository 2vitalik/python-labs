<script setup>
import { computed } from 'vue'

import GuideText from '@core/components/GuideText.vue'

import { author } from '../lecLook.js'
import { markMd } from '../lectureChangeMarks.js'
import { locate, markRaw } from '../lectureChangeSpots.js'

// one block of a lecture in an open change: rendered as the lecture shows it (its look, its pictures) with the edits lit,
// or its raw markdown with the same marks; `empty` — what stands for a block that is not there
const props = defineProps({ text: String, ranges: { type: Array, default: () => [] }, raw: Boolean, slug: String, empty: String })
const IMG = /(\]\(|src=")img\//g  // a lecture's pictures are the site's media (content_disk.py)
const spots = computed(() => locate(props.text || '', props.ranges))
const md = computed(() => markMd(props.text, spots.value).replace(IMG, `$1/api/media/${props.slug}/`).replace(/<!--[^>]*-->/g, ''))
const html = computed(() => markRaw(props.text, spots.value))
</script>

<template>
  <p v-if="!text" class="chg-none">{{ empty }}</p>
  <pre v-else-if="raw" class="chg-raw" v-html="html"></pre>
  <div v-else class="lecture chg-view" :class="{ 'lec-author': author }"><GuideText :text="md" /></div>
</template>
