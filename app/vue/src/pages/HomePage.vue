<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { getGuidePage } from '../api.js'
import GuideBrief from '../components/GuideBrief.vue'
import GuideText from '../components/GuideText.vue'
import { loadGuide, SECTIONS } from '../guide.js'
import { canAccess, user } from '../user.js'

const statusText = { pending: 'доступ надає викладач', student: 'студент', admin: 'викладач' }
const router = useRouter()
const home = ref(null)
// home.md body: text before the marker, the section briefs, the rest
const parts = computed(() => (home.value?.body || '').split('<!-- sections -->'))
const can = (path) => canAccess(router.resolve(path).meta.access)

loadGuide()
getGuidePage('home').then((p) => (home.value = p))
</script>

<template>
  <div class="col-lg-8 mx-auto">
    <div class="d-flex flex-wrap justify-content-between align-items-baseline gap-2 mb-3">
      <h1 class="mb-0">{{ home?.title || 'Python Labs' }}</h1>
      <div v-if="user" class="d-flex flex-wrap align-items-center gap-2 small">
        <span>Привіт, {{ user.name || user.email }} · {{ statusText[user.status] }}</span>
        <RouterLink v-if="can('/profile')" to="/profile" class="btn btn-outline-primary btn-sm">Профіль</RouterLink>
        <RouterLink v-if="can('/my/game')" to="/my/game" class="btn btn-outline-primary btn-sm">Моя гра</RouterLink>
      </div>
    </div>
    <template v-if="home">
      <GuideText :text="home.brief" class="lead" />
      <GuideText v-if="parts[0]" :text="parts[0]" class="mt-4" />
      <div class="my-4">
        <GuideBrief v-for="s in SECTIONS" :key="s.slug" :slug="s.slug" :to="s.path" />
        <GuideBrief slug="changes" />
      </div>
      <GuideText v-if="parts[1]" :text="parts[1]" />
      <p class="small mt-4 mb-0"><RouterLink to="/guide" class="text-secondary">Уся методичка однією сторінкою →</RouterLink></p>
    </template>
  </div>
</template>
