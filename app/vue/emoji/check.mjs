// node app/vue/emoji/check.mjs [запит …] — the picker's search without a browser (T309): with queries — what each finds;
// without — the checks below: «query → the icon that must come first» (or among the first five, after «~»)
import { readFileSync } from 'node:fs'

import { ready } from '../src/emoji/load.js'
import { find, suggest } from '../src/emoji/search.js'

const { items } = ready(JSON.parse(readFileSync(new URL('../src/emoji/data.json', import.meta.url), 'utf8')))
const top = (q, n = 5) => find(items, q).rows.slice(0, n).map((r) => r.it.char)

const CHECKS = `
стіна 🧱 · стіни 🧱 · wall 🧱 · ключ 🔑 · key 🔑 · монетка 🪙 · coin 🪙 · серденько ❤️ · червоне серце ❤️ · хп ❤️
зірочка ⭐ · зірка ⭐ · бомба 💣 · міна 💣 · привид 👻 · ghbdbl 👻 · ghost 👻 · ворог 👾 · enemy 👾 · гравець 🧍
двері 🚪 · вихід 🚪 · фініш 🚩 · скарб 💎 · кіт 🐱 · змія 🐍 · трава 🌱 · вогонь 🔥 · кружечок ~🔴 · квадратик ~🟩
зелений квадратик 🟩 · blue square 🟦 · жовтий 🟨 · білий привид 👻 · чорний кіт 🐈‍⬛ · тетріс 🟩 · пакмен 👻
ящик ~📦 · зілля ~🧪 · аптечка ~🩹 · танк ~🚜 · портал ~🌀 · вода ~🌊 · пастка ~🕳️ · сегмент 🟩 · шахи ~♟️
# # · █ █ · 🦄 🦄`.trim().split(/\n| · /).map((s) => s.trim().split(/ (?=\S+$)/))

if (process.argv.length > 2) {
  for (const q of process.argv.slice(2)) {
    const { rows, as } = find(items, q)
    console.log(`${q}${as ? ` → «${as}»` : ''} (${rows.length}): ${rows.slice(0, 24).map((r) => r.it.char + (r.why ? `‹${r.why}›` : '')).join(' ')}`)
    console.log(`  за назвою: ${suggest(items, q).map((it) => it.char).join(' ')}`)
  }
} else {
  const bad = CHECKS.filter(([q, want]) => (want.startsWith('~') ? !top(q).includes(want.slice(1)) : top(q, 1)[0] !== want))
  for (const [q, want] of bad) console.log(`✗ ${q}: чекали ${want}, є ${top(q).join(' ')}`)
  console.log(`${CHECKS.length - bad.length} / ${CHECKS.length}`)
  process.exit(bad.length ? 1 : 0)
}
