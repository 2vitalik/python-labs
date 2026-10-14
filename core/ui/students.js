import { site } from './site.js'
import { user } from './user.js'

// /students and the pages under it: the admin's «Студенти» sits at the root of the crumbs; a student gets the site's slice
// of the same page (site.students.asStudent) — its own name, hung where the site says (python-labs: under «Ігри»)
export function studentsHome() {
  const own = user.value?.status !== 'admin' && site.students.asStudent
  return own ? { name: own.title, parents: own.crumbs } : { name: 'Студенти', parents: [] }
}

// crumbs of /students itself (no tail) or of a page under it
export function studentsCrumbs(...tail) {
  const { name, parents } = studentsHome()
  return [...parents, tail.length ? ['/students', name] : name, ...tail]
}
