import { putFieldValue, putStudentLab } from './api.js'

// a cell of /table edited: the row takes what the API answers, nothing else reloads
export async function editCell(c, row, value) {
  if (c.edit === 'field') {
    const r = await putFieldValue(row.nick, c.field.key, { value, lab: c.lab || 0 })
    if (r.value === null) delete row.fields[r.column]
    else row.fields[r.column] = r.value
  } else if (c.edit === 'mark') {
    // one field of the lab's mark, '' when its text is cleared — or several at once: the column says them itself, `patch(value)`
    const body = c.patch ? c.patch(value) : { [c.field]: value ?? (c.type === 'bool' ? false : '') }
    row.labs[c.lab] = await putStudentLab(row.nick, c.lab, body)
  }
}
