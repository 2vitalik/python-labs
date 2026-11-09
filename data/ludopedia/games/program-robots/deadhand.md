---
title: Deadhand
slug: deadhand
aka: []
family: program-robots
also: [grid-platformer, thinky]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: none
  info: partial
  random: runtime
  goal: state
year: null
platforms: [PC (Windows, Steam)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5395820/Deadhand/", best: true, note: "Chris Karageorge, «coming soon»; черга команд наперед, оголошені зміни рівня, одне переривання, медалі, денний пазл"}
  - {kind: other, url: "https://store.steampowered.com/api/appdetails?appids=5395820", note: "JSON тієї ж сторінки: категорії (Keyboard/Mouse/Touch Only, Playable without Timed Input), опис"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Deadhand+puzzle+game", note: "пошук; відео не перевірено"}
stage: v1
coverage: 50
mechanics: [command-program, reach-exit, push-object, button-toggle, gravity-fall, daily-puzzle, leaderboard, replay, sequential-levels, keyboard-controls, cell-click, +plan-then-execute, +crumbling-floor, +announced-perturbations, +single-interrupt, +medal-rating, +shared-queue-runners, +solver-verified-levels, +watch-others-solutions]
proposes: ["+effect:interrupt", "+effect:announce", "+effect:wait", "+trigger:run_start", "+trigger:level_change(kind)", "+feature:daily-attempts", "+feature:watch-others-solutions", "+ui:change-forecast", "+card:announced-perturbations", "+card:single-interrupt", "+card:shared-queue-runners", "+card:solver-verified-levels"]
author: opus
date: 2026-11-09
---

# Deadhand — запрограмуй увесь забіг наперед, а рівень після запуску зміниться: план мусить мати запас міцності

## Суть
Покрокова головоломка-платформер на маленькій сітці: гравець складає чергу команд для бігуна (кроки, підйом, стрибки, ящик, перемикач), тисне «run» — і далі не керує. Після запуску рівень **змінюється**: гра заздалегідь каже, скільки буде змін і якого типу (таймінг, розкладка, стан), але не каже, який обʼєкт. Тож «тугий план — крихкий план»: виграє програма із запасом. Раз за спробу можна перервати виконання й переписати решту черги — коштом очок.

## Поле і час
- Невелика квадратна сітка, вид збоку (теги Side Scroller, Puzzle Platformer, Grid-Based Movement).
- Фаза плану: нічого не рухається, гравець складає чергу. Фаза виконання: одна команда на тік, без вводу (крім одного переривання).
- Кожна спроба отримує свій набір змін; гра оголошує їх кількість і типи до запуску (`info: partial`).
- Таймінгу реакції нема (категорія «Playable without Timed Input»).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Бігун (runner) | player | орієнтація (?) | виконує чергу команд по одній за тік |
| Другий бігун (етап 8) | player | спільна черга | виконує ту саму чергу; утекти мають обидва |
| Ящик | object | — | команда push зсуває його |
| Перемикач | switch | стан | команда flip перемикає; що саме вмикає — (?) |
| Тріснута плитка (етап 7) | terrain | — | обвалюється через 1 тік після того, як бігун зійшов; не відновлюється |
| Вихід | static | — | бігун дійшов → утеча |
| Оголошена зміна | zone | тип: timing / layout / state | після запуску міняє таймінг, розкладку або стан невідомого обʼєкта |
| Черга команд | mark | довжина; par (?) | програма бігуна; вся складається до запуску |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(command)` → ТО `custom: «команда дописується в кінець черги»` — рух на полі не відбувається.
- КОЛИ `input(run)` → ТО `custom: «план зафіксовано»`, `custom: «оголошено N змін і їхні типи, без обʼєкта»`.
- КОЛИ `tick` → ТО `custom: «бігун виконує наступну команду черги»`.
- КОЛИ `exec(step_left|step_right)` → ЯКЩО `free(cell)` → ТО `move(runner, dir)`; інакше (?) `block`.
- КОЛИ `exec(climb|descend|leap|hop|drop)` → ТО `custom: «рух угору / вниз / стрибок через клітину / зістрибування»` (?) — точна геометрія не описана.
- КОЛИ `exec(push)` → ЯКЩО `occupied(front_cell, crate)` → ТО `push(crate)`.
- КОЛИ `exec(flip)` → ЯКЩО `occupied(cell, switch)` → ТО `set_state(switch, toggled)`.
- КОЛИ `exec(turn)` → ТО `face(runner, opposite)` (?).
- КОЛИ `exec(wait)` → ТО `custom: «тік без дії»`; `hold` — `custom: «утримання (?)»`.
- КОЛИ `leave(runner, cracked_tile)` → ТО `custom: «через 1 тік»` `set_cell(cracked_tile, void)` — назавжди.
- КОЛИ `custom: «настав момент оголошеної зміни»` → ТО `custom: «змінюється таймінг, розкладка або стан одного обʼєкта»`.
- КОЛИ `input(interrupt)` → ЯКЩО `first_time` (за спробу) → ТО `custom: «пауза; решту черги можна переписати»`, `score(-n)`.
- КОЛИ `reach(runner, exit)` → ЯКЩО `custom: «на етапі 8 — обидва бігуни»` → ТО `win`.
- КОЛИ `program_end` → ЯКЩО `custom: «бігун не дійшов до виходу»` → ТО `lose` — нова спроба з новими змінами (?).
- КОЛИ `win` → ЯКЩО `counter(score, <=, par)` → ТО `custom: «медаль par»`; ЯКЩО `first_time` → `custom: «медаль першої спроби»`; ЯКЩО `custom: «без переривання»` → `custom: «третя медаль»`.
- Перемога: бігун(и) утекли · Поразка: план не довів до виходу (?) · Рахунок: очки, мінус за переривання; до 3 медалей за рівень.

## Керування і ввід
- Команди: step left, step right, climb, descend, leap, hop, drop, wait, push, flip, turn, hold.
- Клавіатура, миша або тач — кожен спосіб окремо достатній; працює офлайн.
- «Run» запускає план; «interrupt» — одне переривання за спробу.

## Вікна, меню, HUD
- `game-screen`: сітка рівня, черга команд (`code-editor`), прогноз змін (custom: «N змін, тип»), лічильник par (`par-moves`) (?).
- `level-select`: 8 етапів + фінальний рівень ALL HANDS, що поєднує всі механіки.
- `daily-window`: денний пазл, 3 спроби.
- `leaderboard`: Steam — глобально, друзі, біля свого рангу.
- `replay-window` (WATCH): перегляд переможного плану іншого гравця разом зі змінами, які випали в його спробі.
- `end-screen`: медалі рівня (?).

## Фічі поза полем
- 81 пазл у 8 етапах + ALL HANDS; етап 7 — тріснуті плитки, етап 8 — два бігуни на одній черзі.
- `daily-puzzle`: однаковий для всіх; 3 спроби з різними змінами; очки — у Steam-лідерборди.
- Кожен рівень перевірено розвʼязувачем: виграшний за будь-якої зміни, яку він може оголосити.
- 21 досягнення, Steam Cloud, офлайн-гра з синхронізацією.

## Варіації й родичі
- Програмування бігуна командами: [lightbot](lightbot.md), [robozzle](robozzle.md), [cargo-bot](cargo-bot.md); спільна програма кількох виконавців — [7-billion-humans](7-billion-humans.md).
- План наперед проти невизначеного світу: [roborally](roborally.md), [colt-express](colt-express.md) (план одночасно з суперниками, а не з «долею»).
- **Осі варіацій:** невизначеність (нема / оголошені зміни / приховані) · втручання під час виконання (нема / одне переривання / кілька) · виконавці (1 / 2 на спільній черзі) · оцінка (par / перша спроба / без переривань).

## Цікавинки для курсу
- Інтерпретатор черги команд бігуна на сітці з гравітацією — 🥉.
- Оголошені зміни: генератор змін типу timing/layout/state і прогноз «N змін, тип» — 🥉.
- Розвʼязувач, що перевіряє план проти **всіх** можливих змін (робастне планування) — 🥇.
- Одне переривання: пауза й переписування хвоста черги — 📎.
- Тріснута плитка з затримкою на 1 тік — 🌱.
- Спільна черга двох бігунів — 📎.
- WATCH: replay плану разом із випалими змінами — 📎.

## Мапа на каталог
- Є: `command-program` · `reach-exit` · `push-object` (ящик) · `button-toggle` (перемикач) · `gravity-fall` · `daily-puzzle` · `leaderboard` · `replay` (WATCH) · `sequential-levels` (етапи) · `keyboard-controls` · `cell-click` (миша/тач).
- **Нема** → пропозиції карток:
  - `+announced-perturbations` «Після запуску рівень змінюється; оголошено кількість і тип» · game-logic/program · 🥉.
  - `+single-interrupt` «Одне переривання програми за спробу зі штрафом» · game-logic/program · 📎.
  - `+shared-queue-runners` «Кілька виконавців однієї черги команд» · game-logic/program · 📎.
  - `+solver-verified-levels` «Рівень перевірено на виграшність за всіх змін» · levels/solvability · 🥇.
  - `+plan-then-execute`, `+crumbling-floor`, `+medal-rating`, `+watch-others-solutions` — підтвердження.

## Пропозиції до словників
- `+effect:interrupt` — зупинити виконання програми для правки (підтвердження).
- `+effect:announce` — оголосити майбутню подію гравцеві (підтвердження).
- `+effect:wait` — команда «нічого не робити тік» (підтвердження).
- `+trigger:run_start` — гравець запустив програму (підтвердження).
- `+trigger:level_change(kind)` — настала оголошена зміна рівня.
- `+feature:daily-attempts` — N спроб денного пазла (підтвердження), `+feature:watch-others-solutions` — перегляд чужих розвʼязків.
- `+ui:change-forecast` — прогноз «скільки змін і якого типу».
- `+card:announced-perturbations`, `+card:single-interrupt`, `+card:shared-queue-runners`, `+card:solver-verified-levels` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Deadhand](https://store.steampowered.com/app/5395820/Deadhand/) — Chris Karageorge; черга команд, оголошені зміни (timing/layout/state), одне переривання, 3 медалі, 81 пазл, етапи 7–8, денний пазл, WATCH, розвʼязувач, 21 досягнення; теги.
- [Steam API appdetails](https://store.steampowered.com/api/appdetails?appids=5395820) — той самий опис, категорії керування й лідербордів.

## Непевне
- (?) Дата виходу — «coming soon», рік не вказано.
- (?) Точна дія climb / descend / leap / hop / drop / hold і чи є драбини, ями, смерть від падіння.
- (?) Що вмикає перемикач; чи є двері, вороги, рухомі платформи.
- (?) Одиниця par — кількість команд чи тіків; формула очок.
- (?) Як обираються зміни спроби (випадково з набору, оголошеного рівнем) — `random: runtime` за описом «each attempt gets its own changes».
- (?) Що стається при провалі: рестарт рівня з новими змінами чи кінець спроби.
- (?) Вигляд меню й екрана медалей — опису нема; гра ще не вийшла, відео не знайдено.
