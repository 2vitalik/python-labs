---
title: Fibble
slug: fibble
aka: [fibble.xyz, «Wordle, що бреше»]
family: word-number
also: [hidden-deduction]
klass: puzzle
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: setup
  goal: state
year: 2022
platforms: [web]
links:
  - {kind: play, url: "https://fibble.xyz", best: true, note: "грати; довідка «Fibble rules», налаштування (Hard mode, лічильники брехні, розкладки), Daily/Unlimited, календар, статистика, Watch Mode — прочитано з JS-бандла сайту"}
  - {kind: other, url: "https://kotaku.com/wordle-today-games-like-alternatives-best-nerdle-heardl-1848782927/3", note: "Kotaku 2022: стартове слово з фідбеком + ще 8 спроб; в кожному рядку одна плитка бреше; шукати суперечності між рядками"}
  - {kind: other, url: "https://drchangliu.github.io/FibbleArena", note: "Fibble Arena: щоденний бенчмарк LLM на правилах Fibble (5 плиток, рівно одна брехня в рядку, 8 спроб)"}
  - {kind: other, url: "https://github.com/lynn/hello-wordl", note: "hello wordl — відкритий клон Wordle, форк якого лежить в основі коду Fibble"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fibble+wordle+lies+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [daily-puzzle, keyboard-controls, cell-click, word-validation, completion-detection, mode-select, puzzle-select, stats-window, streak-stats, profile-stats, share-result, save-progress, replay, replay-window, theme-select, event-effects, game-screen, help-window, settings-window, +letter-feedback, +lying-feedback, +lie-consistency-check, +lie-flag-marks, +keyboard-state, +hard-mode, +watch-others-solutions]
proposes: ["+effect:false_feedback", "+cond:mismatch_count", "+ui:on-screen-keyboard", "+ui:lie-flag", "+ui:true-lock", "+ui:lie-count", "+ui:color-totals", "+feature:hard-mode", "+feature:keyboard-layout", "+card:lying-feedback", "+card:lie-consistency-check", "+card:lie-flag-marks", "+card:watch-others-solutions"]
author: opus
date: 2026-11-09
---

# Fibble — Wordle, де в кожному рядку фідбеку рівно одна плитка бреше

## Суть
Це Wordle (`wordle.md`) на 5-літерне слово, але в кожному рядку відповіді рівно одна з п'яти кольорових плиток показує неправду. Яка саме — невідомо; гравець шукає слово, що узгоджується з усіма рядками «з точністю до однієї брехні на рядок». Перший рядок уже заповнено випадковим стартовим словом з фідбеком, далі — 8 власних спроб. Ядро — дедукція з шумом (як «20 питань з брехнею»): суперечності між рядками видають, де бреше гра. Автори — K & R Garfield, код — keldor (Kelly Dornhaus), на основі hello wordl.

## Поле і час
- Поле 9 рядків × 5 клітин: рядок 1 — стартове слово гри, рядки 2–9 — спроби гравця (`maxGuesses: 9`, у share — «k/8»).
- Праворуч від кожного рядка — колонка прапорця 🏴 і колонка лічильника брехні; під полем — екранна клавіатура + рядок трьох лічильників кольорів.
- Хід = одне підтверджене слово; часу нема.
- Сесія: Daily — задача на день, однакова для всіх («The lies are in the same positions for everyone»); Unlimited — нескінченні випадкові з номером; минулі дні — з календаря.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загадане слово | static (приховане) | 5 літер зі списку відповідей | фіксоване seed-ом дня |
| План брехні | static (прихований) | 9 пар {position 0–4, offset 1\|2} | заздалегідь для кожного рядка; однаковий для всіх гравців дня |
| Стартове слово | static | випадкове, < 5 спільних із відповіддю літер (green + yellow < 5) | рядок 1, уже з (брехливим) фідбеком |
| Плитка-літера | tile | літера, колір green/yellow/grey, прапорець, замок | колір = правда, крім однієї плитки рядка |
| Прапорець брехні 🏴 | mark | ≤ 1 на рядок | позначка гравця «тут бреше»; виключає плитку з підрахунку клавіатури |
| Замок «правда» | mark | будь-скільки | позначка гравця «тут точно правда»; клавіша літери отримує позначку |
| Клавіша клавіатури | tile (UI) | найкращий колір літери | за пріоритетом green > yellow > grey по всіх невідзначених прапорцем плитках |
| Словник | static | допустимі спроби (ширший за відповіді) | спроба поза ним відхиляється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «seed = номер дня (Unlimited — випадковий номер); обрати відповідь, стартове слово й 9 пар {позиція брехні, зсув 1|2}»`, `feedback(start_word)` у рядок 1.
- КОЛИ `input(letter)` → ЯКЩО `count(typed, <, 5)` → ТО `custom: «літера в наступну клітину активного рядка»`; `input(backspace)` — стерти останню.
- КОЛИ `input(enter)` → ЯКЩО `count(typed, <, 5)` → ТО `message("More letters, please.")`, `block`.
- КОЛИ `input(enter)` → ЯКЩО `custom: «це слово вже є серед спроб»` → ТО `message("You've already guessed that!")`, `block`.
- КОЛИ `input(enter)` → ЯКЩО `not in_dictionary(guess)` → ТО `message("That's not in the word list!")`, `block`.
- КОЛИ `input(enter)` → ЯКЩО `mode(hard)` and `custom: «для якогось попереднього рядка кількість розбіжностей ≠ 1»` → ТО `message("CRANE would have 2 lies.")`, `block` — спроба мусить «пояснювати» кожен рядок рівно однією брехнею.
- КОЛИ `input(enter)` → ЯКЩО слово валідне → ТО `feedback(guess)` (як у `wordle.md`: прохід green, потім yellow з лічильником залишку літер), потім `custom: «плитка на позиції брехні рядка зсуває колір на offset по циклу green → yellow → grey → green»` — брехня завжди інший колір, ніж правда.
- КОЛИ `custom: «спроба == відповідь»` → ТО `win`; переможний рядок показано без брехні (усі green), `animate(confetti)`; «епічна» анімація, якщо вгадано за ≤ 2 власні спроби.
- КОЛИ `counter(guesses, ==, 9)` → ЯКЩО не вгадано → ТО `lose`.
- КОЛИ `game_over` → ТО `reveal(lie_tiles)` — справжні позиції брехні підсвічуються в усіх рядках.
- КОЛИ `input(click tile)` → ЯКЩО рядок підтверджено і гра триває → ТО `mark(tile, flag)`; клік по іншій плитці рядка переносить прапорець, повторний — знімає (≤ 1 на рядок).
- КОЛИ `input(long-press | right click tile)` → ТО `mark(tile, true)` — «знаю, що правда»; КОЛИ `after(mark)` → ТО `custom: «клавіша літери отримує позначку замка»`.
- КОЛИ `after(feedback)` або `after(mark)` → ТО `paint(key[letter], max(color))` по всіх плитках, крім тих, що під прапорцем.
- КОЛИ `input(letter)` → ЯКЩО `mode(show_lie_counts)` → ТО `custom: «біля кожного попереднього рядка — скільки розбіжностей дав би поточний набір як відповідь»` (1 = узгоджено).
- КОЛИ `input(share)` → ТО `custom: «у буфер: Fibble #N k/8 [🔥🔥🔥, якщо кожна спроба мала рівно 1 брехню щодо всіх попередніх] [j/q🏴 — скільки з q прапорців влучили в брехню] + емодзі-сітка показаних кольорів»`.
- КОЛИ `game_over` → ТО `counter(played, +1)`; перемога — `counter(streak, +1)`, поразка або пропущений день — `counter(streak, =0)`.
- Перемога: ввести відповідь до 9-го рядка включно · Поразка: 8 власних спроб без вгадування · Рахунок: k/8 (номер спроби без стартового рядка) + бонусні значки 🔥 і точність прапорців.

## Керування і ввід
- Фізична клавіатура (літери, Backspace, Enter) або екранна; розкладки QWERTY / AZERTY / QWERTZ / Dvorak / Colemak, опція «"Enter" on left side».
- Клік по плитці підтвердженого рядка — прапорець 🏴 (підказка в правилах: «Use 🏴 to track which letters you think might be lies»); клік по 🏳️ у колонці рядка — зняти.
- Long-press / правий клік по плитці — замок «правда»; на клавіатурі такі літери позначено.

## Вікна, меню, HUD
- `game-screen`: заголовок з лого, перемикач Daily / Unlimited, іконки About · Settings · Stats · Calendar; поле 9×5 з колонками `lie-flag` і `lie-count`; рядок повідомлень (`toast`); `on-screen-keyboard` зі станами й замками; `color-totals` (скільки літер green / yellow / grey); після гри — Share, Watch Live (N), Watch Replay (N).
- `help-window` («About»): опис сімейства сайтів-варіантів (Xordle, Fibble, Double-Dabble, Warmle, Shuntle) + «Fibble rules» з поясненням кольорів, брехні й прапорців.
- `settings-window`: Dark theme · High-contrast colors · Show lie counts for current guess · 🔥 Hard mode (guesses must imply exactly one lie per prior clue) · Keyboard layout · "Enter" on left side · Live / Replays.
- `stats-window`: played · win % · streak · max streak · гістограма спроб 1–8 (рядок 9, якщо траплявся).
- `puzzle-select` (Calendar): місячний календар, кожен день з 🎲 (в процесі) / ✔️ / 💀 і мінісіткою емодзі; клік — відкрити задачу того дня.
- `replay-window` (Watch Mode): вступний модал «▶ Enable and watch»; банер «Watching Live» / «Replay — Player Won / Lost», чуже поле з прапорцями й клавіатурою, кнопки Next Live (N) · Next Replay (N) · Your Solution, підсумок «The answer was …».
- Переходи: `game-screen` ↔ About / Settings / Stats / Calendar (одна кнопка ❌ Close); кінець гри → Share або перегляд чужих розвʼязків.

## Фічі поза полем
- `mode-daily` + `mode-endless` (Unlimited з номером задачі в share), `puzzle-bank` через календар минулих днів.
- `autosave`: спроби, прапорці й замки дня — у localStorage за ключем дня; посилання `?save=` переносить збереження.
- `stats`, `streaks`, `share-result` (з 🔥 і точністю прапорців).
- `hard-mode` (опційне правило узгодженості), лічильники брехні як вбудована підказка (`hint`-подібне).
- `spectator` + `replay`: Live / Replays — дивитися чужі розвʼязки наживо або записом після власного; твій розвʼязок іде в спільний пул.
- `colorblind-palette` (High-contrast: ⬛🟦🟧 у share), `theme-select` (Dark), `keyboard-layout`.

## Варіації й родичі
- Wordle (`wordle.md`) — без брехні; Absurdle (`absurdle.md`) — гра «змінює» відповідь, а не бреше; Quordle (`quordle.md`) — кілька полів.
- Mastermind і Jotto (`../hidden-deduction/mastermind.md`, `../hidden-deduction/jotto.md`) — предки фідбеку.
- Сайти-родичі того ж кодера (з About): Xordle — дві відповіді на одному полі без спільних літер; Double-Dabble — кожна літера «привʼязана» до іншої; Warmle — жовтий означає «близько в цій позиції»; Shuntle — слово 4–7 літер, зсунуте пробілами.
- Fibble Arena — та сама гра як бенчмарк для LLM.
- **Осі варіацій:** кількість брехні в рядку (0 / рівно 1 / до k) · вид брехні (будь-який інший колір / лише сусідній за циклом) · чи бреше переможний рядок (тут ні) · чи план брехні однаковий для всіх (seed дня) · допомога гравцю (прапорці, замки, лічильники розбіжностей, hard mode).

## Цікавинки для курсу
- Брехня як зсув кольору по циклу на заздалегідь вибраній позиції — 🌱: одна функція поверх фідбеку Wordle, детермінована seed-ом.
- Лічильник розбіжностей «скільки брехні дав би кандидат для рядка» + hard mode «рівно 1 для кожного рядка» — 📎: перевірка гіпотези проти всієї історії.
- Розвʼязувач: фільтр кандидатів, де кожен рядок допускає рівно одну розбіжність (5 позицій × 2 кольори) — 🥈; вибір спроби з найбільшим очікуваним скороченням множини — 🥇.
- Прапорці й замки гравця, що змінюють похідну клавіатуру — 🌱.
- Share з «🔥🔥🔥» за повну узгодженість і точністю прапорців j/q — 🌱.
- Watch Live / Replay чужих розвʼязків тієї ж задачі — 🥈 (сервер, потік ходів, програвач).

## Мапа на каталог
- Є: `daily-puzzle` · `keyboard-controls` / `cell-click` ↔ ввід літер і прапорці · `word-validation` · `completion-detection` ↔ вгадане слово · `mode-select` ↔ Daily / Unlimited · `puzzle-select` ↔ календар минулих днів · `stats-window` / `streak-stats` / `profile-stats` · `share-result` · `save-progress` ↔ localStorage по днях · `replay` / `replay-window` ↔ Watch Mode · `theme-select` · `event-effects` ↔ конфеті, «juice» рядка · `game-screen` · `help-window` · `settings-window`.
- Вже запропоновано в інших файлах: `+letter-feedback`, `+keyboard-state`, `+hard-mode` (`wordle.md`).
- **Нема** → пропозиції карток:
  - `+lying-feedback` «Фідбек з рівно однією брехнею на рядок» · game-logic/constraints · 🌱 · слоти {lies_per_row: 1, shift: any|adjacent}.
  - `+lie-consistency-check` «Кількість розбіжностей кандидата з рядком; hard mode = рівно 1» · game-logic/constraints · 📎.
  - `+lie-flag-marks` «Прапорець брехні й замок правди, що впливають на похідну клавіатуру» · interface/input · 🌱.
  - `+watch-others-solutions` «Дивитися чужі розвʼязки тієї ж задачі live / replay» · interface/results · 🥈.

## Пропозиції до словників
- `+effect:false_feedback` — спотворити відгук однієї плитки рядка (зсув кольору на 1 або 2 по циклу); Fibble, варіанти Mastermind з брехнею.
- `+cond:mismatch_count` — скільки плиток рядка не збігаються з відгуком, який дав би кандидат як відповідь (hard mode, лічильник брехні).
- `+ui:on-screen-keyboard` — екранна клавіатура зі станами (див. `wordle.md`); `+ui:lie-flag` — прапорець 🏴 на плитці й у колонці рядка; `+ui:true-lock` — позначка «точно правда»; `+ui:lie-count` — число розбіжностей біля рядка; `+ui:color-totals` — лічильники літер кожного кольору під клавіатурою.
- `+feature:hard-mode` (див. `wordle.md`); `+feature:keyboard-layout` — вибір розкладки екранної клавіатури (QWERTY / AZERTY / Dvorak / Colemak).
- `+card:lying-feedback`, `+card:lie-consistency-check`, `+card:lie-flag-marks`, `+card:watch-others-solutions` — див. «Мапа на каталог».

## Джерела
- ⭐ [Fibble](https://fibble.xyz) — гра; з JS-бандла прочитано: правила («But there's one lie in every row!», «The lies are in the same positions for everyone»), генерація задачі (9 пар позиція/зсув, стартове слово), повідомлення, hard mode, налаштування, статистика, календар, share, Watch Mode.
- [Kotaku: ігри, схожі на Wordle](https://kotaku.com/wordle-today-games-like-alternatives-best-nerdle-heardl-1848782927/3) — опис Fibble, стартове слово + 8 спроб, порада шукати суперечності.
- [Fibble Arena](https://drchangliu.github.io/FibbleArena) — LLM-бенчмарк на правилах Fibble, легенда плиток (Correct / Wrong spot / Not in word / Lied tile).
- [hello wordl](https://github.com/lynn/hello-wordl) — база коду (посилання з About).
- YouTube: пошук «fibble wordle lies gameplay».

## Непевне
- (?) Рік — 2022 за статтею Kotaku; точної дати запуску не бачив.
- (?) «K & R Garfield» — так підписано в About; повні імена авторів не перевірено.
- (?) Розмір списків відповідей і допустимих спроб не рахував (у бандлі — великий словник різної довжини, відповіді — 5-літерні з початку списку).
- (?) Чи перший (стартовий) рядок теж має брехню — за кодом план брехні має 9 записів і застосовується до кожного рядка, включно з першим; на сайті цього словами не сказано.
- (?) Серія обнуляється за пропущений день — так рахує код статистики (непрограний день рве серію), але в UI не пояснено.
