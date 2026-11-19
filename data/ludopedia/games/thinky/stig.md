---
title: Stig
slug: stig
aka: []
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
year: 2024
platforms: [Windows, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2834830/", best: true, note: "мета — пройти кольорові клітини в порядку заданого візерунка; 100+ рівнів, undo/рестарт; доступність: візерунок на кожному кольорі, контраст, яскравість, переназначення"}
  - {kind: steam, url: "https://store.steampowered.com/app/2910530", note: "безкоштовне демо: 15 рівнів, 07.04.2024, частина механік"}
  - {kind: youtube, url: "https://www.youtube.com/watch?v=uQVI9IrP7sc", note: "трейлер (ID з новини про реліз у Steam)"}
  - {kind: other, url: "https://steamcommunity.com/app/2834830/reviews/?browsefilter=toprated&l=english", note: "відгуки з переліком механік: кулі-фарби, куби й диски, реверс, крихкі клітини, стрілки, кілька аватарів; 110 рівнів, 3 секретні"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2834830", note: "новини: пропуск рівня з паузи, профілі збереження, анімація невдалого поштовху, бандл із BOND"}
stage: v1
coverage: 45
mechanics: [move-4dir, move-by-input, keyboard-controls, controls-remap, push-object, inertia-slide, floor-types, party-switch, undo-redo, restart-level, skip-level, level-unlock, save-multi-slot, pause-menu, achievements-window, game-settings, volume-control, +color-sequence-walk, +paint-cell, +shape-toggle-tile, +sequence-reverse-tile, +crumbling-floor, +branching-campaign, +colorblind-palette, +secret-area]
proposes: ["+cond:sequence_match", "+effect:append_sequence", "+ui:sequence-bar", "+card:color-sequence-walk", "+card:shape-toggle-tile", "+card:sequence-reverse-tile"]
author: opus
date: 2026-11-19
---

# Stig — пройди кольорові клітини в порядку візерунка вгорі екрана; кулі-фарби, куби й диски міняють саме поле

## Суть
Покроковий сокобан-подібний пазл про «шлях крізь кольори» (Miriam and Lage, BergBerg Games, 2024): гравець ходить сіткою кольорових клітин, і кожен перехід на клітину іншого кольору записується в послідовність, яку треба звести з візерунком угорі екрана. Зібрана послідовність відкриває вихід рівня (відгуки). Далі гра щокілька рівнів додає механіку: кулі-фарби, що лишають кольоровий слід, обʼєкти-куби (крок) і диски (котяться), клітини реверсу порядку, крихкі клітини, стрілки, кілька аватарів. Steam: «100+ unique levels», відгук: 110 рівнів, 4–8 годин.

## Поле і час
- Квадратна сітка, вид згори; клітини — білі, сірі, «колір гравця» та інші кольори (відгук); зразок-послідовність — рядок кольорів угорі екрана.
- Покроково, без таймерів: «не вимагає швидких реакцій», один ввід за раз.
- Мапа рівнів — центральний шлях із короткими бічними гілками; гілки складніші й необовʼязкові, для просування регіоном треба пройти достатньо рівнів; 3 секретні рівні (відгуки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | свій колір; форма куб / куля | рух 4 напрямки; перехід на клітину іншого кольору додає колір до послідовності |
| Кольорова клітина | terrain | колір | вхід на неї з іншого кольору записується |
| Біла / сіра клітина | terrain | — | окремі «кольори» базової механіки (?) |
| Куля-фарба | object | колір | штовхається; фарбує клітини, якими проходить |
| Куб | object | — | штовхається на 1 клітину |
| Диск (куля) | object | — | після поштовху котиться до упору |
| Обʼєкти кольору гравця | object | фіолетові кулі й куби | «того ж кольору, що ти» — роль (?) |
| Клітина форми | terrain | — | перемикає обʼєкт або гравця між кубом і кулею |
| Клітина реверсу | terrain | — | далі послідовність набирається у зворотному порядку |
| Клітина-хамелеон | terrain | — | міняє колір, коли на неї стають |
| Крихка клітина | terrain | 1 прохід | після проходу пройти вже не можна (?) |
| Стрілка | terrain | напрям | примусовий рух |
| Клітина аватара | switch | — | керування переходить до іншого аватара |
| Вихід | gate | закрито / відкрито | відкривається, коли послідовність зібрано |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`.
- КОЛИ `enter(player, color_tile)` → ЯКЩО `not same(color_tile, prev_tile, color)` → ТО `custom: «колір додається до набраної послідовності й звіряється із зразком»`.
- КОЛИ `custom: «набрана послідовність збіглась із зразком»` → ТО `unlock(exit)`.
- КОЛИ `enter(player, exit)` → ЯКЩО `state(exit, open)` → ТО `win`, `next_level`.
- КОЛИ `contact(player, cube)` → ЯКЩО `free(cell_behind)` → ТО `push(cube)`; інакше `block`, `animate(bump)` (оновлення 15.12.2024).
- КОЛИ `contact(player, ball)` → ЯКЩО `free(cell_behind)` → ТО `slide(ball, dir)` — котиться до упору.
- КОЛИ `contact(player, paint_ball)` → ЯКЩО `free(cell_behind)` → ТО `push(paint_ball)`, `paint(passed_cells, ball_color)`.
- КОЛИ `enter(player, shape_tile)` → ТО `transform(player, ball)` або назад у куб; так само для обʼєкта, що заїхав на клітину.
- КОЛИ `enter(player, reverse_tile)` → ТО `custom: «напрям набору послідовності змінюється на зворотний»`.
- КОЛИ `enter(player, chameleon_tile)` → ТО `set_cell(chameleon_tile, next_color)`.
- КОЛИ `leave(player, fragile_tile)` → ТО `set_cell(fragile_tile, hole)` (?).
- КОЛИ `enter(player, arrow_tile)` → ТО `move(player, arrow_dir)`.
- КОЛИ `enter(player, avatar_tile)` → ТО `custom: «керування переходить до іншого аватара»`.
- КОЛИ `input(dir)` → ЯКЩО `custom: «наступний елемент зразка вимагає напрям, напр. «вгору»»` → ТО `custom: «зараховується лише хід у цьому напрямку»` (?).
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(restart)` → ТО `restart`.
- Перемога: послідовність зібрано, вихід відкрито й досягнуто. · Поразки нема (undo / рестарт). · Рахунку нема.

## Керування і ввід
- Лише чотири напрямки + undo; окремо рестарт і пауза; клавіатура або геймпад (повна підтримка), переназначення клавіш.
- Гра «не вимагає одночасних натискань» і читання (крім кількох навчальних текстів і меню).

## Вікна, меню, HUD
- `main-menu` з профілями збереження: кілька профілів і кнопка скидання прогресу (оновлення 01.12.2024).
- `map-window`: мапа-стежка — центральний шлях із бічними гілками, регіони, секретні рівні (відгуки).
- `game-screen`: поле + зразок кольорів угорі (`sequence-bar`); як показано прогрес набору — (?).
- `pause-menu`: пропуск рівня (пропущений не зараховується й не дає досягнень), вихід, налаштування (?).
- `settings-window`: переназначення клавіатури й геймпада, висококонтрастні кольори, візерунок поверх кожного кольору (зокрема для повної колірної сліпоти), яскравість, гучність ефектів і музики.
- `achievements-window` (Steam).
- Переходи: меню → мапа → рівень → (вихід) мапа; пауза → пропуск → мапа.

## Фічі поза полем
- `undo`, `restart-level`; `skip-level` із паузи без зарахування (01.12 і 15.12.2024).
- `save-slots`: кілька профілів, скидання прогресу; Steam Cloud, Family Sharing.
- `colorblind-palette` (візерунок на кожному кольорі), `high-contrast`, яскравість, `volume-sliders`, `remap-controls`, `gamepad-support`.
- `achievements`; локалізація EN, SV, традиційна китайська; безкоштовне демо на 15 рівнів.

## Варіації й родичі
- Бандл «Stig & BOND — Colorful Cube Conundrums» (02.2025) із [BOND](../push-slide/bond.md) — 3D-сокобаном Gustav Almström.
- Родичі: [Alephant](alephant.md) — відтворити послідовність; [Colorboration](../push-slide/colorboration.md) — кольорові шляхи, що заважають одне одному; [Sokoban](../push-slide/sokoban.md) — поштовх як основа.
- **Осі варіацій**: що записується — колір клітини / лише перехід між різними кольорами (Stig) · порядок набору — прямий / зворотний (клітина реверсу) · елемент зразка — колір / колір + напрям ходу · хто міняє поле — гравець / кулі-фарби / клітини-хамелеони · форма — куб (крок) / куля (котиться до упору).

## Цікавинки для курсу
- Запис послідовності переходів між кольорами і звірка з префіксом зразка — 📎.
- Куля-фарба, що перефарбовує клітини на своєму шляху, — 📎.
- Перемикання форми куб ↔ куля (крок проти котіння до упору) — 🥉.
- Клітина реверсу порядку й обмеження «наступний хід — угору» в зразку — 🥉.
- Мапа-стежка з гілками, регіони відкриваються після N рівнів — 📎.
- Візерунок поверх кожного кольору для дальтоніків — 🌱 (мало коду, багато користі).
- Розвʼязувач BFS зі станом «позиція + індекс у зразку + кольори поля + обʼєкти» — 🥈.

## Мапа на каталог
- Є: `move-4dir` · `move-by-input` · `keyboard-controls` · `controls-remap`; `push-object` ↔ куби й кулі-фарби; `inertia-slide` ↔ котіння диска; `floor-types` ↔ стрілки, хамелеони, крихкі клітини; `party-switch` ↔ кілька аватарів; `undo-redo` · `restart-level`; `skip-level`; `level-unlock` ↔ регіони; `save-multi-slot` ↔ профілі; `pause-menu`; `achievements-window`; `game-settings` · `volume-control`.
- **Нема** → пропозиції карток:
  - `+color-sequence-walk` «Пройти кольори в порядку зразка» · game-logic/win · 📎 · слот {record: tile | transition}.
  - `+shape-toggle-tile` «Клітина міняє форму обʼєкта: крок ↔ котіння» · entities/state · 🥉.
  - `+sequence-reverse-tile` «Клітина реверсує порядок набору» · game-logic/constraints · 📎.
  - Уже в корпусі: `+paint-cell` (куля-фарба), `+crumbling-floor` (крихкі клітини), `+branching-campaign` (центральний шлях із гілками), `+colorblind-palette` (візерунки на кольорах), `+secret-area` (3 секретні рівні).

## Пропозиції до словників
- `+cond:sequence_match` — набрана послідовність збігається з (префіксом) зразка (уже пропоновано в alephant.md).
- `+effect:append_sequence` — додати колір / дію до набраної послідовності.
- `+ui:sequence-bar` — зразок послідовності вгорі екрана з позначкою набраного.
- `+card:color-sequence-walk`, `+card:shape-toggle-tile`, `+card:sequence-reverse-tile` — див. вище.

## Джерела
- ⭐ [Steam: Stig](https://store.steampowered.com/app/2834830/) — опис і мета, «100+ unique levels», 4 напрямки + undo + рестарт, розділ доступності, теги, дата 20.11.2024, мови.
- [Steam: Stig Demo](https://store.steampowered.com/app/2910530) — 15 рівнів, «some (but far from all) of the mechanics».
- [Відгуки Steam](https://steamcommunity.com/app/2834830/reviews/?browsefilter=toprated&l=english) — sdumitriu: запис переходів між кольорами, кулі-фарби, фіолетові кулі й куби, кілька аватарів, реверс, хамелеони, куб ↔ куля, крихкі клітини, стрілки, обмеження «next move must be up», 110 рівнів, 3 секретні; Jonman: «sequence of colors at the top of the screen»; ramtha666: «unlock the level exit».
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2834830) — реліз (трейлер), оновлення 01.12 і 15.12.2024, бандл із BOND.
- [Трейлер](https://www.youtube.com/watch?v=uQVI9IrP7sc) — не дивився.

## Непевне
- (?) Як саме записується послідовність: «перехід з кольору на колір» (sdumitriu) чи «торкнутись кольорів у правильному порядку» (ramtha666); що роблять білі й сірі клітини.
- (?) Що буває при хибному кольорі — скидання набору, блок ходу чи просто не зараховується.
- (?) Вихід — окрема клітина чи рівень завершується одразу після набору («unlock the level exit» — лише з відгуку).
- (?) Роль обʼєктів «кольору гравця»; чи крихка клітина після проходу стає дірою чи стіною; чи гравець-куля котиться до упору.
- (?) 110 рівнів, 3 секретні, 4–8 год — з одного відгуку; Steam каже «100+»; глибина undo невідома.
