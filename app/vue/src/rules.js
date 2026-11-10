import { iconOf, vocab } from './catalog.js'

// sentences КОЛИ / ЯКЩО / ТО built from the API's vocab (models/vocab.py). A clause is a list of typed pieces, so the page
// can show an entity, a number, a state and the student's own words each in its own way (T270 §4.1)

export const specOf = (dic, kind) => vocab.value[dic]?.[kind]
export const groups = (dic) => {
  const out = {}
  for (const [k, s] of Object.entries(vocab.value[dic] || {})) (out[s.group] ??= []).push({ key: k, ...s })
  return out
}

// what an entity arg may hold besides a Part: anyone, the trigger's sides
export const sidesFor = (when) => {
  const out = ['*']
  if (when?.a !== undefined) out.push('@a')
  if (when?.b !== undefined) out.push('@b')
  if (when?.a !== undefined && when?.b !== undefined) out.push('@both')
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

function argPiece(a, v, item, ctx) {
  if (a.type === 'entity' || a.type === 'window') {
    if (vocab.value.sides[v]) return { t: 'side', v: vocab.value.sides[v] }
    const p = ctx.parts.find((x) => x.id === v)
    return p ? { t: a.type, id: p.id, v: p.title, icon: iconOf(p) } : { t: 'free', v: '?' }
  }
  if (a.type === 'int') return { t: 'num', v: String(v).replace('-', '−') }
  if (a.type.startsWith('choice:')) return { t: 'choice', v: vocab.value.options[a.type.slice(7)]?.[v] ?? String(v) }
  const t = NAMED[a.name] || 'free'
  return t === 'state' ? { t, v: String(v), unknown: !knowsState(item, v, ctx) } : { t, v: String(v) }
}

// one word of a sentence with its arguments → pieces [{ t: word|entity|window|side|num|choice|state|name|free|not, v, … }]
export function pieces(dic, item, ctx) {
  const spec = specOf(dic, item.kind)
  const out = item.not ? [{ t: 'not', v: 'не' }] : []
  if (!spec) return [...out, { t: 'free', v: item.kind || '?' }]
  let tpl = spec.tpl
  for (const seg of tpl.match(/\[[^\]]*\]/g) || []) {  // an optional part stays only when all its args are given
    const keys = [...seg.matchAll(/\{(\w+)/g)].map((m) => m[1])
    tpl = tpl.replace(seg, keys.every((k) => filled(item[k])) ? seg.slice(1, -1) : '')
  }
  const args = Object.fromEntries(spec.args.map((a) => [a.name, a]))
  for (const chunk of tpl.split(/(\{\w+(?::\+)?\})/)) {
    const m = chunk.match(/^\{(\w+)(:\+)?\}$/)
    if (!m) {
      const w = chunk.replace(/[«»]/g, '').trim()  // the quotes of a template give way to the piece's own look
      if (w) out.push({ t: 'word', v: w })
    } else if (filled(item[m[1]])) {
      const p = argPiece(args[m[1]], item[m[1]], item, ctx)
      if (m[2] && p.t === 'num' && !p.v.startsWith('−')) p.v = `+${p.v}`
      out.push(p)
    }
  }
  return out
}

export function clauses(rule, parts) {
  const ctx = { parts, when: rule.when }
  return {
    when: pieces('triggers', rule.when, ctx),
    cond: (rule.cond || []).map((c) => pieces('conditions', c, ctx)),
    then: rule.then.map((e) => pieces('effects', e, ctx)),
  }
}

// the same as plain text — for a title, a table cell, a search
export const plain = (ps) => ps.map((p) => (p.icon ? `${p.icon} ${p.v}` : p.v)).join(' ')
export function sentence(rule, parts) {
  const c = clauses(rule, parts)
  return { when: plain(c.when), cond: c.cond.map(plain).join(' і '), then: c.then.map(plain).join(' · ') }
}

// which group a rule belongs to on the page — by its trigger's group in the vocab
export const ruleGroup = (rule) => specOf('triggers', rule.when.kind)?.group || 'інше'
export const RULE_GROUP_ORDER = ['контакт', 'ввід і час', 'стан і лічильники', 'життєвий цикл', 'пазли', 'інше']

// does the rule mention this part — in the trigger, the conditions or the effects
export const mentions = (rule, id) => [rule.when, ...(rule.cond || []), ...rule.then].some((it) => Object.values(it).includes(id))
