---
title: Hackenbush (Хакенбуш)
slug: hackenbush
aka: [Red-Blue Hackenbush, Blue-Red Hackenbush, Green Hackenbush, Blue-Red-Green Hackenbush]
family: connect-rotate
also: [chess-abstract]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: full
  random: none
  goal: survive
year: 1976
platforms: [paper, PC, Mac]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Hackenbush", best: true, note: "правила, варіанти Green / Blue-Red / Blue-Red-Green, surreal numbers, colon і fusion principle"}
  - {kind: official, url: "http://geometer.org/hackenbush/index.html", note: "Tom Davis: програма Hackenbush (Mac/Windows) — гра проти AI, редактор, збереження"}
  - {kind: other, url: "http://geometer.org/hackenbush/hackdoc.pdf", note: "посібник програми: меню, wizard mode зі значенням позиції, редактор, пошук складних розфарбувань, ліміти"}
  - {kind: other, url: "http://geometer.org/mathcircles/hackenbush.pdf", note: "Davis: теорія Blue-Red для школярів — значення, стебла, дерева, петлі"}
  - {kind: other, url: "https://combinatorialgames.wordpress.com/2012/08/19/ii-4-hackenstrings-and-0-999-vs-1/", note: "Hackenstrings (лише бачив у Wikipedia)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Hackenbush", note: "пошук; пояснення й партії"}
stage: v1
coverage: 65
mechanics: [hot-seat, turn-enforcement, ai-opponent, ai-minimax, cell-click, hover-highlight, no-moves-left, connectivity-check, rule-variants, level-solver, difficulty-rating, in-game-editor, editor-palette, editor-draw-tools, editor-erase, editor-playtest, save-game, undo-step, restart-level, tutorial-window, help-window, settings-window, game-screen, +edge-cut-cascade, +game-value-sum, +nim-reduction, +value-hint]
proposes: ["+role:node", "+role:edge", "+effect:delete_edge", "+ui:game-value", "+feature:wizard-mode", "+axis:goal=normal-play", "+card:edge-cut-cascade", "+card:game-value-sum", "+card:nim-reduction"]
author: opus
date: 2026-11-09
---

# Hackenbush — по черзі зрізаєте ребра графа, що росте з «землі»; відірване від землі падає; хто не може ходити — програв

## Суть
Малюнок з відрізків стоїть на лінії «землі»: кожен відрізок звʼязаний із землею напряму або через інші. Хід — зрізати одне ребро; усе, що після цього втратило звʼязок із землею, зникає. Хто не має чого різати, програє (normal play). Гру придумав John Conway як навчальний приклад комбінаторної теорії ігор: у Blue-Red-версії (синій ріже лише сині, червоний — червоні) кожна позиція має **значення-число**, а позиція з кількох окремих малюнків варта суми значень.

## Поле і час
- Поле `graph`: вершини (точки) і ребра (відрізки, у цифровій версії — також криві й петлі); уся земля — одна спеціальна вершина; кратні ребра між двома точками дозволені.
- Покроково, без часу; кожен хід зменшує кількість ребер, тож скінченна партія гарантовано скінчиться.
- Нескінченні дошки — лише в теорії: дають дійсні числа й ординали; у програмі Davis — до 64 ребер.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Земля | static | одна вершина-корінь | ребра, що мають шлях до неї, стоять; решта падає |
| Вершина | node (custom) | координати | точка стику будь-якої кількості ребер |
| Ребро синє | edge (custom) | колір blue | зрізати може лише Blue (Left) |
| Ребро червоне | edge (custom) | колір red | зрізати може лише Red (Right) |
| Ребро зелене | edge (custom) | колір green | зрізати може будь-хто (Green та Blue-Red-Green) |
| Стебло | zone | послідовність кольорів знизу вгору | ланцюжок без розгалужень; значення — за двійковим правилом |
| Гравець Blue / Red | player | сторона | ходять по черзі; хто без ходу — програв |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, edge)` → ЯКЩО `turn_of(side)` and `same(edge, side, color)` → ТО `disappear(edge)`, `end_turn` (Blue-Red: колір ребра = колір сторони).
- КОЛИ `input(click, edge)` → ЯКЩО `state(edge, green)` → ТО `disappear(edge)`, `end_turn` (зелене — будь-якій стороні).
- КОЛИ `input(click, edge)` → ЯКЩО `not same(edge, side, color)` and `not state(edge, green)` → ТО `block`.
- КОЛИ `after(disappear(edge))` → ЯКЩО `not path_exists(e, ground)` → ТО `disappear(e)` — для кожного ребра e, що втратило звʼязок із землею (каскад).
- КОЛИ `no_moves(side)` → ТО `lose(side)` (normal play: хто не може ходити — програв; у порожній позиції програє той, хто ходить першим).
- Цифрова версія: КОЛИ `input(click, edge)` → ТО `custom: «ребро блимає пару секунд, потім зникає разом із залежними»`; AI відповідає так само.
- Значення Blue-Red: КОЛИ `custom: «значення позиції > 0»` → ТО виграє Blue за будь-якого першого ходу; `< 0` — Red; `= 0` — програє той, хто ходить.
- Сума: КОЛИ `custom: «позиція розпалась на компоненти без спільних ребер (окрім землі)»` → ТО значення = сума значень компонент (програма аналізує частини окремо й додає).
- Стебло Blue-Red: n однакових від землі = ±n; кожне наступне ребро після першої зміни кольору додає ±1/2, ±1/4, ±1/8… (синє «+», червоне «−»): синє з червоним на ньому = 1/2.
- Green Hackenbush: стебло з n ребер = купка Nim з n (*n); дерево зводиться за **colon principle** (гілки в одній вершині → стебло довжини їхньої nim-суми), цикли — за **fusion principle** (вершини циклу зливаються в одну) → гра стає Nim.
- Blue-Red — «холодна» гра: ходити першим ніколи не вигідно.
- Тривіальна стадія: КОЛИ `custom: «жоден розріз не зносить ребер суперника»` → ЯКЩО `mode(stop_trivial)` → ТО b − r > 0 — `win(blue)`, < 0 — `win(red)`, = 0 — `lose(side_to_move)` (b, r — кількість синіх і червоних ребер).
- Wizard: КОЛИ `input(hover, edge)` → ЯКЩО `mode(wizard)` and `turn_of(player)` → ТО `message(value_after_cut)`.
- Перемога: суперник не має ходу · Поразка: нема свого ребра для зрізу · Рахунку нема (є значення позиції).

## Керування і ввід
- Папір: стерти (перекреслити) ребро й усе, що повисло в повітрі.
- Програма Davis: клік по ребру свого кольору — зріз; за замовчуванням людина — Blue і ходить першою, машина — Red.
- Редактор: режими Select (S), Add Points (P; клік по землі — точка на землі; клік по ребру — розбити його точкою), Add Edges (E; дві точки — ребро; двічі одна — петля), Set Color (C); R / B — колір вибраного ребра, D — видалити ребро чи вільну точку; криві — кубічні Безьє з двома жовтими контрольними точками.

## Вікна, меню, HUD
- `game-screen` (програма Davis): поле з землею, кнопка Play / Stop / Manual (у ручній грі напис чергує кольори — чий хід), перемикач кольору Red / Blue, вибір режиму редагування, поле Value (у wizard mode).
- Меню Games: вбудовані позиції, файли `.hack`, навчання (`tutorial-window`: позиції вантажаться одна за одною).
- Меню Actions: Take Back Move, Reset Game, Play Manual Game (людина проти людини), Abort (зупинити аналіз).
- Меню Settings: хто грає Blue, хто ходить першим, wizard mode, Edit Curves, шукати лише ненульові розфарбування.
- Меню Edit: New Empty Game, Edit Game, Save Game / Save Game As, Swap Colors, Delete, Copy / Shift / Insert Game / Insert Game Inverted, Test This Coloring, Find Good Colorings, Get Position Count.
- `settings-window` — Preferences: Wizard Mode, Snap to Grid (20 px), Skip Tutorial on Startup, Edit Curves, Stop Trivial Games.
- `help-window` — документація в меню Help.
- HUD: `game-value` (число позиції), підказка значення біля курсора (wizard), лічильник проаналізованих позицій під час довгого аналізу; кратні ребра — число поверх, змішані — пунктир червоно-синій.
- Переходи: Games → позиція → (аналіз стратегії) гра → Stop → редагування → Play.

## Фічі поза полем
- `ai-opponent-levels`: один, ідеальний — перед партією програма робить повний аналіз через surreal numbers (дівчинка з малюнка — 10 447 позицій; дві, що тримаються за руки, — мільйони).
- `hotseat` — режим Manual (комп'ютер як дошка); `undo` — Take Back Move; `restart-level` — Reset Game.
- `hint` — wizard mode: значення поточної позиції й позиції після кожного можливого зрізу (= ідеальна гра).
- `level-editor` + `export-import` — свої позиції у `.hack`; Swap Colors / Insert Game Inverted — складати позиції з потрібною перевагою.
- `difficulty-rating` — оцінка розфарбування: частка «вразливих» синіх ребер × частка різнокольорових вершин × частка програшних зрізів для Blue; Find Good Colorings зберігає 10 найкращих.
- Ліміти: до 64 ребер; пошук розфарбувань повний лише до 25 ребер.

## Варіації й родичі
- Green Hackenbush (безсторонній, Sprague–Grundy) · Blue-Red (числа) · Blue-Red-Green (нечислові значення: *, німбери) · Hackenstrings (рядки без розгалужень) · HAKENBUSH для iPad (Whitehead, Plambeck) — серії тематичних позицій (?).
- Корпус: [Shannon switching](shannon-switching.md) — теж хід = дія над ребром графа, але мета — звʼязність; [Sim](sim-pencil-game.md) — ребра фарбують, а не стирають; [Saboteur](saboteur.md) — обвал карти шляху; Nim (стебла Green Hackenbush).
- Осі варіацій: **хто що ріже** — усі все (Green) / кожен свій колір (Blue-Red) / змішано · **поле** — стебла / дерева / графи з циклами · **скінченність** — скінченна / нескінченна дошка · **мета** — normal play (останній хід виграє) / misère.

## Цікавинки для курсу
- Каскад «відірване від землі зникає»: BFS від землі після кожного зрізу — 📎.
- Значення стебла Blue-Red за двійковим правилом і сума незалежних частин → хто виграє — 📎.
- Green Hackenbush на деревах: colon principle (nim-сума гілок знизу вгору) і ідеальний AI — 🥉; з циклами (fusion principle) — 🥇.
- Значення довільної Blue-Red позиції через {L | R} і «найпростіше число між» з мемоізацією — 🥇.
- Редактор позицій: точки, ребра, кольори, земля, збереження в текстовий формат — 🥈.
- Wizard-підказка значення біля курсора — 🌱 поверх готового розвʼязувача.
- Генератор «складних» розфарбувань за метрикою Davis — 🥈.

## Мапа на каталог
- Є: `hot-seat` ↔ Manual; `turn-enforcement`; `ai-opponent` + `ai-minimax` ↔ ідеальний AI з повного аналізу; `cell-click` ↔ клік по ребру; `hover-highlight` ↔ wizard-підказка біля ребра; `no-moves-left` ↔ поразка без ходу; `connectivity-check` ↔ звʼязок із землею; `rule-variants` ↔ Green / Blue-Red / Blue-Red-Green; `level-solver` ↔ повний аналіз позиції; `difficulty-rating` ↔ оцінка розфарбувань; `in-game-editor` + `editor-palette` + `editor-draw-tools` + `editor-erase` + `editor-playtest` ↔ режими редагування й Play; `save-game` ↔ `.hack`; `undo-step` ↔ Take Back Move; `restart-level` ↔ Reset Game; `tutorial-window`, `help-window`, `settings-window`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+edge-cut-cascade` «Зріз ребра: усе, що втратило звʼязок із коренем, зникає» · entities/interact · 📎.
  - `+game-value-sum` «Значення позиції як число; сума незалежних частин» · game-logic/opponent · 🥉.
  - `+nim-reduction` «Зведення до Nim (Sprague–Grundy, colon / fusion)» · game-logic/opponent · 🥇.
  - `+value-hint` «Підказка: значення позиції після кожного можливого ходу» · game-logic/difficulty · 🌱 (поверх розвʼязувача).

## Пропозиції до словників
- `+role:node` / `+role:edge` — вершина й ребро графа як сутності (підтвердження: Shannon, Sim).
- `+effect:delete_edge` — видалити ребро графа (підтвердження: Shannon); тут замінено на `disappear(edge)`.
- `+ui:game-value` — поле зі значенням позиції (число / nimber) і знаком переваги.
- `+feature:wizard-mode` — показ значення позиції й наслідку кожного ходу (ідеальна підказка).
- `+axis:goal=normal-play` — мета «зробити останній хід» (хто без ходу — програв): Hackenbush, Nim.
- `+card:edge-cut-cascade`, `+card:game-value-sum`, `+card:nim-reduction`.

## Джерела
- ⭐ [Wikipedia: Hackenbush](https://en.wikipedia.org/wiki/Hackenbush) — правила, земля, normal play, варіанти, surreal numbers, Sprague–Grundy, colon / fusion principle з доведенням.
- [Tom Davis: What is Hackenbush?](http://geometer.org/hackenbush/index.html) — програма для Mac / Windows: гра проти комп'ютера, вбудовані позиції, редактор, ручний режим.
- [Hackenbush User's Guide (PDF)](http://geometer.org/hackenbush/hackdoc.pdf) — меню Games / Actions / Settings / Edit, Preferences, wizard mode, Stop Trivial Games, оцінка й пошук розфарбувань, ліміти 64 / 25 ребер, гарячі клавіші, згадка HAKENBUSH для iPad.
- [Tom Davis: Hackenbush (PDF)](http://geometer.org/mathcircles/hackenbush.pdf) — теорія Blue-Red: значення, {L | R}, стебла (двійкове правило), дерева, петлі (Berlekamp).
- [Hackenstrings, and 0.999… vs. 1](https://combinatorialgames.wordpress.com/2012/08/19/ii-4-hackenstrings-and-0-999-vs-1/) — рядкова версія (посилання з Wikipedia, не відкривав).

## Непевне
- (?) Рік: гра Conway зʼявилась у On Numbers and Games (1976) і Winning Ways (1982); поставлено 1976 — точну дату першої публікації не перевіряв.
- (?) HAKENBUSH для iPad (Whitehead, Plambeck) — лише згадка в посібнику Davis; чи доступний зараз — невідомо.
- (?) Чи є в програмі Davis окреме вікно кінця партії — посібник не каже; переможця, мабуть, видно з поля й напису.
- (?) Рівні складності AI — у програмі Davis лише ідеальний; інші реалізації не перевіряв.
