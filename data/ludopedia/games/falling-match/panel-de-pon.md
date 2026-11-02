---
title: Panel de Pon (Tetris Attack, Puzzle League)
slug: panel-de-pon
family: falling-match
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: survive
year: 1995
platforms: [SNES, Game Boy, Satellaview, N64, GBC, GameCube, GBA, DS, DSiWare, 3DS, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Panel_de_Pon", best: true, note: "серія: курсор на 2 клітини, стек росте знизу, chain vs combo, стоп, сміття і його перетворення, shock-блоки, Garbage Battle, усі версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetris_Attack", note: "SNES/GB-версія для Заходу: режими Endless, Timed 2 хв, Stage Clear, Puzzle, Story"}
  - {kind: fandom, url: "https://www.mariowiki.com/Tetris_Attack", note: "Super Mario Wiki: режими, Stop (Mr. Time), швидкість 1–99, Stage Clear з лінією, Puzzle з лімітом ходів, Shock Panels"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Puzzle_League", note: "N64: поле 6 завширшки, 3D-циліндр шириною 18, режими Marathon/Time Zone/Spa Service/Puzzle University"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tile-matching_video_game", note: "Panel de Pon запровадив обмін плиток, Bejeweled популяризував"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=panel+de+pon+chain+gameplay", note: "пошук; геймплей і техніки ланцюгів"}
stage: v1
coverage: 75
mechanics: [keyboard-controls, gravity-fall, progress-acceleration, event-points, combo-multiplier, time-out, score-records, game-pause, end-screen, difficulty-levels, ai-opponent, hot-seat, sequential-levels, satisfy-constraints, +rising-stack, +manual-row-add, +swap-cursor, +line-match-clear, +chain-reaction, +cascade-gravity, +garbage-attack, +garbage-adjacent-clear, +stop-timer, +skill-chain, +move-limit-puzzle, +level-password]
proposes: ["+trigger:settled", "+trigger:pattern", "+effect:swap", "+effect:fall", "+effect:raise_stack", "+effect:convert_garbage", "+effect:send_garbage", "+cond:state", "+cond:chain", "+ui:stop-timer", "+ui:chain-counter", "+ui:danger-line", "+window:character-select", "+feature:mode-puzzle", "+axis:control", "+axis:gravity"]
author: opus
date: 2026-11-02
---

# Panel de Pon — міняй дві сусідні панелі в стеку, що росте знизу; ланцюги, стоп-час і сміття

## Суть
Стек кольорових панелей повільно піднімається знизу; торкнувся стелі — поразка. Курсор шириною 2 клітини міняє місцями дві горизонтально сусідні панелі (або панель і порожнечу) — **без жодної умови**, обмін завжди легальний. 3+ однакових у рядок чи стовпець зникають, панелі зверху падають; **combo** — багато панелей одним обміном, **chain** — збіг, викликаний падінням після попереднього. Комбо й ланцюги дають **стоп** підйому та, у versus, кидають супернику **сміттєві блоки**, які розсипаються на панелі, коли поруч зчищено збіг. Це «модель обміну в живому стеку»: на відміну від Bejeweled, поле не поповнюється згори, а росте знизу.

## Поле і час
- Поле 6 стовпців × 12 рядів (?); під ним видно **наступний ряд** — затемнений, ще не активний, доки не підніметься.
- Шари: стек панелей (сітка) + сміттєві блоки (прямокутники кількох клітин, можуть стирчати над видимим полем) + курсор 2×1.
- Real-time: стек піднімається плавно (по пікселях), новий ряд стає активним, коли повністю вийшов; темп = рівень швидкості (1–99 в Endless). Під час зчищення й стоп-часу підйом зупиняється.
- Стани панелі: `idle` · `swapping` (кілька кадрів) · `hover` (коротка пауза над порожнечею перед падінням) · `falling` · `landing` · `clearing` (мигання → «лопання» по одній) · `chain-flag` (впала через зчищення).
- Pokémon Puzzle League: 3D-режим — поле-**циліндр** шириною 18, курсор переходить через край (тор по горизонталі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | 2×1, позиція | рух 4 напрямки в межах поля; обмін вмісту двох клітин |
| Панель | tile | колір/символ (5–6: серце, коло, трикутник, зірка, ромб, обернений трикутник (?)) | обмінюється; без опори — hover → падає; 3+ в рядок/стовпець → зникає |
| Новий ряд (preview) | spawner | випадкові кольори, без готових збігів (?) | піднімається знизу; неактивний, доки не вийшов повністю |
| Сміття combo | hazard | ширина 3–6, висота 1 | падає зверху на стек; не обмінюється; перетворюється від сусіднього збігу |
| Сміття chain | hazard | ширина 6, висота = chain−1 (?) | так само; перетворюється по одному ряду за раз |
| Shock Panel «!» (Vs.) | tile | сіра з «!» | збіг 3+ shock-панелей → супернику сірий/хромований блок (?) |
| Сірий (chrome) блок | hazard | — | очищається лише за іншими правилами (поруч зі збігом shock-панелей (?)) |
| Лінія Stage Clear | zone | висота | зʼявляється після достатньої кількості зчищень; стек нижче неї — ціль |
| Item-панелі (Planet Puzzle League, Garbage Battle) | tile | Fever / Tri-Color / Reflect / Twitch / Paralyze / Fog | спецефект на себе чи суперника |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swap)` → ЯКЩО `not state(a|b, clearing) and not occupied(a|b, garbage)` → ТО `swap(a, b)` (панель ↔ панель або панель ↔ порожнеча); обмін зараховано **завжди**, навіть без збігу.
- КОЛИ `after(swap)` → ЯКЩО `free(cell_below)` → ТО `set_state(panel, hover)`, потім `fall(panel)`; під час hover/падіння панель ще можна підхопити обміном знизу чи збоку (?).
- КОЛИ `pattern(line(3+, same_color))` (лише рядок або стовпець) → ТО `set_state(cells, clearing)`, `score(10 × n)` (?), `timer(stop, +)`; через анімацію `clear(cells)`.
- КОЛИ кілька ліній утворено одним обміном/падінням → ТО `custom: «combo = кількість панелей»`; ЯКЩО `combo ≥ 4` → ТО `score(combo_bonus)` і (Vs.) `custom: «send_garbage — блок шириною ≈ combo−1 (?)»`.
- КОЛИ `after(clear)` → ТО `fall(panels_above)` з `set_state(chain_flag)`.
- КОЛИ `pattern(line(3+))` → ЯКЩО `state(any_cell, chain_flag)` → ТО `combo(+1)` = chain ×2, ×3…, `score(chain_bonus)` (?), `timer(stop, +більше)`, (Vs.) `send_garbage(full_width × (chain−1) rows)` (?).
- КОЛИ `settled` (нема падінь із прапорцем) → ТО `reset_combo`, `custom: «chain_flag знімається з усіх, хто ліг»`.
- **Skill/time-lag chain**: КОЛИ `state(cells, clearing)` → ТО гравець може робити нові обміни деінде; збіг, утворений панелями з прапорцем під час падіння, продовжує ланцюг.
- КОЛИ `pattern(line)` → ЯКЩО `adjacent(cleared_cell, garbage)` → ТО `custom: «convert_garbage — нижній ряд блока стає випадковими панелями (chain_flag), решта блока опускається й лишається сміттям»`; суміжні блоки, що торкаються, теж перетворюються (?).
- КОЛИ `tick` → ЯКЩО `not state(stop) and not state(clearing_any)` → ТО `custom: «raise_stack — стек вгору на темп рівня»`; КОЛИ новий ряд вийшов повністю → ТО він стає активним, `spawn_at(new_row_preview, bottom)`.
- КОЛИ `input(raise)` (L/R) → ЯКЩО `not state(stop) and not state(clearing_any)` → ТО `custom: «raise_stack — швидкий підйом»`, `score(+1)` за ряд (?), `timer(stop, =0)`.
- КОЛИ `custom: «стек торкнувся стелі під час підйому»` → ЯКЩО `timer(stop, ==, 0)` → ТО `lose`; у Vs. є коротка пільга (?).
- Endless: КОЛИ `counter(time|cleared, ≥, step)` → ТО `speed(rise, +)`; Endless до 99 999 очок → титри.
- Timed / Time Zone: КОЛИ `timer(2:00, ==, 0)` → ТО `game_over`, підсумок очок.
- Stage Clear: КОЛИ `count(panels_above(clear_line), ==, 0)` (стек опустився нижче лінії) → ТО `win`, `next_level`; 30 раундів.
- Puzzle: стек не росте; КОЛИ `count(panels, ==, 0)` → ЯКЩО `counter(swaps, ≤, limit)` → ТО `win`; КОЛИ `counter(swaps, ==, limit) and count(panels) > 0` → ТО `restart`.
- Vs.: КОЛИ `combo|chain` → ТО `send_garbage`; сміття падає на суперника, коли його поле стабільне; поразка — стек торкнувся стелі.

## Керування і ввід
- D-pad — рух курсора 2×1 на клітину (утримання — автоповтор); A/B — обмін двох панелей під курсором; L/R — ручний підйом стеку; Start — пауза.
- Planet Puzzle League (DS тримають боком): **стилус** — тягнеш панель ліворуч/праворуч на кілька клітин підряд (послідовність обмінів одним жестом); кнопки — альтернатива.
- Важливо: обмін — не «хід із перевіркою», а миттєва маніпуляція в живому полі; швидкість рук (APM) — частина майстерності.

## Вікна, меню, HUD
- `splash-screen` → `main-menu` з `mode-select`: 1P (Endless · Time Trial · Stage Clear · Puzzle · Vs. CPU/Story) · 2P Vs. · Options.
- `difficulty-select` (Easy/Normal/Hard; Super Hard — схований), вибір стартової швидкості 1–99 (Endless).
- `character-select` — персонаж (феї у Panel de Pon / Йоші й друзі в Tetris Attack / тренери в Pokémon Puzzle League) — косметика + суперник у Story.
- `level-password` — Puzzle і Stage Clear зберігають прогрес паролями.
- `game-screen`: поле 6×12 з курсором, `score`, `timer-elapsed` / `timer-countdown` (Timed), `level-number` (швидкість), `custom: «stop-timer»` (будильник Mr. Time з лічильником), `popup-text` combo «4», «5» та chain «×2», «×3» над місцем збігу; `danger-line`-ефект — стовпці біля стелі підстрибують, музика пришвидшується (?).
- Vs.: два поля поруч, портрети, лічильник перемог у сеті (?).
- Puzzle: `move-counter` «лишилось обмінів».
- `pause-menu`; `end-screen` — Game Over / Clear / результат; `leaderboard` для Endless/Timed.
- Переходи: main-menu → mode → (difficulty/character) → game-screen → end-screen → retry / main-menu; Stage Clear — після раунду наступний з паролем.

## Фічі поза полем
- Режими: `mode-endless`, `mode-time-attack` (2 хв), `custom: «stage-clear»` (опустити стек нижче лінії), `mode-puzzle` (банк пазлів з лімітом ходів), `mode-versus` (CPU — Story, 2P), Garbage Battle з предметами (Planet Puzzle League), 3D-циліндр (Pokémon PL).
- `difficulty-presets`, `custom-difficulty` (швидкість 1–99), `ai-opponent-levels`.
- `level-password`, `leaderboard-local`, `pause`; Planet PL — `online-multiplayer` (Nintendo WFC) (?), `touch-controls`.
- `tutorial` (Pokémon PL: Professor Oak's Lab, Mimic Mansion).

## Варіації й родичі
- Panel de Pon (SFC, 1995) → Tetris Attack (SNES/GB, 1996; Йоші-скін, назва «Tetris» лише маркетинг) → Pokémon Puzzle League (N64, 2000; 3D-циліндр) / Pokémon Puzzle Challenge (GBC) → Dr. Mario & Puzzle League (GBA, 2005) → Planet Puzzle League (DS, 2007; стилус, предмети) → Animal Crossing Puzzle League (3DS, 2016).
- Родичі: Bejeweled (обмін сусідів, але лише зі збігом, поле поповнюється згори), Magical Drop і Puzzle Bobble (тиск стелі), Tetris/Puyo (сміття), Yoshi's Cookie (зсув рядів).
- **Осі варіацій**: звідки нові плитки (згори / знизу ростом / падаюча фігура) · легальність обміну (лише зі збігом / будь-який) · напрямок обміну (горизонтальний 2×1 / 4 сусіди / drag на N клітин) · топологія (прямокутник / циліндр) · сміття (нема / прямокутні блоки, що перетворюються / сірі блоки з особливим правилом).

## Цікавинки для курсу
- Курсор 2×1 і обмін без умови + стани панелі (swap/hover/fall/clear) як автомат — 🥉 (автомат станів на клітину).
- Стек, що росте знизу, з неактивним рядом-превʼю і ручним підйомом — 📎.
- Розрізнення combo і chain через прапорець «впала після зчищення» — 🥉.
- Skill-chain: ввід триває під час анімацій, ланцюг подовжується руками гравця — 🥈 (асинхронні таймери на панелях, а не глобальний «фаза каскаду»).
- Стоп-час як нагорода, що відтерміновує поразку — 🌱.
- Сміттєві блоки, що розсипаються по ряду від сусіднього збігу й можуть продовжувати ланцюг — 🥈.
- Puzzle-режим: зчистити поле за N обмінів + розвʼязувач перебором — 🥇.
- Циліндричне поле (wrap по X) — 🌱 поверх наявного.

## Мапа на каталог
- Є: `keyboard-controls` · `gravity-fall` · `progress-acceleration` (швидкість 1–99) · `event-points` · `combo-multiplier` (combo, chain) · `time-out` (Timed) · `score-records` · `game-pause` · `end-screen` · `difficulty-levels` · `ai-opponent` (Vs. CPU) · `hot-seat` (2P одночасно; найближча картка) · `sequential-levels` (Stage Clear) · `satisfy-constraints` (Puzzle: поле порожнє за ліміт).
- **Нема** → пропозиції карток:
  - `+rising-stack` «Стек росте знизу» · game-logic/waves · 📎 · слоти {speed, preview_row: yes|no}.
  - `+manual-row-add` · interface/input · 🌱 (спільна з Magical Drop) — ручний підйом.
  - `+swap-cursor` «Курсор-обмін 2×1 без умови» · interface/input · 📎 (родич `+match-3-swap` з {revert: no, need_match: no}).
  - `+line-match-clear` · entities/legality · 📎 · {directions: 4} (спільна).
  - `+chain-reaction` · game-logic/score · 🥉 (спільна; тут chain ≠ combo).
  - `+cascade-gravity` · entities/move · 📎 (спільна).
  - `+garbage-attack` · game-logic/opponent · 🥉 (спільна; тут блоки-прямокутники).
  - `+garbage-adjacent-clear` · entities/interact · 🌱 (спільна з Puyo; тут — розсипання по ряду).
  - `+stop-timer` «Стоп-час як нагорода» · game-logic/waves · 🌱 · слот {per_combo, per_chain}.
  - `+skill-chain` «Ланцюг, що триває під час анімацій» · game-logic/score · 🥈.
  - `+move-limit-puzzle` «Зчистити за N ходів» · game-logic/win · 📎.
  - `+level-password` · interface/menus · 🌱 (спільна з Chip's Challenge).

## Пропозиції до словників
- `+trigger:settled` — 🔥 підтверджую (кінець ланцюга); `+trigger:pattern` — ⏳ підтверджую.
- `+effect:swap` — 🔥 підтверджую; `+effect:fall` — 🔥 підтверджую (з hover-затримкою).
- `+effect:raise_stack` — зсунути все поле на ряд угору з новим рядом знизу (Panel de Pon, Magical Drop навпаки — стеля вниз).
- `+effect:convert_garbage` — сміття → звичайні плитки по ряду (Panel de Pon; родич Puyo `disappear` сміття).
- `+effect:send_garbage` — 🔥 підтверджую.
- `+cond:state` — 🔥 підтверджую (clearing, hover, chain_flag); `+cond:chain` — ⏳ підтверджую.
- `+ui:stop-timer` — індикатор паузи підйому (Mr. Time); `+ui:chain-counter` — «×N» над місцем збігу (родич `action-text`); `+ui:danger-line` — ⏳ підтверджую (стовпці біля стелі підстрибують).
- `+window:character-select` — 🔥 підтверджую; `+feature:mode-puzzle` — ⏳ підтверджую.
- `+axis:control` — значення `swap-cursor` (курсор над двома клітинами).
- `+axis:gravity` — `cascade` + стани hover (затримка перед падінням як параметр).

## Джерела
- ⭐ [Wikipedia: Panel de Pon](https://en.wikipedia.org/wiki/Panel_de_Pon) — правила серії, chain vs combo, стоп, сміття (перетворення від сусіднього збігу, ширина/товщина від комбо/ланцюга), shock-блоки, Garbage Battle, усі версії.
- [Wikipedia: Tetris Attack](https://en.wikipedia.org/wiki/Tetris_Attack) — режими Story/Endless/Timed 2 хв/Stage Clear/Puzzle, різниця з японським оригіналом.
- [Super Mario Wiki: Tetris Attack](https://www.mariowiki.com/Tetris_Attack) — Stop і Mr. Time, Endless зі швидкістю 1–99 і складністю, Stage Clear 30 раундів, Puzzle з паролями, Shock Panels у Vs.
- [Wikipedia: Pokémon Puzzle League](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Puzzle_League) — поле 6 завширшки, 3D-циліндр 18, режими.
- [Wikipedia: Tile-matching video game](https://en.wikipedia.org/wiki/Tile-matching_video_game) — роль у винаході обміну.
- YouTube: пошук «panel de pon chain gameplay».

## Непевне
- (?) Висота поля 12, набір символів, «наступний ряд без готових збігів» — з памʼяті.
- (?) Таблиці очок (10 за панель, бонуси combo/chain) і розміри сміття (combo 4 → 3 клітини, chain N → N−1 рядів) — з памʼяті; Wikipedia лише «товщина росте з ланцюгом».
- (?) Наскільки можна маніпулювати падаючими панелями: підхоплення обміном під час hover/падіння — з памʼяті, StrategyWiki недоступна (403).
- (?) Пільга перед поразкою у Vs., ефекти паніки, правило сірих (chrome) блоків від shock-панелей.
- (?) Онлайн у Planet Puzzle League.
