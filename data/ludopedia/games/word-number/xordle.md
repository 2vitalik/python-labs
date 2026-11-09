---
title: Xordle
slug: xordle
aka: [xordle.org, xordle.xyz, «Wordle на два слова»]
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
  - {kind: play, url: "https://xordle.org/", best: true, note: "грати; правила «Xordle Rules!», налаштування, режими Daily/Unlimited/Custom, Calendar, Stats, Gallery, Create — прочитано з JS-бандла сайту (xordle.xyz → 301 на xordle.org)"}
  - {kind: other, url: "https://www.hey.gg/blog/xordle", note: "огляд: два слова без спільних літер, кожна підказка правдива рівно для одного, тематичні відповіді, безкоштовна стартова підказка, календар і unlimited, автор Kelly Dornhaus"}
  - {kind: other, url: "https://playpile.gg/games/xordle", note: "каталог: daily з оновленням раз на 24 год + unlimited, видавець Keldor"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=xordle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [daily-puzzle, keyboard-controls, cell-click, word-validation, completion-detection, mode-select, puzzle-select, stats-window, streak-stats, profile-stats, share-result, save-progress, replay, replay-window, theme-select, controls-remap, in-game-editor, level-exchange, state-string, event-effects, game-screen, help-window, settings-window, about-window, +letter-feedback, +keyboard-state, +hard-mode, +watch-others-solutions, +challenge-link, +dual-target-merged-feedback, +disjoint-answers, +crossover-letter, +bonus-guess-on-last, +feedback-switch-after-solve]
proposes: ["+cond:disjoint", "+effect:merge_feedback", "+trigger:target_found", "+ui:on-screen-keyboard", "+ui:theme-badge", "+ui:status-line", "+window:gallery-window", "+window:create-puzzle", "+feature:hard-mode", "+feature:challenge-link", "+feature:history-export-code", "+card:dual-target-merged-feedback", "+card:disjoint-answers", "+card:crossover-letter", "+card:bonus-guess-on-last", "+card:feedback-switch-after-solve"]
author: opus
date: 2026-11-09
---

# Xordle — Wordle на два загадані слова без спільних літер на одному полі: кожна кольорова підказка правдива лише для одного з них

## Суть
Загадано два 5-літерні слова, які не мають жодної спільної літери. Кожна спроба порівнюється з обома, і на плитку лягає «краща» з двох оцінок: зелена, якщо зелена хоч в одному слові, жовта — якщо жовта хоч в одному, сіра — якщо літери нема в жодному. Оскільки літери не перетинаються, кожен колір стосується рівно одного слова — але якого, гра не каже. Перший рядок уже заповнено стартовим словом-підказкою, далі 8 власних спроб; знайшов одне слово — фідбек перемикається на звичайний Wordle для другого. Автор — keldor (Kelly Dornhaus), той самий, що зробив [fibble.md](fibble.md).

## Поле і час
- Поле 9 рядків × 5 клітин: рядок 1 — стартове слово гри з фідбеком, рядки 2–9 — спроби гравця (`maxGuesses: 9`); якщо на 9-му рядку вгадано перше слово — зʼявляється 10-й, бонусний.
- У Custom-пазлі стартових слів може бути до 7, довжиною 5–9 літер (рядки з «зайвими» літерами).
- Під полем — екранна клавіатура зі станами літер.
- Хід = одне підтверджене слово; часу нема. Сесія: Daily — «Day N» від 1 квітня 2022, однакова для всіх; Unlimited — нескінченні випадкові; Custom — пазл за посиланням.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Відповідь A, відповідь B | static (приховані) | 5 літер, без спільних літер | фіксовані на пазл; часто повʼязані темою дня |
| Crossover-пара (✨) | static (приховані) | рівно одна спільна літера на тій самій позиції | особливий пазл; ця літера — «crossover» із золотою рамкою |
| Стартове слово | static | 1 слово (Custom — до 7, 5–9 літер) | рядок 1 з фідбеком; однакове для всіх |
| Рядок спроби | zone | 5 клітин | Editing → LockedIn; після підтвердження заморожений |
| Плитка-літера | tile | absent / elsewhere / correct / crossover | колір — максимум з оцінок проти A і B |
| Клавіша клавіатури | tile (UI) | найкращий відомий стан | фарбується максимумом зі всіх рядків |
| Словник | static | список допустимих слів | спроба поза ним відхиляється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `custom: «рядок 1 = стартове слово з фідбеком проти обох відповідей»`.
- КОЛИ `level_start` → ЯКЩО `mode(hard)` → ТО `custom: «стартову підказку відкривати по одній літері за кожну з перших 5 спроб»`.
- КОЛИ `input(letter)` → ЯКЩО `count(typed, <, 5)` → ТО `custom: «літера в наступну клітину активного рядка»`.
- КОЛИ `input(enter)` → ЯКЩО `count(typed, <, 5)` → ТО `message("Type more letters")`.
- КОЛИ `input(enter)` → ЯКЩО `custom: «слово вже вводилось»` → ТО `message("You've already guessed that")`.
- КОЛИ `input(enter)` → ЯКЩО `not in_dictionary(guess)` → ТО `message("That's not in the word list")`; спроба не витрачається.
- КОЛИ `input(enter)` → ЯКЩО слово валідне → ТО `feedback(guess)` окремо проти A і проти B (за правилом Wordle з дублікатами), далі `custom: «на кожну позицію: зелений, якщо зелений хоч в одному; інакше жовтий, якщо жовтий хоч в одному; інакше сірий»`.
- КОЛИ `input(enter)` → ЯКЩО `mode(crossover)` і `custom: «позиція зелена в обох словах»` → ТО `custom: «плитка crossover із золотою рамкою та підказкою "appears in the same position in both words"»`.
- КОЛИ `after(feedback)` → ТО `paint(key, best state)` для кожної літери спроби — клавіша бере найкращий стан з усіх рядків.
- КОЛИ `after(feedback)` → ЯКЩО `custom: «усі 5 плиток зелені, але слово не є відповіддю»` → ТО `animate(huh)` — 5 зелених ≠ перемога, бо зелені беруться з двох слів.
- КОЛИ `custom: «спроба = одна з відповідей»` → ТО `message("You got X, one more to go.")`, `custom: «рядки після неї отримують звичайний Wordle-фідбек лише проти другої відповіді»`.
- КОЛИ `counter(rows, ==, 9)` → ЯКЩО `custom: «9-та спроба відгадала першу відповідь»` → ТО `message("Last chance! Do a bonus guess.")`, `extra_move`.
- КОЛИ `custom: «обидві відповіді введено»` → ТО `win`, `window(stats-window)`.
- КОЛИ `counter(rows, >=, 9)` → ЯКЩО `custom: «відгадано менше двох відповідей і бонусу нема»` → ТО `lose`.
- Unlimited: КОЛИ `level_start` → ЯКЩО `custom: «пазл зі списку "instant" — з першого рядка лишився єдиний розвʼязок»` → ТО `message("You found an instant puzzle #k of n!")` (також «hidden nightmare puzzle»).
- Перемога: обидва слова за ≤ 8 власних спроб (+1 бонусна) · Поразка: спроби вичерпано · Рахунок: кількість рядків до перемоги (гістограма), серія днів.
- КОЛИ `game_over` → ТО `counter(streak, +1)` при перемозі, інакше `counter(streak, =0)`.

## Керування і ввід
- Фізична клавіатура (літери, Backspace, Enter) або тап по екранній; Ctrl/Cmd-комбінації ігноруються.
- Налаштування розкладки: QWERTY, AZERTY та інші; «Enter» ліворуч.
- Курсора по клітинах нема: введення завжди в наступну клітину активного рядка.

## Вікна, меню, HUD
- `game-screen`: «Day N» (стрілки «на день назад/вперед»), значки 🎲 (нетематичний пазл) і ✨ (crossover), поле 9×5, `status-line` («Two words remain.» / «You got X, one more to go.»), `on-screen-keyboard` зі станами, посилання «Share» (challenge link), у Unlimited — «+New» і «+New (Hard Mode)».
- Меню у правому верхньому куті: About → `about-window` · Settings → `settings-window` · Stats → `stats-window` · Calendar → `puzzle-select` · Gallery → `gallery-window` · ✏️ Create → `create-puzzle`.
- `about-window` / `help-window` («Xordle Rules!»): правила, кольори, crossover-пазли, пісня-відео з правилами, подання своїх пазлів через форму, перенос історії (Export Code / Import Code).
- `settings-window`: High-contrast colors · Keyboard layout · «Enter» on left side · Hard mode!!! · Live / Replays.
- `stats-window`: games · Win % · Streak · Max Streak · гістограма кількості рядків.
- `puzzle-select` (Calendar): минулі щоденні пазли з позначками пройдено / hard mode «!!!».
- `gallery-window`: AI-зображення до тематичних щоденних пазлів.
- `replay-window` (Watch Mode): «Watching Live (k of n)» / «Replay — Player Won/Lost» — чужі розвʼязки цього пазла.
- `create-puzzle` (Create): дві відповіді, до 7 стартових слів, підказка ≤ 80 символів, валідація («The two answer words must not share any letters», «Starter words must all be different», попередження про слова поза словником), посилання-виклик.
- Переходи: вхід → `game-screen` (Daily) → кінець гри → `stats-window`; Calendar → обраний день → `game-screen`; Create → посилання → `game-screen` (Custom).

## Фічі поза полем
- `mode-daily` (тематичні щоденні, часто від користувачів — з підписом автора), `mode-endless` (Unlimited), Custom за посиланням (`challenge-link`, стан пазла в base64-рядку URL).
- `hard-mode`: стартова підказка відкривається поступово; результат позначено «!!!» у share і календарі.
- `share-result`: емодзі-сітка ⬛🟨🟩 (high contrast — ⬛🟦🟧); crossover-плитки показуються як зелені.
- `streaks`, `stats`, `autosave` стану кожного дня; `export-import` історії кодом між пристроями.
- `colorblind-palette` (High-contrast), `remap-controls` (розкладки), `spectator`/`replay` (Watch Mode з опт-аутом), `level-editor` (Create), `level-sharing` (подання пазлів).
- Нема: undo, підказок, таймера.

## Варіації й родичі
- [wordle.md](wordle.md) — одне слово, 6 спроб; [quordle.md](quordle.md) — 4 слова на **окремих** полях однією спробою; Xordle — 2 слова на **одному** полі зі злитим фідбеком.
- [fibble.md](fibble.md) — той самий автор і рушій: одна брехня на рядок; родичі з About Fibble: Warmle, Double-Dabble, Shuntle; [absurdle.md](absurdle.md) — адверсарна відповідь.
- Crossover-пазли (✨) — підваріант: рівно одна спільна літера на одній позиції.
- **Осі варіацій:** кількість відповідей (1 / 2 на одному полі / 4–8 на окремих) · злиття фідбеку (максимум / сума / по полях) · звʼязок відповідей (без спільних літер / одна спільна позиція / тема) · старт (порожньо / стартове слово / кілька стартових) · що після першої знахідки (злитий фідбек лишається / перемикання на друге слово).

## Цікавинки для курсу
- Злитий фідбек: два Wordle-порівняння з дублікатами + максимум по позиції — 🌱; валідатор пари «без спільних літер» / «рівно одна спільна позиція» — 🌱.
- Перемикання фідбеку після першої знахідки й перерахунок клавіатури — 📎.
- Розвʼязувач: множина кандидатів — **пари** слів (A, B) без спільних літер, сумісні з усіма злитими рядками; лічильник лишених розвʼязків («instant puzzle» = 1 після стартового рядка) — 🥈.
- Редактор пазла з валідацією й кодуванням стану в URL (base64 JSON) — 📎.
- Watch Mode: запис спроб і програвання чужих розвʼязків наживо/повтором — 🥉 (потрібен сервер).
- Hard mode «підказка по літері за спробу» — 🌱.

## Мапа на каталог
- Є: `daily-puzzle` · `keyboard-controls` · `cell-click` ↔ екранна клавіатура · `word-validation` · `completion-detection` ↔ обидва слова введено · `mode-select` ↔ Daily/Unlimited/Custom · `puzzle-select` ↔ Calendar · `stats-window` + `streak-stats` + `profile-stats` · `share-result` · `save-progress` · `replay` + `replay-window` ↔ Watch Mode · `theme-select` ↔ high contrast · `controls-remap` ↔ розкладки · `in-game-editor` ↔ Create · `level-exchange` ↔ посилання й подання пазлів · `state-string` ↔ пазл у base64-рядку · `event-effects` ↔ «juice»-анімації рядків · `game-screen` · `help-window` · `settings-window` · `about-window`.
- **Нема** → пропозиції карток:
  - `+letter-feedback`, `+keyboard-state`, `+hard-mode`, `+watch-others-solutions`, `+challenge-link` — є в корпусі (Wordle, Fibble, Crosswordle).
  - `+dual-target-merged-feedback` «Одна спроба проти двох відповідей, фідбек — максимум по позиції» · game-logic/constraints · 🌱.
  - `+disjoint-answers` «Відповіді без спільних літер — підказка належить рівно одній» · levels/generation · 🌱.
  - `+crossover-letter` «Рівно одна спільна літера на позиції, окремий колір» · game-logic/constraints · 🌱.
  - `+bonus-guess-on-last` «Знахідка на останній спробі дає бонусну» · game-logic/win · 🌱.
  - `+feedback-switch-after-solve` «Після першої відповіді фідбек — лише проти другої» · game-logic/constraints · 📎.

## Пропозиції до словників
- `+cond:disjoint` — дві множини (літери слів) не перетинаються.
- `+effect:merge_feedback` — злити кілька оцінок однієї спроби в одну (максимум по позиції).
- `+trigger:target_found` — знайдено одну з кількох відповідей (Xordle, Quordle).
- `+ui:on-screen-keyboard` — екранна клавіатура зі станами; `+ui:theme-badge` — значки 🎲/✨ біля номера дня; `+ui:status-line` — рядок «скільки слів лишилось».
- `+window:gallery-window` — галерея зображень до пазлів; `+window:create-puzzle` — редактор власного пазла з валідацією.
- `+feature:hard-mode`, `+feature:challenge-link`, `+feature:history-export-code` — перенос статистики кодом.
- `+card:dual-target-merged-feedback`, `+card:disjoint-answers`, `+card:crossover-letter`, `+card:bonus-guess-on-last`, `+card:feedback-switch-after-solve`.

## Джерела
- ⭐ [Xordle](https://xordle.org/) — гра; з JS-бандла прочитано: правила («There are two secret words. They share no letters in common. You get 8 tries…»), функцію злиття фідбеку, crossover, `maxGuesses: 9`, бонусну спробу, повідомлення, налаштування, режими, Stats, Calendar, Gallery, Create з валідацією, Watch Mode, export/import, старт Day 1 = 2022-04-01.
- [hey.gg: Xordle](https://www.hey.gg/blog/xordle) — опис правил, тематичні відповіді, безкоштовна стартова підказка, календар і unlimited, AI-зображення, автор.
- [PlayPile: Xordle](https://playpile.gg/games/xordle) — daily + unlimited, видавець Keldor.
- YouTube: пошук «xordle gameplay».

## Непевне
- (?) Чи під клавіатурою показано лічильники кольорів (у коді рахуються absent/elsewhere/correct) — як у Fibble; інтерфейсу наживо не бачив.
- (?) Як саме стилізуються літери знайденого слова після першої знахідки («-fin»-класи) — з коду, без скриншота.
- (?) Рік 2022 — з дати Day 1 у коді (1 квітня 2022); статті hey.gg/PlayPile датовані 2023.
- (?) Повний перелік розкладок клавіатури (видно QWERTY і AZERTY) і точний вигляд Calendar/Gallery — не перевірено.
