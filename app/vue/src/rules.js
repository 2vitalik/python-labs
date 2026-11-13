import { iconOf, vocab } from './catalog.js'
import { marks, sidePiece } from './ruleSides.js'

// sentences КОЛИ / ЯКЩО / ТО built from the API's vocab (models/vocab.py). A clause is a list of typed pieces, so the page
// can show an entity, a number, a state and the student's own words each in its own way (T270 §4.1)

export const specOf = (dic, kind) => vocab.value[dic]?.[kind]
export const groups = (dic) => {
  const out = {}
  for (const [k, s] of Object.entries(vocab.value[dic] || {})) (out[s.group] ??= []).push({ key: k, ...s })
  return out
}

// what an entity arg may hold besides a Part: anyone, the trigger's sides it has filled
export const sidesFor = (when) => {
  const out = ['*']
  if (filled(when?.a)) out.push('@a')
  if (filled(when?.b)) out.push('@b')
  if (filled(when?.a) && filled(when?.b)) out.push('@both')
  return out
}

const NAMED = { s: 'state', name: 'name', phase: 'name' }  // text args that name something declared elsewhere
const filled = (v) => v !== undefined && v !== null && v !== ''

// does the entity the clause talks about (its `a`, a side resolved through the trigger) declare this state
function knowsState(item, s, ctx) {
  const ref = String(item.a || '').startsWith('@') ? ctx.when?.[item.a.slice(1)] : item.a
  const own = ctx.parts.find((p) => p.id === ref)?.states
  return (own?.length ? own : ctx.parts.flatMap((p) => p.states || [])).includes(s)
}

// `flip` — the comparison turned around for a negation ({op:!}): «≥» for «не <»
function argPiece(a, v, item, ctx, flip) {
  if (a.type === 'entity' || a.type === 'window') {
    if (v === '@a' || v === '@b') return sidePiece(v.slice(1), ctx)
    if (vocab.value.sides[v]) return { t: 'side', v: vocab.value.sides[v] }
    const p = ctx.parts.find((x) => x.id === v)
    return p ? { t: a.type, id: p.id, v: p.title, icon: iconOf(p) } : { t: 'free', v: '?' }
  }
  if (a.type === 'int') return { t: 'num', v: String(v).replace('-', '−') }
  if (a.type.startsWith('choice:')) {
    const label = (x) => vocab.value.options[a.type.slice(7)]?.[x] ?? String(x)
    return flip ? { t: 'not', v: label(vocab.value.op_not?.[v] ?? v), tip: `заперечення: не «${label(v)}»` } : { t: 'choice', v: label(v) }
  }
  const t = NAMED[a.name] || 'free'
  return t === 'state' ? { t, v: String(v), unknown: !knowsState(item, v, ctx) } : { t, v: String(v) }
}

// a template's words; a negation marks its word of «not» as !не! (models/vocab.py NEG)
const words = (chunk) => chunk.split(/!([^!]+)!/)
  .map((w, i) => ({ t: i % 2 ? 'not' : 'word', v: w.replace(/[«»]/g, '').trim() }))  // template quotes give way to the pieces' look
  .filter((p) => p.v)

// one word of a sentence with its arguments → pieces [{ t: word|entity|window|side|num|choice|state|name|free|not, v, … }].
// A negated condition reads through its `neg` template; a word without one starts with a `lead` «не» (RuleText: «ЯКЩО НЕ»).
// ctx: { parts, when, marks } — marks from ruleSides.js put a side's letter (`sub`, of side `sd`) next to the trigger's side
export function pieces(dic, item, ctx) {
  const spec = specOf(dic, item.kind)
  const neg = item.not && spec?.neg
  const out = item.not && !neg ? [{ t: 'not', v: 'не', lead: true }] : []
  if (!spec) return [...out, { t: 'free', v: item.kind || '?' }]
  let tpl = neg || spec.tpl
  for (const seg of tpl.match(/\[[^\]]*\]/g) || []) {  // an optional part stays only when all its args are given
    const keys = [...seg.matchAll(/\{(\w+)/g)].map((m) => m[1])
    tpl = tpl.replace(seg, keys.every((k) => filled(item[k])) ? seg.slice(1, -1) : '')
  }
  const args = Object.fromEntries(spec.args.map((a) => [a.name, a]))
  for (const chunk of tpl.split(/(\{\w+(?::[+!])?\})/)) {
    const m = chunk.match(/^\{(\w+)(?::([+!]))?\}$/)
    if (!m) out.push(...words(chunk))
    else if (filled(item[m[1]])) {
      const p = argPiece(args[m[1]], item[m[1]], item, ctx, m[2] === '!')
      if (m[2] === '+' && p.t === 'num' && !p.v.startsWith('−')) p.v = `+${p.v}`
      if (dic === 'triggers' && ctx.marks?.[m[1]]) Object.assign(p, { sub: ctx.marks[m[1]], sd: m[1] })
      out.push(p)
    }
  }
  return out
}

export function clauses(rule, parts) {
  const ctx = { parts, when: rule.when, marks: marks(rule) }
  return {
    when: pieces('triggers', rule.when, ctx),
    cond: (rule.cond || []).map((c) => pieces('conditions', c, ctx)),
    then: rule.then.map((e) => pieces('effects', e, ctx)),
  }
}

// the same as plain text — for a title, a table cell, a search
export const plain = (ps) => ps.map((p) => [p.icon, p.v, p.sub && `(${p.sub})`].filter(Boolean).join(' ')).join(' ')
export function sentence(rule, parts) {
  const c = clauses(rule, parts)
  return { when: plain(c.when), cond: c.cond.map(plain).join(' та '), then: c.then.map(plain).join(' · ') }
}

// which group a rule belongs to on the page — by its trigger's group in the vocab
export const ruleGroup = (rule) => specOf('triggers', rule.when.kind)?.group || 'інше'
export const RULE_GROUP_ORDER = ['контакт', 'ввід і час', 'стан і лічильники', 'життєвий цикл', 'пазли', 'інше']

// does the rule mention this part — in the trigger, the conditions or the effects
export const mentions = (rule, id) => [rule.when, ...(rule.cond || []), ...rule.then].some((it) => Object.values(it).includes(id))
