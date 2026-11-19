---
title: Dave's Word Game
slug: daves-word-game
aka: [DWG]
family: word-number
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: both
  goal: score
year: 2025
platforms: [iOS, Android, PC, macOS, Linux]
links:
  - {kind: other, url: "https://www.electrondance.com/?p=18599", best: true, note: "Electron Dance, Puzzleworks 12: очко за літеру, поповнення лише після порожнього ряду / стовпця / 3×3, бонуси, стратегія"}
  - {kind: steam, url: "https://store.steampowered.com/app/3670940/Daves_Word_Game/", note: "ПК-версія 23.06.2026: Daily, Endless, Puzzle, Timed, денний і місячний лідерборди; знімки поля 5×5"}
  - {kind: official, url: "https://playdwg.com/", note: "посилання на App Store і Google Play"}
  - {kind: itch, url: "https://bearwaves.itch.io/daves-word-game", note: "ввід (клавіатура, миша, геймпад, тач), інтерактивний туторіал, режим однієї кнопки"}
  - {kind: other, url: "https://apps.apple.com/app/daves-word-game/id6739985012", note: "iOS: щоденне поле безкоштовно, Premium-режими, паки пазлів MOVIES і GAMES"}
  - {kind: other, url: "https://steamcommunity.com/app/3670940/discussions/0/570415959124246250/", note: "розробник: у Puzzle таймера нема, мета — повне очищення одним махом"}
  - {kind: other, url: "https://steamcommunity.com/stats/3670940/achievements", note: "досягнення: бонус-очки за слово, слова з 15+ літер, тематичні слова, вітер в Endless"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Dave%27s+Word+Game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [word-validation, cell-click, multi-select, event-points, daily-puzzle, leaderboard, share-result, mode-select, time-out, puzzle-select, achievements-window, game-screen, end-screen, settings-window, tutorial-window, +line-clear, +all-clear-bonus, +clear-all-goal, +monthly-reset-leaderboard, +word-from-anywhere, +box-clear-3x3, +clear-triggers-refill, +daily-unlimited-retries, +theme-word-solution]
proposes: ["+trigger:region_emptied", "+effect:refill", "+ui:word-preview", "+feature:daily-attempts", "+feature:monthly-leaderboard", "+feature:one-button-mode"]
author: opus
date: 2026-11-19
---

# Dave's Word Game — щоденне поле 5×5: слова з будь-яких літер, порожні ряди, стовпці й квадрати 3×3 дають бонус і нові літери

## Суть
Щоденна словесна гра Bearwaves: усім дається те саме поле 5×5 з літерами. Слово складається з літер будь-де на полі (суміжність не потрібна), вжиті літери зникають, кожна дає очко. Нові літери приходять лише тоді, коли спорожніє цілий ряд, стовпець або будь-який квадрат 3×3 — це ще й бонус; тому головне рішення — коли і що чистити, щоб не «замкнути» собі кращі слова. Поле можна переграти скільки завгодно разів за день; найкращий результат іде в денний і місячний лідерборди.

## Поле і час
- Сітка 5×5 (знімки Steam); клітина — плитка-літера або порожня.
- Порожні ряди, стовпці й квадрати 3×3 рахуються в будь-якому положенні: порожній 4×4 містить чотири квадрати 3×3, і кожен дає бонус.
- Хід = одне слово; Daily, Endless і Puzzle — без часу; Timed — на годинник.
- Над полем — лічильник зі смугою, що зменшується з ходом гри (на знімках 8 → 4 → 1); що він рахує — (?).
- Endless: декоративна вертушка й лічильник «N words»; досягнення «тримати вітер хвилину» натякає на темп у цьому режимі (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка-літера | tile | літера | вибирається будь-де на полі; після слова зникає |
| Порожня клітина | terrain | — | лишається після вжитої літери; заповнюється лише поповненням |
| Ряд / стовпець | zone | 5 клітин | спорожнів → бонус і нові літери |
| Квадрат 3×3 | zone | будь-яке з 9 положень | спорожнів → бонус; квадрати перекриваються |
| Слово в рядку вводу | mark | вибрані літери | × — скинути, ▷ / ✓ — подати |
| Тематичне слово (Puzzle) | mark | тема паку | слово з розвʼязку пазла |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap tile)` → ТО `custom: «літера додається в кінець слова; суміжність не потрібна»`.
- КОЛИ `input(submit)` → ЯКЩО `in_dictionary(word)` → ТО `disappear(вжиті плитки)`, `score(+1 за літеру)`; інакше `block` (?).
- КОЛИ `custom: «ряд, стовпець або квадрат 3×3 спорожнів»` → ТО `score(+bonus)` за кожну таку ділянку, `custom: «ділянка поповнюється новими літерами»`.
- Без очищення поповнення нема: поле лише порожніє.
- КОЛИ `all_gone(tile)` → ТО `score(+bonus)` (повне очищення).
- Puzzle: КОЛИ `all_gone(tile)` → ТО `win`; рано очищений ряд поповнюється й заважає, тож ряди й стовпці треба чистити всі разом.
- Timed: КОЛИ `counter(time_left, ==, 0)` → ТО `game_over`.
- КОЛИ `game_over` (Daily) → ТО `window(end-screen)`, `custom: «результат іде в денний і місячний лідерборд; поле можна переграти»`.
- Перемога: нема (рекорд дня) / повне очищення в Puzzle · Поразка: нема · Рахунок: очко за літеру + бонуси за порожні ряди, стовпці, квадрати 3×3 і все поле; у лідерборді — результати близько 200.

## Керування і ввід
- Тап / клік по літерах у потрібному порядку; кнопка ✓ / ▷ — подати, × — скинути набране.
- ПК: миша, геймпад (повна підтримка, Steam Deck); набір з клавіатури в червні 2026 не працював — лише клік по кожній літері (тред Steam).
- Доступність: інтерактивний туторіал, режим «однієї кнопки» (itch).

## Вікна, меню, HUD
- `game-screen`: «DWG», шестерня налаштувань, меню ☰; великий рахунок ліворуч зі спливними «+4», «+6» (`popup-text`); над полем — лічильник зі смугою (`progress-bar`); поле 5×5; рядок вводу слова з × і ▷; праворуч — бонсай (Daily) або вертушка (Endless) як індикатор (?); в Endless — «N words».
- `mode-select`: Daily (безкоштовно) · Endless · Puzzle · Timed (Premium, кнопка «unlock all»).
- `puzzle-select`: категорії-паки (MOVIES, GAMES, віршові форми …), позначка «ідеально» за пазл.
- `end-screen` з кнопкою «поділитися рахунком»; `leaderboard` денний і місячний.
- `settings-window`, `tutorial-window` (інтерактивний), `achievements-window` (Steam, Game Center); світла й темна тема (знімки).

## Фічі поза полем
- `mode-daily` (те саме поле для всіх, безкоштовно, без реклами) + необмежені спроби за день; `leaderboard-online` денний і місячний.
- `mode-endless` (1.1.0), `mode-puzzle` і `mode-time-attack` (Timed) (1.2.0), паки пазлів MOVIES (1.3.0) і GAMES (1.4.0, про студії ігор).
- `share-result`, `achievements` (34 на Steam), `cloud-save`, `gamepad-support`, `tutorial`.
- Premium ($4.99 на iOS) відкриває режими; на ПК гра платна з безкоштовним демо.

## Варіації й родичі
- Корпус: Letterpress (`letterpress.md` — літери будь-де на полі 5×5), Wordle (`wordle.md` — щоденність і лідерборд), Wordatro (`wordatro.md` — слово з руки за очки), SpellTower (`spelltower.md` — чистити поле словами), Scrabble (`scrabble.md`).
- Поза сімʼєю: блок-пазли «ряд / стовпець / квадрат 3×3» (1010!, Woodoku) і блоки судоку — те саме очищення, але тут ділянка має стати порожньою, а не повною.
- **Осі варіацій:** вибір літер (будь-де / суміжний шлях) · що дає бонус (повний ряд / порожній ряд / квадрат 3×3 / усе поле) · коли поповнення (після кожного слова / лише після очищення / ніколи) · сесія (щоденна / нескінченна / пазл / на час).

## Цікавинки для курсу
- Перевірка після ходу: порожні ряди, стовпці й усі 9 вікон 3×3 (ковзне вікно) — 🌱.
- Поповнення лише за очищення як «ручка» темпу: коли оновити поле — 📎.
- Щоденне поле з фіксованим seed, необмежені спроби, денний і місячний лідерборди — 🥉.
- «Прибиральник»: слово-анаграма з усіх літер, що лишились (пошук мультимножини в словнику) — 🥉; перебір найкращого порядку слів для рекорду дня — 🥇.
- Puzzle: повне очищення з тематичними словами, рано очищене поповнюється — 📎.

## Мапа на каталог
- Є: `word-validation` · `cell-click` + `multi-select` ↔ вибір літер · `event-points` ↔ очко за літеру · `daily-puzzle` · `leaderboard` · `share-result` · `mode-select` · `time-out` ↔ Timed · `puzzle-select` ↔ паки Puzzle · `achievements-window` · `game-screen` · `end-screen` · `settings-window` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - Уже в корпусі: `+line-clear` (тут слот lines: rows+cols+boxes, але ділянка «порожня», а не «повна»), `+all-clear-bonus`, `+clear-all-goal` (Puzzle), `+monthly-reset-leaderboard`.
  - `+word-from-anywhere` «Слово з літер будь-де на полі» · game-logic/constraints · 🌱.
  - `+box-clear-3x3` «Порожній квадрат 3×3 у будь-якому положенні — бонус» · game-logic/score · 🌱.
  - `+clear-triggers-refill` «Нові літери лише після очищення ділянки» · entities/spawn · 📎.
  - `+daily-unlimited-retries` «Щоденне поле: спроби без ліміту, у таблицю — найкраща» · interface/results · 🌱.
  - `+theme-word-solution` «Пазл із тематичними словами розвʼязку» · levels/bank · 🌱.

## Пропозиції до словників
- `+trigger:region_emptied` — ряд / стовпець / квадрат спорожнів (дзеркало `pattern(row_full)`).
- `+effect:refill` — ділянка поповнюється новими плитками.
- `+ui:word-preview` — рядок вводу слова з × і ▷.
- `+feature:daily-attempts` — скільки разів можна грати щоденне поле (тут без ліміту).
- `+feature:monthly-leaderboard` — таблиця, що скидається щомісяця.
- `+feature:one-button-mode` — гра однією кнопкою (доступність).

## Джерела
- ⭐ [Electron Dance: Puzzleworks 12](https://www.electrondance.com/?p=18599) — правила від гравця-критика: очко за літеру, поповнення лише після порожнього ряду / стовпця / 3×3, бонус, перекриття квадратів у 4×4, повторні спроби; коментар розробника про словник.
- [Steam: Dave's Word Game](https://store.steampowered.com/app/3670940/Daves_Word_Game/) — опис, режими, лідерборди; 5 знімків (поле 5×5, вибір несуміжних літер REAL і EMU, бонуси «+3», «+6», Endless з вертушкою).
- [App Store](https://apps.apple.com/app/daves-word-game/id6739985012) — історія версій (1.0.0 — 24.11.2025, Endless, Puzzle, Timed, паки).
- [itch.io](https://bearwaves.itch.io/daves-word-game) — ввід і доступність.
- [Steam: тред про Puzzle](https://steamcommunity.com/app/3670940/discussions/0/570415959124246250/) — без таймера, мета — повне очищення.
- [Steam: досягнення](https://steamcommunity.com/stats/3670940/achievements) — бонус-очки за слово (9 / 21 / 84), слова з 15+ літер, тема, вітер.
- [PocketGamer: анонс](https://www.pocketgamer.com/daves-word-game/coming-soon) — мобільний реліз 15.12.2025, «формуєш поле».
- YouTube: пошук «Dave's Word Game gameplay».

## Непевне
- (?) Чим закінчується щоденна гра (нема слів / ліміт слів / рішення гравця); лічильник зі смугою над полем — можливо, запас поповнень чи ходів.
- (?) Скільки очок дає кожне очищення (на знімках «+3» на ряду, «+6» у квадраті 3×3, сума «+9»).
- (?) Мінімальна довжина слова; чи штрафується неправильне слово.
- (?) Звідки нові літери (випадкові чи наперед задані для всіх у Daily).
- (?) Досягнення «Twenty's Plenty — найменший можливий рахунок у Daily» і «вітер» в Endless — правила за ними не знайдено.
- (?) Рік: мобільний реліз — грудень 2025 (PocketGamer; App Store 1.0.0 — 24.11.2025), ПК — 23.06.2026; черга пише 2026.
- PlayPile описує «4×4, 10 спроб, 60 секунд» — схоже на згенерований текст, суперечить знімкам; не враховано.
