import { zones } from './catalog.js'

// what a record of /ideas is (T274 §4): its sign, its name alone and in the filter, the form's hints for it
export const KINDS = {
  link: { icon: '🔗', one: 'посилання', many: 'посилання', title: 'Назва — за бажанням', note: 'Що тут крутого' },
  idea: { icon: '💡', one: 'ідея картки', many: 'ідеї карток', title: 'Назва картки', note: 'Що це і що має бути видно в грі' },
  fix: { icon: '🛠', one: 'про наявну картку', many: 'про картки', title: 'Що не так', note: 'Де їй місце, який опис чи ціна були б точніші' },
  site: { icon: '🐞', one: 'про сайт', many: 'про сайт', title: 'Що сталося або чого бракує', note: 'Подробиці: де це, що робив — за бажанням' },
}
export const STATES = { inbox: 'нові', linked: 'взяті', dropped: 'відхилені' }
// records from before T274 know only link | idea, and a url makes a find
export const refKind = (r) => (KINDS[r.kind] ? r.kind : r.url ? 'link' : 'idea')

// «👾 Сутності → 🎭 Типи сутностей»; '' for no category or one the catalog doesn't know
export function zonePath(zone, sub) {
  const z = zones.value[zone]
  if (!z) return ''
  const s = z.subzones[sub]
  return `${z.icon} ${z.title}${s ? ` → ${s[1]} ${s[0]}` : ''}`
}
