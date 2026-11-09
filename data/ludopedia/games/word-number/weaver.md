---
title: Weaver (word ladder)
slug: weaver
aka: [Word ladder, Doublets, Word-links, Word golf, Laddergram, Stepword, Словесна драбина]
family: word-number
also: []
klass: puzzle
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: state
year: 2022
platforms: [web]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Word_ladder", best: true, note: "правила драбини, Doublets Керролла (1877–1879), варіанти з додаванням/зняттям літери й анаграмою, Кнут: 5757 слів, 671 «aloof»"}
  - {kind: play, url: "https://wordwormdormdork.com/", note: "Weaver, грати в браузері (сторінка на JS, текст правил не читається ботом)"}
  - {kind: other, url: "https://www.producthunt.com/products/weaver-game/launches", note: "запуск 29.07.2022, «Wordle-подібний» дизайн, команда wordwormdormdork"}
  - {kind: other, url: "https://ggwpacademy.com/?p=5538", note: "варіанти (word golf, драбини з підказками, ±літера), Hamming-відстань як нижня межа, пошук з двох кінців"}
  - {kind: other, url: "https://ggwpacademy.com/?p=3000", note: "Weaver: щоденна задача, безлімітна практика, менше кроків — краще"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=weaver+word+ladder+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [word-validation, keyboard-controls, daily-puzzle, completion-detection, move-counter, undo-step, level-solver, reachability-check, game-screen, help-window, settings-window, end-screen, share-result, streak-stats, +one-letter-step, +position-match-highlight, +optimal-path-par, +practice-unlimited]
proposes: ["+cond:hamming_one", "+ui:ladder-rungs", "+ui:optimal-ladder", "+feature:mode-practice-unlimited", "+card:one-letter-step"]
author: opus
date: 2026-11-09
---

# Weaver — драбина Керролла: від слова до слова, міняючи по одній літері, і кожен щабель — справжнє слово

## Суть
Дано початкове й кінцеве слово однакової довжини. Гравець вписує проміжні слова: кожне відрізняється від попереднього рівно однією літерою на тій самій позиції і має бути в словнику. Мета — дійти до кінцевого слова якомога меншою кількістю кроків. Weaver (2022) — Wordle-оболонка над класичною «драбиною» Льюїса Керролла (Doublets, 1877–1879): щоденна задача, зелені літери на позиціях, що вже збігаються з ціллю, показ оптимальної драбини.

## Поле і час
- «Поле» — стовпчик щаблів-рядків: угорі початкове слово, внизу кінцеве, між ними — вписані гравцем (кожен рядок — N клітин-літер).
- Насправді гра відбувається на прихованому графі: вершини — слова словника довжини N, ребра — пари з різницею в одну позицію.
- Час статичний; щоденна задача однакова для всіх, практика — без ліку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Початкове слово | static | N літер | перший щабель, не змінюється |
| Кінцеве слово | static | N літер | ціль; щабель, що з ним збігся, закінчує задачу |
| Щабель | tile | слово з N літер | вписується з клавіатури; приймається лише за правилом «одна літера» |
| Літера щабля | mark | зелена / звичайна | зелена, якщо на цій позиції вже стоїть літера кінцевого слова |
| Оптимальна драбина | mark | довжина = мінімум кроків | показується після розвʼязання (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(type word)` → ЯКЩО `in_dictionary(word)` і `custom: «рівно одна позиція відрізняється від попереднього щабля»` → ТО `place(word, next rung)`, `counter(steps, +1)`.
- КОЛИ `input(type word)` → ЯКЩО `not in_dictionary(word)` → ТО `block`, `message(«not a word»)`.
- КОЛИ `input(type word)` → ЯКЩО `custom: «відрізняється на 0 або ≥2 позиції»` → ТО `block`.
- КОЛИ `after(place)` → ЯКЩО `same(letter, target letter at position)` → ТО `paint(letter, green)`.
- КОЛИ `after(place)` → ЯКЩО `same(word, target)` → ТО `win`, `window(end-screen)`.
- КОЛИ `input(delete rung)` → ТО `undo` — прибрати останній щабель (?).
- КОЛИ `level_end` → ТО `custom: «показати кількість кроків і оптимальну драбину для порівняння»`.
- Літери не переставляються, не додаються й не зникають — довжина слова стала (у класичному Weaver).
- Нижня межа кроків — кількість позицій, де початкове й кінцеве слово різняться; реальна драбина часто довша.
- Перемога: дійти до кінцевого слова · Поразки нема (кроків без ліку) · Рахунок: кількість кроків порівняно з оптимумом.

## Керування і ввід
- Клавіатура (фізична чи екранна): набрати слово, Enter — додати щабель, Backspace — стерти.
- Задача з обох кінців: гравець бачить і початок, і кінець, тож планує «міст» посередині.

## Вікна, меню, HUD
- `game-screen`: стовпчик щаблів (`ladder-rungs`) між початковим і кінцевим словом, зелені літери, екранна клавіатура, лічильник кроків.
- `help-window`: правила одним прикладом (?).
- `settings-window`: перемикачі режимів (челендж / показ оптимального розвʼязку) (?).
- `end-screen`: «розвʼязано за N кроків», `optimal-ladder` — одна з найкоротших драбин, `share-result` (?).
- Переходи: `game-screen` → `end-screen` → практика (нова випадкова пара).

## Фічі поза полем
- `daily-puzzle`: одна пара слів на день для всіх.
- `mode-practice-unlimited`: випадкові пари без ліку.
- `show-solution`: оптимальна драбина після розвʼязання.
- Weaver X — варіант, де щаблі можуть мати різну довжину (?).
- `streaks` / `share-result` — як у Wordle-подібних (?).

## Варіації й родичі
- Doublets (Керролл, Vanity Fair 1879), Word-links (щоденник 1878, гра на двох), Laddergrams (1927), «word golf» у Набокова, Stepword (Canberra Times, 1990-ті).
- Варіанти правил: додати/зняти літеру; переставити всі літери (анаграма) як окремий крок; драбини з підказкою-визначенням на кожному щаблі; «гольф» — двоє розвʼязують ту саму і порівнюють кроки.
- Wordle-родина корпусу: [wordle.md](wordle.md) (оболонка, зелені літери), [absurdle.md](absurdle.md), [quordle.md](quordle.md); перестановка літер — [typeshift.md](typeshift.md), [waffle.md](waffle.md).
- **Осі варіацій:** довжина слова (стала / змінна) · дозволений крок (заміна / ±літера / анаграма) · оцінка (будь-яка драбина / кроки проти оптимуму / ліміт кроків) · словник (загальний / список гри) · мультиплеєр (гольф на двох).

## Цікавинки для курсу
- Перевірка кроку «рівно одна позиція різна» + словник — 🌱.
- Граф слів і BFS найкоротшої драбини (показ оптимуму) — 📎.
- Двобічний BFS і перелік усіх найкоротших драбин (як «cold → warm» має 7 розвʼязків) — 🥉.
- Компоненти звʼязності графа: «aloof»-слова без сусідів, перевірка, що пара взагалі розвʼязна — 🥉.
- Генератор щоденної пари з контролем складності (довжина оптимуму, кількість найкоротших шляхів, рідкість слів) — 🥈.
- Weaver X: граф зі змінною довжиною (ребра ±літера) — 🥈.

## Мапа на каталог
- Є: `word-validation` ↔ щабель у словнику · `keyboard-controls` · `daily-puzzle` · `completion-detection` ↔ щабель = ціль · `move-counter` ↔ кроки · `undo-step` ↔ стерти щабель · `level-solver` / `reachability-check` ↔ BFS оптимуму й розвʼязності · `share-result` · `streak-stats` · `game-screen` · `help-window` · `settings-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+one-letter-step` «Хід = слово, що відрізняється на одну літеру» · game-logic/legality · 🌱 · слоти {ops: replace|insert|delete|anagram}.
  - `+position-match-highlight` «Підсвітити літери, що вже збігаються з ціллю» · interface/hud · 🌱.
  - `+optimal-path-par` «Порівняти шлях гравця з найкоротшим» · game-logic/score · 📎 · слоти {show_after: win}.
  - `+practice-unlimited` «Безлімітні випадкові задачі поруч із щоденною» · levels/generation · 🌱.

## Пропозиції до словників
- `+cond:hamming_one` — два слова однакової довжини різняться рівно в одній позиції (Weaver; варіант `edit_one` для ±літери).
- `+ui:ladder-rungs` — стовпчик щаблів між двома закріпленими словами.
- `+ui:optimal-ladder` — показ однієї з найкоротших драбин після розвʼязання.
- `+feature:mode-practice-unlimited` — безлімітна практика поруч із daily (Weaver, Wordle-клони).
- `+card:one-letter-step` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Word ladder](https://en.wikipedia.org/wiki/Word_ladder) — правила, приклад cold → warm (4 кроки, 7 найкоротших), історія Doublets, варіанти ±літера та анаграма, дослідження Кнута.
- [Weaver](https://wordwormdormdork.com/) — сама гра (JS-сторінка; правила зі сторонніх описів).
- [Product Hunt: Weaver Game](https://www.producthunt.com/products/weaver-game/launches) — дата запуску, звʼязок із Wordle.
- [ggwpacademy: Word Ladder Puzzle](https://ggwpacademy.com/?p=5538) — варіанти й прийоми (з двох кінців, «містки», Hamming-відстань: MAN → APE — 5 кроків, не 3).
- [ggwpacademy: Weaver Game Rules](https://ggwpacademy.com/?p=3000) — щоденна задача, практика, оцінка за кроками.
- YouTube: пошук «weaver word ladder game gameplay».

## Непевне
- (?) Довжина слова у Weaver (за памʼяттю — 4 літери) — офіційну сторінку правил не прочитав.
- (?) Набір налаштувань: челендж-режим, показ оптимального розвʼязку, статистика, share — з памʼяті й вторинних сайтів.
- (?) Weaver X — точні правила зміни довжини щаблів.
- (?) Чи можна видалити не лише останній щабель, а будь-який; чи є ліміт кроків.
- (?) Автор(и) Weaver — Product Hunt називає лише «команду wordwormdormdork».
