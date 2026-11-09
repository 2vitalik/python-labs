---
title: Codeword
slug: codeword
aka: [Cipher crossword, Code Breaker, Code Cracker, Kaidoku, Кодворд]
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: none
  goal: constraints
year: null
platforms: [paper, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cipher_crossword", best: true, note: "розділ Crossword про cipher crosswords: числа 1–26, однакове число = однакова літера, стартові літери, панграма, Німеччина XIX ст., інші назви"}
  - {kind: other, url: "https://www.puzzles.wiki/wiki/Codeword", note: "визначення, ключ для запису, британські сітки, вибір стартових літер під складність"}
  - {kind: other, url: "https://simplydailypuzzles.com/daily-codeword/how-to-play.html", note: "цифрова версія: автозаповнення однакових чисел, Reveal Letter, Solution, Restore, таймер, друк"}
  - {kind: other, url: "https://amuselabs.com/docs/puzzles/codeword/overview/", note: "цифрова версія PuzzleMe: екранна клавіатура, збереження прогресу, кілька мов"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=how+to+solve+codeword+puzzle", note: "пошук; розвʼязування"}
stage: v1
coverage: 70
mechanics: [cell-click, keyboard-controls, selection-highlight, word-validation, daily-puzzle, save-progress, game-screen, help-window, unique-puzzle-generation, difficulty-levels, +substitution-key, +auto-fill-same-symbol, +pangram-constraint, +letter-tracker, +reveal-letter, +print-version]
proposes: ["+cond:same_symbol_same_value", "+ui:cipher-key", "+ui:alphabet-tracker", "+window:print-view"]
author: opus
date: 2026-11-09
---

# Codeword — кросворд без підказок: кожна клітина має число 1–26, однакові числа — однакові літери, розгадай шифр підстановки

## Суть
Сітка кросворду, де замість підказок у кожній білій клітині стоїть число від 1 до 26. Однакове число всюди означає одну літеру, різні числа — різні літери, а кожне вписане слово мусить бути справжнім. На старті відомі одна чи кілька пар «число → літера»; решту гравець виводить, як криптограму: частоти чисел, ймовірні голосні, шаблони слів і перетини. Англійські версії майже завжди панграмні — у відповіді є всі 26 літер, тож ключ заповнюється повністю.

## Поле і час
- Квадратна сітка британського типу з чорними клітинами (менше перетинів, ніж в американській); у журналах типово 13×13 або 15×15 (?).
- Шари: сітка (біла / чорна) + число в кутку білої клітини + вписана літера; поза полем — ключ 1–26 і алфавіт A–Z.
- Часу нема; у цифрових версіях — необовʼязковий таймер.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Біла клітина | mark | число 1–26, літера або порожньо | показує літеру, призначену її числу |
| Чорна клітина | static | — | розділяє слова, не заповнюється |
| Стартова літера | mark | пара число → літера | дана на початку, не змінюється |
| Слово | zone | ряд/стовпець білих клітин довжиною ≥ 2 | має бути словом мови |
| Ключ 1–26 | zone | 26 слотів | запис знайдених пар; вписане тут = вписане в усі клітини числа |
| Алфавіт A–Z | zone | 26 літер | використані літери викреслюються |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `reveal(given cells)`, `mark(key, given pairs)`.
- КОЛИ `input(type letter, cell)` → ЯКЩО `not state(cell, given)` → ТО `mark(cell, letter)` і `custom: «та сама літера з'являється в усіх клітинах з цим числом»`, `mark(key[number], letter)`.
- КОЛИ `input(type letter, cell)` → ТО `custom: «літера викреслюється в A–Z; стара літера цього числа повертається»`.
- КОЛИ `input(type letter, cell)` → ЯКЩО `custom: «цю літеру вже призначено іншому числу»` → ТО `custom: «конфлікт ключа — підсвітка або заміна (?)»`.
- Обмеження 1: `custom: «однакове число ↔ однакова літера»` (автоматично в цифровій версії).
- Обмеження 2: `unique(key)` — різні числа мають різні літери.
- Обмеження 3: `in_dictionary(word)` для кожного слова сітки.
- Обмеження 4 (англ. версії): `custom: «панграма — кожна з 26 літер ужита»`.
- КОЛИ `all_constraints_met` → ЯКЩО `custom: «усі клітини заповнено, ключ збігається з розвʼязком»` → ТО `win`.
- КОЛИ `input(reveal letter)` → ТО `mark(selected cell, correct letter)` (і всіх клітин цього числа).
- КОЛИ `input(solution)` → ТО `custom: «показати правильну літеру клітини без вписування»`.
- КОЛИ `input(restore)` → ТО `restart` — усе введене стерто, лишаються стартові літери.
- Складність: менше стартових літер → важче; укладач обирає тематичні, одну часту або кілька рідкісних літер.
- Перемога: шифр розгадано · Поразка: нема · Рахунок: нема (у цифрових — час).

## Керування і ввід
- Папір: вписування в клітини й ключ, викреслення A–Z.
- Цифрова версія: клік/тап по клітині (виділяється), набір літери з клавіатури або екранної клавіатури; автозаповнення всіх клітин того ж числа; кнопки Reveal Letter, Solution, Restore.

## Вікна, меню, HUD
- `game-screen` (цифрова версія): сітка з числами, `selection-highlight` клітини і, можливо, всіх клітин того ж числа (?), ключ 1–26 (`cipher-key`), алфавіт A–Z з викресленими (`alphabet-tracker`), таймер (`timer-elapsed`, необовʼязковий, перетягуваний), кнопки.
- `print-view`: версія для друку (simplydailypuzzles).
- `puzzle-select` / `daily-window`: «Today's Codeword» і архів (?).
- `end-screen`: розвʼязано, час (?).
- `help-window`: правила.

## Фічі поза полем
- `daily-puzzle` на сайтах і в газетах; `hint` = Reveal Letter, `show-solution`, `restart-level` = Restore.
- `save-progress` локально (PuzzleMe), кілька мов (PuzzleMe).
- Друк для розвʼязування на папері.

## Варіації й родичі
- Криптограма (зашифрована фраза без сітки), Cryptolist; Kaidoku — японська версія (панграмність там не діє).
- Кросворд, кросчисло (crossnumber), arroword — інші варіанти кросворду; філворди й fill-in (слова дані, місця ні).
- Корпус: [wordle.md](wordle.md) (виведення літер з відгуків), [crosswordle.md](crosswordle.md), [knotwords.md](knotwords.md) (кросворд-обмеження без підказок).
- **Осі варіацій:** алфавіт (26 літер / кана / цифри) · панграма (так / ні) · стартові підказки (тематичні / часті / рідкісні) · геометрія сітки (британська / американська / вільна).

## Цікавинки для курсу
- Модель: сітка чисел + словник «число → літера» з автозаповненням і перевіркою біекції — 🌱.
- Перевірка розвʼязку: усі слова в словнику, ключ взаємно однозначний, панграма — 📎.
- Розвʼязувач: пошук з поверненням за шаблонами слів зі словника (обмеження «однакові числа — однакові літери») — 🥇.
- Генерація: заповнити сітку словами-панграмою і підібрати мінімум стартових літер для однозначності — 👑.
- Підказки «частота чисел» і «де Q, там U» як допомога гравцю — 🌱.

## Мапа на каталог
- Є: `cell-click` · `keyboard-controls` ↔ набір літер · `selection-highlight` · `word-validation` ↔ кожне слово справжнє · `daily-puzzle` · `save-progress` · `game-screen` · `help-window` · `unique-puzzle-generation` ↔ один розвʼязок · `difficulty-levels` ↔ кількість стартових літер.
- **Нема** → пропозиції карток:
  - `+substitution-key` «Ключ підстановки символ → значення» · game-logic/constraints · 🌱.
  - `+auto-fill-same-symbol` «Ввід у клітину заповнює всі з тим самим символом» · interface/input · 🌱.
  - `+pangram-constraint` «Усі літери алфавіту ужито» · game-logic/constraints · 🌱.
  - `+letter-tracker` «Алфавіт з викресленими літерами» · interface/hud · 🌱.
  - `+reveal-letter` «Підказка: відкрити одну літеру» · game-logic/hints · 🌱.
  - `+print-version` «Версія для друку» · interface/render · 📎.

## Пропозиції до словників
- `+cond:same_symbol_same_value` — клітини з однаковим символом мають однакове значення (Codeword, криптограми).
- `+ui:cipher-key` — таблиця «символ → значення» з вписаними парами; `+ui:alphabet-tracker` — алфавіт з викресленими літерами.
- `+window:print-view` — версія пазла для друку.

## Джерела
- ⭐ [Wikipedia: Cipher crossword](https://en.wikipedia.org/wiki/Cipher_crossword) (розділ статті Crossword) — правила, панграма, історія, назви, Kaidoku.
- [Puzzles Wiki: Codeword](https://www.puzzles.wiki/wiki/Codeword) — ключ, британські сітки, вибір стартових літер.
- [Simply Daily Puzzles: How to play](https://simplydailypuzzles.com/daily-codeword/how-to-play.html) — цифровий інтерфейс.
- [Amuse Labs PuzzleMe: Codeword](https://amuselabs.com/docs/puzzles/codeword/overview/) — ввід, збереження, мови.
- YouTube: пошук «how to solve codeword puzzle».

## Непевне
- (?) Типові розміри 13×13 / 15×15 — з фрагмента пошуку, не з відкритої сторінки.
- (?) Рік: Wikipedia — «винайдено в Німеччині в XIX ст.» без дати; черга подає «XX ст.» (масова газетна популярність) — `year: null`.
- (?) Як цифрові версії реагують на дубль літери (підсвітка, заміна, заборона) і чи підсвічують усі клітини того ж числа.
- (?) Чи є в цифрових версіях `end-screen` з часом і архів пазлів.
- Окремої статті Wikipedia «Codeword (puzzle)» нема (404) — є розділ у Crossword.
