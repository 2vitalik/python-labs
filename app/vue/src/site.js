import StudentCards from './components/StudentCards.vue'

// what this site is; the platform (core/ui) takes it through start() in main.js

// guide sections in menu order: slug = data/guide/<slug>.md; `page` = own route rendered by GuidePage
export const SECTIONS = [
  { slug: 'labs', path: '/labs', nav: 'Лаби', page: true },
  { slug: 'game', path: '/games', nav: 'Ігри' },  // text on top of the catalog page (GuideHead)
  { slug: 'tasks', path: '/tasks', nav: 'Таски' },
  { slug: 'score', path: '/score', nav: 'Бали', page: true },
  { slug: 'howto', path: '/howto', nav: 'Здача', page: true },
]
export const CHANGES = { slug: 'changes', path: '/changes', nav: 'Що змінилось', page: true }  // not in the menu: linked from the home page
const LABS = [1, 2, 3, 4, 5].map((n) => ({ slug: `lab${n}`, path: `/labs/${n}`, n }))

export default {
  name: 'Python Labs',
  links: [
    ...SECTIONS.map((s) => [s.path, s.nav]),
    ['/students', 'Студи'], ['/activity', 'Актив'], ['/polls', 'Опитування'], ['/my/game', 'Моя гра'], ['/week', 'Тиждень'], ['/my/profile', 'Профіль'],
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
    facets: [{ key: 'game', text: '🎮 гра', title: 'Гра створена', has: (s) => s.game.id }],
    cards: StudentCards,
  },
}
