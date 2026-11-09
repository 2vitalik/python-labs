---
title: "increpare: Scalesoban і Explodoban"
slug: increpare-sokoban-variants
aka: [Scalesoban, Explodoban]
family: thinky
also: [push-slide]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2019
platforms: [web]
links:
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=08e343d25a15ad264003fdcb16f05763", best: true, note: "Explodoban — грати (7 рівнів)"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=08e343d25a15ad264003fdcb16f05763", note: "Explodoban — вихідний код PuzzleScript"}
  - {kind: play, url: "https://www.puzzlescript.net/play.html?p=0e8d097c183abae53c788320f198941a", note: "Scalesoban — грати (3 рівні)"}
  - {kind: other, url: "https://www.puzzlescript.net/editor.html?hack=0e8d097c183abae53c788320f198941a", note: "Scalesoban — вихідний код"}
  - {kind: official, url: "https://www.increpare.com/", note: "каталог increpare games: Scalesoban 2019/07/11, Explodoban 2021/07/13"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=increpare+puzzlescript+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 80
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, all-on-targets, explode-area, blast-wave, sequential-levels, save-progress, undo-unlimited, restart-level, level-from-txt, sound-effects, +counter-move-all, +push-only-by-blast, +rule-minimal-variant]
proposes: ["+card:counter-move-all", "+card:push-only-by-blast"]
author: opus
date: 2026-11-09
---

# increpare: Scalesoban і Explodoban — Sokoban, де ящик рухає не дотик, а «відгук» поля

## Суть
Дві мініатюри Stephen Lavelle (increpare) на PuzzleScript: класичний Sokoban (гравець, стіни, ящики, цілі; перемога — на кожній цілі ящик), де переписано правило поштовху. *Scalesoban* (2019) — штовхаєш один ящик, а **всі інші ящики одночасно зсуваються на 1 назустріч**, як шальки терезів. *Explodoban* (2021) — гравець ящиків не штовхає взагалі: ящики для нього стіни, а клавіша дії — **вибух**, що відкидає всі сусідні ящики на 1 від гравця. Продовження `increpare-micro-puzzles.md`: та сама ідея «один рядок правил — нова гра».

## Поле і час
- Квадратна сітка, текстова мапа PuzzleScript (`#` стіна, `P` гравець, `*` ящик, `O` ціль, `@` ящик на цілі). Рівні малі: 6×7…9×8.
- Шари колізії: фон → ціль → {гравець, стіна, ящик} → (Explodoban) спрайт вибуху.
- Покроково; хід = одне натискання. Explodoban: після вибуху ще один авто-тік (`again`), щоб прибрати спалах.
- Scalesoban: рівні — 3 розкладки з Microban (David W. Skinner). Explodoban: 7 власних рівнів (стара версія на 10 рівнях Microban лишилась у коді закоментованою).

## Сутності
**Scalesoban** (2019-07-11, 3 рівні)
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок на 1 у 4 напрямки; штовхає ящик |
| Ящик | object | — | поштовхнутий — на 1 від гравця; решта ящиків у той самий хід — на 1 у протилежний бік, якщо вільно |
| Стіна | static | — | непрохідна |
| Ціль | static | — | має бути під ящиком |

**Explodoban** (2021-07-13, 7 рівнів)
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок на 1; у ящик не йде і не штовхає його; X — вибух навколо себе |
| Ящик | object | — | рухається лише від вибуху: на 1 від гравця, якщо за ним вільно |
| Вибух | projectile | 4 сусідні клітини | спалах у кожній сусідній не-стіні; живе один тік |
| Стіна | static | — | непрохідна, вибух її не чіпає |
| Ціль | static | — | має бути під ящиком |
| Мертва зона | zone | — | ящик на ній скасовує хід (лише в закоментованих рівнях) |

## Правила (КОЛИ → ЯКЩО → ТО)
Спільне:
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`; у стіну — `block`.
- КОЛИ `all_on(crate, target)` → ТО `win`, `message(«level N of M»)`, `next_level`.
- Поразки нема (глухий кут → undo/restart). Рахунку нема.

Scalesoban (`[ > player | > crate ] [ stationary crate ] -> [ > player | > crate ] [ < crate ]`):
- КОЛИ `contact(player, crate)` → ЯКЩО `free(cell_behind)` → ТО `push(crate)`.
- КОЛИ `contact(player, crate)` → ЯКЩО `occupied(cell_behind, wall|crate)` → ТО `block` — увесь хід скасовано, гравець теж стоїть.
- КОЛИ `after(push)` → ЯКЩО `state(crate, stationary)` і `free(cell_opposite)` → ТО `move(crate, opposite_dir)` — кожен інший ящик на 1 назустріч; заблокований просто стоїть (хід не скасовано).
- КОЛИ `after(push)` → ЯКЩО `custom: «зустрічний ящик через одну клітину від штовхнутого»` → ТО `block` для зустрічного (щоб обидва не влізли в одну клітину).
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)` і більше нічого: «терези» гойдаються лише від поштовху.

Explodoban (`[ action Player | Crate ] -> [ action Player | > Crate ]`):
- КОЛИ `contact(player, crate)` → ТО `block` (ящик для кроку — стіна).
- КОЛИ `input(action)` → ТО `explode(cross, 1)` — спалах у 4 сусідніх клітинах, що не стіни, `sound(blast)`.
- КОЛИ `after(explode)` → ЯКЩО `adjacent(player, crate)` і `free(cell_behind_crate)` → ТО `move(crate, away_from_player)`; ланцюга нема — ящик у ящик стоїть.
- КОЛИ `after(explode)` → ТО `custom: «спалах зникає наступного авто-тіку»`.
- КОЛИ `enter(crate, deadzone)` → ТО `custom: «хід скасовано (cancel)»` — лише в чернетках.

## Керування і ввід
- Стрілки / WASD — крок; Explodoban: X (або пробіл) — вибух; Z — undo без ліміту; R — рестарт; Esc — меню (стандарт PuzzleScript).

## Вікна, меню, HUD
- `main-menu` (титул PuzzleScript): назва, автор, start / continue.
- `game-screen`: лише поле, без HUD; звуки на рух ящика, вибух, крок, кінець рівня.
- `custom-window` повідомлення: «level N of 3» / «Level N of 7» (перше в Explodoban — «[you can press x to explode]»), фінал «congratulations!».
- Переходи: main-menu → game-screen → повідомлення → наступний рівень.

## Фічі поза полем
- `levels-sequential`, `continue` (прогрес у браузері).
- `undo` ∞, `restart-level`.
- Вихідний код відкритий (`editor.html?hack=…`); у коді Explodoban лишились коментарі автора з оцінкою рівнів («kinda cute», «middle-hard!») і блок генератора TRANSFORMATION (випадкові ящики й цілі, `choose N`), у Scalesoban — закоментований «impossibly hard» рівень.

## Варіації й родичі
- Батько — `games/push-slide/sokoban.md`; брати — `games/thinky/increpare-micro-puzzles.md` (усі ящики їдуть від кроку, штовхання/тягнення за віссю, ряд ≥2).
- Рух на відстані: `games/thinky/yoohoo.md` (порив-снаряд штовхає ящики), Bomberman (`games/maze-arcade/`) — вибух хрестом, але руйнує, а не штовхає.
- Tetromino Slide того ж автора (2019) — не Sokoban, а Tetris з нахилом поля: `games/falling-match/tetromino-slide.md`.
- **Осі варіацій:** що рухає ящик — дотик / вибух навколо / «відгук» усіх ящиків; хто ще рухається — ніхто / усі ящики назустріч / усі в тому ж напрямку; чи блокує невдалий зсув увесь хід — так (поштовхнутий) / ні (решта).

## Цікавинки для курсу
- Scalesoban: «дія тут — протидія скрізь» (усі стаціонарні ящики назустріч) з розвʼязанням конфлікту зустрічних — 📎.
- Explodoban: вибух-хрест, що відкидає сусідів на 1, без ланцюга — 🌱; з ланцюгом і радіусом — 📎.
- Обидві ігри + Sokoban на одному рушії «правило → заміна» — студент перемикає варіант прапорцем — 🥉.
- Розвʼязувач BFS для Scalesoban: хід змінює весь стан, deadlock-евристики Sokoban уже не працюють — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls`; `push-object` ↔ Scalesoban; `impassable-cells`; `all-on-targets`; `explode-area` + `blast-wave` ↔ вибух хрестом (тут штовхає, не руйнує); `sequential-levels`, `save-progress`, `undo-unlimited`, `restart-level`, `level-from-txt`, `sound-effects`.
- **Нема** → пропозиції карток:
  - `+counter-move-all` «Поштовх зсуває всі інші обʼєкти назустріч» · entities/move · 📎.
  - `+push-only-by-blast` «Обʼєкт рухається лише від вибуху поруч» · entities/legality · 🌱 · слот {radius: 1, chain: false}.
  - `+rule-minimal-variant` «Варіант гри заміною одного правила» · game-logic/constraints · 🥉 (уже запропоновано в `increpare-micro-puzzles.md`).

## Пропозиції до словників
- `+card:counter-move-all`, `+card:push-only-by-blast` — механік нема в каталозі.

## Джерела
- ⭐ [Explodoban — грати](https://www.puzzlescript.net/play.html?p=08e343d25a15ad264003fdcb16f05763) · [код](https://www.puzzlescript.net/editor.html?hack=08e343d25a15ad264003fdcb16f05763) — правило `[ action Player | Crate ] -> [ action Player | > Crate ]`, 7 рівнів, `deadzone`, TRANSFORMATION.
- [Scalesoban — грати](https://www.puzzlescript.net/play.html?p=0e8d097c183abae53c788320f198941a) · [код](https://www.puzzlescript.net/editor.html?hack=0e8d097c183abae53c788320f198941a) — `[ stationary crate ] -> [ < crate ]`, 3 рівні за Microban.
- [increpare.com](https://www.increpare.com/) — дати й лінки play/source.
- Код прочитано через GitHub gist API (GET `api.github.com/gists/<hash>`).

## Непевне
- (?) Черга давала роки 2017–2020: за каталогом increpare — Scalesoban 2019-07-11, Explodoban 2021-07-13, Tetromino Slide 2019-08-30.
- (?) Порядок зсуву зустрічних ящиків у Scalesoban, коли кілька ящиків в одному ряду, — у PuzzleScript ящик за ящиком назустріч зрушить лише перший вільний; грою не перевірено.
- (?) Esc-меню і пробіл як дія — стандарт рушія з памʼяті.
