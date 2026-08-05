<script setup>
defineProps({ zones: Object, counts: Object, zone: String, sub: String })
defineEmits(['select'])
</script>

<template>
  <div class="list-group">
    <button type="button" class="list-group-item list-group-item-action" :class="{ active: !zone }"
            @click="$emit('select', '', '')">
      Всі зони <span class="float-end opacity-75">{{ counts[''] || 0 }}</span>
    </button>
    <template v-for="(z, zk) in zones" :key="zk">
      <button type="button" class="list-group-item list-group-item-action fw-semibold"
              :class="{ active: zone === zk && !sub }" @click="$emit('select', zone === zk ? '' : zk, '')">
        {{ z.title }} <span class="float-end opacity-75">{{ counts[zk] || 0 }}</span>
      </button>
      <template v-if="zone === zk">
        <button v-for="(st, sk) in z.subzones" :key="sk" type="button"
                class="list-group-item list-group-item-action ps-4 py-1 small"
                :class="{ active: sub === sk }" @click="$emit('select', zk, sub === sk ? '' : sk)">
          {{ st }} <span class="float-end opacity-75">{{ counts[`${zk}/${sk}`] || 0 }}</span>
        </button>
      </template>
    </template>
  </div>
</template>
