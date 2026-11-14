import { FENCE, fenced, headText, parse, quoted } from './momentsText.js'

// a game's examples cut for the page (T274 §8, T276): the legend, then scenarios of frames, the text itself unchanged.
// A frame is a picture with its caption under it (T284 §5) → { grid, caption, after }: the caption was written to stand
// before the picture and ends with a colon — shown under it, the colon is left out; the stored text keeps it. Nothing is
// dropped: a scenario's text after its last grid stays with its last frame. A bare fence is drawn as a field all the same

// «…праворуч:» · «…не потрібно):*» · «…приз (🟡):⏎*(стрілки малювати не потрібно)*» → the same without the colon
const under = (caption) => caption.replace(/:(\*{0,3})(\s*\n\*\([^\n]*\)\*)?\s*$/, '$1$2')

export function moments(text) {
  const m = parse(text)
  const scenarios = m.scenarios.map((s) => ({
    title: s.title,
    tail: s.frames.length ? '' : s.tail,
    frames: s.frames.map((f, i) => ({
      grid: fenced(f, FENCE), caption: under(f.caption),
      after: [f.note && quoted(f.note), i === s.frames.length - 1 && s.tail].filter(Boolean).join('\n\n'),
    })),
  })).filter((s) => s.frames.length || s.tail || s.title)
  if (!scenarios.some((s) => s.frames.length)) return { legend: text || '', scenarios: [] }
  return { legend: headText(m), scenarios }
}
