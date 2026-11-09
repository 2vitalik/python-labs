---
title: Tetrisweeper
slug: tetrisweeper
aka: []
family: hidden-deduction
also: [falling-match]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: hidden
  random: runtime
  goal: score
year: 2020
platforms: [web (HTML5), Windows]
links:
  - {kind: itch, url: "https://kertisjones.itch.io/tetrisweeper", best: true, note: "грати в браузері; правила очищення ліній, види очищень, game over, доступність, лідерборд"}
  - {kind: other, url: "https://kertisjones.itch.io/tetrisweeper/devlog/533579/tetrisweeper-v17", note: "v1.7: Clear on Lock, Cleanse, множник ×50, бали за 8, Marathon → Endless"}
  - {kind: other, url: "https://kertisjones.itch.io/tetrisweeper/devlog", note: "девлог 2023–2024: акорд (1.2), ghost piece (1.4), автокліанс (1.8.4), handling"}
  - {kind: steam, url: "https://store.steampowered.com/app/2918460/Tetrisweeper/", note: "лінк з девлогу «now on Steam» (16.04.2024); сторінку не відкрив"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Tetrisweeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [gravity-fall, piece-rotate-flip, next-queue, keyboard-controls, cell-click, chord-click, neighbor-count-clue, flood-reveal, combo-multiplier, event-points, chain-reaction, score-records, leaderboard, keep-playing-after-win, controls-remap, game-settings, volume-control, game-pause, save-progress, mode-select, game-screen, end-screen, +line-clear, +ghost-piece, +hold-piece, +lock-delay, +hard-drop, +t-spin-detection, +back-to-back, +solve-to-clear-line, +clear-on-lock, +cleanse-piece, +multiplier-drain, +dual-input-coop]
proposes: ["+trigger:locked", "+cond:row_solved", "+effect:cleanse", "+effect:hard_clear", "+ui:multiplier-drain-meter", "+ui:best-today", "+feature:handling-settings", "+feature:mode-marathon-to-endless", "+card:solve-to-clear-line", "+card:clear-on-lock", "+card:cleanse-piece", "+card:multiplier-drain", "+card:dual-input-coop"]
author: opus
date: 2026-11-09
---

# Tetrisweeper — Tetris і сапер одночасно: заповнений ряд зникає лише тоді, коли його клітини-сапери розвʼязано

## Суть
Тетроміно падають як у Tetris, але кожна клітина фігури — клітина сапера з можливою прихованою міною. Повний ряд ще не зникає: його треба «розмінувати» — правильно відкрити й позначити прапорцями кожну клітину, і лише тоді ряд очищується. Одна рука веде фігури клавіатурою, друга мишею розвʼязує сапер; програш — вежа до стелі або клік по міні.

## Поле і час
- Склянка Tetris (квадратна сітка); «поле росте, поки граєш»: пазл сапера складається з викладених фігур.
- Реальний час: гравітація, lock delay з лімітом 15 скидань (Guideline move-reset), швидкість зростає з рівнем (?).
- Числа рахують міни серед 8 сусідів у викладеній вежі (?) — механіка чисел на сторінці не пояснена.
- Розвʼязані ряди очищуються при фіксації наступної фігури (Clear on Lock, v1.7); фігури над ними осідають каскадом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Активне тетроміно | player | форма, поворот | падає, рухається, обертається, фіксується |
| Клітина-тайл | tile | міна / безпечна, число | після фіксації — клітина сапера |
| Міна | hazard | — | клік ЛКМ по ній = кінець гри |
| Прапорець | mark | — | ПКМ; потрібен на кожній міні ряду, щоб ряд зарахувався |
| Повний ряд | zone | розвʼязано / ні | зникає, якщо всі клітини відкриті або правильно позначені |
| «Очищене» тетроміно | object | без мін, відкрите | приходить за вправне викладення (Cleanse) |
| Тінь фігури | mark | — | показує, куди впаде (v1.4) |
| Стінні тайли (wall tiles) | resource | — | валюта Cleanse: 4 за раз (v1.7) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `fall(piece)`; КОЛИ `input(move|rotate, dir)` → ТО `move(piece, dir)` / `rotate(piece, 90)`.
- КОЛИ `input(hard_drop)` → ТО `fall(piece)` до упору; ЯКЩО `custom: «впала хоч на 1 ряд»` → ТО `multiplier(+k)`.
- КОЛИ `locked(piece)` → ТО `custom: «клітини фігури стають клітинами сапера з прихованими мінами»`.
- КОЛИ `input(reveal, c)` → ЯКЩО `not occupied(c, mine)` → ТО `reveal(c)` з числом (?); `occupied(c, mine)` → ТО `game_over`.
- КОЛИ `input(chord, c)` → ЯКЩО `custom: «прапорців довкола = число»` → ТО `reveal(neighbors8 без прапорців)` (v1.2).
- КОЛИ `pattern(row_full)` → ТО `score(n)` («Line Filled»; 4 ряди — Tetris; T-spin окремо).
- КОЛИ `custom: «усі клітини повного ряду відкриті або позначені правильно»` → ТО `custom: «ряд розвʼязано»` («Line Cleared»).
- КОЛИ `locked(next_piece)` → ЯКЩО `custom: «є розвʼязані ряди»` → ТО `clear(rows)`, `fall(blocks_above)` (Clear on Lock).
- КОЛИ `custom: «ряд розвʼязано до фіксації наступної фігури»` → ТО `score(×1.5)` (Linesweep / Tetrisweep / T-Spinsweep); підряд Tetrisweep чи T-Spinsweep — ще ×1.5 (back-to-back).
- КОЛИ `custom: «поле порожнє після очищення»` → ТО `score(n)` («Perfect Clear»).
- КОЛИ `custom: «відкрито або утворено 8»` → ТО `score(8888)`.
- КОЛИ `input(hard_clear)` → ТО `clear(solved_rows)` негайно, `reset_combo`, `custom: «множник скинуто»`; автоматично — коли вежа ось-ось упреться в стелю.
- КОЛИ `input(cleanse)` → ЯКЩО `counter(wall_tiles, >=, 4)` → ТО `custom: «зняти всі міни з фігури в hold і відкрити її клітини»`, `counter(wall_tiles, -4)`, `score(250)` (v1.7; з v1.8.4 — автоматично).
- КОЛИ `tick` → ЯКЩО `custom: «минула затримка після приросту»` → ТО `multiplier(-drain)`; швидкість спаду росте з рівнем, стеля ×50.
- КОЛИ `custom: «вежа досягла верху (Guideline top-out)»` → ТО `game_over`.
- КОЛИ `custom: «Marathon завершено»` → ТО `window(end-screen)`, `choose(end|endless)`.
- Перемога: — (Marathon має кінець, далі Endless) · Поразка: top-out або клік по міні · Рахунок: очки × множник.

## Керування і ввід
- Клавіатура — фігури (рух, обертання, hard/soft drop, hold); миша — сапер: ЛКМ відкрити, ПКМ прапорець, обидві / середня — акорд.
- F / F2 — Cleanse (до 1.8.4); Backspace / F1 — примусове очищення.
- Перепризначення клавіш; геймпад (гравці: тригер на обертання); handling: ARR, SDF (зокрема нескінченний), затримка вводу сапера після очищення (50 мс за замовчуванням).
- Кооператив 1–2 гравці на одному компʼютері: один веде Tetris, другий — сапер (за коментарем).
- Пауза з кулдауном 0,4 с.

## Вікна, меню, HUD
- `main-menu` (title menu з посиланнями назовні) → `mode-select` (Marathon, Endless (?)).
- `game-screen`: склянка, `next-queue`, hold, `ghost-piece`, очки, множник з індикатором затримки, «Best Today», опційно — індикатор lock delay і превʼю на 4 тайли.
- `settings-window`: керування, handling, окремі гучності музики й SFX, відео (превʼю), доступність.
- `pause-menu` · `end-screen` з переходом в Endless · `leaderboard`.

## Фічі поза полем
- `mode-marathon` → `mode-endless`; `leaderboard-online` (?) — є таблиця рекордів.
- `remap-controls`, `colorblind-palette`, `high-contrast`, субтитри; збереження даних між сесіями.
- Таблиця очок і множників — у зовнішній Google-таблиці автора (за описом).

## Варіації й родичі
- Батько з боку Tetris: [tetris](../falling-match/tetris.md) (Guideline: SRS, T-spin, back-to-back); з боку сапера — [minesweeper](minesweeper.md).
- Інші гібриди сапера з динамікою: [mamono-mower](mamono-mower.md) (реальний час), [mined-out](mined-out.md).
- **Осі варіацій**: умова очищення ряду = заповнення / заповнення + розвʼязок; час на розвʼязок = миттєво / до фіксації наступної фігури / вручну (hard clear); допомога = нема / очищені фігури.

## Цікавинки для курсу
- Подвійна умова очищення: `row_full` і «ряд розвʼязано» — 📎.
- Clear on Lock: відкладене очищення до наступної фіксації — 🌱.
- Генерація мін у фігурі так, щоб сапер у вежі лишався розвʼязним — 🥇.
- Множник із затримкою й спадом, що росте з рівнем — 🌱.
- Cleanse як витрата ресурсу на «чисту» фігуру — 🌱.
- Ввід двома пристроями одночасно (клавіатура — Tetris, миша — сапер) або двома гравцями — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `piece-rotate-flip` · `next-queue` · `keyboard-controls` · `cell-click` + `chord-click` · `neighbor-count-clue` · `flood-reveal` (?) · `combo-multiplier` + `event-points` · `chain-reaction` ↔ каскад осідання · `score-records` + `leaderboard` · `keep-playing-after-win` ↔ Marathon → Endless · `controls-remap` · `volume-control`.
- **Нема** → пропозиції карток:
  - `+solve-to-clear-line` «Ряд зникає лише розвʼязаним (клітини-сапери)» · game-logic/constraints · 📎.
  - `+clear-on-lock` «Очищення відкладено до наступної фіксації» · entities/interact · 🌱.
  - `+cleanse-piece` «Фігура без мін за ресурс» · entities/state · 🌱.
  - `+multiplier-drain` «Множник спадає після затримки» · game-logic/score · 🌱.
  - `+dual-input-coop` «Дві підігри на двох пристроях / двох гравцях» · game-logic/opponent · 📎.
  - Решта `+` — як у Tetris (`+line-clear`, `+ghost-piece`, `+hold-piece`, `+lock-delay`, `+hard-drop`, `+t-spin-detection`, `+back-to-back`).

## Пропозиції до словників
- `+trigger:locked` — фігура зафіксувалась (уже ⏳-кандидат у Tetris; тут ключовий для Clear on Lock).
- `+cond:row_solved(row)` — усі клітини ряду відкриті або правильно позначені.
- `+effect:cleanse(piece)` — зняти міни з фігури й відкрити її.
- `+effect:hard_clear` — примусово очистити розвʼязані ряди ціною комбо.
- `+ui:multiplier-drain-meter` — множник з видимою затримкою спаду · `+ui:best-today`.
- `+feature:handling-settings` (ARR/SDF/lock delay) · `+feature:mode-marathon-to-endless`.

## Джерела
- ⭐ [itch.io: Tetrisweeper](https://kertisjones.itch.io/tetrisweeper) — правила, види очищень, game over, доступність, лідерборд.
- [v1.7](https://kertisjones.itch.io/tetrisweeper/devlog/533579/tetrisweeper-v17) — Clear on Lock, Cleanse, множник, очки, Marathon/Endless.
- [Девлог](https://kertisjones.itch.io/tetrisweeper/devlog) — акорд, ghost piece, автокліанс, handling.
- [Steam](https://store.steampowered.com/app/2918460/Tetrisweeper/) — лінк з девлогу; сама сторінка не відкрилась (редирект на головну).

## Непевне
- (?) Як рахуються числа: лише всередині фігури чи по всій вежі через межі фігур; як розміщуються міни.
- (?) Чи є каскад нулів.
- (?) Звідки беруться wall tiles (Linesweep їх більше не дає) і як працює автоматичний Cleanse з 1.8.4.
- (?) Скільки рівнів у Marathon, зростання швидкості, бали за Line Filled / Tetris.
- (?) Чи є режими, крім Marathon і Endless; локальний кооп — за коментарем.
