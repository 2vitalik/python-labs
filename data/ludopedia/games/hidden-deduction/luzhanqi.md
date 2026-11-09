---
title: Luzhanqi (Лучжаньці, китайські армійські шахи)
slug: luzhanqi
aka: [陆战棋, Junqi, 军棋, Land Battle Chess, Chinese Army Chess, Китайський Стратего]
family: hidden-deduction
also: [chess-abstract]
klass: figure
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: hidden
  random: none
  goal: state
year: null
platforms: [board, web, mobile]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Luzhanqi", best: true, note: "дошка 65 пунктів, дороги й залізниці, табори, штаби, склад 25 фігур, бій, бомби й міни, розкриття прапора, суддя, варіанти 2/4/6 гравців"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=luzhanqi+junqi+rules+how+to+play", note: "пошук; правила і партії"}
  - {kind: other, url: "https://en.wikipedia.org/w/index.php?search=Junqi&ns0=1", note: "пошук; Junqi / Si Guo Junqi"}
stage: v1
coverage: 65
mechanics: [piece-move-patterns, piece-capture, impassable-cells, legal-move-highlight, cell-click, drag-drop-piece, hot-seat, turn-enforcement, placement-screen, pass-device, fog-of-war, interaction-table, rule-variants, online-multiplayer, ai-opponent, last-move-highlight, game-screen, end-screen, main-menu, help-window, settings-window, lobby-window, match-setup, +hidden-rank-reveal, +rank-combat, +capture-flag, +setup-zone-placement, +rail-line-movement, +safe-camp-cells, +immobile-on-enter, +mutual-destruction-piece, +commander-death-reveals-flag, +referee-hidden-combat, +team-play-2v2]
proposes: ["+trigger:attack", "+cond:rank_cmp", "+cond:rail_path", "+cond:safe_cell", "+role:referee", "+ui:combat-result-only", "+feature:referee-mode", "+feature:allied-visible", "+card:rail-line-movement", "+card:safe-camp-cells", "+card:immobile-on-enter", "+card:mutual-destruction-piece", "+card:commander-death-reveals-flag", "+card:referee-hidden-combat", "+card:team-play-2v2"]
author: opus
date: 2026-11-09
---

# Luzhanqi — китайський Stratego на графі: залізниці, безпечні табори, бомби-камікадзе і суддя, що мовчки порівнює ранги

## Суть
Двоє гравців (третій — необовʼязковий суддя) приховано розставляють по 25 фігур і по черзі ходять однією фігурою; хід на ворожу фігуру — бій за рангом, слабша гине, рівні — обидві. Мета — захопити ворожий прапор, що стоїть в одному з двох штабів. Ядро таке саме, як у [Stratego](stratego.md) (прихований ранг + дедукція з ходів і боїв), але поле — граф із **залізницями** (хід на будь-яку відстань), **таборами** (там фігуру не можна атакувати) і **штабами** (зайшов — застиг). Нижче — передусім відмінності від Stratego.

## Поле і час
- 65 пунктів: по 30 на гравця (5 стовпців × 6 рядів) + один розділовий ряд із 2 **горами** і 3 **фронтовими переходами**.
- Пункти зʼєднані **дорогами** (крок на 1 пункт) і **залізницями** (будь-яка відстань по прямій, якщо шлях вільний). Через табори є діагональні дороги, тож суміжність — не квадратна сітка, а граф (`field: graph`).
- Типи пунктів: 23 пости, 5 таборів, 2 штаби на гравця; гори й фронти — спільні.
- Фронтові переходи — єдиний шлях на чужу половину; на них не зупиняються, а проходять крізь.
- Покроково, хід = рух однієї фігури (зокрема атака). Дві фази: прихована розстановка → гра. Ранг фігури бачить лише власник.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Маршал (司令) | piece | ранг 9, ×1 | найсильніший; його загибель змушує розкрити штаб із прапором |
| Генерал (军长) | piece | 8, ×1 | дорога: 1 крок; залізниця: по прямій без поворотів |
| Генерал-майор (师长) | piece | 7, ×2 | те саме |
| Бригадний генерал (旅长) | piece | 6, ×2 | те саме |
| Полковник (团长) | piece | 5, ×2 | те саме |
| Майор (营长) | piece | 4, ×2 | те саме |
| Капітан (连长) | piece | 3, ×3 | те саме |
| Лейтенант (排长) | piece | 2, ×3 | те саме |
| Сапер (工兵) | piece | 1, ×3 | єдиний **повертає** на залізниці (обʼїжджає кути); атакуючи міну — знищує лише її |
| Бомба (炸弹) | piece | спец., ×2, рухома | будь-який бій за її участі знищує обох; може взяти прапор; не на першому ряду при розстановці |
| Міна (地雷) | piece | спец., ×3, нерухома | атакувальник гине (крім сапера і бомби); лише в 5–6 рядах |
| Прапор (军旗) | piece | спец., ×1, нерухомий | лише в штабі; захоплення = перемога |
| Пост (兵站) | static | 23 на гравця | звичайний пункт; тут фігуру можна атакувати |
| Табір (行营) | zone | 5 на гравця | фігуру в таборі не можна атакувати; на старті порожній |
| Штаб (大本营) | zone | 2 на гравця, 6-й ряд | фігура, що зайшла або стоїть тут, більше не рухається |
| Гора (山界) | static | 2 спільні | непрохідна |
| Фронтовий перехід (前线) | static | 3 спільні | прохідний коридор на чужу половину, без зупинки |
| Залізниця | terrain | ребра графа | рух на будь-яку відстань по прямій без перешкод |

## Правила (КОЛИ → ЯКЩО → ТО)
- Розстановка: КОЛИ `input(place, piece, cell)` → ЯКЩО `cell(cell, post)` або `cell(cell, headquarters)` у своїй зоні і `free(cell)` → ТО `place(piece, cell)`; табори лишаються порожніми.
- КОЛИ `input(place, flag, cell)` → ЯКЩО `not cell(cell, headquarters)` → ТО `block`.
- КОЛИ `input(place, mine, cell)` → ЯКЩО `custom: «ряд не 5-й і не 6-й»` → ТО `block`. КОЛИ `input(place, bomb, cell)` → ЯКЩО `custom: «перший ряд»` → ТО `block`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `turn_of(side)` і `state(piece, immobile)` (міна, прапор, фігура у штабі) → ТО `block`.
- Дорога: КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «to — сусідній пункт по дорозі»` і `free(to)` → ТО `move(piece, to)`.
- Залізниця: КОЛИ `input(move, piece, to)` → ЯКЩО `custom: «to на тій самій прямій залізниці»` і `path_exists(rail, piece, to)` без фігур між → ТО `move(piece, to)`.
- Сапер: КОЛИ `input(move, engineer, to)` → ЯКЩО `path_exists(rail, engineer, to)` з поворотами → ТО `move(engineer, to)`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `cell(to, mountain)` → ТО `block`; ЯКЩО `cell(to, frontline)` → ТО `custom: «пройти крізь, не зупиняючись»`.
- КОЛИ `input(move, piece, to)` → ЯКЩО `occupied(to, enemy)` і `cell(to, camp)` → ТО `block` (у таборі атакувати не можна).
- Бій: КОЛИ `input(move, A, to)` → ЯКЩО `occupied(to, enemy D)` → ТО `custom: «порівняти ранги A і D»`:
  - ЯКЩО A або D — бомба → ТО `disappear_both`.
  - ЯКЩО D — міна → ЯКЩО A — сапер → ТО `disappear_b`, `move(A, to)`; інакше `disappear_a` (у правилі «Explosive Mines» — `disappear_both`).
  - ЯКЩО `custom: «ранг A > ранг D»` → ТО `disappear_b`, `move(A, to)`; ЯКЩО менше → ТО `disappear_a`; ЯКЩО рівні → ТО `disappear_both`.
- КОЛИ `died(marshal)` → ТО `reveal(custom: «штаб із прапором власника»)`.
- КОЛИ `enter(A, headquarters)` → ТО `set_state(A, immobile)`.
- КОЛИ `enter(A, enemy_headquarters)` → ЯКЩО `occupied(headquarters, flag)` → ТО `win`; інакше звичайний бій, а атакувальник знає, що прапор в іншому штабі.
- КОЛИ `turn_start(side)` → ЯКЩО `no_moves(side)` → ТО `lose` (?).
- Суддя: КОЛИ `custom: «бій»` → ЯКЩО `mode(referee)` → ТО `custom: «суддя таємно порівнює ранги й оголошує лише, хто зник»` — ранги не розкриваються навіть після бою.
- Перемога: захопити прапор · Поразка: втратити прапор · 4 гравці: втративши прапор, гравець знімає всі фігури, гра триває, доки живий союзник; можлива нічия за згодою, коли ніхто не може перемогти.

## Керування і ввід
- Розстановка (цифрова версія): drag фігур із лотка на пости і штаби своєї зони; заборонені пункти (табори, неправильні ряди для мін і бомб) не приймають фігуру; swap двох фігур кліком.
- Хід: клік по своїй рухомій фігурі → підсвітка досяжних пунктів (дорогою і залізницею; для сапера — з поворотами) → клік по цілі.
- Бій — той самий ввід на ворожу фігуру. Із суддею (настолка) — третя людина дивиться обидві фігури і знімає програвшу; у цифровій версії суддя — сервер.
- Hotseat без судді незручний (ранги видно), тому цифрова гра — онлайн або проти AI.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): Онлайн → `lobby-window`; Проти AI; Правила → `help-window`; Налаштування → `settings-window`.
- `match-setup` (цифрова версія): 2 / 4 гравці, «Explosive Mines», «Flying Bombs», «Flag Carrier», видимість фігур союзника.
- `placement-screen` (цифрова версія): своя половина, лоток 12 типів з лічильниками, підсвітка дозволених пунктів для мін, бомб і прапора, «Готово».
- `game-screen` (цифрова версія): граф пунктів із залізницями й таборами; свої фігури з рангами, чужі — спинки; `turn-indicator`; `last-move-highlight`; `legal-move-highlight`; `combat-result-only` (суддя показав, хто зник, без рангів); `captured-pieces`; позначка розкритого штабу з прапором.
- `end-screen` (цифрова версія): переможець, повне розкриття армій.
- Переходи: main-menu → lobby / match-setup → placement-screen → game-screen → end-screen.

## Фічі поза полем
- `custom-rules`: Flying Bombs (бомба їздить як сапер), Explosive Mines (міна гине разом з атакувальником), Flag Carrier (прапор треба донести до свого штабу; полонений носій повертає прапор), Allied Visible і All Visible (4 гравці; All Visible = повна інформація).
- `referee-mode` — бій вирішує суддя, ранги лишаються прихованими; без судді — розкриття як у Stratego.
- `online-multiplayer`, `mode-coop` (команди 2×2 у 4-гравцевій версії), `ai-opponent-levels` (?).

## Варіації й родичі
- [Stratego](stratego.md) — найближчий родич: квадратна сітка 10×10 з озерами, 40 фігур, розвідник «як тура» замість залізниць, шпигун, нерухомі бомби (тут їх роль грає міна), розкриття рангів обом.
- Gunjin Shōgi (Японія) — так само із суддею, ранги не розкриваються (див. Stratego). [Kriegspiel](dark-chess-kriegspiel.md) — шахи із суддею, що знає повну позицію.
- Si Guo Junqi (四国战棋) — дошка на 4 гравці без гір, 9 спільних центральних пунктів, вигнуті залізниці з одностороннім рухом (сапер — виняток). Six-player (六国战棋) — три команди по двоє.
- **Осі варіацій**: розкриття бою «обом / лише результат (суддя) / все відкрито»; рух «дорога / залізниця без поворотів / залізниця з поворотами (сапер)»; бомба «нерухома (Stratego) / рухома камікадзе / літаюча»; міна після невдалої атаки «лишається / гине»; мета «торкнутись прапора / донести прапор додому».
- Родичі за прихованою інформацією: [Battleship](battleship.md), [Geister](geister.md).

## Цікавинки для курсу
- Залізниця: пошук досяжних пунктів по прямій без перешкод, а для сапера — BFS по залізничному підграфу з поворотами — 🥉.
- Поле-граф замість сітки: пункти, дороги, залізниці, діагоналі через табори як дані — 📎.
- Табір як «безпечна зона» і штаб як «пастка, що заморожує» — дві прості умови з великим впливом на тактику — 🌱.
- Таблиця бою з бомбою-камікадзе і міною, яку знешкоджує лише сапер — 📎 (кандидат на `interaction-table`).
- Режим судді: сервер вирішує бій і повідомляє кожному лише те, що той має знати — 🥉 (різні проєкції стану для гравців).
- Розкриття штабу з прапором після загибелі маршала — тригер на смерть конкретної фігури — 🌱.
- 4 гравці у двох командах: вибування з гри без кінця партії — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` (дорога/залізниця/сапер) · `piece-capture` (бій) · `impassable-cells` (гори) · `legal-move-highlight` · `cell-click` + `drag-drop-piece` · `hot-seat` + `turn-enforcement` · `placement-screen` · `pass-device` · `fog-of-war` (ворожі ранги) · `interaction-table` (таблиця бою) · `rule-variants` (Flying Bombs, Explosive Mines) · `online-multiplayer` · `ai-opponent` · `last-move-highlight` · `game-screen` / `end-screen` / `main-menu` / `help-window` / `settings-window` / `lobby-window` / `match-setup`.
- **Нема** → пропозиції карток:
  - `+rail-line-movement` «Рух лінією на будь-яку відстань, з поворотами для спецфігури» · entities/move · 🥉 · слот {turns: none|any}.
  - `+safe-camp-cells` «Клітини, де фігуру не можна атакувати» · entities/legality · 🌱.
  - `+immobile-on-enter` «Клітина заморожує фігуру, що увійшла» · entities/legality · 🌱.
  - `+mutual-destruction-piece` «Фігура, що в бою гине разом із суперником» · entities/combat · 🌱.
  - `+commander-death-reveals-flag` «Загибель ключової фігури розкриває ціль» · game-logic/info · 🌱.
  - `+referee-hidden-combat` «Суддя порівнює приховані ранги, гравцям — лише результат» · game-logic/info · 🥉.
  - `+team-play-2v2` «Команди і вибування без кінця партії» · game-logic/players · 🥉.
  - `+hidden-rank-reveal`, `+rank-combat`, `+capture-flag`, `+setup-zone-placement` — як у Stratego.

## Пропозиції до словників
- `+trigger:attack` — фігура пішла на ворожу (як у Stratego: результат вирішує таблиця бою).
- `+cond:rank_cmp` — порівняння рангів із винятками (бомба, міна, сапер).
- `+cond:rail_path` — шлях залізницею по прямій без фігур (або з поворотами для сапера); `path_exists` не каже, що повертати не можна.
- `+cond:safe_cell` — фігуру в цій клітині не можна атакувати (табір).
- `+role:referee` — суддя: не фігура, а учасник, що бачить усе і вирішує бій.
- `+ui:combat-result-only` — показ результату бою без рангів.
- `+feature:referee-mode` — бій вирішує суддя/сервер, ранги приховані; `+feature:allied-visible` — союзник бачить твої ранги.

## Джерела
- ⭐ [Wikipedia: Luzhanqi](https://en.wikipedia.org/wiki/Luzhanqi) — дошка (65 пунктів, 23 пости, 5 таборів, 2 штаби, 2 гори, 3 фронти), 25 фігур і ранги, обмеження розстановки, рух дорогами й залізницями, бій, бомби й міни, розкриття штабу, суддя, варіанти 2/4/6 гравців.
- [Stratego у корпусі](stratego.md) — база для порівняння.
- YouTube: пошук «luzhanqi junqi rules how to play»; Wikipedia-пошук «Junqi».

## Непевне
- (?) Рік появи гри — у прочитаному тексті не названо; `year: null`.
- (?) Точне розташування таборів, штабів і залізничних ліній на 5×6 половині — у статті немає координат; не відтворюю.
- (?) Поразка, коли нема ходів, і нічия у двогравцевій грі — стаття їх не описує.
- (?) Як розкривають бій без судді (показують фігури одне одному чи лише результат) — стаття не уточнює.
- (?) Цифрові версії (QQ Games тощо) і їхні рівні AI — не перевірено.
- (?) Чи лишається міна після невдалої атаки — залежить від набору правил.
