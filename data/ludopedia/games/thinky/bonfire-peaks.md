---
title: Bonfire Peaks
slug: bonfire-peaks
family: thinky
also: [push-slide, grid-platformer]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC, Mac, Linux, Switch, PS4, PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bonfire_Peaks", best: true, note: "геймплей: уперед/назад/поворот без кроку вбік, до 6 ящиків на собі, підйом лише ящиків на рівні ніг, мета — ящик з речами у вогнище; хаб, undo, 200+ рівнів"}
  - {kind: official, url: "https://bonfirepeaks.com/", note: "офіційний сайт: Corey Martin + Alan Hazelden, Draknek & Friends; платформи"}
  - {kind: steam, url: "https://store.steampowered.com/app/1147890/Bonfire_Peaks/", note: "досягнення, Steam Cloud, 11 мов; DLC Lost Memories"}
  - {kind: steam, url: "https://store.steampowered.com/app/2008250/Bonfire_Peaks_Lost_Memories/", note: "DLC «Lost Memories» (2023–2025)"}
  - {kind: play, url: "https://draknek.itch.io/bonfire-peaks", note: "itch.io: Photo Mode, коментар розробника про повороти довгих ящиків"}
  - {kind: other, url: "http://bonfirepeaks.com/press/", note: "прес-кіт: хаб-острів, можна пропускати рівні, трейлери"}
  - {kind: youtube, url: "http://www.youtube.com/watch?v=w9gzBfD5qS8", note: "Aliensrock: проходження демо — правила в дії"}
  - {kind: youtube, url: "http://www.youtube.com/watch?v=yGd1cP_dKQE", note: "трейлер з датою релізу"}
stage: v1
coverage: 65
mechanics: [move-by-input, keyboard-controls, gravity-fall, impassable-cells, multi-cell-size, orientation-state, floor-types, reach-exit, sequential-levels, level-unlock, save-progress, movement-animation, player-camera, +tank-controls, +height-levels, +carry-stack, +climb-step, +burn-goal, +undo-redo, +world-map, +optional-levels, +photo-mode]
proposes: ["+trigger:input", "+trigger:enter", "+cond:free", "+cond:supported", "+cond:count", "+cond:facing", "+effect:move", "+effect:face", "+effect:fall", "+effect:carry", "+effect:drop", "+effect:climb", "+effect:destroy", "+role:hazard", "+role:terrain", "+window:map-window", "+feature:undo", "+feature:world-map", "+feature:photo-mode", "+axis:undo"]
author: opus
date: 2026-11-02
---

# Bonfire Peaks — тримай ящики на голові, будуй сходи з ящиків і кинь у вогнище ящик зі своїми речами

## Суть
Sokoban у воксельному 3D: персонаж ходить по клітинах з висотами, піднімає ящики й несе їх стосом над собою (до шести), ставить їх, щоб збудувати сходинки, і лізе вгору. На кожному рівні є вогнище і ящик з «речами» персонажа — його треба довести й скинути в огонь. Керування «танкове»: уперед, назад і поворот, без кроку вбік, тож стос на голові повертається разом з тобою і чіпляється за стіни. Ядро — висота як третя вісь: щоб дістати вогнище, треба пожертвувати ящиками на сходи, а кожен ящик потрібен ще й як вантаж.

## Поле і час
- 3D-воксельна сітка: клітини мають висоту (уступи, вежі руїн), рівень — невеликий «острівець», камера ізометрична з поворотом (?).
- Хід = один крок/поворот; після ходу — гравітація для ящиків (і гравця (?)) без опори.
- Ні часу, ні випадковості, ні ворогів; повна інформація.
- Рівні — окремі пазли, повʼязані хабом-островом, який сам є пазлом із ящиками.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Персонаж | player | напрямок погляду; стос на голові 0…6 | уперед/назад на 1, поворот на місці; піднімає/ставить ящики; лізе на 1 рівень (?) |
| Ящик (дерев'яний) | object | 1×1×1 | піднімається з рівня ніг, несеться на голові, ставиться перед собою; опора/сходинка; горить у вогнищі |
| Ящик з речами | object | 1×1×1, особливий | мета рівня: потрапити у вогнище |
| Довгий ящик | object | 1×2 / 1×N | несеться й повертається разом з персонажем; при повороті може зачепити перешкоду |
| Вогнище | static | висота | ціль; ящик з речами в ньому → перемога рівня |
| Земля / камінь | static | висота клітини | опора; уступ вище 1 — стіна (?) |
| Потік (stream) | terrain | напрямок | переносить персонажа (пізні рівні) |
| Пастка | hazard | — | пізні рівні; поведінку не перевірено (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(turn_left|turn_right)` → ТО `face(player, ±90°)`; стос на голові повертається разом → ЯКЩО довгий ящик зачіпає перешкоду → ТО `block` (допустимі «легкі перекриття» на тісних поворотах — коментар розробника).
- КОЛИ `input(forward|back)` → ЯКЩО `free(next)` для персонажа **і всього стосу над ним** → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `input(forward)` → ЯКЩО клітина попереду на 1 вища і над нею вільно → ТО `custom: «залізти на сходинку»` (?).
- КОЛИ `input(pick)` / рух у ящик на рівні ніг (?) → ЯКЩО `count(stack) < 6` і над ним вільно → ТО `carry(box)` — ящик стає на верх стосу.
- КОЛИ `input(drop)` (?) → ЯКЩО клітина попереду вільна → ТО `drop(box)`, далі `fall(box)` до опори.
- КОЛИ ящик на голові — можна підняти лише ящик на рівні ніг; ящики вище не підбираються.
- КОЛИ `after(move)` → ЯКЩО `not supported(box)` → ТО `fall(box)`.
- КОЛИ `enter(box, bonfire)` → ТО `destroy(box)` (горить); ЯКЩО це ящик з речами → ТО `win`, повернення в хаб.
- КОЛИ `enter(player, stream)` → ТО `move(player, stream_dir)` (?).
- Поразки нема: глухий кут → undo до початку рівня без ліміту. Рахунку нема.

## Керування і ввід
- Клавіатура/геймпад (Xbox, PlayStation): уперед, назад, поворот ліворуч/праворуч; дія — підняти/поставити (?); Z — undo, R — рестарт (?).
- Поворот обертає і стос на голові — головна «незручність», яку критикували рецензенти й на якій тримаються пазли.

## Вікна, меню, HUD
- `main-menu` — Continue, Options, Quit (?).
- `map-window` (хаб-острів) — ходиш тим самим персонажем між входами в рівні; хаб — теж пазл з ящиками.
- `game-screen` — 3D-рівень, мінімальний HUD (підказки undo/restart).
- `pause-menu` — повернутися, рестарт, у хаб, налаштування (?).
- `settings-window` — мова (11–12), звук, графіка (у т.ч. згладжування), керування (?).
- `custom-window` — Photo Mode (додано 2022).
- Переходи: main-menu → хаб → (вхід у рівень) game-screen → (речі згоріли) хаб з новим ящиком-нагородою.

## Фічі поза полем
- `undo` ∞ до початку рівня + `restart-level`.
- `world-map` (хаб) + `level-unlock`: пройдені рівні дають ящики, які відкривають шлях далі; достатньо ~половини пазлів — `optional-levels`, можна пропустити й повернутися.
- `achievements`, `cloud-save`; `localization` (11+ мов); Photo Mode.
- DLC «Lost Memories» (3 частини: 2023, 2025).
- Кількість рівнів: 100+ (прес-кіт) / понад 200 (Wikipedia, після того як Alan Hazelden подвоїв набір).

## Варіації й родичі
- Прототип — Ludum Dare 43 (тема «sacrifices must be made», листопад 2018).
- Сімʼя Draknek: A Monster's Expedition, Stephen's Sausage Roll (танкове керування, висоти), Pipe Push Paradise (попередня гра автора).
- Sokoban → «нести замість штовхати»: тут ящик не штовхають, а піднімають і ставлять.
- **Осі варіацій:** взаємодія з ящиком — штовхати / тягнути / нести; скільки нести — 1 / стос N; рух — 4 напрямки / танковий; висота — нема / сходинки на 1 / довільні; ціль — ящик на мітку / ящик знищити.

## Цікавинки для курсу
- Воксельна сітка з висотами: «залізти на 1, впасти на будь-скільки» — 🥈 (3D-масив, перевірка опори).
- Стос ящиків на голові як стек, що рухається й колізить разом з персонажем — 🥉 (список над гравцем + перевірка всіх клітин).
- Танкове керування з обертанням вантажу — 📎; з довгими ящиками, що зачіпають стіни при повороті, — 🥈.
- Ящик як ресурс: кожен використаний на сходи — мінус вантаж; знищення у вогнищі — 🌱.
- Хаб, що сам є пазлом, і нагороди-ящики, які відкривають шлях — 🥉.
- Undo через знімки 3D-стану — 📎.

## Мапа на каталог
- Є: `move-by-input` + `keyboard-controls` ↔ крок; `gravity-fall` ↔ падіння ящиків; `impassable-cells`; `multi-cell-size` ↔ довгі ящики; `orientation-state` ↔ напрямок погляду і стосу; `floor-types` ↔ потоки; `reach-exit` ↔ вогнище як ціль (наближено); `sequential-levels` + `level-unlock` + `save-progress`; `movement-animation`; `player-camera`.
- **Нема** → пропозиції карток:
  - `+tank-controls` «Уперед/назад + поворот» · interface/input · 📎 (з Sausage Roll).
  - `+height-levels` «Висоти клітин, уступи» · entities/legality · 🥈 (з Sausage Roll).
  - `+carry-stack` «Нести стос обʼєктів над собою» · entities/state · 🥉 · слот {max: 6}.
  - `+climb-step` «Залізти на сходинку висоти 1» · entities/move · 📎 — дитина `height-levels`.
  - `+burn-goal` «Знищити цільовий обʼєкт у клітині-цілі» · game-logic/win · 🌱.
  - `+undo-redo` · game-logic/flow · 📎.
  - `+world-map` «Хаб із вузлами-рівнями» · levels/progression · 🥉.
  - `+optional-levels` «Достатньо частини рівнів для прогресу» · levels/progression · 🌱.
  - `+photo-mode` «Фоторежим: вільна камера без HUD» · interface/render · 📎.

## Пропозиції до словників
- `+trigger:input`; `+trigger:enter` — ящик у вогнище, гравець у потік.
- `+cond:free` (для всього стосу), `+cond:supported`, `+cond:count(stack, <, 6)`, `+cond:facing`.
- `+effect:move`, `+effect:face`, `+effect:fall`; `+effect:carry(a, b)` / `+effect:drop(b)` — взяти на себе / поставити (вже є `carry` з Monster's Expedition); `+effect:climb`; `+effect:destroy` — знищення обʼєкта без «смерті» (горіння).
- `+role:hazard` (пастки), `+role:terrain` (потоки).
- `+window:map-window`, `+feature:undo`, `+feature:world-map`, `+feature:photo-mode`.
- `+axis:undo` — `unlimited`.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Bonfire_Peaks) — правила руху й перенесення, ліміт 6 ящиків, «лише на рівні ніг», хаб, undo, розробка, DLC.
- [Офіційний сайт](https://bonfirepeaks.com/) · [прес-кіт](http://bonfirepeaks.com/press/) — автори, платформи, хаб з пропуском рівнів, 100+ рівнів.
- [Steam](https://store.steampowered.com/app/1147890/Bonfire_Peaks/) · [DLC Lost Memories](https://store.steampowered.com/app/2008250/Bonfire_Peaks_Lost_Memories/).
- [itch.io (Draknek)](https://draknek.itch.io/bonfire-peaks) — Photo Mode, повороти довгих ящиків.
- [Aliensrock: демо-проходження](http://www.youtube.com/watch?v=w9gzBfD5qS8) · [трейлер](http://www.youtube.com/watch?v=yGd1cP_dKQE).

## Непевне
- (?) Як саме піднімається/ставиться ящик (окрема кнопка чи рух у ящик) і куди ставиться — перед собою чи під себе.
- (?) Висота підйому персонажа (1 рівень) і чи може персонаж падати з будь-якої висоти.
- (?) Чи блокує стос ящиків рух під низькою стелею (логічно так).
- (?) Поведінка потоків і пасток (Wikipedia лише називає).
- (?) Чи горять у вогнищі звичайні ящики, чи туди можна кинути лише ящик з речами.
- (?) Кількість рівнів: 100+ (прес-кіт) vs 200+ (Wikipedia); пункти меню й клавіші.
