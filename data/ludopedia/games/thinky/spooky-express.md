---
title: Spooky Express
slug: spooky-express
aka: []
family: thinky
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC, Mac, iOS, Android]
links:
  - {kind: official, url: "https://spooky.express/", best: true, note: "сайт: лінки на всі магазини і прескіт"}
  - {kind: other, url: "https://spooky.express/press/", note: "прескіт: опис механіки (вампіри → труни, зомбі → могили, люди), дата 21.10.2025, автори"}
  - {kind: steam, url: "https://store.steampowered.com/app/3352310/Spooky_Express/", note: "опис: одне місце у вагоні, колія без перетинів, 200+ рівнів"}
  - {kind: itch, url: "https://draknek.itch.io/spooky-express", note: "itch.io, Windows і macOS"}
  - {kind: official, url: "https://www.draknek.org/", note: "Draknek & Friends — видавець"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spooky+Express+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [path-drawing, path-cut, cell-click, reach-exit, collect-all, completion-detection, impassable-cells, sequential-levels, level-select, save-progress, game-screen, main-menu, achievements-window, +adjacent-transfer, +carriage-capacity, +run-simulation, +typed-destination, +escort-before-threat]
proposes: ["+effect:board", "+effect:alight", "+card:typed-destination", "+card:escort-before-threat"]
author: opus
date: 2026-11-09
---

# Spooky Express — Cosmic Express з нечистю: вампірів до трун, зомбі до могил, людей — геть, поки не зʼїли

## Суть
Наступник [Cosmic Express](../connect-rotate/cosmic-express.md) від тієї ж команди (Alan Hazelden — креативний директор). Гравець прокладає колію для потяга, що возить «нежить» Трансильванії: кожен вид монстра має свій дім (вампір — труна, зомбі — могила). У вагоні одне місце, колія не може перетинати себе, потяг не має проминути жодної зупинки. Нове відносно Cosmic Express — **люди**: їх треба вивезти, поки монстри їх не «перекусили».

## Поле і час
- Квадратна сітка-діорама (Steam-теги: Isometric, 3D); локації-світи — Pumpkin Patch, Morbid Manor, Impish Inferno тощо.
- Час програмний, як у Cosmic Express: спершу план колії, потім поїздка (?).
- Понад 200 рівнів (Steam).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Колія | mark | шлях без самоперетину | малює гравець; потяг іде лише нею |
| Потяг / вагон | container | 1 місце | везе одного пасажира за раз |
| Вампір | object | вид = vampire | має бути доставлений до труни |
| Зомбі | object | вид = zombie | має бути доставлений до могили |
| Труна | sink | для вампіра | дім вампіра |
| Могила | sink | для зомбі | дім зомбі |
| Людина | object | — | «незвані гості»: їх треба вивезти, поки їх не зʼїли монстри |
| Вхід / вихід | source / sink | край поля (?) | початок і кінець колії, як у Cosmic Express (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag)` → ЯКЩО `free(cell)` → ТО `custom: «колія подовжується на клітину»`; ЯКЩО клітина вже з колією → `block` (колія не перетинає себе).
- КОЛИ `adjacent(car, monster)` → ЯКЩО `not has(car, passenger)` → ТО `custom: «монстр сідає у вагон»` (?).
- КОЛИ `adjacent(car, home)` → ЯКЩО `has(car, monster)` and `same(monster, home, kind)` → ТО `custom: «монстр виходить у свій дім»` (?).
- КОЛИ `adjacent(car, human)` → ЯКЩО `not has(car, passenger)` → ТО `custom: «людина сідає й вивозиться»` (?).
- КОЛИ `custom: «монстр дістався людини»` → ТО `lose` / рівень не зараховано (?).
- Перемога: кожен монстр у домі свого виду, люди вивезені, жодна зупинка не пропущена.
- Поразки й рахунку в класичному сенсі нема (?) — «розвʼязано / ні», як у Cosmic Express.

## Керування і ввід
- Мишею / дотиком — малювання колії, як у Cosmic Express (?). Одиночна гра.

## Вікна, меню, HUD
- `game-screen`: діорама локації з колією й пасажирами.
- `level-select` по локаціях (?); комікси між розділами (David Hellman, Zac Gorman, Zach Cunningham).
- `achievements-window` (Steam Achievements).

## Фічі поза полем
- `achievements`, `cloud-save` (Steam Cloud), Remote Play Together.
- Саундтрек Priscilla Snow — окремим DLC; локалізація (Warlocs).
- `undo` / `restart-level` — не згадано в описах (?).

## Варіації й родичі
- Лінія Draknek-потягів: Train Braining (прототип) → [Cosmic Express](../connect-rotate/cosmic-express.md) (2017) → Sokobond Express (2024) → Spooky Express (2025).
- Родичі від Draknek: [A Monster's Expedition](a-monsters-expedition.md), [A Good Snowman Is Hard to Build](a-good-snowman-is-hard-to-build.md).
- **Осі варіацій** (продовжують Cosmic Express): пасажир → дім за кольором / за видом · вантаж лише «довезти» / «вивезти до загрози» · місткість 1 / N.

## Цікавинки для курсу
- Колія drag-ом без самоперетину з відкатом — 📎 (як у Cosmic Express).
- Посадка/висадка за сусідством, дім за видом пасажира — 📎.
- Люди під загрозою: черговість «спершу врятувати, потім довезти» в одній колії — 🥉 (стан загрози на кожному кроці симуляції).
- Розвʼязувач: DFS по колії з симуляцією — 🥇.

## Мапа на каталог
- Є: `path-drawing`, `path-cut` ↔ колія · `cell-click` · `reach-exit` · `collect-all` ↔ усі монстри вдома · `completion-detection` · `impassable-cells` · `sequential-levels`, `level-select`, `save-progress` · `game-screen`, `main-menu`, `achievements-window`.
- **Нема** → пропозиції карток:
  - `+adjacent-transfer`, `+carriage-capacity`, `+run-simulation` — див. cosmic-express.md.
  - `+typed-destination` «Пасажир має дім свого виду» · entities/interact · 🌱 · слоти {match: color|kind}.
  - `+escort-before-threat` «Вивезти вразливих, поки до них не дістались загрози» · game-logic/win · 🥉.

## Пропозиції до словників
- `+effect:board` / `+effect:alight` — пасажир у носій / з носія (підтверджую з cosmic-express.md; у `vocab/` ще нема).
- `+card:typed-destination`, `+card:escort-before-threat` — див. вище.

## Джерела
- ⭐ [spooky.express](https://spooky.express/) — сайт, лінки на Steam, itch.io, App Store, Google Play.
- [Прескіт](https://spooky.express/press/) — «take the vampires to their coffins and the zombies to their graves», «escort the interloping humans away before they're snacked upon», «room for one at a time», «track can't cross itself», «don't let the train miss its stops»; реліз 21.10.2025; повні титри.
- [Steam](https://store.steampowered.com/app/3352310/Spooky_Express/) — 200+ рівнів, локації, комікси, Achievements, Cloud.
- [itch.io](https://draknek.itch.io/spooky-express) — Windows, macOS.
- YouTube: пошук «Spooky Express gameplay».

## Непевне
- Веб-пошук сесії вичерпано; оглядів і вікі не знайдено. Механіка — лише з маркетингового опису; решта — за аналогією з Cosmic Express.
- (?) Чи посадка й висадка, як у Cosmic Express, відбувається за сусідством.
- (?) Як саме монстри «зʼїдають» людину (сусідство з монстром у вагоні? з вільним монстром на полі?) і куди вивозять людей (вихід? окрема зупинка?).
- (?) Чи є інші види монстрів (привиди тощо) у пізніх світах.
- (?) Керування, undo, рестарт — не описані в джерелах.
