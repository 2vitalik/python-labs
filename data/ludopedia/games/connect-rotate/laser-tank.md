---
title: LaserTank
slug: laser-tank
family: connect-rotate
also: [push-slide, thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 1995
platforms: [Windows, iOS (2015), web, macOS, Linux]
links:
  - {kind: official, url: "https://laser-tank.com/instructions.html", best: true, note: "офіційний список усіх обʼєктів і їхньої поведінки + редактор"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/LaserTank", note: "історія, 16×16, NP-повнота, колекції рівнів"}
  - {kind: play, url: "https://antaciid.itch.io/lasertank", note: "LaserTank-RE: браузер/десктоп, ~15k рівнів, undo, редактор"}
  - {kind: official, url: "https://laser-tank.com/welcome.html", note: "фічі 4.1: undo ∞, replay, 2030 рівнів, рекорди з доказом"}
  - {kind: official, url: "https://laser-tank.com/help.html", note: "навчальні рівні tutor.lvl з записами проходжень"}
  - {kind: official, url: "https://forum.laser-tank.com/", note: "форум спільноти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=LaserTank+puzzle+gameplay", note: "пошук; геймплей"}
stage: v2
coverage: 75
mechanics: [move-4dir, push-object, floor-types, inertia-slide, cell-transform, teleport-pair, reach-exit, environment-death, projectile-shot, row-conveyor, in-game-editor, level-exchange, level-bank, replay, score-records, +beam-tracing, +mirror-reflect, +shot-push, +shot-rotate, +destructible-block, +see-through-block, +line-of-fire-enemy, +facing-turn, +undo-redo, +solution-proof]
proposes: ["+trigger:beam_hit", "+cond:hit_side", "+ui:shot-counter", "+feature:solution-proof", "+card:shot-push", "+card:line-of-fire-enemy", "+card:facing-turn"]
author: opus
date: 2026-11-02
---

# LaserTank — доведи танк до прапора, стріляючи лазером, що штовхає, руйнує й відбивається

## Суть
Покроковий пазл на полі 16×16: танк ходить у 4 боки й стріляє лазером уперед. Лазер — це «довга рука»: штовхає блоки й дзеркала на відстані, ламає цеглу, повертає обертові дзеркала, відбивається від дзеркальних граней і вбиває протитанкові гармати, якщо влучити їм у дуло. Протитанкові гармати стріляють самі, щойно танк опиниться перед дулом. Лід, тонкий лід, вода й тунелі роблять із цього Sokoban з дистанційним штовханням; гра формально NP-повна.

## Поле і час
- Поле 16×16 клітин, один екран, без камери. Шар підлоги (земля, вода, лід, тонкий лід, конвеєр, тунель) + шар обʼєктів (блоки, дзеркала, гармати, танк, прапор).
- Покроково: хід = рух, поворот або постріл; між ходами система ходить сама (промінь летить, ковзання по льоду, конвеєр, відповідь гармат) до стабільного стану.
- Лазер пролітає над землею й водою; рахунок рівня — кількість ходів і пострілів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Танк | player | напрям | рух 4 боки; натиснув інший напрям — поворот на місці; стріляє вперед |
| Лазер | projectile | напрям | летить прямо до першого непрозорого обʼєкта; ефект залежить від обʼєкта й грані |
| Прапор | static | — | танк на ньому → перемога |
| Земля (dirt) | terrain | — | ходити й стріляти можна |
| Вода | terrain | — | танк/обʼєкт тоне; рухомий блок → міст |
| Міст | terrain | — | рухомий блок у воді: тепер звичайна земля |
| Твердий блок | static | — | не руйнується, не рухається, лазер зупиняє |
| Рухомий блок | object | — | лазер штовхає на 1 у напрямку пострілу; єдиний, хто «плаває» → міст |
| Цегла | object | — | постріл руйнує |
| Кришталевий блок | static | — | нерухомий; лазер проходить, але гармата крізь нього танк не бачить |
| Дзеркало | conduit (custom) | 4 орієнтації (діагональна грань) | лазер у дзеркальну грань → відбиття на 90°; у основу → дзеркало зсувається на 1 |
| Обертове дзеркало | conduit (custom) | 4 орієнтації | дзеркальна грань відбиває; постріл в основу → поворот на 90° за годинниковою |
| Протитанкова гармата | enemy | напрям дула | стріляє, коли танк перед дулом; постріл у бік → зсув (і у воду); у дуло непомітно → знищена |
| Конвеєр (tank mover) | terrain | напрям | везе лише танк до кінця; у дорозі не можна ні рухатись, ні стріляти; блок на конвеєрі = зупинка |
| Тунель ×8 кольорів | terrain | колір | танк або рухомий обʼєкт заходить → виходить з тунелю того ж кольору |
| Тунель без пари | hazard | — | «чорна діра»: зайшов — зник |
| Лід | terrain | — | усе рухоме (і танк) ковзає до упору |
| Тонкий лід | terrain | — | як лід, але після проходу стає водою; зупинитись на ньому = впасти у воду |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `not facing(tank, dir)` → ТО `face(tank, dir)` (хід зараховано).
- КОЛИ `input(dir)` → ЯКЩО `facing(tank, dir) and free(cell_ahead)` → ТО `move(tank, dir)`; інакше `block`.
- КОЛИ `input(fire)` → ТО `spawn(laser)` у напрямку танка, `counter(shots, +1)`; промінь летить, доки не влучить у непрозоре.
- КОЛИ `contact(laser, brick)` → ТО `disappear_b`.
- КОЛИ `contact(laser, movable_block)` → ЯКЩО `free(cell_behind)` → ТО `push`; інакше нічого.
- КОЛИ `contact(laser, solid_block)` → ТО `custom: «промінь зупинено»`.
- КОЛИ `contact(laser, crystal)` → ТО `custom: «промінь проходить»`.
- КОЛИ `contact(laser, mirror)` → ЯКЩО `custom: «hit_side(mirror, face)»` → ТО `bounce(laser)` (90°); інакше `push(mirror)`.
- КОЛИ `contact(laser, rotary_mirror)` → ЯКЩО `custom: «hit_side(face)»` → ТО `bounce(laser)` (90°); інакше `rotate(rotary_mirror, 90)`.
- КОЛИ `contact(laser, antitank)` → ЯКЩО `custom: «hit_side(barrel)»` і не `line_of_sight(antitank, tank)` → ТО `disappear_b`; ЯКЩО `custom: «hit_side(side)»` → ТО `push(antitank)` (і у воду).
- КОЛИ `line_of_sight(antitank, tank)` (танк перед дулом, без кришталю між) → ТО `spawn(laser)` від гармати → `lose`.
- КОЛИ `contact(laser, tank)` (власний промінь через дзеркала) → ТО `lose` (?).
- КОЛИ `enter(tank, water)` → ТО `lose`; КОЛИ `enter(object, water)` → ЯКЩО `object = movable_block` → ТО `set_cell(bridge)`, `disappear_a`; інакше `disappear_a` (тоне).
- КОЛИ `enter(a, ice)` → ТО `slide(a, dir)` до упору.
- КОЛИ `leave(a, thin_ice)` → ТО `set_cell(water)`; КОЛИ `custom: «танк зупинився на тонкому льоду»` → ТО `set_cell(water)`, `lose`.
- КОЛИ `enter(tank, conveyor)` → ТО `move(tank, conveyor_dir)` щотік до кінця; `input` ігнорується.
- КОЛИ `enter(a, tunnel[c])` → ЯКЩО `count(tunnel[c], ==, 2)` → ТО `teleport(a, pair)`; ЯКЩО пари нема → ТО `disappear_a` (чорна діра); більше двох однакових — «складна» поведінка (?).
- КОЛИ `contact(tank, flag)` → ТО `win`, `custom: «записати ходи й постріли як рекорд рівня»`.
- Перемога: танк на прапорі. Поразка: постріл гармати, вода, чорна діра, тонкий лід — рівень з початку або undo. Рахунок: менше ходів + пострілів = краще; локальний і глобальний рекорд.

## Керування і ввід
- Стрілки / WASD — поворот або крок; Space / F — постріл; Backspace (оригінал (?)) / U / Q (RE) — undo; R — рестарт.
- Миша (з 4.1; у RE: ЛКМ — рух, ПКМ — постріл).
- Запис ходів (Game Record) і програвання `.lpb`.

## Вікна, меню, HUD
- `game-screen`: поле 16×16 + панель: назва рівня, автор, номер, складність, `move-counter`, `shot-counter`, кнопки Undo/Restart/Hint (?).
- Меню (Windows): Game (New, Open data file — інший файл рівнів, Restart, Undo, Record/Playback, Skip completed levels) · Level (Previous/Next, Goto, Editor) · Options (графіка LTG / Ctrl+G, звук, мова) · Help (`help-window`, `about-window`).
- `level-select` / `puzzle-select`: список рівнів файла з позначками пройдених і фільтром за складністю (5 рівнів у RE).
- `hints-window`: текстова підказка автора рівня (поле Hint у редакторі).
- `editor-window`: палітра обʼєктів праворуч унизу, ЛКМ/ПКМ — два обраних обʼєкти, поля Title/Author/Hint/Difficulty, Save у номер рівня (найбільший номер — новий рівень, інший — заміна), Close Editor = грати.
- `leaderboard`: локальні рекорди (ходи/постріли) і порівняння з Global High Score.
- `replay-window`: програвання запису проходження.
- `end-screen`: рівень пройдено → рахунок → наступний; загибель → повідомлення → undo/restart.

## Фічі поза полем
- `undo` ∞ (з 4.1), `restart-level`, `replay` / `export-import` записів `.lpb`.
- `level-editor` + `level-sharing`: рівні надсилаються лише з розвʼязком (`.lpb`) — автор гарантує розвʼязність; щомісячні нові рівні.
- `puzzle-bank` тисяч рівнів у файлах `.lvl` (+ `.ghs` глобальні й `.hs` локальні рекорди) (4.1 — 2030, у порядку надходження, не за складністю; RE — ~15k у 21 паку); навчальні Tutor.lvl (92), Game-Objects-in-LT (16), Tutor-with-Playbacks (112); колекції Beginner, Challenge, Sokoban-подібна, Special (?).
- `leaderboard-online` (глобальний файл рекордів; побив — надішли `.hs` + запис як доказ); `level-rating` (Level's Evaluator).
- `theme-select` (LTG-графіка), `localization`, `mouse-and-keyboard`; RE — `snapshots` (Save/Restore position), `difficulty-presets` (5: Kids, Easy, Medium, Hard, Deadly).

## Варіації й родичі
- Версія 4.1 додала тунелі, лід і тонкий лід, undo ∞, Replay, мишу. LaserTank-RE (HTML5 + Windows/macOS/Linux), iOS-порт Jack Powell (01.02.2015, з магазину знятий); Deflektor (дзеркала, але курсором і real-time), Khet (дзеркала-фігури, суперник), Sokoban (штовхання), Chip's Challenge (лід, вода, блок-міст, тунелі-телепорти), Adventures of Lolo (вороги з лінією вогню).
- Осі варіацій: **штовхання: тілом / пострілом здалеку** · **дзеркало: нерухоме / зсувне / обертове** · **ворог-гармата: стріляє по лінії / по наміру** · **лід: товстий / тонкий (руйнується)** · **рахунок: лише ходи / ходи + постріли**.

## Цікавинки для курсу
- Постріл як дистанційна дія: таблиця «обʼєкт × грань влучання → ефект» (зруйнувати / штовхнути / відбити / повернути / пройти / зупинити) — 🥈 (картка `interaction-table` у чистому вигляді).
- Промінь з відбиттями від дзеркал + ворог, що бачить уздовж лінії (кришталь прозорий для пострілу, але не для погляду) — 🥉.
- Поворот на місці як окремий хід (`facing` — частина стану) — 🌱.
- Ланцюг наслідків одного ходу: постріл → блок ковзає по льоду → падає в тунель → виходить з пари → тоне/стає мостом — 🥈 (черга подій до стабільного стану).
- Тонкий лід (клітина міняє тип після проходу) і чорна діра (тунель без пари) — 📎.
- Undo ∞ + запис/програвання ходів як доказ рекорду — 🥉.
- Розвʼязувач (BFS по станам) і NP-повнота як тема доповіді — 👑.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `push-object` (лазером, не тілом) · `floor-types` (вода, лід, тонкий лід) · `inertia-slide` · `cell-transform` (блок у воді → міст, тонкий лід → вода) · `teleport-pair` (тунелі) · `row-conveyor` (найближче до tank mover) · `reach-exit` (прапор) · `environment-death` · `touch-death` (постріл гармати) · `projectile-shot` · `level-from-txt` (формат `.lvl` — бінарний (?)) · `in-game-editor` + `editor-palette` + `editor-playtest` · `level-exchange` · `level-metadata` (Title/Author/Hint/Difficulty) · `level-select` · `level-bank` · `level-rating` · `replay` · `score-records` · `leaderboard` · `theme-select` · `keyboard-controls` · `cell-click`.
- **Нема** → пропозиції карток:
  - `+beam-tracing` «Трасування променя» · entities/combat · 🥉.
  - `+mirror-reflect` «Дзеркало з кутом» · entities/interact · 📎.
  - `+shot-push` «Постріл штовхає обʼєкт» · entities/combat · 📎.
  - `+shot-rotate` «Постріл повертає обʼєкт» · entities/combat · 🌱.
  - `+destructible-block` «Руйнівний блок» · entities/combat · 🌱.
  - `+see-through-block` «Прозорий для пострілу, непрозорий для погляду» · entities/legality · 📎.
  - `+line-of-fire-enemy` «Ворог стріляє по лінії» · entities/combat · 🥉 · слоти {range, blockers}.
  - `+facing-turn` «Поворот на місці як хід» · entities/move · 🌱.
  - `+undo-redo` «Undo ходів гравця» · game-logic · 📎.
  - `+black-hole` «Телепорт без пари знищує» · entities/interact · 🌱 (дитина `teleport`).
  - `+thin-ice` «Клітина руйнується після проходу» · entities/interact · 🌱.
  - `+par-score` «Рахунок = кількість ходів/дій, менше краще» · game-logic/score · 🌱.
  - `+solution-proof` «Рекорд/рівень приймається лише з записом розвʼязку» · levels/solvability · 📎.

## Пропозиції до словників
- Вжито наявні ролі `projectile`, `terrain`, тригер `line_of_sight`, умову `facing`, ефекти `bounce` (відбиття від дзеркала), `rotate`, `face`, `slide`, `set_cell`, вікно `editor-window`.
- `+trigger:beam_hit(a)` — промінь влучив у сутність (спільне з Deflektor); у правилах поки записано як `contact(laser, a)`.
- `+cond:hit_side(a, face|base|barrel|side)` — у яку грань влучив промінь.
- `+ui:shot-counter` — окремий лічильник пострілів поруч з ходами.
- `+feature:solution-proof` — розвʼязок як обовʼязковий додаток до рівня/рекорду.
- `+card:shot-push`, `+card:line-of-fire-enemy`, `+card:facing-turn` — див. вище.

## Джерела
- ⭐ [LaserTank: Instructions](https://laser-tank.com/instructions.html) — повний офіційний список обʼєктів (вода, блоки, кришталь, цегла, гармати, дзеркала, обертові дзеркала, конвеєри, тунелі ×8 і чорна діра, лід, тонкий лід) і редактор.
- [Wikipedia](https://en.wikipedia.org/wiki/LaserTank) — Jim Kindley, 1995, 16×16, ходи+постріли, колекції рівнів, NP-повнота, iOS-порт 2015.
- [LaserTank-RE на itch.io](https://antaciid.itch.io/lasertank) — грати в браузері, клавіші (поворот/рух, Space, U/Q undo, R), ~15k рівнів, 5 складностей, редактор.
- [Welcome / фічі 4.1](https://laser-tank.com/welcome.html) — undo ∞, Replay, 2030 рівнів, рекорд лише з `.lpb`.
- [Help](https://laser-tank.com/help.html) — навчальні рівні з записами проходжень, рахунок за ходами й пострілами.
- [Форум](https://forum.laser-tank.com/) — спільнота, нові рівні.

## Непевне
- (?) Чи вбиває танк власний промінь, повернутий дзеркалами, — з памʼяті; в інструкції не сказано.
- (?) Що лишається від знищеної гармати і чи стріляють гармати після кожного ходу чи лише в момент входу танка в лінію — порядок подій не описано.
- (?) Чи штовхає лазер гармати рухомий блок/дзеркало так само, як лазер танка.
- (?) Клавіша undo в оригіналі (Backspace), назви пунктів меню Windows-версії (крім Skip completed levels, Save/Load, Close Editor), кнопка Hint — з памʼяті.
- (?) Поведінка за >2 тунелів одного кольору — офіційно «складна», без пояснення.
- (?) Формат `.lvl` — бінарний, а не текстовий; тег `level-from-txt` — лише за ідеєю «рівні як файли».
