import { vocab } from './catalog.js'

// a wallet in one number and the grade it would give (T284 §4, app/api/grading.py): coins double from kind to kind, so
// the sum is counted in the cheapest, 🌱; the scale — when the API hands it out — maps the sum to a grade

// {coin: amount} → the sum in 🌱
export const woodOf = (coins) => Object.entries(coins || {}).reduce((s, [c, n]) => s + n * (vocab.value.grade?.wood?.[c] || 0), 0)

// → the grade, or null when the viewer is not shown the scale
export function gradeOf(wood) {
  const scale = vocab.value.grade?.scale || []
  if (!scale.length) return null
  for (let i = 1; i < scale.length; i++) {
    const [w0, g0] = scale[i - 1], [w1, g1] = scale[i]
    if (wood < w1) return Math.floor(g0 + ((g1 - g0) * (wood - w0)) / (w1 - w0))
  }
  return scale.at(-1)[1]
}
