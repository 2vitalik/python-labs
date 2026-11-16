// typical game emojis for an entity's own icon (T270 §7), in small groups — the form's field and the card's head
export const EMOJI_SETS = [
  ['люди й істоти', '🧍 🧙 🥷 🤖 👾 👻 🧟 💀 🐉 🐍 🕷️ 🦇 🐺 🐱 🐸 🐟 👽'],
  ['речі', '🔑 💎 🪙 🍎 🍒 ❤️ ⭐ 💣 🔸 🏹 🗡️ 🛡️ 📦 🧪 🎁'],
  ['клітини й природа', '🧱 🟫 🟩 🟦 ⬛ 🌲 🪨 🌊 🔥 ❄️ 🌵 🚪 🕳️'],
  ['знаки', '🚩 🏁 🎯 ❌ ⭕ ⚡ ✨ 💥 ❓ 🔒'],
].map(([name, list]) => [name, list.split(' ')])
