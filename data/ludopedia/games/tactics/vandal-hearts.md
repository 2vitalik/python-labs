---
title: Vandal Hearts
slug: vandal-hearts
aka: [ヴァンダルハーツ, "Vandal Hearts: The Lost Ancient Civilization", Vandaru Hātsu]
family: tactics
also: []
klass: figure
axes:
  field: layers
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1996
platforms: [PS1, Saturn, PC (JP/KR 1998)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Vandal_Hearts", best: true, note: "ізометричне 3D-поле з поворотом, хід сторонами, розділений рух, 7 класів і «камінь-ножиці-папір», умови перемоги, смерть лідера, штраф золотом"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Vandal_Hearts_II", note: "сиквел: Dual-Turn (одночасні ходи), класи без фіксації; кінцівки першої гри від Trials of Toroah"}
  - {kind: other, url: "https://www.gamespot.com/reviews/vandal-hearts-review/1900-2550081/", note: "огляд GameSpot (агенту не відкрився, 403)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Vandal+Hearts", note: "пошук; гри в Steam нема"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Vandal+Hearts+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [hp-damage, melee-vs-ranged, impassable-cells, height-levels, floor-types, legal-move-highlight, reachable-highlight, inventory-items, inventory-limit, shop-between-levels, shop-catalog, unit-xp-skills, ai-opponent, destroy-all-enemies, reach-exit, player-death, sequential-levels, save-game, environment-death, player-camera, +class-triangle, +leader-death-lose, +split-movement, +class-promotion, +map-traps, +escort-npc, +hidden-trials, +retaliation]
proposes: ["+trigger:attacked", "+effect:counterattack", "+cond:height_diff", "+role:trap", "+feature:hidden-trials", "+window:headquarters", "+window:promotion-window", "+ui:height-badge", "+axis:session"]
author: opus
date: 2026-11-09
---

# Vandal Hearts — ранній ізометричний SRPG: висота, класи-трикутник і пастки, вбудовані в мапу бою

## Суть
Загін героя Еша проходить сюжетну послідовність боїв на ізометричних мапах-сітках з висотою. Сторони ходять по черзі: спершу всі юніти гравця, потім усі вороги. Класи повʼязані «камінь-ножиці-папір» (мечник/броня бʼють лучника, лучник — яструболицаря, яструболицар — мечника; маг — броню). Мапи — не лише рельєф: у багатьох боях є пастки й механізми поля, а умови перемоги різні (вбити всіх, вбити ватажка, довести юніта до точки, вберегти заручника).

## Поле і час
- Квадратна сітка з висотою клітин, 3D-рельєф з поворотом камери; персонажі — 2D-спрайти.
- Непрохідні клітини: вода, дерева, будівлі; рельєф і перепади висоти впливають на рух і бій (?).
- Хід — сторонами (`turn-structure: sequential`): гравець рухає всіх, потім AI.
- Рух юніта — бюджет клітин на хід, який **можна розбити** на кілька переміщень (підійти, ще підійти, тоді діяти).
- Інформація повна; випадковість — у влучаннях/критах (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Еш (лідер) | piece | HP, MP, Move, клас | його загибель = миттєва поразка |
| Swordsman (мечник) | piece | ближній бій | сильний проти Archer, слабкий проти Hawknight |
| Armor (важкий піхотинець) | piece | висока броня, малий Move | сильний проти Archer, слабкий проти магії |
| Archer (лучник) | piece | дальній бій | сильний проти Hawknight; дальність від висоти (?) |
| Hawknight (летун) | piece | політ | сильний проти Swordsman; перелітає перешкоди (?) |
| Monk | piece | лікування + середня сила | гібрид підтримки й бою |
| Mage | piece | MP, атакувальна магія | сильний проти Armor; слабкий захист |
| Cleric | piece | MP, лікування | слабкий захист |
| Ворожі юніти тих самих класів, монстри | enemy | — | AI; ходять у фазі ворога |
| Ватажок ворогів | boss | — | у частині боїв його смерть = перемога |
| Заручник / NPC для порятунку | ally | — | його смерть = поразка (місії порятунку) |
| Цільова клітина (вихід) | zone | — | довести юніта = перемога (частина боїв) |
| Пастка / механізм мапи | hazard | — | спрацьовує від наступання або за ходом: шипи, обвали, стріли (?) |
| Скриня | container | предмет | відкривається, ставши поруч/на неї (?) |
| Вода, дерево, будинок | static | — | непрохідні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «кожен юніт гравця по разу: рух (частинами) і одна дія»`; КОЛИ `custom: «усі юніти гравця походили або гравець завершив хід»` → ТО `end_turn` (фаза ворога).
- КОЛИ `input(move, u, cell)` → ЯКЩО `free(cell)` and `custom: «сумарний пройдений шлях за хід ≤ Move»` → ТО `move(u, cell)`; лишок Move можна витратити пізніше в тому ж ході.
- КОЛИ `input(attack, a, b)` → ЯКЩО `in_range(a, b, range)` → ТО `damage(b, n)`, де `n` множиться за трикутником класів: `custom: «×більше, якщо клас a сильний проти класу b»`.
- КОЛИ `custom: «атака»` → ЯКЩО `custom: «магічна атака»` and `custom: «ціль — Armor»` → ТО `custom: «підвищена шкода»`.
- КОЛИ `custom: «атака»` → ЯКЩО `custom: «атакувальник вище за ціль»` → ТО `custom: «шкода більша; знизу — менша»` (?).
- КОЛИ `custom: «юніт атакований у ближньому бою»` → ЯКЩО `custom: «вижив і може відповісти»` → ТО `custom: «контратака»` (?).
- КОЛИ `enter(u, trap)` → ТО `damage(u, n)` або `custom: «механізм мапи: обвал / постріл / зміна клітин»` (?).
- КОЛИ `input(heal, cleric, b)` → ТО `heal(b, n)`; `custom: «MP витрачається»`.
- КОЛИ `hp_zero(ash)` → ТО `lose`.
- КОЛИ `hp_zero(ally_unit)` → ТО `disappear(ally_unit)` до кінця бою + `currency(-n)`; у наступному бою юніт повертається.
- КОЛИ `hp_zero(hostage)` → ТО `lose`.
- КОЛИ `all_gone(enemy)` → ТО `win` (більшість боїв); КОЛИ `hp_zero(boss)` → ТО `win` (бої «вбити ватажка»); КОЛИ `reach(u, exit)` → ТО `win` (бої «дійти»).
- КОЛИ `custom: «досвід ≥ порогу»` → ТО `custom: «рівень +1»`; КОЛИ `custom: «рівень досяг порогу підвищення»` → ТО `choose(новий клас)` у штабі (?).
- КОЛИ `custom: «знайдено вхід у Trial of Toroah»` → ТО `custom: «таємний бій-випробування»`; усі Trials → Еш отримує вищий клас і іншу кінцівку (?).

## Керування і ввід
- Курсор по клітинах (хрестовина), обертання камери шифтами (?).
- Вибір юніта → підсвічені досяжні клітини → рух → меню дії: Attack / Magic / Item / Stay (?).
- Розділений рух: після першого кроку юніт лишається активним із залишком Move.

## Вікна, меню, HUD
- `main-menu`: New Game / Load.
- `headquarters` — штаб між боями: магазини зброї/броні/предметів, підвищення класів, збереження (?).
- `promotion-window` — вибір гілки класу при підвищенні (?).
- `game-screen`: ізометрична мапа; панель юніта (HP/MP, рівень, клас); `reachable-highlight`; `height-badge` клітини (?).
- `inventory-window` — предмети юніта (ліміт на руках) (?).
- `dialogue-window` — сюжетні сцени до й після бою; `end-screen` бою; Game Over.
- `save-slots` (картка памʼяті).

## Фічі поза полем
- `levels-sequential`: лінійна послідовність боїв з сюжетом; між ними — штаб.
- Прогресія юнітів (рівні, підвищення класів), магазини, `save-slots`.
- Таємні Trials of Toroah → альтернативні кінцівки.
- Saturn-версія (лише JP): відео, кілька кінцівок, додаткові персонажі, нова зброя і закляття.

## Варіації й родичі
- Сиквел Vandal Hearts II (Dual-Turn: гравець і AI рухають по одному юніту одночасно), приквел Flames of Judgment (2010).
- Родичі: Shining Force (хід сторонами), Final Fantasy Tactics / Tactics Ogre (висота, ізометрія), Fire Emblem (трикутник зброї замість класів).
- Осі варіацій:
  - **трикутник переваг**: за класом (VH) / за зброєю (Fire Emblem) / нема (Wesnoth — за типом шкоди);
  - **рух**: одним заходом / частинами (VH, XCOM-подібні) / за очками дії;
  - **смерть союзника**: остаточна (Fire Emblem) / штраф золотом і повернення (VH) / лічильник (FFT);
  - **поле**: лише рельєф / пастки й механізми як частина мапи (VH, Into the Breach).

## Цікавинки для курсу
- Трикутник класів як таблиця множників — 🌱.
- Розділений рух із залишком бюджету — 📎 (стан «юніт ще має Move»).
- Умови перемоги на вибір (вбити всіх / ватажка / дійти / вберегти) як дані рівня — 📎.
- Смерть союзника = штраф і повернення в наступному бою — 🌱.
- Пастки, привʼязані до клітин мапи (тригер на вхід) — 📎.
- Таємний рівень, що відкривається дією на звичайній мапі — 📎.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `impassable-cells` ↔ вода/дерева/будинки · `height-levels` · `floor-types` · `reachable-highlight` · `inventory-items` · `shop-between-levels` · `unit-xp-skills` · `destroy-all-enemies` · `reach-exit` · `player-death` ↔ смерть Еша · `environment-death` ↔ пастки · `player-camera` ↔ поворот камери.
- **Нема** → пропозиції карток:
  - `+class-triangle` «Трикутник класів» · entities/combat · 🌱 · слот {matrix}.
  - `+split-movement` «Рух частинами» · entities/legality · 📎.
  - `+class-promotion` «Підвищення класу за рівнем» · entities/state · 📎.
  - `+map-traps` «Пастки мапи» · entities/cells · 📎.
  - `+escort-npc` «Вберегти NPC» · levels/goal · 🌱.
  - `+hidden-trials` «Таємні випробування» · levels/progression · 📎.
  - `+leader-death-lose`, `+retaliation` — як у Fire Emblem/Wesnoth.

## Пропозиції до словників
- `+trigger:attacked`, `+effect:counterattack` — контратака (вже пропоновані іншими тактиками).
- `+cond:height_diff(a, b)` — різниця висот атакувальника й цілі.
- `+role:trap` — пастка мапи з тригером.
- `+window:headquarters` — штаб між боями (магазини, підвищення, збереження); `+window:promotion-window`.
- `+ui:height-badge` — висота клітини під курсором.
- `+feature:hidden-trials`; `+axis:session` = `campaign`.

## Джерела
- ⭐ [Wikipedia: Vandal Hearts](https://en.wikipedia.org/wiki/Vandal_Hearts) — ізометрія, поворот камери, непрохідні клітини, розділений рух, хід сторонами, умови перемоги, смерть лідера, штраф золотом, 7 класів і трикутник, версії.
- [Wikipedia: Vandal Hearts II](https://en.wikipedia.org/wiki/Vandal_Hearts_II) — Dual-Turn сиквела; кінцівки першої гри залежать від Trials of Toroah.
- [GameSpot: Vandal Hearts Review](https://www.gamespot.com/reviews/vandal-hearts-review/1900-2550081/) — огляд (не відкрився агенту).
- YouTube: пошук «Vandal Hearts gameplay».

## Непевне
- (?) StrategyWiki, GameFAQs, MobyGames і GameSpot віддали 403 — висота, пастки, контратаки, скрині, штаб і підвищення класів описано з памʼяті.
- (?) Як саме висота змінює шкоду й дальність лучників; чи є бонус за удар у спину.
- (?) Типи пасток (шипи, обвали, стріли) і чи вони видимі заздалегідь.
- (?) Рівні підвищення класів (10/20?) і розгалуження класу на другому підвищенні.
- (?) Як відкриваються Trials of Toroah (дія на певних мапах) і що дають.
