---
title: Fire Emblem (GBA, The Blazing Blade як база)
slug: fire-emblem
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
year: 2003
platforms: [GBA, Wii U VC, Switch Online]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fire_Emblem:_The_Blazing_Blade", best: true, note: "GBA-гра, на якій тримається опис: фази, трикутник, permadeath, підтримки, обмін"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Fire_Emblem", note: "серія: класи, досвід, трикутник, міцність зброї, Casual Mode"}
  - {kind: other, url: "https://serenesforest.net/the-blazing-blade/miscellaneous/calculations/", note: "Serenes Forest: формули атаки, швидкості, влучності, криту FE7"}
  - {kind: other, url: "https://serenesforest.net/the-blazing-blade/miscellaneous/true-hit/", note: "Serenes Forest: «справжня» влучність 2RN"}
  - {kind: fandom, url: "https://fireemblem.fandom.com/wiki/Special:Search?query=weapon+triangle", note: "пошук по вікі серії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fire+emblem+blazing+blade+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [piece-move-patterns, legal-move-highlight, melee-vs-ranged, hp-damage, player-death, inventory-items, inventory-limit, key-and-door, destroy-all-enemies, reach-exit, sequential-levels, save-multi-slot, +weapon-triangle, +terrain-move-cost, +terrain-bonus, +battle-forecast, +permadeath, +rescue-carry, +trade-items, +recruit-talk, +support-adjacency, +weapon-durability, +level-up-growth, +class-promotion, +fog-of-war]
proposes: ["+trigger:phase_start", "+effect:counterattack", "+effect:carry", "+effect:recruit", "+cond:affinity", "+role:boss", "+ui:battle-forecast", "+ui:terrain-window", "+window:battle-animation", "+window:unit-status", "+window:prep-screen", "+feature:mode-casual"]
author: opus
date: 2026-11-02
---

# Fire Emblem — армія з іменами на квадратній карті: трикутник зброї, ландшафт і смерть назавжди

## Суть
Гравець — тактик, що веде загін персонажів (кожен — фігура з класом, характеристиками, інвентарем зброї) через главу-карту. Хід — фаза гравця: кожен юніт рухається і робить одну дію; потім фаза ворога. Бій між двома юнітами — обмін ударами з передбаченими шансами (прогноз), де ключ — **трикутник зброї**, ландшафт і швидкість (подвійний удар). Загиблий юніт зникає з кампанії назавжди, тому гра — ще й керування ризиком.

## Поле і час
- Квадратна сітка (карти ~15×10 … 30×30), камера з прокруткою; клітина — тип ландшафту з ціною руху й бонусами.
- Хід = фази: **Player Phase** → **Enemy Phase** → **Other Phase** (зелені NPC-союзники) → наступний хід. У кожній фазі всі юніти сторони діють по одному в довільному (гравець) / заданому (ШІ) порядку.
- Туман війни в окремих главах: видно лише в радіусі зору юнітів (злодії бачать далі; смолоскипи).
- Випадковість під час бою (влучність, крит), ріст характеристик на рівні — випадковий за «growth rates».

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Лорд (Lyn / Eliwood / Hector) | piece | HP, Str/Mag, Skl, Spd, Lck, Def, Res, Con, Mov | загибель = поразка глави; Seize трону |
| Піхота (Myrmidon, Fighter, Soldier, Knight…) | piece | Mov 4–5; броньовані Mov 4 | меч / сокира / спис; броня — висока Def, повільна |
| Кіннота (Cavalier, Paladin, Troubadour) | piece | Mov 7–8 | великий рух; ліс/пустеля дорогі |
| Літуни (Pegasus, Wyvern) | piece | Mov 7 | ціна руху 1 майже скрізь; луки ефективні проти них (×3) |
| Лучники | piece | дальність 2 | не контратакують упритул |
| Маги (Mage, Shaman, Monk) | piece | Mag, Res | anima / dark / light — свій трикутник; дальність 1–2 |
| Цілителі (Cleric, Priest) | piece | посохи | лікують, не атакують; досвід за лікування |
| Злодій (Thief) | piece | Spd, без ключа | відкриває скрині/двері без ключа, Steal, бачить далі в тумані |
| Танцівниця (Ninian/Dancer) | piece | — | Dance: дає сусідньому юніту ще одну дію |
| Ворог (усі ті ж класи) | enemy | — | ШІ: атакує досяжних, деякі стоять до тригера |
| Бос глави | boss | на троні, високий захист | часто не рухається; вбити = перемога в главі «Rout/Defeat» |
| NPC-союзник (зелений) | ally | — | діє в Other Phase; врятувати — бонус |
| Персонаж для вербування | enemy → piece | — | Talk певним юнітом → переходить на бік гравця |
| Зброя | — | Mt, Hit, Crit, Wt, Rng, Uses, ранг E…S | ламається після Uses ударів |
| Скриня | container | — | ключ (Chest Key) або злодій → предмет |
| Двері | gate | — | ключ (Door Key)/відмичка/злодій → відкрито |
| Село | static | — | Visit лордом/юнітом → предмет або вербування; бандити руйнують |
| Магазин / зброярня / арена | static | — | купівля за золото / бої на ставку |
| Ландшафт: рівнина | terrain | Def 0, Avo 0 | ціна 1 |
| Ліс | terrain | Def +1, Avo +20 | ціна 2 піхоті, 3 кінноті |
| Гора / пік | terrain | Avo +30 / +40, Def +1/+2 | ціна 3–4 піхоті; кіннота не проходить |
| Форт / трон / ворота | terrain | Def +2…+3, Avo +20…+30, лікування % HP щоходу | захисна позиція |
| Вода / море / річка | terrain | — | лише літуни, пірати/берсерки (море), кіннота ні |
| Стіна / тріщина | static | HP у тріщини | непрохідна; тріщину можна розбити |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(select, unit)` → ТО `custom: «Dijkstra по ціні ландшафту ≤ Mov»` → підсвітка синіх клітин руху і червоних клітин атаки.
- КОЛИ `move(unit, cell)` → ЯКЩО `not occupied(cell, enemy)` → ТО рух; ворожі юніти блокують прохід, союзні — ні (?).
- КОЛИ `input(attack, target)` → ЯКЩО `in_range(weapon.rng)` → ТО бій: атакуючий бʼє → захисник контратакує, якщо його зброя дістає → якщо `AS_a − AS_d ≥ 4` → атакуючий бʼє вдруге (симетрично для захисника).
- Сила удару: `Atk = Str + Mt × (3 якщо зброя ефективна)`; шкода `= Atk − Def` (маг. — `Res`), ×3 при криті.
- Attack Speed `AS = Spd − max(0, Wt − Con)` (?); Hit `= Hit_зброї + Skl×2 + Lck/2` (?) − Avoid цілі `= AS×2 + Lck + бонус ландшафту`; Crit `= Crit_зброї + Skl/2` − Lck цілі.
- Влучання: `custom: «два випадкові числа 0–99, середнє < Hit»` (2RN: 70 відображено ≈ 82 % справжніх).
- Трикутник: меч > сокира > спис > меч; anima > light > dark > anima; КОЛИ перевага → ТО `custom: «+15 Hit, +1 шкоди»`, недолік — навпаки (?).
- КОЛИ `hp_zero(unit)` → ЯКЩО unit гравця → ТО `custom: «permadeath — зникає з кампанії»`; ЯКЩО лорд → `lose`.
- КОЛИ `input(rescue, ally)` → ЯКЩО `Con(ally) ≤ Aid(rescuer)` → ТО `custom: «ally знімається з поля й несеться»`; рятівник: Skl і Spd ½; Drop / Give / Take — передати на сусіда.
- КОЛИ `input(trade, adjacent_ally)` → ТО `swap(items)` (інвентар 5 слотів); Trade і Rescue не закінчують хід, атака — закінчує.
- КОЛИ `input(talk, unit)` → ЯКЩО пара визначена сценарієм → ТО `set_side(unit, player)` (вербування) або підтримка.
- КОЛИ `turn_end` → ЯКЩО двоє з парою підтримки поруч (?) → ТО `counter(support_points, +n)`; поріг → розмова C/B/A → бонуси до Hit/Avo/Crit/Def у радіусі 3 клітин за «affinity».
- КОЛИ `input(chest|door)` → ЯКЩО `has(key)` або клас = thief → ТО `disappear_b`/`pickup(item)`; ключ витрачає `uses`.
- КОЛИ удар → ТО `counter(weapon.uses, -1)`; `== 0` → `disappear(weapon)`.
- КОЛИ бій/лікування/вбивство → ТО `counter(exp, +n)`; `≥ 100` → `custom: «level up: кожна характеристика +1 з імовірністю growth%»`.
- КОЛИ `input(promote_item)` → ЯКЩО `level ≥ 10` → ТО `transform(promoted_class)` + бонуси характеристик.
- КОЛИ `turn_start(side)` → ЯКЩО на форті/троні → ТО `heal(unit, %)`.
- КОЛИ `enter(lord, throne)` + Seize → ТО `win` (глава «Seize»); інші цілі: Rout (усі вороги), Defeat Boss, Survive N turns, Defend, Escape/Arrive.
- Перемога: умова глави · Поразка: смерть лорда, загибель захищуваного NPC, обрана умова · Рахунок: ранг тактика (швидкість, виживання, досвід, фонд, бойові) (?).

## Керування і ввід
- Курсор по клітинах (D-pad), A — вибір юніта → клітина руху → меню дій; B — скасування (рух можна скасувати до вибору дії).
- Меню дій юніта (контекстне): Attack · Staff · Rescue · Drop · Give · Take · Talk · Visit · Seize · Chest · Door · Steal · Dance · Item · Trade · Supply (?) · Wait.
- Map menu (A на порожній клітині): Unit (список) · Status (цілі, хід) · Options · Suspend · End (кінець фази).
- R — інфо-екран юніта; L — наступний юніт, що ще не ходив; Select/R на ворозі — показати його зону атаки.

## Вікна, меню, HUD
- `main-menu` (Resume Chapter, Restart Chapter, New Game, Extras) → `save-slots` (3 файли) (?).
- `custom-window` «Preparations» — перед главою: розстановка, вибір юнітів, обмін, склад (Convoy), магазин.
- `game-screen`: карта; `terrain-window` (назва, DEF, AVO) у куті; міні-вікно юніта під курсором (імʼя, HP); `objective-text` (Goal, хід); `legal-move-highlight` (синє — рух, червоне — атака); `threat-range` ворога.
- `custom-window` «Battle forecast» — для обох сторін: HP, Mt (шкода), Hit, Crit, `x2` подвійний удар, стрілки трикутника.
- `custom-window` «Battle animation» — сцена бою (вимикається: map-анімація).
- `custom-window` «Unit status» — характеристики, зброярні ранги, предмети, підтримки.
- `dialogue-window` — сюжетні сцени, розмови підтримки.
- `shop-window` (Armory/Vendor), арена — ставка й бій.
- `end-screen`: Game Over при смерті лорда; кінець глави → збереження → наступна.
- `settings-window`: швидкість анімацій, анімації бою on/off, курсор, музика, вікна HUD on/off.

## Фічі поза полем
- `levels-sequential` (глави) з побічними главами (gaiden) за умовами; `save-slots` + `suspend` (призупинити посеред глави).
- `permadeath` — ядро; пізніші ігри: Casual Mode (з New Mystery), Phoenix Mode (Fates).
- `difficulty-presets`: Normal / Hard (GBA), у FE7 — сюжетні режими Lyn/Eliwood/Hector.
- Економіка: золото з глав і сіл, магазини; Convoy (склад) у FE7 — у Merlinus.
- Підтримки: зібрані розмови в extras; arena і Link Arena (мультиплеєр) у GBA.
- Ранги тактика наприкінці (FE7) (?); sound room / extras (?).

## Варіації й родичі
- Серія від 1990 (NES): Genealogy (трикутник, діти), Path of Radiance (3D), Awakening/Fates (пари, Casual/Phoenix), Three Houses (батальйони), Engage (Break замість трикутника-бонусу).
- Родичі: Advance Wars (того ж розробника, армія без імен), Shining Force, Langrisser, Tactics Ogre, Wargroove.
- **Осі варіацій**: смерть — назавжди / Casual / Phoenix · трикутник — нема / ±бонус / Break (ціль не контратакує) · зброя — міцність / без міцності · відкат — нема / Divine Pulse (Three Houses) / Mila's Turnwheel (Echoes).

## Цікавинки для курсу
- Рух за ціною ландшафту за класом (Dijkstra з лімітом Mov) + підсвітка руху/атаки — 🥉; з ворожою зоною загрози — 🥈.
- Прогноз бою (детермінована формула шкоди + шанси) до натискання «Attack» — 🥉.
- Трикутник зброї як матриця переваг — 🌱 (таблиця 3×3), разом з ефективністю зброї проти класу — 📎.
- Rescue/Drop: юніт несе іншого, характеристики ріжуться навпіл — 📎.
- Permadeath + рівні з випадковим ростом за growth% — 📎.
- Фази ходу трьох сторін (гравець → ворог → NPC) — 🌱.
- ШІ ворога: «атакуй досяжного з найбільшою шкодою / найлегшого для вбивства» — 🥈.

## Мапа на каталог
- Є: `piece-move-patterns` (класи як патерни руху/дальності) · `legal-move-highlight` · `hover-highlight` · `melee-vs-ranged` (луки/маги без контри впритул) · `hp-damage` · `player-death` · `inventory-items` + `inventory-limit` (5 слотів) · `key-and-door` (скрині, двері, злодій) · `item-pickup` (села, скрині) · `destroy-all-enemies` (Rout) · `reach-exit` (Seize/Arrive) · `sequential-levels` · `save-multi-slot` · `save-progress` · `shop-window` · `game-screen` · `main-menu` · `settings-window` · `ai-greedy` · `mode-indicator` (фаза).
- **Нема** → пропозиції карток:
  - `+weapon-triangle` «Трикутник переваг» · entities/combat · 🌱 · слот {matrix}.
  - `+terrain-move-cost` «Ціна руху за ландшафтом і класом» · entities/move · 🥉.
  - `+terrain-bonus` «Бонус захисту/ухилу від клітини» · entities/combat · 🌱.
  - `+battle-forecast` «Прогноз бою» · interface/hud · 🥉.
  - `+permadeath` «Смерть назавжди в кампанії» · game-logic/lose · 🌱.
  - `+rescue-carry` «Нести союзника» · entities/interact · 📎.
  - `+trade-items` «Обмін між сусідами» · entities/state · 📎.
  - `+recruit-talk` «Вербування розмовою» · entities/interact · 📎.
  - `+support-adjacency` «Бонус від сусідства пари» · entities/state · 🥉.
  - `+weapon-durability` «Міцність зброї» · entities/state · 🌱.
  - `+level-up-growth` «Рівні з випадковим ростом» · entities/state · 📎.
  - `+class-promotion` «Підвищення класу предметом» · entities/state · 📎.
  - `+fog-of-war` «Туман війни за радіусом зору» · interface/render · 🥉.

## Пропозиції до словників
- `+trigger:phase_start` — початок фази сторони (player/enemy/other) — уточнення ⏳ `turn_start(side)` для 3+ сторін.
- `+effect:counterattack` — захисник бʼє у відповідь, якщо дістає; `+effect:carry` — юніт піднімає союзника; `+effect:recruit` — синонім `set_side` для вербування (може злитися з ним).
- `+cond:affinity` — пара має підтримку/спорідненість.
- `role:boss` (⏳) — вжито.
- `+ui:battle-forecast` — модал з прогнозом обох сторін; `+ui:terrain-window` — назва і бонуси клітини під курсором.
- `+window:battle-animation` — окрема сцена розіграшу бою; `+window:unit-status` — повна картка юніта; `+window:prep-screen` — підготовка перед главою.
- `+feature:mode-casual` — режим без permadeath.

## Джерела
- ⭐ [Wikipedia: The Blazing Blade](https://en.wikipedia.org/wiki/Fire_Emblem:_The_Blazing_Blade) — фази, трикутник, permadeath, підтримки, обмін, туман.
- [Wikipedia: Fire Emblem](https://en.wikipedia.org/wiki/Fire_Emblem) — механіки серії, міцність, Casual/Phoenix.
- [Serenes Forest: FE7 calculations](https://serenesforest.net/the-blazing-blade/miscellaneous/calculations/) — формули Atk, AS, Hit, Avoid, Crit, подвійного удару.
- [Serenes Forest: True hit](https://serenesforest.net/the-blazing-blade/miscellaneous/true-hit/) — 2RN.
- YouTube: пошук «fire emblem blazing blade gameplay».

## Непевне
- (?) Бонуси трикутника в GBA (+15 Hit / +1 шкоди) — з памʼяті; сторінка Serenes, що мала це показати, віддала дані іншої гри.
- (?) Формули: Serenes дав спрощені (Hit = Weapon Hit + Skill; AS = Spd − Wt) — розходиться з памʼяттю (Skl×2 + Lck/2, урахування Con); у таблиці — версія з памʼяті з позначкою.
- (?) Поріг подвійного удару ≥4 — з памʼяті; Serenes-сторінка каже «AS > AS ворога» (ймовірно, інша гра).
- (?) Бонуси ландшафту (числа) і лікування фортів — з памʼяті.
- (?) Накопичення підтримок (поруч наприкінці ходу / в радіусі) і ранги тактика — з памʼяті.
- (?) Чи блокують союзні юніти прохід — у GBA союзники проходимі, вороги — ні (з памʼяті).
