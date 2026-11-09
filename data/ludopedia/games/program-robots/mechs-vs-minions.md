---
title: Mechs vs. Minions
slug: mechs-vs-minions
aka: [MvM, "League of Legends: Mechs vs. Minions"]
family: program-robots
also: [board-digital, tactics]
klass: avatar
axes:
  field: square
  time: programmed
  opponent: coop
  info: full
  random: runtime
  goal: state
year: 2016
platforms: [board]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/mechs-vs-minions/game-rules.php", best: true, note: "правила: 6 слотів, драфт з пісочним годинником, стоси однієї стихії до 3, Damage Cards Glitch/System/Slot, фази, бомба, бос, лавова стіна"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mechs_vs._Minions", note: "огляд: 2–4 гравці, Command Line з 6 слотів, три фази раунду, кампанія місій"}
  - {kind: other, url: "https://rulespal.com/mechs-vs-minions/rulebook", note: "текст правил: Chain Lightning, Fuel Tank, Skewer, буксирування, бос GG-101, Zhonya's Minuteglass ~40 с"}
  - {kind: official, url: "https://eune.leagueoflegends.com/en/featured/mechs-vs-minions", note: "сторінка Riot Games"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=mechs+vs+minions+how+to+play", note: "пошук; правила і партії"}
stage: v1
coverage: 55
mechanics: [command-program, orientation-state, push-object, impassable-cells, item-pickup, spawn-points, button-toggle, key-and-door, in-round-upgrades, sequential-levels, move-timer, +card-programming-registers, +element-stacking-power, +slot-override-discard, +damage-cards-in-program, +timed-card-draft, +shared-team-draft, +slot-swap-by-scrap, +stomp-on-enter, +towing, +lava-wall-push, +escort-objective, +boss-program-line, +rune-gate-color-key, +mech-cannot-die, +team-kill-tracker, +schematic-unlocks, +coop-campaign-envelopes]
proposes: ["+effect:draft", "+effect:discard", "+effect:draw_card", "+effect:roll_dice", "+effect:stack(card, slot)", "+cond:stack_power(slot, op, n)", "+effect:tow", "+role:card", "+role:die", "+window:program-board", "+window:draft-window", "+ui:program-slots", "+ui:doom-tracker", "+feature:sealed-mission-envelopes"]
author: opus
date: 2026-11-09
---

# Mechs vs. Minions — кооператив, де кожен програмує свого меха лінією з 6 слотів, а пошкодження вписуються прямо в програму

## Суть
2–4 гравці разом ведуть мехів (йордлів з League of Legends) крізь місії кампанії: тиснуть міньйонів, носять кристали, ескортують бомбу, тікають від лавової стіни, бʼються з босом. Кожен мех має **Command Line з 6 слотів**; щораунду команда спільно драфтує карти під тиском пісочного годинника, і кожна взята карта або **кладеться в слот** (поверх тієї ж стихії — підсилює, поверх іншої — стирає), або йде на брухт. Програма змінюється лише трохи за раунд, тож план тягнеться з раунду в раунд. Пошкодження — це карти, що вкриють випадковий слот і виконуватимуться **замість** твоєї команди: мех не гине, але стає дедалі некерованішим.

## Поле і час
- Поле — квадратна сітка з картонних тайлів мапи (5 тайлів у коробці; усі місії після навчальної — з двох і більше). Суміжність для атак міньйонів — лише по ребру, без діагоналей.
- Шари клітини: підлога / рунна клітина кольору / ремонтний майданчик / масивний валун + фігури (мехи з напрямом, міньйони, бомба, кристали, бос).
- Раунд = три фази: **гравців** (драфт → програмування → виконання ліній по черзі гравців за годинниковою стрілкою), **міньйонів** (рух → спавн → атака), **небезпеки** (бос, лавова стіна — лише в деяких місіях). Потім перший гравець передається далі.
- `time: programmed`: виконання — слоти 1→6, порожні пропускаються, кожну карту виконувати обовʼязково.
- Усе на столі відкрите; випадковість — драфт, колода пошкоджень, кубики й «компас кольорів» (`random: runtime`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мех | player | позиція, напрям, Command Line (6 слотів), Damage Cards | виконує свою лінію; не може загинути |
| Command Card | — (команда, `+role:card`) | стихія (Fire/Electric/Metal/Computery), тип (Attack/Move/Turn), Power 1–3 = висота стосу | дія на виконанні; стос однієї стихії підсилює верхню карту |
| Slot Damage | — (карта) | номер слота з кубика | вкриває слот, виконується як некерована команда, блокує програмування слота |
| System Damage | — (карта) | — | постійний ефект поруч із лінією |
| Glitch Damage | — (карта) | — | миттєвий ефект, потім у скид |
| Міньйон | enemy | 1 HP | рухається за правилом місії, атакує суміжного меха чи бомбу, гине від 1 шкоди |
| Рунна клітина | switch | колір (червоний, зелений, жовтий, синій) | наступ: блокує спавн на ній; вимикає рунні щити й ворота того ж кольору |
| Рунні ворота | gate | колір | пропускають лише Move-карту відповідної стихії (Blaze, Speed, Skewer, Omnistomp) |
| Масивний валун | static | — | блокує мехів, міньйонів, боса й Ripsaw, як край поля |
| Ремонтний майданчик | terrain | — | наступ прибирає 1 Damage Card; можна зійти і стати знову |
| Кристал (Crystal Shard) | pickup | крихкий / ні | підбирається наступом; мех несе лише один; при шкоді падає у випадкову сторону |
| Бомба | object | здоровʼя на Doom Tracker | штовхається й буксирується, давить міньйонів, але отримує 1 шкоди за кожного; вибух = поразка |
| Лавова стіна | hazard | позиція | у фазі небезпеки штовхає мехів і бомбу вперед, 1 шкода за клітину; вбиває міньйонів на шляху |
| Бос | boss | Boss Command Line (4 слоти), 4 рунні щити | у фазі небезпеки виконує свою лінію; щит гасить шкоду свого кольору |
| Zhonya's Minuteglass | — (таймер) | ~40 с піску | обмежує драфт |
| Gear Tracker | — (лічильник) | вбивства, Team Gears, Doom, руни | кожні 5 вбивств → Team Gear; пороги відкривають схеми й Overdrive |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(player)` → ТО перший гравець `custom: «відкрити 5 карт (Double Draft — 10)»`, `timer(start, minuteglass)`.
- КОЛИ `input(pick, card)` → ЯКЩО `timer(>, 0)` → ТО `custom: «draft»` за годинниковою стрілкою, доки не взято 4 карти (у Double Draft кожен бере 2); при 4 гравцях — по 1 карті на гравця.
- КОЛИ `custom: «пісок вичерпано»` → ТО `custom: «решту карт роздати випадково, доки не взято 4»`, невзяте — у скид.
- КОЛИ `input(program, card, slot)` → ЯКЩО `not state(slot, damaged)` і `same(card, slot_top, element)` → ТО `custom: «покласти зверху; Power = висота стосу (≤3)»`; четверта карта скидає нижню.
- КОЛИ `input(program, card, slot)` → ЯКЩО `not same(card, slot_top, element)` → ТО `custom: «discard усього слота»`, карта лягає першою.
- КОЛИ `input(program, card, slot)` → ЯКЩО `state(slot, damaged)` → ТО `block`.
- КОЛИ `input(scrap, card)` → ЯКЩО `same(card, electric|computery, element)` → ТО `swap(slot_a, slot_b)` (два непошкоджені слоти); ЯКЩО Fire або Metal → `custom: «прибрати 1 Damage Card»` (ціна — у «Непевне»). Зберегти карту на потім не можна.
- КОЛИ `exec(slot n)` → ЯКЩО `count(cards_in_slot, >, 0)` → ТО `custom: «виконати верхню карту з Power = висота стосу»`; порожній слот пропускається.
- КОЛИ `exec(move k)` → ЯКЩО `free(front)` → ТО `move(mech, facing)` k разів; ЯКЩО `occupied(front, minion)` → ТО `disappear(minion)`, `counter(kills, +1)` (мех тисне, а не штовхає); ЯКЩО непрохідне → `block`. Мех мусить рухатись, якщо не заблокований.
- Omnistomp: КОЛИ `exec(omnistomp)` → ТО `move(mech, forward|left|right)`; назад — ніколи.
- КОЛИ `exec(turn p)` → ТО p=1: `rotate(mech, ±90)`; p=2: `rotate(mech, ±90|180)`; p=3: `custom: «будь-який поворот, включно з повним колом»`; поворот обовʼязковий.
- КОЛИ `exec(attack)` → ТО `damage(target, 1)` кожній цілі; атака не рухає й не повертає меха.
- КОЛИ `exec(chain_lightning p)` → ТО `damage(first, 1)` — ціль прямо або по діагоналі попереду, далі `custom: «ланцюг по діагоналі до 2/4/6 цілей за Power 1/2/3»` (?).
- КОЛИ `died(minion)` → ЯКЩО `custom: «убитий Skewer»` → ТО `give(mech, shield)` — одноразовий щит на карті.
- КОЛИ `custom: «мех от-от отримає шкоду»` → ЯКЩО `custom: «у лінії стос Fuel Tank»` → ТО `custom: «підірвати: ігнорувати шкоду, discard стосу»`, `damage(all_in_range, 1)`; радіус росте з Power.
- КОЛИ `exec(move k)` → ЯКЩО `adjacent(mech, bomb|mech)` і `custom: «k ≥ 2 в одній карті»` → ТО `custom: «tow: обʼєкт займає клітину, яку мех звільнив»`; дві карти Move 1 поспіль не буксирують.
- КОЛИ `custom: «поштовх ланцюжка»` → ЯКЩО `custom: «будь-який елемент ланцюга не може зрушити»` → ТО `block` для всього ланцюга; у валун, активні ворота й за край штовхати не можна.
- КОЛИ `phase_start(minion)` → ТО `move(minion, mission_rule)`; ЯКЩО `not free(target)` або `edge(minion)` → ТО `block` (у клітину з кристалом — можна); мехів міньйони не штовхають.
- КОЛИ `phase_start(minion)` → ЯКЩО `free(spawn_cell)` і `not occupied(rune_cell, mech)` → ТО `spawn_at(minion, rune_cell)` (місце — за місією).
- КОЛИ `phase_start(minion)` → ЯКЩО `adjacent(minion, mech)` → ТО `custom: «мех тягне Damage Card»`; ЯКЩО `adjacent(minion, bomb)` → ТО `damage(bomb, 1)`.
- КОЛИ `custom: «мех отримав 1 шкоду»` → ТО `custom: «draw_card(damage)»`, по одній і до кінця: Glitch → ефект і скид; System → `set_state(mech, system_damage)`; Slot → `custom: «roll_dice(number) → вкрити слот n, замінивши попередню шкоду там»`.
- КОЛИ `exec(slot n)` → ЯКЩО `state(slot, damaged)` → ТО `custom: «виконати текст Damage Card замість команд»`.
- КОЛИ `enter(mech, repair_pad)` → ТО `custom: «прибрати 1 Damage Card»`.
- КОЛИ `enter(mech, crystal)` → ЯКЩО `not has(mech, crystal)` → ТО `pickup(mech, crystal)`; КОЛИ мех отримує шкоду → ЯКЩО `has(mech, crystal)` → ТО `custom: «кристал падає у бік за компасом і кубиком»`; крихкий кристал бʼється від 1 шкоди або наступу.
- КОЛИ `enter(mech, rune_cell)` → ТО `clear_state(rune_shields|rune_gates, color)` — щити й ворота цього кольору вимикаються; ворота знову активні, коли крізь них пройшли або бос отримав шкоду того кольору.
- КОЛИ `counter(kills, ==, 5k)` → ТО `counter(team_gears, +1)`; КОЛИ `counter(team_gears, >=, threshold)` → ТО `unlock(schematic)`; КОЛИ `counter(team_gears, >=, 15)` → ТО `unlock(overdrive)` усім.
- КОЛИ `phase_start(danger)` → ЯКЩО `mode(lava_wall)` → ТО `push(mechs, bomb)`, `damage(each, 1)` за клітину поштовху, `disappear(minion)` під стіною.
- КОЛИ `phase_start(danger)` → ЯКЩО `mode(boss)` → ТО бос виконує 4 слоти; порожній слот — дія за замовчуванням. Щораунду перший гравець бере 2 карти боса, одну програмує, другу скидає.
- КОЛИ `custom: «виконано слот боса з Power 3»` → ТО `lose` (Doom Cannon GG-101).
- КОЛИ `hp_zero(bomb)` → ТО `lose` (місія провалена).
- Перемога: мета місії (Mission Dossier) — напр. донести кристали, вивести бомбу, перемогти боса. Мех ніколи не знищується — поразка лише через обʼєкти місії.

## Керування і ввід
- Спільний драфт: перший гравець перевертає годинник, гравці по колу хапають карти з відкритого ряду — розмова й узгодження в реальному часі.
- Програмування: для кожної взятої карти — слот (підсилити / переписати) або брухт (обмін двох слотів, ремонт).
- Виконання: гравець сам «грає» свою лінію, обираючи параметри кожної карти (куди повернути, кого бити, скільки клітин іти в межах Power).
- Фази міньйонів і боса виконує перший гравець за правилами місії, кидаючи кубики й компас.

## Вікна, меню, HUD
- (цифрова версія) `main-menu` → `level-select` кампанії (10 місій у конвертах + фінальний конверт).
- (цифрова версія) `+window:draft-window` — відкритий ряд карт драфту з `timer-countdown` пісочного годинника.
- (цифрова версія) `+window:program-board` — планшет Command Line: `+ui:program-slots` (6 слотів зі стосами і Power), покриті шкодою слоти, System Damage збоку, клітинка Overdrive.
- (цифрова версія) `game-screen` — тайли мапи, мехи з напрямом, міньйони, `+ui:doom-tracker` (лічильник бомби / HP боса), лічильник вбивств і Team Gears, рунні монети.
- (цифрова версія) `instruction-highlight` — поточний слот при виконанні; `message-log` подій фази міньйонів.
- (цифрова версія) `end-screen` — місію пройдено / провалено; `codex-window` — каталог схем і карт.
- Переходи: брифінг місії → раунди (драфт → лінії → міньйони → небезпека) → кінець місії → наступний конверт.

## Фічі поза полем
- `levels-sequential` / `level-unlock`: кампанія з 10 місій у запечатаних конвертах (`+feature:sealed-mission-envelopes`), кожна вводить нові правила, компоненти й схеми.
- Навчальна місія (`tutorial`) — без таймованого драфту; з місії 1 драфт іде під годинник.
- `mode-coop` 2–4 гравці; при меншій кількості кожен бере більше карт у драфті.
- Схеми (Schematic Cards) — постійні здібності, що вмикаються на порогах Team Gears (`meta-progression` у межах кампанії).

## Варіації й родичі
- Родичі в корпусі: `roborally` (5 регістрів з руки, пошкодження замикають регістри — тут шкода **вписується** в слот), `colt-express` (спільна стопка програмування), `asteroyds` (програма маневрів під таймером), `robot-turtles` і `lightbot` (одиночне програмування картами/командами).
- Осі варіацій: **як змінюється програма** (переписується вся щораунду — RoboRally / по одній карті в раунд — MvM); **пошкодження** (менше карт / замкнені регістри / карта-шкода в слоті); **гравці** (суперники / кооператив проти автоматизованої загрози); **таймер** (на програмування / на драфт).

## Цікавинки для курсу
- Стос однієї стихії = Power, інша стихія стирає слот — 📎 (дані-стек у слоті, правило злиття).
- Damage Card у випадковому слоті, що виконується замість команди — 🥉 (програма як мутабельна структура).
- Драфт під таймером: невзяте роздається випадково — 🌱.
- Буксирування з правилом «≥2 кроки в одній карті» і ланцюгові поштовхи з відмовою всього ланцюга — 🥉.
- Лавова стіна, що штовхає й шкодить за кожну клітину — 📎.
- Бос з власною 4-слотовою програмою, що «дозріває» до Power 3 = програш — 🥈.
- Chain Lightning по діагоналях до 6 цілей — 📎.

## Мапа на каталог
- Є: `command-program` (Command Line) · `orientation-state` (напрям меха) · `push-object` (лавова стіна, ланцюг поштовху) · `impassable-cells` (валуни, край) · `item-pickup` (кристали) · `spawn-points` (рунні клітини) · `button-toggle` (рунна клітина вимикає щити/ворота) · `key-and-door` (ворота кольору — «ключ» стихія Move-карти) · `in-round-upgrades` (схеми) · `sequential-levels` (кампанія) · `move-timer` (пісочний годинник драфту).
- **Нема** → пропозиції карток:
  - `+card-programming-registers` (з RoboRally) — слоти програми з карт.
  - `+element-stacking-power` «Карти однієї стихії в слоті стосуються, Power = висота» · game-logic/program · 📎.
  - `+slot-override-discard` «Інша стихія в слоті скидає весь стос» · game-logic/program · 🌱.
  - `+damage-cards-in-program` «Карта пошкодження вкриває слот і виконується замість команди» · game-logic/program · 🥉.
  - `+timed-card-draft` «Драфт під таймером, невзяте роздається випадково» · game-logic/opponent · 📎.
  - `+shared-team-draft` «Спільний ряд драфту для команди» · game-logic/opponent · 📎.
  - `+slot-swap-by-scrap` «Скинути карту, щоб поміняти два слоти місцями» · game-logic/program · 🌱.
  - `+stomp-on-enter` «Вхід у клітину ворога вбиває його» · entities/combat · 🌱.
  - `+towing` «Буксирування сусіднього обʼєкта ходом ≥2» · entities/move · 🥉.
  - `+lava-wall-push` «Стіна-загроза щофази штовхає всіх і шкодить» · entities/interact · 📎.
  - `+escort-objective` «Вивести вразливий обʼєкт (бомбу)» · game-logic/win · 🥉.
  - `+boss-program-line` «Бос з власною лінією команд, що підсилюється» · entities/combat · 🥈.
  - `+rune-gate-color-key` «Ворота пропускають рух лише своєї стихії» · entities/interact · 🌱.
  - `+mech-cannot-die` «Аватар не гине, шкода лише псує керування» · entities/state · 🌱.
  - `+team-kill-tracker` «Спільний лічильник вбивств → пороги нагород» · game-logic · 🌱.
  - `+schematic-unlocks` «Постійні здібності на порогах лічильника» · levels/progression · 📎.
  - `+coop-campaign-envelopes` «Кампанія із запечатаних місій з новими правилами» · levels/progression · 🥉.

## Пропозиції до словників
- `+effect:draft` — гравець бере одну карту зі спільного відкритого ряду.
- `+effect:discard` — карта / стос іде в скид.
- `+effect:draw_card` — витягти карту з колоди (тут — пошкодження).
- `+effect:roll_dice` — кинути кубик і використати результат (номер слота, напрям).
- `+effect:stack(card, slot)` — покласти карту поверх стосу того ж виду.
- `+cond:stack_power(slot, op, n)` — висота стосу в слоті (Power).
- `+effect:tow` — тягти сусідній обʼєкт за собою (відмінне від `pull`: потрібна сила ходу ≥ 2).
- `+role:card` — карта команди / пошкодження як сутність гри.
- `+role:die` — кубик / компас як джерело випадковості на столі.
- `+window:program-board` — планшет програми (слоти + стани слотів).
- `+window:draft-window` — спільний драфт з таймером.
- `+ui:program-slots` — ряд слотів зі стосами й покриттям шкодою.
- `+ui:doom-tracker` — лічильник загрози місії (бомба, HP боса).
- `+feature:sealed-mission-envelopes` — нові правила відкриваються з конвертів кампанії.

## Джерела
- ⭐ [UltraBoardGames: правила](https://www.ultraboardgames.com/mechs-vs-minions/game-rules.php) — склад гри, драфт, стоси, override, Damage Cards, фази, бомба, кристали, рунні клітини й ворота, лава, бос, Gear Tracker.
- [Wikipedia: Mechs vs. Minions](https://en.wikipedia.org/wiki/Mechs_vs._Minions) — огляд: 2–4 гравці, 60–120 хв, Command Line з 6 слотів, фази, кампанія.
- [RulesPal: rulebook](https://rulespal.com/mechs-vs-minions/rulebook) — Chain Lightning, Fuel Tank, Skewer, буксирування, бос, Minuteglass, Overdrive.
- [League of Legends: Mechs vs. Minions](https://eune.leagueoflegends.com/en/featured/mechs-vs-minions) — офіційна сторінка Riot.
- YouTube: пошук «mechs vs minions how to play».

## Непевне
- (?) Chain Lightning: UltraBoardGames — 1 ціль на Power 1, до 4 і 6 на Power 2/3; RulesPal — максимум 2/4/6.
- (?) Ремонт брухтом: в одному місці правил «6 Fire or 9 Metal», в іншому «6 Fire or Metal» — суперечність у джерелі.
- (?) Рух міньйонів за замовчуванням: RulesPal — у навчальній місії на 1 клітину за кубиком; у місіях 4 і 7 — на 2–3 клітини до цілі (з пошукових сніпетів); «до найближчого меха» не підтверджено.
- (?) Повний перелік назв Command Cards (Flamespitter, Hexmove, Scythe, Cycle, Memory Core, Aimbot тощо) і їхніх ефектів за Power — з памʼяті, у відкритих джерелах лише Blaze, Fuel Tank, Speed, Chain Lightning, Skewer, Omnistomp, Ripsaw.
- (?) Назви окремих Damage Cards і їхні ефекти — не знайдено.
- (?) Офіційної цифрової версії джерела не згадують; вікна описано як «(цифрова версія)».
