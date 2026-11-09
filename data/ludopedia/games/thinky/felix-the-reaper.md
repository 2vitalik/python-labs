---
title: Felix the Reaper
slug: felix-the-reaper
aka: []
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: iso
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [PC, macOS, PS4, Xbox One, Switch, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Felix_the_Reaper", best: true, note: "геймплей: сітка плиток, ходити лише в тіні, перемикачі й поворот сонця, перенесення обʼєктів, 5 розділів до 6 рівнів, необовʼязкові цілі"}
  - {kind: steam, url: "https://store.steampowered.com/app/919410/Felix_The_Reaper/", note: "Kong Orange / Daedalic, 17.10.2019; time trials і hardcore-рівні"}
  - {kind: other, url: "https://hardcoregamer.com/reviews/review-felix-the-reaper/359631/", note: "рецензія: Sun Master — дві позиції сонця, ящики й гілля, телепорти й перемикачі, черепи за мінімум поворотів/ходів, hardcore без підказок"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Felix+the+Reaper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-4dir, cell-click, impassable-cells, floor-types, item-pickup, teleport-pair, button-toggle, height-levels, reach-exit, move-counter, path-preview, sequential-levels, level-unlock, level-select, save-progress, movement-animation, idle-animation, player-camera, +shadow-walk, +light-source-rotate, +carry-and-place, +shadow-casting, +optional-challenges, +chain-of-events-goal]
proposes: ["+cond:in_shadow", "+effect:recast_shadows", "+trigger:goal_event", "+card:shadow-walk", "+card:light-source-rotate", "+ui:sun-dial", "+feature:optional-challenges", "+feature:hardcore-variant"]
author: opus
date: 2026-11-09
---

# Felix the Reaper — танцюючий жнець ходить лише по тіні; поверни сонце й переставляй предмети, щоб тінь проклала шлях

## Суть
Покрокова ізометрична головоломка на сітці плиток. Felix може стояти й ходити **лише по клітинах у тіні**; тінь кидають дерева, бочки, ящики й інші обʼєкти залежно від положення сонця. Гравець перемикає сонце між двома положеннями (Sun Master) і переносить предмети, щоб тіні склались у шлях до потрібної точки. Мета рівня — підлаштувати ланцюг подій, що закінчується «приписаною» смертю цільового NPC. Ядро — поле, прохідність якого обчислюється з геометрії тіней, а не задана заздалегідь.

## Поле і час
- Плаваючі «острівці» з плиток-блоків у сітці, ізометрична 3D-камера, яку можна зсувати (?) повертати.
- Кожна клітина освітлена або в тіні; тінь клітини = функція (обʼєкти + висоти + напрямок сонця).
- Покроково: хід = крок Felix, поворот сонця або підняти/поставити обʼєкт; без часу (крім time trials).
- Структура: 5 розділів до 6 рівнів; рівень починається з 1–2 доступних ходів, далі відкриваються нові варіанти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Felix | player | позиція, несе 0/1 обʼєкт (?) | ходить лише по тіні; одним кліком — довгим шляхом; танцює |
| Сонце (Sun Master) | switch | 2 положення на рівень | перемикання перераховує всі тіні |
| Плитка-клітина | terrain | висота (?), освітлена / тінь | прохідна для Felix, лише коли в тіні |
| Дерево, будинок, нерухомий обʼєкт | static | висота | кидає тінь; непрохідний |
| Ящик, бочка, гілля | object | — | Felix піднімає й ставить в іншу клітину; нова позиція → нова тінь; можна ставити один на одного |
| Людина / тварина | neutral | — | частину можна підняти й перенести (Wikipedia) |
| Перемикач | switch | — | змінює кут/розміщення тіней або рухає машину, прапор тощо |
| Телепорт | static | парний (?) | переносить Felix |
| Цільовий NPC | neutral | — | наприкінці ланцюга подій гине (мета рівня) |
| Монета | pickup | лише в hardcore-версіях | необовʼязкова колекційка |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click cell)` → ЯКЩО `path_exists(felix, cell)` по тіньових клітинах → ТО `move(felix, cell)` (уздовж шляху), `counter(moves, +1)`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «наступна клітина в тіні»` і `free(next_cell)` → ТО `move(felix, dir)`; інакше `block`.
- КОЛИ `input(sun)` → ТО `rotate(sun, other_position)`, `custom: «перерахувати тіні всіх клітин»`, `counter(sun_turns, +1)`.
- КОЛИ `input(pick)` → ЯКЩО `adjacent(felix, object)` і `custom: «обʼєкт можна нести»` → ТО `carry(object)`.
- КОЛИ `input(place cell)` → ЯКЩО `free(cell)` або `custom: «на обʼєкт, що допускає стос»` → ТО `place(object, cell)`, `custom: «перерахувати тіні»`.
- КОЛИ `rotate(sun)` або `place(object)` → ЯКЩО `custom: «клітина Felix стала освітленою»` → ТО `block` (?) — хід, що виводить Felix на світло, ймовірно, заборонено.
- КОЛИ `enter(felix, switch)` / `input(use switch)` → ТО `custom: «змінити кут тіней або перемістити обʼєкт сцени (машина, прапор)»`.
- КОЛИ `enter(felix, teleport)` → ТО `teleport`.
- КОЛИ `custom: «ланцюг подій запущено (предмет на місці, NPC іде)»` → ТО `custom: «кат-сцена смерті цілі»` → `win`.
- КОЛИ `win` → ЯКЩО `counter(moves, <=, par)` / `counter(sun_turns, <=, par)` / `custom: «у межах часу»` → ТО `give(skull)`.
- КОЛИ `counter(skulls, >=, n)` → ТО `unlock(levels | time_trials)`.
- Перемога: ланцюг смерті цілі запущено · Поразка: формально нема (?) · Рахунок: черепи за необовʼязкові умови.

## Керування і ввід
- Миша+клавіатура або геймпад; клік по клітині — Felix іде туди довгим шляхом; клік по обʼєкту — підняти/поставити на відстані.
- Кнопка Sun Master — перемкнути сонце.
- Камера рухома; ізометрія ускладнює прицілювання (рецензія — ставлення обʼєкта інколи «не туди»).
- Підказки (вимкнені в hardcore).

## Вікна, меню, HUD
- `main-menu` — продовжити, вибір розділу/рівня, налаштування (?).
- `level-select` / `map-window` — розділи (XV ст. і 1980-ті) з рівнями; позначки черепів (?).
- `game-screen` — ізометричний острів; HUD: відображення мети (вимкнено в hardcore), лічильник ходів/поворотів (?), індикатор положення сонця (`+ui:sun-dial`).
- `hints-window` — підказки рівня (?) форма.
- `custom-window` «статті» — 5 статей історика Søren Hein Rasmussen, що відкриваються з прогресом.
- `end-screen` — рівень пройдено, отримані черепи; феєрверк і повідомлення на вехах.
- `settings-window` — мова (14), звук (?).

## Фічі поза полем
- `stars-rating`-подібні черепи: мінімум поворотів сонця / ходів / час; черепи відкривають додаткові рівні й time trials (`mode-time-attack`).
- `+feature:hardcore-variant`: hardcore-версії рівнів без підказок і показу мети, з монетами.
- `hint` у звичайних рівнях.
- `codex`-подібні статті історика; оригінальний саундтрек 10+ інді-артистів; режим «потанцювати з Felix».
- `achievements`, `cloud-save`, `localization`.

## Варіації й родичі
- Порівняння з джерел: Hitman GO (вузли й ланцюг подій), Monument Valley, Sokoban.
- Тінь як прохідність: Shadowmatic (проєкції), Contrast (ходити по тінях у 2D), Lumino City; світло-тінь як механіка стелсу (Mark of the Ninja).
- **Осі варіацій:** джерело світла — 2 положення / 4 / вільне; тінь — шлях (Felix) / сховок (стелс) / шкода (вампіри); обʼєкти — нерухомі / переносні / стос; мета — дійти / запустити подію.

## Цікавинки для курсу
- Обчислення тіней на сітці від точкового «сонця» за напрямком і висотою обʼєктів — 🥉 (кидання променя/зсув маски).
- Пошук шляху лише по тіньових клітинах (BFS із динамічною прохідністю) — 📎.
- Поворот сонця = перерахунок усієї маски прохідності; вибір ходу «поворот vs крок vs переставити» — 🥉.
- Перенесення й стос обʼєктів як зміна поля, що змінює тіні — 🥉.
- Черепи за мінімум ходів/поворотів (par) — 🌱.
- Розвʼязувач на мінімум поворотів сонця (BFS по станах: Felix + обʼєкти + сонце) — 🥇.

## Мапа на каталог
- Є: `move-4dir` + `cell-click` ↔ рух кліком; `impassable-cells` + `floor-types` ↔ світло непрохідне, тінь прохідна; `item-pickup` ↔ підняти обʼєкт; `teleport-pair` ↔ телепорти; `button-toggle` ↔ перемикачі; `height-levels` ↔ обʼєкти різної висоти, стос; `reach-exit` ≈ дійти до місця події; `move-counter` ↔ ходи/повороти; `path-preview` ↔ довгий шлях кліком; `sequential-levels` + `level-unlock` + `level-select` + `save-progress`; `movement-animation` + `idle-animation` ↔ танці; `player-camera`.
- **Нема** → пропозиції карток:
  - `+shadow-walk` «Ходити лише по тіні» · entities/legality · 🥉.
  - `+shadow-casting` «Тінь від обʼєктів за напрямком світла» · entities/state · 🥉.
  - `+light-source-rotate` «Перемикання положення сонця» · entities/state · 📎.
  - `+carry-and-place` «Підняти, перенести, поставити, стос» · entities/interact · 📎.
  - `+optional-challenges` (Toodee and Topdee) — необовʼязкові умови рівня з нагородою.
  - `+chain-of-events-goal` «Мета — запустити ланцюг подій» · game-logic/win · 🥉.

## Пропозиції до словників
- `+cond:in_shadow(cell)` — клітина в тіні за поточним світлом.
- `+effect:recast_shadows` — перерахувати маску тіней (після повороту сонця чи переставлення обʼєкта).
- `+trigger:goal_event` — спрацювала цільова подія ланцюга (NPC дійшов, предмет упав).
- `+card:shadow-walk`, `+card:light-source-rotate` — див. «Мапа на каталог».
- `+ui:sun-dial` — індикатор поточного положення сонця.
- `+feature:optional-challenges` — черепи/сонечка за необовʼязкові умови; `+feature:hardcore-variant` — та сама мапа без підказок і мети, з колекційками.

## Джерела
- ⭐ [Wikipedia: Felix the Reaper](https://en.wikipedia.org/wiki/Felix_the_Reaper) — сітка плиток на островах, тінь як шлях, перемикачі й поворот сонця, перенесення обʼєктів, людей і тварин, мета — фатальний ланцюг, необовʼязкові цілі (мінімум ходів), 5 розділів до 6 рівнів, танці, платформи й дати, рецепція.
- [Steam](https://store.steampowered.com/app/919410/Felix_The_Reaper/) — сітка, лише тінь, поворот сонця, переміщення обʼєктів, time trials і hardcore-рівні, статті історика, саундтрек.
- [Hardcore Gamer: рецензія](https://hardcoregamer.com/reviews/review-felix-the-reaper/359631/) — Sun Master з двома напрямками світла, ящики й гілля, телепорти й перемикачі, стос, черепи за мінімум поворотів/ходів, hardcore без підказок і мети з монетами, клік — довгий шлях.
- YouTube: [пошук «Felix the Reaper gameplay»](https://www.youtube.com/results?search_query=Felix+the+Reaper+gameplay).

## Непевне
- (?) Що стається, якщо хід робить клітину Felix освітленою: заборона ходу чи провал — джерела кажуть лише «має лишатися в тіні».
- (?) Чи сонце завжди має рівно 2 положення (рецензія TechRaptor з видачі натякає на це) чи кількість різна на рівнях.
- (?) Чи Felix може нести більше одного обʼєкта; чи переносить він лише в тіні.
- (?) Наявність undo/рестарту; вигляд підказок; HUD-лічильники.
- (?) Чи має камера поворот, чи лише зсув.
