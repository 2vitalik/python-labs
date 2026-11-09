---
title: "Combat Commander: Europe"
slug: combat-commander-europe
aka: [CC:E, Combat Commander]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: score
year: 2006
platforms: [board]
links:
  - {kind: other, url: "https://rulespal.com/combat-commander-europe/rulebook", best: true, note: "повний текст правил: колода долі, накази, дії, події, тригери кубиків, трек часу, раптова смерть, вогонь, ближній бій, ПО, місцевість, укріплення"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Combat+Commander+Europe+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 65
mechanics: [line-of-sight-attack, melee-vs-ranged, floor-types, impassable-cells, height-levels, explode-area, hot-seat, placement-screen, help-window, +hex-grid-render, +deck-draw, +hand-limit, +card-driven-orders, +cards-as-dice, +dice-triggers, +random-event-deck, +time-track-turns, +sudden-death-roll, +opportunity-fire, +fire-groups, +command-radius, +morale-states, +suppression-pin, +rout-rally, +reroll-token, +secret-objective, +public-objectives, +exit-points, +surrender-track, +artillery-request, +smoke-screen, +minefield, +fortifications, +asymmetric-sides]
proposes: ["+trigger:card_played", "+trigger:deck_empty", "+trigger:dice_face", "+trigger:enemy_moved", "+effect:draw_card", "+effect:discard", "+effect:shuffle", "+effect:roll_dice", "+effect:interrupt", "+effect:suppress", "+effect:rally", "+effect:rout", "+effect:reroll", "+cond:in_command_radius", "+cond:posture", "+role:card", "+role:leader", "+role:weapon", "+ui:hand-of-cards", "+ui:discard-pile", "+ui:time-track", "+ui:casualty-track", "+ui:deck-counter", "+window:scenario-briefing", "+axis:turn-structure:card-driven"]
author: opus
date: 2026-11-09
---

# Combat Commander: Europe — немає фаз і фіксованої довжини: що можна наказати і коли скінчиться бій, вирішує колода долі

## Суть
Піхотний бій Другої світової на гексовій мапі, як у Squad Leader, але без фаз ходу. Кожна нація має власну колоду з 72 **карт долі**: карта — це наказ (рух, вогонь, просування, ралі…), дія, яку можна зіграти навіть у хід суперника (вогонь у відповідь, засідка, гранати), подія, випадковий гекс і **пара кубиків** — кидок у грі робиться відкриттям верхньої карти. На картах трапляються тригери «Time!», «Event!», «Sniper!», «Jammed!»: час іде стрибками, і бій закінчується раптово кидком раптової смерті, тож план руйнує рука, якої не обирав. Перемога — за переможними очками (ПО): знищення, вихід за край, контроль цілей, частина з яких секретна.

## Поле і час
- Гексова мапа сценарію з місцевістю (ліс, будинки, чагарник, поле, сад, болото, струмок, яр, пагорби) і пʼятьма **цілями** (Objectives) на кожній мапі; розмір мап — (?).
- Шари: гекс-місцевість → укріплення (окоп, траншея, дот, бункер, міни, дріт) → дим / пожежа → фішки юнітів і зброї.
- Ходу як фаз немає: гравці чергуються **Turns**, і Turn — це або кілька наказів (до ліміту Order Capability нації), або пас зі скидом карт. Час — **трек часу**: маркер просувається на тригер «Time!» або коли хтось добрав останню карту колоди.
- Прихована інформація: рука й колода кожного таємні, скид відкритий; частина цілей — секретні фішки. Випадковість — лише з карт: кубики, випадковий гекс, події.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Відділення (Squad) | piece | 4 фігурки / 10 бійців; FP, Range, Movement, Morale | рухається, стріляє, бʼється; 2 ПО супернику, якщо знищено |
| Група (Team) | piece | 2 фігурки / 5 бійців | як Squad, 1 ПО |
| Лідер (Leader) | leader | Command (у чорному гексі), Morale | активує юнітів у радіусі Command; додає Command до FP, Range, Movement, Morale відділень і груп у своєму гексі; 1 ПО + Command |
| Герой (Hero) | leader | — | лідер, що не дає ПО; може активуватись кілька разів за Turn; повертається в запас |
| Зброя (MG, міномет…) | weapon | FP, Range; біла смуга — не отримує бонус Command | несе юніт; ламається від «Jammed!», Sustained Fire, події Malfunction; зламана вдруге — знищена |
| Радіо | weapon | FP 8–13 | позамапна артилерія; одне на гравця |
| Карта долі | card | наказ · дія · подія · випадковий гекс · 2 кубики (± тригер) | грається з руки як наказ або дія; низ карти — генератор випадковості |
| Карта ініціативи | card | — | власник може скасувати останній кидок і перекинути, після чого віддає карту; у нічиїй перемагає її власник |
| Маркер часу | mark | позиція на треку | Time Advance → пересортування, раптова смерть, підкріплення, +1 ПО захиснику |
| Маркер раптової смерті | mark | клітина треку | з неї починаються кидки на кінець гри |
| Трек втрат + маркер капітуляції | zone | нумеровані клітини | знищений юніт стає на наступну клітину; дійшов до маркера — поразка |
| Ціль (Objective) | zone | ПО з фішки цілі | контролює той, хто останнім одноосібно зайняв гекс |
| Фішка цілі | mark | відкрита / секретна; накопичувальна; подвоєння | задає ПО цілей; секретні рахуються в кінці або при розкритті |
| Відкрита місцевість | terrain | Cover 0; 1 MP | бачення вільне |
| Чагарник / сад / поле | terrain | Cover 1/1/0; Hindrance 3/2/1; 2/1/1 MP | зменшує FP вогню крізь себе |
| Ліс / будинок | terrain | Cover 2 / 3; перешкода; 2 MP | блокує бачення |
| Болото / струмок | terrain | Cover 0 / −1; 3 MP | звідти не можна стріляти |
| Яр | terrain | Cover 1; 2 MP | — |
| Паркан / живопліт / мур | terrain | +1 MP за перетин | паркан — завада, живопліт і мур — перешкода (окрім суміжних з ціллю граней) |
| Пагорб | terrain | +1 MP угору; ±1 FP за висоту | лінія бачення, «сліпі» гекси |
| Пожежа (Blaze) / водна перешкода / урвище | hazard | — | непрохідні; урвище — лише просуванням для беззбройних |
| Окоп / траншея / дот / бункер | terrain | Cover 3 / 4 / 5 / 6 (+1 проти мінометів і артилерії) | укриття; у бункері чи доті нічия в ближньому бою на користь захисника |
| Міни | hazard | 6 FP | атакують, хто входить/виходить/відступає |
| Дріт | hazard | −1 FP, Range, Morale | зупиняє рух при вході й виході; звідти не стріляють |
| Дим | terrain | Hindrance 1–10 з маркера | не стекується — лишається найбільша завада |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «колода нації перетасована; рука за позицією — Attack 6, Recon 5, Defend 4»`; сценарій ставить трек часу, раптову смерть, капітуляцію, власника карти ініціативи.
- КОЛИ `turn_start(side)` → ТО `choose(orders | pass)`: кілька наказів до ліміту Order Capability або пас.
- КОЛИ `input(pass)` → ТО `custom: «скинути карти до ліміту скиду нації»`.
- КОЛИ `input(order, card)` → ЯКЩО `turn_of(side)` → ТО `custom: «відкрити й скинути карту»`, `set_state(unit, activated)` — один юніт або лідер разом з юнітами в радіусі Command; наказ виконується повністю до наступного.
- КОЛИ `turn_end(side)` → ТО `custom: «добрати до розміру руки»`.
- КОЛИ `custom: «потрібен кидок»` → ТО `custom: «відкрити верхню карту колоди, взяти 2 кубики з її кута; сума (у наведенні — добуток)»`; карта йде у скид.
- КОЛИ `custom: «на відкритій карті — Event!»` → ТО `custom: «відкрити ще карту й виконати її подію»`; Jammed! (лише на кидку вогню) → `set_state(firing_weapons, broken)`; Sniper! → `custom: «зламати один юніт у випадковому гексі чи поруч»`; Time! → `custom: «Time Advance»`. Тригер виконується до результату кидку; кидки всередині тригера тригерів не дають.
- КОЛИ `custom: «добрано останню карту колоди»` → ТО `custom: «Time Advance»`.
- КОЛИ `custom: «Time Advance»` → ТО `custom: «перетасувати колоду зі скидом»`, `custom: «кидок раптової смерті, якщо маркер на/за клітиною SD»`, `score(+1)` захиснику, `custom: «зняти 1 дим»`, `spawn_at(reinforcements, friendly_edge)` з клітини треку, `custom: «обидва можуть зіграти Dig In»`.
- КОЛИ `custom: «кидок раптової смерті < числа на клітині маркера часу»` → ТО `game_over`.
- КОЛИ `input(order, move, unit)` → ЯКЩО `free(hex)` and `not occupied(hex, enemy)` and `custom: «вистачає MP на терен»` → ТО `move(unit, hex)`; юніти з одного гекса можуть іти разом.
- КОЛИ `enter(moving_unit, hex)` → ЯКЩО `line_of_sight(enemy, moving_unit)` → ТО `custom: «суперник може зіграти дію Fire (Op Fire) активованими юнітами — один вогонь на кожну витрату MP»`; міномети й гармати не можуть.
- КОЛИ `input(order, advance, unit)` → ТО `move(unit, adjacent_hex)` — навіть у зайнятий ворогом, без вартості MP і без Op Fire; КОЛИ `custom: «після наказу в гексі обидві сторони»` → ТО `custom: «ближній бій»`.
- КОЛИ `custom: «ближній бій»` → ТО `custom: «сума FP сторони +1 за кожен юніт з FP у рамці + кидок; першим кидає неактивний»`; менший результат → `disappear(all_losers)`; рівність — гинуть обидві сторони, якщо одна не почала бій у бункері чи доті.
- КОЛИ `input(order, fire, group, target)` → ЯКЩО `line_of_sight(each, target)` and `in_range(each, target, range)` and `custom: «група — ланцюг сусідніх гексів, без гармат»` → ТО `custom: «Attack = FP групи (X+Y) ± Command, − завади, ± дії + кидок»`.
- КОЛИ `custom: «вогонь по гексу»` → ТО `custom: «для кожного юніта окремо: Defense = Morale + Cover + Command + кидок»`; Attack > Defense → `set_state(target, broken)`; рівність → рухомий ламається, нерухомий — `set_state(target, suppressed)`; Defense більший — без ефекту.
- КОЛИ `custom: «зламаний юніт ламають знову»` → ТО `disappear(unit)`, `custom: «на трек втрат; ПО супернику»`.
- КОЛИ `state_on(unit, suppressed)` → ТО `custom: «−1 FP, Range, Movement, Morale; не стріляє зброєю»`; зламаний — теж не стріляє зброєю.
- КОЛИ `input(order, recover)` → ЯКЩО `custom: «є зламаний або придушений юніт»` → ТО `clear_state(all, suppressed)`, `custom: «кидок ралі для кожного зламаного: менше Morale — ралі; рівно — придушений; більше — без змін»`.
- КОЛИ `input(order, rout, side)` → ЯКЩО `custom: «у сторони є зламаний юніт»` → ТО `custom: «кидок проти Morale: менше — нічого; рівно — придушення; більше — відступ до свого краю на різницю»`; вихід за свій край, у ворога, непрохідне чи урвище → `disappear(unit)`.
- КОЛИ `input(order, artillery_request)` → ЯКЩО `custom: «є ціле радіо й незламаний неактивований лідер»` → ТО `custom: «наведення → точність → удар»`, `explode(hex7, radio_fp)` — центральний гекс і 6 сусідів.
- КОЛИ `input(action, card)` → ЯКЩО `custom: «виконано передумову дії»` → ТО `custom: «ефект дії»` у будь-чий хід (Ambush, Assault Fire, Crossfire, Hand Grenades, Concealment, Smoke Grenades, Spray Fire, Sustained Fire…); одночасні дії — першим неактивний.
- КОЛИ `input(initiative_card)` → ТО `custom: «скасувати останній кидок разом із тригером і перекинути»`, `custom: «карта ініціативи переходить супернику»`.
- КОЛИ `custom: «юніт вийшов за ворожий край (1 MP)»` → ТО `score(+exit_vp)`, `custom: «юніт повертається на трек часу»`.
- КОЛИ `enter(unit, objective)` → ЯКЩО `custom: «в гексі лише свої»` → ТО `set_side(objective, side)`; відкриті ПО рахуються одразу, секретні — в кінці або при розкритті.
- КОЛИ `custom: «знищений юніт став на клітину маркера капітуляції»` → ТО `lose`; так само `all_gone(own_units)` → `lose`; одночасно — перемагає власник карти ініціативи.
- КОЛИ `custom: «кінець від раптової смерті або виходу останнього юніта»` → ТО `custom: «розкрити секретні цілі, порахувати ПО; більше ПО — win; 0:0 — власник ініціативи»`.
- Перемога: більше ПО на кінці або капітуляція суперника · Поразка: свій трек капітуляції чи знищення всіх · Рахунок: ПО — відділення 2, група 1, лідер 1 + Command, герой 0; вихід; цілі; подвоєння фішками.

## Керування і ввід
- Настільна: рука карт, гравець оголошує наказ, відкриває карту й активує юніт / лідера з групою; у хід суперника — грає дії з руки як реакцію (особливо Fire у відповідь на рух).
- Кидок — відкриття карти, тож кожен кидок «з'їдає» колоду й наближає Time Advance.
- Карта ініціативи — окремий жетон «перекинь», що ходить між гравцями.
- Цифрової версії не знайдено; вікна нижче — для уявної цифрової.

## Вікна, меню, HUD
- (цифрова версія) `level-select` — сценарії; `scenario-briefing` — позиції Attack/Recon/Defend, OB сторін, трек часу, раптова смерть; `match-setup` — хто кожна нація.
- `placement-screen` (цифрова версія): розстановка за сценарієм, вибір секретної цілі.
- `game-screen` (цифрова версія): гексова мапа з 5 цілями; `hand-of-cards`; `discard-pile` обох (відкритий); `deck-counter`; `time-track` з маркерами часу й раптової смерті; `casualty-track` з маркером капітуляції; рахунок ПО (`score`); `turn-indicator`; `threat-range` (дальність/лінія бачення); `message-log` подій і тригерів.
- `confirm-dialog` (цифрова версія) — реакції в хід суперника: «зіграти Op Fire?».
- `help-window` — довідка нації (Order Capability, ліміт скиду, таблиця підтримки) і таблиця місцевості.
- `end-screen` (цифрова версія): ПО, розкриті секретні цілі.

## Фічі поза полем
- `custom-rules`: сценарії + генератор випадкового сценарію (у випадковій генерації карту ініціативи отримує більше число ініціативи).
- `hotseat` на одному столі; позиції Attack / Recon / Defend як асиметричний рівень складності (розмір руки).
- Таблиця підтримки нації (додаткова зброя, радіо) — вибір перед боєм.

## Варіації й родичі
- Серія Combat Commander: Mediterranean, Pacific і «бойові пакети» — (?), у джерелах не бачив.
- Родичі в корпусі: [Memoir '44](memoir-44.md) (карта наказу обирає фланг; без реакцій суперника), паралельно в пачці — [Squad Leader](squad-leader.md) (той самий масштаб, але 8 фіксованих фаз і кубики), Undaunted: Normandy (колода = загін), [Steel Panthers](steel-panthers.md) (opportunity fire, придушення).
- Осі варіацій:
  - **що дозволено цього ходу**: усе (Squad Leader) / секція з карти (Memoir) / тип наказу з карти + реакції з руки (Combat Commander);
  - **кубик**: справжні кубики / низ карти колоди з тригерами;
  - **кінець гри**: фіксована кількість ходів / трек часу з кидками раптової смерті;
  - **вогонь у чужий хід**: захисна фаза / карта Fire як реакція на кожну витрату MP;
  - **ціль**: знищити / ПО з відкритих і секретних цілей.

## Цікавинки для курсу
- Колода як генератор випадковості: кидок = відкрити карту, тригери на картах, перетасування на Time Advance — 📎.
- Трек часу з раптовою смертю: «гра закінчиться десь між ходом N і M» — 🌱.
- Op Fire як реакція з руки на кожну витрату MP у чужому русі — 🥉 (стек реакцій, хто відповідає першим).
- Вогневі групи — ланцюг сусідніх гексів, кожен бачить ціль — 📎 (перевірка звʼязності + лінія бачення для кожного).
- Лідер активує всіх у радіусі Command і бафає свій гекс — 🌱.
- Порівняння Attack (FP + кидок) проти Defense (Morale + Cover + кидок) з трьома результатами й особливим випадком рухомої цілі — 🌱.
- Ціль з секретною фішкою і подвоєннями ПО — 🌱; AI для гри з рукою й реакціями — 🥇.

## Мапа на каталог
- Є: `line-of-sight-attack` ↔ вогонь лише з лінією бачення · `melee-vs-ranged` ↔ вогонь і ближній бій · `floor-types` ↔ таблиця місцевості · `impassable-cells` ↔ пожежа, вода, урвище · `height-levels` ↔ пагорби ±1 FP · `explode-area` ↔ артилерійський удар на 7 гексів · `hot-seat` · `placement-screen` · `help-window` ↔ аркуші націй.
- **Нема** → пропозиції карток:
  - `+card-driven-orders` «Наказ лише з карти руки» · game-logic/opponent · 📎 · слот {order_cap, discard_limit, hand_by_posture}.
  - `+cards-as-dice` «Кидок = відкрити карту колоди» · game-logic/random · 📎 · слот {dice_per_card: 2}; `+dice-triggers` — тригери на картах (Event!, Jammed!, Sniper!, Time!); `+random-event-deck`.
  - `+time-track-turns` (корпус) + `+sudden-death-roll` «Кінець гри кидком після порогу» · game-logic/win · 🌱.
  - `+opportunity-fire` — реакція на рух; `+fire-groups` «Вогнева група з ланцюга сусідніх гексів» · entities/combat · 📎.
  - `+command-radius` «Лідер активує всіх у радіусі» · entities/state · 🌱.
  - `+morale-states`, `+suppression-pin`, `+rout-rally` (Steel Panthers) — придушений → зламаний → знищений, ралі наказом.
  - `+reroll-token` «Жетон перекидання, що переходить супернику» · game-logic/random · 🌱.
  - `+secret-objective`, `+public-objectives` (корпус) — відкриті й секретні фішки цілей; `+exit-points` — ПО за вихід за край; `+surrender-track` «Трек втрат до капітуляції» · game-logic/lose · 🌱.
  - `+artillery-request`, `+smoke-screen`, `+minefield`, `+fortifications`, `+asymmetric-sides` (колоди націй), `+hex-grid-render`, `+deck-draw`, `+hand-limit`.

## Пропозиції до словників
- `+trigger:card_played` — зіграно карту наказу/дії.
- `+trigger:deck_empty` — добрано останню карту (Time Advance).
- `+trigger:dice_face` — на кидку випав тригер (Event!, Jammed!, Sniper!, Time!).
- `+trigger:enemy_moved` — ворог витратив MP на вхід у гекс у лінії бачення.
- `+effect:draw_card`, `+effect:discard`, `+effect:shuffle` — робота з колодою; `+effect:roll_dice` — кидок (тут — відкрити карту); `+effect:reroll` — скасувати й перекинути.
- `+effect:interrupt` — реакція в хід суперника; `+effect:suppress`, `+effect:rally`, `+effect:rout` — стани моралі.
- `+cond:in_command_radius` — юніт у радіусі Command лідера; `+cond:posture` — позиція сторони (Attack / Recon / Defend).
- `+role:card`, `+role:leader`, `+role:weapon`.
- `+ui:hand-of-cards`, `+ui:discard-pile`, `+ui:time-track`, `+ui:casualty-track`, `+ui:deck-counter` — скільки карт до Time Advance.
- `+window:scenario-briefing` — сценарій: позиції, OB, трек часу, цілі.
- `+axis:turn-structure:card-driven` — дозволені дії визначає рука карт; ходи без фаз.

## Джерела
- ⭐ [RulesPal: Combat Commander: Europe rulebook](https://rulespal.com/combat-commander-europe/rulebook) — колода долі (72 карти, розмір руки 6/5/4), накази O14–O23, дії A24–A41, події E42–E77, тригери кубиків, карта ініціативи, трек часу й раптова смерть, кінець гри, ПО, вогонь (Attack vs Defense), придушення й злам, лідери й радіус Command, вогневі групи, ближній бій, місцевість і укріплення.
- YouTube: пошук «Combat Commander Europe how to play».

## Непевне
- (?) Розмір і формат мап (геоморфні? скільки гексів) — у тексті правил не знайшов; лише «5 цілей на мапу».
- (?) Ралі при Recover: джерело каже «менше Morale — ралі, рівно — придушення» — чи юніт при цьому ралі, не ясно.
- (?) Order Capability і ліміт скиду кожної нації — на аркушах націй (діапазон треку 1–6), числа не бачив.
- (?) Рік 2006, видавець GMT і дизайнер Chad Jensen — з черги й памʼяті; у відкритому джерелі не підтверджено. Продовження серії (Mediterranean, Pacific) — з памʼяті.
- (?) Цифрової версії не знайшов (Wikipedia-статті нема — 404 у пошуковця черги); вікна описано як уявну цифрову.
