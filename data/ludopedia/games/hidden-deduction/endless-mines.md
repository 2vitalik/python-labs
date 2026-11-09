---
title: endless mines
slug: endless-mines
aka: [Endless Mines]
family: hidden-deduction
also: [falling-match]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: hidden
  random: runtime
  goal: survive
year: null
platforms: [web (HTML5, itch.io), mobile browser (touch)]
links:
  - {kind: itch, url: "https://ruin.itch.io/endless-mines", best: true, note: "автор ruin; гра в браузері; правила: розвʼязані рядки зникають, вибух блокує рядок, кінець — коли в кожному рядку вибухла міна; є туторіал"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=endless+mines+ruin+itch+minesweeper", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [cell-click, chord-click, neighbor-count-clue, tutorial-window, game-screen, end-screen, infinite-field, +row-clear-when-solved, +row-lock-on-mine, +locked-rows-as-lives, +touch-hold-flag]
proposes: ["+trigger:row_solved", "+effect:lock_row", "+feature:one-button-mode", "+card:row-clear-when-solved", "+card:row-lock-on-mine", "+card:locked-rows-as-lives", "+card:touch-hold-flag"]
author: opus
date: 2026-11-09
---

# endless mines — сапер-«тетріс»: розвʼязаний рядок зникає, рядок із вибухом лишається назавжди

## Суть
Браузерний мешап Minesweeper і Tetris. Правила відкриття — сапер, але рядок, де все розвʼязано, зникає, а поле продовжується далі, тож гра нескінченна. Клік по міні не вбиває одразу: він «запечатує» свій рядок — той уже ніколи не зникне. Гра закінчується, коли в кожному рядку поля є вибухла міна: запечатані рядки працюють як втрачені життя.

## Поле і час
- Прямокутне поле фіксованої висоти (?) — з точки зору гравця смуга рядків, що оновлюється: зниклий рядок поступається місцем новому згенерованому (?).
- Сусідство — як у сапері (8 (?)), числа рахують міни серед сусідів, у тому числі через межу щойно доданого рядка.
- Час статичний: тиску таймера нема (тег «Relaxing»); сесія — кілька хвилин.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Закрита клітина | static | — | відкрити / прапорець |
| Число | mark | n = міни серед сусідів | підказка; клік по числу відкриває незапрапорених сусідів |
| Міна | hazard | — | клік → вибух, але не кінець гри |
| Вибухла міна | hazard | — | лишається в рядку; рядок більше не зникає |
| Прапорець | mark | — | права кнопка / утримання; можливо, потрібен для зникнення рядка (?) |
| Рядок | zone | стан: відкритий / запечатаний | розвʼязаний → зникає; з вибухом → запечатаний |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(open, c)` → ЯКЩО `not cell(c, mine)` → ТО `reveal(c)` зі значенням `adjacent_count(c, mine)`.
- КОЛИ `input(open, c)` → ЯКЩО `cell(c, mine)` → ТО `explode(c)`, `custom: «рядок c запечатано — більше не зникне»`.
- КОЛИ `input(flag, c)` → ТО `mark(c, flag)`.
- КОЛИ `input(open, n)` → ЯКЩО `cell(n, opened)` → ТО `reveal(закриті незапрапорені сусіди n)` (акорд кліком по числу).
- КОЛИ `pattern(row_full)` → ЯКЩО `custom: «рядок розвʼязано і в ньому нема вибуху»` → ТО `clear(row)`, `drop_rows`, `custom: «додати новий згенерований рядок»` (?).
- КОЛИ `custom: «у кожному рядку поля є вибухла міна»` → ТО `lose` / `game_over`.
- Перемоги нема — нескінченна гра. · Поразка: усі рядки запечатані. · Рахунок: очки (за зниклі рядки?) — правила автора не пояснюють.

## Керування і ввід
- Ліва кнопка / тап — відкрити клітину.
- Права кнопка / утримання — прапорець.
- Клік / тап по числу — відкрити незапрапорених сусідів.
- Позначено як придатне для «one button» та тач-екрана.

## Вікна, меню, HUD
- `tutorial-window`: навчальний режим для старту.
- `game-screen`: поле-смуга рядків, рахунок (?).
- `end-screen`: кінець, коли всі рядки запечатані (?).
- Доступність за тегами itch: color-blind friendly, high-contrast, interactive tutorial, one button.

## Фічі поза полем
- `tutorial`, `colorblind-palette`, `high-contrast`, `touch-controls`, `one-button-mode`.

## Варіації й родичі
- [minesweeper](minesweeper.md) — основа відкриття; [minesweeper-infinite](minesweeper-infinite.md) — нескінченність у просторі замість часу; [kaboom](kaboom.md) і [voltorb-flip](voltorb-flip.md) — інші способи «пробачити» міну.
- Межа з `falling-match`: зникнення заповненого рядка — Tetris, але без падіння фігур.
- Осі варіацій: **ціна вибуху** — кінець гри / життя / запечатаний рядок; **умова зникнення** — усі безпечні відкриті / усі міни з прапорцями; **подача рядків** — по одному після очищення / за таймером (Tetris-тиск).

## Цікавинки для курсу
- Рядок, що зникає після розвʼязання, + зсув поля й генерація нового рядка — 📎: перерахунок чисел на межі.
- Запечатаний рядок як «життя» — 🌱: поразка = усі рядки з вибухом.
- Варіант з таймером подачі рядків (Tetris-тиск) — 🥉: перехід `static` → `realtime`.
- Генерація нового рядка, узгоджена з уже відкритими числами сусіднього — 🥉.

## Мапа на каталог
- Є: `cell-click` · `chord-click` ↔ клік по числу · `neighbor-count-clue` · `tutorial-window` · `game-screen` · `end-screen` · `infinite-field` ↔ нескінченна подача рядків.
- **Нема** → пропозиції карток:
  - `+row-clear-when-solved` «Розвʼязаний рядок зникає» · entities/interact · 📎.
  - `+row-lock-on-mine` «Помилка запечатує рядок» · game-logic/lose · 🌱.
  - `+locked-rows-as-lives` «Запечатані рядки = втрачені життя» · game-logic/lose · 🌱.
  - `+touch-hold-flag` «Утримання = прапорець на тачі» · interface/input · 🌱.

## Пропозиції до словників
- `+trigger:row_solved` — рядок розвʼязано за правилами пазла (не те саме, що `pattern(row_full)`).
- `+effect:lock_row` — позначити рядок як незнищенний.
- `+feature:one-button-mode` — гра одним вводом (тег доступності itch).

## Джерела
- ⭐ [itch.io: endless mines](https://ruin.itch.io/endless-mines) — автор ruin; «Clicking on a mine will prevent that row from being cleared»; кінець — «when every row contains an exploded mine»; керування мишею й тачем; туторіал; теги доступності; коментарі гравців про умову зникнення рядка.
- YouTube: пошук «endless mines ruin itch minesweeper».

## Непевне
- (?) Точна умова зникнення рядка: коментатор пише — лише коли всі міни рядка з прапорцями, інший — що автоматично; автор не уточнює.
- (?) Звідки беруться нові рядки (знизу/згори, одразу після зникнення) і чи висота поля фіксована.
- (?) Сусідство 8 і каскад нулів — очікувано, не перевірено.
- (?) Рахунок і рік випуску — на сторінці нема.
