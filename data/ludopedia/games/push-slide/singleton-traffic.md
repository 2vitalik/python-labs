---
title: Singleton Traffic (Toph Wells)
slug: singleton-traffic
aka: []
family: push-slide
also: [thinky]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2014
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=eb0f9102f85b5ea536b1", best: true, note: "грати в браузері (PuzzleScript), 6 рівнів"}
  - {kind: other, url: "https://api.github.com/gists/eb0f9102f85b5ea536b1", note: "повний код: блокування поперек осі, рух потягом, перевірка «ніщо не рухається», індикатори"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Singleton+Traffic+puzzlescript", note: "пошук; геймплей"}
stage: v1
coverage: 85
mechanics: [move-4dir, keyboard-controls, no-moves-left, highlights, sequential-levels, undo-unlimited, restart-level, level-from-txt, sound-effects, +move-all-with-player, +cross-axis-lock, +no-moves-win]
proposes: ["+cond:neighbor_on_axis", "+ui:lock-marker", "+card:cross-axis-lock", "+card:no-moves-win"]
author: opus
date: 2026-11-09
---

# Singleton Traffic — усі плитки їдуть від одного вводу, сусід поперек осі блокує рух; перемога — коли ніщо не може рухатись

## Суть
PuzzleScript-гра Toph Wells: на полі лише однакові плитки, і стрілка рухає **всі** одночасно на одну клітину. Плитка не їде горизонтально, якщо має сусіда згори чи знизу, і не їде вертикально, якщо має сусіда зліва чи справа — тож тільки самотні плитки («singleton») вільні в усіх напрямках. Мета перевернута: не довести щось до цілі, а заклинити поле так, щоб жодна плитка вже не могла зрушити.

## Поле і час
- Квадратна сітка 8×8 … 13×8 (шість карт: 11×9, 10×10, 8×8, 8×8, 9×13, 13×8).
- Рамка поля — не стіни, а ті самі плитки: кутові мають сусідів по обох осях і стоять завжди, тому тримають усю рамку.
- Хід = одне натискання; у межах ходу плитки зсуваються на 1 «потягом»: передня звільняє клітину, наступна заходить у неї.
- Шари: фон · плитки · індикатори H · індикатори V; індикатори малюються щоходу й на старті рівня (`run_rules_on_level_start`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Плитка | tile | маркери H/V | отримує рух з кожним вводом; заблокована по осі, якщо має сусіда поперек; їде на 1, якщо попереду вільно |
| Плитка рамки | tile | — | та сама плитка; кути заблоковані по обох осях → рамка нерухома |
| Порожня клітина | terrain | — | чорний фон, куди можна заїхати |
| Маркер H | mark | — | плитка має сусіда зліва/справа → вертикально не поїде |
| Маркер V | mark | — | плитка має сусіда згори/знизу → горизонтально не поїде |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `custom: «кожна плитка поля отримує рух dir»` (у коді всі плитки — обʼєкти Player).
- КОЛИ `input(dir)` → ЯКЩО `custom: «у плитки є сусід поперек dir»` → ТО `block` для цієї плитки.
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(tile, dir)`, `sound(sfx0)`; правило повторюється, доки є рухомі плитки з вільною клітиною попереду — ряд уздовж осі руху їде цілим.
- КОЛИ `input(dir)` → ЯКЩО `occupied(next_cell, tile)` і та не поїхала → ТО `block`; штовхання нема.
- Після ходу: КОЛИ `custom: «обидві клітини плитки по одній осі порожні»` → ЯКЩО `not custom: «по іншій осі плитка затиснута з обох боків»` → ТО `set_state(tile, can_move)`.
- КОЛИ `no_moves(tiles)` (жодна плитка не має `can_move`) → ТО `win`, `next_level`.
- КОЛИ `adjacent(tile, tile)` по вертикалі → ТО `mark(tile, V)`; по горизонталі → `mark(tile, H)`; старі маркери щоходу стираються.
- КОЛИ `input(z)` → ТО `undo(1)`, `sound(undo)` · КОЛИ `input(r)` → ТО `restart`.
- Перемога: на полі не лишилось жодної плитки, здатної зрушити. · Поразка: нема. · Рахунок: нема.

## Керування і ввід
- Стрілки / WASD — рух усіх плиток; кнопки дії нема (`noaction`).
- Z — undo без ліміту, R — рестарт; Esc — титул (стандарт PuzzleScript (?)).
- Керування «рукою»: аватара нема, ввід — це напрямок для всього поля одразу.

## Вікна, меню, HUD
- `splash-screen` / `main-menu` — титул PuzzleScript: назва, автор (?).
- `custom-window` — три екрани `message` з правилами перед першим рівнем: «Tiles can't move horizontally if there's something vertically adjacent.» · «…vertically if there's something horizontally adjacent.» · «You win when nothing can move.»
- `custom-window` — лічильник перед кожним рівнем із жартом: «1 OF 3» … «5 OF 3», «LAST OF 3».
- `game-screen` — поле; на плитках жовтогарячі маркери блокування H/V (HUD — самі плитки).
- Переходи: титул → правила → «N OF 3» → рівень → … → фінал.

## Фічі поза полем
- `levels-sequential` (6 рівнів), `undo` (∞), `restart-level`.
- Звуки: зсув плитки, undo, кінець рівня.
- Підказка вбудована в поле: маркери показують, яку вісь кожна плитка вже втратила.

## Варіації й родичі
- Осі варіацій:
  - **кого рухає ввід**: один аватар (`sokoban`) / усі ящики (`thinky/increpare-micro-puzzles`) / усі плитки до упору (`falling-match/2048`) / усі плитки на 1 (Singleton Traffic) / усі актори своєї осі (`thinky/elephant-in-a-bottle`);
  - **що блокує рух**: зайнята клітина / власна вісь фігури (`rush-hour`) / сусід поперек осі (Singleton Traffic);
  - **мета**: фігури на цілях / злиття до числа / повна нерухомість поля (Singleton Traffic).
- Родичі: `rush-hour`, `falling-match/2048`, `thinky/increpare-micro-puzzles`, `thinky/elephant-in-a-bottle`.

## Цікавинки для курсу
- Усі плитки — «гравці»: один ввід рухає всіх, рух потягом через повторне застосування правила — 📎.
- Блокування осі сусідом поперек — 🌱.
- Умова перемоги «ніщо не може рухатись»: локальна мітка рухомості на кожній плитці + глобальна перевірка — 📎.
- Рамка зі звичайних плиток замість стін — рівень як стан однакових обʼєктів — 🌱.
- Маркери блокування на плитках, що перераховуються щоходу — 🌱.
- Розвʼязувач BFS по позиціях плиток (4 детерміновані ходи зі стану) — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `no-moves-left` ↔ виявлення «ходів нема» (тут це перемога, а не поразка); `highlights` ↔ маркери H/V; `sequential-levels` ↔ 6 рівнів; `undo-unlimited` + `restart-level` ↔ Z / R; `level-from-txt` ↔ ASCII-карти; `sound-effects` ↔ звуки зсуву й undo.
- **Нема** → пропозиції карток:
  - `+move-all-with-player` (вже пропонована increpare) · слот {mode: step} — тут «гравець» = кожна плитка.
  - `+cross-axis-lock` «Сусід поперек осі забороняє рух уздовж неї» · entities/legality · 🌱.
  - `+no-moves-win` «Перемога — ніщо на полі не може рухатись» · game-logic/win · 📎 — дзеркало `no-moves-left`.

## Пропозиції до словників
- `+cond:neighbor_on_axis` — у сутності є сусід по осі h|v (блокування поперек осі; маркери H/V).
- `+ui:lock-marker` — позначка на сутності, яку вісь руху вона втратила.
- `+card:cross-axis-lock` · `+card:no-moves-win` — див. «Мапа на каталог».

## Джерела
- ⭐ [PuzzleScript: Singleton Traffic](https://www.puzzlescript.net/play.html?p=eb0f9102f85b5ea536b1) — гра в браузері.
- [GitHub Gist (API)](https://api.github.com/gists/eb0f9102f85b5ea536b1) — сирці: `[Perpendicular Player|Player] -> [Player|Player]`, рух `[> Player|No Player] -> [|Player]`, перевірка `[No Player|Player|No Player] -> [|Action Player|]` → `[Stationary Player] -> Win`, індикатори H/V, прапорці `noaction` і `run_rules_on_level_start`, 6 карт і повідомлення; гіст створено 30.04.2014.
- YouTube: пошук «Singleton Traffic puzzlescript».

## Непевне
- (?) Чи перевірка мітками точно збігається з «жодна плитка не зрушить» у всіх станах — виведено з коду аналізом випадків, у грі не перевірено.
- (?) Сайт автора (tophwells.com зі шапки гри) не відкривав; інші публікації гри не шукав.
- (?) Титул і фінальний екран — стандарт PuzzleScript, у цій грі не перевірені.
