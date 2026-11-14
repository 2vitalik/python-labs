import { COINS } from './catalog.js'
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

export default {
  name: 'Python Labs',
  // the menu: [path, text, access, bold, icon] — the icon (a name of Icon.vue) stands for the word in a menu of icons
  links: [
    ...SECTIONS.slice(0, 2).map(link),
    ['/my/game', 'Гра', null, true, 'gamepad'],  // the student's own game — bold, right after the catalog of games «Ігри» (T291 §9)
    ...SECTIONS.slice(2).map(link), ['/lessons', 'Пари', 'admin', false, 'cap'],  // students see it later
    ['/ludopedia', 'Ігротека', 'admin', false, 'books'],  // the corpus of reference games — the teacher's while it is v1 (T260)
    ['/students', 'Студи', 'admin', false, 'users'], ['/deadlines', 'Строки', null, false, 'alarm'], ['/table', 'Звід', null, false, 'table'],  // a student reaches /students as «Ігри студентів» from the games catalog
    ['/activity', 'Актив', null, false, 'chart'], ['/polls', 'Polls', null, false, 'bars'], ['/week', 'Week', null, false, 'calendar'], ['/my/profile', 'Профіль', null, false, 'user'],
  ],
  guide: [...SECTIONS.flatMap((s) => (s.slug === 'labs' ? [s, ...LABS] : [s])), CHANGES],
  colls: {
    student_games: 'гра', game_parts: 'обʼєкт гри', claims: 'заявка', rules: 'правило',
    tasks: 'картка каталогу', games: 'гра каталогу', refs: 'ідея',
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
    cols: [
      { key: 'game', type: 'text', title: 'Гра', short: '🎮', get: (s) => s.game.title, link: (s) => s.game.id && `/students/${s.nick}` },
      { key: 'claims', type: 'number', title: 'Заявок у «Моїй грі»', short: '📋', get: (s) => s.game.claims },
      { key: 'coins', type: 'text', title: 'Монетки за заявками', short: '🪙', get: (s) => coins(s.game.coins) },
      { key: 'waiting', type: 'number', title: 'Заявок чекають вердикту', short: '⏳', get: (s) => s.game.waiting },
      { key: 'wood', type: 'number', title: 'Заявлено, у 🌱', short: '🌱', get: (s) => s.game.wood_claimed },
      { key: 'wood_ok', type: 'number', title: 'Зараховано, у 🌱', short: '🌱✓', get: (s) => s.game.wood_accepted },
    ],
  },
}

// {gold: 2, silver: 1.5} → «🥇2 🥈1.5»
const coins = (c) => Object.entries(c || {}).map(([kind, n]) => `${COINS[kind] || kind}${Number.isInteger(n) ? n : n.toFixed(1)}`).join(' ')
