import { COINS } from './catalog.js'
import EmojiPanel from './components/EmojiPanel.vue'
import StudentCards from './components/StudentCards.vue'

// what this site is; the platform (core/ui) takes it through start() in main.js

// guide sections in menu order: slug = data/guide/<slug>.md; `page` = own route rendered by GuidePage;
// `pic` — the drawing that stands for the word in a menu of icons (Icon.vue)
export const SECTIONS = [
  { slug: 'labs', path: '/labs', nav: 'Лаби', icon: '🧪', pic: 'flask', page: true },
  { slug: 'game', path: '/games', nav: 'Ігри', icon: '👾', pic: 'games' },  // text on top of the catalog page (GuideHead)
  { slug: 'tasks', path: '/tasks', nav: 'Таски', icon: '🧩', pic: 'puzzle' },
  { slug: 'score', path: '/score', nav: 'Бали', icon: '🪙', pic: 'medal', page: true },
  { slug: 'howto', path: '/howto', nav: 'Здача', icon: '✅', pic: 'done', page: true },
]
const link = (s) => [s.path, s.nav, null, false, s.pic]
export const CHANGES = { slug: 'changes', path: '/changes', nav: 'Що змінилось', page: true }  // not in the menu: linked from the home page
const LABS = [1, 2, 3, 4, 5].map((n) => ({ slug: `lab${n}`, path: `/labs/${n}`, n }))
// /table: how far a student's game description has got — entities, windows, rules
const FILL = { full: { emoji: '🟢', text: 'є сутності, вікна й правила', color: 'green' }, part: { emoji: '🟡', text: 'почато', color: 'yellow' },
               name: { emoji: '🌱', text: 'лише назва', color: 'orange' }, none: { emoji: '∅', text: 'гри нема', color: 'red' } }
const parts = (s) => [s.game.entities || 0, s.game.windows || 0, s.game.rules || 0]
const filled = (s) => (!s.game.id ? 'none' : parts(s).every(Boolean) ? 'full' : parts(s).some(Boolean) ? 'part' : 'name')
// /table: a video of «Супровід» as `game.videos[key]` carries it — { at, n, link, status, need }
const VIDEO = { ok: { emoji: '✅', text: 'прийнято', color: 'green' }, sent: { emoji: '🎬', text: 'надіслано, чекає слова', color: 'yellow' },
                back: { emoji: '↩️', text: 'повернуто на доробку', color: 'orange' }, must: { emoji: '❗', text: 'обовʼязкове, ще нема', color: 'red' },
                skip: { emoji: '➖', text: 'не потрібно', color: 'gray' } }
function video(s, key) {
  const v = s.game.videos?.[key]
  if (!v) return null
  if (v.need === 'skip') return 'skip'
  if (!v.n) return v.need === 'must' ? 'must' : null
  return { accepted: 'ok', returned: 'back' }[v.status] || 'sent'
}
// when the first link came; «🕒» — after the lab's deadline of that student
function sent(s, key, lab) {
  const at = s.game.videos?.[key]?.at
  const due = lab && s.labs?.[lab]?.due
  return at ? { at, pre: due && new Date(at) > new Date(due) ? '🕒 ' : '' } : ''
}

export default {
  name: 'Python Labs',
  // the menu: [path, text, access, bold, icon] — the icon (a name of Icon.vue) stands for the word in a menu of icons
  links: [
    ...SECTIONS.slice(0, 2).map(link),
    ['/my/game', 'Гра', null, true, 'gamepad'],  // the student's own game — bold, right after the catalog of games «Ігри» (T291 §9)
    ...SECTIONS.slice(2).map(link), ['/lessons', 'Пари', 'admin', false, 'cap'],  // students see it later
    ['/ludopedia', 'Ігротека', 'admin', false, 'books'],  // the corpus of reference games — the teacher's while it is v1 (T260)
    ['/students', 'Студи', 'admin', false, 'users'], ['/deadlines', 'Строки', null, false, 'alarm'], ['/defenses', 'Захисти', 'admin', false, 'shield'], ['/table', 'Звід', null, false, 'table'],  // a student reaches /students as «Ігри студентів» from the games catalog
    ['/activity', 'Актив', null, false, 'chart'], ['/polls', 'Polls', null, false, 'bars'], ['/week', 'Week', null, false, 'calendar'], ['/my/profile', 'Профіль', null, false, 'user'],
  ],
  guide: [...SECTIONS.flatMap((s) => (s.slug === 'labs' ? [s, ...LABS] : [s])), CHANGES],
  colls: {
    student_games: 'гра', game_parts: 'обʼєкт гри', claims: 'заявка', rules: 'правило',
    tasks: 'картка каталогу', games: 'гра каталогу', refs: 'ідея', defenses: 'захист', remarks: 'зауваження',
  },
  profile: {
    repo: 'https://github.com/username/python-labs',
    github: [
      'Репозиторій має бути <b>приватним</b>, назву оберіть самостійно',
      '<b>Єдиний</b> на всі лаби — це один великий проєкт, без папок Lab1/Lab2',
      '<b>Розшар</b> його на викладача: Settings → Collaborators → <code>2vitalik</code>',
    ],
  },
  students: {
    page: 'Гра',
    cols: [{ title: 'Гра', text: (s) => s.game.title, to: (s) => `/students/${s.nick}` }],
    facets: [
      { key: 'game', text: '🎮 гра', title: 'Гра створена', has: (s) => s.game.id },
      { key: 'review', text: '⏳ є що перевірити', title: 'Є заявки, що чекають вердикту', has: (s) => s.game.waiting, keep: true, table: false },
    ],
    cards: StudentCards,
    inGallery: (s) => s.game.id,  // the gallery is of games: no card without one
    asStudent: { title: 'Ігри студентів', crumbs: [['/method', 'Методичка'], ['/games', 'Ігри']] },
  },
  table: {  // /table, the site's own columns (T240): the student's game as the API row carries it (`game`)
    emojiPanel: EmojiPanel,
    cols: [
      { key: 'gname', type: 'text', title: 'Назва гри', short: '🕹', get: (s) => s.game.title, link: (s) => s.game.id && `/students/${s.nick}` },
      // how far the game's description has got (T315 §10): what deadline 2 and lab 3 ask for
      { key: 'gfill', type: 'enum', title: 'Опис гри: що заповнено', short: '📖', fam: 'gfill', options: FILL, get: filled,
        sub: (s) => (parts(s).some(Boolean) ? `🧩${parts(s)[0]} 🪟${parts(s)[1]} ⚡${parts(s)[2]}` : '') },
      { key: 'gents', type: 'number', title: 'Сутностей', short: '🧩', fam: 'gfill', get: (s) => s.game.entities },
      { key: 'gwins', type: 'number', title: 'Вікон', short: '🪟', fam: 'gfill', get: (s) => s.game.windows },
      { key: 'grules', type: 'number', title: 'Правил', short: '⚡', fam: 'gfill', get: (s) => s.game.rules },
      { key: 'glevels', type: 'number', title: 'Рівнів', short: '🗺', fam: 'gfill', get: (s) => s.game.levels },
      // the videos of «Супровід» (T318): a demo for labs 3 and 4, the defenses — the mark is the teacher's word, the link opens it
      ...[['demo3', 'Демо до лаби 3', '🎬', 3], ['demo4', 'Демо до лаби 4', '🎬', 4], ['defense1', 'Асинхронний захист 1', '🛡', 0], ['defense2', 'Асинхронний захист 2', '🛡', 0]]
        .map(([key, title, short, lab]) => ({ key, type: 'enum', title, short, fam: key.replace(/\d/, ''), options: VIDEO, get: (s) => video(s, key),
          link: (s) => s.game.videos?.[key]?.link, sub: (s) => sent(s, key, lab), hint: (s) => s.game.videos?.[key]?.n > 1 && `версій: ${s.game.videos[key].n}` })),
      { key: 'claims', type: 'number', title: 'Заявок у «Моїй грі»', short: '📋', fam: 'claims', get: (s) => s.game.claims },
      { key: 'waiting', type: 'number', title: 'Заявок чекають вердикту', short: '⏳', fam: 'claims', get: (s) => s.game.waiting },
      { key: 'coins', type: 'text', title: 'Монетки за заявками', short: '🪙', fam: 'coins', get: (s) => coins(s.game.coins) },
      { key: 'wood', type: 'number', title: 'Заявлено, у 🌱', short: '🌱', fam: 'coins', get: (s) => s.game.wood_claimed },
      { key: 'wood_ok', type: 'number', title: 'Зараховано, у 🌱', short: '🌱✓', fam: 'coins', get: (s) => s.game.wood_accepted },
    ],
  },
}

// {gold: 2, silver: 1.5} → «🥇2 🥈1.5»
const coins = (c) => Object.entries(c || {}).map(([kind, n]) => `${COINS[kind] || kind}${Number.isInteger(n) ? n : n.toFixed(1)}`).join(' ')
