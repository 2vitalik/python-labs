// guide markdown headings: stable ids (explicit `{#id}` or transliterated text) and section slicing for the editor
const TR = {
  а: 'a', б: 'b', в: 'v', г: 'h', ґ: 'g', д: 'd', е: 'e', є: 'ie', ж: 'zh', з: 'z', и: 'y', і: 'i', ї: 'i', й: 'i',
  к: 'k', л: 'l', м: 'm', н: 'n', о: 'o', п: 'p', р: 'r', с: 's', т: 't', у: 'u', ф: 'f', х: 'kh', ц: 'ts', ч: 'ch',
  ш: 'sh', щ: 'shch', ь: '', ю: 'iu', я: 'ia',
}
export const slugify = (s) => s.toLowerCase().replace(/[а-яґєії]/g, (c) => TR[c] ?? c)
  .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '')

export const ANCHOR = /\s*\{#([\w-]+)\}/g

// [id, plain text] of a heading's source text
export function headingId(raw) {
  const m = raw.match(/\{#([\w-]+)\}/)
  const plain = raw.replace(ANCHOR, '').replace(/[*_`]/g, '').trim()
  return [m ? m[1] : slugify(plain), plain]
}

// headings outside fenced code with their line ranges: a section runs to the next heading of the same or higher level
export function sections(text) {
  const lines = (text || '').split('\n')
  const out = []
  let fence = false
  lines.forEach((l, i) => {
    if (/^\s*```/.test(l)) fence = !fence
    const m = !fence && l.match(/^(#{1,6})\s+(.*)$/)
    if (m) {
      const [id, title] = headingId(m[2])
      out.push({ id, title, depth: m[1].length, from: i })
    }
  })
  out.forEach((h, i) => (h.to = out.slice(i + 1).find((n) => n.depth <= h.depth)?.from ?? lines.length))
  return out
}

export const section = (text, id) => sections(text).find((h) => h.id === id)

export function sliceSection(text, id) {
  const h = section(text, id)
  return h ? text.split('\n').slice(h.from, h.to).join('\n') : ''
}

export function spliceSection(text, id, part) {
  const h = section(text, id)
  if (!h) return text
  const lines = text.split('\n')
  return [...lines.slice(0, h.from), ...part.split('\n'), ...lines.slice(h.to)].join('\n')
}
