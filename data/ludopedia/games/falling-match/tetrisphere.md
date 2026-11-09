---
title: Tetrisphere
slug: tetrisphere
aka: []
family: falling-match
also: []
klass: cursor
axes:
  field: layers
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: state
year: 1997
platforms: [Nintendo 64]
links:
  - {kind: fandom, url: "https://tetris.wiki/Tetrisphere", best: true, note: "TetrisWiki: сітка 32×32 з обгортанням, 6 типів фігур і правила дотику, кристали, power pieces, іскри, gravity/fuse combo, магія, усі режими"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tetrisphere", note: "drop, комбо з 3 однакових, ковзання за тінню, множник 1×–20×, магія за 20+ фігур, таймери й 3 життя, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tetrisphere+n64+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [gravity-fall, multi-cell-size, wrap-edges, chain-reaction, combo-multiplier, explode-area, destructible-blocks, next-queue, player-death, time-out, level-select, character-select, mode-select, tutorial-window, simultaneous-versus, garbage-attack, background-music, +layered-sphere-field, +drop-from-above-cursor, +shape-touch-match, +slide-by-shadow, +power-pieces, +magic-weapons, +dig-to-core]
proposes: ["+trigger:meter_full", "+cond:shape_match", "+cond:aligned_layers", "+effect:drop_into", "+effect:slide_layer", "+effect:power_up", "+effect:spark", "+effect:camera_approach", "+role:core", "+ui:shadow-cursor", "+ui:x-count", "+ui:speed-meter", "+ui:magic-slot", "+feature:character-stats", "+feature:mode-hide-and-seek"]
author: opus
date: 2026-11-09
---

# Tetrisphere — скидай фігури на шарувату «сферу», щоб однакові дотики вибухали й прокопували шари до ядра

## Суть
Від [Tetris](tetris.md) тут лишились тетроміно-подібні цеглини, але гра інша: поле — **кулясте**, зроблене з кількох **шарів** цеглин довкола ядра, а гравець — це курсор-тінь над поверхнею. Ти **скидаєш** фігуру вглиб (drop) так, щоб вона стала поруч з **такою самою формою** — три й більше однакових, що торкаються, вибухають ланцюгом. Мета рівня — прокопати шари й відкрити ядро (у Rescue — звільнити робота). Кожен drop без реакції коштує життя; таймер тисне камерою, що наближається до сфери.

## Поле і час
- «Сфера» насправді — квадратна сітка 32×32 з обгортанням схід/захід і північ/південь (тор, намальований кулею); фігури зберігають орієнтацію, коли курсор обходить сферу.
- Глибина: ядро + 2–5 шарів цеглин (Practice); фігура падає з поверхні до найближчої опори (`gravity: toward-center`).
- Real-time: таймер (синій → жовтий → червоний) тече, коли нічого не зчищається; на жовтому камера повільно наближається до сфери.
- Шари: ядро (секції, які треба відкрити) + шари цеглин + кристали в пустотах + курсор-тінь з активною фігурою над поверхнею.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор-тінь з фігурою | player | форма поточної фігури, 3 у черзі | рухається поверхнею; A — скинути фігуру вглиб під тінню; B — захопити й ковзати цеглину |
| Синя O (2×2) | tile | — | зчищається лише з повним боковим контактом з такою ж формою |
| Зелена I · жовта горизонтальна I (3×1) | tile | орієнтація | як O — потрібен повний дотик стороною (лежать під 90°) |
| Червона T · блакитна Z · рожева мала L | tile | — | зчищаються, якщо торкаються будь-яким ребром |
| Кристал 1×1 | object | — | заповнює пустоти; ламається, коли в нього ковзнули фігуру або поруч зчистились фігури |
| Wild card | pickup | — | скидається як будь-який тип, може ковзати будь-яку фігуру |
| Power Piece | object | світиться | зʼявляється після очистки; може ковзати на шар вгору; зчищення сильно поповнює таймер; детонує довше |
| Іскра | projectile | — | падає після очистки ≤19 фігур (стільки ж, скільки зчищено); перетворює звичайну фігуру, якої торкнулась (?) |
| Магічний кристал 1×1 | pickup | — | рідко; розбитий — дає/підвищує магію |
| Темна фігура (Vs) | hazard | — | приходить від суперника; зчищається лише сусідньою очисткою |
| Ядро | static | секції | мета: відкрити потрібну кількість секцій; у Rescue всередині — робот |
| Персонаж | — (налаштування) | Speed, Power | швидкість курсора звичайна / під час ковзання (автоповтор) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place)` → ЯКЩО `free(column_under_shadow)` → ТО `custom: «drop_into — фігура падає вглиб до опори»`.
- КОЛИ `custom: «фігура лягла»` → ЯКЩО `count(same_shape_touching, ≥, 3)` і `custom: «shape_match — O/I: повний боковий дотик; T/Z/L: будь-яке ребро; на сусідніх шарах — точно одна над одною»` → ТО `custom: «група світиться й імплодує»`, `clear(group)`, ланцюг на однакові сусідні.
- КОЛИ `custom: «фігура лягла»` → ЯКЩО `not custom: «почалась реакція»` → ТО `lives(-1)`, `reset_combo`, `timer(reset)`.
- КОЛИ `input(place)` → ЯКЩО `custom: «шар під тінню блимає червоним (надто високо)»` → ТО `lives(-1)` навіть з реакцією.
- КОЛИ `input(hold_b + dir)` → ЯКЩО `same(shadow_shape, piece_below, shape)` → ТО `slide(piece, dir)`; інакше `block`. Ковзна фігура проходить крізь кристали й знищує їх, але не інші фігури.
- КОЛИ `destroyed(support)` → ТО `fall(piece)` вглиб — **gravity combo**: КОЛИ `after(fall)` → ЯКЩО `pattern(group(3))` → ТО `combo(+1)` (X count).
- КОЛИ `after(clear)` → ТО `custom: «power_up — випадкові фігури починають світитися (кількість залежить від розміру комбо)»`.
- Fuse combo: КОЛИ `input(hold_b)` → ЯКЩО `state(fuse, flashing)` до детонації → ТО `slide(fuse, to_another_group)`, `combo(+1)`.
- Множник X count: 1× … 20×; gravity combo додає до ×10, fuse combo — до ×11; `score(points × X)`.
- КОЛИ `after(clear)` → ЯКЩО `count(cleared, ≤, 19)` → ТО `custom: «spark — падає стільки ж іскор, що перетворюють звичайні фігури»`.
- КОЛИ `input(b_over_crystals)` → ЯКЩО `custom: «кристали складають форму, як поточна фігура»` → ТО `transform(crystals → power_piece)`.
- КОЛИ `after(clear)` → ЯКЩО `count(cleared, ≥, 20)` → ТО `give(player, magic)` замість power pieces; повторно — `custom: «апгрейд магії»`; також за наповнену шкалу під комбо або розбитий магічний кристал.
- КОЛИ `input(use_magic)` → ТО `explode(area by level)`: Rocket/Firecracker (мала площа верхнього шару) < Dynamite (5 частин) < Magnet (зап по цілі) < Molecule/Atom (весь верхній шар) < Atom Bomb/Bomb (крізь кілька шарів) < Laser/Raygun.
- КОЛИ `custom: «втрачено життя»` → ЯКЩО `has(player, magic)` → ТО `take(player, magic)` — невикористана магія згорає.
- КОЛИ `timer(blue, ==, 0)` → ТО `custom: «жовтий таймер, camera_approach — камера наближається»`; КОЛИ `reach(camera, field)` → ТО `custom: «автоскидання фігури»` / `lives(-1)`; зчищення частково поповнює таймер.
- КОЛИ `counter(lives, ==, 0)` → ТО `lose` (3 життя на рівень).
- КОЛИ `counter(core_sections_open, ≥, goal)` → ТО `win`, `next_level` (Rescue — робот звільнений).
- Vs: КОЛИ `after(clear)` → ЯКЩО `counter(cleared, ≥, n)` → ТО `send_garbage(dark_pieces)`, більший X count — більше; раунд виграє той, хто відкрив досить ядра, або суперник втратив 3 життя.

## Керування і ввід
- D-pad — курсор-тінь по поверхні сфери; A — скинути фігуру; утримання B над рухомою фігурою + D-pad — ковзання.
- Повороту, hard drop і hold нема; черга показує поточну + 2 наступні.
- Курсор яскравішає, якщо скидання почне реакцію (підказка легальності).
- Puzzle: L/R — зум камери, C-вгору — рестарт; кнопка магії — окремо (?).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Rescue · Hide and Seek · Puzzle · Time Trial · Vs. CPU · Vs. Player · Practice · Training (`tutorial-window`); прихований Lines.
- `character-select` — персонаж-робот зі Speed/Power; `custom: «вибір музичного треку»`.
- `settings-window` Practice: ≥2 з 6 типів фігур, 2–5 шарів, 1–99 секцій ядра.
- `game-screen`: сфера на весь екран з курсором-тінню; `next-piece-preview` (3); `custom: «X count»`; `custom: «шкала магії під комбо + слот магії»`; `lives` (серця); `custom: «таймер-шкала синя/жовта/червона»`; `score`, `level-number`; підсвітка курсора (`legal-move-highlight`).
- Vs: розділений екран (`opponent-boards`), лічильник відкритого ядра.
- `pause-menu`, `end-screen`, `leaderboard` (Time Trial), `level-select`/`puzzle-select` для Puzzle (?).

## Фічі поза полем
- Режими: `custom: «Rescue»` (кампанія рівнів), `custom: «Hide and Seek»` (особливі цілі: відкрити картинку на ядрі, оголити вежу…), `mode-puzzle` (фіксована розстановка, ліміт ковзань і скидань, усі фігури — wild card, без таймера), `mode-time-attack`, `mode-versus` (CPU/людина), `mode-practice`, прихований `custom: «Lines»` (без скидань, вибух трьох в ряд).
- `tutorial` — Training; `custom-difficulty` — Practice-параметри.
- `custom: «character-stats»` — персонаж змінює швидкість курсора.
- `music-toggle`/вибір треку (саундтрек Ніла Восса).
- `save-slots`/рекорди на картці памʼяті N64 (?).

## Варіації й родичі
- [tetris.md](tetris.md) — лише форми фігур; ядро — [samegame-flood.md](samegame-flood.md)/[puyo-puyo.md](puyo-puyo.md) (група однакових зникає, каскад), але зі скиданням згори в шари.
- [meteos.md](meteos.md) — інша «планетарна» falling-match; [puzzle-quest.md](puzzle-quest.md) — магія як нагорода за великі комбо.
- [blockout.md](blockout.md) — інший спосіб перенести тетріс у 3D.
- **Осі варіацій**: правило дотику (за кольором / за формою; O/I — повний бік, T/Z/L — будь-яке ребро) · гравітація (униз / до центру) · поле (стакан / тор-сфера з шарами) · штраф (висота стеку / життя за drop без реакції) · подовження ланцюга (gravity / fuse ковзанням).

## Цікавинки для курсу
- Тор 32×32 з обгортанням як «сфера» + шари в глибину (`grid[layer][y][x]`) — 📎.
- Правило збігу за формою з двома режимами дотику (повний бік vs будь-яке ребро) — 🥉 (компоненти звʼязності з умовою на ребра).
- Скидання вглиб з «гравітацією до центру» й gravity combo після вибуху — 🥉.
- Ковзання лише коли тінь збігається з формою під нею — 📎.
- Power pieces, іскри, fuse combo (перехопити детонацію) — 🥈 (таймери детонації на кожну групу).
- Магія з рівнями, що апгрейдується повторним отриманням і зникає зі смертю — 📎.
- Puzzle-режим: фіксована розстановка + ліміт ходів (банк задач) — 🥉, розвʼязувач — 🥇.

## Мапа на каталог
- Є: `gravity-fall` (падіння вглиб), `multi-cell-size`, `wrap-edges` (тор), `chain-reaction` (gravity/fuse combo), `combo-multiplier` (X count), `explode-area` (магія), `destructible-blocks` (кристали), `next-queue`, `player-death` (3 життя), `time-out` (таймер, Time Trial), `level-select`, `character-select`, `mode-select`, `tutorial-window`, `simultaneous-versus` + `garbage-attack` (темні фігури), `background-music`.
- **Нема** → пропозиції карток:
  - `+layered-sphere-field` «Поле-сфера з шарів довкола ядра» · entities/move · 🥉 · слоти {size: 32, layers: 2–5}.
  - `+drop-from-above-cursor` «Курсор-тінь скидає фігуру вглиб» · interface/input · 📎.
  - `+shape-touch-match` «Збіг за формою з правилом дотику» · entities/interact · 🥉 · слот {touch: full_side|any_edge}.
  - `+slide-by-shadow` «Ковзання фігури, якщо тінь збігається» · entities/move · 📎.
  - `+power-pieces` «Фігури-підсилювачі після очистки» · entities/state · 🥈.
  - `+magic-weapons` «Зброя-нагорода за велике комбо з рівнями» · entities/combat · 📎.
  - `+dig-to-core` «Мета — прокопати шари до ядра» · game-logic/win · 📎.

## Пропозиції до словників
- `+trigger:meter_full` — шкала заряду наповнилась (магія; також Tetris Effect Zone).
- `+cond:shape_match` — дві фігури однієї форми торкаються за правилом (повний бік / ребро); `+cond:aligned_layers` — фігури сусідніх шарів точно одна над одною.
- `+effect:drop_into` — скинути фігуру з курсора вглиб до опори; `+effect:slide_layer` — ковзати фігуру шаром, лише якщо тінь збігається.
- `+effect:power_up` — позначити випадкові фігури як підсилені; `+effect:spark` — снаряд, що перетворює фігуру, якої торкнувся.
- `+effect:camera_approach` — камера наближається як візуальний таймер небезпеки.
- `+role:core` — ціль у центрі поля, яку треба відкрити.
- `+ui:shadow-cursor` — тінь фігури на поверхні, що яскравішає перед реакцією; `+ui:x-count` — множник комбо; `+ui:speed-meter` — кольоровий таймер-шкала; `+ui:magic-slot` — поточна магія.
- `+feature:character-stats` — персонаж міняє швидкість вводу; `+feature:mode-hide-and-seek` — кампанія з особливими цілями рівнів.

## Джерела
- ⭐ [TetrisWiki: Tetrisphere](https://tetris.wiki/Tetrisphere) — сітка 32×32 з обгортанням, 2–5 шарів, 6 типів і правила дотику, кристали, wild card, курсор і B-ковзання, 3 next, 3 життя, червоний шар, таймер із камерою, персонажі Speed/Power, power pieces, іскри (≤19), gravity/fuse combo, магія (20+, шкала, кристал) і 6 видів, усі режими, Vs з темними фігурами.
- [Wikipedia: Tetrisphere](https://en.wikipedia.org/wiki/Tetrisphere) — drop, «3 однакових торкаються», ковзання за тінню, множник 1×–20×, gravity до ×10 і fuse до ×11, магія (Firecracker…Raygun), таймери і 3 серця, режими, H2O, 1997.

## Непевне
- (?) Назви магії розходяться: TetrisWiki — Rocket/Dynamite/Magnet/Molecule/Atom Bomb/Laser; Wikipedia — Firecracker/Dynamite/Magnet/Atom/Bomb/Raygun (регіональні версії?).
- (?) На що саме іскра перетворює фігуру (на power piece?) — сторінка каже лише «converts».
- (?) Кількість зчищених фігур для відправки темних фігур у Vs і для поповнення таймера — без чисел.
- (?) Кнопка застосування магії, вибір рівнів Puzzle і збереження на картці памʼяті — з памʼяті.
- (?) Значення очок за фігуру — джерела не дають.
- (?) Робоча назва «Phear» (до ліцензії Tetris) — з памʼяті.
