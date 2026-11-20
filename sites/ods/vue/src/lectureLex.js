import { fold } from './lectureText.js'

// the lexicon (search/lexicon.json, CONTRACT §6.1, .dev/.drafts/T374/lexicon-format.md): per lemma, the lemma first,
// then its forms; a form may stand in several groups. A string `стол|а|у|ом` packs forms of one stem (the stem + each
// ending; an empty ending — the stem itself), should the file ever come packed
const unpack = (s) => {
  const [stem, ...ends] = String(s).split('|')
  return ends.length ? ends.map((e) => stem + e) : [stem]
}

// no file — a lexicon that knows nothing: every word is looked for as written
export function lexiconOf(data) {
  const forms = [], heads = [], of = new Map()  // lemma id → its forms (folded), its lemma as written; a form → lemma ids
  for (const entry of Array.isArray(data?.lemmas) ? data.lemmas : []) {
    const id = forms.push([...new Set(entry.flatMap(unpack).map(fold))]) - 1
    heads.push(unpack(entry[0])[0])
    for (const f of forms[id]) {
      const ids = of.get(f)
      if (!ids) of.set(f, [id])
      else if (!ids.includes(id)) ids.push(id)
    }
  }
  const lemmas = (w) => of.get(w) || []
  return {
    stop: new Set((Array.isArray(data?.stop) ? data.stop : []).map(fold)),  // the lectures' own service words (lexicon-format.md §3)
    knows: (w) => of.has(w),
    lemmas,
    // the lemma of a group the found form shares with the query's word
    lemma: (found, w) => heads[lemmas(found).find((id) => lemmas(w).includes(id)) ?? lemmas(found)[0]] ?? found,
    // every form of every lemma of the word; null — the lexicon does not know it
    spread: (w) => (of.has(w) ? new Set(lemmas(w).flatMap((id) => forms[id])) : null),
  }
}
