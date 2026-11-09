---
title: Warhammer Underworlds
slug: warhammer-underworlds
aka: ["Warhammer Underworlds: Shadespire", "Warhammer Underworlds: Nightvault", "Warhammer Underworlds: Beastgrave", "Warhammer Underworlds: Harrowdeep", "Warhammer Underworlds: Gnarlwood", "Warhammer Underworlds: Wyrdhollow", "Warhammer Underworlds - Shadespire Edition", WHU]
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
year: 2017
platforms: [board, PC]
links:
  - {kind: other, url: "https://rulespal.com/warhammer-underworlds/rulebook", best: true, note: "правила поточного видання (Wintermaw): 3 раунди × 4 ходи, базові здібності, кубики, Flanked/Surrounded, відкидання, Inspire, крок сили, Delve, кінець фази, перемога"}
  - {kind: steam, url: "https://store.steampowered.com/app/1022310", note: "Warhammer Underworlds - Shadespire Edition (2020): онлайн-PvP, боти, виклики, 14 ворбендів, колоди 20 + 12"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Warhammer+Underworlds+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 60
mechanics: [line-of-sight-attack, melee-vs-ranged, impassable-cells, hp-damage, hot-seat, online-multiplayer, ai-opponent, character-select, placement-screen, pocket, +hex-grid-render, +alternating-activation, +turn-limit-score, +inspire-flip, +secret-objective, +surge-scoring, +glory-spend-upgrades, +equipment-cards, +deck-building, +draw-to-hand-size, +reactive-cards, +combat-dice-symbols, +flanking, +knockback, +overrun-follow, +stand-fast, +guard-token, +charge-move-attack, +stagger-reroll, +weapon-abilities, +bounty-glory, +catch-up-initiative, +treasure-tiebreak, +delve-flip-token, +focus-redraw, +roll-off-ranking, +deployment-phase, +heal]
proposes: ["+trigger:all_passed", "+cond:flanked", "+effect:roll_dice", "+effect:flip", "+effect:draw_card", "+effect:discard", "+ui:glory-counter", "+ui:dice-tray", "+ui:fighter-card", "+window:deck-builder", "+feature:deck-construction", "+card:inspire-flip", "+axis:turn-structure:alternating-activation"]
author: opus
date: 2026-11-09
---

# Warhammer Underworlds — три раунди по чотири ходи: один боєць за хід, кубики з символами, картки цілей і боєць, що «надихається» й перевертає свою картку

## Суть
Змагальна дуельна гра Games Workshop (2017, Shadespire) у світі Age of Sigmar: у кожного гравця **ворбенд** з кількох бійців на гексовому полі й власні колоди — **12 карток цілей** і **20 карток сили** (хитрощі й покращення). Гра — рівно **3 раунди**, у кожному гравці по черзі роблять **по 4 ходи**: один боєць — одна дія (рух, атака, ривок, захист, фокус), після кожної дії — **крок сили**, де обидва по черзі грають картки. Очки — **Glory** за виконані цілі й убитих ворогів (за їхню «нагороду»), і та сама Glory — бюджет на покращення. Ключова фішка: боєць має двосторонню картку, і коли виконує **умову Inspire** зі свого варскролу, картку перевертають на золотий бік — характеристики кращають.

## Поле і час
- Гексове поле (одна дошка з двома бойовищами на боках); **територія** кожного гравця — червона чи синя половина з протилежних країв, середні гекси нейтральні.
- Спеціальні гекси: **заблоковані** (товста біла рамка) — непрохідні й закривають видимість; **stagger-гекси** (червона рамка) — дають жетон Stagger; **стартові** (символ гри) — розстановка; **крайові** — найзовнішні.
- 5 жетонів місцевості: двосторонні — скарб / укриття; кожна територія має ≥ 1; не ближче 2 гексів один до одного й не на краю (якщо можна інакше).
- Дальність — найкоротший шлях у гексах (заблоковані теж рахуються); видимість — пряма від центру до центру, заблокований гекс на ній закриває ціль.
- Час: 3 раунди × (фаза бою: 8 ходів, по 4 на гравця, кожен = крок дії + крок сили) + фаза кінця раунду.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Боєць | piece | Move, Save, Health, Bounty; зброя: Range, Dice, Damage, здібності; двостороння картка | одна базова здібність за хід; гине, коли жетонів шкоди ≥ Health |
| Боєць (Inspired) | piece | кращі характеристики (золотий бік) | стає таким за умовою Inspire; деякі — назад за умовою Uninspire |
| Варскрол ворбенду | supply | умова Inspire, здібності, трекер | задає «характер» ворбенду |
| Картка цілі (Objective) | supply | Glory, умова; Surge або в кінці фази | 3 у руці; таємна до виконання |
| Картка сили: хитрощі (ploy) | supply | ефект, тривалість; Surge — до/після події | грається в крок сили |
| Картка сили: покращення (upgrade) | supply | вартість у Glory | надягається на бійця; сума вартостей ≤ Glory ворбенду |
| Жетон місцевості: скарб | object | номер-вартість | боєць на ньому «тримає» скарб; Delve перевертає на укриття |
| Жетон місцевості: укриття | terrain | — | у кидку захисту бійця на ньому символ Surrounded — успіх |
| Заблокований гекс | static | — | непрохідний, закриває видимість |
| Stagger-гекс | hazard | — | вхід або поставлення → жетон Stagger |
| Стартовий гекс | zone | у своїй території | розстановка бійців |
| Територія | zone | червона / синя / нейтральна | розстановка, нічия за скарбами |
| Жетони Move / Charge / Guard / Stagger / шкоди | mark | — | стани бійця до кінця раунду |
| Кубики атаки (5) і захисту (3) | — | Critical, Hammer, Swords, Flanked, Surrounded / Critical, Shield, Dodge, Flanked, Surrounded | успіхи рахують за символами |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кидок за територію; переможець обирає бік поля й свою територію; інший ставить перший жетон місцевості; по черзі 5 жетонів; розстановку починає той, хто поставив останній»`; бійці — у порожні стартові гекси своєї території.
- КОЛИ `game_start` → ТО `custom: «взяти 3 цілі й 5 карток сили, один раз можна перетягнути»`.
- КОЛИ `phase_start(round)` → ТО `custom: «кидок одного кубика атаки: Critical > Swords > Hammer > Surrounded > Flanked; нічия — перекид»`; переможець ходить першим, інший бере 1 картку сили; у раундах 2–3 нічию виграє underdog (у кого сумарна Bounty вбитих своїх більша).
- КОЛИ `turn_start(player)` → ТО `custom: «крок дії: один боєць виконує одну базову здібність»`.
- КОЛИ `input(move, fighter)` → ЯКЩО `not state(fighter, moved)` and `not state(fighter, charged)` → ТО `move(fighter, adjacent_empty)` до Move гексів, `set_state(fighter, moved)`.
- КОЛИ `input(move, fighter, hex)` → ЯКЩО `cell(hex, blocked)` → ТО `block`.
- КОЛИ `input(charge, fighter, target)` → ЯКЩО `not state(fighter, moved)` and `not state(fighter, charged)` → ТО `clear_state(fighter, guard)`, `custom: «рух, потім атака»`, `set_state(fighter, charged)`.
- КОЛИ `input(any, fighter)` → ЯКЩО `state(fighter, charged)` and `custom: «не всі свої бійці мають жетон Charge»` → ТО `block` (рух, атака й захист заборонені).
- КОЛИ `input(guard, fighter)` → ТО `set_state(fighter, guard)` (лише один жетон).
- КОЛИ `input(focus)` → ТО `custom: «скинути будь-які картки, добрати стільки ж тих самих типів + 1 картку сили»`.
- КОЛИ `input(attack, fighter, target)` → ЯКЩО `line_of_sight(fighter, target)` and `in_range(fighter, target, weapon_range)` → ТО `custom: «атакер кидає Dice кубиків атаки, ціль — кубики захисту за Save; успіхи: Critical + символ зброї (Hammer чи Swords)»`.
- КОЛИ `custom: «рахуються успіхи»` → ЯКЩО `adjacent_count(target, attacker_friends, ≥, 1)` → ТО `custom: «Flanked на кубиках атаки — успіх»`.
- КОЛИ `custom: «рахуються успіхи»` → ЯКЩО `adjacent_count(target, attacker_friends, ≥, 2)` → ТО `custom: «Surrounded — теж успіх»`; так само для кубиків захисту відносно атакера.
- КОЛИ `custom: «кидок захисту»` → ЯКЩО `state(target, guard)` → ТО `custom: «Shield і Dodge — успіхи; ціль не можна відкинути»`.
- КОЛИ `custom: «кидок захисту»` → ЯКЩО `occupied(target_hex, cover_token)` → ТО `custom: «Surrounded — успіх»`.
- КОЛИ `custom: «кидок атаки»` → ЯКЩО `state(target, staggered)` → ТО `custom: «перекинути 1 кубик атаки»`.
- КОЛИ `custom: «успіхів атаки більше, ніж захисту»` → ТО `damage(target, weapon_damage)`; рівність — атака «внічию», без шкоди.
- КОЛИ `custom: «успіхів атаки ≥ успіхів захисту і ≥ 1»` → ТО `push(target)` на 1 гекс від атакера (drive back).
- КОЛИ `custom: «Critical атаки більше, ніж Critical захисту»` → ТО `custom: «після відкидання чи вбивства атакер може зсунутись у звільнений гекс (overrun)»`.
- КОЛИ `custom: «Critical захисту більше, ніж Critical атаки»` → ТО `custom: «Stand Fast: −1 Damage цієї атаки, ціль не відкидається»`.
- КОЛИ `custom: «зброя з Grievous / Cleave / Ensnare / Brutal / Grapple / Stagger»` → ТО `custom: «+1 Damage / Shield не рахується / Dodge не рахується / Flanked і Surrounded не рахуються / поштовх на 1 замість відкидання / жетон Stagger цілі»`; критичні здібності — лише при ≥ 1 Critical.
- КОЛИ `custom: «жетонів шкоди ≥ Health»` → ТО `disappear(fighter)`, `score(+bounty)` (Glory вбивці).
- КОЛИ `custom: «боєць виконав умову Inspire з варскролу»` → ТО `transform(fighter, inspired)` (картку на золотий бік).
- КОЛИ `custom: «умова Uninspire»` → ТО `transform(fighter, uninspired)`.
- КОЛИ `enter(fighter, stagger_hex)` → ТО `set_state(fighter, staggered)`; поштовх — не рух, жетона Move не дає.
- КОЛИ `turn_end(player)` → ТО `custom: «крок сили: по черзі зіграти картку сили, здібність варскролу, Delve або пас»`.
- КОЛИ `custom: «обидва поспіль пасують»` → ТО `end_turn`.
- КОЛИ `input(delve, fighter)` → ЯКЩО `occupied(fighter_hex, feature_token)` and `custom: «у цьому кроці сили ворбенд ще не робив Delve»` → ТО `custom: «перевернути жетон: скарб ↔ укриття»`, `set_state(fighter, staggered)`.
- КОЛИ `custom: «умова Surge-цілі виконана»` → ЯКЩО `has(player, surge_objective)` → ТО `score(+glory)` одразу; нову Surge-ціль до наступного ходу не зарахувати.
- КОЛИ `input(heal, fighter)` → ТО `heal(fighter, 1)` (зняти 1 жетон шкоди).
- КОЛИ `phase_start(end)` → ТО `custom: «зарахувати цілі → надягнути покращення (сума ≤ Glory) → скинути → добрати до 3 цілей і 5 карток сили»`, `clear_state(all, moved|charged|guard|staggered)`.
- КОЛИ `counter(round, =, 3)` and `custom: «кінець фази»` → ТО `custom: «більше Glory — велика перемога; інакше нічию розбивають: більше живих бійців → більша сума скарбів у своїй території → більша Bounty живих (мала перемога)»`; усе рівно — `draw`.
- Перемога: найбільше Glory після 3 раундів. · Поразка: менше Glory. · Рахунок: Glory = цілі + Bounty вбитих ворогів.

## Керування і ввід
- Настільна: кожен хід — одна дія одного бійця, далі крок сили з картками; кидки відкриті; жетони на бійцях показують стани.
- Цифрова версія (Steam, 2020): онлайн-PvP, матчі з ботами, одиночні виклики, збір колод; інтерфейс деталей не бачив.

## Вікна, меню, HUD
- `main-menu` (цифрова версія): онлайн / боти / виклики / колоди.
- `character-select`: вибір ворбенду (у цифровій — 14).
- `deck-builder`: колода сили 20 (хитрощі, покращення, закляття) + колода цілей 12.
- `placement-screen`: вибір боку поля, жетони місцевості, розстановка у стартових гексах.
- `game-screen`: гексове поле, території; `fighter-card` (двостороння: звичайний / Inspired) з жетонами Move/Charge/Guard/Stagger і шкоди; `glory-counter` обох гравців; `turn-counter` (раунд 1–3, хід 1–4); `pocket` — рука цілей і сили; `dice-tray`; `threat-range` зброї; `legal-move-highlight`.
- `lobby-window` (цифрова версія) — онлайн-матч (?).
- `end-screen`: велика / мала перемога, нічия.

## Фічі поза полем
- `deck-construction`: «Rivals»-колоди по 32 картки (12 цілей + 20 сили), у старіших сезонах — вільний збір з пулу.
- Сезони-коробки з новими полями й ворбендами, сумісні між собою.
- Цифрова версія: `online-multiplayer`, `ai-opponent-levels` (боти), виклики; косметичні нагороди (скіни, портрети колод, титули).

## Варіації й родичі
- Сезони: Shadespire (2017), Nightvault, Beastgrave, Harrowdeep, Gnarlwood, Wyrdhollow, Deathgorge, Wintermaw — поточні правила («Wintermaw rulebook») сумісні з усіма цими коробками.
- Старі видання (?): дві дошки, жетони-цілі на полі, хитрощі (gambits) і покращення за Glory під час гри; цифрова Shadespire Edition (2020) — «20 карт сили: хитрощі, покращення й закляття».
- Родичі в корпусі: [Blood Bowl](blood-bowl.md) (кубики з символами, відкидання), [HeroQuest / Space Hulk](heroquest-space-hulk.md) (Games Workshop, кубики з символами), [Summoner Wars](summoner-wars.md) і [Unmatched](unmatched.md) (колода як сила ворбенду), [Tannhäuser](tannhauser.md) (поперемінна активація).
- Осі варіацій:
  - **тривалість партії**: до знищення / **фіксовані 3 × 4 ходи** / ліміт ходів сценарію;
  - **рахунок**: убивства / **цілі з карт + Bounty** / контроль гексів;
  - **кубики**: число-поріг / **символи з умовними успіхами** (Flanked/Surrounded);
  - **зростання бійця**: досвід / **перевертання картки за умовою** / покращення-карти.

## Цікавинки для курсу
- Inspire: подієві умови («атакував», «отримав шкоду», «скарб у руках») → перевернути картку на кращі характеристики — 📎.
- Кубики з символами й умовними успіхами (Flanked/Surrounded залежно від кількості сусідів) — 📎.
- Відкидання / overrun / stand fast з порівняння кількості успіхів і критів — 🥉.
- Крок сили після кожної дії: обидва по черзі грають картки, доки двоє не пасують поспіль — 🥉 (вікно реакцій).
- Glory як і очки, і бюджет покращень — 🌱.
- Розбиття нічиєї ланцюжком (живі → скарби в території → Bounty) — 🌱.
- Розстановка жетонів з обмеженнями (≥ 1 у кожній території, не ближче 2 гексів, не на краю) — 📎.

## Мапа на каталог
- Є: `line-of-sight-attack` ↔ видимість від центру до центру · `melee-vs-ranged` ↔ Range зброї · `impassable-cells` ↔ заблоковані гекси · `hp-damage` ↔ Health і жетони шкоди · `hot-seat`, `online-multiplayer`, `ai-opponent` (цифрова) · `character-select` ↔ ворбенд · `placement-screen` ↔ розстановка · `pocket` ↔ рука карт.
- **Нема** → пропозиції карток:
  - `+inspire-flip` «Перевернути картку бійця за умовою» · entities/state · 📎 · слот {condition, uninspire: bool}.
  - `+alternating-activation`, `+turn-limit-score` (3 раунди × 4 ходи), `+reactive-cards` (крок сили).
  - `+secret-objective`, `+surge-scoring` «Ціль зараховується одразу» · game-logic/score · 🌱; `+glory-spend-upgrades`; `+equipment-cards`; `+bounty-glory`.
  - `+combat-dice-symbols`, `+flanking`, `+knockback`, `+overrun-follow`, `+stand-fast`, `+guard-token`, `+charge-move-attack`, `+stagger-reroll`, `+weapon-abilities`.
  - `+catch-up-initiative` (underdog), `+treasure-tiebreak`, `+delve-flip-token`, `+focus-redraw`, `+roll-off-ranking`, `+deployment-phase`, `+deck-building`, `+draw-to-hand-size`, `+heal`.

## Пропозиції до словників
- `+trigger:all_passed` — обидва гравці поспіль пасували (кінець кроку сили).
- `+cond:flanked` — ціль поруч із ≥ 1 / ≥ 2 іншими ворогами (умовні успіхи кубиків).
- `+effect:roll_dice` · `+effect:flip` — перевернути двосторонню картку/жетон · `+effect:draw_card` · `+effect:discard`.
- `+ui:glory-counter` — очки-бюджет; `+ui:dice-tray`; `+ui:fighter-card` — двостороння картка бійця з жетонами.
- `+window:deck-builder` — збір колод сили й цілей.
- `+feature:deck-construction` — власна колода з пулу карт.
- `+card:inspire-flip` — механіки «прокачка перевертанням за умовою» в каталозі нема.
- `+axis:turn-structure:alternating-activation` — по одній дії бійця, далі крок реакцій.

## Джерела
- ⭐ [RulesPal: Warhammer Underworlds rulebook (Wintermaw)](https://rulespal.com/warhammer-underworlds/rulebook) — колоди 12 + 20, 3 раунди × 4 ходи, крок дії й сили, Move/Charge/Guard/Focus, кубики й символи, Flanked/Surrounded, відкидання, overrun, stand fast, здібності зброї, Stagger, Delve, жетони скарб/укриття, гекси, території, Inspire, Surge, кінець фази, underdog, перемога й нічиї.
- [Steam: Warhammer Underworlds - Shadespire Edition](https://store.steampowered.com/app/1022310) — цифрова версія 2020: PvP, боти, виклики, 14 ворбендів, колоди 20 + 12, розробники Steel Sky Productions і Tin Man Games.
- YouTube: пошук «Warhammer Underworlds how to play».

## Непевне
- (?) Сторінка RulesPal — правила поточного видання (Wintermaw); правила 2017 Shadespire (дві дошки, жетони-цілі, gambits) відрізняються — описано з памʼяті, не перевірено.
- (?) Що саме визначає, чи успіх — Hammer чи Swords (символ на зброї), і як Save бійця задає кількість кубиків і символ — у переказі не сказано.
- (?) Розмір ворбенду й кількість гексів поля — у джерелі не наведено.
- (?) Конкретні умови Inspire (наприклад, «після атаки» чи «отримав шкоду») — на варскролах ворбендів, у правилах нема.
- (?) Наявність лобі й рейтингу в цифровій версії — на Steam сказано лише «online PvP».
