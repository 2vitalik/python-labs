// line diff for the guide history: [{t: ' ' | '+' | '-', s}] from an LCS table (pages are a few hundred lines)
export function diffLines(a, b) {
  const A = a.split('\n')
  const B = b.split('\n')
  const n = A.length
  const m = B.length
  const L = Array.from({ length: n + 1 }, () => new Uint16Array(m + 1))
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) L[i][j] = A[i] === B[j] ? L[i + 1][j + 1] + 1 : Math.max(L[i + 1][j], L[i][j + 1])
  }
  const out = []
  let i = 0
  let j = 0
  while (i < n && j < m) {
    if (A[i] === B[j]) {
      out.push({ t: ' ', s: A[i] })
      i++
      j++
    } else if (L[i + 1][j] >= L[i][j + 1]) out.push({ t: '-', s: A[i++] })
    else out.push({ t: '+', s: B[j++] })
  }
  while (i < n) out.push({ t: '-', s: A[i++] })
  while (j < m) out.push({ t: '+', s: B[j++] })
  return out
}

// unchanged runs beyond `ctx` lines around a change fold into {t: '…', n}
export function fold(diff, ctx = 2) {
  const out = []
  let same = []
  const flush = (end) => {
    const head = out.length ? ctx : 0
    const tail = end ? 0 : ctx
    if (same.length > head + tail) {
      out.push(...same.slice(0, head), { t: '…', n: same.length - head - tail }, ...same.slice(same.length - tail))
    } else out.push(...same)
    same = []
  }
  for (const d of diff) {
    if (d.t === ' ') same.push(d)
    else {
      flush(false)
      out.push(d)
    }
  }
  flush(true)
  return out
}
