---
title: Quordle / Octordle
slug: quordle
aka: [Quordle, Octordle, Dordle, Sedecordle]
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
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Quordle", best: true, note: "4 поля Wordle, 9 спроб, daily + practice, натхнення Dordle, Freddie Meyer, Merriam-Webster 2023"}
  - {kind: play, url: "https://www.merriam-webster.com/games/quordle/", note: "грати; JS-сторінка, fetch-ем вміст не прочитано"}
  - {kind: play, url: "https://www.merriam-webster.com/games/octordle/", note: "Octordle — 8 полів; octordle.com переадресовує сюди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=quordle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [daily-puzzle, keyboard-controls, cell-click, word-validation, completion-detection, mode-select, streak-stats, share-result, profile-stats, game-screen, help-window, settings-window, +letter-feedback, +multi-board, +keyboard-state, +split-keyboard-state]
proposes: ["+ui:split-key-state", "+ui:board-solved-badge", "+feature:mode-sequence", "+feature:mode-rescue", "+card:split-keyboard-state"]
author: opus
date: 2026-11-09
---

# Quordle / Octordle — одна спроба одразу в 4 (8) полів Wordle; розподіли 9 (13) спроб між усіма

## Суть
Це Wordle (`wordle.md`), де одночасно загадано 4 різних 5-літерних слова — по одному на поле. Кожне введене слово записується в усі ще не розвʼязані поля і отримує там свій кольоровий фідбек. На все — 9 спроб; спроба, корисна для одного поля, «витрачається» і в решті. Ядро — розподіл уваги й вибір спроби, що дає найбільше інформації сумарно по полях; Octordle доводить це до 8 полів.

## Поле і час
- 4 поля Wordle (2×2), кожне — 9 рядків × 5 клітин; спільна екранна клавіатура.
- Octordle — 8 полів, 13 спроб (?); Dordle — 2 поля, 7 спроб (?); Sedecordle — 16 полів (?).
- Хід = одне слово для всіх незакритих полів; часу нема.
- Сесія: щоденна задача (однакова для всіх) + practice — нескінченні випадкові.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Поле | zone | 9 × 5, власне загадане слово | приймає кожну спробу, доки не розвʼязане; потім заморожується |
| Загадане слово | static (приховане) | 5 літер, по одному на поле | різні в кожному полі (?) |
| Плитка-літера | tile | стан green/yellow/grey у своєму полі | як у Wordle, для кожного поля окремо |
| Клавіша клавіатури | tile (UI) | стан по кожному полю | поділена на 4 сектори кольорів (?) |
| Словник | static | допустимі спроби | спроба поза ним відхиляється |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(letter)` / `input(backspace)` → ТО `custom: «редагувати спільний рядок спроби у всіх незакритих полях»`.
- КОЛИ `input(enter)` → ЯКЩО `not in_dictionary(guess)` → ТО `message("Not a valid word")`, `shake` (?); спроба не витрачається.
- КОЛИ `input(enter)` → ЯКЩО слово валідне → ТО для кожного незакритого поля `feedback(guess)` (правило дублікатів — як у `wordle.md`), `counter(guesses, +1)`.
- КОЛИ `after(feedback)` → ЯКЩО `custom: «у полі рядок усіх green»` → ТО `set_state(board, solved)` — поле більше не приймає спроб.
- КОЛИ `after(feedback)` → ТО `paint(key[letter], state_per_board)` — клавіша показує стан окремо для кожного поля.
- КОЛИ `custom: «усі поля solved»` → ТО `win`, `window(stats-window)`.
- КОЛИ `counter(guesses, ==, 9)` → ЯКЩО `custom: «є нерозвʼязане поле»` → ТО `lose`, `message(answers)`.
- Перемога: усі 4 поля до 9-ї спроби · Поразка: 9 спроб, хоч одне поле не розвʼязане · Рахунок: номер спроби, на якій розвʼязано кожне поле (4 числа).
- Sequence (?): КОЛИ `custom: «поле розвʼязано»` → ТО `reveal(next_board)` — наступне поле стає видимим (попередні спроби в ньому вже з фідбеком).
- Rescue (?): КОЛИ `game_start` → ТО `custom: «перші кілька спроб уже введено за гравця»`.

## Керування і ввід
- Фізична клавіатура або екранна; Enter / Backspace — як у Wordle.
- Курсора по полях нема: спроба пишеться одночасно в усі незакриті поля.

## Вікна, меню, HUD
- `game-screen`: 4 поля 2×2, `on-screen-keyboard` з `split-key-state` (кожна клавіша поділена на сектори за полями) (?), `board-solved-badge` (номер спроби на розвʼязаному полі) (?).
- `mode-select`: Daily · Practice · Sequence · Rescue (?).
- `stats-window`: розподіл, серії, кнопка share (?).
- `help-window`, `settings-window` (тема, контраст (?)).

## Фічі поза полем
- `mode-daily` + `mode-practice` (Wikipedia).
- `share-result` — емодзі-сітка з номерами спроб по полях (?).
- `streaks`, `stats` (?).
- `mode-sequence`, `mode-rescue` (?) — модифікатори того самого ядра.

## Варіації й родичі
- Wordle (`wordle.md`) — одне поле; Dordle — 2 поля (натхнення Quordle); Octordle — 8; Sedecordle — 16 (?).
- Absurdle (`absurdle.md`), Nerdle (`nerdle.md`) — інші осі оболонки Wordle.
- **Осі варіацій:** кількість полів (1/2/4/8/16) · бюджет спроб (поля + 5 у Quordle, поля + 5 в Octordle (?)) · видимість полів (усі одразу / Sequence) · стартові спроби (порожньо / Rescue).

## Цікавинки для курсу
- Один ввід → N незалежних автоматів Wordle — 🌱: масив станів поля, одна функція фідбеку.
- Клавіатура з секторами по полях — 📎: похідний стан на N полів, рендер поділеної клавіші.
- Sequence: поле відкривається з уже накопиченим фідбеком попередніх спроб — 🌱.
- Розвʼязувач на кілька полів: спроба з максимумом сумарної ентропії, баланс «добити поле / розвідати решту» — 🥇.

## Мапа на каталог
- Є: `daily-puzzle` · `keyboard-controls` / `cell-click` ↔ ввід літер · `word-validation` ↔ словник спроб · `completion-detection` ↔ усі поля розвʼязано · `mode-select` ↔ Daily/Practice/Sequence/Rescue · `streak-stats` / `profile-stats` / `share-result` ↔ результати (?).
- Вже запропоновано у `wordle.md`: `+letter-feedback`, `+multi-board`, `+keyboard-state`.
- **Нема** → пропозиція картки: `+split-keyboard-state` «Клавіша зі станом по кожному з N полів» · interface/hud · 📎 (дитина `+keyboard-state`).

## Пропозиції до словників
- `+ui:split-key-state` — клавіша, поділена на сектори за полями.
- `+ui:board-solved-badge` — позначка на розвʼязаному полі (номер спроби).
- `+feature:mode-sequence` — поля відкриваються по черзі; `+feature:mode-rescue` — стартові спроби введено за гравця.
- `+card:split-keyboard-state` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Quordle](https://en.wikipedia.org/wiki/Quordle) — 4 поля, 9 спроб, кольори, daily і practice, Dordle, Freddie Meyer / David Mah, Merriam-Webster (січень 2023).
- [Merriam-Webster: Quordle](https://www.merriam-webster.com/games/quordle/) — грати (вміст не прочитано, JS).
- [Merriam-Webster: Octordle](https://www.merriam-webster.com/games/octordle/) — грати; адреса octordle.com переадресовує сюди.
- YouTube: пошук «quordle gameplay».

## Непевне
- (?) Режими Sequence, Rescue, Chill/Extreme, Weekly і їх правила — з памʼяті; сторінки Merriam-Webster віддали лише «Loading…».
- (?) Octordle — 13 спроб; Dordle — 7; Sedecordle — 16 полів і 21 спроба — з памʼяті.
- (?) Поділена на 4 сектори клавіша і позначка номера спроби на розвʼязаному полі — з памʼяті.
- (?) Чи можуть два поля мати однакове слово.
- (?) Share-сітка, статистика й серії.
