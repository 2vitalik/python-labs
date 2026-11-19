---
title: Crossmath (математичний кросворд)
slug: crossmath
aka: [Cross Math, Crossmath Puzzle, Math Crossword, Математичний кросворд]
family: word-number
also: [pencil-logic]
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: constraints
year: 2023
platforms: [iOS, iPadOS, macOS, Windows]
links:
  - {kind: other, url: "https://apps.apple.com/us/app/id6460980049", best: true, note: "Cross Math: Crossmath Puzzle (Can Citoglu, 03.10.2023): × і ÷ раніше за + і −, 4 складності, щоденна задача, підказки, серії з захистом, досягнення, лідерборди"}
  - {kind: other, url: "https://appynation.helpshift.com/hc/en/24-puzzling-com/faq/589-cross-math", note: "правила Cross Math (Puzzling.com): плитки 1–99 і + − × ÷ =, фіксовані плитки, чергування число/знак, зліва направо й згори вниз, зелені/червоні рівності, підказки за монети"}
  - {kind: other, url: "https://apps.apple.com/us/app/id6740814784", note: "Crossmath: Math & Logic Game (iGeniusDev, 2025): 4 складності, daily, підказки й power-ups, undo, статистика, змагальні режими на швидкість"}
  - {kind: steam, url: "https://store.steampowered.com/app/4528620/Cross_Math__Logic_Number_Puzzle/", note: "Cross Math — Logic Number Puzzle (Popoko VM Games, 2026): drag числа й знаки, миттєвий відгук, свої пазли (розмір, операції), автосейв, час"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cross-figure", note: "паперовий предок: кросворд із числами, підказки-рівняння, вимога унікального розвʼязку"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crossmath+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [drag-drop-piece, pocket, satisfy-constraints, completion-detection, markup-validity, conflict-highlight, difficulty-levels, daily-puzzle, streak-stats, achievements-window, leaderboard, undo-step, save-autosave, unique-puzzle-generation, difficulty-rating, level-solver, rule-variants, field-size-picker, theme-select, game-screen, end-screen, settings-window, help-window, +equation-grid, +tile-tray-exact, +operator-precedence, +coin-hint, +streak-protection]
proposes: ["+cond:equation_true", "+ui:piece-tray", "+ui:equation-status", "+feature:streak-protection", "+feature:coin-hints", "+card:equation-grid"]
author: opus
date: 2026-11-09
---

# Crossmath — кросворд із рівнянь: розклади числа з лотка так, щоб кожен рядок і стовпець став правильною рівністю

## Суть
Поле — кросворд, де замість слів рівності («7 + 5 = 12»), що перетинаються в спільних клітинах. Частина чисел і знаків уже стоїть, порожні клітини треба заповнити плитками з лотка під полем. Кожна плитка лотка вживається рівно раз, і в кінці всі рівності — горизонтальні й вертикальні — мають бути правильними. По суті — Kakuro/cross-figure з відкритим набором «відповідей»: дедукція «яке число куди», а не обчислення суми.

## Поле і час
- Квадратна сітка з «чорними» (порожніми) і робочими клітинами; робочі утворюють рядки й стовпці-рівняння, що перетинаються.
- У рівнянні клітини чергуються: число · знак · число · `=` · результат (або результат спереду: `N = N op N`).
- Розмір сітки росте зі складністю; у Steam-версії задається вручну.
- Час статичний; у деяких версіях — лічильник часу й змагальні режими на швидкість.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Фіксована плитка-число | static | ціле (1–99 у Puzzling) | дана умовою; не рухається |
| Фіксований знак | static | + − × ÷ = | задає операцію рівняння |
| Порожня клітина | zone | частина 1–2 рівнянь | приймає одну плитку з лотка |
| Плитка лотка | tile | число (у деяких версіях — і знак) | перетягується в порожню клітину; вживається раз |
| Рівняння | zone | рядок або стовпець | правильне / неправильне / незаповнене |
| Лоток | container | рівно стільки плиток, скільки порожніх клітин | спорожнів + усі рівняння правильні → перемога |
| Підказка | pickup | ціна в монетах | ставить правильну плитку або показує помилки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag tile → cell)` → ЯКЩО `free(cell)` → ТО `place(tile, cell)`, `take(tray, tile)`.
- КОЛИ `input(drag tile → cell)` → ЯКЩО `occupied(cell, fixed)` → ТО `block`.
- КОЛИ `input(drag placed tile)` → ТО `custom: «плитка повертається в лоток або переїжджає в іншу порожню клітину»`.
- КОЛИ `after(place)` → ЯКЩО `custom: «рівняння заповнене»` і `custom: «рівність правильна»` → ТО `paint(equation, green)`.
- КОЛИ `after(place)` → ЯКЩО `custom: «рівняння заповнене»` і `not custom: «рівність правильна»` → ТО `paint(equation, red)` (Puzzling.com).
- Порядок обчислення: у Can Citoglu — × і ÷ раніше за + і −; у Puzzling.com — рівність читається зліва направо / згори вниз, тож віднімання й ділення «навпаки» треба переставити.
- Сусідні клітини рівняння не можуть бути двома числами чи двома знаками — лише чергування (Puzzling.com).
- КОЛИ `all_constraints_met` → ЯКЩО `count(tray tiles, ==, 0)` → ТО `win`, `window(end-screen)`.
- КОЛИ `input(hint)` → ЯКЩО `has(player, coins)` → ТО `take(player, coins)`, `place(correct tile, cell)` або `custom: «перевірити помилки»`.
- КОЛИ `input(undo)` → ТО `undo` (iGeniusDev).
- КОЛИ `level_end` → ЯКЩО `mode(daily)` → ТО `counter(streak, +1)`; ЯКЩО `custom: «день пропущено»` і `has(player, streak protection)` → ТО `custom: «серія не обривається»`.
- Перемога: лоток порожній і всі рівності правильні · Поразки нема · Рахунок: час (?), серія днів, лідерборди.

## Керування і ввід
- Drag-n-drop: плитку з лотка — у клітину; з клітини — назад або в іншу клітину.
- Тап-варіант: тап по клітині, потім по плитці (?).
- Кнопки: Undo, Hint; у Steam — пауза і повтор.

## Вікна, меню, HUD
- `game-screen`: сітка рівнянь, лоток плиток (`piece-tray` / `pocket`), підсвітка рівнянь (`equation-status`: зелене/червоне), кнопки Undo і Hint, баланс монет, таймер (?).
- `mode-select` / `difficulty-select`: Easy · Medium · Hard · Expert; щоденна задача окремо.
- `end-screen`: розвʼязано, час, серія.
- `achievements-window`, `leaderboard` (Game Center).
- `shop-window`: монети й «Remove Ads» (IAP).
- `settings-window`: тема світла/темна, великий шрифт, звук.
- Переходи: `main-menu` → вибір складності / daily → `game-screen` → `end-screen` → наступна задача.

## Фічі поза полем
- `difficulty-presets` (4 рівні), `daily-puzzle`, `streaks` + `streak-protection`, `achievements`, `leaderboard-online`.
- `hint` за монети, `undo`, `autosave` і продовження (Steam), `font-scale`, `theme-select`.
- `custom-difficulty` (Steam): розмір сітки, набір операцій, глибина складності.
- Змагальні режими на швидкість і «Star Race» (iGeniusDev).

## Варіації й родичі
- Паперовий предок — cross-figure / cross-number: кросворд, де відповіді — числа, підказки — арифметика або посилання на інші відповіді.
- Kakuro, Sumplete ([sumplete.md](sumplete.md)) — числова дедукція по рядках і стовпцях; Mathable ([mathable.md](mathable.md)) — рівності на полі з руки, як Scrabble; Nerdle ([nerdle.md](nerdle.md)) — одна рівність у Wordle-оболонці; Bananagrams ([bananagrams.md](bananagrams.md)) — розкласти всю руку в кросворд.
- **Осі варіацій:** що в лотку (лише числа / числа й знаки) · порядок операцій (пріоритет / зліва направо) · діапазон чисел · відгук (миттєво зелене/червоне / лише в кінці) · форма сітки (решітка «через рядок» / вільний кросворд).

## Цікавинки для курсу
- Парсинг і перевірка рівності з пріоритетом × ÷ (і варіант «зліва направо») — 🌱.
- Сітка-кросворд: розбити поле на рядки/стовпці-рівняння з перетинами — 📎.
- Лоток з точним набором плиток, drag-n-drop, зелене/червоне на рівнянні — 📎.
- Солвер: розставити k плиток лотка перебором з відсіканням по заповнених рівняннях — 🥉.
- Генератор: випадкова правильна сітка рівнянь → прибрати клітини → перевірити унікальність розвʼязку — 🥇.
- Оцінка складності за технікою розвʼязання (скільки клітин виводяться «в лоб») — 🥇.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ плитка в клітину · `pocket` ↔ лоток · `satisfy-constraints` / `completion-detection` ↔ всі рівності правильні · `markup-validity` / `conflict-highlight` ↔ червоне рівняння · `difficulty-levels` · `daily-puzzle` · `streak-stats` · `achievements-window` · `leaderboard` · `undo-step` · `save-autosave` · `unique-puzzle-generation` · `difficulty-rating` · `level-solver` · `rule-variants` / `field-size-picker` ↔ свої пазли в Steam · `theme-select` · `game-screen` · `end-screen` · `settings-window` · `help-window`.
- **Нема** → пропозиції карток:
  - `+equation-grid` «Сітка рівнянь, що перетинаються, як кросворд» · game-logic/constraints · 📎 · слоти {ops, precedence: standard|ltr}.
  - `+tile-tray-exact` «Лоток рівно з потрібних плиток, кожна раз» · entities/legality · 🌱.
  - `+operator-precedence` «Обчислення виразу з пріоритетом операцій» · game-logic/constraints · 🌱.
  - `+coin-hint` «Підказка за внутрішню валюту» · game-logic/difficulty · 🌱.
  - `+streak-protection` «Захист серії від пропуску дня» · interface/results · 🌱.

## Пропозиції до словників
- `+cond:equation_true` — заповнений рядок/стовпець утворює правильну рівність (Crossmath, Nerdle, Mathable).
- `+ui:piece-tray` — лоток плиток під полем (як у ubongo.md).
- `+ui:equation-status` — колір рівняння: правильне / неправильне.
- `+feature:streak-protection` — пропущений день не обриває серію.
- `+feature:coin-hints` — підказки за монети з магазину.
- `+card:equation-grid` — див. «Мапа на каталог».

## Джерела
- ⭐ [App Store: Cross Math — Crossmath Puzzle](https://apps.apple.com/us/app/id6460980049) — пріоритет × ÷, складності, daily, підказки, серії, досягнення.
- [Puzzling.com: Cross Math FAQ](https://appynation.helpshift.com/hc/en/24-puzzling-com/faq/589-cross-math) — найповніші правила: формати рівностей, чергування, напрям читання, зелене/червоне, підказки.
- [App Store: Crossmath — Math & Logic Game](https://apps.apple.com/us/app/id6740814784) — undo, power-ups, змагальні режими.
- [Steam: Cross Math — Logic Number Puzzle](https://store.steampowered.com/app/4528620/Cross_Math__Logic_Number_Puzzle/) — drag чисел і знаків, свої пазли, автосейв.
- [Wikipedia: Cross-figure](https://en.wikipedia.org/wiki/Cross-figure) — паперовий предок.
- YouTube: пошук «crossmath puzzle gameplay».

## Непевне
- (?) «Crossmath» — жанр із десятками клонів; правила розходяться (пріоритет чи зліва направо, чи бувають знаки в лотку). ⭐-застосунок не описує розкладку сітки й ввід — це з Puzzling.com і Steam.
- (?) Чи є в ⭐-застосунку таймер, ліміт помилок і миттєва підсвітка помилок.
- (?) Чи гарантовано унікальний розвʼязок у генерованих задачах.
- (?) Розміри сіток за складністю — не бачив чисел.
- 2026-11-19 (T364, знахідка хвилі 3): alias «Number Sums Crossword» знято — Number Sums ближча до Sumplete.
