---
title: Liquid War
slug: liquid-war
aka: [Liquid War 5, Liquid War 6, GNU Liquid War]
family: dig-gravity
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: hotseat
  info: full
  random: none
  goal: territory
year: 1995
platforms: [MS-DOS, Windows, Mac OS X, Linux, FreeBSD]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Liquid_War", best: true, note: "правила коротко: курсор, частинки найкоротшим шляхом, асиміляція замість смерті, перемога, AI, версії 3/5/6"}
  - {kind: other, url: "https://manpages.debian.org/testing/liquidwar/liquidwar.6.en.html", note: "повна документація LW5: правила, меню Map/Teams/Graphics/Sound/Rules/Advanced, клавіші F1–F10, формат мап, стратегія"}
  - {kind: other, url: "https://www.gnu.org/software/liquidwar6/manual/html_node/Map-rules_002exml.html", note: "LW6: усі параметри правил — атака 500, нове здоровʼя 5000, бокова атака 20 %, спроби напрямків, тор, шари, зони glue/boost/danger/medicine, профілі команд"}
  - {kind: other, url: "https://www.gnu.org/software/liquidwar6/manual/html_node/Core-algorithm.html", note: "LW6: два проходи раунду — spread (поле відстаней) і move; 100 % детермінізм без float і rand"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Liquid+War+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-auto, chase-bfs, hp-damage, impassable-cells, floor-types, wrap-edges, time-out, ai-opponent, ai-random, realtime-ai, online-multiplayer, keyboard-controls, game-pause, game-settings, settings-elements, field-scaling, main-menu, settings-window, end-screen, logic-render-split, +distance-field-flow, +swarm-cursor, +convert-on-defeat, +conserved-units, +side-attack-factor, +group-regen, +winner-help, +level-from-image, +team-profiles, +layer-depth-move, +deathmatch-respawn]
proposes: ["+cond:closer", "+effect:spread_distance", "+card:distance-field-flow", "+card:swarm-cursor", "+card:convert-on-defeat", "+card:conserved-units", "+card:side-attack-factor", "+card:group-regen", "+card:winner-help", "+card:level-from-image", "+feature:handicap-slider"]
author: opus
date: 2026-11-09
---

# Liquid War — армії-рідини течуть найкоротшим шляхом до твого курсора; переможений боєць не гине, а перефарбовується

## Суть
Гравець керує **лише курсором**; тисячі його бійців-пікселів самі течуть до курсора найкоротшим шляхом в обхід стін, тому армія виглядає як рідина. Коли бійці різних кольорів упираються одне в одного, вони **атакують**: у жертви падає здоровʼя, а на нулі вона **переходить у команду нападника** — загальна кількість бійців стала. Виграє той, хто перефарбує всіх, або в кого найбільше бійців, коли вийде час. Ядро — алгоритм «поле відстаней до курсора» (Thomas Colcombet, 1995), гра — Christian Mauduit; з версії 6 — проєкт GNU.

## Поле і час
- Мапа — растр: темні пікселі — стіни, світлі — підлога; кожен боєць займає одну клітину. Малі мапи збільшуються принаймні до 160×100 (налаштування).
- Real-time раундами: кожен раунд — два проходи: **spread** (для кожної команди поширити від курсора відстань до кожної клітини — хвиля в обхід стін) і **move** (кожен боєць робить крок у бік меншої відстані або атакує). Обмеження кадрів/с і раундів/с — у налаштуваннях.
- LW6: кілька **шарів глибини** (вісь Z) — бійці часом самі переходять між шарами; тор по X/Y (звичайний або з віддзеркаленням) і по Z.
- Вся інформація видна; «хвилі» — лише графічний ефект спотворення (F4), на логіку не впливають.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Курсор | player | швидкість 1× / 2× / 3× бійця | рухається клавішами/мишею/джойстиком; крізь стіни не проходить |
| Боєць (fighter) | piece | команда-колір; здоровʼя (LW6: нове 5000, макс. 10000) | крок до клітини, ближчої до свого курсора; упершись у ворога — атакує, у свого — регенерує |
| Стіна | static | — | непрохідна для бійців і курсора |
| Підлога | terrain | — | прохідна |
| Glue-зона (LW6) | terrain | сила 20 | щоб перетнути, треба більше кроків |
| Boost-зона (LW6) | terrain | ×3 | прискорює бійців |
| Danger-зона (LW6) | hazard | −200 HP за крок | шкодить бійцям |
| Medicine-зона (LW6) | terrain | +100 HP за крок | лікує бійців |
| Зброя (LW6) | — (властивість команди) | id 0–19, тривалість 3 с | профіль команди має зброю й альтернативну (фіксовані або випадкові); як застосовується — (?) |
| Команда | zone | колір з 12; Off / Human / Cpu | до 6 у LW5, до 10 у LW6; профіль швидкості/агресії/вразливості (LW6) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(cursor, dir)`; стіна → `block`.
- КОЛИ `tick` → ТО `custom: «spread: для кожної команди перерахувати відстань від курсора до кожної клітини підлоги»` (наближено: сусід клітини на відстані N — щонайбільше N+1).
- КОЛИ `tick` → ЯКЩО `free(dir_main)` and `custom: «клітина ближча до курсора за полем відстаней»` → ТО `move(fighter, dir_main)`; зайнято — пробує наступні напрямки, до `nb-move-tries` (LW6: 5).
- КОЛИ `blocked(fighter)` → ЯКЩО `occupied(target, enemy_fighter)` → ТО `damage(enemy_fighter, fighter_attack)` (LW6: 500); удар не в основному напрямку — `damage(× side_attack_factor)` (20 %); спроб атаки — `nb-attack-tries` (3).
- КОЛИ `hp_zero(fighter)` → ТО `set_side(fighter, attacker_team)`, `custom: «здоровʼя := fighter-new-health»` — боєць не гине, а міняє колір.
- КОЛИ `blocked(fighter)` → ЯКЩО `occupied(target, own_fighter)` → ТО `heal(fighter, fighter_defense)` (50); бік-у-бік — `heal(fighter, defense × side_defense_factor)` (20 %).
- КОЛИ `tick` → ЯКЩО `custom: «боєць не в групі»` → ТО `heal(fighter, fighter_regenerate)` (LW6: 5).
- Атака однобічна: боєць, якого атакують, може в цей самий раунд атакувати когось іншого, а не відповідати — оточений не відбивається з усіх боків.
- Світліший = здоровіший: `custom: «колір бійця темнішає зі здоровʼям»` — HUD прямо на полі.
- КОЛИ `enter(fighter, glue|boost|danger|medicine)` → ТО `speed(fighter, ÷glue | ×boost)`, `damage(fighter, danger)`, `heal(fighter, medicine)` (LW6).
- КОЛИ `edge(fighter)` → ЯКЩО `mode(polarity ≠ 0)` → ТО `wrap(fighter)` (LW6; −1 — з віддзеркаленням).
- КОЛИ `count(enemy_fighters, ==, 0)` → ТО `win` — одна команда перефарбувала всіх.
- КОЛИ `counter(time_left, ==, 0)` → ТО `custom: «перемагає команда з найбільшою кількістю бійців»`, `window(end-screen)`.
- КОЛИ `count(team_fighters, ==, 0)` → ТО `custom: «команда вибуває»`; LW6 deathmatch: ЯКЩО `mode(respawn_team)` → ТО `respawn(team, new_position)`, очки за фраги.
- Winner help: `custom: «атака множиться за розміром команди: допомога більшим / рівно / меншим (тоді партія може не скінчитись)»`.
- CPU: КОЛИ `tick` → ТО `custom: «курсор CPU — у випадкову точку ворожої армії»`; налаштування «CPU vs human»: спершу людей / будь-кого / спершу інших CPU.
- Перемога: усі бійці твого кольору або найбільше на кінець часу. · Поразка: усіх твоїх перефарбовано. · Рахунок: кількість бійців (LW6 deathmatch — фраги, чотири режими підрахунку).

## Керування і ввід
- Кожна команда — 4 клавіші (вгору/вниз/вліво/вправо), або миша, або джойстик; до 6 гравців за однією клавіатурою одночасно; чутливість миші — повзунок.
- Курсор — **єдиний ввід**: бійцями напряму не керують (непряме керування роєм). Стратегія автора: оточувати, відрізати від стін, не тримати курсор нерухомо всередині своєї армії.
- F1 — інфопанель, F2 — перемістити її; F3 — пауза (не в мережевій грі); F4 — хвилі; F5–F8 — лічильники fps і CPU; F9 — режим скріншотів; F10 — вихід без підтвердження.

## Вікна, меню, HUD
- `main-menu` (LW5): гра, Net Game, підменю налаштувань.
- `custom-window` «Map»: повзунок вибору мапи, текстура стін і підлоги (128 кнопок однотонних текстур).
- `match-setup` «Teams»: 6 зон команд — Off / Human / Cpu, колір, клавіші.
- `settings-window` з підменю: Graphics (режим, яскравість, роздільність меню й гри, viewport, хвилі), Sound (ефекти, клік, «вода» гри й меню, музика), Rules (час, швидкість, розмір армій, швидкість курсора, мінімум 160×100), Speeds, Waves, Advanced (атака, захист, нове здоровʼя, winner help, сила CPU, CPU vs human).
- `lobby-window` (Net Game): підключення до сервера / вузла (LW6 — спільноти вузлів).
- `game-screen`: поле з бійцями кольорів команд + інфопанель (F1); лічильники fps/CPU за бажанням.
- `end-screen`: результати команд за кількістю бійців (опція `-tombola` підміняє рахунки трьома випадковими числами).
- Переходи: main-menu → (Map, Teams, Options) → гра → end-screen → main-menu.

## Фічі поза полем
- `custom-rules`: усі числа бою (атака, захист, нове здоровʼя, бокові множники, спроби напрямків, розміри армій) — налаштування; LW6 — `rules.xml` для кожної мапи.
- `level-editor` неявно: мапа — будь-який 256-кольоровий BMP/LBM/PCX/TGA, текстури підвʼязуються за іменем файла; LW6 — окремі PNG-маски зон glue/boost/danger/medicine.
- `local-multiplayer` до 6 (LW5) / 10 команд (LW6); `online-multiplayer` з 5.4 (2001); `ai-opponent-levels` — повзунок сили CPU.
- `pause`; детермінізм LW6 (без float і rand) — для синхронізації мережі й повторюваності.

## Варіації й родичі
- Версії: 3.0 (1995, DOS, без мережі) → 5.x (1998–2007, Allegro, мережа з 5.4) → 6 (GNU, OpenGL, шари, зброя, deathmatch з респавном, профілі команд за кольором).
- Родичі в корпусі: [Lemmings](lemmings.md) і [Gussun Oyoyo](gussun-oyoyo.md) (непряме керування), [The Powder Toy](the-powder-toy.md) і [Sandspiel](sandspiel.md) (клітинна «рідина»), з `chess-abstract` — Ataxx і Reversi (перефарбування замість знищення), з `tower-lanes` — потоки ворогів по полю відстаней.
- **Осі варіацій**: керування роєм — «кожен юніт / курсор-магніт для всіх (тут) / роздача вмінь (Lemmings)»; смерть — «зникає / міняє сторону (тут, Reversi) / респавн»; бій — «HP і шкода / миттєве захоплення / атака лише лобова vs бокова з множником».

## Цікавинки для курсу
- Поле відстаней від курсора (BFS/хвиля в обхід стін) і крок кожної частинки «вниз по градієнту» — 🥉; на тисячі частинок щокадру і кілька команд — 🥈.
- Частинка не гине, а переходить до нападника: збереження загальної кількості як інваріант гри — 📎.
- Атака з HP, бокові множники, регенерація в групі — тактика «оточи» з'являється сама — 🥈.
- Детерміноване ядро без float і rand для мережевої гри lockstep — 🥇.
- Мапа з картинки: поріг яскравості → стіни, маски зон окремими зображеннями — 🌱.
- CPU, що «ціляє в випадкову точку ворога», — 🌱; він же — гарний базовий суперник для порівняння з розумнішим.

## Мапа на каталог
- Є: `move-auto` ↔ бійці · `chase-bfs` ↔ найкоротший шлях до курсора · `hp-damage` ↔ здоровʼя бійця · `impassable-cells` ↔ стіни · `floor-types` ↔ зони LW6 · `wrap-edges` ↔ polarity · `time-out` ↔ кінець часу · `ai-opponent` + `ai-random` + `realtime-ai` ↔ CPU · `online-multiplayer` · `keyboard-controls` · `game-pause` · `game-settings` + `settings-elements` + `settings-window` ↔ Rules/Advanced · `field-scaling` ↔ мінімум 160×100 · `main-menu` · `end-screen` · `logic-render-split` ↔ рендер читає стан, поки ядро рахує.
- **Нема** → пропозиції карток:
  - `+distance-field-flow` «Поле відстаней від цілі + крок униз по градієнту для багатьох агентів» · entities/move · 🥉.
  - `+swarm-cursor` «Курсор-магніт: увесь рій іде до нього» · interface/input · 📎.
  - `+convert-on-defeat` «HP = 0 → юніт переходить до нападника» · entities/combat · 📎 (родич `convert-adjacent`).
  - `+conserved-units` «Кількість юнітів стала; рахунок — частка» · game-logic/score · 🌱.
  - `+side-attack-factor` «Множник шкоди за напрямком удару» · entities/combat · 📎.
  - `+group-regen` «Регенерація, коли поруч свої» · entities/state · 📎.
  - `+winner-help` «Допомога більшим/меншим командам» · game-logic/difficulty · 🌱.
  - `+level-from-image` «Мапа з картинки за порогом яскравості» · levels/editor · 🌱.
  - `+team-profiles` «Профіль команди: швидкість, агресія, вразливість» · entities/state · 📎; `+layer-depth-move` (LW6 шари) · 🥈; `+deathmatch-respawn` (LW6) · 🌱.

## Пропозиції до словників
- `+cond:closer(cell, target)` — клітина ближча до цілі за полем відстаней (Liquid War; також потоки ворогів TD).
- `+effect:spread_distance(from)` — перерахувати поле відстаней від точки (прохід spread).
- `+card:distance-field-flow`, `+card:swarm-cursor`, `+card:convert-on-defeat`, `+card:conserved-units`, `+card:side-attack-factor`, `+card:group-regen`, `+card:winner-help`, `+card:level-from-image` — див. «Мапа на каталог».
- `+feature:handicap-slider` — повзунок, що підсилює більші або менші команди.

## Джерела
- ⭐ [Wikipedia: Liquid War](https://en.wikipedia.org/wiki/Liquid_War) — правила (курсор, найкоротший шлях, атака лише по напрямку до курсора, асиміляція, стала кількість), умови перемоги, 2–6 гравців, AI «випадкова точка», версії й автори.
- [Debian man: liquidwar(6)](https://manpages.debian.org/testing/liquidwar/liquidwar.6.en.html) — документація LW5: ухил і атака, здоровʼя й колір, регенерація, меню й повзунки, клавіші F1–F10, формат мап, стратегія.
- [GNU LW6: Map rules.xml](https://www.gnu.org/software/liquidwar6/manual/html_node/Map-rules_002exml.html) — усі параметри бою з типовими значеннями, тор, шари, зони, профілі команд, deathmatch.
- [GNU LW6: Core algorithm](https://www.gnu.org/software/liquidwar6/manual/html_node/Core-algorithm.html) — проходи spread і move, детермінізм.
- YouTube: пошук «Liquid War gameplay».

## Непевне
- (?) Числа (атака 500, захист 50, нове здоровʼя 5000, бокові 20 %, спроби 5/3/1, glue 20, boost 3, danger 200, medicine 100) — типові значення LW6; у LW5 ті самі ручки — повзунками без чисел.
- (?) Скільки напрямків усього розглядає боєць і в якому порядку їх перебирає — не знайдено (LW6 каже лише «скільки спроб»).
- (?) Що саме показує інфопанель (F1) і як виглядає екран результатів.
- (?) Як працює зброя LW6 (20 id) і режим Solo з профілями — у прочитаних сторінках лише параметри.
- Межа сімʼї: гравітації тут нема — «рідина» з поля відстаней, а не з падіння; у `dig-gravity` за спорідненістю з клітинними симуляціями рідин.
