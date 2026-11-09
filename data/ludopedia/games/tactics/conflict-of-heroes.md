---
title: Conflict of Heroes
slug: conflict-of-heroes
aka: [CoH, "Conflict of Heroes: Awakening the Bear!", "Conflict of Heroes: Storms of Steel", "Conflict of Heroes: Price of Honour", "Conflict of Heroes: Guadalcanal"]
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
year: 2008
platforms: [board, PC]
links:
  - {kind: other, url: "https://rulespal.com/conflict-of-heroes-awakening-the-bear/rulebook", best: true, note: "текст правил Awakening the Bear: 7 ОД, CAP, опортуністичні й командні дії, терен, AV/DV, hit-маркери, групи, техніка, картки дій, VP"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Conflict_of_Heroes", note: "серія, дизайнер Uwe Eickert, Academy Games, Origins 2009"}
  - {kind: steam, url: "https://store.steampowered.com/app/510320", note: "цифрова Awakening the Bear (2016); бачив у пошуку Steam, сторінку не відкривав"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Conflict+of+Heroes+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 60
mechanics: [line-of-sight-attack, melee-vs-ranged, height-levels, floor-types, impassable-cells, hot-seat, sequential-levels, placement-screen, help-window, status-panel, +hex-grid-render, +alternating-activation, +action-points, +command-points, +interrupt-reaction, +opportunity-fire, +facing-arcs, +armor-by-facing, +terrain-move-cost, +terrain-defense, +height-attack-bonus, +opposed-roll-threshold, +random-hit-counters, +rally-roll, +fire-groups, +move-group, +armor-piercing-split, +close-combat-same-hex, +hidden-setup-tokens, +smoke-screen, +entrenchment, +minefield, +indirect-fire-spotter, +deck-draw, +card-colors, +reroll-spend, +turn-limit-objectives, +variable-action-points, +solitaire-rules]
proposes: ["+trigger:action_done", "+trigger:all_passed", "+cond:in_arc", "+cond:stacked_with", "+effect:roll_dice", "+effect:draw_chit", "+effect:rally", "+role:vehicle", "+ui:cap-track", "+ui:vp-track", "+ui:hit-marker", "+ui:dice-tray", "+window:scenario-briefing", "+feature:solitaire-rules", "+feature:programmed-instruction", "+axis:turn-structure:alternating-activation"]
author: opus
date: 2026-11-09
---

# Conflict of Heroes — активуй один загін на 7 очок дій, а суперник відповідає після кожної твоєї дії

## Суть
Тактичний варгейм Uwe Eickert (Academy Games) рівня взводу–роти про Другу світову: фішки-відділення, кулемети, гармати й техніка на гексовій мапі. Замість фаз (як у Squad Leader) — **поперемінна активація**: активний гравець бере один невикористаний юніт, дає йому **7 ОД** і витрачає їх по одній дії, а **після кожної дії** суперник може відреагувати — опортуністичною дією свіжого юніта, командною дією за спільні **командні ОД (CAP)** або карткою. Вогонь — це `2d6 + FP` проти захисту фронту чи флангу, а влучання тягнуть **випадковий hit-маркер** (притиснутий, у паніці, оглушений, вбитий…). Мета — очки перемоги за знищені юніти й контроль гексів у ходи підрахунку.

## Поле і час
- Гексова мапа; терен гекса визначає **точка в центрі** гекса; розставляти юніти можна лише на повних гексах.
- Пагорби мають рівні: +1 ОД за кожен рівень підйому, **крутий схил** (два рівні в одному гексі) — +2 ОД і непрохідний для техніки. Пагорби й перешкоди рівня 1 блокують лінію бачення, гекси одразу за ними — **сліпі**.
- Лінія бачення — від центру до центру гекса; блокує гекс з блокувальним тереном; юніти лінію бачення не блокують.
- Фішка має **напрямок**: 3 передні гекси — сектор вогню й руху вперед, решта — фланг.
- **Хід (turn)**: підготовка (перевернути всі фішки на «невикористаний», відновити CAP, добрати картки, зменшити дим, артилерія, підкріплення) → кидок ініціативи 2d6 → поперемінна активність. Хід закінчується, коли **обидва гравці поспіль передали активність без жодної дії**. Тривалість сценарію (firefight) — на аркуші сценарію.
- Інформація: картки в руці таємні, приховані юніти, опційно — таємний статус hit-маркера.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Піхотне відділення | piece | вартість вогню в ОД (чорна), FP червона, дальність, вартість руху (червона — пішки), фронтальна й флангова DR (червона — неброньований) | рухається в 3 передні гекси; стріляє в секторі; у ближньому бою +4 FP |
| Кулемет / міномет / гармата | piece | як вище; міномет — непрямий вогонь | ближній бій −2 FP; міномет стріляє з коректувальником ≤ 2 гекси, по фланговій DR |
| Танк (гусеничний) | piece | синя FP (бронебійна) + червона; синя DR; синя вартість руху | вежа: вогонь поза сектором за +1 ОД без розвороту; ближній бій +4 |
| Бронеавтомобіль / вантажівка (колісні) | piece | зелена вартість руху; значок коліс | гекси відкритого й дороги — безкоштовно; вантажівка в ближньому бою −2 |
| БТР | container | 1 піший юніт | перевезеним +2 DM; перевезені не стріляють |
| Hit-маркер піхоти | mark | тип, число ралі 7/8 | тягнеться випадково з купки; змінює параметри юніта (таблиця нижче) |
| Hit-маркер техніки | mark | Destroyed, Gun Damaged, Light Damage, Immobilized, Panicked, Stunned, Suppressed | частина — «без ралі» |
| Картка дії: зелена | supply | ОД, CAP або дія | тримається таємно; грається як дія |
| Картка дії: жовта | supply | подія / очки | грається одразу |
| Картка дії: сіра | supply | зброя поза мапою (артилерія) | тримається відкрито |
| Відкритий терен / дорога | terrain | +0 ОД, +0 DM | дорога скасовує вартість терену в гексі, DM не змінює |
| Камʼяний будинок | terrain | +1 ОД, +2 DM | блокує бачення |
| Деревʼяний будинок | terrain | +1 ОД, +1 DM | блокує бачення |
| Мур | terrain | +1 ОД, +1 DM | бачення не блокує; не дає бонус ралі |
| Ліс | terrain | +1 ОД, +2 DM | блокує бачення |
| Вода | terrain | +4 ОД, −1 DM | — |
| Пагорб | terrain | +1 ОД за рівень | вищий захисник +1 DM, вогонь униз +1 FP; сліпі гекси за схилом |
| Дим | terrain | +2 DM → +1 DM | +2 блокує бачення, на початку наступного ходу стає +1 і вже не блокує |
| Окоп / бункер | terrain | DM | ставляться сценарієм |
| Поспішні укріплення | terrain | 8 ОД, +1 DM | будує юніт |
| Колючий дріт / загородження / міни | hazard | — | штраф руху; міни атакують |
| Гекс перемоги | zone | VP | контроль — за тим, хто останнім стояв у ньому сам |

Hit-маркери піхоти (7.4):

| Маркер | Ефект | Ралі |
|---|---|---|
| Pinned | не рухається й не розвертається | 7 |
| Suppressed | вогонь +1 ОД, FP −2 | 7 |
| Cowering | вогонь +2 ОД, рух +1 ОД за гекс, дальність 1, DR вища | 8 |
| Panicked | не стріляє; флангова DR вища, фронтальна нижча | 8 |
| Stunned | лише ралі | 7 |
| Unnerved | параметри ті самі; наступне влучання знищує | 7 |
| BERSERK | вогонь −1 ОД, FP +1, дальність 1, DR вища | 8 |
| KILLED! | знищено одразу | — |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(pre_turn)` → ТО `clear_state(all_units, used)`, `counter(cap, =scenario_cap − lost_units)`, `custom: «добрати картки, зменшити дим, розіграти артилерію, підготувати підкріплення»`.
- КОЛИ `phase_start(initiative)` → ТО `custom: «кожен кидає 2d6»`; вищий стає активним; нічия → перекид; CAP можуть змінити кидок.
- КОЛИ `input(activate, unit)` → ЯКЩО `turn_of(active)` and `not state(unit, used)` and `custom: «цього разу активний ще не активував юніт»` → ТО `set_state(unit, activated)`, `counter(ap, =7)` (опційно `=2d6`).
- КОЛИ `input(move, unit, hex)` → ЯКЩО `custom: «гекс — один із 3 передніх»` → ТО `move(unit, hex)`, `counter(ap, −(move_cost + terrain_cost))`; кожен гекс — окрема дія.
- КОЛИ `input(move, unit, hex)` → ЯКЩО `custom: «гекс позаду-збоку (фланг)»` → ТО `move(unit, hex)`, `counter(ap, −(move_cost + terrain_cost + 1))` (рух назад).
- КОЛИ `enter(unit, hex)` → ТО `face(unit, any)` безкоштовно.
- КОЛИ `input(pivot, unit, dir)` → ТО `face(unit, dir)`, `counter(ap, −1)` — це окрема дія.
- КОЛИ `input(move, unit, hex)` → ЯКЩО `cell(hex, steep)` and `state(unit, vehicle)` → ТО `block`.
- КОЛИ `input(fire, unit, target)` → ЯКЩО `line_of_sight(unit, target)` and `custom: «ціль у секторі 3 передніх гексів»` and `in_range(unit, target, 2 × range)` → ТО `counter(ap, −fire_cost)`, `custom: «AV = FP + 2d6 (+ до 2 CAP); DV = фронтальна DR, якщо стріляють із сектора вогню цілі, інакше флангова, + DM терену»`.
- КОЛИ `custom: «AV ≥ DV»` → ЯКЩО `not state(target, hit)` → ТО `custom: «витягти наосліп hit-маркер з купки»`, `set_state(target, hit_type)`.
- КОЛИ `custom: «AV ≥ DV»` → ЯКЩО `state(target, hit)` → ТО `disappear(target)`, `score(+unit_vp)`.
- КОЛИ `custom: «AV ≥ DV + 4»` → ТО `disappear(target)` (два влучання одразу).
- КОЛИ `input(fire, unit, target)` → ЯКЩО `in_range(unit, target, 1)` → ТО `custom: «+3 FP впритул»`; ЯКЩО `custom: «далі за дальність, до подвоєної»` → ТО `custom: «−2 FP»`.
- КОЛИ `input(fire, unit, target)` → ЯКЩО `custom: «червона FP по синій DR або синя FP по червоній DR»` → ТО `custom: «FP ділиться навпіл після всіх модифікаторів, униз»`; в одній дії — або червона, або синя.
- КОЛИ `input(fire, unit, stack)` → ТО `custom: «окремий кидок проти кожного юніта в гексі»`.
- КОЛИ `input(fire, unit, target)` → ЯКЩО `custom: «стрілець вище за ціль»` → ТО `custom: «+1 FP»`; ЯКЩО `custom: «ціль вище»` → ТО `custom: «+1 DM цілі»`.
- КОЛИ `custom: «активний виконав одну дію»` → ТО `custom: «реагуючий може: опортуністична дія, командна дія або картка; активувати юніт не може»`.
- КОЛИ `input(opportunity, unit, action)` → ЯКЩО `not state(unit, used)` and `not state(unit, activated)` → ТО `custom: «одна дія (вогонь, рух, ралі) без витрати ОД і CAP»`, `set_state(unit, used)`.
- КОЛИ `input(command, unit, action)` → ЯКЩО `counter(cap, ≥, action_cost)` → ТО `counter(cap, −action_cost)`; юніт може бути будь-яким (активованим, використаним чи свіжим), маркер «використаний» не ставиться.
- КОЛИ `input(supplement, unit)` → ЯКЩО `state(unit, activated)` → ТО `counter(cap, −n)`, `counter(ap, +n)` (1 до 1).
- КОЛИ `input(modify_roll, n)` → ЯКЩО `custom: «свій кидок, оголошено до кидка, n ≤ 2»` → ТО `counter(cap, −n)`, `custom: «+n до кидка»`; кидки суперника змінювати не можна; захисник не додає CAP до DV.
- КОЛИ `input(end_activation, unit)` або `counter(ap, =, 0)` → ТО `set_state(unit, used)`, `pass_turn`; залишок ОД згорає.
- КОЛИ `input(pass)` → ТО `pass_turn`.
- КОЛИ `custom: «обидва гравці поспіль передали активність без дій»` → ТО `end_turn`, `counter(turn, +1)`; невитрачені CAP не переносяться.
- КОЛИ `input(rally, unit)` → ЯКЩО `state(unit, hit)` and `not occupied(unit_hex, enemy)` → ТО `counter(ap, −5)`; ЯКЩО `custom: «2d6 + 1 у прикритті ≥ +1 DM (не мур) + 1 за кожного неураженого сусіда в стеку ≥ числа ралі маркера»` → ТО `clear_state(unit, hit)`.
- КОЛИ `custom: «ворожі юніти в одному гексі»` → ТО `custom: «ближній бій проти флангової DR; FP +4 піхоті, танкам, бронеавтомобілям і БТР; −2 кулеметам, гарматам, мінометам, вантажівкам і возам»`.
- КОЛИ `input(group, units)` → ЯКЩО `custom: «в одному гексі або в суміжних звʼязних гексах»` → ТО `custom: «спільний пул 7 ОД; група не в одному гексі коштує +1 CAP»`; наприкінці всі учасники `set_state(unit, used)`.
- КОЛИ `input(group_move, units)` → ТО `custom: «платять найвищу вартість руху серед учасників»`.
- КОЛИ `input(group_fire, units)` → ТО `custom: «вартість — лідера вогню, +1 FP за кожного помічника»`; суперник реагує один раз — після всієї групової дії.
- КОЛИ `custom: «прихований юніт діє, отримав влучання, у його гексі свій видимий юніт або ворог підійшов на ≤ 2 гекси до прихованого у відкритому»` → ТО `reveal(unit)`.
- КОЛИ `input(fire, mortar, target)` → ЯКЩО `custom: «свій коректувальник ≤ 2 гекси від цілі»` → ТО `custom: «непрямий вогонь по фланговій DR»`; артилерія поза мапою — із затримкою в 1 хід, накриває 7 гексів.
- КОЛИ `input(dig_in, unit)` → ЯКЩО `counter(ap, ≥, 8)` → ТО `counter(ap, −8)`, `spawn_at(hasty_defense, unit_hex)` (+1 DM).
- КОЛИ `enter(vehicle, rough_hex)` → ТО `custom: «кидок 2d6 на знерухомлення»`; ЯКЩО `custom: «кидок нижче порогу»` → ТО `set_state(vehicle, immobilized)`.
- КОЛИ `custom: «хід підрахунку зі сценарію»` → ТО `score(vp_per_controlled_hex)`; контроль — останній, хто стояв у гексі сам; обидві сторони в гексі — спірний, нічий.
- Перемога: більше VP наприкінці останнього ходу сценарію. · Поразка: менше VP. · Рахунок: VP за знищені юніти + за контроль гексів перемоги в ходи підрахунку; жовті картки теж дають VP.

## Керування і ввід
- Настільна: активний гравець оголошує дію й рухає маркер ОД на треку; суперник після кожної дії каже «реагую» або «ні»; кидки 2d6 відкриті; CAP — окремий синій трек.
- Активувати за раз можна лише **один** юніт (або групу), але дій у нього скільки дозволяють ОД + CAP; дострокове завершення — перевернути фішку.
- Hit-маркер тягнеться наосліп з купки (окремо для піхоти й техніки); опційно лежить лицем донизу, доки його ефект не знадобиться.
- Цифрова версія (Steam, 2016): ті самі дії мишею; інтерфейс не бачив.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): кампанія / сценарії / мультиплеєр (?).
- `level-select`: 10 сценаріїв-firefight Awakening the Bear, 1–5 — навчальні.
- `scenario-briefing`: мапа, розстановка, стартові CAP, картки, умови перемоги, кількість ходів.
- `placement-screen`: розстановка, приховані юніти.
- `game-screen`: гексова мапа; `action-points` (зелений трек 7 ОД), `cap-track`, `vp-track`, `turn-counter`; `hit-marker` на фішці; `selection-highlight` активованого юніта; `dice-tray`; `pocket` — рука карток дії.
- `help-window`: таблиця терену (ОД / DM / блокує бачення), таблиці hit-маркерів.
- `end-screen` (цифрова версія): VP сторін.
- Переходи: main-menu → level-select → scenario-briefing → placement-screen → game-screen → end-screen.

## Фічі поза полем
- `levels-sequential` + `programmed-instruction`: перші сценарії вводять правила поступово.
- `hotseat` на столі; від 1 до 4 гравців (мультиплеєр — розділ 24.0).
- `solitaire-rules` (25.0): рекомендовані змінні ОД і соло-картки.
- `custom-rules`: опційні правила — змінні ОД (2d6), таємний статус влучання, штраф −1 DM рухомим або «обережний рух» за +1 ОД.

## Варіації й родичі
- Серія: Awakening the Bear! (Східний фронт 1941–42; Origins 2009), Storms of Steel (Курськ 1943), Price of Honour (Польща 1939), Guadalcanal (1942). На Steam бачив Awakening the Bear і Storms of Steel (обидва 2016), Ghost Divisions.
- Родичі в корпусі: [Squad Leader](squad-leader.md) — той самий масштаб, але 8 фіксованих фаз і мораль замість ОД; [Combat Commander: Europe](combat-commander-europe.md) — накази з карт; [Undaunted: Normandy](undaunted-normandy.md) — колода як ресурс ходу; [Memoir '44](memoir-44.md) — спрощений гекс-варгейм; [Laser Squad](laser-squad.md) — очки дій і переривання.
- Осі варіацій:
  - **структура ходу**: фази (Squad Leader) / поперемінна активація з реакцією після кожної дії (CoH) / накази з карт (Combat Commander);
  - **ресурс дії**: ОД юніта / спільний пул команди / обидва (CoH: 7 ОД + CAP);
  - **результат влучання**: HP / мораль-кидок / **випадковий маркер стану** (CoH);
  - **захист**: одна DR / фронт і фланг (CoH) / броня на 6 граней (Star Fleet Battles).

## Цікавинки для курсу
- Поперемінна активація: цикл «дія активного → вікно реакції суперника → наступна дія», кінець ходу на двох пасах поспіль — 🥉 (подієвий цикл з перериваннями, а не фази).
- Два пули ресурсу: 7 ОД юніта + спільні CAP на доповнення ОД, командні дії й модифікацію кидка — 📎.
- AV/DV: `FP + 2d6` проти фронтальної або флангової DR залежно від того, чи стрілець у секторі цілі; +4 — знищення — 📎.
- Випадкові hit-маркери з купки, кожен — свій набір модифікаторів і число ралі — 📎 (таблиця станів як дані).
- Сектор вогню з 3 передніх гексів + сліпі гекси за пагорбами — 🥉.
- Групи: перевірка звʼязності юнітів у тому самому або суміжних гексах (BFS) + спільний пул — 📎.
- Контроль гекса «останній, хто стояв сам» — 🌱.

## Мапа на каталог
- Є: `line-of-sight-attack` ↔ вогонь лише по видимих · `melee-vs-ranged` ↔ ближній бій у спільному гексі · `height-levels` ↔ рівні пагорбів · `floor-types` ↔ терен з ОД і DM · `impassable-cells` ↔ крутий схил для техніки · `hot-seat` · `sequential-levels` ↔ навчальні сценарії · `placement-screen` ↔ розстановка · `help-window` ↔ таблиці · `status-panel` ↔ треки ОД/CAP/VP.
- **Нема** → пропозиції карток:
  - `+alternating-activation` (Tannhäuser) — тут з вікном реакції після кожної дії.
  - `+action-points` (25 тактик) · `+command-points` — спільний пул CAP · entities/state · 🌱.
  - `+interrupt-reaction`, `+opportunity-fire` — опортуністична дія свіжого юніта.
  - `+facing-arcs`, `+armor-by-facing` — фронтальна/флангова DR; `+height-attack-bonus` — ±1 за висоту.
  - `+opposed-roll-threshold` «AV ≥ DV, +4 — знищення» · entities/combat · 🌱.
  - `+random-hit-counters` «Влучання — випадковий маркер стану» · entities/state · 📎 · слот {pool: foot|vehicle, secret: bool}.
  - `+rally-roll` — зняти маркер кидком ≥ числа; `+fire-groups`, `+move-group` — групові дії.
  - `+armor-piercing-split` «Червона/синя FP проти червоної/синьої DR — ½» · entities/combat · 🌱.
  - `+close-combat-same-hex`, `+hidden-setup-tokens`, `+smoke-screen`, `+entrenchment`, `+minefield`, `+indirect-fire-spotter`.
  - `+deck-draw`, `+card-colors` — три кольори карток з різним таймінгом; `+reroll-spend` — CAP на ±2 до кидка; `+turn-limit-objectives`; `+variable-action-points`; `+solitaire-rules`.

## Пропозиції до словників
- `+trigger:action_done` — активний виконав одну дію (вікно реакції суперника); `+trigger:all_passed` — обидва поспіль передали активність без дій (кінець ходу).
- `+cond:in_arc` — ціль/гекс у секторі з 3 передніх гексів.
- `+cond:stacked_with` — юніти в одному гексі (група без доплати, ралі +1).
- `+effect:roll_dice` — кидок 2d6 як ефект; `+effect:draw_chit` — витягти випадковий маркер з купки; `+effect:rally` — зняти маркер стану.
- `+role:vehicle` — техніка з окремим типом руху, бронею й маркерами пошкоджень.
- `+ui:cap-track` — спільний пул командних очок; `+ui:vp-track` — очки перемоги; `+ui:hit-marker` — маркер стану на фішці; `+ui:dice-tray`.
- `+window:scenario-briefing` — аркуш сценарію (мапа, сили, CAP, умови).
- `+feature:solitaire-rules` — правила соло-гри з окремими картками; `+feature:programmed-instruction` — перші сценарії вводять правила поступово.
- `+axis:turn-structure:alternating-activation` — по одному юніту з реакцією суперника після кожної дії.

## Джерела
- ⭐ [RulesPal: Conflict of Heroes: Awakening the Bear! rulebook](https://rulespal.com/conflict-of-heroes-awakening-the-bear/rulebook) — підготовка ходу, ініціатива, 7 ОД, опортуністичні й командні дії, CAP (3.2–3.24), рух і розворот, таблиця терену, пагорби й лінія бачення, AV/DV, ±FP за дальністю, червоне/синє, hit-маркери з ефектами й ралі, групи, техніка, приховані юніти, укріплення, міномети, дим, картки, VP.
- [Wikipedia: Conflict of Heroes](https://en.wikipedia.org/wiki/Conflict_of_Heroes) — серія, дизайнер, видавці, 1–4 гравці, «простіше за ASL», 7 ОД і CAP, нагорода.
- [Steam: Conflict of Heroes: Awakening the Bear](https://store.steampowered.com/app/510320) — цифрова версія 2016 (лише з результатів пошуку Steam).
- YouTube: пошук «Conflict of Heroes how to play».

## Непевне
- (?) Значення DM рідколісся — рядок таблиці в джерелі обрізано.
- (?) Поріг кидка на знерухомлення техніки на терені «!» — у переказі «2D6 ≥ 6», чи це поріг успіху, чи провалу, — не ясно.
- (?) Скільки CAP дає сценарій і скільки ходів триває — лише «на аркуші firefight».
- (?) Вікна цифрової версії (меню, кампанія, онлайн) — інтерфейс не бачив; описано як «цифрова версія» за правилами.
- (?) Як саме юніт отримує точну зміну DR у станах Cowering / Panicked / BERSERK — на маркері, числа в тексті не наведено.
