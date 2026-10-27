// what a site is, as the platform sees it. start() fills it from the site's own site.js before anything is drawn:
// read it inside functions and components, never at the top of a module
export const site = {
  name: '',  // the tab title «<page> · name», the hint of the home link
  links: [],  // the menu: [path, text, access?, bold?]; access — when the entry is narrower than the page (a page students reach another way)
  guide: [],  // guide pages in the order of /method: { slug, path, nav }; `n` — a lab's number
  colls: {},  // /activity: what an edit in the site's own collection is called — { claims: 'заявка' }
  profile: {
    repo: '',  // the example in the GitHub field
    github: [],  // hints under it, HTML lines
  },
  students: {
    page: '',  // what /students/<nick> shows, the text of links to it — «Гра»
    cols: [],  // /students, columns after the name: { title, text: (s) => …, to: (s) => … }
    facets: [],  // /students, filters after «вхід»: { key, text, title, has: (s) => … }
    cards: null,  // /students as a gallery: a component that takes `students`
    inGallery: null,  // who has a card in the gallery: (s) => …; null = everyone
    asStudent: null,  // the same page for a student — a slice of it: { title, crumbs: [[to, text], …] } — its name and where it hangs; null = the admin's only
  },
  table: {
    cols: [],  // /table (T240), the site's own columns: { key, type, title, short, get: (row) => …, link?: (row) => url }; `group` — the band above, default students.page
  },
}
