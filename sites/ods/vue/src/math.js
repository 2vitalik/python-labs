import 'katex/dist/katex.min.css'

import katex from 'katex'

// formulas in lectures and labs: `$…$` in a line, `$$…$$` as a block — each on one line (sites/ods/data READMEs)
const MATH = /^\$\$([^\n]+?)\$\$|^\$([^\n$]+?)\$/
// `\col{b}{…}` — a part of a formula in the lecturer's colour (T381): that part gets the class of his tag `<c-b>`
// (lecAuthor.css). Of KaTeX's \html… only this class is let in
const OPTIONS = { throwOnError: false, macros: { '\\col': '\\htmlClass{c-#1}{#2}' },
                  trust: (c) => c.command === '\\htmlClass' && /^c-[a-z]$/.test(c.class),
                  strict: (code) => (code === 'htmlExtension' ? 'ignore' : 'warn') }

export default {
  extensions: [{
    name: 'math',
    level: 'inline',
    start: (src) => src.indexOf('$'),
    tokenizer(src) {
      const m = MATH.exec(src)
      if (m) return { type: 'math', raw: m[0], tex: m[1] ?? m[2], block: !!m[1] }
    },
    renderer: (t) => katex.renderToString(t.tex, { ...OPTIONS, displayMode: t.block }),
  }],
}
