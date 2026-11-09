---
title: Grain
slug: grain
aka: [Grain Free Demo]
family: dig-gravity
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: none
year: 2026
platforms: [web, PC (Windows, macOS, Linux)]
links:
  - {kind: itch, url: "https://frizzle3.itch.io/grain", best: true, note: "повна версія: 60+ матеріалів, 16 видів тварин, харчова мережа й піраміда енергії, машини, погода, 17 челенджів"}
  - {kind: play, url: "https://frizzle3.itch.io/grain-demo", note: "безкоштовне демо в браузері: 16 матеріалів, таблиця «демо / повна»"}
  - {kind: other, url: "https://frizzle3.itch.io/grain/devlog/1719410/grain-is-out", note: "девлог релізу, 20.10.2026"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Grain+falling+sand+ecosystem+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 30
mechanics: [cell-click, gravity-fall, cell-transform, spawner-entity, hunger-clock, editor-palette, editor-erase, save-multi-slot, save-progress, field-scaling, game-loop, +falling-sand-cell, +predator-prey, +decomposer-cycle, +food-web-view, +energy-pyramid, +day-night-cycle, +season-cycle, +weather-modifiers, +natural-disasters, +view-modes, +challenge-list, +discoveries-log]
proposes: ["+trigger:hunger", "+effect:breed", "+effect:eat", "+effect:decay", "+role:material", "+window:food-web", "+window:challenges", "+feature:photo-mode", "+card:decomposer-cycle", "+card:food-web-view", "+card:energy-pyramid", "+card:natural-disasters"]
author: opus
date: 2026-11-09
---

# Grain — falling-sand банка з живою харчовою мережею: тварини їдять, плодяться, голодують і гниють назад у ґрунт

## Суть
Пісочниця жанру falling sand: обираєш матеріал і «сиплеш» його в банку — пісок, воду, лаву, насіння, тварин, машини. Незвичне — **екосистема поверх клітинної фізики**: 16 видів тварин (жуки, бджоли, черви, риби, жаби, качки, кролі, лисиці, сови, змії…) їдять, розмножуються, голодують і стають їжею, а редуценти перетворюють рештки на ґрунт. Мережу видно наживо — діаграмою харчових звʼязків і пірамідою енергії; поверх — погода, сезони, катастрофи, 17 челенджів і «відкриття».

## Поле і час
- Квадратна сітка-«банка»; три розміри, включно з цілим світом, що скролиться; зум до 3×.
- Real-time; день і ніч, сезони, вітер і погода змінюють банку.
- Тепловий вид (thermal view) — другий шар відображення температури.
- Уся гра — один офлайновий HTML-файл (~150 кБ).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пісок · ґрунт (dirt) · камінь | object | порошок / тверде | падають / лежать |
| Вода · лава | object | рідина | течуть (?) щодо реакцій |
| Лід · дерево | object | тверде | (?) |
| Вогонь · тепло (heat) | hazard | — | палить; гріє сусідів (?) |
| Насіння · рослини · водорості | neutral | — | ростуть; їжа травоїдних |
| Тварини ×16 | neutral | енергія (?) | їдять, плодяться, голодують, гинуть; самі їжа для хижаків |
| Редуценти (черви, жуки (?)) | neutral | — | рештки → ґрунт |
| Батарея · лампа · вентилятор · конвеєр · насос | object | — | машини (?) щодо правил |
| Хмари · джерела · вентиляційні отвори | spawner | — | «makers»: породжують речовину (?) щодо якої |
| Гумка | — | — | інструмент: стирає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag)` → ТО `spawn_at(material, brush)`; гумка — `set_cell(cell, empty)`.
- КОЛИ `tick` → ЯКЩО `free(below)` → ТО `fall(powder)` — базове правило falling sand.
- КОЛИ `contact(predator, prey)` → ТО `custom: «зʼїсти»`, `disappear(prey)`, `custom: «енергія хижаку»`.
- КОЛИ `custom: «тварина сита»` → ТО `spawn(same_species)` — розмноження.
- КОЛИ `custom: «голод: енергія скінчилась»` → ТО `transform(animal, remains)`.
- КОЛИ `contact(decomposer, remains)` → ТО `transform(remains, soil)`.
- КОЛИ `timer(day)` → ТО `custom: «день ↔ ніч»`; КОЛИ `timer(season)` → ТО `custom: «наступний сезон»`.
- КОЛИ `custom: «катастрофа»` → ТО `custom: «землетрус / метеор / торнадо»` (?) щодо запуску: випадково чи кнопкою.
- КОЛИ `tick` → ТО `custom: «вітер і погода рухають частинки»` (?).
- КОЛИ `tick` → ТО `spawn_at(substance, maker)` — хмари, джерела, отвори (?) щодо речовин.
- КОЛИ `custom: «умову челенджу виконано»` → ТО `custom: «челендж зараховано»`; перша поява реакції/явища → `custom: «відкриття»` (?).
- Перемоги й поразки нема; є 17 челенджів (у демо — Glassblower, Aquarist) і десятки відкриттів.

## Керування і ввід
- Обрати матеріал → клік або drag (на тачі — drag пальцем) по банці: матеріал «сиплеться».
- Зум до 3×; скрол у великій банці; фото й відео з поля.

## Вікна, меню, HUD
- `game-screen`: банка + `element-picker` матеріалів і машин.
- `save-slots` — панель «Saved jars» (до 3, у демо — 1); банки не зберігаються самі — треба натиснути Save.
- `level-select` — готові банки (луг, ставок, вулканічний острів, ніч феєрверків; у демо — ставок, акваріум, бджолиний сад, вулканічний острів, порожня) і випадкові світи.
- `food-web` — жива діаграма харчової мережі й піраміда енергії (`+window:food-web`).
- `challenges` — список челенджів і відкриттів (`+window:challenges`).
- `settings-window` — зберігається автоматично.
- Перемикач теплового виду; захоплення фото/відео.

## Фічі поза полем
- `mode-sandbox` — уся гра; `puzzle-bank`-подібні челенджі (17) і `collectibles`-відкриття зберігаються автоматично.
- `save-slots` (3) без автосейву банки; `+feature:photo-mode` (фото й відео).
- `custom-difficulty` — розмір банки (3 варіанти).
- Демо: 16 матеріалів, 4 банки + порожня, 2 челенджі, 1 слот; повна ($5): 66 матеріалів, 17 банок + випадкові, 17 челенджів, 3 слоти, великі банки.
- Позначка автора: зроблено з допомогою AI (AI-код).

## Варіації й родичі
- Falling sand: [the-powder-toy](the-powder-toy.md), [sandspiel](sandspiel.md), [sandboxels](sandboxels.md); екологія на сітці — Wa-Tor і Sugarscape у `build-sim` (`+predator-prey`).
- **Осі варіацій**: живе в пісочниці — «нема (Powder Toy) / прості агенти (кліщі Sandspiel) / харчова мережа з 16 видів (Grain)»; мета — «нема / челенджі й відкриття»; вид — «звичайний / тепловий».

## Цікавинки для курсу
- Хижак і жертва на falling-sand сітці: енергія, розмноження, голод — 🥉.
- Редуценти: смерть → рештки → ґрунт (замкнений цикл речовини) — 📎.
- Жива діаграма харчової мережі (граф «хто кого їсть» з поточного поля) — 🥈.
- Піраміда енергії як HUD екосистеми — 📎.
- Тепловий вид як другий рендер того самого поля — 📎.
- Челенджі-умови над пісочницею («зроби скло», «тримай акваріум») — 📎.

## Мапа на каталог
- Є: `cell-click` (сипати курсором) · `gravity-fall` · `cell-transform` (рештки → ґрунт) · `spawner-entity` (хмари, джерела, отвори) · `hunger-clock` (голод тварин) · `editor-palette` + `editor-erase` · `save-multi-slot` + `save-progress` · `field-scaling` (3 розміри, скрол, зум) · `game-loop`.
- **Нема** → пропозиції карток:
  - Повтори з корпусу: `+falling-sand-cell`, `+predator-prey`, `+day-night-cycle`, `+season-cycle`, `+weather-modifiers`, `+view-modes`.
  - `+decomposer-cycle` «Рештки перетворюються на ґрунт редуцентами» · entities/interact · 📎.
  - `+food-web-view` «Жива діаграма, хто кого їсть» · interface/hud · 🥈.
  - `+energy-pyramid` «Піраміда енергії рівнів живлення» · interface/hud · 📎.
  - `+natural-disasters` «Землетрус, метеор, торнадо над полем» · game-logic/events · 🥉.
  - `+challenge-list` «Челенджі-умови в пісочниці» · game-logic/goals · 🌱 · `+discoveries-log` «Журнал відкритих явищ» · game-logic/history · 🌱.

## Пропозиції до словників
- `+trigger:hunger(a)` — енергія/їжа тварини скінчилась (повтор корпусу).
- `+effect:eat(a, b)` · `+effect:breed(a)` · `+effect:decay(a → soil)` — повтори корпусу; у правилах поки `custom`/`transform`.
- `+role:material` — матеріали банки (повтор; у таблиці — `object`).
- `+window:food-web` — діаграма харчової мережі; `+window:challenges` — челенджі й відкриття.
- `+feature:photo-mode` — фото й відео поля (повтор).
- `+card:…` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Grain](https://frizzle3.itch.io/grain) — Zachary Fritz; 60+ матеріалів, машини (батарея, лампа, вентилятор, конвеєр, насос), makers (хмари, джерела, отвори), 16 видів тварин, харчова мережа й піраміда енергії, редуценти, погода, сезони, катастрофи, 17 челенджів, тепловий вид, 3 слоти.
- [Grain Free Demo](https://frizzle3.itch.io/grain-demo) — 16 матеріалів поіменно, банки й челенджі демо, таблиця відмінностей.
- [Девлог «Grain is out!»](https://frizzle3.itch.io/grain/devlog/1719410/grain-is-out) — реліз 20.10.2026.

## Непевне
- (?) Хто кого їсть: сторінка не каже; природні пари (лисиця → кролик, сова → ?, жаба → жук) — лише здогад, у правила не писав.
- (?) Решта 6 видів тварин не названі; які саме з них редуценти (черви — найімовірніше).
- (?) Правила машин (батарея живить лампу? вентилятор — вітер?) і makers — лише назви.
- (?) Реакції матеріалів (лава + вода, тепло + пісок → скло для «Glassblower») — не описані.
- (?) Катастрофи — подія погоди чи кнопка гравця.
- (?) Як працює енергія тварини (лічильник? шанс?) і умова розмноження.
