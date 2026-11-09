---
title: Cloud Gardens
slug: cloud-gardens
aka: []
family: build-sim
also: []
klass: cursor
axes:
  field: free
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 2021
platforms: [PC, Mac, Xbox One, Xbox Series, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1372320", best: true, note: "офіційний опис: предмети підживлюють ріст, кожен предмет треба вкрити зеленню, sandbox і creative"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cloud_Gardens_(video_game)", note: "сміття обмежене, точне розміщення, покрити достатньо діорами, інакше рестарт"}
  - {kind: other, url: "https://waytoomany.games/2022/07/26/review-cloud-gardens-switch/", note: "огляд: коло впливу предмета, рослина росте до межі й дає насіння, типи насіння"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cloud+Gardens+Noio+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [coverage-area, collect-quota, restart-level, sequential-levels, in-game-editor, editor-palette, share-result, player-camera, +influence-radius-growth, +cover-objects-goal, +seed-from-growth, +limited-placement-stock]
proposes: ["+trigger:covered(obj)", "+effect:grow_toward(plant, obj)", "+ui:influence-ring", "+feature:loop-video-export", "+card:influence-radius-growth"]
author: opus
date: 2026-11-09
---

# Cloud Gardens — кладеш сміття біля паростка, і рослина росте до нього, доки зелень не вкриє всю діораму

## Суть
Гравець садить насіння на маленькій 3D-діорамі покинутого міста (парковка, дах, майданчик) і **ставить поруч уламки** — іграшки, автівки, банки. Кожен предмет має **коло впливу**: рослини в ньому ростуть. Рослина росте до фіксованого розміру, дає насіння і зупиняється; щоб росла далі — знову підживити предметом. Рівень пройдено, коли зелень вкрила досить діорами (кожен цільовий предмет); сміття обмежене, тож невдале розміщення змушує почати рівень заново.

**Межа сімʼї**: поле **вільне** (3D-поверхні діорами, без клітин), тому це не клітинна гра — опис короткий, як межовий випадок поруч із [townscaper](townscaper.md) (там нерегулярна сітка, тут сітки нема зовсім).

## Поле і час
- Поле — 3D-діорама з вільним розміщенням на поверхнях; камера лише обертається й наближається.
- Предмети мають фізику — стоси сміття можуть хитатися й падати (огляди).
- Час — ріст рослин після підживлення триває кілька секунд (?), без ворогів і таймера рівня.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Насіння | supply | тип (лоза, кактус, бамбук…) | садиться на поверхню; типи ростуть по-різному |
| Рослина | neutral | межа росту | росте, коли в колі впливу предмета; досягла межі — дає насіння, зупиняється |
| Предмет-сміття | object | коло впливу, запас обмежений | поставлений поруч підживлює ріст; ціль покриття |
| Цільові предмети діорами | zone | — | кожен треба вкрити листям для проходження |
| Насіння на рослині | pickup | — | збирається (часом треба покрутити камеру) і садиться деінде |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(plant, seed, point)` → ТО `place(player, plant)`, `take(player, seed)`.
- КОЛИ `input(place, junk, point)` → ЯКЩО `has(player, junk)` → ТО `place(player, junk)`, `take(player, junk)`.
- КОЛИ `in_range(junk, plant, r)` → ЯКЩО `not state(plant, max_size)` → ТО `grow(plant, n)`, `custom: «гілки тягнуться до предмета»`.
- КОЛИ `counter(plant_size, ==, max)` → ТО `set_state(plant, max_size)`, `spawn(seed)`.
- КОЛИ `picked(player, seed)` → ТО `give(player, seed)`, `clear_state(plant, max_size)` — рослина знову може рости від нового предмета.
- КОЛИ `custom: «усі цільові предмети вкриті зеленню»` → ТО `win`, `next_level`.
- КОЛИ `custom: «запас сміття вичерпано, покриття недостатнє»` → ТО `restart`.

## Керування і ввід
- Миша/геймпад: вибір насіння або предмета з панелі → привид з колом впливу → клік у точку діорами; обертання й зум камери.
- Перемикач типу насіння на панелі (огляд: «не дуже пояснено»).

## Вікна, меню, HUD
- `main-menu`: кампанія, creative, налаштування.
- `level-select` — розділи кампанії з діорамами (?).
- `game-screen`: діорама, панель насіння й предметів з кількістю, `influence-ring` при перенесенні, `progress-bar` покриття (?).
- `editor-window` — creative mode: зібрати свою діораму з відкритих предметів і рослин.
- `end-screen` рівня з експортом зацикленого відео.

## Фічі поза полем
- `mode-sandbox` (без цілей) і creative-конструктор з розблокованим каталогом предметів і рослин.
- Експорт зацикленого відео готової діорами; генеративний звук.

## Варіації й родичі
- [townscaper](townscaper.md) — іграшка розміщення з контекстом, але на сітці; [terra-nil](terra-nil.md) — відновлення природи на клітинах з умовами покриття.
- **Осі варіацій**: поле (клітини / вільне) · що живить ріст (сусіди-клітини / коло впливу предмета) · мета (нема / % покриття / кожна ціль).

## Цікавинки для курсу
- Ріст у колі впливу предмета, обмежений межею розміру з «перезарядкою» через збір насіння — 📎 (на клітинах — `coverage-area` + лічильник).
- Мета «вкрити кожну ціль» замість % поля — 🌱.
- Обмежений запас предметів = пазл розміщення з рестартом — 🌱.

## Мапа на каталог
- Є: `coverage-area` ↔ коло впливу · `collect-quota` ↔ покрити цілі · `restart-level` · `sequential-levels` · `in-game-editor` + `editor-palette` ↔ creative · `share-result` ↔ експорт відео · `player-camera`.
- **Нема** → пропозиції карток:
  - `+influence-radius-growth` «Предмет у радіусі живить ріст сутності» · entities/state · 📎 · слоти {radius, max_size}.
  - `+cover-objects-goal` «Вкрити кожен цільовий обʼєкт» · game-logic/win · 🌱.
  - `+seed-from-growth` «Виросла сутність дає ресурс на наступну посадку» · game-logic/economy · 🌱.
  - `+limited-placement-stock` «Обмежений запас предметів на рівень» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:covered(obj)` — обʼєкт вкрито (рослинністю/фарбою) повністю.
- `+effect:grow_toward(plant, obj)` — ріст у напрямку джерела, не рівномірно.
- `+ui:influence-ring` — коло впливу предмета під час перенесення.
- `+feature:loop-video-export` — експорт зацикленого відео результату.
- `+card:influence-radius-growth` — див. вище.

## Джерела
- ⭐ [Steam: Cloud Gardens](https://store.steampowered.com/app/1372320) — офіційний опис: предмети заохочують ріст, кожен предмет треба вкрити, sandbox, creative, експорт відео, Noio, дати.
- [Wikipedia: Cloud Gardens](https://en.wikipedia.org/wiki/Cloud_Gardens_(video_game)) — насіння, обмежене сміття, точне розміщення, покриття рівня, рестарт, платформи (Coatsink).
- [WayTooManyGames: огляд Switch](https://waytoomany.games/2022/07/26/review-cloud-gardens-switch/) — коло впливу, межа росту й насіння, типи насіння, creative, понад 100 рівнів.

## Непевне
- (?) Чи є індикатор % покриття і як саме рахується «досить» (за предметами чи площею).
- (?) Тривалість росту; чи шкодить «неправильне розміщення» (Wikipedia: може зашкодити саду) — механізм невідомий.
- (?) Структура кампанії (розділи), кількість рівнів (огляд: «понад сто»).
