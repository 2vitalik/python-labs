---
title: Blast One Standing
slug: blast-one-standing
aka: [Blast 1 Standing, "The Sound of Inevitability"]
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
year: 2023
platforms: [web, PuzzleScript]
links:
  - {kind: itch, url: "https://thinkycollective.itch.io/blast-one-standing", best: true, note: "грати в браузері; мета «destroy all but one block», керування WASD/Z/R/ESC/M, історія колективної розробки"}
  - {kind: play, url: "https://html-classic.itch.zone/html/7486435/index.html", note: "сам PuzzleScript-файл гри: OBJECTS / RULES / LEVELS з dev-логом 30 авторів — джерело правил цього файла"}
  - {kind: other, url: "https://www.bontegames.com/2023/03/blast-one-standing-browser.html", note: "анонс березня 2023, коментарі гравців (38 рівнів, підказки)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=blast+one+standing+puzzlescript", note: "пошук; проходження"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, chain-reaction, connectivity-check, cell-transform, undo-unlimited, restart-level, level-select, sequential-levels, sound-effects, +last-one-standing, +typed-spread-table, +directional-spread, +initiator-becomes-wall, +link-indicator]
proposes: ["+cond:spreads_to(a, b)", "+effect:spread(from, layer)", "+ui:link-indicator", "+card:last-one-standing", "+card:typed-spread-table"]
author: opus
date: 2026-11-09
---

# Blast One Standing — штовхни блок, що торкається інших, і вся звʼязна група вибухне; лиш один блок має лишитись

## Суть
Колективна PuzzleScript-гра Thinky Collective (≈30 авторів по черзі додавали рівень чи механіку, «exquisite corpse», липень 2022 — березень 2023). Метелик-аватар ходить між блоками: ізольований блок він штовхає, як у Sokoban, а блок, що торкається сусідів, **не рухається, а запускає вибух** — хвиля шар за шаром проходить усю звʼязну групу й знищує її, а сам ініціатор стає нерухомою стіною. Мета — лишити на рівні рівно один блок. Кольори блоків змінюють, хто може запустити, передати чи прийняти вибух.

## Поле і час
- Квадратна сітка з ASCII-рівня; рамка `_` задає непрямокутні кімнати (її контур малюється автоматично).
- Шари: фон → гравець і блоки (один шар, клітина зайнята одним) → декоративні конектори між зʼєднаними сусідами → анімації вибуху.
- Хід = один крок гравця; вибух розгортається кількома `again`-тіками (по шару на тік, ≈0,07 с), потім блоки зникають; `realtime_interval` крутить лише кадри анімації. Перемога зараховується, коли анімації скінчились.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Метелик | player | — | рух 4 напрямки; вхід у блок → поштовх або запуск вибуху |
| Рамка `_` (StaticWall) | static | не рахується | непрохідна; не ловить і не передає вибух |
| Рожевий ящик `*` (Crate) | object | рахується | ізольований — штовхається; зʼєднаний — запускає вибух і стає рожевою стіною |
| Рожева стіна `#` (Wall) | static | рахується | не штовхається; вхід у неї запускає вибух; ловить і передає вибух |
| Зелений `s` (StartCrate) | object | рахується | «only start blasts»: запускає вибух; чужий вибух його не бере, лише вибух іншого зеленого |
| Блакитний `t` (ThruCrate) | object | рахується | «don't start blasts, but do continue them»: завжди лише штовхається; ловить і передає вибух |
| Сірий `w` (WallCrate) | object | рахується | як рожевий, але знищений чи ініціатор стає рамкою `_` — «leave a solid wall behind» |
| Помаранчевий ящик `c` (CrossCrate) | object | рахується, вісь H/V | «only spread a blast straight through»: передає вибух лише по осі, якою той прийшов; поштовхом запускає в обидві осі; ініціатор → помаранчева стіна |
| Помаранчева стіна `+` (CrossWall) | static | рахується, вісь | як помаранчевий ящик, але не штовхається |
| Конектор | mark | — | перемичка між блоками, які передають вибух один одному: видно, чи блок штовхнеться |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`.
- КОЛИ `contact(player, block)` → ЯКЩО `custom: «блок — джерело (не блакитний)»` and `custom: «є сусід, до якого вибух може перейти за таблицею типів»` → ТО `custom: «запустити вибух із цього блока»`; гравець лишається на місці.
- КОЛИ `contact(player, block)` → ЯКЩО `custom: «сусідів для вибуху нема»` and `custom: «блок рухомий (ящик, не стіна)»` and `free(cell_behind)` → ТО `push`, `move(player, dir)`; інакше `block`.
- КОЛИ `contact(player, blue)` → ЯКЩО `free(cell_behind)` → ТО `push` — навіть якщо блакитний зʼєднаний; інакше `block`.
- КОЛИ `tick` (again) → ЯКЩО `custom: «фронт вибуху не порожній»` → ТО `custom: «з кожної клітини фронту — на 4 сусіди, до яких дозволено: будь-хто → рожеві, сірі, блакитні, помаранчеві; зелений → ще й зелені»`; уже охоплені клітини вдруге не беруться (BFS по шарах).
- КОЛИ `custom: «вибух увійшов у помаранчевий по горизонталі (вертикалі)»` → ТО `custom: «далі він іде з нього лише по горизонталі (вертикалі)»`; ініційований поштовхом помаранчевий іде в обидві осі.
- КОЛИ `settled` (фронт порожній) → ТО `disappear` для всіх охоплених, крім ініціатора; `transform(initiator, wall)`: рожевий/зелений → `#`, помаранчевий → `+`, сірий → `_`.
- КОЛИ `destroyed(gray)` → ТО `set_cell(cell, static_wall)`, `custom: «перемалювати контур рамки»`.
- КОЛИ `settled` → ЯКЩО `count(counted_blocks, ==, 1)` and `custom: «анімацій нема»` → ТО `win`, `next_level`.
- Перемога: рівно один блок (рамка не рахується). · Поразка: нема; 0 блоків (сірий ініціатор може «зʼїсти» останній) або неприступний блок — глухий кут, лише undo/restart. · Рахунок: нема.

## Керування і ввід
- WASD або стрілки — крок / поштовх / запуск; Z — undo; R — рестарт; ESC — до вибору рівня / меню; M — без звуку. Дії-кнопки нема (`noaction`).
- Ввід блокується, поки триває вибух (again-тіки).

## Вікна, меню, HUD
- `main-menu` — титульний екран PuzzleScript (почати / продовжити) (?).
- `level-select` — список рівнів (форк PuzzleScript від pancelor, `enable_level_select`), вхід за ESC.
- `game-screen` — кімната рівня без HUD: стан читається з самого поля (конектори між блоками, кольори).
- `custom-window` — текстові картки між рівнями: «There can be only one!», «The blue ones don't start blasts, but do continue them», «The green ones can only start blasts», «The gray ones leave a solid wall behind», «The orange ones only spread a blast straight through».
- `end-screen` — фінальна картка «Just as advertised. 99% of germs killed!».
- Переходи: титул → (рівні по черзі з картками-правилами) → фінальна картка; ESC → level-select.

## Фічі поза полем
- `undo` без ліміту, `restart-level`, `level-select`, `levels-sequential` — 38 рівнів (у файлі ще закоментовані рівні й набір рівнів-«юніт-тестів» для перевірки поведінки).
- `autosave` прогресу — стандарт PuzzleScript у браузері (?).
- Відкритий код: правила, рівні й dev-лог авторів читаються в самому файлі гри.

## Варіації й родичі
- [sokoban](sokoban.md) — базове штовхання; [newtons-crates](newtons-crates.md) — поштовх у ряд передається далі; [singleton-traffic](singleton-traffic.md) — мета як стан цілого поля; [prickle](prickle.md) — звʼязна група сусідів як одна сутність; [Explodoban у increpare-sokoban-variants](../thinky/increpare-sokoban-variants.md) — вибухові ящики в Sokoban.
- Осі варіацій:
  - **що робить поштовх**: рухає (Sokoban) / рухає ізольований, підриває зʼєднаний (BOS);
  - **таблиця передачі**: хто запускає / хто передає / хто приймає вибух — окремо за кольором;
  - **напрям передачі**: усі 4 сусіди / лише по осі входу (помаранчевий);
  - **що лишає вибух**: нічого / стіну на місці ініціатора / тверду рамку (сірий);
  - **мета**: прибрати все / лишити рівно один / лишити N.

## Цікавинки для курсу
- Вибух як BFS по звʼязній групі з анімацією «шар за тік» — 📎.
- Таблиця «тип A передає вибух типу B» (несиметрична: зелений лише від зеленого) — 🥉: дані замість гілок `if`.
- Помаранчевий блок: стан «вісь входу» на клітині й повторний вхід з іншої осі — 🥉.
- Перемога «рівно один», з виключенням рамки й очікуванням анімації — 🌱.
- Конектори як візуальна підказка «цей блок не штовхнеться» — 📎 (оновлення після кожного ходу).
- Розвʼязувач: BFS по станах (позиція гравця + множина блоків) з відсіканням «0 блоків» — 🥇.
- Порівняти з PuzzleScript: переписати 30 правил-переписувань у Python-двіжок — 🥈.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ WASD/стрілки; `push-object` ↔ ізольований ящик; `impassable-cells` ↔ рамка; `chain-reaction` ↔ вибух, що йде групою; `connectivity-check` ↔ «чи зʼєднаний блок»; `cell-transform` ↔ ініціатор → стіна, сірий → рамка; `undo-unlimited` + `restart-level` ↔ Z/R; `level-select` + `sequential-levels`; `sound-effects` ↔ звуки руху, поширення, руйнування.
- **Нема** → пропозиції карток:
  - `+last-one-standing` «Перемога, коли лишився рівно один обʼєкт» · game-logic/win · 🌱.
  - `+typed-spread-table` «Поширення ефекту за таблицею типів» · entities/interact · 🥉 · слот {table}.
  - `+directional-spread` «Блок передає ефект лише по осі входу» · entities/interact · 🥉.
  - `+initiator-becomes-wall` «Ініціатор ефекту лишається стіною» · entities/state · 🌱.
  - `+link-indicator` «Перемички між зʼєднаними сусідами» · interface/render · 📎.

## Пропозиції до словників
- `+cond:spreads_to(a, b)` — тип A передає ефект (вибух, струм) сусідові типу B; таблиця типів.
- `+effect:spread(from, layer)` — ефект поширюється на сусідів шар за шаром (BFS з анімацією), на відміну від миттєвого `explode`.
- `+ui:link-indicator` — перемички між зʼєднаними блоками на полі.
- `+card:last-one-standing`, `+card:typed-spread-table`.

## Джерела
- ⭐ [itch: Blast One Standing](https://thinkycollective.itch.io/blast-one-standing) — мета, керування (WASD/стрілки, Z, R, ESC, M), PuzzleScript з level select від pancelor, колективна розробка (≈30 учасників, організатор Toombler, 22.07.2022 — 09.03.2023).
- [PuzzleScript-файл гри](https://html-classic.itch.zone/html/7486435/index.html) — OBJECTS / LEGEND (`SpreadsToFrom…`), RULES (поширення, поштовх, перетворення, перемога «exactly 1 BlockToDelete»), картки-повідомлення, 38 рівнів, dev-лог хто що додав.
- [Bonte Games, березень 2023](https://www.bontegames.com/2023/03/blast-one-standing-browser.html) — «you start a blast by pushing a block which is connected to another block», Z/R, коментарі гравців.

## Непевне
- (?) Вигляд титульного меню й чи зберігається прогрес між сесіями — стандарт PuzzleScript, у грі не перевірено.
- (?) Порядок появи механік (рожеві з 1-го, блакитні з 8-го, зелені з 14-го, сірі з 24-го, помаранчеві з 30-го рівня) — з коментаря гравця на itch; картки в коді йдуть у тому самому порядку.
