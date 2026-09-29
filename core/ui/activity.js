import { onMounted, onUnmounted } from 'vue'

// the activity page (T146): what the filter chips stand for and how a row of each journal reads

// chip → feed sources behind it; `on` — shown until the admin says otherwise:
// every API call is noise, and alerts repeat what the journals already say
export const CHIPS = [
  { key: 'site', icon: '🌐', text: 'Сайт', src: ['login', 'view'], on: true },
  { key: 'edit', icon: '✏️', text: 'Зміни', src: ['edit'], on: true },
  { key: 'tg', icon: '✈️', text: 'Telegram', src: ['tg'], on: true },
  { key: 'note', icon: '📝', text: 'Нотатки', src: ['note'], on: true },
  { key: 'fail', icon: '⚠️', text: 'Збої', src: ['fail'], on: true, title: 'API-виклики, що скінчились помилкою: 4xx і 5xx' },
  { key: 'error', icon: '💥', text: 'Помилки', src: ['error'], on: true, title: 'Необроблені помилки сайту, API і бота — з повним traceback' },
  { key: 'event', icon: '🔔', text: 'Алерти', src: ['event'], on: false, title: 'Важливі події — те, що бот шле в Telegram' },
  { key: 'api', icon: '⚙️', text: 'API', src: ['api'], on: false, title: 'Усі API-виклики' },
]
export const ICONS = { login: '🔑', view: '👁', api: '⚙️', fail: '⚠️', edit: '✏️', event: '🔔', error: '💥' }
export const ERRORS = { api: 'API', bot: 'бот', front: 'сайт' }
export const COLLS = { users: 'профіль', guide: 'методичка' }  // the site's own — site.colls
export const CHATS = { private: 'бот', business: 'особистий чат', group: 'група', supergroup: 'форум' }
export const TG_KINDS = { edit: 'правка', deleted: 'видалено', member: 'членство', reaction: 'реакція' }
export const PERIODS = [[1, 'сьогодні'], [7, '7 днів'], [30, '30 днів'], [0, 'весь час']]
const ONLINE = 5  // minutes since the last row that still count as «зараз на сайті»

const BROWSERS = [['Telegram', /Telegram/], ['Edge', /Edg/], ['Opera', /OPR/], ['Firefox', /Firefox|FxiOS/], ['Chrome', /Chrome|CriOS/], ['Safari', /Safari/]]
const SYSTEMS = [['Android', /Android/], ['iOS', /iPhone|iPad/], ['Windows', /Windows/], ['macOS', /Mac OS X/], ['Linux', /Linux/]]
const first = (list, ua) => list.find(([, re]) => re.test(ua))?.[0]

// «📱 Chrome · Android» out of a user-agent; an unknown one is shown as it is, rows older than the field have none
export function device(ua) {
  if (!ua) return ''
  const names = [first(BROWSERS, ua), first(SYSTEMS, ua)].filter(Boolean)
  return `${/Mobi|Android|iPhone|iPad/.test(ua) ? '📱' : '💻'} ${names.join(' · ') || ua.slice(0, 40)}`
}

// alert texts are Telegram HTML built from what people typed: shown as plain text, never as markup
export const plain = (html) => new DOMParser().parseFromString(html, 'text/html').body.textContent

const minutes = (iso) => (Date.now() - new Date(iso)) / 60000
export const online = (iso) => !!iso && minutes(iso) < ONLINE
export const clock = (iso) => new Date(iso).toLocaleTimeString('uk-UA')
export const dayMonth = (iso) => new Date(iso).toLocaleDateString('uk-UA', { day: 'numeric', month: 'short' })

export function ago(iso) {
  if (!iso) return '—'
  const m = minutes(iso)
  if (m < 1) return 'щойно'
  if (m < 60) return `${Math.floor(m)} хв тому`
  if (m < 60 * 24) return `${Math.floor(m / 60)} год тому`
  return m < 60 * 24 * 7 ? `${Math.floor(m / 60 / 24)} дн тому` : dayMonth(iso)
}

export function dayTitle(iso) {
  const days = Math.round((new Date().setHours(0, 0, 0, 0) - new Date(iso).setHours(0, 0, 0, 0)) / 864e5)
  const date = new Date(iso).toLocaleDateString('uk-UA', { weekday: 'short', day: 'numeric', month: 'long' })
  return days === 0 ? `сьогодні · ${date}` : days === 1 ? `вчора · ${date}` : date
}

// the page refreshes itself, but not in a background tab
export function usePolling(fn, seconds) {
  let timer
  onMounted(() => (timer = setInterval(() => document.hidden || fn(), seconds * 1000)))
  onUnmounted(() => clearInterval(timer))
}
