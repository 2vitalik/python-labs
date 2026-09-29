import 'katex/dist/katex.min.css'

import katex from 'katex'

// formulas in lectures and labs: `$…$` in a line, `$$…$$` as a block — each on one line (sites/ods/data READMEs)
const MATH = /^\$\$([^\n]+?)\$\$|^\$([^\n$]+?)\$/

export default {
  extensions: [{
    name: 'math',
    level: 'inline',
    start: (src) => src.indexOf('$'),
    tokenizer(src) {
      const m = MATH.exec(src)
      if (m) return { type: 'math', raw: m[0], tex: m[1] ?? m[2], block: !!m[1] }
    },
    renderer: (t) => katex.renderToString(t.tex, { displayMode: t.block, throwOnError: false }),
  }],
}
