---
title: Mastermind (+ Bulls and Cows, «Бики й корови»)
slug: mastermind
family: hidden-deduction
also: [word-number]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: setup
  goal: state
year: 1970
platforms: [board (Invicta Plastics 1971–72), paper (Bulls and Cows), mainframe (MOO, Cambridge ~1970), Unix, handheld (Comp IV), PC, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mastermind_(board_game)", best: true, note: "правила, відгук з повторами, очки, алгоритм Кнута, варіанти, складність"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bulls_and_Cows", note: "паперовий предок: 4 різні цифри, бики/корови, MOO, ≤7 спроб, середнє 5.21"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wordle", note: "словесний нащадок: 5 літер, 6 спроб, зелений/жовтий/сірий, hard mode, daily"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=mastermind", note: "пошук BGG; видання й варіанти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mastermind+board+game+how+to+play", note: "пошук; правила"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=knuth+mastermind+algorithm+five+guesses", note: "пошук; пояснення алгоритму Кнута"}
stage: v1
coverage: 75
mechanics: [cell-click, hot-seat, ai-opponent, ai-minimax, level-solver, difficulty-levels, game-settings, custom-window, game-screen, end-screen, main-menu, settings-window, help-window, score-records, profile-stats, daily-puzzle, event-points, +code-feedback-pegs, +guess-row-board, +consistent-guess-filter, +knuth-minimax-solver, +hard-mode-reuse, +emoji-share-grid, +code-setter-role]
proposes: ["+cond:consistent", "+effect:feedback", "+effect:reveal", "+role:mark", "+ui:feedback-pegs", "+ui:color-palette", "+ui:guess-row", "+ui:keyboard-hints", "+window:code-setter", "+feature:hard-mode", "+feature:share-grid", "+feature:role-swap", "+card:code-feedback-pegs", "+card:guess-row-board", "+card:consistent-guess-filter", "+card:knuth-minimax-solver", "+card:hard-mode-reuse", "+card:emoji-share-grid", "+card:code-setter-role"]
author: opus
date: 2026-11-02
---

# Mastermind — вгадай прихований код кольорів за відгуком «точно / є, але не тут»

## Суть
Шифрувальник таємно ставить код із 4 кольорових кілочків (6 кольорів), зламувач робить спроби-рядки; на кожну отримує ключові кілочки: чорний (червоний) — колір на своєму місці, білий — колір є в коді, але на іншому місці. Мета — вгадати код за 8–12 спроб (залежить від дошки). Ядро — дедукція за агрегованим відгуком: незрозуміло, *який саме* кілочок «правильний», тому кожна спроба — питання, що ділить простір кодів. Предок — паперова «Бики й корови» з цифрами, нащадок — Wordle, де відгук стоїть *на кожній літері окремо*.

## Поле і час
- Дошка: N рядів-спроб (8/10/12) × 4 отвори + біля кожного ряду 4 малі отвори для ключових кілочків; під щитком — ряд коду.
- Шари: код (прихований до кінця) · спроби (видимі) · відгук (видимий, без привʼязки до позицій).
- Покроково: хід = одна повна спроба + відгук. Часу нема; у цифрових — інколи секундомір.
- Простір кодів: 6⁴ = 1296 (з повторами); Bulls and Cows: 10·9·8·7 = 5040 (усі цифри різні).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Секретний код | object | довжина 4, алфавіт 6 кольорів | прихований; повтори/порожні — за домовленістю |
| Кілочок коду (code peg) | piece | колір | ставиться в отвір поточного ряду |
| Ряд-спроба | mark | номер спроби | після подачі фіксується назавжди |
| Чорний/червоний ключ | mark | — | на кожну позицію з правильним кольором і місцем |
| Білий ключ | mark | — | на кожен колір, що є в коді, але не на місці (після вирахування чорних) |
| Порожній отвір (blank) | object | — | варіант: «порожньо» як сьомий колір |
| Щиток | static | — | ховає код до кінця раунду |
| Bulls and Cows: бик / корова | mark | — | бик = цифра на місці, корова = цифра є, не на місці |
| Wordle: клітинка-літера | mark | зелена / жовта / сіра | відгук на кожну позицію окремо |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО шифрувальник (людина або AI) задає код; `custom: «AI: випадковий код з алфавіту, з повторами чи без»`.
- КОЛИ `input(place_peg, slot, color)` → ЯКЩО слот у поточному ряду → ТО `set_value(slot, color)`.
- КОЛИ `input(submit)` → ЯКЩО ряд повний → ТО `custom: «відгук: black = Σ позицій, де guess[i]=code[i]; white = Σ_колір min(count_guess, count_code) − black»`, `mark(feedback_row)`; інакше `block`.
- Повтори: кожен кілочок коду дає не більше одного ключа (код RRBB, спроба RRRB → 3 чорних, 0 білих; про другий B не сказано).
- КОЛИ `custom: «black = довжина коду»` → ТО `win`, `reveal(code)`.
- КОЛИ `counter(guesses, ==, rows)` → ЯКЩО не вгадано → ТО `lose`, `reveal(code)`.
- Очки (настолка): шифрувальник отримує `score(+1)` за кожну спробу зламувача і `score(+1)` додатково, якщо код не вгадано; ролі міняються, грають парну кількість раундів, перемагає більший рахунок.
- Bulls and Cows: обидва гравці мають свої коди й ходять почергово; КОЛИ один вгадав → ТО `win` (хто перший).
- Wordle: КОЛИ `input(submit)` → ЯКЩО `not custom: «слово є в словнику»` → ТО `block`, `shake`; відгук — позиційний: зелений/жовтий/сірий; зайві копії літери — сірі, якщо в слові їх менше.
- Wordle hard mode: КОЛИ `input(submit)` → ЯКЩО `not custom: «спроба містить усі зелені на місцях і всі жовті»` → ТО `block`.
- «Послідовний» (consistent) режим / hard mode загалом: спроба мусить бути сумісною з усіма попередніми відгуками.
- Перемога: вгадати код до кінця рядів · Поразка: ряди скінчились · Рахунок: кількість спроб (менше — краще).

## Керування і ввід
- Настолка: рука ставить кілочки; шифрувальник виставляє ключові кілочки (чесність — на ньому; помилка у відгуку ламає гру).
- Цифрова версія: палітра кольорів унизу → клік по слоту поточного ряду (або drag кольору в слот); «Перевірити» подає ряд; клік по поставленому кілочку — прибрати.
- Bulls and Cows / Wordle: ввід з клавіатури (цифри / літери), Backspace, Enter; екранна клавіатура з підсвіткою використаних символів.
- Режим ролей: у цифровій грі людина може бути шифрувальником — тоді вона задає код, а AI ламає й показує хід думок.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Грати (я ламаю) · Я загадую (AI ламає) · Удвох → `settings-window` (довжина коду, кількість кольорів, повтори, порожні, кількість рядів) · Правила → `help-window`.
- `code-setter` (кандидат): вибір секретного коду під щитком для hotseat або режиму «AI ламає».
- `game-screen`: `guess-row` × N зверху вниз (або знизу вгору, як на дошці), біля кожного `feedback-pegs` 2×2; `color-palette`; `check-button`; `turn-counter` «спроба 4/10»; щиток з кодом.
- Wordle: сітка 6×5 з анімацією перевертання плиток, `keyboard-hints` (екранна клавіатура з кольорами), `toast` «Not in word list».
- `end-screen`: розкритий код, кількість спроб, кнопки «Ще раз» / «Поділитися» (Wordle: `share-grid` з емодзі-квадратів без літер).
- `stats-window` (Wordle): зіграно, % перемог, серія, гістограма «за скільки спроб».
- Переходи: main-menu → (code-setter) → game-screen → end-screen → main-menu / нова гра.

## Фічі поза полем
- `custom-difficulty`: довжина коду (3–5), кольори (6–8, Super Mastermind — 8×5), повтори так/ні, порожні так/ні, рядів 8–12.
- `ai-opponent-levels` у ролі зламувача: випадковий сумісний код → мінімакс Кнута → оптимальний за середнім (≈4.34 спроби).
- `hint`: показати, скільки кодів ще сумісні з відгуками; «наступна найкраща спроба».
- `mode-daily` + `streaks` + `share-code`-подібний `share-grid` (Wordle); `stats`; `hotseat` з обміном ролей (`role-swap`).
- Bulls and Cows на мейнфреймах (MOO) вела `leaderboard-local` — захист цієї таблиці став кейсом комп'ютерної безпеки.

## Варіації й родичі
- Bulls and Cows (паперова, можливо ~100 років): 4 різні цифри, бики/корови, хто перший; MOO (Frank King, Cambridge, до літа 1970) → Multics (MIT 1972) → Unix; Comp IV (Milton Bradley) — ручний компʼютер на FOCAL-версії.
- Видання Mastermind: Bagels (3 цифри з 10), Super (8 кольорів × 5), Royale / Grand (5 кольорів × 5 форм, 3/4 отвори), Word Mastermind (лише справжні слова з 4 літер), Mini (6 спроб), Number Mastermind (цифри + опційна підказка суми).
- Словесна лінія: Jotto (лише кількість спільних літер), Lingo (телешоу), Wordle (2021, Josh Wardle; позиційний відгук, словник, daily, емодзі-шер) → Absurdle (адверсарний, див. Kaboom) (?).
- **Осі варіацій**: відгук «агрегований (Mastermind) / позиційний (Wordle) / лише кількість спільних (Jotto)»; алфавіт «кольори / цифри / літери зі словником»; повтори «так / ні»; спроби «вільні / мусять бути сумісні (hard mode)»; шифрувальник «людина / випадковий / адверсарний (код не фіксований, обирає найгірший сумісний)».

## Цікавинки для курсу
- Функція відгуку black/white з повторами (`min(count)` по кольорах) — 🌱 сама, 📎 з тестами на крайні випадки (RRBB vs RRRB).
- Сітка рядів-спроб з палітрою й ключовими кілочками 2×2 — 📎 (UI, який легко зробити і в консолі, і в GUI).
- Фільтр сумісних кодів («лишилось 37 можливих») + підказка — 🥉.
- Алгоритм Кнута: мінімакс по 1296 кодах, старт 1122, ≤5 спроб — 🥇 (класичний перебір з оцінкою найгіршого розбиття).
- Режим «я загадую — AI ламає» з показом ходу думок — 🥈.
- Wordle-обгортка: словник, позиційний відгук, hard mode, daily за датою, емодзі-шер — 🥉.
- Адверсарний шифрувальник (код обирається пізніше як найгірший сумісний) — 🥇, місток до Kaboom.

## Мапа на каталог
- Є: `cell-click` (слот/палітра) · `hot-seat` · `ai-opponent` + `ai-minimax` (Кнут) · `level-solver` (зламувач) · `difficulty-levels` + `game-settings` · `daily-puzzle` (Wordle) · `score-records` + `profile-stats` · `event-points` (очки шифрувальника) · `game-screen` / `end-screen` / `main-menu` / `settings-window` / `help-window` · `custom-window` (code-setter).
- **Нема** → пропозиції карток:
  - `+code-feedback-pegs` «Відгук на код: точні / неточні» · game-logic/constraints · 📎 · слот {feedback: aggregate|positional|common-count}.
  - `+guess-row-board` «Дошка рядів-спроб» · interface/render · 📎 · слоти {rows, length}.
  - `+consistent-guess-filter` «Фільтр сумісних кандидатів» · levels/solvability · 🥉.
  - `+knuth-minimax-solver` «Мінімакс-зламувач коду» · game-logic/opponent · 🥇 (дитина `ai-opponent`).
  - `+hard-mode-reuse` «Спроба мусить використати відкрите» · game-logic/constraints · 📎.
  - `+emoji-share-grid` «Шер результату емодзі» · interface/results · 🌱.
  - `+code-setter-role` «Обмін ролей загадує/вгадує» · game-logic/opponent · 📎.

## Пропозиції до словників
- `+cond:consistent` — спроба сумісна з усіма попередніми відгуками (hard mode, фільтр кандидатів).
- `+effect:feedback` — видати відгук на спробу (кількість точних/неточних або колір позицій); не `message`, бо це дані для дедукції.
- `+effect:reveal` — ⏳, тут: відкрити код у кінці.
- `+role:mark` — ключові кілочки, плитки Wordle.
- `+ui:feedback-pegs` — блок ключів 2×2 біля ряду; `+ui:color-palette` — вибір кольору для слота; `+ui:guess-row` — ряд-спроба; `+ui:keyboard-hints` — екранна клавіатура з кольорами відгуку.
- `+window:code-setter` — екран загадування коду.
- `+feature:hard-mode` — сумісні спроби обовʼязкові; `+feature:share-grid` — шер результату без спойлера; `+feature:role-swap` — обмін ролями між раундами.

## Джерела
- ⭐ [Wikipedia: Mastermind (board game)](https://en.wikipedia.org/wiki/Mastermind_(board_game)) — Meirowitz 1970, 6×4, відгук з повторами, очки шифрувальника, Кнут (1122, ≤5), Koyama–Lai 4.34, NP-повнота, таблиця варіантів.
- [Wikipedia: Bulls and Cows](https://en.wikipedia.org/wiki/Bulls_and_Cows) — правила, MOO/Multics/Unix, Comp IV, ≤7 спроб, середнє 5.21.
- [Wikipedia: Wordle](https://en.wikipedia.org/wiki/Wordle) — правила, повтори літер, hard mode, daily, емодзі-шер, звʼязок з Mastermind/Jotto/Lingo.
- [BGG пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=mastermind) — видання.
- YouTube: пошук «mastermind board game how to play», «knuth mastermind algorithm five guesses».

## Непевне
- (?) Absurdle як адверсарний Wordle — з памʼяті, не перевірено.
- (?) Кількість рядів у конкретних виданнях (8/10/12) — Wikipedia дає лише діапазон.
- (?) Чи у класичній настолці колір ключа «black» чи «red» — залежить від видання; Wikipedia: «red (or black)».
