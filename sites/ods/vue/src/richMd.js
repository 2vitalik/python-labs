// the lab pages' callouts (T357 §4): a quote that starts with 💡 · ⚠️ · 🎯 is a tip · a trap · the answers; rich.css
// gives each its colour. Any other quote is left to the platform's renderer (`false`)
const KINDS = [['💡', 'tip'], ['⚠', 'trap'], ['🎯', 'check']]  // ⚠ with or without its emoji selector

export default {
  renderer: {
    blockquote({ tokens }) {
      const first = tokens[0]?.type === 'paragraph' ? tokens[0].text.trimStart() : ''
      const kind = KINDS.find(([emoji]) => first.startsWith(emoji))?.[1]
      return kind ? `<blockquote class="callout ${kind}">\n${this.parser.parse(tokens)}</blockquote>\n` : false
    },
  },
}
