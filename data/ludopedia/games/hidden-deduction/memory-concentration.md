---
title: Memory / Concentration / Pairs («Мемо», «Знайди пару»)
slug: memory-concentration
family: hidden-deduction
also: [board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: collect
year: 1959
platforms: [cards (Concentration, Pelmanism), board (Ravensburger Memory, 1959), TV (Concentration, NBC 1958–1991), PC, web, mobile, PS4/PS5 (Ravensburger, 2022–2023)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Concentration_(card_game)", best: true, note: "правила, варіанти (Zebra, One Flip, Spaghetti, Pexeso), соло-рахунок, оптимальна стратегія, ≈41.6 ходу"}
  - {kind: wiki, url: "https://de.wikipedia.org/wiki/Memory_(Spiel)", note: "Ravensburger Memory 1959, 33 пари, турнірні правила, торгова марка, цифрові версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Concentration_(game_show)", note: "телегра: дошка 30/25, приз за пару, wild card, TAKE/Forfeit, ребус під картками"}
  - {kind: other, url: "https://arxiv.org/abs/2103.08264", note: "Chazottes et al.: Concentration як фізична модель (спін-фліп динаміка)"}
  - {kind: other, url: "https://doi.org/10.4169%2Famer.math.monthly.120.09.787", note: "Velleman & Warrington: What to Expect in a Game of Memory"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=memory+pairs", note: "пошук; цифрові версії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=memory+matching+pairs+game+tutorial+code", note: "пошук; приклади реалізації"}
stage: v1
coverage: 85
mechanics: [cell-click, hover-highlight, completion-detection, collect-all, difficulty-levels, field-size-picker, theme-select, game-settings, score-records, leaderboard, profile-stats, hot-seat, turn-enforcement, ai-opponent, ai-random, mode-indicator, goal-counter, status-panel, event-effects, sound-effects, game-screen, main-menu, end-screen, settings-window, +pair-flip-match, +flip-back-delay, +input-lock, +extra-turn-on-success, +shuffle-unmatched, +ai-forgetful-memory, +card-sets, +special-cards]
proposes: ["+trigger:delay", "+effect:flip", "+ui:pairs-found", "+feature:card-sets", "+axis:info-asymmetry", "+card:pair-flip-match", "+card:flip-back-delay", "+card:input-lock", "+card:extra-turn-on-success", "+card:shuffle-unmatched", "+card:ai-forgetful-memory", "+card:special-cards"]
author: opus
date: 2026-11-02
---

# Memory — сітка карт сорочкою догори: відкрий дві, запамʼятай, збери всі пари

## Суть
Карти розкладено сіткою сорочкою догори, кожен малюнок трапляється рівно двічі. Хід — відкрити дві карти: однакові лишаються відкритими (або забираються), різні — через мить перевертаються назад. Мета — зібрати всі пари за найменше ходів/часу (соло) або більше пар, ніж суперники (по черзі). Мінімальна гра з прихованою інформацією: приховано **від усіх однаково**, дедукції нема — лише памʼять і порядок відкриття; через це — ідеальний перший «hidden»-проєкт.

## Поле і час
- Прямокутна сітка W×H з парною кількістю клітин (типово 4×4, 4×5, 6×6, 8×8 — Pexeso 64 карти; колода 52 = 4×13); варіанти «Spaghetti» — карти розкидано довільно, «Fancy» — коло, трикутник, ромб.
- Шар клітини: малюнок (прихований) + стан `down / up / matched` (+ «порожньо», якщо пари забирають).
- Покроково: хід = 2 відкриття; між другим відкриттям і перевертанням — пауза показу (цифрова версія, ≈0.5–1.5 с) (?). Соло — таймер, що йде від першого кліку.
- Інформація: усе приховане однаково від усіх гравців — суперник бачить те саме, що й ти.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта закрита | tile | малюнок (прихований), пара-id | клік → відкривається |
| Карта відкрита (вибрана) | tile | 1-ша або 2-га у ході | чекає другу; після показу — matched або назад down |
| Знайдена пара | tile / mark | власник (у мультиплеєрі) | лишається відкритою або зникає з поля |
| Джокер (варіант Any Color) | tile | — | у варіанті з джокерами пара джокерів рахується подвійно |
| Спецкартки (телегра) | tile | Wild Card · Take · Forfeit | wild — пара до будь-якої; take/forfeit — забрати/віддати приз |
| Ребус під дошкою (телегра) | zone | — | кожна знайдена пара відкриває шматок картинки-загадки |

## Правила (КОЛИ → ЯКЩО → ТО)
- Підготовка: `custom: «N/2 малюнків × 2, перемішати, розкласти»` (Fisher–Yates).
- КОЛИ `input(flip, c)` → ЯКЩО `state(c, down)` і `counter(open, <, 2)` і не `state(board, locked)` → ТО `reveal(c)`, `counter(open, +1)`; інакше `block` (клік по відкритій/знайденій — ігнор).
- КОЛИ `counter(open, ==, 2)` → ЯКЩО `same(c1, c2, picture)` → ТО `set_state(c1, c2, matched)`, `counter(pairs_found, +1)`, `extra_move` (класика: «wins the pair and plays again»).
- КОЛИ `counter(open, ==, 2)` → ЯКЩО не `same` → ТО `set_state(board, locked)`; `delay(t)` → `hide(c1, c2)`, `clear_state(board, locked)`, `pass_turn`; соло — `counter(misses, +1)`.
- Варіант: клік деінде під час показу — одразу `hide` (пропустити паузу) (?).
- Варіант One Flip: знайшов пару — забираєш, але хід переходить далі (без `extra_move`).
- Варіант Zebra: пара = той самий ранг, протилежний колір; Two Decks: пара = ідентичні карти; MemoCards: трійки замість пар.
- Варіант «карти рухаються» (деякі компʼютерні версії): КОЛИ `after(mismatch)` → ТО `swap`/перемішати частину закритих карт — памʼять частково знецінюється.
- КОЛИ `all_gone(down)` → ТО `win` (соло) / `custom: «перемагає той, у кого більше пар; нічия можлива»`.
- Рахунок соло: кількість ходів (або промахів) і час; оптимальна гра з ідеальною памʼяттю — ≈0.8·n ходів (52 карти → ≈41.6).
- Телегра Concentration: знайдена пара дає приз і відкриває частину ребуса; розгадав ребус — виграв накопичене.

## Керування і ввід
- Лише клік/тап по карті; клавіатура — стрілки + Enter по курсору (доступність) (?).
- Під час паузи показу ввід заблоковано (`input-lock`) — інакше гравець відкриє 3-тю карту і зламає стан.
- Hotseat: гравці клацають по черзі на одному екрані; завіса не потрібна — нічого приватного нема.

## Вікна, меню, HUD
- `main-menu`: Грати · Складність · Тема карт · Рекорди · Налаштування.
- `difficulty-select` / `settings-window`: розмір сітки (4×4 / 6×6 / 8×8), кількість гравців, AI-суперник і його «памʼять», час показу, тема.
- `game-screen`: сітка карт; HUD — `move-counter` (ходи або промахи), `timer-elapsed`, `pairs-found` (знайдено x / N), `turn-indicator` і рахунок пар кожного гравця (мультиплеєр); `restart-button`.
- `end-screen`: «Усі пари знайдено» — ходи, час, зірки/оцінка, новий рекорд? → Ще раз / Меню.
- `leaderboard` (найкращі за розміром сітки), `stats-window` (ігри, середні ходи) — у мобільних версіях (?).
- Переходи: main-menu → (difficulty) → game-screen → end-screen → game-screen / main-menu.

## Фічі поза полем
- `difficulty-presets` = розмір сітки (і час показу), `custom-difficulty`, `card-sets` (тематичні колоди малюнків: Ravensburger — тематичні набори; цифрові «Pairs» — вибір набору карток), `theme-select`.
- `stats`, `leaderboard-local`, `stars-rating` (за ходи відносно оптимуму).
- `hotseat`, `ai-opponent-levels` (AI з обмеженою памʼяттю), `mode-time-attack` (відлік).
- Ravensburger: тематичні набори, «Zeitreise Memory» (старе↔нове як пара); відеогра для PS4/PS5 (2022–2023).

## Варіації й родичі
- Концентрація картами (52 або 54 з джокерами), Pexeso (64 квадратні картки 8×8), Pelmanism; Ravensburger Memory (William Hurter, 1959; базовий набір 33 пари).
- Телегра Concentration (NBC 1958–1973, Classic Concentration 1987–1991): пари-призи, спецкарти, ребус.
- Родичі: Simon (запамʼятати послідовність), «Shell game», Minesweeper (приховане однаково від усіх, але з підказками), Wordle (відкриття з відгуком).
- **Осі варіацій**: що таке пара «однаковий малюнок / ранг+колір / протилежний колір / трійка»; після пари «ходиш ще / хід далі»; знайдене «лишається / зникає»; закрите «стоїть / перемішується»; гравці «соло на ходи/час / по черзі на пари / проти AI».

## Цікавинки для курсу
- Машина станів ходу: idle → one open → two open (locked) → resolve — 🌱; з таймером паузи без блокування UI (after/timer) — 📎.
- Блокування вводу під час анімації — класична помилка студентів (3-тя карта) — 🌱, але повчально.
- AI із «забудькуватою» памʼяттю: памʼятає кожну побачену карту з імовірністю p або лише K останніх — 📎; оптимальна стратегія (спершу невідома карта, потім вирішувати, чи відкривати відому) — 🥈.
- Перемішування закритих карт після промаху — 🌱.
- Генерація поля довільної форми (Fancy: коло/ромб) з парною кількістю клітин — 📎.
- Порахувати очікувану кількість ходів симуляцією і порівняти з формулою ≈0.8·n — 🥉.

## Мапа на каталог
- Є: `cell-click` + `hover-highlight` · `completion-detection` + `collect-all` · `difficulty-levels` + `field-size-picker` + `game-settings` · `theme-select` · `score-records` + `leaderboard` + `profile-stats` · `hot-seat` + `turn-enforcement` · `ai-opponent` / `ai-random` · `mode-indicator` (чий хід) · `goal-counter` (пар лишилось) · `status-panel` · `event-effects` (переворот карти) · `sound-effects` · `game-screen` / `main-menu` / `end-screen` / `settings-window`.
- **Нема** → пропозиції карток:
  - `+pair-flip-match` «Відкрий дві — однакові лишаються» · entities/interact · 🌱 · слот {group: 2|3, rule: same|zebra}.
  - `+flip-back-delay` «Показ промаху і переворот назад за таймером» · game-logic/turn · 🌱 · слот {delay_ms}.
  - `+input-lock` «Блокування вводу під час анімації/резолву» · interface/input · 🌱.
  - `+extra-turn-on-success` «Успіх — ще хід» · game-logic/opponent · 🌱.
  - `+shuffle-unmatched` «Перемішування закритих після промаху» · levels/generation · 🌱.
  - `+ai-forgetful-memory` «AI з обмеженою памʼяттю» · game-logic/opponent · 📎 · слот {p_remember | k_last}.
  - `+card-sets` «Набори малюнків» · interface/settings · 🌱 (близько до `theme-select`, але змінює сам вміст пар).
  - `+special-cards` «Спецкартки: wild / take / forfeit» · entities/interact · 📎.

## Пропозиції до словників
- `+trigger:delay(t)` — одноразова затримка після події (відмінно від `timer(every)`, що повторюється).
- `+effect:flip` — перевернути карту: пара `reveal`/`hide` в одному ефекті з анімацією.
- `+ui:pairs-found` — «знайдено x / N» і по гравцях.
- `+feature:card-sets` — набори малюнків (змінює вміст пар, а не лише вигляд).
- `+axis:info-asymmetry` — див. Geister; тут `everyone` (приховано від усіх однаково, тому hotseat без завіси).
- Вжито наявні ⏳/🔥 без пропозицій: `same`, `extra_move`, `tile`, `move-counter`, `timer-elapsed`, `difficulty-select`, `stars-rating`.

## Джерела
- ⭐ [Wikipedia: Concentration (card game)](https://en.wikipedia.org/wiki/Concentration_(card_game)) — розкладка, хід, пара → ще хід, варіанти (Any Color, One Flip, Zebra, Two Decks, Spaghetti, Pexeso), соло-рахунок, стратегія, ≈41.6 ходу.
- [Wikipedia DE: Memory (Spiel)](https://de.wikipedia.org/wiki/Memory_(Spiel)) — Ravensburger 1959, William Hurter, 33 пари, турніри (32 пари), цифрові «Pairs» на секундомір і ходи, PS4/PS5.
- [Wikipedia: Concentration (game show)](https://en.wikipedia.org/wiki/Concentration_(game_show)) — дошка 30/25, спецкарти, ребус.
- [Velleman & Warrington (2013)](https://doi.org/10.4169%2Famer.math.monthly.120.09.787) · [Chazottes et al. (arXiv)](https://arxiv.org/abs/2103.08264) — математика гри (лінки з Wikipedia).
- Steam / YouTube — пошукові лінки.

## Непевне
- (?) Типова пауза показу (0.5–1.5 с) і «клік — пропустити паузу» — з досвіду цифрових версій, не з джерела.
- (?) Розміри сіток цифрових пресетів (4×4/6×6/8×8) — типові, не з конкретної гри.
- (?) Наявність `leaderboard`/`stats-window` — загальна практика мобільних версій, конкретну гру не перевірено.
- (?) Рік: 1959 — Ravensburger Memory; картковий Concentration старший, точна дата невідома.
