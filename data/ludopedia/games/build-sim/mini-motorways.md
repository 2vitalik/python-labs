---
title: Mini Motorways
slug: mini-motorways
aka: [«Міні-автостради»]
family: build-sim
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: both
  goal: survive
year: 2019
platforms: [iOS (Apple Arcade), macOS, tvOS, PC (Windows), Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mini_Motorways", best: true, note: "будинки й будівлі за кольором, шпильки (7 / 10), таймер переповнення, щотижневі апгрейди, мости/тунелі/світлофори/кільця/автостради"}
  - {kind: steam, url: "https://store.steampowered.com/app/1127500", note: "режими Endless / Expert / Creative, Daily і Weekly челенджі, палітри (дальтонізм, ніч), експорт GIF"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mini+motorways+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [path-drawing, path-cut, cell-click, spawn-random-cell, progress-acceleration, chase-bfs, impassable-cells, multi-cell-size, game-pause, score-records, leaderboard, daily-puzzle, mode-select, end-screen, level-select, level-unlock, theme-select, game-settings, save-progress, +drag-build-line, +track-budget, +span-crossing-tool, +choose-upgrade, +overflow-timer, +color-matched-delivery, +traffic-light-cycle, +gif-export]
proposes: ["+trigger:week_end", "+effect:return_to_inventory", "+role:demand-building", "+ui:overflow-ring", "+ui:week-clock", "+ui:tool-inventory", "+feature:mode-expert", "+feature:mode-creative", "+card:overflow-timer", "+card:color-matched-delivery", "+card:choose-upgrade"]
author: opus
date: 2026-11-09
---

# Mini Motorways — малюй дороги по сітці, щоб машини з будинків встигали до будівель свого кольору

## Суть
Продовження Mini Metro від Dinosaur Polo Club: замість ліній метро — дороги по квадратній сітці. Будинки кольору X породжують машини, будівлі кольору X накопичують «шпильки» попиту; машина їде до будівлі свого кольору, забирає шпильку й повертається. Місто росте випадково, ліміт дорожніх плиток і щотижневий вибір із двох апгрейдів змушують перебудовувати мережу; переповнена будівля запускає таймер — коли він заповнився, гра скінчена. Рахунок — кількість зібраних шпильок.

## Поле і час
- Квадратна сітка карти міста (25 карт реальних міст станом на 09.2026) з водою (річки, затоки) і горами як перешкодами; карта процедурно варіюється від гри до гри.
- Будівлі займають кілька клітин; будинки — одну (?); дорога — 1 клітина, зʼєднується з сусідніми.
- Real-time з паузою; «тиждень» гри ≈ 2,5 хв на нормальній швидкості — після нього вибір апгрейда.
- Камера показує все місто; місто поступово «відкриває» більшу площу (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Будинок | spawner | колір, машини | випускає машини свого кольору до будівлі з попитом; машина повертається додому |
| Будівля (квадратна) | zone | колір, ємність 7 шпильок | накопичує шпильки попиту; переповнення → таймер |
| Будівля (кругла) | zone | колір, ємність 10 шпильок | те саме, більша ємність |
| Шпилька (pin) | resource | — | одиниця попиту на будівлі; машина забирає одну |
| Машина | neutral | колір | їде найкоротшим шляхом мережею; пріоритет — будівлі з активним таймером |
| Таймер переповнення | mark | заповнення | росте, поки шпильок більше за ємність; прибуття машин трохи гальмує; спадає, коли шпильок у межах |
| Дорога | terrain | 1 клітина | гравець малює; запас плиток обмежений |
| Міст / тунель | terrain | 1 штука = 1 переправа будь-якої довжини | через воду / крізь гору |
| Світлофор | switch | на перехресті | чергує потоки; можна перенести без видалення |
| Кільце (roundabout) | terrain | 3×3, одностороннє | не витрачає дорожніх плиток |
| Автострада (motorway) | terrain | 2 кінці | пряме зʼєднання двох точок над усім, крім гір; кінці можна перенести |
| Вода | static | — | непрохідна без мосту |
| Гора | static | — | непрохідна без тунелю; автострада теж не проходить |
| Поїзд і станція (NYC, London, Mumbai) | object | — | кросовер з Mini Metro (оновлення 07.2023) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, cells)` → ЯКЩО `has(player, road_tiles)` and `free(cell)` → ТО `place(road)`, `take(player, road_tile)`.
- КОЛИ `input(erase, road)` → ТО `disappear_a`, `give(player, road_tile)` (`custom: «плитка повертається, коли трафік на ній завершився»`).
- КОЛИ `input(drag, water | mountain)` → ЯКЩО `has(player, bridge | tunnel)` → ТО `place(bridge | tunnel)`; інакше `block`.
- КОЛИ `rng(spawn)` / `schedule(growth)` → ТО `spawn_at(house | building, random_free_area)` — нові кольори зʼявляються з часом.
- КОЛИ `timer(demand)` → ТО `spawn_at(pin, building)`.
- КОЛИ `custom: «на будівлі є шпилька без призначеної машини»` → ЯКЩО `path_exists(house_same_color, building)` → ТО `spawn(car)` з будинку того ж кольору; машина йде найкоротшим шляхом.
- КОЛИ `contact(car, building)` → ЯКЩО `same(car, building, color)` → ТО `take(building, pin)`, `score(+1)`, машина повертається додому.
- КОЛИ `counter(pins, >, capacity)` → ТО `timer(start)` на будівлі; КОЛИ `contact(car, building)` під час таймера → ТО `custom: «таймер трохи сповільнюється»`; КОЛИ шпильок ≤ ємності → ТО таймер спадає.
- Пріоритет: КОЛИ машина обирає ціль → ЯКЩО `state(building, timer_active)` → ТО туди першою.
- КОЛИ `counter(timer, ==, full)` → ТО `lose` (`game_over`, `window(end-screen)`).
- КОЛИ `schedule(week_end)` → ТО `choose(2 options)`: обидві дають дорожні плитки, одна — ще й спецінструмент (міст, тунель, світлофор, кільце, автострада).
- КОЛИ `contact(car, traffic_light)` → ЯКЩО `custom: «зараз зелене для іншого напрямку»` → ТО `block` (чекає).
- КОЛИ `enter(car, roundabout)` → ТО `custom: «рух по колу в один бік, вихід на потрібній гілці»`.
- КОЛИ `enter(car, motorway_end)` → ТО `custom: «їде напряму до другого кінця над містом»`.
- КОЛИ `input(delete, tool)` → ТО `custom: «інструмент повертається в запас після того, як трафік завершився або перебудувався маршрут»`.
- Expert: КОЛИ `input(erase, road)` → ЯКЩО `mode(expert)` → ТО `block` (дороги постійні), апгрейди обмежені.
- Endless: КОЛИ `lose` → ЯКЩО `mode(endless)` → ТО можна будувати далі.
- Рахунок: шпильки (не поїздки); рекорд — на карту.

## Керування і ввід
- Мишею / пальцем: drag від клітини — малювати дорогу (дороги автоматично зʼєднуються з сусідніми); стирання — ПКМ-drag на ПК (?).
- Перетягнути інструмент (міст, кільце, світлофор, автостраду) з запасу на поле; щит автостради можна відтягнути, щоб побачити, що під ним; кінці автостради й світлофори переносяться.
- Пауза й прискорення часу (?); вибір апгрейда кліком по одній з двох карт.

## Вікна, меню, HUD
- `main-menu` / `level-select`: список карт-міст (нові відкриваються грою), рекорд на кожній.
- `mode-select`: Normal, Endless, Expert, Creative; Daily і Weekly Challenge (`daily-window`, `leaderboard`).
- `game-screen`: карта, `score` (шпильки), `week-clock` (день/тиждень), `tool-inventory` (плитки доріг і спецінструменти з кількістю), `overflow-ring` над будівлею з таймером, кнопки паузи/швидкості (?).
- `upgrade-window`: дві картки апгрейда наприкінці тижня — гра на паузі, доки не обереш.
- `end-screen`: рахунок, рекорд, продовжити в Endless, експорт GIF міста.
- `settings-window`: палітри кольорів на кожній карті (зокрема `colorblind-palette`, нічна), мова, гучність.
- `achievements-window` (Steam Achievements).
- Переходи: main-menu → карта → game-screen · кінець тижня → upgrade-window → game-screen · таймер повний → end-screen → (Endless) game-screen або main-menu.

## Фічі поза полем
- Режими: Endless (будувати після Game Over), Expert (постійні дороги, обмежені апгрейди), Creative (необмежені апгрейди й редагування — `mode-sandbox`), Daily і Weekly Challenge (`mode-daily`, `leaderboard-online`).
- `level-unlock` карт і `achievements`; `cloud-save` (Steam Cloud); `stats` рекордів по картах.
- `colorblind-palette`, нічна палітра (`theme-select`); `share-result` — експорт GIF міста; локалізація (англ. + 13 мов).

## Варіації й родичі
- **Осі варіацій:** мережа — лінії-маршрути (Mini Metro) / вільний граф доріг по сітці (Mini Motorways) · агенти — пасажири на поїздах / машини, що самі шукають шлях · ресурс будівництва — лінії й вагони / плитки доріг + інструменти · спеціальні переправи — лімітовані (міст = 1 переправа).
- Mini Metro (2015) — попередник; крос-овер з поїздами на трьох картах.
- Родичі в корпусі: [openttd-rails](openttd-rails.md) (транспортні мережі на сітці), [townscaper](townscaper.md) (місто на сітці без цілей), [dorfromantik](dorfromantik.md) (обмежений запас плиток і вибір), [trainyard](../connect-rotate/trainyard.md) (кольорові агенти до приймачів).

## Цікавинки для курсу
- Будинки/будівлі за кольором + машини з BFS до найближчої потрібної будівлі — 📎 (пошук шляху на графі доріг, що змінюється).
- Таймер переповнення: ріст понад ємність, сповільнення від прибуття, спадання — 🌱 (окремий стан будівлі + `danger`-кільце).
- Малювання доріг drag-ом з автозʼєднанням сусідів і бюджетом плиток — 📎.
- Щотижневий вибір 1 з 2 апгрейдів з гарантованим спецінструментом — 🌱.
- Світлофори й кільце як вузли з чергами — 🥉 (симуляція заторів, черга на перехресті).
- Ріст міста: випадковий спавн будинків/будівель нових кольорів зі зростанням темпу — 📎.
- Автострада як ребро графа «над» сіткою (ігнорує клітини між кінцями) — 🥉 (два шари топології).

## Мапа на каталог
- Є: `path-drawing` + `path-cut` (малювати/стирати дороги) · `cell-click` · `spawn-random-cell` (нові будинки й будівлі) · `progress-acceleration` (місто росте) · `chase-bfs` (машини шукають шлях) · `impassable-cells` (вода, гори) · `multi-cell-size` (будівлі, кільце 3×3) · `game-pause` · `score-records` + `leaderboard` · `daily-puzzle` (Daily Challenge) · `mode-select` · `end-screen` · `level-select` + `level-unlock` (карти) · `theme-select` + `game-settings` (палітри) · `save-progress`.
- Перевикористано: `+drag-build-line`, `+track-budget` (ліміт плиток), `+gif-export`.
- **Нема** → пропозиції карток:
  - `+overflow-timer` «Переповнення запускає таймер програшу» · game-logic/lose · 🌱 · слоти {capacity, slowdown}.
  - `+color-matched-delivery` «Агенти кольору X доставляють до приймача кольору X» · entities/interact · 📎.
  - `+choose-upgrade` «Періодичний вибір 1 з 2 апгрейдів» · game-logic/economy · 🌱 · слот {period}.
  - `+traffic-light-cycle` «Світлофор чергує потоки на перехресті» · entities/move · 🥉.
  - `+span-crossing-tool` «Одна штука перекриває перешкоду будь-якої довжини (міст, тунель)» · entities/legality · 🌱.

## Пропозиції до словників
- `+trigger:week_end` — кінець ігрового періоду (тиждень), що відкриває вибір; узагальнення `schedule`.
- `+effect:return_to_inventory` — знята будова повертається в запас гравця (дороги, мости, світлофори).
- `+role:demand-building` — будівля, що накопичує попит і приймає агентів (відрізняється від `sink`: має ємність і таймер).
- `+ui:overflow-ring` — кругова шкала таймера над будівлею; `+ui:week-clock` — годинник тижня до вибору; `+ui:tool-inventory` — запас плиток і спецінструментів з кількістю.
- `+feature:mode-expert` — постійні рішення (не можна стерти) + менше апгрейдів; `+feature:mode-creative` — необмежені ресурси й редагування міста.
- `+card:…` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Mini Motorways](https://en.wikipedia.org/wiki/Mini_Motorways) — механіка шпильок (7 / 10), таймер переповнення, пріоритет машин, рахунок шпильками, тиждень ≈ 2,5 хв, 5 спецінструментів, 25 карт, поїзди з 07.2023, дати релізу.
- [Steam](https://store.steampowered.com/app/1127500) — режими Endless/Expert/Creative, Daily/Weekly челенджі, процедурні міста, палітри, GIF, досягнення, Steam Cloud, лідерборди.
- YouTube: пошук «mini motorways gameplay».

## Непевне
- (?) Розмір будинку (1 клітина) і будівель, «розширення» карти з часом — з памʼяті.
- (?) Стирання ПКМ-drag на ПК, кнопки паузи/прискорення — з памʼяті.
- (?) Повернення дорожніх плиток при стиранні — Wikipedia пише про інструменти; для доріг — з памʼяті.
- (?) Як саме будинок «вирішує» випустити машину (одна машина на шпильку, ліміт машин на будинок) — не перевірено.
- (?) Рік: Apple Arcade 19.09.2019, Steam 20.07.2021 — у шапці 2019 за першим релізом (у черзі — 2021).
