import { roleOf, vocab } from './catalog.js'

// sentences КОЛИ → ЯКЩО → ТО rendered from the API's vocab (models/vocab.py), the same way the server and the bot do

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

export function partName(parts, id) {
  if (vocab.value.sides[id]) return vocab.value.sides[id]
  const p = parts.find((x) => x.id === id)
  if (!p) return '?'
  return p.kind === 'entity' ? `${roleOf(p.role).icon}${p.title}` : p.title
}

export function render(spec, args, name) {
  const values = {}
  for (const a of spec.args) {
    const v = args[a.name]
    if (v === undefined || v === null || v === '') { values[a.name] = ''; continue }
    if (a.type === 'entity' || a.type === 'window') values[a.name] = name(v)
    else if (a.type.startsWith('choice:')) values[a.name] = vocab.value.options[a.type.slice(7)]?.[v] ?? String(v)
    else values[a.name] = String(v)
  }
  let out = spec.tpl
  for (const seg of out.match(/\[[^\]]*\]/g) || []) {
    const keys = [...seg.matchAll(/\{(\w+)/g)].map((m) => m[1])
    out = out.replace(seg, keys.some((k) => !values[k]) ? '' : seg.slice(1, -1))
  }
  for (const [k, v] of Object.entries(values)) {
    out = out.replaceAll(`{${k}:+}`, v && !v.startsWith('-') ? `+${v}` : v).replaceAll(`{${k}}`, v)
  }
  return out.trim()
}

export const wordText = (dic, item, name) => {
  const spec = specOf(dic, item.kind)
  return (item.not ? 'не ' : '') + (spec ? render(spec, item, name) : item.kind || '?')
}

export function sentence(rule, parts) {
  const name = (id) => partName(parts, id)
  const when = wordText('triggers', rule.when, name)
  const cond = (rule.cond || []).map((c) => wordText('conditions', c, name)).join(' і ')
  const then = rule.then.map((e) => wordText('effects', e, name)).join(' · ')
  return { when, cond, then }
}

// which group a rule belongs to on the page — by its trigger's group in the vocab
export const ruleGroup = (rule) => specOf('triggers', rule.when.kind)?.group || 'інше'
export const RULE_GROUP_ORDER = ['контакт', 'ввід і час', 'стан і лічильники', 'життєвий цикл', 'пазли', 'інше']

// does the rule mention this part — in the trigger, the conditions or the effects
export const mentions = (rule, id) => [rule.when, ...(rule.cond || []), ...rule.then].some((it) => Object.values(it).includes(id))
