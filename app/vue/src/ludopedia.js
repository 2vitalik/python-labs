import { request } from '@core/http.js'

// the ludopedia corpus (data/ludopedia/, T253): reference games described in the language of the students' games

export const getLudoGames = () => request('/api/ludopedia')
export const getLudoGame = (slug) => request(`/api/ludopedia/${slug}`)
export const getLudoStats = () => request('/api/ludopedia/stats')
export const getLudoByCard = (slug) => request(`/api/ludopedia/by-card/${slug}`)

// family folder → [title, what the player mostly does] (taxonomy/families.md)
export const FAMILIES = {
  'push-slide': ['Штовхання і ковзання', 'штовхнути, зсунути'],
  'dig-gravity': ['Копання і клітинна фізика', 'копати, падати'],
  'maze-arcade': ['Лабіринтні аркади', 'бігти, тікати, їсти'],
  'grid-platformer': ['Платформери на сітці', 'лазити, ставити блоки'],
  'falling-match': ['Падаючі блоки і збіги', 'скласти, зібрати 3'],
  thinky: ['Thinky-головоломки', 'думати, відкривати правило'],
  'pencil-logic': ['Паперові логічні пазли', 'розмітити за обмеженнями'],
  'hidden-deduction': ['Приховане поле й дедукція', 'відкрити, вгадати безпечно'],
  'chess-abstract': ['Шахи й абстрактні стратегії', 'ходити фігурою, бити'],
  tactics: ['Покрокові тактики', 'рухати загін, атакувати'],
  roguelike: ['Роглайки', 'досліджувати, виживати'],
  'tower-lanes': ['Tower defense і смуги', 'ставити, захищати'],
  'build-sim': ['Будування й автоматизація', 'ставити, вирощувати, крутити'],
  'program-robots': ['Програмування на сітці', 'написати програму'],
  'connect-rotate': ['Зʼєднання й обертання', 'зʼєднати, повернути, відбити'],
  'board-digital': ['Настільні з сіткою', 'викласти плитку, заповнити'],
  'word-number': ['Словесні й числові', 'вгадати, скласти слово'],
}
export const KLASSES = { avatar: 'аватарна', cursor: 'курсорна', figure: 'фігурна', puzzle: 'пазл', hybrid: 'гібрид' }
export const STAGES = { v1: 'вільний опис', v2: 'перевірено', v3: 'звірено з каталогом' }
// axis → [label, EN value → UA] (vocab/classes.md)
export const AXES = {
  field: ['Поле', { square: 'квадрат', hex: 'гекс', graph: 'граф', free: 'вільне', iso: 'ізометрія', layers: 'шари', '1d': 'лінія', '3d': 'обʼєм', nested: 'вкладене', hyperbolic: 'гіперболічне' }],
  time: ['Час', { turn: 'покрокова', realtime: 'реальний час', static: 'статична', rhythm: 'ритм', programmed: 'програмована', wego: 'усі планують → виконання' }],
  opponent: ['Суперник', { none: 'нема', ai: 'AI', hotseat: 'hot-seat', online: 'онлайн', coop: 'кооп' }],
  info: ['Інформація', { full: 'повна', hidden: 'прихована', partial: 'часткова' }],
  random: ['Випадковість', { none: 'нема', setup: 'на старті', runtime: 'у грі', both: 'на старті й у грі' }],
  goal: ['Мета', { score: 'очки', survive: 'вижити', state: 'стан поля', constraints: 'обмеження', race: 'гонка', territory: 'територія', collect: 'зібрати', none: '—' }],
}
export const axisText = (k, v) => AXES[k]?.[1][v] || v
// the 13 sections of TEMPLATE.md, in order
export const SECTIONS = [
  ['essence', 'Суть'], ['field', 'Поле і час'], ['entities', 'Сутності'], ['rules', 'Правила (КОЛИ → ЯКЩО → ТО)'],
  ['controls', 'Керування і ввід'], ['ui', 'Вікна, меню, HUD'], ['features', 'Фічі поза полем'], ['variations', 'Варіації й родичі'],
  ['course', 'Цікавинки для курсу'], ['catalog_map', 'Мапа на каталог'], ['proposals', 'Пропозиції до словників'],
  ['sources', 'Джерела'], ['uncertain', 'Непевне'],
]
export const LINK_KINDS = { wiki: 'Wikipedia', official: 'офіційний', steam: 'Steam', youtube: 'YouTube', play: 'грати', fandom: 'вікі', bgg: 'BGG', itch: 'itch.io', other: 'стаття' }
