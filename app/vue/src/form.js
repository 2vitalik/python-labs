import { computed, reactive, ref } from 'vue'

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

  return { form, dirty, saved, error, fill, save }
}
