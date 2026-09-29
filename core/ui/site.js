// what a site is, as the platform sees it. start() fills it from the site's own site.js before anything is drawn:
// read it inside functions and components, never at the top of a module
export const site = {
  name: '',  // the tab title «<page> · name», the hint of the home link
  links: [],  // the menu: [path, text]
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
  },
}
