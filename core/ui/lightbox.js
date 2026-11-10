import { ref } from 'vue'

// pictures opened over the page (components/Lightbox.vue shows them): the list being looked at and the place in it
export const box = ref(null)  // { list: [url…], i }
export const showShot = (list, i = 0) => (box.value = { list, i })
