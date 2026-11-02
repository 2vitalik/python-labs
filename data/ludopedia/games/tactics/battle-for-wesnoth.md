---
title: The Battle for Wesnoth (Битва за Веснот)
slug: battle-for-wesnoth
family: tactics
also: [build-sim]
klass: figure
axes:
  field: hex
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2003
platforms: [PC, Mac, Linux, Android, iOS]
links:
  - {kind: official, url: "https://www.wesnoth.org/manual/dev/manual.en.html", best: true, note: "офіційний посібник гравця: ZOC, місцевість, час доби, бій, досвід, найм, села"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Battle_for_Wesnoth", note: "огляд: гекси, захист місцевості, день/ніч, шість типів шкоди, GPL"}
  - {kind: wiki, url: "https://wiki.wesnoth.org/FAQ", note: "ZOC, рівень 0 без ZOC, skirmisher, AMLA"}
  - {kind: wiki, url: "https://wiki.wesnoth.org/BasicStrategy", note: "XP 8×рівень за вбивство, лінії оборони з ZOC"}
  - {kind: wiki, url: "https://wiki.wesnoth.org/GettingStarted", note: "цикл 6 ходів, найм із замку, села, upkeep, лікування, перенесення в кампанії"}
  - {kind: official, url: "https://www.wesnoth.org/", note: "завантаження; open source"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=battle+for+wesnoth"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=battle+for+wesnoth+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, impassable-cells, floor-types, hp-damage, melee-vs-ranged, legal-move-highlight, ai-opponent, hot-seat, save-game, replay, in-game-editor, +zone-of-control, +movement-points, +terrain-defense, +hit-chance, +retaliation, +day-night-cycle, +pilot-xp-skills, +recruit-from-base, +capture-income, +status-effects, +fog-of-war, +leader-death-lose, +turn-limit-lose, +damage-forecast]
proposes: ["+trigger:attacked", "+trigger:enter_zone", "+cond:prob", "+cond:status", "+effect:set_status", "+effect:set_side", "+effect:currency", "+role:site", "+role:piece", "+role:zone", "+ui:reachable-highlight", "+ui:damage-forecast", "+ui:time-of-day", "+window:attack-dialog", "+window:recruit-window", "+window:unit-window", "+window:status-table", "+window:map-window", "+feature:roster-carryover", "+axis:actors", "+axis:session"]
author: opus
date: 2026-11-02
---

# The Battle for Wesnoth — гексова війна, де вирішують місцевість, час доби й зони контролю

## Суть
Гравець веде армію фентезі-юнітів по гексовій мапі: наймає їх із замку за золото, захоплює села заради доходу й лікування, атакує ворогів у раундах ударів із шансом влучання, що залежить від **місцевості під ціллю**. Сторони мають «світогляд» (lawful/chaotic/neutral/liminal), і цикл дня й ночі на 6 ходів змінює їхню шкоду на ±25 %. Юніти набирають досвід і переходять на вищий рівень, а в кампаніях ветерани переходять у наступний сценарій. Відкрита гра (GPL) з редактором мап, мультиплеєром і сотнями кампаній.

## Поле і час
- Поле — гексова сітка довільного розміру (мапи від ~20×20 до 50×50+). Кожен гекс має тип місцевості (або мішаний «псевдотип», напр. гори+ліс), може містити село, замок, донжон (keep) і одного юніта.
- Покроково: ходять сторони по черзі; за свій хід гравець рухає й атакує будь-якими юнітами в будь-якому порядку, потім **End Turn**. Сценарій має ліміт ходів (напр. 24).
- Час доби — 6 фаз циклом, по одній на хід: Dawn → Morning → Afternoon → Dusk → First Watch → Second Watch. Печери — вічна темрява; деякі гекси й юніти «освітлюють» сусідів (illuminates).
- Видимість: туман (fog) — місцевість видно, юніти поза зоною огляду ні; пелена (shroud) — не розвідані гекси чорні. Обидва — налаштування сценарію/гри.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лідер (canrecruit) | piece | рівень 2–3, HP, рух | наймає й відкликає юнітів, стоячи на донжоні; його смерть зазвичай = поразка |
| Юніт рівня 1+ (Spearman, Elvish Fighter, Orcish Grunt…) | piece | cost, HP, MP, XP, рівень, alignment, атаки, опори, movetype | рух за очками руху, атака сусіда, ZOC на 6 сусідів |
| Юніт рівня 0 (Walking Corpse, Peasant, Goblin) | piece | дешевий | **не має ZOC**; дає мало XP |
| Skirmisher (Saurian, Thief-гілка, Fencer) | piece | здібність `skirmisher` | ігнорує ворожі ZOC |
| Цілитель (Elvish Shaman, White Mage) | piece | `heals +4` / `heals +8`, `cures` | на початку ходу лікує сусідніх союзників; White Mage знімає отруту |
| Регенератор (Troll) | piece | `regenerates` | +8 HP щоходу і зняття отрути замість лікування |
| Засідник (Elvish Ranger, Wose) | piece | `ambush` | невидимий для ворога в лісі |
| Нічний мисливець (Nightgaunt-лінія) | piece | `nightstalk` | невидимий уночі |
| Лідер-ватажок (Lieutenant) | piece | `leadership` | сусідні союзники нижчого рівня бʼють сильніше |
| Літун (Gryphon, Drake, Bat) | piece | movetype fly | майже вся місцевість коштує 1 руху, але низький захист |
| Рівнина / дорога | terrain | рух 1, захист ~40 % (люди) | базова клітина |
| Ліс | terrain | рух 2, захист 50 % (ельфи 70 %, кіннота 30 %) | різний за movetype |
| Пагорби / гори | terrain | рух 2 / 3, захист 50 / 60 % | гноми — 60/70 % |
| Мілководдя / болото | terrain | рух 3, захист 20 % | водні раси — навпаки добре |
| Глибока вода / прірва / непрохідне | static | — | непрохідна для більшості (крім літунів і водяних) |
| Печера, гриби, пісок, лід, риф | terrain | свої ціни | — |
| Село | zone | власник, дохід, лікування 8 HP | захоплюється входом; дає золото щоходу, лікує й знімає отруту |
| Замок (castle) | terrain | захист 60 % | гекси, куди ставлять найнятих |
| Донжон (keep) | terrain | — | лідер на ньому може наймати в повʼязані гекси замку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, unit, hex)` → ЯКЩО `custom: «сума цін місцевості по шляху ≤ залишок MP»` → ТО `move(unit, hex)`; ціна гекса = `movetype[terrain]`.
- КОЛИ `enter_zone(unit, zoc(enemy))` (гекс, сусідній з ворогом рівня ≥1) → ЯКЩО `not has(unit, skirmisher)` → ТО `custom: «залишок руху = 0»` (зупинка).
- КОЛИ рух у тумані → ЯКЩО `custom: «відкрився прихований ворог поруч / засідник»` → ТО `custom: «рух перервано (ambushed)»`.
- КОЛИ `enter(unit, village)` → ЯКЩО `not same(unit, village, side)` → ТО `set_side(village, unit.side)`, `custom: «MP = 0»`.
- КОЛИ `input(recruit, type)` → ЯКЩО `cell(leader, keep)` and `has(side, gold ≥ cost)` and `free(castle_hex)` → ТО `currency(−cost)`, `spawn_at(unit, castle_hex)`; новий юніт не ходить цього ходу; трейти (`strong`, `quick`, `resilient`, `intelligent`…) — випадкові.
- КОЛИ `input(recall, veteran)` → ЯКЩО ті самі умови → ТО `currency(−20)`, `spawn_at(veteran, castle_hex)`.
- КОЛИ `input(attack, a, b)` → ЯКЩО `adjacent(a, b)` → ТО бій: `attacked(b, a)` → раунди ударів почергово (атакувальник першим), кожен удар — `prob(100 − defense(b.terrain))` → `damage(dmg)` або промах. Захисник **відповідає** зброєю того ж діапазону (melee/ranged), якщо має.
- Шкода удару: `custom: «base × (1 + ToD + leadership) × (1 − resistance[type])»`; типи шкоди — blade, pierce, impact, fire, cold, arcane.
- ToD: lawful `+25 %` удень (Morning, Afternoon), `−25 %` уночі; chaotic — навпаки; neutral — без змін; liminal — найкращий у сутінках (?).
- Спецзброї: `magical` — `prob(70)` незалежно від місцевості (лише в атаці); `marksman` — шанс щонайменше 60 % (лише в атаці); `firststrike` — бʼє першим навіть у захисті; `charge` — в атаці обидві сторони бʼють подвійно; `backstab` — подвійна шкода, якщо за ціллю стоїть ворог цілі; `drain` — лікує себе на половину завданої шкоди; `berserk` — бій триває до 30 раундів, доки хтось не загине.
- `poison`: КОЛИ влучання → ТО `set_status(b, poisoned)`; КОЛИ `turn_start(side)` → ЯКЩО `status(poisoned)` → ТО `damage(8)` (не нижче 1 HP), замість лікування.
- `slow`: КОЛИ влучання → ТО `set_status(b, slowed, до кінця його наступного ходу)` — половина шкоди й руху.
- КОЛИ `hp_zero(unit)` → ТО `disappear_a`; вбивці `custom: «XP += 8 × рівень убитого (рівень 0 → 4)»`; інакше кожна сторона бою отримує XP = рівень суперника.
- КОЛИ `counter(xp, ≥, max_xp)` → ТО `transform(next_level)` (вибір гілки, якщо їх кілька) + `heal(full)`; на максимальному рівні — AMLA: `+3 max HP` і повне лікування.
- КОЛИ `turn_start(side)` → ТО лікування: село 8 HP · цілитель +4/+8 · regenerates 8 · відпочинок (не рухався й не бився хід) +2; не сумуються, береться найбільше (?).
- КОЛИ `turn_start(side)` → ТО `currency(+base_income + villages × village_gold − max(0, upkeep − villages))`; upkeep = сума рівнів юнітів (крім `loyal`).
- КОЛИ `died(enemy_leader)` для всіх ворожих лідерів → ТО `win` (типова ціль; сценарій може задати іншу).
- КОЛИ `counter(turn, >, limit)` → ТО `lose` (у кампаніях) / нічия-завершення (у MP).
- Перемога: виконати цілі сценарію (зазвичай вбити лідерів). Поразка: загибель свого лідера чи героя або вичерпання ходів. Рахунок: у кампанії — золото, що переходить далі, з бонусом за ранню перемогу (?).

## Керування і ввід
- Миша: клік по юніту — вибір і підсвітка досяжних гексів (недосяжні затемнюються); наведення на гекс — шлях з номерами ходів, якщо треба кілька; клік — рух. Якщо шлях довший за MP, юніт продовжить його наступного ходу (goto).
- Клік по ворогу поруч → вікно атаки з вибором зброї і прогнозом. Правий клік — контекстне меню (Recruit, Recall, Describe Unit, Label…).
- Undo/redo руху, доки не відкрито нову інформацію (туман) і не було випадковості (бій).
- Клавіші: наступний юніт, завершити хід юніта, End Turn, найм, статус-таблиця, чат (?).
- Сторони: AI, hotseat за одним компʼютером, онлайн-лобі; черга сторін фіксована сценарієм.

## Вікна, меню, HUD
- `main-menu`: Tutorial, Campaigns, Multiplayer, Load, Add-ons, Map Editor, Preferences, Help, Credits, Quit, Language.
- `game-screen`: гексове поле; верхня панель — `coins` (золото), кількість сіл, юніти/upkeep, дохід, `turn-counter` «Turn 5/24», `time-of-day` (іконка фази); права панель — `minimap`, портрет часу доби з бонусами, `stat-panel` вибраного юніта (тип, трейти, HP, XP, рух, атаки, опори), кнопка `end-turn-button`.
- `attack-dialog`: список атак обох сторін (шкода × удари, тип, спецзброї), шанс влучання; кнопка «Damage Calculations» — розподіл HP після бою й шанс загибелі кожної сторони (`damage-forecast`).
- `recruit-window` / recall: список типів з ціною й описом юніта; recall — ветерани з XP і трейтами.
- `unit-window` (Describe Unit) + довідка-енциклопедія `codex-window`: юніти, місцевості, здібності, спецзброї, трейти.
- `status-table`: сторони, золото, села, юніти, upkeep, дохід. Unit list — усі свої юніти.
- Objectives — цілі сценарію й умови поразки; діалоги-катсцени `dialogue-window`.
- `save-slots` / Load, `replay-window` (збережені повтори), `lobby-window` і екран налаштування гри (мапа, ера, fog/shroud, золото за село, ліміт ходів).
- `editor-window` — редактор мап із генератором випадкових мап.
- `end-screen`: перемога/поразка сценарію з перенесенням золота.

## Фічі поза полем
- Кампанії з послідовними сценаріями: виживші юніти й золото переносяться (`roster-carryover`), recall ветеранів.
- `level-editor` мап і сценаріїв, `mod-support` (WML, Lua), браузер аддонів — тисячі кампаній і ер.
- `hotseat`, `online-multiplayer` з лобі, `spectator`, `replay`, `chat`, `ai-opponent-levels` (RCA AI).
- `difficulty-presets` (зазвичай ворогу більше золота й сильніші найми, гравцю менше ходів), `autosave` на початку ходу, `save-slots`.
- `undo` руху, `tutorial`, `codex` (вбудована довідка), `localization` ~30 мов, `remap-controls`, `fullscreen`.

## Варіації й родичі
- Ери (набори фракцій): Default (Loyalists, Rebels, Northerners, Undead, Knalgans, Drakes, Dunefolk), Age of Heroes (старт з рівня 2), Ladder Era.
- Родичі: Master of Monsters, Warsong/Langrisser (джерело натхнення), Advance Wars (квадратна сітка, без RNG у бою), Fire Emblem (зброя-трикутник), Heroes of Might and Magic (гекси в бою).
- Осі варіацій:
  - **рух**: фіксовані клітини / очки руху з ціною місцевості за типом юніта;
  - **бій**: детермінований (Advance Wars, Polytopia) / раунди ударів із RNG (Wesnoth) / кубики (Blood Bowl);
  - **захист**: від клітини цілі (Wesnoth) / від укриття поруч (XCOM) / від напрямку удару (FFT);
  - **ZOC**: нема / зупиняє (Wesnoth) / вимагає кидка для виходу (Blood Bowl).

## Цікавинки для курсу
- Очки руху + ціна гекса за типом юніта = Dijkstra на гексах; підсвітка досяжних — 🥉 (гексові координати + пошук).
- Зона контролю (вхід у сусідство ворога обнуляє рух) як модифікатор того ж Dijkstra — 📎.
- Шанс влучання від місцевості цілі + раунди ударів + прогноз розподілу HP (`Damage Calculations`) — 🥈: точна ймовірність результату бою динамічним програмуванням.
- Цикл дня/ночі з alignment як глобальний модифікатор шкоди — 🌱.
- Економіка: села як захоплювані точки доходу + upkeep за рівні юнітів — 📎.
- Туман і пелена з переривом руху при відкритті ворога — 🥉.
- XP і рівні з деревом підвищень і переносом у кампанії — 🥉.

## Мапа на каталог
- Є: `piece-move-patterns` ↔ рух за movetype · `impassable-cells` ↔ глибока вода/прірва для піших · `floor-types` ↔ місцевість із ціною руху й захистом · `hp-damage` · `melee-vs-ranged` ↔ відповідь лише тим самим діапазоном · `legal-move-highlight` + `hover-highlight` ↔ досяжні гекси і шлях · `ai-opponent` · `hot-seat` · `save-game`/`save-autosave` · `replay` · `in-game-editor` · `sequential-levels` ↔ кампанія · `round-currency` ↔ золото · `minimap-radar` · `field-scaling` · `game-screen`/`main-menu`/`settings-window`/`help-window`.
- **Нема** → пропозиції карток:
  - `+zone-of-control` «Зона контролю» · entities/legality · 📎 · слот {effect: stop|roll_to_leave} — Wesnoth, Blood Bowl.
  - `+movement-points` «Очки руху з ціною клітини» · entities/move · 🥉 · слот {cost_by_type: table} — Dijkstra-досяжність.
  - `+terrain-defense` «Захист від місцевості» · entities/combat · 📎 · слот {defense: table}.
  - `+hit-chance` «Шанс влучання» · entities/combat · 📎 · слот {p_formula}.
  - `+retaliation` «Відповідь на атаку» · entities/combat · 📎.
  - `+day-night-cycle` «Цикл дня і ночі з модифікаторами» · game-logic/difficulty · 🌱 · слот {phases: 6}.
  - `+pilot-xp-skills` (вже запропоновано в Into the Breach) — XP за бій/вбивство, рівні, AMLA.
  - `+recruit-from-base` «Найм на базі» · game-logic/economy · 📎 · слот {where: keep+castle}.
  - `+capture-income` «Захоплювані точки доходу» · game-logic/economy · 📎 · слот {income, heal}.
  - `+status-effects` «Статуси з тривалістю» · entities/state · 🥉 · слот {list} — poison, slow (дитина `temporary-modes`).
  - `+fog-of-war` «Туман війни» · interface/render · 🥉 · слот {mode: fog|shroud}.
  - `+leader-death-lose` «Загибель лідера» · game-logic/lose · 🌱.
  - `+turn-limit-lose` «Ліміт ходів» · game-logic/lose · 🌱 · слот {turns}.
  - `+damage-forecast` «Прогноз бою» · interface/hud · 🥈 — розподіл HP і шанс загибелі.

## Пропозиції до словників
- `+trigger:attacked(b, a)` — початок бою як подія (спецзброї, відповідь); `+trigger:enter_zone(a, zone)` — вхід у зону (ZOC, тенетна зона), відмінне від `enter` у тип клітини.
- `+cond:prob` ⏳ — тут головна умова кожного удару; `+cond:status` / `+effect:set_status` — poisoned, slowed (вже з Into the Breach).
- `+effect:set_side` ⏳ — захоплення села; `+effect:currency` ⏳ — дохід/найм.
- `+role:site` — захоплювана точка з власником і пасивним ефектом (село Wesnoth, місто Polytopia); `+role:piece` ⏳, `+role:zone` ⏳ — ZOC як зона навколо фігури.
- `+ui:reachable-highlight` (є в Sokoban) — досяжні гекси з урахуванням ціни; `+ui:damage-forecast` — прогноз результату; `+ui:time-of-day` — індикатор фази й бонусів.
- `+window:attack-dialog` — вибір зброї з прогнозом; `+window:recruit-window`; `+window:unit-window` — картка юніта; `+window:status-table` — таблиця сторін; `+window:map-window` ⏳ — редактор/огляд мапи.
- `+feature:roster-carryover` — юніти й золото переходять між сценаріями (Wesnoth, XCOM, Blood Bowl-ліга).
- `+axis:actors` = `party`; `+axis:session` = `campaign` / `match`.

## Джерела
- ⭐ [Battle for Wesnoth User's Manual](https://www.wesnoth.org/manual/dev/manual.en.html) — офіційний посібник: інтерфейс, рух, ZOC, бій, час доби, досвід (сайт за анти-бот-захистом: людині відкривається, агенту — ні).
- [Wikipedia](https://en.wikipedia.org/wiki/The_Battle_for_Wesnoth) — гекси, захист місцевості, день/ніч, типи шкоди, історія, GPL.
- [Wesnoth wiki: FAQ](https://wiki.wesnoth.org/FAQ) — ZOC зупиняє рух, рівень 0 без ZOC, skirmisher, AMLA +3 HP.
- [Wesnoth wiki: BasicStrategy](https://wiki.wesnoth.org/BasicStrategy) — XP 8 за рівень убитого, лінії оборони через ZOC.
- [Wesnoth wiki: GettingStarted](https://wiki.wesnoth.org/GettingStarted) — цикл 6 ходів, найм лише з донжона, upkeep за рівень, лікування, перенос юнітів.
- [wesnoth.org](https://www.wesnoth.org/) — завантаження.
- YouTube: пошук «battle for wesnoth gameplay».

## Непевне
- (?) Числа без першоджерела (офіційний посібник і units.wesnoth.org заблоковані для агента): ±25 % день/ніч, magical 70 % (підтверджено GiantBomb), marksman ≥60 %, село лікує 8, отрута 8/хід, відпочинок +2, recall 20 золота, berserk 30 раундів.
- (?) Liminal: точна формула бонусу в сутінках.
- (?) Чи сумуються джерела лікування (за памʼяттю — береться максимум, відпочинок додається окремо).
- (?) Формула бонусу за ранню перемогу й частка золота, що переходить (80 %?).
- (?) Конкретні клавіші; захист у відсотках подано як типові для людської піхоти.
