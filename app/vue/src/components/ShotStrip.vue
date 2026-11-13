<script setup>
import { deleteShot, uploadShot } from '../api.js'
import { useEd } from '../ed.js'
import ShotTiles from './ShotTiles.vue'

// the screenshots of a part (T270 §10.3): thumbnails that open over the page; the owner adds through the violet tile,
// always there (not in the sample's sandbox: nothing is uploaded there), and takes one off by the round control in its corner
defineProps({ part: Object })
const ed = useEd()
</script>

<template>
  <ShotTiles :game="part.game" :names="part.screenshots || []" :adds="ed.editable && !ed.sandbox" :drops="ed.editable"
             word="скриншот" what="скриншот" :add="(file) => uploadShot(part.id, file)" :drop="(name) => deleteShot(part.id, name)" />
</template>
