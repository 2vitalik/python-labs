---
title: A Directionless Cycle
slug: a-directionless-cycle
aka: [ADC]
family: push-slide
also: [thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3417520/A_Directionless_Cycle/", best: true, note: "опис, фічі (70+ рівнів, undo, підказка-рівень, Extra, редактор), демо першої зони"}
  - {kind: other, url: "https://steamcommunity.com/app/3417520/reviews/?browsefilter=toprated&l=english", note: "відгуки: стрілки на фігурах, 4 типи руху, штовхання, стрілки-підбирачки й антистрілки, зелені кола-цілі"}
  - {kind: itch, url: "https://ugdev.itch.io/a-directionless-cycle", note: "сторінка розробника (Half Sun / ugdev), devlog демо й релізу"}
  - {kind: official, url: "https://ugdev.xyz/adc", note: "промо-сторінка: «control multiple tiles with different directions at the same time»"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3417520&count=15&maxlength=3000", note: "патчноути: undo до 1000 ходів, move trials, carvings, inverse indicator, cycle ability"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=A+Directionless+Cycle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-by-input, push-object, inertia-slide, impassable-cells, item-pickup, all-on-targets, goal-counter, move-counter, move-limit, undo-unlimited, restart-level, level-select, in-game-editor, level-exchange, keyboard-controls, +broadcast-move, +arrow-markings, +arrow-pickup, +mirror-move, +hint-level, +move-trial, +secret-codes, +undo-hold-repeat]
proposes: ["+axis:control=broadcast", "+effect:mirror_move", "+feature:hint-level", "+feature:move-trial", "+feature:undo-hold-repeat", "+feature:confirm-restart", "+window:dialogue-window", "+card:broadcast-move", "+card:arrow-markings", "+card:hint-level"]
author: opus
date: 2026-11-09
---

# A Directionless Cycle — один ввід рухає одразу всі фігури зі стрілкою цього напрямку; накрий фігурами всі зелені кола

## Суть
Sokoban-подібна головоломка без аватара: на полі кілька фігур, і **кожна має мітки-стрілки**. Натискаєш напрямок — **одночасно рушать усі фігури, на яких є стрілка цього напрямку**, кожна за правилом свого типу (простий крок, «два на два», ковзання, дзеркальний рух). Мета рівня — накрити фігурами всі зелені кола. Поверх пазлів — мета-шар «гра, що повільно розпадається»: секретні рівні, коди, «заборонена магія», здібність «cycle» і кілька кінцівок.

## Поле і час
- Квадратна сітка в рамці з білих блоків-стін; підлога темна; частина рамки буває «зламана» (чорні діри — естетика розпаду).
- Хід = один ввід напрямку; усі відповідні фігури рушають в один такт. Без вводу нічого не рухається.
- Рівні згруповано в зони/світи (W1…W3+, напр. «Interception» = W3) з хабом і виходами; у кожній кімнаті вкладено менший рівень-підказку (W1-5.1, W1-5.2).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фігура «простий рух» | piece | набір стрілок | крок на 1 у напрямку вводу, якщо є така стрілка |
| Фігура «два на два» | piece | набір стрілок | рух за правилом «two by two» (?) |
| Фігура «ковзання» | piece | набір стрілок | ковзає до упору |
| Фігура «дзеркальна» | piece | набір стрілок | рух дзеркально до вводу (?) |
| Синя / червона фігура | piece | — | можуть штовхати інші фігури |
| Зелене коло | zone | — | ціль; рівень пройдено, коли всі кола накриті |
| Стрілка-підбирачка | pickup | напрямок | фігура, що стала на неї, отримує новий напрямок руху |
| Антистрілка | pickup | напрямок | забирає здатність рухатись (у цьому напрямку (?)) |
| Стіна | static | — | непрохідна |
| Різьблення (carving) | switch | — | реагує на ввід; поруч може лежати «мертвий ящик» (?) |
| Червоні фігури / червоні кола | — | — | є на скріншотах; червоний контур — «інверсний індикатор» (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `has(piece, arrow(dir))` → ТО фігура рухається за своїм типом; усі такі фігури — в той самий хід.
- КОЛИ `input(dir)` → ЯКЩО `has(piece, arrow(dir))` і `custom: «тип — простий рух»` і `free(next_cell)` → ТО `move(piece, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `has(piece, arrow(dir))` і `custom: «тип — ковзання»` → ТО `slide(piece, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `has(piece, arrow(dir))` і `custom: «тип — дзеркальний»` → ТО `custom: «рух у дзеркальному напрямку»` (?).
- КОЛИ `input(dir)` → ЯКЩО `has(piece, arrow(dir))` і `custom: «тип — two by two»` → ТО `custom: «рух за правилом two by two»` (?).
- КОЛИ `blocked(piece)` → ТО `block` (фігура лишається, інші рушають).
- КОЛИ `contact(blue_or_red_piece, piece)` → ЯКЩО `free(cell_behind)` → ТО `push`.
- КОЛИ `enter(piece, arrow_pickup)` → ТО `give(piece, arrow(dir))`, `disappear_b`.
- КОЛИ `enter(piece, anti_arrow)` → ТО `take(piece, arrow(dir))` (?).
- КОЛИ `counter(covered_circles, =, total)` → ТО `win`.
- КОЛИ `custom: «введено код ендгейму»` → ТО `unlock(move_trials)`, `window(custom-window)`; ЯКЩО `mode(move_trial)` і `counter(moves, >, limit)` → ТО `custom: «випробування не зараховано»`.
- КОЛИ `input(undo)` → ТО `undo(1)` (до 1000 ходів, утримання повторює; рестарт не відкочується) · КОЛИ `input(restart)` → ТО `restart` (з підтвердженням за налаштуванням).
- КОЛИ `custom: «здобуто здібність cycle»` → ТО `custom: «нова дія cycle»` (суть дії не перевірено (?)).
- Перемога: усі зелені кола накриті фігурами. · Поразка: нема; глухий кут — undo/рестарт. · Рахунок: зірки за рівні (жовті), червоні й фіолетові зірки за Extra/випробування (?).

## Керування і ввід
- 4 напрямки (клавіатура або геймпад) — єдиний ігровий ввід; він «транслюється» всім фігурам одразу.
- Undo (утримання — серія), рестарт; перепризначення клавіш планувалось, у грі на старті не було.
- Курсор на вибір рівня: вгору від W1-5 веде до підрівня W1-5.1.

## Вікна, меню, HUD
- `main-menu` — титул (новий UI з демо-оновлення), налаштування, редактор, кастомні рівні.
- `level-select` — сторінка світу: назва («Interception»), плитки W-N з рамкою (зелена — пройдено, червона — (?)), лічильники жовтих і червоних зірок, «Back to Menu», стрілки між світами.
- `map-window` — хаб зони з виходами, зокрема «зовнішніми» (показані завжди з v1.05).
- `game-screen` — поле; HUD: `goal-counter` (накрито кіл «1/2»), `move-counter` або лічильник у ромбі (?), `timer-elapsed` з пісковим годинником (?).
- `dialogue-window` — «балакучі місця»: текстові вставки сюжету й натяки.
- `editor-window` — повний редактор + сцена кастомних рівнів.
- `settings-window` — підтвердження рестарту, звук.

## Фічі поза полем
- `undo` (до 1000 ходів, `+undo-hold-repeat`), `restart-level` + `+confirm-restart`.
- `+hint-level` — у кожному рівні вкладено менший рівень, що підводить до ідеї.
- Extra-рівні для хардкору, `+move-trial` (необовʼязковий ліміт ходів, вмикається кодом ендгейму).
- `level-editor`, обмін кастомними рівнями через Discord (Workshop нема).
- `collectibles`, секретні «зовнішні» рівні, коди, кілька кінцівок; `cloud-save`, `achievements`.

## Варіації й родичі
- Осі варіацій:
  - **кого рухає ввід**: одного аватара (`sokoban`) / усі плитки (`2048`) / **лише фігури з міткою цього напрямку** (тут) / усіх роботів за програмою (`program-robots`);
  - **тип руху фігури**: крок / ковзання (`ice-sliding-puzzles`) / дзеркально / складніші патерни;
  - **мітки змінні**: стрілки можна підібрати й втратити (тут) / фіксовані (`ricochet-robots`).
- Родичі: `sokoban`, `ice-sliding-puzzles`, `ricochet-robots`, Baba Is You (правила як обʼєкти — межа з `thinky`), Atomix-подібні (`atomix`).

## Цікавинки для курсу
- Одночасний рух кількох фігур одним вводом: порядок обробки й конфлікти (дві фігури в одну клітину, ланцюг поштовхів) — 🥈.
- Мітки-стрілки як множина напрямків на фігурі + підбирачки/антистрілки — 📎.
- Чотири типи руху як стратегії (крок / ковзання / дзеркало / «два на два») — 🥉, гарний урок поліморфізму.
- Ціль «усі кола накриті» з лічильником у HUD — 🌱.
- Undo-стек з лімітом 1000 і утриманням-повтором — 🌱.
- Рівень-підказка, вкладений у рівень (менша версія з тією самою ідеєю) — 📎.

## Мапа на каталог
- Є: `move-by-input` ↔ ввід напрямку; `push-object` ↔ сині й червоні фігури штовхають; `inertia-slide` ↔ тип «ковзання»; `impassable-cells` ↔ стіни; `item-pickup` ↔ стрілки-підбирачки; `all-on-targets` ↔ усі кола накриті; `goal-counter` ↔ «1/2»; `move-counter` + `move-limit` ↔ move trials; `undo-unlimited` + `restart-level`; `level-select`; `in-game-editor` + `level-exchange` ↔ редактор і кастомні рівні; `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+broadcast-move` «Ввід рухає всі фігури, що на нього реагують» · entities/move · 🥉 — між `move-by-input` і `swipe-all-shift`.
  - `+arrow-markings` «Мітки-стрілки на фігурі задають дозволені напрямки» · entities/legality · 📎 · слот {pickup: bool}.
  - `+arrow-pickup` «Підібрати/втратити напрямок руху» · entities/interact · 🌱.
  - `+mirror-move` «Фігура рухається дзеркально до вводу» · entities/move · 🌱 (?).
  - `+hint-level`, `+move-trial`, `+secret-codes` «Коди відкривають режими й секрети» · levels/progression · 🌱.

## Пропозиції до словників
- `+axis:control=broadcast` — один ввід розсилається всім фігурам, кожна реагує за своїми мітками (ширше за `swipe-all`).
- `+effect:mirror_move` — рух у дзеркальному до вводу напрямку для однієї сутності (`mirror_input` — про весь ввід гравця).
- `+feature:hint-level` — підказка як окремий спрощений рівень (тут і E9uations).
- `+feature:move-trial` — необовʼязкове випробування з лімітом ходів поверх пройденого рівня.
- `+feature:undo-hold-repeat` — утримання undo повторює (тут, Headlong Hunt).
- `+feature:confirm-restart` — підтвердження рестарту в налаштуваннях.
- `+window:dialogue-window` — ⏳ підтверджую: «балакучі місця» з сюжетом.
- `+card:broadcast-move`, `+card:arrow-markings`, `+card:hint-level` — див. вище.

## Джерела
- ⭐ [Steam: A Directionless Cycle](https://store.steampowered.com/app/3417520/A_Directionless_Cycle/) — «everything moves at the same time», 70+ рівнів, undo, підказки в кожному рівні, Extra, редактор, демо першої зони.
- [Steam: відгуки](https://steamcommunity.com/app/3417520/reviews/?browsefilter=toprated&l=english) — «moving all the pieces that have an arrow matching the direction you pushed», «simple movement, two by two, sliding, and mirrored», «Blue and red pieces can also push», стрілки-підбирачки, антистрілки, «green circles… win when all… covered», рівень-підказка в кожній кімнаті, undo без рестарту, move challenge.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=3417520&count=15&maxlength=3000) — undo cap 1k, move trials і код ендгейму, carvings і dead box, inverse indicator, cycle ability, outerbound exits, фіолетова зірка W3-10.
- [itch: ugdev](https://ugdev.itch.io/a-directionless-cycle) і [ugdev.xyz/adc](https://ugdev.xyz/adc) — автор Half Sun (Unai Giz), Unity, демо жовтень 2024, утримання undo, підтвердження рестарту, редактор.
- Скріншоти Steam (переглянуто): HUD «пісковий годинник / коло 1/2 / ромб 23», сторінка світу «Interception» зі зірками, фігури зі стрілками, діалог «if something feels impossible… it probably is!».

## Непевне
- (?) Яка фігура якого кольору/форми має який тип руху; що саме означають «two by two» і «mirrored».
- (?) Що показують годинник і лічильник у ромбі (час і ходи? ліміт випробування?).
- (?) Роль червоних фігур-«желе», червоних кіл і «різьблень»; що робить здібність «cycle»; що таке «заборонена магія».
- (?) Як розвʼязуються конфлікти, коли кілька фігур претендують на одну клітину в той самий хід.
- (?) Чи є окремий `end-screen` після рівня.
