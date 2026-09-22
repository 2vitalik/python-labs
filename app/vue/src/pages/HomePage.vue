<script setup>
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'

import { getGuidePage } from '../api.js'
import GuideBody from '../components/GuideBody.vue'
import GuideFoot from '../components/GuideFoot.vue'
import { loadGuide, pages } from '../guide.js'
import { canAccess, user } from '../user.js'

const router = useRouter()
const home = ref(null)
const can = (path) => canAccess(router.resolve(path).meta.access)
const firstName = computed(() => user.value.first_name || user.value.name?.split(' ')[0] || user.value.email)

getGuidePage('home').then((p) => (home.value = p))
loadGuide()
</script>

<template>
  <div>
    <div class="d-flex flex-wrap justify-content-between align-items-baseline gap-2 mb-3">
      <h1 class="mb-0">{{ home?.title || 'Python Labs' }}</h1>
      <div v-if="user" class="d-flex flex-wrap align-items-center gap-2 small">
        <span>Привіт, {{ firstName }}!<template v-if="user.status === 'pending'"> · доступ надає викладач</template></span>
        <RouterLink v-if="can('/my/profile')" to="/my/profile" class="btn btn-outline-primary btn-sm">Профіль</RouterLink>
        <RouterLink v-if="can('/my/game')" to="/my/game" class="btn btn-outline-primary btn-sm">Моя гра</RouterLink>
      </div>
    </div>
    <template v-if="home">
      <GuideBody v-model:page="home" />
      <GuideFoot>
        <div><RouterLink to="/changes">{{ pages.changes?.title || 'Що змінилось' }}</RouterLink></div>
      </GuideFoot>
    </template>
  </div>
</template>
