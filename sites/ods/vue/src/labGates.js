import { ref } from 'vue'

import { request } from '@core/http.js'

// how open each lab is to students (sites/ods/api/lab_gates.py): {n: 'telegram' | 'site'} — a hidden lab is not in a
// student's answer; the teacher gets every lab, 'hidden' too, and says how open each one is
export const gates = ref(null)
let loading
export const loadGates = () => (loading ??= request('/api/labgates').then((g) => (gates.value = g)))
export const setGate = async (n, state) => (gates.value = await request(`/api/labgates/${n}`, 'PUT', { state }))

// state · the word on the switch · what it means for students
export const GATES = [
  ['hidden', 'сховано', 'Студенти не бачать лаби: ні тексту, ні картки'],
  ['telegram', 'Telegram', 'Студенти читають лабу й беруть картку; файл надсилають викладачеві в Telegram'],
  ['site', 'сайт', 'Студенти здають файл ноутбука на сайті'],
]
