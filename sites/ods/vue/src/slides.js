// a lecture's slides: its text cut at `<!-- слайд N -->` (T166 Q2–Q3); a slide with nothing on it is left out
const MARK = /<!--\s*слайд\s+(\d+)\s*-->/

export function slidesOf(text) {
  const parts = (text || '').split(MARK)  // [before, n, text, n, text, …]
  const out = parts[0].trim() ? [{ n: 0, text: parts[0].trim() }] : []
  for (let i = 1; i < parts.length; i += 2) {
    if (parts[i + 1].trim()) out.push({ n: Number(parts[i]), text: parts[i + 1].trim() })
  }
  return out
}
