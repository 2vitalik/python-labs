<script setup>
import { shown, toggleDrafts } from '../drafts.js'
import Icon from './Icon.vue'
</script>

<template>
  <a href="#" title="Чернетки — нотатки й неготове в коментарях: показати їх чи сховати" @click.prevent="toggleDrafts">
    <Icon :name="shown ? 'eye' : 'eyeoff'" /> {{ shown ? 'з чернетками' : 'без чернеток' }}
  </a>
</template>
