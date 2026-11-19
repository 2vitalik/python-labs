---
title: Lava and Aqua
slug: lava-and-aqua
aka: [Lava & Aqua]
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
year: 2022
platforms: [web]
links:
  - {kind: itch, url: "https://rob1221.itch.io/lava-and-aqua", best: true, note: "грати в браузері; мета й керування (WASD, Z/U undo, R, Esc/B)"}
  - {kind: play, url: "https://www.coolmathgames.com/0-lava-and-aqua", note: "Cool Math Games: інструкції, лічильник 0/24 рівнів, «water that touches lava creates a barrier»"}
  - {kind: play, url: "https://mathplayground.com/puzzle_lava_and_aqua.html", note: "Math Playground: «lava will flow every time you take a step», «push blocks to seal off lava pipes»"}
  - {kind: play, url: "https://www.crazygames.com/game/lava-and-aqua", note: "CrazyGames: автор Robert Alvarez, червень 2022"}
  - {kind: other, url: "https://www.bontegames.com/2022/06/lava-and-aqua-browser.html", note: "Bart Bonte; коментарі гравців про таймери й блоки"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Lava+and+Aqua+rob1221+walkthrough", note: "пошук; проходження"}
stage: v1
coverage: 80
mechanics: [move-4dir, move-by-input, keyboard-controls, push-object, impassable-cells, reach-exit, key-and-door, button-toggle, environment-death, player-death, timed-despawn, undo-redo, undo-unlimited, restart-level, sequential-levels, level-select, level-unlock, save-progress, volume-control, main-menu, game-screen, +spreading-terrain, +reaction-table, +countdown-tile, +pressure-plate, +block-displaces-fluid, +fluid-stop-cell]
proposes: ["+effect:spread", "+card:block-displaces-fluid", "+card:fluid-stop-cell"]
author: opus
date: 2026-11-19
---

# Lava and Aqua — після кожного кроку лава й вода розтікаються на клітину: дійди до виходу, поки лава не наздогнала

## Суть
Покрокова кімнатна головоломка з видом згори: персонаж іде до порталу-виходу, а після кожного його кроку лава й вода розширюються на одну клітину в усі 4 боки. Де вода зустрічає лаву, клітина застигає каменем — так воду використовують як щит, а блоки штовхають, щоб перекрити «труби» з лавою або випустити воду. Додаткові елементи: стіни з таймером ходів, плита-перемикач зі стінами, ключі, що активують вихід. Автор — Robert Alvarez (rob1221), рушій Stencyl; 24 рівні.

## Поле і час
- Квадратна сітка одного екрана; шари: плитки (стіна, лава, вода, камінь) + актори (гравець, блоки, стіни з таймером, стіни-перемикачі, ключі, вихід, плити, стоки).
- Хід = один крок гравця (з поштовхом блока); без вводу світ стоїть. Таймера реального часу нема.
- Фази ходу після кроку (з коду): вихід → ключ → блоки витісняють рідину → плити-перемикачі → розтікання води → розтікання лави → стіни з таймером −1 → перевірка смерті.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | — | крок у 4 напрямки; штовхає блок; стоїть у воді безпечно; у лаві гине |
| Стіна | static | — | непрохідна для гравця, блоків і рідин |
| Блок | object | — | штовхається на 1, якщо за ним не стіна й не інший блок; заштовхнутий у рідину витісняє її; рідину крізь себе не пускає |
| Лава | hazard | — | щоходу займає сусідні (4) порожні клітини; сусідня вода → камінь |
| Вода (Aqua) | terrain | — | щоходу займає сусідні (4) порожні клітини; сусідня лава → камінь |
| Камінь | static | — | утворюється, де вода й лава зустрілись; стіна для всіх |
| Стіна з таймером | static | число N на стіні | кожен хід N−1; на 0 зникає; поки стоїть — блокує гравця й рідини |
| Плита-перемикач | switch | — | поки на будь-якій плиті стоїть гравець або блок — усі стіни-перемикачі відчинені |
| Стіна-перемикач | gate | відчинено / зачинено | зачинена — стіна для гравця й рідин; відчинена — прохід |
| Ключ | pickup | — | береться кроком гравця; коли зібрано всі — вихід активується |
| Вихід (фіолетовий портал) | static | активний / неактивний | неактивний, доки на рівні є незібрані ключі; гравець на активному виході → рівень пройдено |
| Сток (Drain) | terrain | — | рідина в цю клітину не тече; лежить під гравцем, як плита (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` (не стіна, не камінь, не зачинена стіна, не стіна з таймером) → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `contact(player, block)` → ЯКЩО `free(cell_behind)` і `not occupied(cell_behind, block)` → ТО `push`, `move(player, dir)`; інакше `block`.
- КОЛИ `enter(player, exit)` → ЯКЩО `state(exit, active)` → ТО `win`, `next_level` (Level NN → наступна сцена).
- КОЛИ `enter(player, key)` → ТО `pickup`; КОЛИ `all_gone(key)` → ТО `set_state(exit, active)`.
- КОЛИ `enter(block, water|lava)` → ТО `set_cell(cell, empty)` — блок витісняє рідину зі своєї клітини.
- КОЛИ `after(move)` → ЯКЩО `occupied(any_switch, player|block)` → ТО `set_state(switch_walls, open)`; інакше `set_state(switch_walls, closed)`.
- КОЛИ `after(move)` → ТО для кожної клітини води `custom: «вода займає кожну сусідню (4) порожню клітину»`; ЯКЩО `cell(neighbor, lava)` → ТО `set_cell(neighbor, stone)`.
- КОЛИ `after(water)` → ТО для кожної клітини лави `custom: «лава займає кожну сусідню (4) порожню клітину»`; ЯКЩО `cell(neighbor, water)` → ТО `set_cell(neighbor, stone)`.
- Рідина не тече в клітини з блоком, стіною, каменем, стіною з таймером, зачиненою стіною-перемикачем і стоком; у клітину гравця — тече.
- КОЛИ `after(move)` → ТО `counter(timer_wall, -1)`; КОЛИ `counter(timer_wall, ==, 0)` → ТО `disappear_a`.
- КОЛИ `enter(lava, player_cell)` або `custom: «клітина гравця застигла каменем»` → ТО `lose` (анімація смерті; далі лише undo або рестарт).
- КОЛИ `input(Z|U)` → ТО `undo(1)` — відкочує крок, рідини, камінь, ключ, перемикачі й таймери; `input(R)` → `restart`; `input(Esc|B)` → `window(level-select)`.
- Перемога: гравець на активному виході. · Поразка: торкнувся лави / замурований каменем (тимчасова — undo). · Рахунку нема; ліміту ходів нема.

## Керування і ввід
- WASD або стрілки — крок (з поштовхом блока); Z або U — undo; R — рестарт; Esc або B — назад.
- Меню: Enter або Space — старт; вліво/вправо — гучність музики й звуків.
- На тач-пристроях (Math Playground) — екранні кнопки.

## Вікна, меню, HUD
- `main-menu`: назва, «by Robert Alvarez», «Press Enter or Space to Start», підказка керування (Move / Undo / Reset / Back), налаштування гучності Music і Sound.
- `level-select`: сітка кнопок рівнів зі станами Locked / Unlocked / Completed.
- `game-screen`: поле на весь екран; на старті рівня — назва «Level NN», що згасає; число на кожній стіні з таймером.
- `end-screen` («End Scene»): «Thanks for Playing» після останнього рівня.
- Переходи: main-menu → level-select → game-screen → (вихід) наступний рівень з плитковим переходом → … → end-screen; Esc/B → level-select.

## Фічі поза полем
- `undo` без ліміту (стек дій з точним відкатом рідин), `restart-level`.
- `levels-sequential` + `level-unlock`: пройдений рівень відкриває наступний; прогрес зберігається (`autosave`).
- `volume-sliders` для музики й звуків; у версії для Newgrounds — медалі за 4/8/12/16/20/24 пройдені рівні (`achievements`).
- Нема редактора, підказок, рахунку, ліміту ходів.

## Варіації й родичі
- [Sokoban](../push-slide/sokoban.md) — штовхання по одному блоку; [Wildfire Swap](wildfire-swap.md) — вогонь шириться після кожного ходу гравця; [Forest-fire model](../build-sim/forest-fire-model.md) — поширення по сусідах як автомат; [Terraria: рідини](../build-sim/terraria-liquids.md) — вода + лава → обсидіан.
- [Chip's Challenge](../maze-arcade/chips-challenge.md): блок у воду → земля (тут блок витісняє рідину).
- Осі варіацій: **швидкість поширення** — щоходу / раз на N ходів · **сусідство** — 4 / 8 · **реакція рідин** — камінь / нейтралізація / нічого · **що спиняє рідину** — стіна, блок, таймер-стіна, сток · **рідина і гравець** — безпечна (вода) / смертельна (лава).

## Цікавинки для курсу
- Поширення рідин «фронтом» по знімку стану: зібрати цілі, потім застосувати (інакше рідина пробіжить кілька клітин за хід) — 📎.
- Порядок фаз ходу (вода раніше за лаву, таймери після рідин) як явний конвеєр подій — 🥉.
- Undo з точним відкатом рідин, каменю, ключів і перемикачів (журнал змін на хід) — 🥉.
- Плита-перемикач, натиснута, поки на ній гравець або блок — 🌱; стіна з лічильником ходів — 🌱.
- Розвʼязувач «перегони з лавою» (BFS по станах «гравець + блоки + рідини») — 🥇: стан росте з кожним ходом.

## Мапа на каталог
- Є: `move-4dir` + `move-by-input` + `keyboard-controls` ↔ крок; `push-object` ↔ блоки; `impassable-cells` ↔ стіни й камінь; `reach-exit` ↔ портал; `key-and-door` ↔ ключі активують вихід; `button-toggle` ↔ плита й стіни-перемикачі; `environment-death` + `player-death` ↔ лава / замурування; `timed-despawn` ↔ стіна з таймером зникає; `undo-redo` + `undo-unlimited` + `restart-level`; `sequential-levels` + `level-select` + `level-unlock` + `save-progress`; `volume-control`; `main-menu`, `game-screen`.
- **Нема** → пропозиції карток:
  - `+spreading-terrain` (є в корпусі) — слот {rate: 1 клітина/хід, neighbors: 4}.
  - `+reaction-table` (є в корпусі) — вода × лава → камінь.
  - `+countdown-tile` (є в корпусі) — стіна з лічильником ходів.
  - `+pressure-plate` (є в корпусі) — плита, натиснута гравцем або блоком.
  - `+block-displaces-fluid` «Блок, заштовхнутий у рідину, витісняє її зі своєї клітини» · entities/interact · 🌱.
  - `+fluid-stop-cell` «Клітина, куди рідина не тече, хоч гравець по ній ходить» · entities/legality · 🌱.

## Пропозиції до словників
- `+effect:spread` — клітина-стихія займає сусідні вільні клітини (лава, вода); у корпусі вже багато разів, у словнику нема.
- `+card:block-displaces-fluid`, `+card:fluid-stop-cell` — див. «Мапа на каталог».

## Джерела
- ⭐ [itch.io: Lava and Aqua](https://rob1221.itch.io/lava-and-aqua) — гра в браузері, мета «reach the exit without touching the lava», керування; у коментарях автор: «You can push the block up from the bottom», «you can't block the lava in that level».
- [Cool Math Games](https://www.coolmathgames.com/0-lava-and-aqua) — «get to the purple portal before the lava reaches you», ящик перед лавою, «water that touches lava creates a barrier», 24 рівні.
- [Math Playground](https://mathplayground.com/puzzle_lava_and_aqua.html) — «The lava will flow every time you take a step», «Push blocks to seal off lava pipes», екранні кнопки на тачі.
- [CrazyGames](https://www.crazygames.com/game/lava-and-aqua) — автор, дата (червень 2022), керування.
- [bontegames](https://www.bontegames.com/2022/06/lava-and-aqua-browser.html) — коментарі: «riveted blocks» рухаються, «timers».
- Збірка гри (Stencyl/OpenFL, `Lava and Aqua.js` + `lib/default.pak`): типи акторів (Player, Block, Exit, Exit Key, Switch, Switch Wall, Timed Wall, Drain), фази ходу в `Game Functions`, розтікання й камінь, undo в `Grid Controller`, тексти меню.
- Проходження progameguides «How to beat Lava and Aqua» бачив у пошуку (зелені числа — ходи до зникнення блока), сторінка віддає 403 у фетчі.

## Непевне
- (?) Сток (Drain): з коду лише видно, що рідина в його клітину не тече і він лежить на нижньому шарі; як виглядає і чи ходить по ньому гравець — не перевірено.
- (?) Багатоклітинні блоки: у коді є групи акторів (Group ID), що рухаються разом; чи є такі блоки в рівнях — не перевірено.
- (?) «On/off block» і «metal block» з коментарів гравців — імовірно плита-перемикач і стіна-перемикач.
- (?) Як саме виглядає перехід між рівнями на CoolMath (там можуть бути власні меню/реклама).
