---
title: "Mutant Year Zero: Road to Eden"
slug: mutant-year-zero
aka: [MYZ, Mutant Year Zero, "Mutant Year Zero: Seed of Evil"]
family: tactics
also: []
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: runtime
  goal: state
year: 2018
platforms: [PC, PS4, Xbox One, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mutant_Year_Zero:_Road_to_Eden", best: true, note: "реальний час дослідження ↔ покроковий бій як у XCOM, загін 3 з 5, мутації, ліхтарик, розділення загону для засідки, Ark-хаб"}
  - {kind: official, url: "https://www.mutantyearzero.com/?p=5142", note: "розробники про стелс: вимкнений ліхтарик = стелс, тиха зброя на відбитих від групи, засідки"}
  - {kind: official, url: "https://www.mutantyearzero.com/?p=5313", note: "розробники про тактику: 2 дії, постріл завершує хід, висота, крити, ворог кличе підмогу у свій хід, Treehugger/Hog Rush"}
  - {kind: steam, url: "https://store.steampowered.com/app/760060/", note: "фічі: стелс у тінях, руйнування стін, прожектори й лінія огляду"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mutant+Year+Zero+Road+to+Eden+ambush+gameplay", note: "пошук; засідки"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, status-effects, fog-of-war, ai-opponent, inventory-items, shop-between-levels, unit-xp-skills, party-switch, reachable-highlight, path-preview, threat-range, +destructible-blocks, height-levels, difficulty-levels, save-game, map-window, +action-points, +cover-system, +hit-chance, +overwatch, +stealth-to-combat, +silent-kill, +call-reinforcements, +vision-radius, +light-toggle-stealth, +split-party, +mutation-loadout, +kill-recharge]
proposes: ["+trigger:spotted", "+trigger:combat_start", "+trigger:call_help", "+cond:hidden", "+cond:silent_weapon", "+effect:knockdown", "+effect:root", "+effect:call_help", "+ui:detection-ring", "+ui:silent-icon", "+window:ark-hub", "+axis:time-mode-switch", "+card:stealth-to-combat", "+card:silent-kill"]
author: opus
date: 2026-11-09
---

# Mutant Year Zero — підкрадаєшся в реальному часі, ставиш засідку й перемикаєш світ у покроковий бій, де тиха смерть не будить решту табору

## Суть
Три мутанти (з пʼяти доступних) ходять зруйнованою «Зоною» **в реальному часі** — без сітки ходів, з ліхтариком і стелсом. Коли гравець сам починає бій або його помітили, гра перемикається в **покрокову тактику XCOM-типу**: 2 дії, укриття, шанс влучання, Overwatch. Ядро — дві фази однієї зустрічі: розставити загін у засідку поза боєм, а в бою **вбивати відірваних ворогів тихою зброєю за один раунд**, бо вцілілий ворог у свій хід кличе підмогу.

## Поле і час
- 3D-локації з ізометричною камерою; бій іде на прихованій квадратній сітці (клітини руху, укриття, висота) (?).
- Два режими часу: **real-time** — дослідження, стелс, розставляння загону по одному; **turn** — бій, ходить весь загін гравця, потім вороги.
- Видимість: вороги мають зону помічання; прожектори і ліхтарі посилюють огляд; тінь і присід (стелс) зменшують помітність.
- Висота дає бонус до влучання; стіни й будівлі частково руйнуються.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Dux (качка) | piece | арбалет — тиха дальня зброя | снайпер загону; мутації для стелсу |
| Bormin (кабан) | piece | дробовик, HP | танк; Hog Rush — збиває ворога з ніг на 1 раунд |
| Selma | piece | вибухівка | Treehugger — корені тримають ворогів на місці 1 раунд |
| Farrow, Magnus (найм) | piece | — | ще два мутанти, вибір 3 у загін |
| Звичайний ворог (гуль, Pyro, стрілець) | enemy | HP, броня (?) | стоїть групами або патрулює; у бою — укриття й постріли |
| Шаман гулів | enemy | — | у свій хід кличе підкріплення — пріоритетна ціль |
| Tank | enemy | важкий | ривком збиває мутантів; коріння зупиняє |
| Робот / дрон | enemy | — | броня, вибухи (?) |
| Укриття | terrain | половинне / повне (?) | знижує шанс влучання |
| Висота (дах, вежа) | terrain | бонус влучання | Alpinist — дуже високий крит з висоти |
| Руйнівна стіна / будівля | object | — | руйнується вибухом |
| Прожектор / ліхтар | hazard | світло | збільшує помітність у зоні |
| Скриня / лут | pickup | скрап, артефакти, частини зброї | обмінюються в хабі на спорядження |
| Ark (хаб) | static | — | крамниці, апгрейди, мутації між вилазками |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(light_off)` → ТО `set_state(squad, stealth)` — присід, менша помітність; КОЛИ `input(light_on)` → ТО `clear_state(squad, stealth)`, видно обʼєкти, але `custom: «ліхтар приваблює увагу»`.
- КОЛИ `enter(mutant, detection_zone)` → ЯКЩО not `state(mutant, stealth)` or `custom: «надто близько»` → ТО `custom: «ворог помітив»` → `custom: «бій починається з ходу ворогів»` (?).
- КОЛИ `input(split, mutant)` → ТО `custom: «мутант рухається сам, решта стоїть»` — розставлення засідки в реальному часі.
- КОЛИ `input(ambush)` → ЯКЩО `state(squad, stealth)` → ТО `custom: «перемкнутись у покроковий режим, перший хід — гравця»`.
- КОЛИ `turn_start(player)` → ТО кожен мутант `custom: «2 дії»`.
- КОЛИ `input(move, m, cell)` → ТО `move`, −1 дія (дальший рух — 2 дії (?)).
- КОЛИ `input(shoot, m, t)` → ЯКЩО `line_of_sight(m, t)` → ТО `prob(hit)` → `damage`; `end_turn(m)` (постріл завершує хід).
- Шанс: `custom: «база зброї − укриття цілі + висота»`; крит — окремий шанс (Skull Splitter: 100 % криту, −25 % влучання; Silent Assassin: ×2 крит, поки мутант прихований).
- КОЛИ `input(shoot, m, t)` → ЯКЩО `custom: «зброя тиха»` → ТО `custom: «сусідні групи не чують»`; ЯКЩО `custom: «зброя гучна»` → ТО `custom: «постріл може підняти великі групи»`.
- КОЛИ `turn_start(enemy)` → ЯКЩО `custom: «ворог пережив раунд і не збитий з ніг»` → ТО `custom: «кличе підмогу»` (`spawn` / активація сусідньої групи).
- КОЛИ `custom: «всі вороги бою загинули і ніхто не покликав підмогу»` → ТО `custom: «повернення в реальний час, стелс збережено»`.
- КОЛИ `input(mutation, bormin, t)` (Hog Rush) → ТО `custom: «knockdown 1 раунд»` — збитий не кличе підмогу.
- КОЛИ `input(mutation, selma, area)` (Treehugger) → ТО `custom: «root 1 раунд»` — ворог не рухається.
- КОЛИ `input(molotov, m, area)` → ТО `set_state(targets, burning)` — шкода щораунду.
- КОЛИ `input(reload, m)` → ТО `custom: «важка зброя після пострілу потребує перезарядки — рух + перезарядка = без пострілу цього ходу»`.
- КОЛИ `died(enemy)` → ТО `custom: «мутації перезаряджаються вбивствами (?)»`.
- КОЛИ `input(overwatch, m)` → ТО `set_state(m, overwatch)`; КОЛИ `custom: «ворог рухається в огляді»` → ТО постріл.
- КОЛИ `input(explosive, m, area)` → ТО `damage(area)`, `custom: «руйнує стіни й укриття»`.
- Перемога (бій): усі вороги знищені. Поразка: усі мутанти впали (?); у бою — збитий мутант може бути піднятий аптечкою (?).

## Керування і ввід
- Real-time: клік по землі — рух загону (за лідером); перемикання лідера; кнопка ліхтарика; «розділити загін» — рухати по одному; клік по ворогу з засідки — почати бій.
- Бій: вибір мутанта → підсвітка руху на 1 і 2 дії; наведення на ворога → шанс влучання й шкода; кнопки зброї, мутацій, гранат, аптечок, Overwatch, End Turn.
- Мутації й спорядження міняються лише поза боєм.

## Вікна, меню, HUD
- `main-menu`: Continue, New Game (складність, Iron mode (?)), Load, Options, Exit.
- `game-screen` (дослідження): локація, портрети загону з HP, `detection-ring` навколо ворогів (?), індикатор стелсу, позначки луту.
- `game-screen` (бій): `reachable-highlight` дві зони, `cover-icon`, `hit-chance` %, `silent-icon` (тиха чи гучна зброя), `ability-buttons` мутацій, `turn-indicator`.
- `map-window` — мапа Зони з локаціями й рівнем небезпеки (?).
- `ark-hub` — Ark: крамниця (скрап → зброя, гранати, аптечки), майстер апгрейдів (частини зброї), «артефакти» → пасивні бонуси загону.
- `upgrade-window` — дерево мутацій при підвищенні рівня; `inventory-window` — спорядження кожного.
- `pause-menu`: Save, Load, Options, Quit.

## Фічі поза полем
- Спільний рівень загону, дерева мутацій кожного (1 пасивна + 2 активні слоти, міняються між боями).
- Економіка хабу: скрап, частини зброї, артефакти.
- `difficulty-presets` (3 рівні); `mode-hardcore` (Iron mode) (?); `save-slots` (?).
- DLC Seed of Evil (2019) — нові вороги й персонажі; Switch-версія 2019.

## Варіації й родичі
- Родичі: [xcom](xcom.md) (бій 1:1 — 2 дії, укриття, Overwatch; приховування в XCOM 2), [invisible-inc](invisible-inc.md) (увесь рівень стелсу), [hard-west](hard-west.md) (стелс-фаза за конусами огляду перед боєм), [phoenix-point](phoenix-point.md); Commandos/Shadow Tactics — стелс у реальному часі без покрокового бою.
- **Осі варіацій «перехід у бій»:**
  - **хто починає**: гравець із засідки (перший хід — свій) / помічений (перший хід ворогів) (?);
  - **що вирішує**: зона огляду / шум пострілу / сусідній ворог кличе підмогу;
  - **повернення**: тиха перемога → знову стелс / шумна → нова група;
  - **час**: real-time ↔ turn (MYZ) / весь рівень turn з прихованістю (XCOM 2) / лише real-time (Commandos).

## Цікавинки для курсу
- Перемикання режиму часу real-time ↔ turn на тій самій мапі — 🥈: два цикли й передача стану.
- Тиха зброя + «вцілілий кличе підмогу у свій хід» — 📎: правило, що робить фокус-вогонь обовʼязковим.
- Зона помічання з модифікаторами (ліхтар, присід, прожектор) — 📎.
- Розділення загону й розставлення засідки поза боєм — 📎.
- Контроль натовпу: knockdown/root на 1 раунд блокує «кличе підмогу» — 🌱.
- Бонус висоти до влучання і криту — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` · `status-effects` ↔ горіння, коріння, збиття · `fog-of-war` · `ai-opponent` · `inventory-items` · `shop-between-levels` ↔ Ark · `unit-xp-skills` ↔ мутації · `party-switch` ↔ розділення загону · `reachable-highlight` / `path-preview` / `threat-range` · `+destructible-blocks` (з XCOM) ↔ стіни · `height-levels` ↔ висота · `difficulty-levels` · `save-game` · `map-window`.
- **Нема** → пропозиції карток:
  - `+action-points`, `+cover-system`, `+hit-chance`, `+overwatch` (з XCOM).
  - `+stealth-to-combat` «Real-time стелс перемикається в покроковий бій» · game-logic/opponent · 🥈 · слот {first_turn: ambusher}.
  - `+silent-kill` «Тиха атака не будить сусідів» · entities/combat · 📎.
  - `+call-reinforcements` «Вцілілий ворог кличе підмогу у свій хід» · game-logic/waves · 📎.
  - `+vision-radius` (поруч із `+vision-cone`) «Коло помічання з модифікаторами світла» · entities/legality · 📎.
  - `+light-toggle-stealth` «Ліхтар: бачиш більше — помітніший» · entities/state · 🌱.
  - `+split-party` «Рух загону цілим або по одному» · entities/move · 📎.
  - `+mutation-loadout` «Слоти здібностей: 1 пасивна + 2 активні» · entities/state · 🌱.
  - `+kill-recharge` «Здібність перезаряджається вбивствами» · entities/state · 🌱.

## Пропозиції до словників
- `+trigger:spotted(a, by)` — A помічений ворогом (≈ `sighted` з XCOM, але з боку жертви) — можна злити.
- `+trigger:combat_start(by)` — перемикання в бій; `+trigger:call_help(e)` — ворог кличе підмогу.
- `+cond:hidden(a)` — A у стелсі (можна як `state(a, stealth)` ⏳); `+cond:silent_weapon(w)`.
- `+effect:knockdown(a, n)` — ціль втрачає хід (≈ `stun` ⏳ — краще злити); `+effect:root(a, n)` — не рухається, але діє; `+effect:call_help`.
- `+ui:detection-ring` — коло помічання навколо ворога; `+ui:silent-icon` — позначка тихої зброї.
- `+window:ark-hub` — хаб з крамницями між вилазками.
- `+axis:time-mode-switch` — гра має два режими часу (`time: turn` тут — лише для бою).
- `+card:stealth-to-combat`, `+card:silent-kill` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Mutant Year Zero: Road to Eden](https://en.wikipedia.org/wiki/Mutant_Year_Zero:_Road_to_Eden) — real-time ↔ покроковий бій, загін 3 з 5, мутації, ліхтарик, засідки розділенням загону, Ark, 3 рівні складності.
- [Офіційний сайт: Master the Stealthy Approach](https://www.mutantyearzero.com/?p=5142) — ліхтар = стелс, тиха зброя на відбитих, шаман кличе підмогу, Tank і коріння.
- [Офіційний сайт: in-depth tactics](https://www.mutantyearzero.com/?p=5313) — 2 дії, постріл завершує хід, висота, Skull Splitter / Silent Assassin / Alpinist, ворог кличе лише у свій хід, збитий не кличе, Molotov, 1+2 мутації.
- [Steam: Mutant Year Zero](https://store.steampowered.com/app/760060/) — стелс у тінях, прожектори й лінія огляду, руйнування.
- YouTube: пошук «Mutant Year Zero ambush gameplay».

## Непевне
- (?) Хто ходить першим, коли загін помітили (ймовірно — вороги).
- (?) Форма зони помічання (коло навколо ворога, червоний ореол) — з памʼяті; у джерелах лише «line of sight», «floodlights».
- (?) Перезарядка мутацій за кількість вбивств (а не за ходи).
- (?) Укриття половинне/повне з числами; броня ворогів — у джерелах нема.
- (?) Iron mode, ручні сейви, умова поразки — не перевірено.
- (?) Чи бій іде на явній клітинній сітці (рух XCOM-подібний, але клітини не перевірено).
