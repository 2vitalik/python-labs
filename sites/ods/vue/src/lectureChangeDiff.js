// edits for a pair of blocks the catalogue gave none for (the look's automatic items — only the markup differs): a diff by
// words, tags and `*` runs, the changed neighbours joined; offsets are in UTF-16 units (`js`), not the catalogue's
const TOKEN = /<\/?[a-z][^>\n]*>|\*+|\s+|[\p{L}\p{N}_]+|./gsu
const MAX = 400000  // tokens × tokens: a longer pair is one edit whole

export function diffEdits(a, b) {
  const A = [...a.matchAll(TOKEN)], B = [...b.matchAll(TOKEN)]
  const n = A.length, m = B.length
  const whole = [{ del: a, ins: b, a: [0, a.length], b: [0, b.length], js: true }]
  if (n * m > MAX) return whole
  const L = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1))
  for (let i = n - 1; i >= 0; i--) for (let j = m - 1; j >= 0; j--) L[i][j] = A[i][0] === B[j][0] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1])
  const end = (k, T, s) => (k < T.length ? T[k].index : s.length)
  const out = []
  let i = 0, j = 0, cur = null
  while (i < n || j < m) {
    if (i < n && j < m && A[i][0] === B[j][0]) { cur = null; i++; j++; continue }
    if (!cur) out.push(cur = { a: [end(i, A, a), end(i, A, a)], b: [end(j, B, b), end(j, B, b)] })
    if (j >= m || (i < n && L[i + 1][j] >= L[i][j + 1])) cur.a[1] = end(++i, A, a)
    else cur.b[1] = end(++j, B, b)
  }
  return out.map((e) => ({ ...e, del: a.slice(...e.a), ins: b.slice(...e.b), js: true }))
}
