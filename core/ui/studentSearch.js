// the search box of /students: every word typed must start a word of the row — the name («Прізвище Імʼя»), the nick, the Telegram handle.
// Word starts, not substrings: «ан» finds Анна and Андрієнко, not half the list through Іванов and Степан; case and apostrophes do not count
const fold = (s) => String(s || '').toLowerCase().replace(/['ʼ’]/g, '')
const words = (s) => fold(s).split(/[\s._-]+/).filter(Boolean)  // a nick splits at its dots and dashes

export function matches(student, q) {
  const need = words(q)
  if (!need.length) return true
  const have = [student.name, student.nick, student.tg_username].flatMap(words)
  return need.every((w) => have.some((x) => x.startsWith(w)))
}
