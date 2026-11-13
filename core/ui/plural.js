// the Ukrainian word after a number: plural(23, 'сутність', 'сутності', 'сутностей') → 'сутності'
export function plural(n, one, few, many) {
  const d = n % 10
  const t = n % 100
  return d === 1 && t !== 11 ? one : d >= 2 && d <= 4 && (t < 12 || t > 14) ? few : many
}
