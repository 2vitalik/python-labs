// a game's history (T278 §12): who made a change — the role's badge; what was done — a word in its colour; the «хто» filter

export const ROLES = {
  student: { icon: '🎓', name: 'студент' },
  teacher: { icon: '👩‍🏫', name: 'викладач' },
  agent: { icon: '🤖', name: 'агент' },
  system: { icon: '⚙️', name: 'автоматично: скрипт каталогу' },
}

export const ACTIONS = {
  added: { word: 'додано', cls: 'text-success' },
  changed: { word: 'змінено', cls: 'text-body-secondary' },
  deleted: { word: 'видалено', cls: 'text-danger' },
  accepted: { word: '✓ зараховано', cls: 'text-success' },
  returned: { word: '↩ повернуто', cls: 'text-danger' },
  claimed: { word: 'знову заявлено', cls: 'text-body-secondary' },
}

// the student's own hand, or everyone else's: the teacher, an agent, a script
export const WHO = [
  { key: '', label: 'усі', keep: () => true },
  { key: 'student', label: 'студент', mine: 'я', keep: (r) => r.actor.role === 'student' },
  { key: 'staff', label: 'викладач і агент', keep: (r) => r.actor.role !== 'student' },
]

export const PAGE = 50
