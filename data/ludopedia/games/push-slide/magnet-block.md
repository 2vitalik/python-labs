---
title: Magnet Block
slug: magnet-block
aka: [Магнітний блок]
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: 3d
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2022
platforms: [PC (Windows), Linux (SteamOS)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2092660/Magnet_Block/", best: true, note: "Isaac Andrews, 11.11.2022; «push monopole magnets… Opposites attract - Identical repulse», 107 пазлів; трейлер з підписами Robotic player, Move cardinally, Scared of heights, Exit teleporter, Button, Coil and counter, Do not overload"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2092660&count=30&maxlength=6000", note: "патч-ноти v1.41–1.71 (JSON Steam News): падіння й підйом блоків, порядок розвʼязання сил, jams, котушки, кнопки, кастомні рівні до 127 сутностей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Magnet+Block+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-4dir, keyboard-controls, push-object, stick-together, gravity-fall, height-levels, impassable-cells, button-toggle, reach-exit, completion-detection, sequential-levels, level-unlock, level-select, language-picker, main-menu, settings-window, +magnet-polarity, +pressure-plate, +coil-counter, +scared-of-heights, +resolution-order, +infinite-loop-detect, +camera-orbit, +custom-levels]
proposes: ["+effect:attract", "+effect:repel", "+ui:wall-height-highlight", "+feature:custom-levels", "+card:magnet-polarity", "+card:coil-counter", "+card:scared-of-heights", "+card:resolution-order", "+card:infinite-loop-detect"]
author: opus
date: 2026-11-19
---

# Magnet Block — 3D-Sokoban з монополями: різні полюси злипаються, однакові розштовхуються, а робот має дійти до телепорта

## Суть
Робот ходить кімнатою з уступами й штовхає кубики-магніти двох полюсів (червоні й сині), щоб відкрити вихід-телепорт і зайти в нього. Магніти — монополі: різні притягуються й далі їздять гуртом, однакові відштовхуються, а без опори блоки падають. Правила прості, але кожен поштовх запускає каскад сил, тож головне — передбачити, куди «поїде» весь гурт. Вихід вмикають кнопки й котушки з лічильником; 107 пазлів «No filler».

## Поле і час
- Квадратна сітка з висотами (`field: 3d`): кімната зі стінами, уступами й нижчими смугами обабіч; вигляд згори під кутом, камеру можна рухати (діапазон розширено в 1.46) (?).
- Хід = крок робота; після кожного кроку гра розвʼязує магнітні сили й гравітацію («gravity ticked blocks»), і ланцюг реакцій буває довгим; для нього є детектор нескінченного циклу (1.42), а один із рівнів зветься «Halting Problem».
- Порядок розвʼязання одночасних сил змінювався: «north-first» → «world priority» (спершу блок, ближчий до −∞ по X, потім по Y) → «rotationally symmetric» (1.64); «jams» (два однополярні блоки під гравітацією тиснуть на третій) розвʼязуються за позицією, не за id (1.32).
- Затиснутий Shift підсвічує стіни «half-step pattern», щоб читати висоти (1.46).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Робот | player | — | рух у 4 сторони («Move cardinally»); штовхає блоки; не сходить з уступу вниз («Scared of heights»); під важким вантажем сплющується (1.49) |
| Червоний магніт | object | полюс A | монополь: притягує сині, відштовхує червоні; падає без опори |
| Синій магніт | object | полюс B | навпаки до червоного |
| Білий блок | object | без полюса | звичайний ящик Sokoban (?) |
| Вихід-телепорт | gate | неактивний (білий) / активний (зелений) | робот, що зайшов в активний, проходить рівень |
| Кнопка | switch | світло-зелена плита | поки на ній робот чи блок — вихід активний |
| Котушка з лічильником | switch | лічильник: зелені поділки / червоний хрест | реагує на магніти поруч (?); «Do not overload» — перевантаження вимикає вихід |
| Стіни, уступи, нижні смуги | static | висота | обмежують рух; блоки з уступу падають, робот — ні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` і `supported(next_cell)` → ТО `move(robot, dir)`; інакше `block` — робот не сходить з краю вниз (трейлер «SCARED OF HEIGHTS»).
- КОЛИ `contact(robot, block)` → ЯКЩО `free(cell_behind)` → ТО `push` — зсувається весь звʼязаний магнітами гурт (трейлер: L-трійка синій–червоний–синій їде цілою).
- КОЛИ `adjacent(magnet, magnet)` → ЯКЩО `not same(a, b, pole)` → ТО `attach(a, b)` — різні полюси притягуються й далі рухаються разом.
- КОЛИ `in_range(magnet, magnet, 2)` → ЯКЩО `same(a, b, pole)` → ТО `custom: «відштовхнути інший блок на клітину далі»` — трейлер: синій, підсунутий до синьо-червоної пари, відганяє її, не торкаючись (?).
- КОЛИ `turn_end` → ЯКЩО `not supported(block)` → ТО `fall(block)` — падаючий блок спершу відштовхується по осі, якою його штовхнули востаннє (1.63); блоки, що падають чи піднімаються, завжди зсуваються блоками, які рухаються вбік (1.71).
- КОЛИ `enter(robot|block, button)` → ТО `set_state(exit, active)` (трейлер «BLOCKS: BUTTON»).
- КОЛИ `leave(robot|block, button)` → ТО `clear_state(exit, active)` — кнопка діє, лише поки на ній щось стоїть.
- КОЛИ `custom: «лічильник котушки в зеленій зоні»` → ТО `set_state(exit, active)` (трейлер «COIL AND COUNTER») (?).
- КОЛИ `custom: «перевантаження — червоний хрест»` → ТО `clear_state(exit, active)` (трейлер «DO NOT OVERLOAD») (?).
- КОЛИ `enter(robot, exit)` → ЯКЩО `state(exit, active)` → ТО `win`, `next_level` (трейлер «EXIT TO SOLVE»).
- Перемога: робот зайшов в активний (зелений) телепорт. · Поразка: нема; глухий кут → рестарт чи undo (?). · Рахунок: нема.

## Керування і ввід
- Клавіатура (з 1.57 — і не-QWERTY розкладки) або геймпад (повна підтримка, DualShock / DualSense, Steam Input); чотири напрямки руху робота.
- Shift — підсвітка стін; керування камерою — (?).
- Undo й рестарт у джерелах не згадано (?).

## Вікна, меню, HUD
- `main-menu` (трейлер, v0.1): Play > · Options · Exit, обертовий синій куб.
- `level-select` (Play >): рівні мають назви; лічильник рівнів показує лише вже відкриті (1.32); вигляд — (?).
- `settings-window` (Options): мова (EN, FR, JA, KO, RU, ZH), обмежувач кадрів / VSync (1.70) (?).
- `game-screen`: кімната з роботом, блоками й виходом; HUD у трейлері не видно.
- `credits-window` — титри після всіх пазлів (1.33).
- Переходи: main-menu → level-select → game-screen → (вихід) наступний рівень → … → титри.

## Фічі поза полем
- `levels-sequential` + `level-unlock`: рівні відкриваються поступово (баг 1.58 «Tertiary unlocking many more levels than it should»); у трейлері 2022 — «over 79 levels», у релізі — 107.
- Кастомні рівні: ліміт 127 сутностей, кілька виходів-телепортів (1.52), котушки в 3D (1.49); як їх створюють і чи є редактор — (?).
- Переклади від гравців (французька, китайська, японська, корейська, російська); демо — окрема сторінка Steam (2023).
- Автор 51 патчем правив рівні: прибирав «unintended solutions», «зменшував ентропію», замінював рівні.

## Варіації й родичі
- [kye](kye.md) — магніти, що тягнуть предмети; [magnets](../pencil-logic/magnets.md) — паперовий пазл про полюси (однакові не стикаються); [sokobond](../thinky/sokobond.md) — зчеплення при контакті.
- [kiki-the-nano-bot](../grid-platformer/kiki-the-nano-bot.md) — 3D-Sokoban з падінням блоків; [pipe-push-paradise](pipe-push-paradise.md) — магнітні труби зчіплюються кінцями.
- Осі варіацій:
  - **сила між блоками**: нема (Sokoban) / злипання при контакті (Sokobond) / різні притягуються, однакові відштовхуються (тут);
  - **дальність сили**: лише сусіди / через клітину (тут, ?);
  - **умова виходу**: просто дійти / при натиснутих кнопках / при лічильнику котушки в межах (тут — усе);
  - **порядок розвʼязання одночасних сил**: напрямковий пріоритет («north-first») / координатний / симетричний до поворотів поля.

## Цікавинки для курсу
- Монополі двох полюсів: притягання → гурт, що рухається разом; відштовхування → зсув іншого блока — 🥈 (каскад сил після кожного ходу).
- Гравітація разом із магнітними силами в 3D: падіння, підйом, «відскок» по осі останнього поштовху — 🥇.
- Детермінований порядок розвʼязання одночасних сил, симетричний до поворотів поля — 🥇 (класична пастка «north-first»).
- Детектор нескінченного циклу реакцій через повтор стану — 🥈.
- Кнопка-плита, що тримає вихід активним, поки натиснута — 🌱.
- Робот, що не сходить з уступу («боїться висоти»), при блоках, що падають — 📎.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ «Move cardinally», клавіатура й геймпад; `push-object`; `stick-together` ↔ притягнуті магніти їздять гуртом; `gravity-fall` ↔ падіння блоків; `height-levels` ↔ уступи; `impassable-cells` ↔ стіни; `button-toggle` ↔ кнопка → вихід; `reach-exit` ↔ телепорт; `completion-detection`; `sequential-levels` + `level-unlock` + `level-select`; `language-picker`; `main-menu`, `settings-window`.
- **Нема** → пропозиції карток:
  - `+magnet-polarity` «Блоки-монополі: різні полюси притягуються, однакові відштовхуються» · entities/interact · 🥈 · слоти {poles: 2, range}.
  - `+coil-counter` «Котушка з лічильником: умова виходу, яку можна перевантажити» · entities/interact · 🥉 (?).
  - `+scared-of-heights` «Аватар не сходить з уступу вниз» · entities/legality · 🌱.
  - `+resolution-order` «Порядок розвʼязання одночасних сил і рухів (пріоритет, симетрія)» · game-logic/rules · 🥇.
  - `+infinite-loop-detect` «Виявлення нескінченного циклу реакцій» · game-logic/constraints · 🥈.
  - `+pressure-plate`, `+camera-orbit` — підтверджую; `+custom-levels` — свої рівні гравців.

## Пропозиції до словників
- `+effect:attract` / `+effect:repel` — притягнути / відштовхнути обʼєкт (уже пропоновані іншими іграми); зараз — `attach` і `custom`.
- `+ui:wall-height-highlight` — підсвітка стін за висотою на затиснуту клавішу.
- `+feature:custom-levels` — рівні гравців поза основним набором.
- `+card:magnet-polarity`, `+card:coil-counter`, `+card:scared-of-heights`, `+card:resolution-order`, `+card:infinite-loop-detect`.

## Джерела
- ⭐ [Steam: Magnet Block](https://store.steampowered.com/app/2092660/Magnet_Block/) — опис (монополі, «Opposites attract - Identical repulse», телепорт-вихід, 107 пазлів), мови, контролери; трейлер з підписами (Magnetic blocks, Robotic player, Move cardinally, Scared of heights, Push the magnet blocks, Exit teleporter, Button, Coil and counter, Do not overload, Exit to solve, Over 79 levels) і 5 скріншотів.
- [Steam News (JSON)](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2092660&count=30&maxlength=6000) — патч-ноти v1.41–1.71: правила падіння й підйому, порядок розвʼязання, детектор циклів, кастомні рівні, котушки, кнопки, Shift-підсвітка, камера; старіші v1.20–1.40 (тим самим API з `enddate`) — jams, титри, лічильник відкритих рівнів.
- YouTube: пошук «Magnet Block gameplay».

## Непевне
- (?) Дальність сил: чи притягання діє лише між сусідами, а відштовхування — через одну клітину, як здається з трейлера; що буває, коли відштовхнутому нема куди зсунутися.
- (?) Що саме рахує котушка (кількість магнітів поруч, проходи магніту крізь котушку) і коли лічильник «перевантажується».
- (?) Чи білий блок — просто ящик без полюса; чи бувають блоки, що «піднімаються» самі (патч 1.71 каже «falling/rising blocks»).
- (?) Чи кілька кнопок мають бути натиснуті всі одразу (на скріншотах групи світло-зелених плит).
- (?) Undo, рестарт, керування камерою, редактор кастомних рівнів — у відкритих джерелах не описано.
