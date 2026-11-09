import { missingParams } from './catalog.js'
import { mentions } from './rules.js'
import { anchorKind } from './myGame.js'

// what the description still lacks — gentle, at most a handful, each pointing at a section
export function hints({ game, parts, rules, claims, tasks, base }) {
  const out = []
  const ents = parts.filter((p) => p.kind === 'entity')
  const wins = parts.filter((p) => p.kind === 'window')
  const effects = new Set(rules.flatMap((r) => r.then.map((e) => e.kind)))
  const puzzle = base?.klass === 'puzzle'
  if (!parts.some((p) => p.kind === 'field')) out.push({ to: 'field', text: 'Опиши поле: розмір, сітка, час, керування.' })
  if (!ents.some((p) => ['player', 'piece', 'mark'].includes(p.role))) out.push({ to: 'entities', text: 'Хто гравець? Додай сутність із роллю «гравець» (або фігуру чи розмітку).' })
  for (const e of ents) {
    if (!claims.some((c) => c.part === e.id) && !rules.some((r) => mentions(r, e.id))) {
      out.push({ to: `p-${e.id}`, text: `«${e.title}» ще без механік і правил: як рухається, що стається при контакті?` })
      break
    }
  }
  if (ents.length && !effects.has('win') && !puzzle) out.push({ to: 'rules', text: 'Як виграти? Правило з ефектом «перемога».' })
  if (ents.length && !effects.has('lose') && !puzzle) out.push({ to: 'rules', text: 'Як програти? Правило з ефектом «поразка».' })
  if (!wins.some((w) => w.task === 'game-screen')) out.push({ to: 'windows', text: 'Додай вікно «Ігровий екран» зі скриншотом гри.' })
  const bare = wins.find((w) => !w.screenshots.length)
  if (bare) out.push({ to: `p-${bare.id}`, text: `Скриншот для вікна «${bare.title}».` })
  const star = claims.find((c) => tasks[c.task]?.tags?.includes('algo') && !c.link)
  if (star) out.push({ to: 'game', text: `⭐ «${tasks[star.task].title}» — додай посилання на код: алгоритмічні картки перевіряються по ньому.` })
  const empty = claims.find((c) => missingParams(tasks[c.task], c.params).length)
  if (empty) out.push({ to: 'game', text: `«${tasks[empty.task].title}» чекає параметрів — відкрий чіп і заповни.` })
  const draft = claims.find((c) => !c.part && anchorKind(tasks[c.task]) !== 'game')
  if (draft) out.push({ to: 'drafts', text: 'У чернетках є картки без господаря — привʼяжи їх до сутності чи вікна.' })
  if (!game.description) out.push({ to: 'about', text: 'Кілька речень опису: що за гра і чим відрізняється від основи.' })
  return out.slice(0, 5)
}
