---
title: Langrisser
slug: langrisser
aka: [Warsong, ラングリッサー, "Langrisser: Hikari no Matsuei", "Langrisser: The Descendants of Light", Lungrisser, "Langrisser I & II"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1991
platforms: [Genesis, PC Engine CD, Saturn, PlayStation, Windows, PS4, Switch, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Langrisser", best: true, note: "серія: командири й наймані загони, радіус командування з бонусом, +3 HP біля командира, трикутник родів військ, хід «кожен юніт раз»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Warsong_(video_game)", note: "перша гра: до 8 загонів одного типу на героя, клас обмежує найм, гроші за вцілілі загони, промоція класу, смерть героя назавжди"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Langrisser", note: "рімейк Langrisser I & II (2019/2020)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Langrisser+Warsong+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, legal-move-highlight, threat-range, floor-types, unit-xp-skills, inventory-items, round-currency, shop-between-levels, ai-opponent, destroy-all-enemies, player-death, permadeath, sequential-levels, placement-screen, save-game, turn-enforcement, +commander-aura, +hired-squads, +squad-hp-strength, +troop-type-triangle, +terrain-bonus, +class-promotion, +leader-death-lose, +commander-heal-adjacent]
proposes: ["+cond:in_aura", "+cond:affinity", "+effect:hire", "+effect:counterattack", "+ui:aura-range", "+window:hire-screen", "+window:class-change", "+role:commander"]
author: opus
date: 2026-11-09
---

# Langrisser — командир і його наймані загони: тримай військо в радіусі ватажка, бо там воно сильніше

## Суть
Гравець веде кількох **командирів**-героїв; перед кожним сценарієм кожен наймає до восьми загонів одного дозволеного класом типу (піхота, кіннота, списники, лучники, летуни…). Загони сильні лише **в радіусі командування** свого ватажка — там у них бонус атаки й захисту, а впритул до командира вони ще й лікуються. Бій — фази сторін: усі мої юніти по разу, потім ворог; одночасно на полі може бути понад 30 юнітів. Ціль сценарію — зазвичай убити ворожого командира або всіх ворогів; смерть головного героя — кінець гри.

## Поле і час
- Поле — квадратна сітка великих мап з тереном (рівнина, ліс, гори, вода, мости, фортеці); терен дає бонус захисту й уповільнює рух (?).
- Час — покроковий, фазами: у фазу гравця кожен юніт може піти раз у будь-якому порядку, потім фаза ворога (і союзних NPC). У Langrisser IV–V з'являється годинник і хід за спритністю.
- Видимість повна. Випадковість — у розрахунку шкоди (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Командир (герой) | piece | HP, AT, DF, MP, Move, клас, рівень, бонус командування (+A/+D), радіус | рух, атака, магія; наймає загони свого класу; підсилює загони в радіусі |
| Найманий загін | ally | HP = кількість солдатів (10 на загін), AT/DF, тип | ходить сам, сильніший у радіусі командира; гине разом зі своїм ватажком (?) |
| Піхота (soldiers) | ally | — | сильна проти списників, слабка проти кінноти |
| Кіннота | ally | більший рух | сильна проти піхоти, слабка проти списників |
| Списники | ally | — | сильні проти кінноти |
| Летуни (грифони) | ally | ігнорують терен (?) | сильні проти піхоти, слабкі проти лучників; наймаються лише певними класами |
| Лучники | ally | дальність | бʼють на відстані; сильні проти летунів |
| Морські загони | ally | — | перевага, коли атакують з води |
| Святі / демонічні загони | ally / enemy | — | святі сильні проти демонів |
| Ворожий командир | boss | як у героя | частіше — ціль сценарію; його загони без нього слабшають / зникають (?) |
| Ворожий загін | enemy | як найманий | AI іде на найближчу ціль |
| Терен (ліс, гори, вода) | terrain | бонус DF, ціна руху | рівнина швидка, ліс і гори захищають |
| Предмет | pickup | — | спорядження командира: стати лише йому, не загонам |

## Правила (КОЛИ → ЯКЩО → ТО)
- Найм: КОЛИ `level_start` → ТО `window(hire-screen)`; КОЛИ `input(hire, commander, type)` → ЯКЩО `custom: «тип дозволено класом»` and `count(squads_of(commander), <, 8)` and `has(player, cash)` → ТО `currency(−price)`, `custom: «загін закріплено за командиром»`.
- Розстановка: КОЛИ `level_start` → ТО `custom: «гравець ставить командирів і їхні загони на стартові клітини, обирає формацію»`.
- КОЛИ `phase_start(player)` → ТО `custom: «кожен юніт гравця може піти один раз»`; КОЛИ `turn_end(player)` → ТО `end_turn` — фаза ворога і союзних NPC.
- Аура: КОЛИ `custom: «бій загону»` → ЯКЩО `in_range(commander, squad, radius)` → ТО `custom: «+A до атаки і +D до захисту загону від командира»`; поза радіусом — без бонусу.
- КОЛИ `phase_start(player)` → ЯКЩО `adjacent(squad, commander)` → ТО `heal(squad, 3)`.
- КОЛИ `input(treat, unit)` → ТО `heal(unit, 3)`, `end_turn` (у пізніших версіях Heal: +3 HP і +2 MP).
- КОЛИ `input(attack, a, t)` → ЯКЩО `adjacent(a, t)` або `in_range(a, t, range)` → ТО `custom: «бій: атакувальник і захисник обмінюються ударами»`; `damage(t, n)`, `damage(a, m)` (?).
- Шкода: `custom: «більше солдатів (HP) — сильніший удар; модифікатори: трикутник родів, аура, терен»` (?).
- Трикутник: КОЛИ `input(attack, a, t)` → ЯКЩО `custom: «тип A сильний проти типу T»` → ТО `custom: «бонус до шкоди й захисту»`.
- Терен: КОЛИ `input(attack, a, t)` → ЯКЩО `cell(under_t, forest|mountain|fort)` → ТО `custom: «бонус захисту T за тереном»`.
- КОЛИ `input(attack, sea_unit, t)` → ЯКЩО `cell(under_a, water)` → ТО `custom: «бонус морському загону»`.
- КОЛИ `input(magic, commander, target)` → ЯКЩО `counter(MP, >=, cost)` → ТО `counter(MP, −cost)`, `damage(area, n)` або `heal` / підсилення.
- КОЛИ `hp_zero(squad)` → ТО `disappear(squad)`, `custom: «досвід — командиру-вбивці»` (?).
- КОЛИ `hp_zero(commander)` → ТО `disappear(commander)`, `custom: «його загони теж зникають»` (?); ЯКЩО `custom: «це ворожий головний командир»` → ТО `win` (у сценаріях «убий ватажка»).
- КОЛИ `hp_zero(main_hero)` → ТО `lose`, `game_over`.
- КОЛИ `level_end` → ТО `currency(+n)` `custom: «за кожен вцілілий загін»`; `custom: «командир з досвідом підвищує рівень»`.
- Промоція: КОЛИ `counter(level, >=, need)` → ТО `choose(classes)` → `transform(commander, new_class)` — нові заклинання, типи загонів, більший радіус (?).
- Перемога: `destroyed(enemy_boss)` / `all_gone(enemy)` / захист персонажа N ходів. Поразка: смерть головного героя або захищуваного.

## Керування і ввід
- Курсор по клітинах (геймпад): вибрати юніта → підсвічена зона руху → клітина → меню: Attack, Magic, Treat/Heal, Stand by.
- Вибір командира показує його радіус командування — підсвічену (у Langrisser II — блимаючу) область.
- Перед боєм: меню найму загонів для кожного командира, вибір предметів, розстановка.
- Кнопка завершення фази; огляд статів будь-якого юніта.

## Вікна, меню, HUD
- `main-menu`: New Game, Load, Options.
- `hire-screen` — найм: командири, дозволені типи загонів, ціни, лічильник до 8, баланс грошей; предмети (`shop-window`).
- `placement-screen` — розстановка, формації.
- `game-screen`: мапа; `legal-move-highlight`; `aura-range` — радіус командування; `threat-range` (у рімейках — небезпечні клітини); панель юніта з HP (кількістю солдатів), AT/DF з бонусом; `turn-counter`; `objective-text` умов перемоги.
- Бойова сцена — анімація зіткнення загонів (`custom-window`).
- `class-change` — дерево промоції класів.
- `end-screen` — підсумок сценарію, гроші; `save-slots` між сценаріями.

## Фічі поза полем
- Кампанія сценаріїв; гроші переходять між сценаріями; командири набирають рівні й міняють клас.
- Перманентна смерть героїв (`permadeath`), смерть головного героя — кінець гри.
- Рімейк Langrisser I & II (2019): вибір класів-гілок, режими складності (?).
- Пізніші частини: сюжетні гілки, годинник ходів за спритністю (IV–V), мобільна Langrisser Mobile.

## Варіації й родичі
- Серія: Langrisser II (1994), III (3D-ракурс), IV–V (годинник), Re:Incarnation (3DS, бої 10 на 10), Mobile.
- Родичі: Fire Emblem (фази сторін, промоція класів — [fire-emblem](fire-emblem.md)), Advance Wars (HP = кількість, менше — слабша атака — [advance-wars](advance-wars.md)), Battle for Wesnoth (лідер, найм у замку — [battle-for-wesnoth](battle-for-wesnoth.md)), Total War (командирська аура, не клітинна).
- Осі варіацій:
  - **аура лідера**: нема / пасивний радіус командира (Langrisser) / суміжна підтримка (FE supports) / лідерство сусідам (Wesnoth Leadership);
  - **армія**: окремі герої (FE) / герой + наймані загони з HP = солдати (Langrisser) / найм у замку на мапі (Wesnoth);
  - **смерть ватажка**: гине лише він / розпадається його загін / гра програна.

## Цікавинки для курсу
- Аура командира: бонус лише в радіусі (манхетенська відстань) — 📎.
- Лікування +3 HP загонам, що стоять поруч з командиром на початку фази — 🌱.
- Найм до N загонів одного типу за гроші з обмеженням класом — 📎 (вікно найму + бюджет).
- Трикутник родів військ — 🌱 (таблиця модифікаторів).
- HP загону = кількість солдатів, шкода залежить від HP — 🌱.
- Повʼязані життя: загони зникають зі смертю ватажка — 🌱 (?).

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ лучники · `legal-move-highlight` · `threat-range` · `floor-types` ↔ терен · `unit-xp-skills` ↔ рівні командирів · `inventory-items` ↔ предмети командира · `round-currency` + `shop-between-levels` ↔ гроші й найм · `ai-opponent` · `destroy-all-enemies` · `player-death` + `permadeath` · `sequential-levels` ↔ сценарії · `placement-screen` · `save-game` · `turn-enforcement` ↔ кожен юніт раз за фазу.
- **Нема** → пропозиції карток:
  - `+commander-aura` «Бонус загонам у радіусі командира» · entities/combat · 📎 · слот {radius, atk, def}.
  - `+hired-squads` «Найм загонів, закріплених за героєм» · progression · 📎 · слот {max: 8}.
  - `+squad-hp-strength` «HP загону = сила атаки» · entities/combat · 🌱 (родич `+strength-is-hp` з Banner Saga).
  - `+troop-type-triangle` «Трикутник родів військ» · entities/combat · 🌱 (родич `+weapon-triangle` з FE).
  - `+terrain-bonus` (з FE) — захист від терену.
  - `+class-promotion` (з FE) — промоція з вибором гілки.
  - `+leader-death-lose` «Смерть головного героя = поразка» · game-logic/end · 🌱.
  - `+commander-heal-adjacent` «Лікування поруч з командиром» · entities/combat · 🌱.

## Пропозиції до словників
- `+cond:in_aura(a, leader)` — A в радіусі командування ватажка (окремий випадок `in_range` з радіусом від класу).
- `+cond:affinity(a, b)` (з FE) — тип A сильний проти типу B.
- `+effect:hire(leader, type)` — додати найманий загін до командира з оплатою.
- `+effect:counterattack` (з FE) — захисник бʼє у відповідь.
- `+ui:aura-range` — підсвічений радіус командира.
- `+window:hire-screen` — найм загонів перед сценарієм; `+window:class-change` — вибір нового класу.
- `+role:commander` — фігура, від якої залежать інші (аура, повʼязане життя).

## Джерела
- ⭐ [Wikipedia: Langrisser (серія)](https://en.wikipedia.org/wiki/Langrisser) — командири, найм, радіус командування з бонусами, +3 HP поруч з командиром, Treat/Heal, трикутник родів, хід «кожен юніт раз», годинник у пізніх частинах, понад 30 юнітів.
- [Wikipedia: Warsong](https://en.wikipedia.org/wiki/Warsong_(video_game)) — до 8 загонів одного типу на героя, загін = 10 солдатів, гроші за вцілілих, промоція, permadeath, цілі сценаріїв, розстановка.
- Steam: пошук «Langrisser» — рімейк I & II.
- YouTube: пошук «Langrisser Warsong gameplay».

## Непевне
- (?) Чи загони зникають зі смертю свого командира (за памʼяттю серії — так, джерелом не підтверджено).
- (?) Формула шкоди і її залежність від HP загону; обмін ударами (контратака) у бою.
- (?) Хто отримує досвід за вбивство загоном; рівень промоції; чи радіус росте з класом.
- (?) Бонуси терену в першій грі (у Langrisser II — «чим грубіший терен, тим більший бонус»; ліс +20 % для стрільців).
- (?) Летуни ігнорують терен і отримують бонус захисту (+25 % за гайдом Mobile).
