<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { getGuidePage } from '../api.js'
import GuideText from '../components/GuideText.vue'
import { canAccess, user } from '../user.js'

const statusText = { pending: 'доступ надає викладач', student: 'студент', admin: 'викладач' }
const router = useRouter()
const home = ref(null)
const text = computed(() => (home.value ? `${home.value.brief}\n\n${home.value.body}` : ''))
const can = (path) => canAccess(router.resolve(path).meta.access)

getGuidePage('home').then((p) => (home.value = p))
</script>

<template>
  <div>
    <div class="d-flex flex-wrap justify-content-between align-items-baseline gap-2 mb-3">
      <h1 class="mb-0">{{ home?.title || 'Python Labs' }}</h1>
      <div v-if="user" class="d-flex flex-wrap align-items-center gap-2 small">
        <span>Привіт, {{ user.name || user.email }} · {{ statusText[user.status] }}</span>
        <RouterLink v-if="can('/profile')" to="/profile" class="btn btn-outline-primary btn-sm">Профіль</RouterLink>
        <RouterLink v-if="can('/my/game')" to="/my/game" class="btn btn-outline-primary btn-sm">Моя гра</RouterLink>
      </div>
    </div>
    <template v-if="home">
      <GuideText :text="text" />
      <p class="small mt-4 mb-0 d-flex flex-wrap gap-3">
        <RouterLink to="/changes" class="text-secondary">🆕 Що змінилось</RouterLink>
        <RouterLink to="/guide" class="text-secondary">Уся методичка однією сторінкою →</RouterLink>
      </p>
    </template>
  </div>
</template>
