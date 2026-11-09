---
title: Minesweeper Sonar
slug: minesweeper-sonar
aka: []
family: hidden-deduction
also: [tower-lanes]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2026
platforms: [PC (Windows 10+), SteamOS / Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3133120/Minesweeper_Sonar/", best: true, note: "опис: ракета = поле сапера, повний/частковий розвʼязок, валюта на атаку й ремонт, режими Story / 99999 / Custom / Static, Radius Blast, chord, швидкість 0.5–3×"}
  - {kind: other, url: "https://steamcommunity.com/app/3133120/discussions/", note: "форум Steam (на 09.11.2026 — два треди без механік)"}
  - {kind: official, url: "https://www.youtube.com/@Linesinorbitstudio", note: "YouTube-канал студії lines in orbit studio (лінк зі сторінки Steam)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Minesweeper+Sonar+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, chord-click, neighbor-count-clue, explode-area, hp-damage, round-currency, spawn-schedule, sequential-levels, mode-select, level-select, in-game-editor, level-exchange, game-settings, controls-remap, game-screen, main-menu, end-screen, editor-window, +minigrid-projectile, +partial-solve-reward, +probabilistic-reveal, +attention-split-actions, +fast-forward, +speed-control]
proposes: ["+trigger:solved", "+cond:solved_fraction", "+effect:reveal_chance", "+feature:mode-survival-hp", "+card:minigrid-projectile", "+card:partial-solve-reward", "+card:probabilistic-reveal", "+card:attention-split-actions"]
author: opus
date: 2026-11-09
---

# Minesweeper Sonar — кожна ракета, що летить у твій човен, несе своє міні-поле сапера: розвʼяжи до удару

## Суть
Ворожий корабель запускає по твоєму човну ракети; кожна ракета — окреме маленьке поле сапера. Повністю розвʼязане поле підриває ракету ще в польоті (вибух шкодить усьому поруч) і дає валюту; частково розвʼязане — ракета все одно влучає, але шкода й нагорода пропорційні розвʼязаній частці; клік по міні — повна шкода й нуль валюти. Валюту витрачають на атаку ворожого корабля й ремонт свого — і саме для цього доводиться **відводити погляд від ракет**. Ядро — класична дедукція сапера під real-time тиском кількох паралельних полів.

## Поле і час
- Екран бою: човен гравця, ворожий корабель і ракети в польоті; кожна ракета несе квадратне міні-поле (розміри — за типом ракети (?)).
- Real-time: ракети летять зі швидкістю свого типу, нові спавняться з інтервалом (у Custom задається «час між спавнами»).
- Глобальна швидкість гри — від 0.5× до 3.0×; утримання кнопки fast-forward тимчасово прискорює (щоб не чекати наступну ракету).
- Режим Static — ракети стоять, поле розвʼязується без поспіху.
- Сусідство для чисел — класичне, імовірно 8 (?): є chord.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Човен гравця | player | HP | ціль ракет; лагодиться за валюту |
| Ворожий корабель | enemy | HP (у режимі 99999 — 99 999) | запускає ракети; гравець атакує його за валюту |
| Ракета | projectile | тип, швидкість | летить до човна; несе міні-поле сапера |
| Міні-поле ракети | zone | розмір/щільність за типом (?) | поле сапера; стан «розвʼязано на X %» |
| Закрита клітина | static | — | відкривається кліком |
| Число | mark | 0–8 (?) | кількість мін серед сусідів |
| Міна | hazard | — | клік → ракета дає повну шкоду, валюти 0 |
| Прапорець | mark | — | позначка гравця; вибухи не відкривають позначене |
| Вибух ракети | hazard | радіус | розвʼязана ракета вибухає, шкодить ціле поруч, відкриває безпечні клітини сусідніх ракет з шансом 50 % |
| Radius Blast | — | вміння гравця | вибух, що відкриває всі небомбові непозначені клітини в радіусі зі 100 % |
| Валюта | resource | — | за розвʼязання ракет; на атаку й ремонт |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `timer(spawn_interval)` → ТО `spawn_at(missile, enemy_ship)`; тип і швидкість — з рівня (у Custom — задані гравцем).
- КОЛИ `tick` → ТО `move(missile, toward_boat)` зі швидкістю типу × швидкість гри.
- КОЛИ `input(reveal, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)` (число сусідніх мін).
- КОЛИ `input(flag, c)` → ТО `mark(c, flag)` / `unmark(c)`.
- КОЛИ `input(chord, c)` → ЯКЩО `custom: «прапорців навколо стільки, скільки показує число»` → ТО `reveal(unflagged_neighbours)`.
- КОЛИ `input(reveal, c)` → ЯКЩО `cell(c, mine)` → ТО `damage(boat, full)` від цієї ракети, `custom: «валюти за ракету 0»`.
- КОЛИ `custom: «усі безпечні клітини ракети відкрито»` → ТО `explode(radius)`, `damage(nearby, n)`, `currency(+повна)`, `disappear(missile)`.
- КОЛИ `after(explode)` → ЯКЩО `prob(50)` and `not cell(c, mine)` and `custom: «клітина без прапорця»` → ТО `reveal(c)` у сусідніх ракетах у радіусі.
- КОЛИ `contact(missile, boat)` → ЯКЩО `custom: «поле розвʼязане частково»` → ТО `damage(boat, n × (1 − частка))`, `currency(+повна × частка)`.
- КОЛИ `input(radius_blast)` → ТО `explode(radius)`, `custom: «відкрити всі небомбові непозначені клітини в радіусі (100 %)»`.
- КОЛИ `input(attack)` → ЯКЩО `custom: «вистачає валюти»` → ТО `currency(-ціна)`, `damage(enemy_ship, n)`.
- КОЛИ `input(repair)` → ЯКЩО `custom: «вистачає валюти»` → ТО `currency(-ціна)`, `heal(boat, n)`.
- КОЛИ `input(fast_forward)` (утримання) → ТО `custom: «прискорити гру, доки кнопку тримають»`.
- КОЛИ `hp_zero(enemy_ship)` → ТО `win`, `next_level` (Story).
- КОЛИ `hp_zero(boat)` → ТО `lose`; у режимі 99999 — `game_over`, `score(час виживання)`.
- Перемога: знищити ворожий корабель. · Поразка: HP човна = 0. · Рахунок: у 99999 — скільки протримався.

## Керування і ввід
- Миша: клік — відкрити клітину на ракеті; прапорець — (?) імовірно права кнопка; chord — **завжди на середній кнопці**, плюс другорядна клавіша на вибір.
- Кнопки атаки й ремонту поза полями ракет — щоб натиснути, треба перевести погляд; звукові сигнали підказують, що відбувається з ракетами, поки дивишся вбік.
- Кнопка fast-forward (утримання) і кнопка Radius Blast.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story · 99999 · Custom · Static.
- `level-select` (Story): рівні зростаючої складності; сюжет «хто стоїть за атаками».
- `editor-window` (Custom): типи ракет і їхня швидкість, час між спавнами, HP гравця й ворога; рівень можна поділитись і скопіювати.
- Static: вибір типу ракети → поле без руху.
- `game-screen`: човен, ворожий корабель, ракети з міні-полями; HUD — HP обох (`hp-bar`), валюта (`coins`), кнопки атаки й ремонту, `fast-forward`, Radius Blast; таймер (у 99999 — час виживання) (?).
- `settings-window`: швидкість гри 0.5–3.0× (`speed-slider`), привʼязка клавіші chord, віджет-скрін.
- `end-screen`: перемога / поразка.

## Фічі поза полем
- `speed-control` (0.5–3.0×) + тимчасовий fast-forward утриманням.
- `remap-controls` — друга клавіша для chord.
- Режими: сюжет (`levels-sequential`), «99999» — виживання проти корабля з величезним HP, `mode-sandbox` (Custom), `mode-practice` (Static).
- `level-editor` + `level-sharing` (копіювати/вставляти рівні Custom).
- Steam: досягнення, Cloud, демо; мови EN, PT-BR, PT-PT.

## Варіації й родичі
- База — [minesweeper](minesweeper.md); real-time сапер з тиском — [tetrisweeper](tetrisweeper.md) (рядки сапера в падаючих фігурах), [mined-out](mined-out.md); бій з економікою «розвʼязав — отримав» — [demoncrawl](demoncrawl.md), [boomboombattle](boomboombattle.md).
- Поза сімʼєю: Missile Command (захист від ракет у польоті), tower-defense-лінія (ціль летить до бази, ти маєш встигнути).
- Осі варіацій: **скільки полів одночасно** — одне / багато дрібних у русі (тут); **частковий розвʼязок** — нічого не дає / пропорційна нагорода й шкода (тут); **автовідкриття** — лише flood-нулі / ймовірнісне від сусідніх вибухів (50 %) / гарантоване вмінням (100 %).

## Цікавинки для курсу
- Ракета як рухомий контейнер міні-поля: кілька незалежних полів сапера в одному кадрі — 🥈.
- Частка розвʼязаного → пропорційні шкода й нагорода — 📎.
- Вибух з ймовірнісним відкриттям сусідніх полів (50 %) проти гарантованого (100 %) і повага до прапорців — 📎.
- Розщеплена увага: економіка атаки/ремонту поза полем, звукові сигнали замість погляду — 🥉.
- Custom як набір параметрів (типи, швидкість, інтервал, HP) з кодом для обміну — 📎.
- Глобальна швидкість 0.5–3× і fast-forward утриманням для real-time циклу — 🌱.

## Мапа на каталог
- Є: `cell-click` · `chord-click` · `neighbor-count-clue` ↔ поля ракет; `explode-area` ↔ вибух ракети й Radius Blast; `hp-damage` ↔ HP човна й корабля; `round-currency` ↔ валюта; `spawn-schedule` ↔ інтервал ракет; `sequential-levels` + `level-select` ↔ Story; `mode-select`; `in-game-editor` + `editor-window` + `level-exchange` ↔ Custom; `game-settings` + `controls-remap`; `game-screen` · `main-menu` · `end-screen`.
- Корпус уже пропонує: `+fast-forward`, `+speed-control`.
- **Нема** → пропозиції карток:
  - `+minigrid-projectile` «Снаряд несе власне міні-поле пазла» · entities/combat · 🥈 · слот {grid: by_type}.
  - `+partial-solve-reward` «Частковий розвʼязок — пропорційний ефект» · game-logic/score · 📎.
  - `+probabilistic-reveal` «Вибух відкриває клітини з шансом» · game-logic/constraints · 📎 · слот {p: 50|100, skip_flags: bool}.
  - `+attention-split-actions` «Дії поза полем у real-time забирають увагу» · design · 🥉.

## Пропозиції до словників
- `+trigger:solved` — поле/підзадача розвʼязана повністю (тут ракета).
- `+cond:solved_fraction` — частка розвʼязаного поля (для пропорційних ефектів).
- `+effect:reveal_chance` — відкрити клітини з імовірністю p, оминаючи прапорці.
- `+feature:mode-survival-hp` — режим «протримайся проти ворога з величезним HP» (99999).
- `+card:minigrid-projectile`, `+card:partial-solve-reward`, `+card:probabilistic-reveal`, `+card:attention-split-actions` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Minesweeper Sonar](https://store.steampowered.com/app/3133120/Minesweeper_Sonar/) — опис «An Even Tenser Minesweeper Experience!», повний/частковий/міна, атака й ремонт за валюту, «look away», звукові сигнали, Radius Blast (100 %) проти вибухів ракет (50 %), chord на Mouse 3, fast-forward, швидкість 0.5–3×, режими, реліз 4.11.2026, lines in orbit studio.
- [Форум Steam](https://steamcommunity.com/app/3133120/discussions/) — без механік (перевірено).
- [YouTube-канал lines in orbit studio](https://www.youtube.com/@Linesinorbitstudio) — посилання зі сторінки Steam (відео не переглянуто).
- Steam News (API): оновлення 28.10.2026 — таймер більше не йде після перемоги/поразки, підтримка widescreen.

## Непевне
- (?) Типи ракет, розміри їхніх полів, кількість мін, ціни атаки й ремонту, шкода від ракет — на сторінці не названі.
- (?) Чи клік по міні шкодить одразу, чи коли ракета долітає.
- (?) Що саме «nearby targets» для вибуху: інші ракети, ворожий корабель чи обидва.
- (?) Як ставиться прапорець і чи є flood-відкриття нулів — сторінка про це мовчить.
- (?) Radius Blast — чи має ціну/перезарядку; сторінка цього не каже.
- (?) Клас `ai` для ворожого корабля — ворог лише запускає ракети за розкладом рівня; «розумності» в описі нема.
