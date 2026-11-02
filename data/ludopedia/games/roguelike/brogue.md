---
title: Brogue
slug: brogue
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2009
platforms: [PC (Windows, macOS, Linux), iOS, Android, web (сервери)]
links:
  - {kind: official, url: "https://sites.google.com/site/broguegame/", best: true, note: "офіційний сайт Brian Walker: правила предметів, стелс, союзники, рідини, поради — найкращий вхід за 10 хвилин"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Brogue_(video_game)", note: "історія, версії, Brogue CE"}
  - {kind: other, url: "https://github.com/tmewett/BrogueCE", note: "Brogue: Community Edition — актуальна версія, сирці (AGPL)"}
  - {kind: wiki, url: "https://www.roguebasin.com/index.php/Brogue", note: "RogueBasin: огляд, онлайн-сервери"}
  - {kind: fandom, url: "https://brogue.fandom.com/wiki/Brogue_Wiki", note: "фан-вікі: монстри, предмети, рельєф"}
  - {kind: play, url: "http://brogue.roguelikelike.com", note: "онлайн-сервер (EU), за RogueBasin"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=brogue+ce+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-8dir, dungeon-generation, hp-damage, inventory, inventory-items, item-pickup, chase-bfs, random-walk, floor-types, environment-death, key-and-door, sequential-levels, player-death, score-records, save-single-slot, replay, console-render, gui-render, cell-click, +remembered-map, +item-identification, +hunger-clock, +permadeath, +search-hidden, +stairs-levels, +run-command, +stealth-range, +dynamic-lighting, +gas-diffusion, +fire-spread, +deep-water-drop, +captive-ally, +sneak-attack, +enchant-progression, +vault-choose-one, +throw-potion, +monster-states, +auto-explore, +split-on-hit, +steal-and-flee]
proposes: ["+trigger:noticed", "+trigger:revealed", "+cond:stealth_range", "+cond:lit", "+cond:identified", "+cond:cursed", "+effect:spread", "+effect:ignite", "+effect:identify", "+effect:steal", "+effect:drop_item", "+effect:make_ally", "+effect:enchant", "+role:stairs", "+role:altar", "+window:inventory-window", "+window:discoveries-window", "+window:log-window", "+ui:entity-sidebar", "+ui:flavor-line", "+ui:stealth-indicator", "+feature:permadeath", "+feature:auto-explore", "+feature:travel-click", "+feature:seed-input", "+axis:session=run"]
author: opus
date: 2026-11-02
---

# Brogue — Rogue, переписаний як симуляція: світло, шум, рідини й гази поширюються клітинами, а прогрес — лише предмети

## Суть
`@` спускається на 26-й поверх Підземель Долі по Амулет Йендора й повертається нагору; глибше (до 40-го) лежать люмен-камені — лише на рахунок. Ядро — **середовище як зброя**: газ розтікається по сусідніх клітинах, вогонь біжить травою, глибока вода змиває речі з рюкзака, а монстри помічають гравця за «радіусом стелсу», який залежить від світла й дій. Досвіду й рівнів нема (з 1.7.3): сила росте лише через сувої зачарування, зілля сили/життя й знайдені предмети. Мінімалістичний інтерфейс з мишею (клік — іти, наведення — опис) робить гру «роглайком, у який можна грати без довідника».

## Поле і час
- Поверх 79×29 клітин (вміщується на екран, камера статична), 26 основних + до 40 у глибині. Поверхи **постійні**: можна піднятися назад, поверх памʼятається.
- Шари клітини: підлога/рельєф (вода, лава, прірва, трава, міст) + **рідина/газ з обсягом** (concentration) + поверхня (кров, павутина, сітка) + предмет + істота. Бачене памʼятається, монстри поза полем зору — ні.
- Видимість: поле зору (тіньове лиття) **+ освітлення**: у темряві клітини видно гірше; гравець має власне світло, що тьмяніє з глибиною (?), світять гриби, лава, вогонь, деякі монстри.
- Покроково: дія = хід; базова дія 100 одиниць часу, швидкі/повільні монстри ходять частіше/рідше; середовище (гази, вогонь) оновлюється раз на хід — газ двічі.
- Генерація: кімнати різних форм (хрести, печери, кола) + «машини» (machines) — сценки-пазли: сховища з ключем, полонені, пастки-кімнати, вівтарі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Rogue `@` | player | HP, Str, ситість, радіус стелсу | рух 8 напрямків; атака входом у клітину монстра |
| Монстр (загалом) | enemy | HP, атака, швидкість, стан sleeping/wandering/hunting/fleeing | помічає гравця в радіусі стелсу → йде шляхом до нього |
| Мавпа | enemy | — | краде предмет з рюкзака й тікає |
| Рожеве желе | enemy | HP | кожен удар **ділить** його на два менших |
| Вугор (eel) | enemy | плаває | живе в глибокій воді, пірнає й виринає для удару |
| Кислотний горб (acid mound) | enemy | — | удар по ньому/від нього роз'їдає зброю/обладунок (−зачарування) |
| Гоблін-заклинач / містик | enemy | заклинання | заклинач кличе спектральні клинки; містик ставить щит союзникам |
| Турель у стіні | enemy | нерухома | стріляє з клітини стіни |
| Болотяний монстр (bog monster) | enemy | у воді/болоті | хапає й тримає під водою (?) |
| Полонений (captive) | ally | у кайданах | «звільнити?» → кілька ходів → стає союзником |
| Союзник | ally | HP, здібності | іде за гравцем, бʼється; може вчити здібності вбитих (?) |
| Підлога / трава / суха трава | terrain | горюча | прохідна; трава й мох горять |
| Мілка вода | terrain | — | прохідна; гасить вогонь (?) |
| Глибока вода | terrain | — | пливеш; щохід шанс, що **неекіпірований** предмет «пливе геть»; гасить горіння |
| Лава | hazard | — | вхід = смерть (без вогнестійкості/левітації) |
| Прірва (chasm) | terrain | — | крок у неї = падіння на поверх нижче з невеликою шкодою |
| Болото (bog/marsh) | terrain | — | сповільнює (?); з нього підіймається болотяний газ (?) |
| Двері / таємні двері | gate | прихованість | блокують зір; таємні знаходить пошук |
| Пастки (яма, вогонь, газ, сітка, затоплення, тривога) | hazard | прихована/видима | спрацьовує при вході; тривога будить поверх |
| Отруйний (caustic) газ | hazard | обсяг | розтікається; отруює — шкода щохід |
| Газ сплутаності | hazard | обсяг | рух у випадковий бік |
| Паралітичний газ | hazard | обсяг | паралізує на N ходів |
| Болотяний газ (метан) | hazard | обсяг | вибухає від вогню |
| Вогонь | hazard | — | палить істот, перекидається на горючі сусідні клітини |
| Сходи `>` `<` | static | — | перехід між поверхами |
| Ключ / клітка / вівтар | switch | звʼязаний зі сховищем | ключ відкриває сховище; «вибери 1 з N» — інші клітки закриваються |
| Bloodwort | terrain | стручки | наступ на стручок лікує |
| Зілля `!` | pickup | колір = тип (свій у кожній партії) | випити; погані — краще **кинути** (розбивається хмарою) |
| Сувій `?` | pickup | назва = тип | прочитати; зачарування — +1 до предмета назавжди |
| Посох `/` | pickup | заряди, відновлюються | ціль + ефект (вогонь, блискавка, телепорт іншого…) |
| Жезл (wand) | pickup | обмежені заряди | не відновлюється |
| Кільце / оберіг (charm) | pickup | +N | постійний ефект / ефект з перезарядкою |
| Зброя / обладунок | pickup | вимога Str, приховане ±N, руни | різні патерни атаки (спис — 2 клітини, сокира — усі сусіди, рапіра — випад) |
| Їжа | pickup | — | відновлює ситість |
| Золото | pickup | — | лише рахунок |
| Амулет Йендора / люмен-камінь | pickup | глибина 26 / 27–40 | ціль гри / бонус рахунку |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move dir)` → ЯКЩО `occupied(cell, monster)` → ТО `custom: «атака»`; ЯКЩО `free(cell)` → ТО `move(rogue, dir)`; стіна → `block`.
- КОЛИ `turn_end(player)` → ТО `custom: «stealth = 14; у темряві ÷2; у тіні ще ÷2; важкий обладунок +; щойно відпочивав/шукав ÷2; кільця стелсу −; невидимість → 1»`.
- КОЛИ `turn_start(monster)` → ЯКЩО `in_range(monster, rogue, stealth)` and `prob(p)` → ТО `set_state(monster, hunting)` (`+trigger:noticed`); сплячий — з меншим шансом (?).
- КОЛИ `contact(rogue, monster)` (атака) → ЯКЩО `state(monster, sleeping|paralyzed|unaware)` → ТО `damage(×3)`, влучання гарантоване (sneak attack).
- КОЛИ `tick` → ТО `custom: «газ: обсяг клітини = середнє по 3×3 сусідах, стохастичне округлення; тип — найбільшого сусіда»` (`+effect:spread`); швидкі гази втрачають 1 обсягу з p=50 %, звичайні — 20 %.
- КОЛИ `tick` → ЯКЩО `cell(x, fire)` → ТО `custom: «підпалити себе й 4 орто-сусідів»` (`+effect:ignite`); горюча клітина згорає (трава → попіл), негорюча — гасне.
- КОЛИ `contact(fire, methane)` → ТО `custom: «вибух — вогонь по всьому обсягу газу»`.
- КОЛИ `enter(a, deep_water)` → ТО щохід `prob(p)` → `drop_item(random non-equipped)` «…floats away»; монстр — кидає ношений предмет.
- КОЛИ `enter(a, chasm)` → ТО `custom: «падіння на поверх нижче»`, `damage(small)`.
- КОЛИ `enter(a, lava)` → ЯКЩО `not state(a, fire_immune|levitating)` → ТО `lose`/`disappear_a`.
- КОЛИ `enter(a, gas)` → ТО за типом: `damage(n)`/`set_state(poisoned)`, `set_state(confused)`, `set_state(paralyzed, n)`.
- КОЛИ `enter(rogue, trap)` → ТО `reveal(trap)` + ефект (яма → поверх нижче, вогонь, газ, сітка, затоплення кімнати, тривога → `set_state(all, hunting)`).
- КОЛИ `input(search)` → ТО 5 ходів пошуку → `reveal(secret doors/traps nearby)` з імовірністю за відстанню (?).
- КОЛИ `input(free captive)` → ЯКЩО `adjacent(rogue, captive)` → ТО кілька ходів → `make_ally(captive)`.
- КОЛИ `input(quaff|read)` → ТО ефект типу, `take(item)`; ЯКЩО `not identified(type)` → ТО `identify(type)` для всіх таких у партії.
- КОЛИ `input(equip weapon|armor|ring)` → ТО `custom: «приховане ±N і руни розкриваються після N ходів носіння»`; ЯКЩО `cursed` → не знімається.
- КОЛИ `input(read enchanting)` → ТО `enchant(item, +1)`: зброя/обладунок — ще й −1 до вимоги Str; посох/кільце — сила або заряди; знімає прокляття.
- КОЛИ `input(throw potion)` → ТО `custom: «розбивається: хмара газу/вогонь/темрява в точці падіння»` — погані зілля як гранати.
- КОЛИ `input(take item in vault)` → ТО `custom: «інші клітки сховища закриваються»` — вибір 1 з N.
- КОЛИ `contact(monster, acid_mound)` → ТО `custom: «−1 зачарування зброї/обладунку»`.
- КОЛИ `contact(rogue, monkey)` → ТО `steal(item)`, монстр тікає; вбити — предмет падає.
- КОЛИ `damage(pink_jelly)` → ТО `split(jelly)` у вільну сусідню клітину.
- КОЛИ `turn_end` → ТО `counter(nutrition, -1)`; пороги Hungry → Weak → Fainting; 0 → шкода щохід до смерті.
- КОЛИ `turn_end` → ТО `heal(rogue, regen)` повільно.
- КОЛИ `enter(rogue, stairs)` → ТО `next_level` (поверх зберігається); вихід угору з поверху 1 з Амулетом → `win`.
- КОЛИ `hp_zero(rogue)` → ТО `lose`, `window(end-screen)` з причиною смерті.
- Перемога: винести Амулет на поверхню (люмен-камені глибше — бонус). Поразка: HP = 0; смерть остаточна. Рахунок: золото (+ люмен-камені й Амулет при перемозі).

## Керування і ввід
- Три рівноправні схеми: vi-клавіші `hjklyubn`, numpad, **миша**: клік по клітині — травел найкоротшим шляхом (`indirect`), наведення — шлях-превʼю і опис клітини/монстра/предмета.
- Shift+напрямок — біг; `x` — автодослідження (йде до найближчого невідомого, підбирає предмети); `>`/`<` — травел до сходів.
- `z` — відпочити хід, `Z` — відпочивати до відновлення; `s` — пошук (5 ходів).
- Предмети: `i` інвентар, далі буква → меню дій (apply, equip, throw, drop, call); `t` кинути, `a` застосувати (?).
- `D` — список відкритих типів предметів (discoveries), `?` — довідка, `G` — тайли/ASCII (CE).
- Нижня панель кнопок (миша): Explore · Rest · Search · Menu · Inventory.

## Вікна, меню, HUD
- `main-menu` (CE): New Game · New Game with Seed · Load · View Recording · High Scores · Quit.
- `game-screen`: мапа в центрі (`console-render` кольоровими символами або тайли) + **ліва бічна панель** (`+ui:entity-sidebar`): гравець (Health, Nutrition, Str, Armor, Stealth range), далі всі видимі монстри й предмети з HP-барами і станом (Sleeping, Hunting, Ally, Fleeing); наведення на рядок підсвічує сутність на мапі. Верх — `message-log` у 3 рядки (?); низ — рядок опису клітини під курсором (`+ui:flavor-line`), глибина, кнопки дій.
- `inventory-window` — список з літерами; клік на предмет → картка опису (що відомо, ймовірності для невідомого) + дії.
- `+window:discoveries-window` — усі типи зіль/сувоїв/кілець/посохів: відомі назви й невідомі «кольори» (з частотою, CE) (?).
- `log-window` — архів повідомлень.
- `help-window` — список клавіш.
- `end-screen` — смерть/перемога з причиною й рахунком → `leaderboard` High Scores.
- `replay-window` — перегляд запису партії з керуванням швидкістю.
- Переходи: main-menu → game-screen; `i`/`D`/`?` → модалі поверх мапи; смерть → end-screen → High Scores → main-menu.

## Фічі поза полем
- `permadeath` + сейв (можна вийти й продовжити, але без скасування смерті).
- `seed-input` / `seed-display` — та сама генерація за сідом (CE: «New Game with Seed»), турніри за сідом.
- `replay` — кожна партія записується, перегляд з будь-якої миті (official: «recording and replay»).
- `leaderboard-local` High Scores; `theme-select` ASCII ↔ тайли (CE `G`).
- `auto-explore`, `travel`, `auto-rest` — QoL, що прибирає рутину роглайка.
- CE: варіанти Rapid Brogue / Bullet Brogue (коротші партії) (?).

## Варіації й родичі
- Предок — Rogue (Амулет, ідентифікація, `@`); родичі — DCSS (автодослідження), NetHack (взаємодії предметів), Cogmind і Caves of Qud (симуляція середовища).
- Форки/нащадки: Brogue CE, gBrogue, UnBrogue, Rapid Brogue; ідеї Brogue (стелс, газ) — в Rift Wizard (автор вказує Brogue серед впливів).
- Осі варіацій: **прогресія** (XP-рівні / лише предмети / мета) · **стелс** (нема / радіус шуму / світло+шум+положення) · **середовище** (статичне / рідини з обсягом / вогонь з поширенням) · **поверхи** (одноразові / постійні) · **керування** (клавіші / клік-травел / автодослідження).

## Цікавинки для курсу
- Дифузія газу: обсяг = середнє по 3×3, з розсіюванням і стохастичним округленням — 🥈 (клітинний автомат з консервацією «маси»).
- Поширення вогню травою й вибух метану — 🥉 (ланцюг правил «вогонь × горюче × газ»).
- Радіус стелсу як формула з множниками (темрява, тінь, обладунок, відпочинок) + стани монстрів sleeping/wandering/hunting — 🥉.
- Глибока вода змиває неекіпіровані предмети — 📎 (проста механіка з сильним рішенням «пливти чи ні»).
- Сховище «візьми один з N» (інші клітки закриваються) — 🌱.
- Прогресія без досвіду: лише сувої зачарування (+1 і −вимога Str) — 📎 (економіка вибору «куди вкласти»).
- Динамічне освітлення: кілька джерел світла, сумація кольорів, поріг «темно» — 🥇 (рендер + вплив на правила).
- Клік-травел з превʼю шляху + автодослідження до найближчого невідомого — 🥇 (A*/Dijkstra-карти).

## Мапа на каталог
- Є: `move-8dir` · `move-by-input` · `dungeon-generation` · `hp-damage` · `inventory` + `inventory-items` · `item-pickup` · `chase-bfs` (монстри йдуть шляхом) · `random-walk` (блукання) · `floor-types` (вода, лава, прірва, болото) · `environment-death` · `key-and-door` (ключ → сховище) · `sequential-levels` · `player-death` · `temporary-modes` (левітація, вогнестійкість, телепатія) · `round-currency` (золото) · `score-records` · `save-single-slot` · `replay` · `console-render` + `gui-render` (тайли) · `status-panel` · `keyboard-controls` · `cell-click` · `hover-highlight` · `game-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+stealth-range` «Радіус стелсу з модифікаторами» · entities/visibility · 🥉 · слоти {base, modifiers}.
  - `+dynamic-lighting` «Динамічне світло як правило видимості» · interface/render · 🥇.
  - `+gas-diffusion` «Газ з обсягом розтікається по клітинах» · entities/interact · 🥈 · слоти {dissipation}.
  - `+fire-spread` «Вогонь поширюється на горючі сусідні клітини» · entities/interact · 🥉.
  - `+deep-water-drop` «Вода змиває неекіпіровані предмети» · entities/interact · 📎 · слот {p}.
  - `+captive-ally` «Полонений → союзник» · entities/interact · 📎.
  - `+sneak-attack` «Удар по неуважному ×3» · entities/combat · 🌱.
  - `+enchant-progression` «Прогрес лише через зачарування предметів» · game-logic/economy · 📎.
  - `+vault-choose-one` «Взяв один — інші закрились» · entities/interact · 🌱.
  - `+throw-potion` «Кинутий предмет діє в точці падіння» · entities/combat · 📎.
  - `+monster-states` «Стани монстра: спить / блукає / полює / тікає» · entities/move · 🥉.
  - `+auto-explore` «Автодослідження до найближчого невідомого» · interface/input · 🥇.
  - `+split-on-hit` «Ворог ділиться від удару» · entities/combat · 📎.
  - `+steal-and-flee` «Крадіжка предмета і втеча» · entities/move · 📎.
  - Перевикористано з Rogue: `+remembered-map`, `+item-identification`, `+hunger-clock`, `+permadeath`, `+search-hidden`, `+stairs-levels`, `+run-command`.

## Пропозиції до словників
- `+trigger:noticed` — монстр помітив гравця (перехід у hunting); `+trigger:revealed` — клітину/таємні двері відкрито.
- `+cond:stealth_range` — гравець у межах радіусу стелсу монстра; `+cond:lit` — клітина освітлена; `+cond:identified`, `+cond:cursed` (як у Rogue).
- `+effect:spread` — рідина/газ розтікається по сусідах з обсягом; `+effect:ignite` — підпалити клітину; `+effect:identify`; `+effect:steal`; `+effect:drop_item` — сутність втрачає предмет на клітину; `+effect:make_ally` — сутність переходить на бік гравця (ширше за `set_side`: зберігає ШІ супутника); `+effect:enchant` — +N до предмета.
- `+role:stairs`; `+role:altar` — вівтар/постамент з правилом (комутація, воскресіння, клітка сховища).
- `+window:inventory-window`, `+window:log-window`; `+window:discoveries-window` — довідник відкритих і невідомих типів предметів.
- `+ui:entity-sidebar` — список видимих сутностей з HP і станом, звʼязаний з мапою наведенням; `+ui:flavor-line` — рядок-опис клітини під курсором; `+ui:stealth-indicator` — поточний радіус стелсу.
- `+feature:permadeath`, `+feature:auto-explore`, `+feature:travel-click` (клік → автошлях), `+feature:seed-input`.
- `+axis:session=run` — одна партія = забіг до смерті/перемоги.

## Джерела
- ⭐ [Brogue — офіційний сайт](https://sites.google.com/site/broguegame/) — мета, керування (миша/vi/numpad), предмети (зачарування, посохи, жезли, кільця, прокляття), стелс, союзники з полонених, пастки, рідини, сховища, автодослідження, replay.
- [Wikipedia: Brogue](https://en.wikipedia.org/wiki/Brogue_(video_game)) — 26 поверхів, люмен-камені, Brogue CE.
- [GitHub: Brogue CE](https://github.com/tmewett/BrogueCE) — актуальна версія, тайли `G`.
- [BrogueCE Time.c](https://raw.githubusercontent.com/tmewett/BrogueCE/master/src/brogue/Time.c) — сирці: формула стелсу, дифузія газу, вогонь, «floats away».
- [RogueBasin: Brogue](https://www.roguebasin.com/index.php/Brogue) — огляд, онлайн-сервери.
- [Brogue Wiki (fandom)](https://brogue.fandom.com/wiki/Brogue_Wiki) — довідник монстрів/рельєфу (WebFetch не відкрився, 402).
- YouTube: пошук «brogue ce gameplay».

## Непевне
- (?) Шанс помітити гравця всередині радіусу і різниця для сплячих — формула не читалась, лише `currentStealthRange()`.
- (?) Світло гравця («miner's light»), що тьмяніє з глибиною — з памʼяті.
- (?) Болото/метан: де саме виникає болотяний газ і чи сповільнює багно — з памʼяті; на сайті лише «swamp gas that explodes near fire».
- (?) Болотяний монстр (тримає під водою), здатність союзників вчити здібності вбитих — з памʼяті; сайт згадує лише «wands of empowerment».
- (?) Частоти невідомих типів у вікні discoveries, клавіші `t`/`a`, 3 рядки логу, Rapid/Bullet Brogue — з памʼяті, не перевірено.
- (?) Онлайн-сервер brogue.roguelikelike.com — з RogueBasin, живість не перевірена.
