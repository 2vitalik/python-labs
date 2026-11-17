import { ref } from 'vue'

import { getDefenseVocab } from './api.js'

// the words of defenses and remarks come from the API (defense_vocab.py): one list for the pages, the bot and a model
export const vocab = ref(null)
let asked
export const loadVocab = () => (asked ||= getDefenseVocab().then((v) => (vocab.value = v)))
export const setVocab = (v) => (vocab.value = { ...vocab.value, ...v })  // a student gets theirs along with the remarks
export const word = (list, key) => vocab.value?.[list]?.find((x) => x.key === key)

// a tag's colour is its family (T328 §2): how the code reads · how it is built · what it means · how it behaves · around it
export const TONES = { naming: 'blue', style: 'blue', dup: 'violet', size: 'violet', structure: 'violet', oop: 'violet', data: 'teal', logic: 'teal',
                       bug: 'red', errors: 'red', game: 'green', repo: 'gray', learn: 'orange', other: 'gray' }
export const STATES = { draft: 'чернетка', open: 'чекає відповіді', answered: 'є відповідь', accepted: 'прийнято', returned: 'повернуто' }

export const mins = (from, to) => Math.max(0, Math.round(((to ? new Date(to) : new Date()) - new Date(from)) / 60000))
export const span = (m) => (m < 60 ? `${m} хв` : `${Math.floor(m / 60)} год${m % 60 ? ` ${m % 60} хв` : ''}`)
export const clock = (iso) => new Date(iso).toLocaleTimeString('uk-UA', { hour: '2-digit', minute: '2-digit' })
export const dayOf = (iso) => new Date(iso).toLocaleDateString('uk-UA', { day: 'numeric', month: 'long' })
export const labsText = (labs) => (labs?.length ? `${labs.length > 1 ? 'лаби' : 'лаба'} ${labs.join(', ')}` : 'без лаби')
export const isToday = (iso) => !!iso && new Date(iso).toDateString() === new Date().toDateString()
