---
title: Squad Leader
slug: squad-leader
aka: [SL, Advanced Squad Leader, ASL, Cross of Iron, Crescendo of Doom, "GI: Anvil of Victory"]
family: tactics
also: []
klass: figure
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: hidden
  random: runtime
  goal: state
year: 1977
platforms: [board, PC (VASSAL)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Squad_Leader", best: true, note: "8 фаз ходу, «design for effect», лінія бачення ниткою, геоморфні мапи 10×32, 12 сценаріїв-уроків, гаметти"}
  - {kind: other, url: "https://rulespal.com/squad-leader/rulebook", note: "текст правил: фази, IFT і модифікатори, мораль, ралі, рут, ближній бій, стек, кулемети, приховування, техніка"}
  - {kind: other, url: "https://www.tacticalwargamer.com/boardgames/squadleader/squadleader.htm", note: "огляд дизайну: фази, мораль, програмоване навчання, техніка без часткових пошкоджень"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Advanced_Squad_Leader", note: "наступник ASL 1985: кольоровий кубик, снайпер SAN, VASL"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Squad+Leader+Avalon+Hill+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 65
mechanics: [line-of-sight-attack, melee-vs-ranged, impassable-cells, floor-types, height-levels, hot-seat, online-multiplayer, sequential-levels, placement-screen, help-window, +hex-grid-render, +phase-sequence, +opportunity-fire, +combat-results-table, +terrain-defense, +point-blank-long-range, +morale-states, +rout-rally, +desperation-morale, +leader-ratings, +mg-penetration, +weapon-breakdown, +portage-weight, +stack-limit, +odds-ratio, +locked-melee, +concealment-counters, +thread-los, +smoke-screen, +minefield, +entrenchment, +modular-board, +point-buy-army, +programmed-instruction]
proposes: ["+trigger:enemy_moved", "+cond:moved_this_turn", "+cond:stacked_with", "+effect:roll_dice", "+effect:morale_check", "+effect:rally", "+effect:rout", "+effect:interrupt", "+role:leader", "+role:weapon", "+ui:phase-indicator", "+ui:fire-table", "+ui:los-thread", "+ui:dice-tray", "+window:scenario-briefing", "+feature:programmed-instruction", "+axis:turn-structure:phased"]
author: opus
date: 2026-11-09
---

# Squad Leader — взвод на гексах проходить 8 фаз ходу: стріляй, біжи під вогнем, тікай зламаним, зійдись у рукопашній

## Суть
Тактичний варгейм Avalon Hill (дизайнер John Hill) про піхотний бій Другої світової: кожна фішка — відділення (squad), лідер, кулемет чи танк на гексовій мапі, де гекс ≈ 40 м. Хід гравця — **8 фаз** у жорсткому порядку: ралі, підготовчий вогонь, рух, **захисний вогонь суперника по тих, хто щойно рухався**, вогонь у русі, втеча зламаних, просування, ближній бій. Принцип «design for effect»: будь-який обстріл дає лише знищення, перевірку моралі (і зламаний стан) або нічого — одна таблиця для всієї зброї. Гра відома **програмованим навчанням**: 12 сценаріїв, кожен додає нові правила.

## Поле і час
- **Геоморфні мапи** 10 гексів заввишки × 32 завширшки (A1…GG10), стикуються будь-яким рівним краєм (крім річкових); у базі 4 мапи. Гекс ≈ 40 м.
- Місцевість намальована на артворку, а не «цілими гексами»: ліс і будинки блокують лінію бачення лише там, де їх перетинає нитка від центру до центру; є пагорби й багатоповерхові будинки (висота, «сліпі» гекси).
- Хід гри = 2 ходи гравців × 8 фаз; номер ходу йде за треком сценарію (≈ 2 хв часу, «підігнано»). Захисний вогонь — переривання всередині руху суперника.
- Інформація: приховані фішки (concealment) — суперник бачить лише маркер; кидки 2d6 скрізь.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Відділення (squad) | piece | FP-Range-Morale, напр. 4-6-7; 4 MF | стріляє, рухається, несе 3 PP безкоштовно; зламане — перевертається |
| Елітне відділення | piece | більші FP і Morale, менша Range | як squad |
| Напіввідділення (COD/GI) | piece | половина параметрів | як squad |
| Лідер | leader | Morale + модифікатор −1…−3; 6 MF; 1 PP безкоштовно | DRM одній вогневій групі за хід, модифікатор ралі й моралі стеку; провал його моралі → стек перевіряє ще раз |
| Легкий/середній/важкий кулемет (LMG/MMG/HMG) | weapon | FP/проникнення, Range, B12 | несеться; бʼє кілька гексів уздовж лінії бачення (LMG — 2, HMG — 6–8); ламається на кидку ≥ B |
| Заряд вибухівки | weapon | 30 FP; ламається на 12 | атака впритул |
| Вогнемет | weapon | FP 20, Range 2; паливо скінчилось на ≥9 | атака по гексу |
| Panzerfaust / Bazooka (COI) | weapon | To Hit за дальністю 1–3 / 1–4 | протитанкова стрільба |
| Бронетехніка (AFV, COI) | piece | MP, броня, To Hit / To Kill | без часткових пошкоджень: лише знищення, несправність гармати, знерухомлення |
| Маркер Prep Fire | mark | — | цей юніт уже стріляв і не рухається до кінця ходу гравця |
| Маркер приховування | mark | — | ховає склад стеку; вогонь по ньому — area fire (½) |
| Відкритий терен | terrain | −2 DRM рухомим під захисним вогнем | 1 MF |
| Ліс | terrain | захист (DRM) | блокує бачення далі першого лісового гекса |
| Будинок дерев'яний / камʼяний | terrain | камʼяний +3 DRM | блокує бачення; багатоповерховий — бачення понад дахами |
| Мур / живопліт | terrain | +2 / +1 DRM | +1 MF за перетин |
| Дорога | terrain | ½ MF уздовж дороги | — |
| Пагорб | terrain | — | рух угору подвоює вартість; висота дає огляд |
| Окоп (entrenchment) | terrain | +2 проти піхоти | будується кидком 2d6 ≤ 5 у Prep Fire |
| Дріт | hazard | — | знімається кидком 2d6 ≤ FP відділення |
| Мінне поле | hazard | фактори мін | кожен фактор атакує за IFT без модифікаторів |
| Дим | terrain | +1 DRM | ставиться технікою/артилерією; знімається з часом |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(rally)` → ТО `custom: «обидва гравці ремонтують зброю й ралі зламаних»`.
- КОЛИ `input(rally, broken_squad)` → ЯКЩО `custom: «у тому ж гексі незламаний свій лідер»` → ТО `custom: «2d6 + модифікатор лідера ≤ Morale → відновлено»`; зламаний лідер ралі себе без модифікатора.
- КОЛИ `input(rally, unit)` → ЯКЩО `custom: «по юніту стріляли з минулої фази ралі»` → ТО `custom: «Desperation Morale — Morale −4»`; немодифіковані 12 → `disappear(unit)`.
- КОЛИ `input(repair, weapon)` (фаза ралі) → ТО `custom: «1d6: 1 — відремонтовано, 6 — знищено назавжди»`.
- КОЛИ `phase_start(prep_fire)` → ЯКЩО `turn_of(attacker)` → ТО `custom: «активний стріляє по ворогах у лінії бачення»`, `set_state(firer, prep_fired)` — не рухається й не стріляє до кінця ходу.
- КОЛИ `phase_start(movement)` → ЯКЩО `not state(unit, broken)` and `not state(unit, prep_fired)` → ТО `move(unit, hex)` за MF: вартість терену, +1 за мур/живопліт, ½ дорогою, ×2 угору.
- КОЛИ `custom: «лідер пройшов фазу руху в одному стеку з відділенням»` → ТО `custom: «відділення отримує +2 MF»`; КОЛИ `custom: «несе понад безкоштовні PP»` → ТО `custom: «−1 MF за кожен зайвий PP»`.
- КОЛИ `enter(moving_stack, hex)` → ЯКЩО `line_of_sight(defender, moving_stack)` → ТО `custom: «захисник може стріляти одразу (напівсиметричний метод)»`; по рухомих у відкритому — DRM −2.
- КОЛИ `phase_start(defensive_fire)` → ТО `custom: «захисник стріляє по юнітах у лінії бачення, зокрема по тих, хто щойно пройшов»`.
- КОЛИ `phase_start(advancing_fire)` → ЯКЩО `not state(unit, prep_fired)` → ТО `custom: «стріляє: хто рухався — ½ FP, хто стояв — повна FP»`; потім `clear_state(all, prep_fired)`.
- КОЛИ `input(fire, group, target)` → ЯКЩО `line_of_sight(group, target)` and `custom: «у межах подвоєної дальності»` → ТО `custom: «сума FP групи → найправіша колонка IFT, що не перевищує суму; надлишок втрачено»`.
- КОЛИ `input(fire, a, target)` → ЯКЩО `in_range(a, target, 1)` → ТО `custom: «FP ×2 (point blank)»`; ЯКЩО `custom: «далі за друковану дальність»` → ТО `custom: «FP ×½ (long range)»`; ×½ також за moving fire і area fire; множники сумуються.
- КОЛИ `custom: «кидок 2d6 на IFT»` → ТО `custom: «+DRM терену цілі (камʼяний будинок +3, мур +2, живопліт +1, окоп +2), +1 за дим, лідер −1…−3»`; результат — K/KIA (знищення) або MC (перевірка моралі з модифікатором).
- КОЛИ `custom: «MC»` → ЯКЩО `custom: «2d6 > Morale»` → ТО `set_state(unit, broken)`; ЯКЩО `state(unit, broken)` → ТО `disappear(unit)`.
- КОЛИ `custom: «у стеку перевіряють мораль»` → ТО `custom: «лідер перевіряє першим»`; ЯКЩО `custom: «лідер зламався або загинув»` → ТО `custom: «решта стеку перевіряє ще раз»`.
- КОЛИ `custom: «кулемет стріляє»` → ТО `custom: «той самий кидок діє на кожен гекс уздовж лінії бачення в межах проникнення»`.
- КОЛИ `custom: «кидок атаки ≥ числа Breakdown зброї»` → ТО `set_state(weapon, malfunctioned)`.
- КОЛИ `custom: «відділення стріляє з кулемета»` → ЯКЩО `custom: «один MG або два LMG»` → ТО `custom: «власна FP відділення не втрачається»`.
- КОЛИ `phase_start(rout)` → ЯКЩО `state(unit, broken)` → ТО `move(unit, toward_cover)` — у ліс або будинок, 4 MF (6 зі своїм лідером); першим тікає активний гравець; зламані не стріляють і не бʼються.
- КОЛИ `phase_start(advance)` → ЯКЩО `not state(unit, broken)` → ТО `move(unit, adjacent_hex)` — на 1 гекс, навіть у зайнятий ворогом.
- КОЛИ `phase_start(close_combat)` → ЯКЩО `occupied(hex, enemy)` and `occupied(hex, own)` → ТО `custom: «співвідношення FP атакера до захисника (дроби — на користь захисника) → Kill Number з таблиці; кидки одночасні»`.
- КОЛИ `custom: «після ближнього бою в гексі лишились обидві сторони»` → ТО `set_state(both, locked_in_melee)` — бʼються далі, доки одна сторона не зникне; зламані в такому гексі `disappear`.
- КОЛИ `custom: «юніт у лісі чи будинку не рухався, не стріляв, не потрапив під вогонь і не став поруч з ворогом»` → ТО `set_state(unit, concealed)`; КОЛИ `custom: «стріляє, рухається, отримав MC або поруч ворожа піхота»` → ТО `clear_state(unit, concealed)`.
- КОЛИ `custom: «кінець фази руху»` → ЯКЩО `custom: «у гексі > 4 піхотних юнітів (>3 відділень) або > 10 PP зброї однієї сторони»` → ТО `block` (у русі ліміт можна тимчасово перевищувати).
- КОЛИ `custom: «піхота атакує AFV»` → ТО `custom: «спершу перевірка моралі перед атакою (2–4 за тереном)»`; у ближньому бою відділення знищує AFV кидком ≤ FP.
- КОЛИ `custom: «AFV заїжджає в ліс або деревʼяний будинок»` → ТО `custom: «кидок на поломку (США/СРСР — 6, Німеччина — 5–6)»`; 12 на To Hit гармати → `set_state(gun, malfunctioned)`.
- КОЛИ `counter(turn, ≥, scenario_length)` → ТО `custom: «перевірити умови перемоги з картки сценарію»`.
- Перемога: умови картки сценарію (утримати будинки, вивести загін, знищити N…) · Поразка: їх не виконано · Рахунок: у Design Your Own — за таблицею очок.

## Керування і ввід
- Настільна: гравці по черзі проходять фази; кидки 2d6; лінію бачення перевіряють натягнутою ниткою між білими точками центрів гексів, спори — кидком.
- Захисник втручається під час руху: каже «стоп» і стріляє, щойно стек увійшов у гекс у його лінії бачення.
- Цифрова версія (VSQL / VASL на VASSAL): перетягування фішок, кнопки кидків, інструмент лінії бачення, чат; правил не нав'язує — гравці стежать самі.

## Вікна, меню, HUD
- (цифрова версія) `level-select`: перелік сценаріїв (1–12 у базі, офіційні серії 101–110, 201–210, 301–310…).
- `scenario-briefing` (цифрова версія): історія, умови перемоги, балансири для сторін, які мапи й фішки.
- `placement-screen`: розстановка за сценарієм; приховані юніти — під маркерами.
- `game-screen`: стиковані мапи; `phase-indicator` (8 фаз); `turn-counter` (Turn Record); `dice-tray`; `los-thread` (лінія між центрами); `selection-highlight` стеку; `message-log` / `chat-box` у мережевій грі.
- `help-window`: IFT, таблиця ближнього бою, Terrain Effects Chart — `fire-table`.
- `end-screen` (цифрова версія): виконані/провалені умови.

## Фічі поза полем
- `levels-sequential` + `programmed-instruction`: сценарій 1 — лише піхота, далі кожен сценарій додає правила (техніка, артилерія…).
- `custom-rules`: Design Your Own — сили тягнуть з колоди 52 карт і звіряють з таблицею, або купують за очки.
- `hotseat` на одному столі; `online-multiplayer` через VSQL/VASL; гаметти-розширення як `custom-rules` з новими фішками й мапами.

## Варіації й родичі
- **Cross of Iron (COI)** — розширені німецькі й радянські сили, піхота малих країн Осі, повні правила техніки («реальні дані» замість «ефекту»).
- **Crescendo of Doom (COD)** — Західний фронт 1939–41: болото, річки, великі мости, сади, три типи човнів; cowering і pinning для піхоти; напіввідділення.
- **GI: Anvil of Victory (1983)** — американці й британське спорядження (PIAT), сценарії 33–47, накладки місцевості A–O, +856 фішок; ELR — відділення «ламається до зеленого»; американців позбавили пільги на Desperation Morale.
- **Advanced Squad Leader (1985, Don Greenwood)** — повна переробка: кольоровий кубик (Rate of Fire, кулемет стріляє знову), дубль-12 — затримка кулемета, дублі при атаці — cowering на іншу колонку IFT, снайпер за Sniper Activation Number, критичне влучання на дубль-1; VASL — Java-клієнт без перевірки правил.
- Компʼютерні: «Avalon Hill's Squad Leader» (2000, MicroProse) — не повʼязана з настолкою; Close Combat і Combat Mission — натхненні ASL.
- Родичі в корпусі: [Steel Panthers](steel-panthers.md) (opportunity fire, придушення, мораль), [Laser Squad](laser-squad.md) (переривання вогнем), [Memoir '44](memoir-44.md) (спрощений гекс-варгейм), [Jagged Alliance 2](jagged-alliance-2.md); паралельно в пачці — Combat Commander: Europe (той самий масштаб, без фаз — з карт).
- Осі варіацій:
  - **структура ходу**: фіксовані фази (SL) / накази з карт (Combat Commander) / очки дій (Laser Squad);
  - **вогонь у чужий хід**: захисний вогонь по кожному входу в гекс / overwatch / нема;
  - **результат вогню**: знищення–MC–нічого (SL) / HP / придушення як шкала;
  - **лінія бачення**: нитка по намальованій місцевості / цілі гекси блокують;
  - **техніка**: без часткових пошкоджень (SL) / локації й бронювання за гранями (ASL, BattleTech).

## Цікавинки для курсу
- Скінченний автомат ходу з 8 фаз × 2 гравці, хто що може в кожній фазі — 🌱.
- IFT: сума FP → колонка «не більше суми», множники ×2/×½ з накопиченням, DRM терену й лідера → результат — 📎.
- Лінія бачення від центру до центру гекса проти полігонів намальованої місцевості, висоти й «сліпі» гекси — 🥈 (перетин відрізка з багатокутниками, а не з гексами).
- Захисний вогонь як переривання руху на кожному вході в гекс — 🥉 (рух стає кроковим процесом з подіями).
- Втеча зламаних до найближчого лісу/будинку з обмеженням MF — 🥉 (BFS з цілями-типами клітин і уникненням ворога).
- Кулемет із проникненням: один кидок на всі гекси вздовж лінії — 📎.
- Приховування: умови появи й зникнення маркера, area fire по прихованих — 📎.
- Програмоване навчання — рушій правил, що вмикає модулі за номером сценарію, — 🥉.

## Мапа на каталог
- Є: `line-of-sight-attack` ↔ вогонь лише по видимих · `melee-vs-ranged` ↔ вогонь і ближній бій у різних фазах · `impassable-cells` ↔ камʼяні будинки для техніки, ріки · `floor-types` ↔ терен з DRM і вартістю руху · `height-levels` ↔ пагорби й поверхи · `hot-seat`, `online-multiplayer` (VSQL/VASL) · `sequential-levels` ↔ 12 сценаріїв-уроків · `placement-screen` ↔ розстановка · `help-window` ↔ таблиці.
- **Нема** → пропозиції карток:
  - `+phase-sequence` «Фазовий хід» · game-logic/opponent · 🌱 · слот {phases: 8, who_acts_per_phase}.
  - `+opportunity-fire` (Steel Panthers, Laser Squad) — тут: захисний вогонь по кожному входу в гекс.
  - `+combat-results-table` (Ogre) — IFT; `+point-blank-long-range` «×2 впритул / ×½ далеко» · entities/combat · 🌱; `+terrain-defense` — DRM терену.
  - `+morale-states` / `+rout-rally` (Steel Panthers) — добрий → зламаний → знищений; втеча й ралі з лідером; `+desperation-morale` — штраф −4, якщо стріляли.
  - `+leader-ratings` — модифікатор лідера на вогонь, мораль, ралі й рух стеку.
  - `+mg-penetration` «Кулемет бʼє кілька гексів по лінії» · entities/combat · 📎 · слот {hexes}.
  - `+weapon-breakdown` «Поломка зброї на високому кидку» · entities/state · 🌱 · слот {b_number, repair: 1, lose: 6}.
  - `+portage-weight` «Вага зброї зʼїдає рух» · entities/state · 🌱; `+stack-limit` — ліміт стеку в гексі.
  - `+odds-ratio` (Ogre) — ближній бій за співвідношенням; `+locked-melee` — рукопашна триває наступні ходи.
  - `+concealment-counters` «Приховані юніти під маркером» · interface/render · 📎; `+thread-los` — лінія по намальованій місцевості.
  - `+smoke-screen`, `+minefield`, `+entrenchment`, `+modular-board` (геоморфні мапи), `+point-buy-army` (DYO), `+programmed-instruction`.

## Пропозиції до словників
- `+trigger:enemy_moved` — ворог увійшов у гекс у лінії бачення (захисний вогонь).
- `+cond:moved_this_turn` — юніт рухався в цьому ході (½ FP у Advancing Fire, −2 DRM у відкритому).
- `+cond:stacked_with` — у тому ж гексі є сутність виду (лідер для ралі, бонус +2 MF).
- `+effect:roll_dice` — кинути 2d6 як ефект; `+effect:morale_check` — перевірка моралі з переходом у «зламаний».
- `+effect:rally` — повернути зламаний юніт у стрій; `+effect:rout` — примусова втеча до укриття.
- `+effect:interrupt` — дія суперника посеред чужого руху.
- `+role:leader` — фігура, що модифікує стек; `+role:weapon` — предмет-зброя, яку несуть і передають.
- `+ui:phase-indicator` — поточна з 8 фаз; `+ui:fire-table` — довідкова таблиця вогню; `+ui:los-thread` — інструмент лінії бачення; `+ui:dice-tray` — результат кидка 2d6.
- `+window:scenario-briefing` — картка сценарію: історія, умови перемоги, балансири.
- `+feature:programmed-instruction` — правила відкриваються поступово від сценарію до сценарію.
- `+axis:turn-structure:phased` — хід гравця з фіксованих фаз, частина з них — для суперника.

## Джерела
- ⭐ [Wikipedia: Squad Leader](https://en.wikipedia.org/wiki/Squad_Leader) — 8 фаз, «design for effect», лінія бачення від центру до центру ниткою, мапи 10×32 (A1–GG10), лідери, кулемети з проникненням, 12 сценаріїв-уроків, DYO з колоди 52 карт, гаметти, VSQL.
- [RulesPal: Squad Leader rulebook](https://rulespal.com/squad-leader/rulebook) — опис фаз, параметри фішок (4-6-7, 4/6 MF, B12), рух і портаж, IFT і множники, DRM, мораль і ралі (Desperation −4), рут, ближній бій за співвідношенням, стек 4/3/10 PP, приховування, базука/фауст, AFV, окопи, дріт, міни, дим.
- [Tactical Wargamer: Squad Leader](https://www.tacticalwargamer.com/boardgames/squadleader/squadleader.htm) — огляд дизайну, програмоване навчання, техніка без часткових пошкоджень, ELR у GI.
- [Wikipedia: Advanced Squad Leader](https://en.wikipedia.org/wiki/Advanced_Squad_Leader) — ASL 1985, кольоровий кубик, SAN-снайпер, VASL і компʼютерні родичі.
- YouTube: пошук «Squad Leader Avalon Hill how to play».

## Непевне
- (?) Точний перелік колонок IFT (1 … 36+?) і позначення результатів (K / KIA / «#MC») — у джерелі уривками; таблиця не відтворена.
- (?) Повна Terrain Effects Chart (вартість лісу й будинку для піхоти, DRM лісу) — RulesPal посилається на таблицю, якої в тексті нема.
- (?) Чи всі 4 базові мапи називаються Urban / Hill / Village / Rural — так у Wikipedia; номери мап 1–4 з памʼяті.
- (?) Як саме сценарій рахує перемогу за замовчуванням і скільки триває — лише «на картці сценарію».
- (?) Вікна VASL/VSQL — з опису Wikipedia (кидки, лінія бачення, таблиці, запис ходів), інтерфейс не бачив.
