---
title: Chessformer
slug: chessformer
aka: [Chess Platformer]
family: chess-abstract
also: [grid-platformer, thinky]
klass: figure
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1701190", best: true, note: "опис ядра: фігури ходять як у шахах, після ходу падають; мета — взяти нерухомого короля"}
  - {kind: other, url: "https://steamcommunity.com/app/1701190/reviews/?browsefilter=toprated", note: "відгуки: 48 рівнів, undo/reset, стіни, ключі й кнопки, вибір фігур"}
  - {kind: itch, url: "https://berkefiliz.itch.io/gravity-grid", note: "Gravity Grid (2024) — браузерний наступник «за мотивами»: чорні бʼють, портали, мости, редактор"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=chessformer+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, piece-capture, gravity-fall, impassable-cells, key-and-door, button-toggle, pawn-promotion, legal-move-highlight, selection-highlight, cell-click, undo-unlimited, restart-level, sequential-levels, level-unlock, level-select, save-progress, placement-screen, game-screen, main-menu, movement-animation, fixture-level-tests, +gravity-chess, +piece-stacking, +static-target-king]
proposes: ["+effect:stack_on", "+cond:falling", "+card:gravity-chess", "+card:piece-stacking", "+card:static-target-king", "+axis:gravity"]
author: opus
date: 2026-11-09
---

# Chessformer — шахові фігури в бічному розрізі: походив — упав, мета — дістати нерухомого короля

## Суть
Пазл-платформер, де поле — вертикальний розріз рівня, а гравець рухає білі шахові фігури за звичайними патернами ходу. Після кожного ходу фігура **падає вниз**, доки не стане на опору, і не може ходити знову, поки не впала. Мета рівня — взяти червоного короля, який ніколи не рухається; власні втрати значення не мають. Ядро — комбінація «патерн ходу × гравітація × фігури як опора одна для одної».

## Поле і час
- Квадратна сітка, вигляд збоку: «вниз» — напрям гравітації. Стіни/підлога — непрохідні клітини; порожнеча під фігурою = падіння.
- Покроково без суперника: хід = переміщення однієї фігури; суперник не відповідає (король статичний).
- Після ходу фігура падає по вертикалі до першої опори (стіна або інша фігура). Фігура в падінні недоступна для ходу.
- Рівні — окремі пазли; за відгуком гравця — 48 рівнів, відкриті порціями по 5.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пішак | piece | перший хід | хід на 2 вперед (перший) або 1; «вперед» — угору екрана; дійшовши до верху, міняється на іншу фігуру |
| Кінь | piece | — | L-стрибок; **єдиний**, хто перескакує стіни |
| Слон | piece | — | діагональ на будь-яку відстань до перешкоди |
| Тура | piece | — | пряма на будь-яку відстань до перешкоди |
| Ферзь | piece | — | тура + слон |
| Король (свій) | piece | — | 1 клітина в будь-який бік |
| Червоний король | enemy | нерухомий | ціль: взяти його будь-якою фігурою |
| Стіна / блок | static | — | непрохідна; опора для падіння |
| Порожнеча | terrain | — | фігура над нею падає |
| Ключ | pickup | — | відмикає клітини (див. замок) |
| Кнопка | switch | постійна / тимчасова | відмикає клітини назавжди або поки натиснута |
| Замкнена клітина | gate | закрито / відкрито | непрохідна, доки ключ/кнопка не відчинить |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, piece)` → ЯКЩО `not custom: «фігура падає»` (`+cond:falling`) → ТО `custom: «показати її ходи до зняття виділення»`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `legal(move)` і `free(to)` → ТО `move(piece, to)`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «на шляху стіна»` і `not` кінь → ТО `block`.
- КОЛИ `after(move)` → ЯКЩО `not supported(piece)` → ТО `fall(piece)`.
- КОЛИ `after(fall)` → ЯКЩО `occupied(cell_below, piece)` → ТО `custom: «стає на фігуру — фігура є опорою»` (`+effect:stack_on`).
- КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «фігура ще в падінні»` (`+cond:falling`) → ТО `block`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, red_king)` і `legal(move)` → ТО `disappear_b`, `win`.
- КОЛИ `reach(pawn, top_row)` → ТО `custom: «замінити пішака іншою фігурою»` (`transform(piece)`).
- КОЛИ `contact(piece, key)` → ТО `pickup`, `set_cell(lock, floor)`.
- КОЛИ `contact(piece, button)` → ЯКЩО `state(button, permanent)` → ТО `set_cell(lock, floor)`; інакше відчинено, поки `occupied(button, piece)`.
- КОЛИ `input(undo)` → ТО `custom: «повернути попередній стан»` (без ліміту); `input(reset)` → `restart`.
- Перемога: король узятий · Поразка: нема (застряг — undo/reset) · Рахунок: нема.

## Керування і ввід
- Лише миша: клік по фігурі — виділення й підсвітка ходів; клік по клітині — хід.
- `U` — undo без ліміту, `R` — reset, `Esc` — вийти з рівня без втрати прогресу; іконки на екрані дублюють клавіші.
- Пізні рівні: гравець сам обирає набір фігур перед стартом.

## Вікна, меню, HUD
- `main-menu`: Грати → `level-select`; вихід.
- `level-select`: сітка рівнів, відкриті порціями (за відгуком — без номерів на плитках).
- `placement-screen` / `character-select` (пізні рівні): вибір своїх фігур.
- `game-screen`: поле, `selection-highlight`, `legal-move-highlight`, `undo-button`, `restart-button`.
- `end-screen` (?): перехід до наступного рівня.
- Переходи: main-menu → level-select → game-screen → (король узятий) наступний рівень / level-select.

## Фічі поза полем
- `undo` (∞), `restart-level`, `level-unlock` порціями, `save-progress` (Steam Cloud), `achievements` (Steam).
- Редактора нема — гравці просять Workshop.

## Варіації й родичі
- **Gravity Grid** (2024, браузер, Berke) — «за мотивами»: чорні фігури бʼють твої, щойно можуть; нові фігури Grasshopper і Butterfly; блоки Portal, Bridge, Stripes міняють рух; заморожування фігур у полі зору; редактор і обмін рівнями, рейтинг «за найменше ходів».
- Інші «шахи з гравітацією»: Gravity Chess (LD41), GraviChess — окремі ігри, не плутати.
- Осі варіацій: **гравітація** (нема / вниз після ходу / по типах) · **суперник** (статичний король / реактивні чорні) · **фігури** (класичні / казкові) · **опора** (лише стіни / фігури теж).
- Родичі в корпусі: `chess.md` (патерни), `chess-rule-twists.md` (правила-«надбудови»), `grid-platformer/catrap.md` і `toki-tori.md` (пазл-платформер з undo), `dig-gravity/*` (падіння).

## Цікавинки для курсу
- Генерація ходів шахових фігур + фільтр стін + виняток коня — 📎.
- Гравітація після ходу з опорою на інші фігури (стоси) — 🥉: порядок падіння, коли кілька фігур нависають одна над одною.
- Розвʼязувач BFS по станах «позиції фігур» з мінімальною кількістю ходів — 🥇 (простір станів великий, треба хеш).
- Ключі й кнопки (постійні / поки натиснута) поверх шахів — 📎.
- Undo без ліміту як стек станів — 🥉.
- Рівень із txt (символи фігур, стін, короля) + фікстура «розвʼязок за N ходів» — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ фігури · `piece-capture` ↔ взяття короля · `gravity-fall` ↔ падіння після ходу · `impassable-cells` ↔ стіни · `key-and-door`, `button-toggle` · `pawn-promotion` ↔ заміна пішака вгорі · `legal-move-highlight`, `selection-highlight`, `cell-click` · `undo-unlimited`, `restart-level` · `sequential-levels`, `level-unlock`, `level-select`, `save-progress` · `placement-screen` ↔ вибір фігур.
- **Нема** → пропозиції карток:
  - `+gravity-chess` «Шахові фігури під гравітацією» · entities/move · 🥉 · слоти {when: after-move, support: walls|pieces} — патерн ходу + падіння.
  - `+piece-stacking` «Фігура як опора» · entities/legality · 🥉 — стоси фігур, нижня тримає верхню.
  - `+static-target-king` «Нерухома ціль-король» · game-logic/win · 🌱 — шаховий пазл без ходів суперника.

## Пропозиції до словників
- `+effect:stack_on` — фігура приземлилась на іншу й тримається на ній (стос).
- `+cond:falling` — сутність у падінні й тимчасово не керована.
- `+axis:gravity` — значення `down` (тут вісь чисто «після ходу»).
- `+card:gravity-chess`, `+card:piece-stacking`, `+card:static-target-king` — див. «Мапа на каталог».

## Джерела
- ⭐ [Steam: Chessformer](https://store.steampowered.com/app/1701190) — опис механіки: падіння після ходу, стоси як ключ до рівнів, мета — король, що не рухається; Mouse Only, Steam Cloud, досягнення.
- [Steam: відгуки](https://steamcommunity.com/app/1701190/reviews/?browsefilter=toprated) — 48 рівнів, порції по 5, unlimited undo (U) і reset (R), кінь стрибає через стіни, пішак 2/1, заміна пішака вгорі, ключі й кнопки, вибір фігур, прохання редактора.
- [itch.io: Gravity Grid](https://berkefiliz.itch.io/gravity-grid) — наступник «inspired by Chessformer».
- YouTube: пошук «chessformer gameplay».

## Непевне
- (?) Чи фігура падає вже **під час** ходу (тура «над прірвою») чи лише після приземлення на цільову клітину — джерела не уточнюють.
- (?) «Не може ходити, поки падає» натякає на анімоване падіння в реальному часі — можливо, можна ходити іншою фігурою, поки ця ще падає; не перевірено.
- (?) Як саме гравець «втрачає» фігури (Steam: «втрати не важать») — падіння за край? взяття? не з'ясовано.
- (?) Як пішак бʼє (діагональ угору?) і на що саме міняється вгорі (вибір чи фіксовано).
- (?) Чи є end-screen між рівнями; 48 рівнів і порції по 5 — з одного відгуку.
