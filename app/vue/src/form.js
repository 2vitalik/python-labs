import { computed, onUnmounted, reactive, ref, watch } from 'vue'
import { onBeforeRouteLeave } from 'vue-router'

const LEAVE = 'Є незбережені зміни. Піти без збереження?'

// editable form + snapshot of what the server holds: dirty = they differ, fill() resets both
export function useForm(fields) {
  const form = reactive({ ...fields })
  const base = reactive({ ...fields })
  const dirty = computed(() => Object.keys(fields).some((k) => form[k] !== base[k]))
  const saved = ref(false)
  const error = ref('')

  function fill(data) {
    for (const k in fields) if (k in data) form[k] = base[k] = data[k]
  }

  async function save(submit) {  // submit(form) → server response, which becomes the new snapshot
    error.value = ''
    try {
      const data = await submit(form)
      fill(data)
      saved.value = true
      setTimeout(() => (saved.value = false), 2000)
      return data
    } catch (e) {
      error.value = e.message
    }
  }

  watch(form, () => (error.value = ''))  // a stale error next to the button reads as "still wrong"

  // unsaved edits: confirm on in-app navigation, browser's own dialog on close/reload
  onBeforeRouteLeave(() => !dirty.value || confirm(LEAVE))
  const unload = (e) => dirty.value && e.preventDefault()
  window.addEventListener('beforeunload', unload)
  onUnmounted(() => window.removeEventListener('beforeunload', unload))

  return { form, dirty, saved, error, fill, save }
}
