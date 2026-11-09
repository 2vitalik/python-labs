---
title: Nerdle
slug: nerdle
aka: [Nerdle Classic, Нердл]
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
platforms: [web, mobile]
links:
  - {kind: official, url: "https://www.nerdlegame.com/games/classic-nerdle.html", best: true, note: "повні правила Classic: 8 символів, 6 спроб, порядок дій, комутативність, дублікати"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nerdle", note: "автор Richard Mann, січень 2022, кольори green/purple/grey"}
  - {kind: official, url: "https://www.nerdlegame.com/", note: "грати; список режимів micro…maxi, bi/quad/octo, speed, instant"}
  - {kind: other, url: "https://www.nerdlegame.com/faqs.html", note: "FAQ: символи, «=» один, праворуч лише число, нулі, відʼємні, streak vs straight, Pro"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=nerdle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [daily-puzzle, keyboard-controls, cell-click, completion-detection, settings-window, help-window, game-screen, end-screen, stats-window, mode-select, streak-stats, share-result, save-progress, time-out, +letter-feedback, +keyboard-state, +equation-validation, +commutative-answers, +multi-board, +puzzle-creator, +instant-one-guess]
proposes: ["+cond:equation_holds", "+cond:commutative_match", "+ui:on-screen-keyboard", "+feature:commutative-answers", "+feature:puzzle-creator", "+feature:mode-instant", "+feature:multi-board", "+feature:local-reset-time"]
author: opus
date: 2026-11-09
---

# Nerdle — Wordle над рівняннями: вгадай 8-символьну правильну рівність за 6 спроб

## Суть
Загадано рівність з 8 символів (`0–9 + - * / =`), наприклад `10+20=30`. Кожна спроба мусить бути **математично правильною** рівністю тієї ж довжини; гра фарбує символи: зелений — на місці, фіолетовий — є, але деінде, сірий/чорний — нема. Ядро — Wordle-фідбек, але «словник» замінено перевіркою арифметики, тож ти одночасно шукаєш позиції символів і розвʼязуєш обмеження «ліва частина = права».

## Поле і час
- Поле 6×8 (Classic); інші розміри — 5 (micro), 6 (mini), 7 (midi), 10 (maxi) колонок.
- Під полем — екранна клавіатура з 10 цифрами, 4 операціями, `=`, Delete, Enter.
- Хід = одна підтверджена спроба. Щоденна задача однакова для всіх; нова опівночі за GMT (у налаштуваннях — за локальним часом).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Загадана рівність | static (прихована) | 8 символів, рівно один `=` | фіксована на день |
| Рядок спроби | zone | 8 клітин | активний до підтвердження, далі заморожений |
| Плитка-символ | tile | символ, стан empty/typed/green/purple/grey | колір визначається при підтвердженні |
| Клавіша клавіатури | tile (UI) | найкращий відомий стан | фарбується за пріоритетом green > purple > grey |
| Поле (multi-режими) | zone | 2 / 4 / 8 полів | одна спроба застосовується до всіх незакритих |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(symbol)` → ЯКЩО `count(typed, <, 8)` → ТО `custom: «символ у наступну клітину»`.
- КОЛИ `input(enter)` → ЯКЩО `count(typed, <, 8)` → ТО `message`, `shake`.
- КОЛИ `input(enter)` → ЯКЩО `not equation_holds(guess)` → ТО `message`, `shake`; спроба не витрачається (?).
- Валідність: рівно один `=`; праворуч від `=` — лише число, не вираз; `*` і `/` раніше за `+` і `-`, однаковий рівень — зліва направо.
- Відповіді (але не обовʼязково спроби) не мають ведучих нулів, самотніх нулів, відʼємних чисел на початку чи після `=`; `0` праворуч дозволено.
- КОЛИ `input(enter)` → ЯКЩО рівність валідна → ТО `feedback(guess)`: `paint(i, green)` для збігів позиції, далі `paint(i, purple)` для решти, поки в відповіді лишились копії символу, інакше `paint(i, grey)`.
- Дублікати: символ двічі в спробі, раз у відповіді — один пофарбований, другий сірий.
- КОЛИ `after(feedback)` → ТО `paint(key, max(state))`.
- КОЛИ `pattern(row all green)` → ТО `win`, `window(end-screen)`.
- КОЛИ `input(enter)` → ЯКЩО `mode(commutative) and commutative_match(guess, answer)` → ТО `win` — `20+10=30` зараховано за `10+20=30`, якщо все інше збігається.
- КОЛИ `counter(guesses, ==, 6)` → ЯКЩО не вгадано → ТО `lose`, `custom: «показати відповідь»` (?).
- Multi (bi/quad/octo): КОЛИ `input(enter)` → ТО `feedback(guess)` на кожному незакритому полі; `win`, коли закрито всі.
- Instant: одна спроба; Speed: КОЛИ `counter(time_left, ==, 0)` → ТО `lose` (?).
- Перемога: усі 8 зелених (або комутативний збіг) · Поразка: 6 спроб без збігу · Рахунок: номер спроби; streak і straight.

## Керування і ввід
- Фізична клавіатура (цифри, `+ - * / =`, Backspace, Enter) або екранна клавіатура.
- Курсор по клітинах — ввід у наступну вільну (?); дублікатів символів у рядку можна скільки завгодно.

## Вікна, меню, HUD
- `game-screen`: поле 6×8, `on-screen-keyboard` зі станами символів, іконки довідки/статистики/налаштувань.
- `help-window`: правила і приклади з кольоровими плитками.
- `end-screen` (win screen): результат, `share-button` (на мобільних — у застосунок, на десктопі — буфер).
- `stats-window`: streak (перемоги поспіль, незалежно від днів), straight (дні поспіль), розподіл спроб (?).
- `settings-window`: Allow commutative answers, Use local time, вимкнути рекламу на 3 дні.
- `mode-select`: Classic, micro, mini, midi, maxi, bi, mini-bi, quad, octo, speed, instant, Pro.
- Переходи: вхід → `game-screen` → кінець → `end-screen` → `stats-window` / інший режим.

## Фічі поза полем
- `mode-daily`, `share-result`, `streaks` + окрема «straight»-серія днів, `stats`.
- `commutative-answers` (перемикач), `local-reset-time`.
- `puzzle-creator` (Pro nerdle): створити власну рівність-виклик для іншої людини і поділитись.
- `multi-board` (bi/quad/octo), `mode-instant` (одна спроба), `mode-time-attack` (speed).
- Архів минулих днів і `unlimited` у частині режимів.

## Варіації й родичі
- Wordle (`wordle.md`) — оригінальна оболонка; Quordle — множинні поля (як bi/quad/octo).
- Digits (`nyt-digits.md`) — арифметика без прихованого стану; Mathable (`mathable.md`) — рівності на полі.
- Інші Wordle-клони з числами: Mathler (ціль дано, вгадуєш вираз) (?), Numberle (?).
- **Осі варіацій:** довжина (5 / 6 / 7 / 8 / 10) · кількість полів (1 / 2 / 4 / 8) · ліміт (6 спроб / 1 / таймер) · еквівалентність (точний збіг / комутативний) · алфавіт (цифри й `+-*/` / з дужками і степенем у варіантах).

## Цікавинки для курсу
- Парсер і обчислювач виразу з пріоритетом операцій, перевірка «рівно один `=`, праворуч число» — 📎.
- Фідбек з дублікатами (як у Wordle) — 🥉.
- Комутативна еквівалентність: перестановка доданків/множників при збігу решти — 🥈 (канонізація дерева виразу).
- Генератор щоденної рівності без ведучих/самотніх нулів і з «цікавим» набором символів — 🥉.
- Розвʼязувач: перелік усіх валідних рівностей довжини 8 і фільтр за відгуками, вибір спроби з макс. ентропією — 🥇.
- Multi-board з однією спробою на всі поля — 📎.

## Мапа на каталог
- Є: `daily-puzzle` · `keyboard-controls` · `cell-click` ↔ екранна клавіатура · `completion-detection` · `streak-stats` · `share-result` · `save-progress` · `time-out` ↔ speed · `stats-window` · `mode-select` · `settings-window` · `help-window` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+letter-feedback`, `+keyboard-state`, `+multi-board` — див. `wordle.md`.
  - `+equation-validation` «Спроба мусить бути правильною рівністю» · game-logic/constraints · 📎 · слоти {ops: list, precedence: bool}.
  - `+commutative-answers` «Зарахувати комутативно рівну відповідь» · game-logic/constraints · 🥈.
  - `+puzzle-creator` «Створити задачу для іншого гравця» · levels/editor · 📎.
  - `+instant-one-guess` «Режим однієї спроби» · game-logic/difficulty · 🌱.

## Пропозиції до словників
- `+cond:equation_holds` — вираз праворуч і ліворуч від `=` рівні (Nerdle, Mathable).
- `+cond:commutative_match` — спроба збігається з відповіддю з точністю до перестановки операндів.
- `+ui:on-screen-keyboard` — екранна клавіатура зі станами символів.
- `+feature:commutative-answers` — перемикач еквівалентності відповідей.
- `+feature:puzzle-creator` — гравець складає задачу іншому (Pro nerdle).
- `+feature:mode-instant` — одна спроба.
- `+feature:multi-board` — кілька полів одночасно (bi/quad/octo).
- `+feature:local-reset-time` — щоденна задача за локальною, а не глобальною північчю.

## Джерела
- ⭐ [Classic nerdle: правила](https://www.nerdlegame.com/games/classic-nerdle.html) — 8 символів, 6 спроб, порядок дій, комутативність, дублікати, щоденне скидання.
- [nerdlegame.com: FAQ](https://www.nerdlegame.com/faqs.html) — символи, `=`, праворуч число, нулі, відʼємні, streak vs straight, налаштування, Pro, share.
- [nerdlegame.com](https://www.nerdlegame.com/) — список режимів.
- [Wikipedia: Nerdle](https://en.wikipedia.org/wiki/Nerdle) — історія (Richard Mann, січень 2022), кольори.
- YouTube: пошук «nerdle gameplay».

## Непевне
- (?) Чи не витрачається спроба на неправильну рівність і точний текст повідомлень — не бачив.
- (?) Деталі Speed nerdle (скільки часу) і чи показується відповідь при поразці.
- (?) Розподіл спроб у статистиці — за аналогією з Wordle.
- (?) Mathler і Numberle як родичі — з памʼяті.
- (?) Чи дозволено ділення з неціловим проміжним результатом — FAQ мовчить.
