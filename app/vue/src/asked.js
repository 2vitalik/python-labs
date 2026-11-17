import { kidsOf, kindOf } from './catalog.js'

// «за запитом» (T319): an active card outside the core — a student adds it with one sentence, its coin waits for the teacher
export const WHY_MIN = 20
const SELF = ['window', 'role', 'stat', 'fieldopt']  // the window or the entity itself explains these claims

export const isCore = (t) => !!t?.core || (kidsOf.value[t?.slug] || []).some(isCore)
export const asked = (t) => t?.status === 'active' && !isCore(t)
// `free` — the teacher or a sample's sandbox: the server asks them no sentence
export const needsWhy = (t, free = false) => !free && asked(t) && !SELF.includes(kindOf(t))
export const whyOk = (text) => (text || '').trim().length >= WHY_MIN
