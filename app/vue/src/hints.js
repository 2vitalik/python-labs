import { kindOf, missingParams } from './catalog.js'
import { isDraft } from './myGame.js'
import { mentions } from './rules.js'

// where a card of a kind must sit; a claim anchored elsewhere is «not in its place» (the catalog changed under it)
const HOME = { mechanic: 'entity', element: 'window', field: 'field', level: 'level' }
const misplaced = (c, task, parts) => {
  const kind = kindOf(task)
  if (c.auto || !c.part) return kind === 'rule' && !c.rule ? false : kind !== 'rule' && !!c.rule
  return (HOME[kind] || 'none') !== parts.find((p) => p.id === c.part)?.kind
}

// what the short form still lacks (T270 §12): entities and windows only
function simpleHints({ game, parts }) {
  const out = []
  const ents = parts.filter((p) => p.kind === 'entity'), wins = parts.filter((p) => p.kind === 'window')
  if (!game.description) out.push({ to: 'about', text: 'Кілька речень опису вгорі: що за гра і чим відрізняється від основи.' })
  if (!ents.length) out.push({ to: 'entities', text: 'Хто й що є на полі? У секції «Сутності» натисни «＋ сутність»: гравець, вороги, стіни, предмети.' })
  if (!wins.length) out.push({ to: 'windows', text: 'Які екрани має гра? У секції «Вікна» натисни «＋ вікно»: ігровий екран, меню, кінець гри.' })
  const bare = ents.find((e) => !e.description)
  if (bare) out.push({ to: `p-${bare.id}`, text: `«${bare.title}» — допиши одним реченням, що це і як поводиться (олівець на картці).` })
  return out
}

// what the description still lacks — gentle, at most a handful, each naming the place and the button
export function hints({ game, parts, rules, claims, info, base, simple }) {
  if (simple) return simpleHints({ game, parts }).slice(0, 4)
  const out = []
  const ents = parts.filter((p) => p.kind === 'entity'), wins = parts.filter((p) => p.kind === 'window')
  const effects = new Set(rules.flatMap((r) => r.then.map((e) => e.kind)))
  const puzzle = base?.klass === 'puzzle'
  if (!parts.some((p) => p.kind === 'field')) out.push({ to: 'field', text: 'Опиши поле: у секції «Поле» натисни «Описати поле» — сітка, вид, час, керування.' })
  if (!ents.some((p) => ['player', 'piece', 'mark'].includes(p.role))) out.push({ to: 'entities', text: 'Хто гравець? «＋ сутність» з типом «гравець» (або фігура чи розмітка).' })
  const lone = ents.find((e) => !claims.some((c) => c.part === e.id && !c.auto) && !rules.some((r) => mentions(r, e.id)))
  if (lone) out.push({ to: `p-${lone.id}`, text: `«${lone.title}» ще ні в чому не бере участі: додай правило з нею — як рухається, що стається при контакті.` })
  if (ents.length && !effects.has('win') && !puzzle) out.push({ to: 'rules', text: 'Як виграти? «＋ правило» з ефектом «перемога».' })
  if (ents.length && !effects.has('lose') && !puzzle) out.push({ to: 'rules', text: 'Як програти? «＋ правило» з ефектом «поразка».' })
  if (ents.length && !parts.some((p) => p.kind === 'level')) out.push({ to: 'levels', text: 'Опиши рівні: «＋ рівень» — хоч один: звідки береться, розмір, скриншот.' })
  if (!wins.some((w) => w.task === 'game-screen')) out.push({ to: 'windows', text: '«＋ вікно» з типом «Ігровий екран» і скриншотом гри.' })
  const bare = wins.find((w) => !w.screenshots.length)
  if (bare) out.push({ to: `p-${bare.id}`, text: `Скриншот для вікна «${bare.title}» — рамка з плюсом на його картці.` })
  const star = claims.find((c) => info(c.task)?.tags?.includes('algo') && !c.link)
  if (star) out.push({ to: `c-${star.id}`, text: `⭐ «${info(star.task).title}» — додай посилання на код: алгоритмічні картки перевіряються по ньому.` })
  const empty = claims.find((c) => !c.auto && missingParams(info(c.task), c.params).length)
  if (empty) out.push({ to: `c-${empty.id}`, text: `«${info(empty.task).title}» чекає параметрів — натисни на рядок картки й заповни.` })
  if (claims.some((c) => isDraft(c, info(c.task)))) out.push({ to: 'drafts', text: 'У чернетках є картки без місця — натисни на картку, далі «Перемістити».' })
  const astray = claims.find((c) => info(c.task) && misplaced(c, info(c.task), parts))
  if (astray) out.push({ to: `c-${astray.id}`, text: `«${info(astray.task).title}» лежить не на своєму місці — натисни на неї, далі «Перемістити».` })
  if (!game.description) out.push({ to: 'about', text: 'Кілька речень опису вгорі: що за гра і чим відрізняється від основи.' })
  return out.slice(0, 5)
}
