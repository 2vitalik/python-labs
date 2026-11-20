// what a site is, as the platform sees it. start() fills it from the site's own site.js before anything is drawn:
// read it inside functions and components, never at the top of a module
export const site = {
  name: '',  // the tab title «<page> · name», the hint of the home link
  links: [],  // the menu: [path, text, access?, bold?, icon?]; access — when the entry is narrower than the page (a page students reach another way); icon — a name of Icon.vue: what stands for the word in a menu of icons
  guide: [],  // guide pages in the order of /method: { slug, path, nav }; `n` — a lab's number
  history: {  // «Історія правок» of the guide's pages (HistoryPage.vue)
    path: '/method/history',  // its address on the site
    // a page's place on the site by its slug: (slug) => ({ path, crumbs: [[to, text], …], more?: { to, text } }) — the way to it
    // and the site's own page on its changes; null — the guide's: site.guide under «Методичка»
    place: null,
  },
  colls: {},  // /activity: what an edit in the site's own collection is called — { claims: 'заявка' }
  start: {  // «Перші кроки» of a home page (StartSteps.vue): sign in and link the bot — always
    week: false,  // …and mark the week: the site has /my/week and asks its students for it
    note: '',  // the site's own line under the steps
  },
  repos: true,  // labs come as GitHub repositories: the profile's link and badge, the /students filter, the repo columns of «Звід» and «Строки»
  profile: {
    repo: '',  // the example in the GitHub field
    github: [],  // hints under it, HTML lines
  },
  students: {
    page: '',  // what /students/<nick> shows, the text of links to it — «Гра»
    cols: [],  // /students, columns after the name: { title, text: (s) => …, to: (s) => … }
    facets: [],  // /students, filters after «вхід»: { key, text, title, has: (s) => …, keep? — remembered as the view is, table? — false: no checkmark column in /table }
    cards: null,  // /students as a gallery: a component that takes `students`
    inGallery: null,  // who has a card in the gallery: (s) => …; null = everyone
    asStudent: null,  // the same page for a student — a slice of it: { title, crumbs: [[to, text], …] } — its name and where it hangs; null = the admin's only
  },
  table: {
    cols: [],  // /table (T240), the site's own columns: { key, type, title, short, get: (row) => …, link?: (row) => url }; `group` — the band above, default students.page; `fam` — like columns share a line of the catalog
    emojiPanel: null,  // a picker for a view's icon: a component with props `icon`, `hint` and the event `pick`; null — a small palette
  },
}
