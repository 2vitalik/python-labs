---
title: Crosswordle
slug: crosswordle
aka: [Reverse Wordle, Обернений Wordle]
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2022
platforms: [web]
links:
  - {kind: other, url: "https://nerdschalk.com/how-to-play-crosswordle-rules-and-gameplay-explained/", best: true, note: "найповніший розбір: розміри, значення кольорів, тексти помилок, режими, share"}
  - {kind: play, url: "https://crosswordle.vercel.app/", note: "грати в браузері (сторінка — SPA, без тексту правил у HTML)"}
  - {kind: other, url: "https://enigmida.substack.com/p/my-favorite-puzzly-wordle-variants", note: "огляд варіантів Wordle; Crosswordle — «reverse engineer Wordle»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crosswordle+reverse+wordle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [word-validation, satisfy-constraints, markup-validity, conflict-highlight, completion-detection, daily-puzzle, difficulty-levels, share-result, keyboard-controls, cell-click, selection-highlight, game-screen, help-window, end-screen, +letter-feedback, +reverse-feedback-puzzle, +hard-mode, +challenge-link]
proposes: ["+cond:feedback_equals", "+cond:consistent_with_hints", "+ui:color-pattern-grid", "+ui:column-error-flag", "+feature:challenge-link", "+card:reverse-feedback-puzzle"]
author: opus
date: 2026-11-09
---

# Crosswordle — Wordle навпаки: відповідь і кольори дано, впиши хибні спроби, що дали б саме ці кольори

## Суть
Гравцю показують фінальний рядок (п'ятилітерне слово-відповідь, усе зелене) і над ним кілька рядків уже розфарбованих, але порожніх клітин. Треба вписати в кожен рядок справжнє слово так, щоб Wordle-відгук на нього проти відповіді дав рівно ті кольори, що намальовані. Ядро — обернена задача до Wordle-відгуку: не «що означають кольори», а «яке слово їх породить», плюс обмеження між рядками, як у судоку (тег «Sudoku meets Wordle»).

## Поле і час
- Сітка рядків × 5 стовпців; останній рядок — відповідь. Щоденний пазл — 4×5 (у джерелі також «5×4» — нестиковка).
- Режими розміру: Easy 3×5 · Normal 4×5 · Hard 6×5 («повний Wordle у зворотному режимі»).
- Час статичний, без ліміту спроб і часу; у щоденному пазлі біжить секундомір (для результату).
- Шари клітини: колір (заданий, незмінний) + літера (вписує гравець).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рядок-відповідь | zone | 5 літер, усі зелені | дано; еталон для відгуку |
| Зелена клітина | mark | колір green | приймає лише літеру відповіді в тій самій позиції |
| Жовта клітина | mark | колір yellow | приймає літеру з відповіді, але не ту, що стоїть у відповіді на цій позиції |
| Сіра клітина | mark | колір grey | приймає лише літеру, якої нема у відповіді (або «зайву» копію) |
| Рядок-спроба | zone | 5 клітин | має скластись у словникове слово |
| Літера гравця | tile | A–Z | вписується в обрану клітину, стирається, переписується без обмежень |
| Прапорець помилки | mark | стовпець + текст | червона рамка стовпця і повідомлення під сіткою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `reveal(answer_row)`, `custom: «намалювати кольори всіх рядків-спроб, літери порожні»`.
- КОЛИ `input(select cell)` → ТО `set_state(cell, selected)`.
- КОЛИ `input(letter)` → ТО `mark(cell, letter)`; КОЛИ `input(delete)` → ТО `unmark(cell)`.
- КОЛИ `input(letter)` → ЯКЩО `cell(cell, green)` and `not same(letter, answer[pos], letter)` → ТО `message(«This letter is in the final row, so it should not be in this tile»)` або аналог; `custom: «стовпець з прапорцем помилки»`.
- КОЛИ `input(letter)` → ЯКЩО `cell(cell, yellow)` and `same(letter, answer[pos], letter)` → ТО `custom: «помилка: жовта не може стояти на своїй позиції відповіді»`.
- КОЛИ `input(letter)` → ЯКЩО `cell(cell, grey)` and `custom: «літера є у відповіді і не зайва»` → ТО `message(«This letter does not appear in the final row»)`-подібна помилка.
- КОЛИ `input(letter)` → ЯКЩО `custom: «у рядку забагато копій літери порівняно з її жовтими/зеленими»` → ТО `message(«Too many occurrences of this letter in this row»)`.
- КОЛИ `input(letter)` → ЯКЩО `custom: «сіра літера вже була в попередньому рядку»` → ТО `message(«A previous row already used this letter»)`.
- КОЛИ `input(letter)` → ЯКЩО `not custom: «рядок містить усі літери, знайдені в попередніх рядках»` → ТО `message(«You must use all previously found letters»)` — правило hard mode Wordle, перенесене на реконструкцію.
- КОЛИ `custom: «рядок заповнено»` → ЯКЩО `not in_dictionary(row)` → ТО `message(«Invalid word in this row»)`.
- КОЛИ `custom: «рядок заповнено»` → ЯКЩО `custom: «feedback(row, answer) = намальовані кольори»` → ТО `custom: «рядок прийнято»`.
- КОЛИ `all_constraints_met` → ТО `timer(stop)`, `win`, `window(end-screen)`.
- Перемога: усі рядки — словникові слова з правильним відгуком і міжрядковими обмеженнями · Поразки нема · Рахунок: час розвʼязання (щоденний).

## Керування і ввід
- Клік/тап по клітині — вибір (пунктирна підсвітка); набір літери з клавіатури або екранної; Delete/кнопка — стерти.
- ПК: стрілки — рух між клітинами.
- Перевірки «на льоту»: кнопки Check нема, помилки зʼявляються одразу (червоний стовпець + текст).
- Кількість спроб не обмежена: літери можна вписувати й переписувати скільки завгодно.

## Вікна, меню, HUD
- `game-screen`: сітка з кольоровими клітинами, рядок-відповідь знизу, `timer-elapsed` (щоденний), `color-pattern-grid` = саме поле, `column-error-flag` + текст помилки під сіткою, екранна клавіатура (?).
- `help-window`: правила і значення кольорів (?).
- `mode-select` (?): Daily · Easy · Normal · Hard.
- `end-screen`: сітка-результат з часом, кнопки «Share Game» (копія в буфер) і «Challenge a friend» (лінк на той самий пазл).
- Переходи: вхід → щоденний `game-screen` → розвʼязано → `end-screen` → share / інший режим.

## Фічі поза полем
- `daily-puzzle` (той самий для всіх, оновлюється щодня) · `difficulty-presets` (3×5 / 4×5 / 6×5).
- `share-result` — результат з часом у буфер; `challenge-link` — надіслати другу той самий пазл.
- `auto-check` — помилки показуються одразу, без кнопки.
- Лише веб, без застосунків у сторах.

## Варіації й родичі
- Wordle (`wordle.md`) — пряма задача; Crosswordle — обернена до тієї ж функції відгуку.
- Absurdle (`absurdle.md`) — теж гра з функцією відгуку, але проти «злого» відповідача; Quordle (`quordle.md`) — кілька відповідей.
- Однойменний crosswordle.com — **інша** гра: міні-кросворд 7×7 з обмінами літер (ближче до `waffle.md`).
- **Осі варіацій:** кількість рядків (3 / 4 / 6) · міжрядкові обмеження (жодних / заборона сірих повторів / hard mode) · що дано (кольори + відповідь / лише кольори) · перевірка (на льоту / кнопкою).

## Цікавинки для курсу
- Функція Wordle-відгуку з правильною обробкою повторних літер — 🌱 (база для гри і перевірки).
- Перевірка рядка: слово зі словника + `feedback(word, answer) == pattern` — 📎.
- Генератор пазла: взяти відповідь, вибрати випадкові словникові слова, порахувати їх кольори — так кольори завжди розвʼязні — 📎.
- Розвʼязувач: для кожного рядка відфільтрувати словник за візерунком, потім backtracking з міжрядковими обмеженнями — 🥉.
- Діагностика помилок по стовпцю з текстом-поясненням (5 видів) — 📎.

## Мапа на каталог
- Є: `word-validation` ↔ «Invalid word in this row» · `satisfy-constraints` ↔ мета пазла · `markup-validity` / `conflict-highlight` ↔ червоний стовпець · `completion-detection` · `daily-puzzle` · `difficulty-levels` ↔ Easy/Normal/Hard · `share-result` · `keyboard-controls` · `cell-click` · `selection-highlight` ↔ пунктирна клітина · `game-screen` · `help-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+letter-feedback`, `+hard-mode` — див. `wordle.md`, `absurdle.md`.
  - `+reverse-feedback-puzzle` «Обернений відгук: дано кольори, знайди спробу» · game-logic/constraints · 📎 · слоти {rows, answer}.
  - `+challenge-link` «Лінк-виклик другу на той самий пазл» · interface/results · 🌱.

## Пропозиції до словників
- `+cond:feedback_equals` — відгук на слово проти відповіді збігається з заданим візерунком (Crosswordle; перевірка розвʼязника Wordle).
- `+cond:consistent_with_hints` — спроба не суперечить попереднім відгукам (hard mode Wordle, Crosswordle).
- `+ui:color-pattern-grid` — сітка заданих кольорів без літер.
- `+ui:column-error-flag` — помилка, привʼязана до стовпця, з текстом під полем.
- `+feature:challenge-link` — надіслати другу той самий пазл.
- `+card:reverse-feedback-puzzle` — див. «Мапа на каталог».

## Джерела
- ⭐ [Nerdschalk: How to play Crosswordle](https://nerdschalk.com/how-to-play-crosswordle-rules-and-gameplay-explained/) — розміри, кольори, тексти помилок, режими, таймер, share, автор (Reddit ymichael з дружиною).
- [crosswordle.vercel.app](https://crosswordle.vercel.app/) — сама гра (у HTML лише назва і «Sudoku meets Wordle»).
- [Enigmida: My favorite puzzly Wordle variants](https://enigmida.substack.com/p/my-favorite-puzzly-wordle-variants) — коротко: «дано фінальне слово, визнач спроби під жовто-зелений візерунок».
- YouTube: пошук «crosswordle reverse wordle gameplay».

## Непевне
- (?) Розмір щоденного пазла: у джерелі і «4×5», і «5×4».
- (?) Точні умови сірої клітини (зайва копія літери з відповіді — сіра?) — виведено з Wordle, у джерелі лише «невикористані літери».
- (?) Чи заборона повтору сірих поширюється на позицію в hard mode — джерело формулює неясно.
- (?) Є `help-window` / `mode-select` як окремі вікна чи режими перемикаються в заголовку — не бачив інтерфейсу наживо.
- (?) Рік: черга й огляди — 2022; дати першого запуску не бачив.
