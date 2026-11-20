import { words } from './lectureText.js'

// the course's names (search/thesaurus.json): a query, or a run of its words, that is one of a group's names — as written
// or by lemmas («методу головних компонент») — is looked for by the group's other names
export function thesOf(data, lex, stop) {
  const sig = (ws) => ws.map((w) => (lex.knows(w) ? `#${lex.lemmas(w)[0]}` : w)).join(' ')
  const groups = (Array.isArray(data?.groups) ? data.groups : [])
    .map((g) => [g.main, ...(g.also || [])].filter((n) => typeof n === 'string' && words(n).length))
  const by = new Map(), known = new Set()  // a name as written and by lemmas → [group, name]; every word of every name
  groups.forEach((names, g) => names.forEach((name) => {
    const ws = words(name)
    ws.forEach((w) => known.add(w))
    for (const k of [ws.join(' '), sig(ws)]) if (!by.has(k)) by.set(k, [g, name])
  }))
  return {
    knows: (w) => known.has(w),
    // the longest run of the query's words that names a group → { from, to, name, alts: the group's other names }
    match(qs) {
      for (let len = qs.length; len > 0; len--) {
        for (let i = 0; i + len <= qs.length; i++) {
          const run = qs.slice(i, i + len), own = [run.join(' '), sig(run)]
          const hit = !run.every(stop) && (by.get(own[0]) || by.get(own[1]))
          if (!hit) continue
          const alts = groups[hit[0]].filter((n) => !own.includes(words(n).join(' ')) && !own.includes(sig(words(n))))
          return { from: i, to: i + len, name: hit[1], alts }
        }
      }
      return null
    },
  }
}
