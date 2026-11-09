---
title: Squabble
slug: squabble
aka: [Squabble Royale, Squabble Blitz, «Wordle battle royale»]
family: word-number
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: realtime
  opponent: online
  info: hidden
  random: runtime
  goal: survive
year: 2022
platforms: [web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Squabble_(video_game)", best: true, note: "Ottomated, 2 лютого 2022; Blitz 2–5 і Royale 6–99 гравців; HP тане щосекунди; правильні літери б'ють суперника й лікують; replay; без денного ліміту"}
  - {kind: play, url: "https://squabble.me/", note: "грати; з JS прочитано How to Play, режими (Blitz, Royale, Solo: Daily / Random), лобі з кодом, READY, налаштування, екран кінця, програвач replay"}
  - {kind: other, url: "https://www.engadget.com/wordle-multiplayer-battle-royale-182452666.html", note: "Engadget 2022: виліт за 0 HP або коли закінчились спроби; розвʼязувати кілька слів поспіль; приватне лобі з друзями; replay усіх спроб"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=squabble+wordle+battle+royale+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [online-multiplayer, simultaneous-versus, hp-damage, word-validation, keyboard-controls, cell-click, mode-select, lobby-window, replay, replay-window, share-result, daily-puzzle, theme-select, event-effects, main-menu, game-screen, end-screen, help-window, settings-window, +letter-feedback, +keyboard-state, +hp-drain-clock, +word-as-attack, +player-elimination, +last-standing-round, +spectate-after-death, +lobby-code, +ready-word-check, +streamer-mode]
proposes: ["+effect:eliminate", "+trigger:last_standing", "+ui:on-screen-keyboard", "+ui:placement-indicator", "+ui:lobby-code", "+feature:streamer-mode", "+feature:ready-check", "+card:hp-drain-clock", "+card:lobby-code", "+card:ready-word-check", "+card:streamer-mode"]
author: opus
date: 2026-11-09
---

# Squabble — Wordle як battle royale: HP тане щосекунди, вгадані літери лікують тебе й б'ють інших

## Суть
Онлайн-гра на 2–99 гравців у реальному часі: кожен розвʼязує на своєму полі Wordle (`wordle.md`) — 5 літер, 6 спроб, — а потім наступне слово, і так до кінця матчу. Здоровʼя кожного гравця падає на 1 щосекунди; влучні спроби лікують і завдають шкоди супернику, промахи шкодять тобі. Хто дійшов до 0 HP або вичерпав спроби — вибуває; останній живий перемагає. Ядро — Wordle, де швидкість набору важить не менше за дедукцію, а результат кожної спроби — це атака.

## Поле і час
- Своє поле Wordle `wordLength × totalGuesses` (5 × 6) по центру; ліворуч і праворуч — мініатюри полів суперників (сітка кольорів спроб) з HP-барами.
- Real-time: тік HP — щосекунди; спроби надходять асинхронно від усіх гравців.
- Матч = кілька слів поспіль для кожного гравця, доки не лишиться один.
- Лобі: гравці «готуються» в окремій фазі; гра стартує за спільним відліком.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | HP, maxHp, місце, статус Unready / Ready / у грі / вибув | HP −1 щосекунди; надлишок понад maxHp показано щитом (?) |
| Суперник | enemy | HP, поле спроб | так само розвʼязує свої слова; його влучання шкодять тобі |
| Поле гравця | zone | 5 × 6 | рядок = спроба; розвʼязав — нове слово |
| Загадане слово | static (приховане) | 5 літер | своє на кожному кроці матчу (?) |
| Плитка-літера | tile | green / yellow / grey | як у Wordle |
| Лобі | container | код гри (shortCode), приватне / публічне, ліміт гравців | збирає гравців до старту |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(type "READY" + enter)` → ЯКЩО `state(me, unready)` → ТО `set_state(me, ready)`; поки набираєш, літери «READY» фарбуються як Wordle-спроба проти слова ready.
- КОЛИ `custom: «лобі готове»` → ТО `timer(start, countdown)`, потім `game_start` — великий відлік секунд на екрані.
- КОЛИ `timer(1 s)` → ЯКЩО `state(me, alive)` → ТО `hp(me, −1)` («You take 1 damage every second»).
- КОЛИ `input(enter)` → ЯКЩО `count(typed, <, 5)` → ТО `block` (клавіша Enter неактивна, сіра).
- КОЛИ `input(enter)` → ЯКЩО `in_dictionary(guess)` → ТО `feedback(guess)` (як у `wordle.md`).
- КОЛИ `after(feedback)` → ЯКЩО `custom: «є правильні літери (green / yellow)»` → ТО `heal(me, n)`, `damage(opponent, n)` — розмір і вибір цілі не опубліковано (?).
- КОЛИ `after(feedback)` → ЯКЩО `custom: «спроба хибна»` → ТО `hp(me, −n)` («guess wrong and take damage») (?).
- КОЛИ `custom: «рядок усіх green»` → ТО `custom: «нове загадане слово, поле очищено»` — розвʼязувати поспіль, доки не лишиться один.
- КОЛИ `counter(guesses, ==, 6)` → ЯКЩО не розвʼязано → ТО `custom: «вибування»` (Engadget: «run out of guesses»).
- КОЛИ `hp_zero(me)` → ТО `custom: «вибування; місце = кількість живих на цей момент»`.
- КОЛИ `custom: «HP упало більше, ніж на щосекундну втрату»` → ТО `shake(board)` — видно, що тебе вдарили.
- КОЛИ `custom: «лишився один живий»` → ТО `win` для нього, `window(end-screen)` для всіх.
- КОЛИ `input(join code)` → ЯКЩО `custom: «гра вже почалась / заповнена / ти вже в іншому браузері»` → ТО `message("The game has already started." | "The game is full." | "You are already connected in another browser.")`.
- Перемога: останній живий (Blitz / Royale) · Поразка: 0 HP або 6 спроб без розвʼязку · Рахунок: місце в матчі.

## Керування і ввід
- Фізична клавіатура: літери, Backspace, Enter (фокус постійно повертається на приховане поле вводу); або екранна QWERTY.
- Мобільних нема: «Mobile support is not here yet! Try playing on a bigger screen.»
- Ворожі поля лише спостерігаються; прямої дії «атакувати когось» у UI не видно (?).

## Вікна, меню, HUD
- `main-menu`: лого Squabble (BETA), GUEST / імʼя, How to Play, Settings; режими Blitz · Squabble Royale · Squabble Solo (Daily / Random); Create Game · JOIN GAME (поле коду) · Find Game; акаунт: Sign up / login / Change Username / Log Out.
- `help-window` (How to Play): 6 рядків правил — останній живий, шкода/лікування, 1 HP за секунду, кольори, кількість гравців у режимах.
- `settings-window`: Streamer Mode · Dark Mode · Colorblind Mode.
- `lobby-window`: «Waiting for other players...», `lobby-code` (Click to Copy → Copied!; у приватній грі код прихований зірочками (?)), рядок «Type "READY" to start», `timer-countdown` (великий відлік до старту).
- `game-screen`: своє поле з `placement-indicator` («#N — 42 HP»), `hp-bar` (+ `shield-bar` для надлишку (?)), `opponent-boards` ліворуч і праворуч, `on-screen-keyboard` зі станами.
- `end-screen` («Game Over»): місце, Copy Results → «Results Copied», Share to Twitter, WATCH REPLAY, SPECTATE, REMATCH, BACK TO HOME.
- `replay-window`: перегляд матчу з HP і полями всіх; кнопки Skip to the Beginning · −5 s · Play / Pause · +5 s · швидкість 0.5× / 1× / 2× / 5×.
- Переходи: `main-menu` → Create / Join / Find → `lobby-window` → READY → відлік → `game-screen` → вибув → SPECTATE або `end-screen` → Replay / Rematch / Home.

## Фічі поза полем
- `online-multiplayer` через WebSocket: публічний підбір (Find Game), приватне лобі за кодом (`invite-link`-подібне), «Reconnecting...» при обриві.
- `mode-versus` (Blitz 2–5, Royale 6–99) і соло-режим (`mode-daily` / випадкове слово).
- `spectator` після вибування, `replay` будь-якого матчу з програвачем.
- `share-result` (копія результату + Twitter); без денного ліміту ігор (Wikipedia).
- `streamer-mode` (?) — для трансляцій; `colorblind-palette`, `theme-select` (Dark Mode); акаунти з імʼям.

## Варіації й родичі
- Wordle (`wordle.md`) — одиночне ядро; Quordle (`quordle.md`) — кілька слів одночасно, без суперника.
- Babble Royale (`babble-royale.md`) — battle royale на дошці Scrabble; Tetris 99 / `simultaneous-versus` — той самий принцип «кожен на своєму полі, шкода іншим»; Pac-Man 99 (`../maze-arcade/pac-man-battle-royale.md`).
- Fibble (`fibble.md`), Absurdle (`absurdle.md`) — інші ускладнення Wordle, без суперника.
- **Осі варіацій:** звідки тиск (годинник HP / ліміт спроб / обидва) · що є атакою (green / yellow / розвʼязане слово) · вибір цілі (випадкова / лідер / найслабший) · кількість гравців (2–5 / до 99) · зміна слова (одне на всіх / свій ланцюг).

## Цікавинки для курсу
- HP як годинник: −1 щосекунди, лікування за влучання, надлишок як щит — 🌱.
- Обмін ударами між N полями Wordle на сервері (кого бити, скільки, черга подій) — 🥈.
- Лобі з кодом, фаза READY і спільний відлік старту — 📎.
- Набір «READY» як Wordle-спроба з живою підсвіткою — 🌱 (той самий фідбек як мікро-туторіал).
- Мініатюри 98 чужих полів на canvas + тряска свого поля при ударі — 📎.
- Replay матчу з програвачем (−5 s / +5 s / швидкість) — 🥉.

## Мапа на каталог
- Є: `online-multiplayer` · `simultaneous-versus` ↔ кожен на своєму полі, перемога виживанням · `hp-damage` ↔ HP, шкода й лікування · `word-validation` · `keyboard-controls` / `cell-click` · `mode-select` ↔ Blitz / Royale / Solo · `lobby-window` · `replay` / `replay-window` · `share-result` · `daily-puzzle` ↔ Solo Daily · `theme-select` ↔ Dark Mode · `event-effects` ↔ тряска поля · `main-menu` · `game-screen` · `end-screen` · `help-window` · `settings-window`.
- Вже запропоновано: `+letter-feedback`, `+keyboard-state` (`wordle.md`); `+word-as-attack`, `+player-elimination`, `+last-standing-round`, `+spectate-after-death` (`babble-royale.md`).
- **Нема** → пропозиції карток:
  - `+hp-drain-clock` «HP тане щотіку, влучні дії лікують» · entities/state · 🌱 · слоти {drain: 1/s, heal: n}.
  - `+lobby-code` «Приватне лобі за коротким кодом» · game-logic/opponent · 📎.
  - `+ready-word-check` «Готовність — набрати слово READY» · interface/menus · 🌱.
  - `+streamer-mode` «Режим стрімера: приховати коди й особисте» · interface/settings · 🌱.

## Пропозиції до словників
- `+effect:eliminate` — гравець вибуває з матчу, решта грає далі (див. `babble-royale.md`).
- `+trigger:last_standing` — лишився один живий гравець.
- `+ui:on-screen-keyboard` (див. `wordle.md`); `+ui:placement-indicator` — поточне місце «#N» (див. `babble-royale.md`); `+ui:lobby-code` — код лобі з копіюванням.
- `+feature:streamer-mode` — приховати чутливе для трансляції; `+feature:ready-check` — гра стартує, коли гравці підтвердили готовність.
- `+card:hp-drain-clock`, `+card:lobby-code`, `+card:ready-word-check`, `+card:streamer-mode` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Squabble (video game)](https://en.wikipedia.org/wiki/Squabble_(video_game)) — розробник Ottomated, 2022, режими й кількість гравців, HP, шкода/лікування, replay, рецепція.
- [Squabble](https://squabble.me/) — гра; з JS: How to Play («You take 1 damage every second, and heal damage when you guess right»), меню, лобі, READY, налаштування, екран кінця, програвач.
- [Engadget, 2022](https://www.engadget.com/wordle-multiplayer-battle-royale-182452666.html) — виліт за HP або спробами, кілька слів поспіль, приватні лобі, replay.
- YouTube: пошук «squabble wordle battle royale gameplay».

## Непевне
- (?) Скільки HP дає / знімає green і yellow, скільки шкоди за хибну спробу й кому саме йде удар (випадковий суперник, усі, лідер) — у клієнті не видно, логіка на сервері.
- (?) Стартове HP / maxHp і чи надлишок HP справді «щит» — у коді HP-бар має окремий колір для hp > maxHp.
- (?) Чи всі гравці отримують однакові слова в тому самому порядку.
- (?) Що саме ховає Streamer Mode (у приватному лобі код показано зірочками — імовірно, це).
- (?) Чи гра досі повноцінно працює онлайн: сторінка відкривається (BETA), але матч не перевірено.
