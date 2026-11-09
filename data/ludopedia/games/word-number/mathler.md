---
title: Mathler
slug: mathler
aka: [Математлер, Mathler Easy, Mathler Hard, Mathler Extreme, Killer Mathler]
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
  - {kind: official, url: "https://www.mathler.com/", best: true, note: "грати щоденний Mathler; сторінка рендериться JS — правила видно лише в браузері"}
  - {kind: official, url: "https://www.mathler.com/easy", note: "Mathler Easy — Beginner Daily Math Puzzle"}
  - {kind: official, url: "https://www.mathler.com/hard", note: "Mathler Hard — Challenging Daily Math Puzzle"}
  - {kind: official, url: "https://www.mathler.com/killer", note: "Mathler Extreme — Ultimate Daily Math Puzzle"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mathler+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [daily-puzzle, keyboard-controls, cell-click, completion-detection, streak-stats, share-result, save-progress, stats-window, help-window, settings-window, mode-select, game-screen, end-screen, +letter-feedback, +keyboard-state, +equation-validation, +commutative-answers, +target-value-shown]
proposes: ["+cond:equals_target", "+effect:canonicalize"]
author: opus
date: 2026-11-09
---

# Mathler — Wordle над виразом з відомою відповіддю: знайди прихований вираз, що дає показане число

## Суть
Щодня загадано арифметичний вираз з 6 символів (цифри й `+ - * /`), а гравцеві **показано його результат** (напр. «= 42»). Кожна спроба — вираз тієї ж довжини, що дає саме це число; гра фарбує символи як у Wordle. На відміну від [nerdle](nerdle.md), знаку `=` у рядку нема, а права частина відома, тож спроба — не будь-яка рівність, а розвʼязок рівняння «вираз = ціль».

## Поле і час
- Поле — 6 рядків × 6 клітин (Normal) (?); над полем — ціль-число; під полем — екранна клавіатура з цифрами, операціями, Enter, Delete.
- Хід = підтверджена спроба. Нова задача раз на добу, однакова для всіх.
- Режими різняться довжиною виразу й складністю: Easy, Normal, Hard, Extreme/Killer (?) — розміри не перевірено.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ціль-число | static | значення | показане відкрито весь день |
| Прихований вираз | static (прихована) | 6 символів | дає ціль за порядком дій |
| Рядок спроби | zone | 6 клітин | активний до Enter, потім заморожений |
| Плитка-символ | tile | символ, стан empty/green/yellow/grey | фарбується при підтвердженні |
| Клавіша | tile (UI) | найкращий відомий стан | green > yellow > grey |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(symbol)` → ЯКЩО `custom: «рядок не заповнено»` → ТО `custom: «символ у наступну клітину»`.
- КОЛИ `input(enter)` → ЯКЩО `custom: «рядок неповний або вираз некоректний»` → ТО `message`, `shake`.
- КОЛИ `input(enter)` → ЯКЩО `custom: «значення виразу ≠ ціль»` (`+cond:equals_target`) → ТО `message` («вираз має дорівнювати цілі»), спроба не витрачається (?).
- Обчислення: `*` і `/` раніше за `+` і `-` (порядок дій) (?).
- КОЛИ `input(enter)` → ЯКЩО `custom: «значення виразу = ціль»` → ТО `feedback(guess)`: `paint(i, green)` — на місці, `paint(i, yellow)` — є деінде, `paint(i, grey)` — нема; дублікати — як у Wordle (?).
- КОЛИ `after(feedback)` → ТО `paint(key, max(state))`.
- КОЛИ `input(enter)` → ЯКЩО `custom: «спроба = відповідь з точністю до перестановки операндів»` → ТО `custom: «переписати спробу у форму відповіді»` (`+effect:canonicalize`), `win` — переставлені доданки/множники приймаються й переставляються на місце (?).
- КОЛИ `pattern(row all green)` → ТО `win`, `window(end-screen)`.
- КОЛИ `counter(guesses, ==, 6)` → ЯКЩО не вгадано → ТО `lose` (?).
- Перемога: усі символи зелені · Поразка: спроби скінчились · Рахунок: номер спроби, серія днів.

## Керування і ввід
- Фізична клавіатура (цифри, `+ - * /`, Backspace, Enter) або екранна клавіатура кліком/тапом.

## Вікна, меню, HUD
- `game-screen`: ціль-число, поле, `on-screen-keyboard` зі станами.
- `help-window` — правила з прикладом · `stats-window` — серія, розподіл спроб (?) · `settings-window` (?) · `end-screen` з кнопкою share.
- Перемикач режимів Easy / Normal / Hard / Extreme — окремі сторінки сайту (`mode-select`).

## Фічі поза полем
- `mode-daily` у кожному з 4 режимів; `streaks`, `stats`, `share-result` (емодзі-сітка) (?).

## Варіації й родичі
- [nerdle](nerdle.md) — рівність з `=` у рядку, ціль невідома; [wordle](wordle.md) — оригінальна оболонка; [nyt-digits](nyt-digits.md), [countdown-numbers](countdown-numbers.md), [krypto](krypto.md) — досягти числа з набору без прихованого стану; [crossmath](crossmath.md), [mathable](mathable.md) — рівності на полі.
- **Осі варіацій**: що відомо — ціль (Mathler) / нічого (Nerdle) · довжина за режимом · еквівалентність — точна / комутативна · фідбек — по символах / лише «більше-менше» (?).

## Цікавинки для курсу
- Перевірка спроби як рівняння «вираз = ціль» з порядком дій — 📎.
- Комутативна канонізація: переставлена відповідь приймається й переписується на правильні позиції — 🥈.
- Генератор щоденного виразу з «цікавим» результатом (ціле, без ділення з остачею (?)) — 🥉.
- Розвʼязувач: усі вирази довжини 6 з потрібним значенням, фільтр за відгуками, макс. ентропія — 🥇.

## Мапа на каталог
- Є: `daily-puzzle` · `keyboard-controls` · `cell-click` · `completion-detection` · `streak-stats` · `share-result` · `save-progress` · `stats-window` · `help-window` · `settings-window` · `mode-select` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+letter-feedback`, `+keyboard-state`, `+equation-validation`, `+commutative-answers` — уже в `wordle.md` / `nerdle.md`.
  - `+target-value-shown` «Відкрита ціль як підказка-обмеження спроби» · game-logic/constraints · 🌱.

## Пропозиції до словників
- `+cond:equals_target` — значення виразу дорівнює показаній цілі (Mathler; близько до Nerdle `equation_holds`).
- `+effect:canonicalize` — переписати еквівалентну спробу в канонічну форму відповіді.

## Джерела
- ⭐ [mathler.com](https://www.mathler.com/) — гра; правила на сторінці «How to play» у браузері (WebFetch бачить лише заголовок).
- [Mathler Easy](https://www.mathler.com/easy) · [Mathler Hard](https://www.mathler.com/hard) · [Mathler Extreme](https://www.mathler.com/killer) — існування режимів (заголовки сторінок).
- YouTube: пошук «mathler gameplay».

## Непевне
- (?) Усі конкретні правила (6 символів, 6 спроб, порядок дій, комутативні розвʼязки, кольори) — з брифа куратора й памʼяті; сайт рендериться JS і тексту правил не віддав. Wikipedia-статті нема.
- (?) Довжини виразу в Easy / Hard / Extreme; чи витрачається спроба на вираз з іншим значенням.
- (?) Автор і точна дата запуску (2022 — з черги).
