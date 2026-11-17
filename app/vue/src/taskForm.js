import { putTask } from './api.js'
import { tasks } from './catalog.js'
import { byLang, OPT_HINT, subzoneKind } from './taskMeta.js'

// a catalog card ⇄ its in-place form on /tasks: flat fields to edit, the payload PUT / POST /api/tasks takes

export const csv = (s) => s.split(',').map((x) => x.trim()).filter(Boolean)
const num = (v, empty) => (v === '' || v == null ? empty : Number(v))

export function toForm(t) {
  const a = byLang(t.aliases)
  const tags = t.tags || []
  return {
    slug: t.slug || '', title: t.title || '', icon: t.icon || '', description: t.description || '',
    zone: t.zone, subzone: t.subzone, status: t.status || 'draft', parent: t.parent || '', order: t.order || 0,
    // the API answers with the kind resolved; the subzone's own stays '' so the card keeps following its subzone
    kind: t.kind && t.kind !== subzoneKind(t.zone, t.subzone, tags) ? t.kind : '', opt: t.opt || '',
    coin: t.coin || '', amount: t.amount ?? 1, max_count: t.max_count ?? 1, tags: tags.join(', '), games: (t.games || []).join(', '),
    slots: (t.slots || []).map((s) => ({ ...s, options: [...(s.options || [])] })),
    aliases: { uk: [...(a.uk || [])], en: [...(a.en || [])], ru: [...(a.ru || [])] },
    rule: t.rule || {}, proof: t.proof || '',
    // price steps (T291 §13): null — the editor was never opened, nothing goes; [] — taken off
    tiers: t.tiers?.length ? t.tiers.map((s) => [...s]) : null,
  }
}

// `rule` and `opt` go only with the kinds they mean something for, `tiers` — once the form touched them; left out, the API
// keeps what the card had
export function toPayload(f, kind) {
  const { rule, opt, tiers, ...rest } = f
  const out = {
    ...rest, tags: csv(f.tags), games: csv(f.games), proof: f.proof || '',
    amount: num(f.amount, 1), max_count: num(f.max_count, 1), order: num(f.order, 0),
    slots: f.slots.map(({ options, ...s }) => (s.type === 'choice' ? { ...s, options } : s)),
  }
  if (kind === 'rule') out.rule = rule
  if (OPT_HINT[kind]) out.opt = opt
  if (tiers) out.tiers = tiers.map(([upto, factor]) => [Number(upto) || 0, Number(factor)])
  return out
}

// loadCatalog() caches its promise: the API's answer goes into the loaded list, in the order the API sorts a subzone by
const bySpot = (a, b) => a.order - b.order || (a.slug > b.slug) - (a.slug < b.slug)
export const place = (t) => { tasks.value = [...tasks.value.filter((x) => x.id !== t.id), t].sort(bySpot) }

// one value changed where it reads (T306): the server takes a card whole, so the rest goes back through the same form.
// Saves run one after another, each from the card the save before brought back — two quick changes must not send the old copy
let line = Promise.resolve()
export function saveTask(task, patch) {
  const run = line.then(async () => {
    const f = { ...toForm(tasks.value.find((x) => x.id === task.id) || task), ...patch }
    place(await putTask(task.id, toPayload(f, f.kind || subzoneKind(f.zone, f.subzone, csv(f.tags)))))
  })
  line = run.catch(() => {})
  return run
}
