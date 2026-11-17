import { kindOf } from './catalog.js'

// what the game page holds beyond its base (T319): the owner turns a feature on — all at once, by checkboxes in
// «Можливості» or in place — and the choice is kept on the game (`game.extras`); a feature that has data is shown whatever
// the switch (featureData.js), so nothing filled is ever hidden. `section` — the editor's section the feature is;
// `place` — the section it sits inside, or `page` — the top of the page (the panel's map, T348); `more` — its word in
// the «ще тут» row of a base section (MoreRow)
export const FEATURES = [
  { id: 'cards', place: 'page', title: 'Вигляд «Картки»', text: 'усе заявлене деревом' },
  { id: 'looks', place: 'page', title: 'Налаштування вигляду', text: 'стовпці, розкладка, згорнуті картки, «усе / коротко / згорнуто»' },
  { id: 'etalon', place: 'page', title: 'Еталон основи', text: 'зразковий опис гри-основи: порожню гру можна почати з нього, а під «чого бракує» — «в еталоні є, а в тебе нема»' },
  { id: 'field', section: 'field', icon: '🗺️', title: 'Поле', text: 'сітка, вид, час, керування, фізика; скриншот; картки про поле' },
  { id: 'stats', place: 'entities', title: 'Параметри й стани', more: 'параметри й стани', text: 'HP, життя, швидкість… і стани «звичайний / посилений» на картці сутності' },
  { id: 'mechanics', place: 'entities', title: 'Механіки', more: 'механіки', text: 'картки каталогу на сутності: інвентар, тіло-черга, зона покриття' },
  { id: 'phases', place: 'rules', title: 'Порядок ходу', more: 'порядок ходу', text: 'що за чим відбувається за один хід чи тік' },
  { id: 'tables', place: 'rules', title: 'Таблиці правил', more: 'таблиці', text: 'ті самі правила таблицями: контакти, керування, час' },
  { id: 'logic', section: 'zone-game-logic', icon: '🎲', title: 'Логіка гри', text: 'картки про гру загалом: пауза, рекорд, збереження, суперник' },
  { id: 'levels', section: 'levels', icon: '🪜', title: 'Рівні', text: 'звідки рівень, розмір, параметри, скриншот; картки про рівні' },
  { id: 'map', place: 'levels', title: 'Мапа рівня клітинками', more: 'мапа рівня клітинками', text: 'намалювати рівень значками сутностей' },
  { id: 'moments', section: 'moments', icon: '🎞️', title: 'Розкадровка', text: 'ігрові моменти по кадрах' },
  { id: 'elements', place: 'windows', title: 'Елементи вікон', more: 'елементи вікон', text: 'що є на вікні: панель стану, лічильники, підсвітки — картками каталогу' },
  { id: 'interface', section: 'zone-interface', icon: '🕹️', title: 'Інтерфейс', text: 'анімації, ефекти, звук, статистика' },
  { id: 'support', section: 'zone-support', icon: '📣', title: 'Супровід: картки', text: 'сторінка гри, інструкція гравця, трейлер (відео — в основі)' },
]
export const FEATURE = Object.fromEntries(FEATURES.map((f) => [f.id, f]))
// what every game has, whatever is turned on — the head of the panel; `place` — its section on the page
export const BASE = [
  { icon: '🎮', title: 'Про гру', text: 'основа, назва, опис' },
  { place: 'entities', icon: '👾', title: 'Сутності', text: 'значок, назва, тип, опис, скриншот' },
  { place: 'rules', icon: '⚡', title: 'Правила', text: '«КОЛИ → ЯКЩО → ТО» списком і картка на правилі' },
  { place: 'windows', icon: '🪟', title: 'Вікна', text: 'назва, тип, опис, скриншот, переходи, схема вікон' },
  { place: 'zone-code', icon: '💻', title: 'Код', text: 'картки лаб і коду з посиланням' },
  { place: 'zone-support', icon: '📣', title: 'Відео', text: 'демки й захисти' },
]

// the feature a card's claim lives in, '' — the base (T321 contract): a `game` card by its category
const OF_KIND = { stat: 'stats', mechanic: 'mechanics', element: 'elements', fieldopt: 'field', field: 'field', level: 'levels' }
const OF_ZONE = { interface: 'interface', support: 'support', code: '' }
export const homeOf = (task) => (kindOf(task) === 'game' ? OF_ZONE[task?.zone] ?? 'logic' : OF_KIND[kindOf(task)] || '')
