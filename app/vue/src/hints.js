import { answersOf, isHidden } from './advice.js'
import { needsWhy } from './asked.js'
import { kindOf, missingParams, NEEDS_SCREEN, PAIRS, vocab } from './catalog.js'
import { isDraft } from './myGame.js'
import { mentions } from './rules.js'
import { dueSoon } from './videos.js'

// where a card of a kind must sit; a claim anchored elsewhere is «not in its place» (the catalog changed under it)
const HOME = { mechanic: 'entity', element: 'window', field: 'field', level: 'level' }
const misplaced = (c, task, parts) => {
  const kind = kindOf(task)
  if (c.auto || !c.part) return kind === 'rule' && !c.rule ? false : kind !== 'rule' && !!c.rule
  return (HOME[kind] || 'none') !== parts.find((p) => p.id === c.part)?.kind
}
const WAITS = { mechanic: 'Сутності', element: 'Вікна й переходи', rule: 'Правила' }  // the section whose strip a claim without a place waits in

// a demo whose lab's deadline is two weeks away or gone, and no link yet (T318): the first thing to say
function demoHint(videos, section) {
  const v = dueSoon(videos)
  return v ? [{ to: `v-${v.slot}`, text: `🎬 Демка до лаби ${v.lab} — дедлайн ${new Date(v.due).toLocaleDateString('uk-UA', { day: 'numeric', month: 'long' })}: встав посилання на відео в секції «${section}».` }] : []
}

// a function of the game claimed with nothing on a window to work it: «є гучність — а де слайдер?» (the other way round
// from PairAdvice). Only the functions that cannot live without their window or element (NEEDS_SCREEN): a pause
// or records do without one. Names the window types and elements that are in the catalog; an advice — it can be hidden (T278 §11)
function reversePair({ game, claims, wins, info }) {
  const has = (slug) => claims.some((c) => c.task === slug) || wins.some((w) => w.task === slug)
  for (const fn of new Set(claims.map((c) => c.task))) {
    const keys = NEEDS_SCREEN.includes(fn) ? Object.keys(PAIRS).filter((k) => answersOf(k).includes(fn)) : []
    const key = `need:${fn}`
    if (!keys.length || keys.some(has) || isHidden(game.id, key)) continue
    const want = keys.filter((k) => info(k)).map((k) => `${kindOf(info(k)) === 'window' ? 'вікно' : 'елемент'} «${info(k).title}»`)
    if (want.length) return { to: 'windows', key, advice: true, text: `Є «${info(fn)?.title || fn}». Може, у грі є й ${want.join(' або ')}? Якщо так — додай у секції «Вікна й переходи».` }
  }
}

// what the description still lacks — gentle, at most a handful, the base first, the most useful first, each naming the
// place and the button; of a feature (T319) — only while it is shown (`has`). `sandbox` — the sample's scratch copy: no
// screenshots to add there, no head form to write the description in, no why to give
export function hints({ game, parts, rules, claims, videos, info, base, has, sandbox = false }) {
  const out = demoHint(videos, has('support') ? 'Супровід' : 'Відео')
  const ents = parts.filter((p) => p.kind === 'entity'), wins = parts.filter((p) => p.kind === 'window')
  const effects = new Set(rules.flatMap((r) => r.then.map((e) => e.kind)))
  const puzzle = base?.klass === 'puzzle'
  if (!sandbox && !game.description) out.push({ to: 'about', text: 'Кілька речень опису вгорі: що за гра і чим відрізняється від основи.' })
  if (!ents.length) out.push({ to: 'entities', text: 'Хто й що є на полі? У секції «Сутності» натисни «＋ сутність»: гравець, вороги, стіни, предмети.' })
  else if (!ents.some((p) => ['player', 'piece', 'mark'].includes(p.role))) out.push({ to: 'entities', text: 'Хто гравець? «＋ сутність» з типом «гравець» (або фігура чи розмітка).' })
  if (!wins.length) out.push({ to: 'windows', text: 'Які екрани має гра? У секції «Вікна й переходи» натисни «＋ вікно»: ігровий екран, меню, кінець гри.' })
  else if (!wins.some((w) => w.task === 'game-screen')) out.push({ to: 'windows', text: '«＋ вікно» з типом «Ігровий екран» і скриншотом гри.' })
  // a field card without the field sits down by itself once the field is described: the field's hint below covers it
  const waiting = claims.filter((c) => isDraft(c, info(c.task)) && WAITS[kindOf(info(c.task))])
  if (waiting.length) {
    const c = waiting[0], kind = kindOf(info(c.task)), more = waiting.length > 1 ? ` (і ще ${waiting.length - 1})` : ''
    const how = kind === 'rule' ? '«нове правило з цієї картки» або «Перемістити»' : '«Перемістити»'
    out.push({ to: `c-${c.id}`, text: `«${info(c.task)?.title || c.task}»${more} ще без місця — у секції «${WAITS[kind]}»: натисни на картку, далі ${how}.` })
  }
  const empty = claims.find((c) => !c.auto && missingParams(info(c.task), c.params).length)
  if (empty) out.push({ to: `c-${empty.id}`, text: `«${info(empty.task).title}» чекає параметрів — натисни на рядок картки й заповни.` })
  const astray = claims.find((c) => info(c.task) && misplaced(c, info(c.task), parts))
  if (astray) out.push({ to: `c-${astray.id}`, text: `«${info(astray.task).title}» лежить не на своєму місці — натисни на неї, далі «Перемістити».` })
  const unsaid = claims.find((c) => c.status === 'claimed' && !c.why && needsWhy(info(c.task), sandbox || vocab.value.features.free))
  if (unsaid) out.push({ to: `c-${unsaid.id}`, text: `«${info(unsaid.task).title}» — картка за запитом без пояснення: допиши одним реченням, що саме в грі це робить.` })
  if (ents.length && !effects.has('win') && !puzzle) out.push({ to: 'rules', text: 'Як виграти? «＋ правило» з ефектом «перемога».' })
  if (ents.length && !effects.has('lose') && !puzzle) out.push({ to: 'rules', text: 'Як програти? «＋ правило» з ефектом «поразка».' })
  if (has('field') && !parts.some((p) => p.kind === 'field')) out.push({ to: 'field', text: 'Опиши поле: у секції «Поле» натисни «Описати поле» — сітка, вид, час, керування.' })
  if (has('levels') && ents.length && !parts.some((p) => p.kind === 'level')) out.push({ to: 'levels', text: 'Опиши рівні: «＋ рівень» — хоч один: звідки береться, розмір, скриншот.' })
  const lone = ents.find((e) => !claims.some((c) => c.part === e.id && !c.auto) && !rules.some((r) => mentions(r, e.id)))
  if (lone) out.push({ to: `p-${lone.id}`, text: `«${lone.title}» ще ні в чому не бере участі: додай правило з нею — як рухається, що стається при контакті.` })
  const plain = ents.find((e) => !e.description)
  if (plain) out.push({ to: `p-${plain.id}`, text: `«${plain.title}» — допиши одним реченням, що це і як поводиться («＋ опис» на картці).` })
  const bare = !sandbox && wins.find((w) => !w.screenshots.length)
  if (bare) out.push({ to: `p-${bare.id}`, text: `Скриншот для вікна «${bare.title}» — рамка з плюсом на його картці.` })
  const pair = has('elements') && reversePair({ game, claims, wins, info })
  if (pair) out.push(pair)
  const star = claims.find((c) => info(c.task)?.tags?.includes('algo') && !c.link)
  if (star) out.push({ to: `c-${star.id}`, text: `⭐ «${info(star.task).title}» — додай посилання на код: алгоритмічні картки перевіряються по ньому.` })
  const nameless = parts.find((p) => p.kind === 'menu' && p.window && p.items.some((it) => !it.title))  // leads somewhere, says not how (T318)
  if (nameless) out.push({ to: `p-${nameless.window}`, text: `У вікні «${wins.find((w) => w.id === nameless.window)?.title || '…'}» є перехід без назви — допиши, як він відбувається: пункт меню, кнопка, клавіша.` })
  return out.slice(0, 5)
}
