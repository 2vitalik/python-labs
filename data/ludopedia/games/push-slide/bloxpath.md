---
title: Bloxpath
slug: bloxpath
aka: []
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2025
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/3249900/Bloxpath/", best: true, note: "опис (~200 пазлів, ~10 базових механік, дерево відкриття), скріншоти з керуванням і склом, трейлер і gameplay-відео"}
  - {kind: itch, url: "https://agoo.itch.io/bloxpath", note: "безкоштовна web/Windows-версія 2024: ~30 пазлів, ~4 механіки, без перемикачів і тупиків (Unity)"}
  - {kind: other, url: "https://agoo.itch.io/bloxpath/devlog/780562/postmortem-designing-and-developing-bloxpath-in-one-month", note: "постмортем: брусок котиться площиною, стіни, симетрія, кілька стартів і фінішів, кольори, вибір бруска; що прибрано з Bloxorz"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Bloxpath+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [move-4dir, keyboard-controls, cell-click, controls-remap, multi-cell-size, orientation-state, height-levels, party-switch, all-on-targets, reach-exit, undo-redo, redo, restart-level, world-map, level-unlock, save-progress, game-settings, language-picker, movement-animation, level-solver, +roll-block, +glass-wall, +block-as-bridge, +camera-rotate, +hint-midpoint-state, +input-buffer, +puzzle-replay]
proposes: ["+effect:tip", "+role:glass-wall", "+feature:hint-midpoint-state", "+feature:input-buffer", "+card:block-as-bridge", "+card:glass-wall"]
author: opus
date: 2026-11-19
---

# Bloxpath — котити бруски, як у Bloxorz, але кількома одразу, по сходинках і повз скляні стіни

## Суть
Мінімалістична «roll-playing» головоломка за мотивами Flash-гри Bloxorz: гравець перекочує прямокутні бруски 1×1×2 (і кубики) по плитках, щоб поставити їх на цілі. У першій (місячній) версії автор свідомо прибрав із Bloxorz перемикачі, помаранчеві плитки й телепорти і будував статичні пазли «як у The Witness»: стіни, симетрія, кілька стартів і фінішів, кольори. Головне ускладнення — **кілька брусків**, між якими перемикаєшся: один брусок, ліг у западину, стає підлогою для іншого. Steam-версія — ~200 пазлів на великій мапі-хабі з деревом відкриття.

## Поле і час
- Квадратна сітка плиток над порожнечею; плитки бувають різної висоти (западини, уступи, «вежі»). Рендер — ізометричне 3D, логіка — 2D-сітка + висота + орієнтація (постмортем: «a long block rolls on a plane… effectively 2D»).
- Стан бруска: клітинки + орієнтація `standing` / `lying_x` / `lying_y`; кілька брусків на полі, активний підсвічено.
- Скляні стіни — прозорі панелі на ребрах клітинок.
- Хід = одне перекидання активного бруска; без вводу нічого не змінюється. Камеру можна повертати на 90°.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Брусок 1×1×2 | player | орієнтація; колір; активний / ні | перекочується на 90° у 4 напрямках; займає 1 або 2 клітинки |
| Кубик 1×1×1 | player | колір | перекочується на 1 клітинку |
| Неактивний брусок | object | — | стоїть, доки не вибрали; є опорою й перешкодою для інших |
| Плитка | terrain | висота | опора; уступ вищий за брусок не пропускає (?) |
| Ціль | static | колір | квадрат на плитці; брусок на ній — фініш; після розвʼязку опускається діркою |
| Скляна стіна | static | ребро | прозора стінка між клітинками; не пускає брусок через ребро (?) |
| Плита, що тоне | terrain | — | за описом Thinky Games (?) |
| Хаб-плитка входу | static | «розвʼязано / всього» | вхід у пазл з мапи; дріб показує прогрес |
| Плитка «?» (хаб) | static | — | підказка правил у хабі (з патча 3.3.2) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `state(block, standing)` → ТО `rotate(block, 90)`, `custom: «лягає на дві клітинки в бік dir»`.
- КОЛИ `input(dir)` → ЯКЩО `state(block, lying)` і `custom: «вісь бруска ∥ dir»` → ТО `rotate(block, 90)`, `custom: «встає на клітинку за дальнім кінцем»`.
- КОЛИ `input(dir)` → ЯКЩО `state(block, lying)` і `custom: «вісь бруска ⊥ dir»` → ТО `rotate(block, 90)`, `move(block, dir)`.
- КОЛИ `input(dir)` → ЯКЩО `not supported(block)` або `custom: «на шляху скло, уступ чи інший брусок»` → ТО `block` (?).
- КОЛИ `input(switch)` → ТО `custom: «активним стає інший брусок»` (1/2, цифри 1–9, Space, миша).
- КОЛИ `enter(block, pit)` → ЯКЩО `custom: «брусок лягає врівень із сусідньою підлогою»` → ТО `custom: «інші бруски котяться по ньому, як по плитці»`.
- КОЛИ `enter(block, target)` → ЯКЩО `same(block, target, color)` → ТО `custom: «ціль зайнята»`; стоячий брусок на цілі — як у Bloxorz (?).
- КОЛИ `all_on(block, target)` → ТО `win`, `custom: «ціль опускається діркою, повернення в хаб»`.
- КОЛИ `input(undo)` → ТО `undo(1)`.
- КОЛИ `input(redo)` → ТО `custom: «повернути скасований хід»`.
- КОЛИ `input(reset)` → ТО `restart`.
- КОЛИ `input(hint)` → ЯКЩО `custom: «для пазла налаштовано Thought Alignment»` → ТО `custom: «показати проміжний стан розвʼязку»`.
- Перемога: усі цілі зайняті (кілька фінішів — кілька брусків). · Поразка: нема — тупиків нема (itch-версія), вихід через undo/R (?). · Рахунок: нема; прогрес — «Solved N / 203».

## Керування і ввід
- Стрілки / WASD (у пазлах зі «спеціальною перспективою» — підказки напрямків), R — Reset Puzzle, Z — Undo, X — Redo, 1/2 — Switch Blox, цифри 1–9 — швидкий вибір, Space — наступний брусок, миша — Select Blox.
- Клавіатура, миша (режим «лише миша»), геймпад; буфер вводу й налаштовна затримка повтору; перепризначення клавіш з автообміном (3.3.3); поворот камери на 90° (3.2.18).

## Вікна, меню, HUD
- `main-menu`: Start Game · Game Settings · Exit Game (номер збірки в куті).
- `map-window` — хаб: мережа доріжок, регіони з вузлами-пазлами, вхідні плитки з дробом «розвʼязано / всього»; гравець котить по хабу свій брусок.
- `game-screen` — пазл у хабі (без завантажень); HUD — підказки клавіш ліворуч угорі.
- `pause-menu` (Esc): Continue Game · Back to Hub · Reset Position · Game Settings · Credits · Save Files · Feedback · Exit Game; унизу «Solved 39 / 203 total», угорі координати / ID пазла (A-01 … Z-07).
- `hints-window` — Thought Alignment: проміжний стан розвʼязку (червоні й більшість жовтих пазлів).
- `settings-window` — мова (10), керування, частота кадрів / VSync, режим камери.
- Переходи: титул → хаб → пазл → (розвʼязано) хаб; пауза → хаб / налаштування / сейви.

## Фічі поза полем
- `world-map` з деревом відкриття: застряг — іди в інший регіон; `puzzle-replay` — постояти на вході розвʼязаного пазла.
- `undo` (∞) + `redo` + `restart-level`; `+hint-midpoint-state` (Thought Alignment).
- `save-slots` (Save Files) (?), `cloud-save`, `achievements` (10: «Klotski», «Mirror Maze», «Swap», «The Great Tower», «Roll A Dice»…).
- `remap-controls`, `gamepad-support`, `mouse-and-keyboard`, `localization` (10 мов).
- Окрема безкоштовна web/Windows-версія 2024 (30 пазлів) — рання версія; Steam-версія новіша й більша.

## Варіації й родичі
- [Bloxorz](bloxorz.md) — пряме натхнення; тут без перемикачів, крихких плиток і телепортів, зате кілька брусків, висоти, скло, кольори.
- Осі варіацій перекочування:
  - **скільки тіл**: одне (Bloxorz) / розщеплення на два (Bloxorz split) / кілька незалежних з перемиканням (Bloxpath);
  - **висота**: пласке поле / западини й уступи, брусок як міст (тут);
  - **стіни**: лише краї плиток / прозорі стіни на ребрах (тут);
  - **що в орієнтації важить**: клітинки (тут) / грані ([Billy Bumbum](billy-bumbum.md), [Stephen's Sausage Roll](../thinky/stephens-sausage-roll.md)).
- Родичі: [Lost in Cheese](lost-in-cheese.md), Cuboid, Edge (див. файл Bloxorz).

## Цікавинки для курсу
- Таблиця перекидів бруска 1×1×2 (3 орієнтації × 4 напрямки) — 📎.
- Кілька брусків з перемиканням + брусок як опора для іншого (висота клітинки = підлога + що на ній лежить) — 🥈.
- Стіни на ребрах, що зупиняють перекид (перевірка ребер, через які проходить брусок) — 📎.
- Хаб-мапа з деревом відкриття і дробами прогресу — 🥉.
- Підказка «проміжний стан» замість готового ходу — 🌱 як фіча, 🥇 як автогенерація з BFS-розвʼязувача.
- BFS-розвʼязувач для кількох брусків (стан = позиції й орієнтації всіх) — 🥈; автор писав солвер для перевірки пазлів.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` + `cell-click` + `controls-remap`; `multi-cell-size` + `orientation-state` ↔ брусок; `height-levels` ↔ уступи й западини; `party-switch` ↔ кілька брусків; `all-on-targets` + `reach-exit` ↔ цілі; `undo-redo` + `redo` + `restart-level`; `world-map` + `level-unlock`; `save-progress`; `game-settings` + `language-picker`; `movement-animation`; `level-solver` ↔ солвер автора.
- **Нема** → пропозиції карток:
  - `+roll-block` (є в корпусі) — перекочування бруска.
  - `+glass-wall` «Прозора стіна на ребрі клітинок» · entities/legality · 🌱.
  - `+block-as-bridge` «Тіло, що лягло в западину, стає підлогою» · entities/legality · 📎.
  - `+camera-rotate` (є в корпусі) — поворот ізокамери на 90°.
  - `+hint-midpoint-state` «Підказка — проміжний стан розвʼязку» · game-logic/history · 🌱.
  - `+input-buffer` «Буфер вводу й затримка повтору» · interface/input · 🌱.
  - `+puzzle-replay` «Повторити розвʼязаний пазл з хабу» · levels/progression · 🌱.
  - (?) `+sinking-tile` — «плити, що тонуть» (опис Thinky Games), правил не бачив.

## Пропозиції до словників
- `+effect:tip` — перекид через ребро зі зміною зайнятих клітинок (повтор; `roll` у словнику — скочування з округлого).
- `+role:glass-wall` — прозора стінка на ребрі, що блокує рух, але не огляд.
- `+feature:hint-midpoint-state`, `+feature:input-buffer` — див. «Мапу».
- `+card:block-as-bridge`, `+card:glass-wall` — див. «Мапу на каталог».

## Джерела
- ⭐ [Steam: Bloxpath](https://store.steampowered.com/app/3249900/Bloxpath/) — опис (Bloxorz, ~200 пазлів, ~10 базових механік, багатобрускові взаємодії, дерево відкриття, буфер вводу), 9 скріншотів (R/Z/X, «1 2 Switch Blox», «Select Blox», скляні стіни, хаб із дробами), трейлер і gameplay-відео (титул, хаб, пазл з трьома брусками, пауза «Solved 39 / 203»), 10 досягнень; Steam News (Thought Alignment, ID пазлів, «?»-плитки, обмін клавіш, Space для наступного бруска, numpad 1–9, поворот камери, «glass panel», replay пазла).
- [itch: Bloxpath](https://agoo.itch.io/bloxpath) — безкоштовна версія 2024: ~4 механіки, ~30 пазлів, «no switches and no dead ends», Unity.
- [Постмортем «Bloxpath in One Month»](https://agoo.itch.io/bloxpath/devlog/780562/postmortem-designing-and-developing-bloxpath-in-one-month) — котіння площиною, стіни, симетрія, кілька стартів і фінішів, кольори, «white block», простий вибір брусків, прибрані перемикачі / помаранчеві плитки / телепорти.

## Непевне
- (?) Що саме робить скляна стіна (блок через ребро для будь-якої орієнтації чи лише для лежачого бруска) — видно лише на скріншотах.
- (?) «Плити, що тонуть» і «кілька брусків» з рядка черги: другі підтверджено, перші — лише в пошуковому описі Thinky Games (сторінка дає 403).
- (?) Чи брусок може впасти з краю (у web-версії «no dead ends»), чи ціль вимагає стоячого положення, чи бруски штовхають один одного.
- (?) Назви досягнень («Mirror Maze», «Swap» = 传送交换 «телепорт-обмін», «Roll A Dice», «The Great Tower», «Klotski») натякають на дзеркальний рух, обмін місцями, кубик-кістку й вежі — правил не бачив.
- (?) «White block» з постмортему — поведінку не описано.
