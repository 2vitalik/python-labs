---
title: Magicube
slug: magicube
aka: []
family: grid-platformer
also: [thinky]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2023
platforms: [PICO-8, PC, web]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2216120/Magicube/", best: true, note: "50 рівнів, керування: ←/→, Z — стрибок, X+стрілка — закляття, ↓ — undo, утримати ↑ — рестарт; реліз 29.06.2023"}
  - {kind: itch, url: "https://nebu-soku.itch.io/magicube", note: "раннє демо 0.03 (січень 2022), грати в браузері; коментарі: нове закляття прибирає старий куб, ціль — куб на постамент"}
  - {kind: other, url: "https://indietsushin.net/posts/2024-02-13-Magicube.html", note: "огляд: один магічний куб, постамент, лазери, кнопки, зникні й прозорі блоки, undo без меж"}
  - {kind: other, url: "https://indietsushin.net/posts/2024-02-17-Interview-with-nebu-soku", note: "інтервʼю: ядро — «вміння змусити блок зникнути», натхнення Portal і Recursed, 50 рівнів за півтора року"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magicube+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-by-input, keyboard-controls, gravity-fall, push-object, projectile-shot, all-on-targets, button-toggle, impassable-cells, player-death, undo-redo, undo-unlimited, restart-level, level-select, sequential-levels, pause-menu, movement-animation, particles, sound-effects, background-music, +push-chain, +jump-fixed-height, +shot-becomes-block, +one-summon-limit, +pressure-plate, +bridge-cell, +crush-by-fall, +hold-to-restart]
proposes: ["+trigger:crushed", "+card:shot-becomes-block", "+card:one-summon-limit", "+ui:goal-marker", "+feature:npc-hints"]
author: opus
date: 2026-11-09
---

# Magicube — чарівник закляттям кидає вбік жовтий куб-опору; поставиш цей куб на постамент — рівень пройдено

## Суть
PICO-8-головоломка з видом збоку: чарівник ходить, стрибає на одну клітину й штовхає кам'яні блоки, а закляттям (X + напрям) випускає снаряд, який летить до першої перешкоди й **стає жовтим магічним кубом**. Куб одночасно лише один: нове закляття прибирає старий — автор називає ядром саме «вміння змусити блок зникнути». Куб падає, штовхається й служить сходинкою, а мета рівня — покласти **саме його** на сірий постамент. 50 компактних однокімнатних рівнів, undo без меж.

## Поле і час
- Рівень — одна кімната зі сітки тайлів 8 px різного розміру (у демо від 10×12 до 17×17 клітин), відцентрована на екрані 128×128; камера нерухома.
- Час реальний: чарівник ходить по 1 px за кадр, стрибок підіймає приблизно на 1¼ клітини; блоки й куб завжди стоять у клітинах сітки, рух і падіння — анімовані (з коду демо).
- Гравітація вниз для чарівника, блоків і куба; блоки падають по 2 px за кадр.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Чарівник | player | напрям погляду | ходить, стрибає на ~1 клітину, штовхає ряд блоків, творить закляття лише стоячи на землі |
| Снаряд закляття | projectile | 2 px/кадр | летить горизонтально; перед стіною або блоком стає магічним кубом; у череп — гасне |
| Магічний куб (жовтий) | object | один на рівні | штовхається й падає як блок; опора; лише він активує постамент |
| Камʼяний блок | object | — | штовхається рядом, якщо за останнім вільно; падає без опори; опора |
| Постамент | static | стрілка над ним | магічний куб, що стоїть на ньому → перемога |
| Стіна | static | — | непрохідна для всіх, зупиняє снаряд |
| Кнопка | switch | натиснута / ні | поки на ній стоїть чарівник чи блок — усі мости рівня тверді |
| Міст (пунктир) | gate | твердий / нема | зʼявляється при натиснутій кнопці, крім клітин, де хтось стоїть |
| Череп | neutral | — | говорить підказки; блоки на нього спираються, снаряд об нього гасне |
| Лазер, зникні й прозорі блоки, червоний перемикач | hazard / gate | — | елементи повної версії; поведінка в джерелах не описана (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(wizard, dir)` (по пікселю); КОЛИ `input(z)` → ЯКЩО `supported(wizard)` → ТО `custom: «стрибок ≈ 1 клітина»`.
- КОЛИ `contact(wizard, block)` під час ходьби → ЯКЩО `supported(wizard)` і `custom: «ряд суміжних блоків закінчується вільною клітиною»` → ТО `custom: «після короткої затримки»` `push` (усього ряду на 1 клітину), `move(wizard, dir)`; інакше `block`.
- КОЛИ `input(x)` → ЯКЩО `supported(wizard)` і `not state(wizard, jumping)` → ТО `set_state(wizard, chanting)` (золота аура); повторний X — `clear_state`.
- КОЛИ `input(dir)` → ЯКЩО `state(wizard, chanting)` і `custom: «у напрямку поруч нема стіни»` → ТО `disappear(magic_cube)` (старий), `spawn_at(spell_shot, beside_wizard)`, `move(spell_shot, dir)` щокадру.
- КОЛИ `blocked(spell_shot)` (стіна або блок у сусідній клітині) → ТО `transform(spell_shot, magic_cube)` у клітині сітки.
- КОЛИ `contact(spell_shot, skull)` → ТО `disappear(spell_shot)` — куб не зʼявляється.
- КОЛИ `tick` → ЯКЩО `not supported(block|magic_cube)` → ТО `fall(block)`.
- КОЛИ `custom: «блок упав на чарівника»` → ТО `lose` (чарівник розплющений; лише undo повертає).
- КОЛИ `enter(wizard|block, button)` → ТО `set_cell(bridges, solid)` для вільних клітин мостів; КОЛИ `leave(…, button)` → ТО `set_cell(bridges, empty)`.
- КОЛИ `all_on(magic_cube, pedestal)` → ТО `win`, `message(«LEVEL CLEARED»)`, `next_level`.
- КОЛИ `input(down)` → ТО `undo(1)` — стан після кожного поштовху й закляття, без ліміту; працює і після смерті.
- КОЛИ `input(hold up)` (повна версія) або пункт меню «restart level» (демо) → ТО `restart`.
- Перемога: магічний куб на постаменті. · Поразка: розчавлення блоком → undo. · Рахунку нема.

## Керування і ввід
- ← / → — ходьба (і поштовх, якщо впираєшся в блок); Z — стрибок (у меню — вибір).
- X — почати закляття; потім ← або → — напрям пострілу; X ще раз — скасувати.
- ↓ — undo; утримання ↑ — рестарт (Steam); Enter — меню PICO-8. Клавіші не переназначаються; геймпад підтримується.

## Вікна, меню, HUD
- `splash-screen` / заставка PICO-8 (?).
- `level-select` — назва «magicube», сітка номерів рівнів по 5 у ряд; курсор стрілками, Z — старт.
- `game-screen` — кімната по центру, `level-number` «level N» у куті; `custom` анімована стрілка над постаментом; діалоги черепа в рамці з лінією до нього (перші рівні: «Welcome, new challenger…», «[Z] to jump», «[X] to chant», «[↓] to undo», «restart from menu»).
- `end-screen` — накладка «LEVEL CLEARED» з анімацією постаменту, шторка-перехід до наступного рівня.
- `pause-menu` (Enter): restart level · level select + стандартні пункти PICO-8 (звук, повноекранний режим).
- Повна версія: зачинені двері «0/40» — секретна зона після 40 пройдених рівнів (огляд Indie Tsushin) (?).
- Переходи: level-select → шторка → game-screen → (куб на постаменті) LEVEL CLEARED → наступний рівень.

## Фічі поза полем
- `undo` без ліміту, `restart-level`, `level-select`, `levels-sequential`; `npc-hints` — підказки черепа в перших рівнях.
- Налаштування — лише стандарт PICO-8: звук увімк/вимк, вікно/повний екран.
- Демо 0.03 (21 рівень) закінчувалось екраном «thanks for playing! post a comment».

## Варіації й родичі
- У сімʼї: [Toki Tori](toki-tori.md) і [Boxboy](boxboy.md) (створення блоків як інструмент), [Solomon's Key](solomons-key.md) (чарівник творить блоки поруч), [Block Dude](block-dude.md).
- Поза сімʼєю: Portal (скидання куба як ідея, за інтервʼю), Recursed (пазл-платформер), Baba Is You і Stephen's Sausage Roll (вплинули на складність).
- Осі варіацій:
  - **де зʼявляється блок**: поруч (Solomon's Key) / там, де зупинився снаряд (Magicube) / власна форма (Boxboy);
  - **скільки блоків одночасно**: один, новий прибирає старий (тут) / ліміт / без ліміту;
  - **що активує ціль**: будь-який блок / лише особливий (тут) / сам гравець.

## Цікавинки для курсу
- Снаряд, що стає блоком у клітині перед перешкодою — 📎.
- «Один куб на рівні»: нове закляття прибирає старий — 🌱, але змінює весь дизайн пазлів.
- Кнопка, що тримає мости, поки на ній щось стоїть (і не створює міст у зайнятій клітині) — 🥉.
- Поштовх ряду блоків із затримкою і гравітацією блоків у сітці при піксельному русі гравця — 🥉.
- Undo-стек станів (гравець + усі блоки + куб) з відновленням після смерті — 📎.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls`; `gravity-fall` ↔ блоки й куб; `push-object` ↔ камʼяні блоки; `projectile-shot` ↔ закляття; `all-on-targets` ↔ куб на постаменті; `button-toggle` ↔ кнопка й мости; `impassable-cells` ↔ стіни; `player-death` ↔ розчавлення; `undo-redo` + `undo-unlimited` + `restart-level`; `level-select` + `sequential-levels`; `pause-menu`; `movement-animation`, `particles` (аура, пил), `sound-effects`, `background-music`.
- **Нема** → пропозиції карток:
  - `+shot-becomes-block` «Снаряд перетворюється на блок там, де зупинився» · entities/spawn · 📎.
  - `+one-summon-limit` «Створена сутність лише одна: нова прибирає стару» · entities/spawn · 🌱.
  - `+push-chain`, `+jump-fixed-height`, `+pressure-plate`, `+bridge-cell`, `+crush-by-fall`, `+hold-to-restart` — уже пропоновані в корпусі.

## Пропозиції до словників
- `+trigger:crushed` — сутність розчавлена блоком, що впав (тут — смерть чарівника).
- `+card:shot-becomes-block`, `+card:one-summon-limit` — див. вище.
- `+ui:goal-marker` — анімована стрілка над ціллю рівня.
- `+feature:npc-hints` — підказки персонажа-провідника в перших рівнях.

## Джерела
- ⭐ [Steam: Magicube](https://store.steampowered.com/app/2216120/Magicube/) — 50 рівнів, керування, опції PICO-8, дата 29.06.2023, розробник nebu soku.
- [itch.io: Magicube (early demo)](https://nebu-soku.itch.io/magicube) — демо 0.03 у браузері, коментарі гравців і автора про правила.
- [Indie Tsushin: огляд](https://indietsushin.net/posts/2024-02-13-Magicube.html) — один куб, постамент, лазери, кнопки, зникні й прозорі блоки, undo, двері «0/40».
- [Indie Tsushin: інтервʼю з nebu soku](https://indietsushin.net/posts/2024-02-17-Interview-with-nebu-soku) — задум «блок зникає», Portal, Recursed, 50 рівнів, undo в PICO-8.
- Код картриджа демо 0.03 з HTML5-збірки на itch — точні правила закляття, куба, поштовху, мостів, смерті, undo, вибору рівня, тексти черепа.
- YouTube: пошук «Magicube gameplay».

## Непевне
- (?) Правила лазерів, червоного перемикача, зникних і прозорих блоків повної версії — у відкритих джерелах лише згадки; код є тільки для демо.
- (?) Кількість рівнів: Steam і інтервʼю — 50; огляд Indie Tsushin пише і про 45 одразу доступних, і про секретну зону після 40.
- (?) Чи змінилися в релізі деталі демо (затримка перед поштовхом, умова «поруч нема стіни» для закляття).
