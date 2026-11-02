---
title: Waffle
slug: waffle
family: word-number
also: []
klass: puzzle
axes:
  field: square
  time: turn
  opponent: none
  info: partial
  random: setup
  goal: state
year: 2022
platforms: [web]
links:
  - {kind: play, url: "https://wafflegame.net/daily", best: true, note: "офіційна гра + How to play: 15 свапів, зірки, кутові літери, статистика"}
  - {kind: other, url: "https://arxiv.org/html/2501.09286v2", note: "S.P. Glasby, «Mathematics of the NYT daily word game Waffle»: правила, цикли перестановки, мінімум 10 свапів"}
  - {kind: other, url: "https://wordfinder.yourdictionary.com/blog/waffle-game-creator-james-robinson-talks-inspiration-behind-his-multi-word-puzzle", note: "інтервʼю автора: історія, 7×7 Deluxe"}
  - {kind: other, url: "https://www.pcgamer.com/a-wordle-inspired-game-called-waffle-has-become-more-popular-than-actual-waffles", note: "PC Gamer, лютий 2022"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=waffle+word+game+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [daily-puzzle, drag-drop-piece, completion-detection, profile-stats, level-bank, end-screen, game-screen, help-window, +swap-tiles, +move-budget, +letter-feedback, +intersection-feedback, +stars-by-moves, +share-result, +streak-stats, +min-swaps-cycles]
proposes: ["+trigger:input", "+effect:swap", "+effect:feedback", "+cond:in_word", "+role:tile", "+ui:swaps-left", "+ui:stars-rating", "+window:stats-window", "+window:archive-window", "+feature:share-result", "+feature:streaks", "+axis:session"]
author: opus
date: 2026-11-02
---

# Waffle — переставляй літери «вафлі» 5×5, доки 6 слів не стануть на місце, за ≤15 обмінів

## Суть
На полі-вафлі з 21 клітини вже лежать усі потрібні літери, але перемішані; треба переставити їх так, щоб три горизонтальні й три вертикальні 5-літерні слова прочиталися правильно. Хід — обмін двох будь-яких літер; після кожного обміну літери перефарбовуються (зелений / жовтий / сірий) як у Wordle. Ліміт — 15 обмінів, мінімум завжди 10; кожен зекономлений обмін — зірка. Незвичне: Wordle-фідбек поєднано з перестановочною головоломкою, а кутові клітини належать двом словам одночасно.

## Поле і час
- Сітка 5×5 з 4 «дірками» в (2,2), (2,4), (4,2), (4,4) → 21 клітина. Слова: рядки 1, 3, 5 і стовпці 1, 3, 5.
- 9 клітин-перетинів (кути й центр сітки слів: «непарні» клітини за Glasby) належать і рядку, і стовпцю; 12 «парних» — лише одному слову.
- Часу нема; хід = один обмін. Сесія — щоденна задача (+ щотижневий Deluxe).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Клітина-перетин | zone | належить 2 словам | фідбек рахується проти обох слів |
| Клітина в одному слові | zone | належить 1 слову | фідбек лише проти свого слова |
| Дірка | static | — | порожня, не бере участі |
| Плитка-літера | tile | літера, стан green/yellow/grey | обмінюється місцем з іншою; перефарбовується після кожного ходу |
| Слово-ціль | zone (приховане) | 5 літер, рядок або стовпець | 6 штук; відомі лише після розвʼязання |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag tile_a → tile_b)` → ЯКЩО `counter(swaps_left, >, 0)` → ТО `swap(tile_a, tile_b)`, `counter(swaps_left, -1)`, `feedback(board)`.
- `feedback` для клітини: green — літера правильна саме тут; інакше для однословної клітини yellow, якщо `in_word(letter, own_word)`, інакше grey; для клітини-перетину yellow, якщо літера є в горизонтальному **або** вертикальному слові, інакше grey (вікно правил: «corner letter … either the vertical word contains this letter or the horizontal word»).
- Жовтий означає «ця літера є в слові», а не «саме ця копія зайва»: повторена літера може лишатися жовтою, доки одна з копій не стане на місце (з довідки гри).
- КОЛИ `paint(cell, green)` → ТО `custom: «плитка зафіксована, її не можна перетягти»` (?).
- КОЛИ `all_constraints_met` (усі 21 клітина зелені) → ТО `win`, `score(stars = swaps_left)`, `animate`, `window(end-screen)`.
- КОЛИ `counter(swaps_left, ==, 0)` → ЯКЩО не розвʼязано → ТО `lose`, `custom: «показати розвʼязок»` (?).
- Початкову розстановку автор генерує так, що мінімальна кількість обмінів = 10 рівно, а розвʼязок єдиний (Glasby: автор уникає «обмінюваних» слів).
- Перемога: усі клітини зелені · Поразка: 15 обмінів без розвʼязку · Рахунок: зірки 0–5 = 15 − використані обміни.

## Керування і ввід
- Drag-n-drop: потягнути літеру на будь-яку іншу клітину — дві літери міняються місцями. Альтернатива — тап по одній, потім по другій (?).
- Жодного введення з клавіатури: алфавіт фіксований, усі літери вже на полі (автор свідомо відмовився від «перетягування з алфавіту»).

## Вікна, меню, HUD
- `game-screen`: вафля 5×5, під нею `swaps-left` («N swaps remaining»), номер Waffle дня, кнопки меню.
- `help-window` («How to play»): правила з прикладами чотирьох станів — правильне місце, є в горизонтальному слові, є у вертикальному слові, кутова літера.
- `end-screen`: розвʼязана вафля, `stars-rating` (0–5 ★), `share-button`, перехід до статистики; на поразці — розвʼязок (?).
- `stats-window`: Played · Total stars · Current streak · Best streak · розподіл зірок 0–5.
- `archive-window`: минулі вафлі (результати не йдуть у статистику); архів Deluxe — за перегляд реклами спонсора.
- Перемикач режимів: Daily · Deluxe (щотижневий) · Number Waffle — `mode-select`.

## Фічі поза полем
- `mode-daily` / `daily-puzzle` + `streaks` + `stats` (зірки як «валюта» серії).
- `share-result`: текст із номером і кольоровими квадратами вафлі + зірки, копія в буфер.
- `puzzle-bank` (архів) окремо від статистики — цікаве рішення: практика не ламає серію.
- Deluxe Waffle: сітка 7×7 з 8 семилітерними словами, щотижнева (у березні 2022 — «секретна вафля», розвʼязали ~17 %).
- Number Waffle: числа 1–7 замість літер, кожен рядок/стовпець містить 1–7, обвідні підказки-суми; 20 обмінів, мінімум 15.
- Undo, hint — нема (?).

## Варіації й родичі
- Wordle (джерело кольорів), Squardle (той самий «хрест» з 6 слів, але введенням спроб, а не обміном), кросворд.
- Sliding/swap-пазли (15-puzzle, Loopover) — та сама перестановочна природа, але без семантики.
- **Осі варіацій:** розмір вафлі (5×5 / 7×7) · алфавіт (літери / числа з сумами) · що є ходом (обмін довільних двох / зсув ряду / введення слова) · кольори для перетинів (будь-яке з двох слів / окремі кольори рядка й стовпця, як у Squardle) · бюджет (мінімум + 5 / мінімум + 5 у Number Waffle).

## Цікавинки для курсу
- Обмін двох плиток drag-n-drop + перерахунок кольорів — 📎.
- Фідбек для клітин, що належать двом словам, з повтореними літерами — 🥉: два набори лічильників і правило «яке слово рахувати».
- Мінімальна кількість обмінів = 21 − кількість циклів перестановки; з повтореними літерами треба обрати перестановку з максимумом циклів — 🥇.
- Зірки за невикористані ходи + статистика зірок — 🌱.
- Генератор: 6 слів, що схрещуються, + перемішування рівно на 10 обмінів з єдиним розвʼязком — 👑 (дитина `unique-puzzle-generation`).

## Мапа на каталог
- Є: `daily-puzzle` · `drag-drop-piece` ↔ перетягування літери · `completion-detection` ↔ усі зелені · `profile-stats` ↔ статистика · `level-bank` ↔ архів · `end-screen` · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+swap-tiles` «Обмін двох плиток місцями» · entities/legality · 📎 · слоти {range: any|adjacent} — Waffle, Bejeweled (adjacent).
  - `+move-budget` «Ліміт ходів на рівень» · game-logic/lose · 🌱 · слоти {moves: int}.
  - `+letter-feedback` — див. wordle.md.
  - `+intersection-feedback` «Фідбек для клітини на перетині двох слів» · game-logic/constraints · 🥉.
  - `+stars-by-moves` «Зірки за зекономлені ходи» · game-logic/score · 🌱 (близька до ⏳ `stars-rating`).
  - `+share-result`, `+streak-stats` — див. wordle.md.
  - `+min-swaps-cycles` «Мінімум обмінів через цикли перестановки» · levels/solvability · 🥇.

## Пропозиції до словників
- `+trigger:input` — тут drag однієї плитки на іншу.
- `+effect:swap` — у словнику ⏳; тут головний ефект гри.
- `+effect:feedback` — кольори всіх клітин після ходу.
- `+cond:in_word` — літера входить у слово (рядок/стовпець), без позиції.
- `+role:tile`.
- `+ui:swaps-left` — лічильник лишених ходів (варіант `move-counter` у зворотний бік); `+ui:stars-rating` — зірки на кінці.
- `+window:stats-window`; `+window:archive-window` — архів минулих щоденних задач, окремий від статистики.
- `+feature:share-result`, `+feature:streaks`.
- `+axis:session` — `daily` + щотижневий спецвипуск.

## Джерела
- ⭐ [Waffle — Daily](https://wafflegame.net/daily) — грати; How to play: 15 обмінів, мінімум 10, зірки, кутові літери, повтори, Number Waffle, Deluxe, архів, статистика.
- [arXiv: Mathematics of the NYT daily word game Waffle](https://arxiv.org/html/2501.09286v2) — формальні правила кольорів, 21 клітина, цикли перестановки, мінімум обмінів, складність.
- [WordFinder: інтервʼю з James Robinson](https://wordfinder.yourdictionary.com/blog/waffle-game-creator-james-robinson-talks-inspiration-behind-his-multi-word-puzzle) — історія (Reddit, 13.02.2022), чому вафля, Deluxe 7×7.
- [PC Gamer про Waffle](https://www.pcgamer.com/a-wordle-inspired-game-called-waffle-has-become-more-popular-than-actual-waffles) — популярність (текст статті не прочитано).
- YouTube: пошук «waffle word game gameplay».

## Непевне
- (?) Назва статті Glasby згадує «NYT daily word game», але Waffle — незалежна гра James Robinson; NYT її не купувала (наскільки відомо).
- (?) Зелені плитки заблоковані від перетягування — з памʼяті.
- (?) На поразці гра показує розвʼязок; кількість обмінів для Deluxe (7×7) — не знайдено.
- (?) Точне правило повторених літер (коли саме друга копія стає сірою) — довідка каже лише «може лишатися жовтою, доки одна копія не на місці»; Glasby прямо пише, що правила повторів складніші й не описані.
- (?) Тап-тап як альтернатива drag — з памʼяті.
