---
title: Mega Man Battle Network (Rockman.EXE)
slug: mega-man-battle-network
aka: [Rockman.EXE, MMBN, Battle Network, BN, Мегамен Батл Нетворк]
family: tower-lanes
also: [tactics]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2001
platforms: [GBA, WonderSwan Color, DS, Wii U VC, Switch, PS4, PC (Legacy Collection 2023)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mega_Man_Battle_Network", best: true, note: "серія: поле 6×3 на дві половини, Custom Gauge, папка чипів, класи Standard/Mega/Giga, Program Advance, сиквели"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mega_Man_Battle_Network_(video_game)", note: "BN1: 5 випадкових чипів за хід, вибір за назвою або кодом, папка 30, 5 елементів, NetBattle на чип"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mega_Man_Battle_Network_2", note: "BN2: код *, Styles, 3 папки, ліміти 5/5"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mega_Man_Battle_Network_3", note: "BN3: Navi Customizer, ліміти Standard/Mega/Giga, PA з 3–4 чипів, поля NetBattle"}
  - {kind: other, url: "https://en.wikibooks.org/wiki/Mega_Man_Battle_Network/Combat_Basics", note: "Wikibooks: червоні/сині панелі, типи панелей, бастер і заряд"}
  - {kind: other, url: "https://en.wikibooks.org/wiki/Mega_Man_Battle_Network/Printable_version", note: "Wikibooks: Custom+1/+2, PA за порядком і кодами, Navi Customizer, Soul"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mega+Man+Battle+Network+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-4dir, hp-damage, projectile-shot, shoot-forward, line-of-sight-attack, floor-types, inertia-slide, cell-transform, impassable-cells, destroy-all-enemies, player-death, temporary-modes, polyomino-placement, world-map, shop-catalog, codex-window, save-game, game-screen, +deck-draw, +hand-select-by-code, +program-advance, +split-field-halves, +panel-steal, +charge-shot, +damage-type-wheel, +folder-limits, +random-encounter, +ante-chip-versus, +panel-regen, +placement-bug-rule, +form-change, +chip-trader, +indirect-command-mode]
proposes: ["+effect:draw_cards", "+trigger:gauge_full", "+cond:same_code", "+role:card", "+role:panel", "+window:custom-screen", "+window:deck-builder", "+ui:custom-gauge", "+ui:chip-queue", "+feature:card-collection", "+feature:ante-versus", "+axis:field=split-halves"]
author: opus
date: 2026-11-09
---

# Mega Man Battle Network — дуель у реальному часі на полі 6×3: свої 9 клітин, чужі 9, атаки — чипи з власної колоди

## Суть
MegaMan.EXE стоїть на своїй половині поля 6×3 і в реальному часі бігає між 9 клітинами, стріляє бастером уздовж рядка й ухиляється від атак вірусів на чужій половині. Головна сила — **Battle Chips**: перед боєм гравець збирає папку (колоду) з 30 чипів, а щоразу, коли заповнюється Custom Gauge, гра зупиняється й видає 5 випадкових чипів; брати можна лише чипи з однаковою назвою або однаковою літерою-кодом. Сума «колодобудування + action на двох половинах поля» — джерело цілого піджанру (One Step From Eden); поле з двома сторонами і власником кожної панелі роблять гру межею `tower-lanes` і `tactics`.

## Поле і час
- Бій — сітка 6×3 = 18 панелей; кожна має червону або синю рамку (власник). MegaMan завжди на червоних 3×3 зліва, вороги — на синіх 3×3 справа; на чужу панель ступити не можна.
- Противники — до трьох вірусів або бос-Navi з перешкодами (камені).
- Час безперервний: рух і стрільба — real-time; Custom Gauge повільно заповнюється, і коли гравець відкриває Custom Screen, бій **зупиняється** на вибір чипів — гібрид real-time і «ходу».
- Поза боєм — два світи: реальний світ (Лан ходить містом, говорить з NPC, читає пошту, купує) і Мережа (MegaMan ходить розгалуженими шляхами, бої — випадкові зустрічі). Завдання в одному світі відкривають прохід в іншому.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| MegaMan.EXE | player | HP, бастер (атака, швидкість, заряд) | рух на 1 панель у межах своїх 9; бастер бʼє першого в рядку; HP 0 → game over |
| Вірус | enemy | HP, елемент, патерн атак | живе на синіх панелях, атакує за своїм патерном; HP 0 → видалений |
| Бос-Navi | boss | HP, елемент | сильний противник з кількома атаками й перешкодами |
| Перешкода (RockCube тощо) | object | HP | займає панель, блокує постріли й рух |
| Battle Chip | card (`+role:card`) | назва, літера-код A–Z або `*`, шкода, елемент | одноразова дія в бою: атака, виклик Navi, лікування, зміна/руйнування панелей |
| Navi-чип | card | — | викликає іншого Navi, що бʼє і зникає |
| Program Advance | card | рецепт з 3–4 чипів | комбінація в черзі → один сильний удар або ефект на кілька секунд |
| Папка (folder) | supply | 30 чипів | колода бою; випадкові 5 щоходу |
| Мішок (sack) | supply | без ліміту | запас чипів поза папкою, міняється поза боєм |
| Звичайна панель | terrain (`+role:panel`) | сторона red/blue | можна стояти власнику |
| Тріснута (cracked) | terrain | — | ламається, коли з неї зійти |
| Зламана (broken) | static | таймер | непрохідна, з часом відновлюється в звичайну |
| Діра (hole) | static | — | непрохідна назавжди, з початку бою |
| Трава (grass) | terrain | — | вогняна атака по тому, хто на траві, — ×2 і трава зникає; Wood-сутності лікуються |
| Лід (ice) | terrain | — | ковзання до стіни або не-льоду |
| Вогонь/лава | hazard | шкода | шкодить, хто ступив, і зникає |
| Отрута (poison) | hazard | — | поступово знімає HP, ігнорує Barrier і Invis |
| Метал (metal) | terrain | — | не тріскається; змінюють лише чипи «зміни поля» |
| Свята (holy) | terrain | — | хто стоїть, отримує половину шкоди (?) |
| Програми Navi Customizer (BN3+) | tile | форма-блок, колір | розкладаються на сітці; неправильна розкладка → баг |
| Style / Soul / Cross / Beast (BN2–6) | — | елемент | форма MegaMan з іншими атаками й слабкостями |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move, dir)` → ЯКЩО `free(target_panel)` and `custom: «панель червона (своя)»` → ТО `move(megaman, dir)`; інакше `block`.
- КОЛИ `enter(a, ice)` → ТО `slide(a, dir)` до стіни або не-льоду.
- КОЛИ `leave(a, cracked)` → ТО `set_cell(panel, broken)`.
- КОЛИ `enter(a, broken|hole)` → ТО `block`; КОЛИ `custom: «минув час відновлення»` → ТО `set_cell(broken, normal)`.
- КОЛИ `enter(a, lava)` → ЯКЩО `not custom: «є Barrier / правильний тип»` → ТО `damage(a, n)`, `set_cell(lava, normal)`.
- КОЛИ `tick` → ЯКЩО `occupied(poison_panel, a)` → ТО `hp(a, -n)`.
- КОЛИ `contact(fire_attack, a)` → ЯКЩО `cell(under_a, grass)` → ТО `damage(a, ×2)`, `set_cell(grass, normal)`.
- КОЛИ `contact(attack, a)` → ЯКЩО `cell(under_a, holy)` → ТО `custom: «шкода ×½»`.
- КОЛИ `input(B)` → ЯКЩО `line_of_sight(megaman, enemy)` → ТО `damage(enemy, buster_atk)` — першому в рядку.
- КОЛИ `custom: «B утримано до кінця заряду»` → ТО `damage(enemy, charged_atk)`.
- КОЛИ `tick` → ТО `counter(custom_gauge, +1)`; КОЛИ `counter(custom_gauge, ==, full)` → ТО `custom: «можна відкрити Custom Screen»`.
- КОЛИ `input(open_custom)` → ЯКЩО `counter(custom_gauge, ==, full)` → ТО `window(custom-screen)`, `custom: «бій на паузі»`, `custom: «effect draw_cards: 5 випадкових з папки»`; на старті бою — те саме без чекання.
- КОЛИ `input(select, chip)` → ЯКЩО `same(chip, selected, name)` or `custom: «cond same_code: та сама літера»` or `custom: «код * — джокер (BN2+)»` → ТО `custom: «чип у чергу»`; інакше `block`.
- КОЛИ `input(ok)` → ЯКЩО `custom: «у черзі чипи PA-рецепта в потрібному порядку й кодах»` → ТО `merge(chips → program_advance)`; у BN5 — `first_time` за бій.
- КОЛИ `input(ok)` → ТО `set_value(custom_gauge, 0)`, `window(game-screen)`; невибрані чипи повертаються в папку.
- КОЛИ `input(A)` → ЯКЩО `count(chip_queue, >, 0)` → ТО `use(megaman, top_chip)`, `disappear(chip)` до кінця бою (з папки не губиться).
- КОЛИ `contact(attack, enemy)` → ЯКЩО `custom: «елемент атаки — слабкість цілі»` → ТО `damage(enemy, ×2)`.
- КОЛИ `use(megaman, navi_chip)` → ТО `spawn(navi)`, `custom: «удар Navi»`, `disappear(navi)`.
- КОЛИ `use(megaman, panel_chip)` → ТО `set_cell(panels, grass|ice|lava|…)` (WoodPwdr → трава, IceStage → увесь лід).
- КОЛИ `use(megaman, area_grab)` → ТО `set_side(enemy_column, red)` (?) — поле гравця росте за рахунок чужого.
- КОЛИ `hp_zero(virus)` → ТО `disappear(virus)`; КОЛИ `all_gone(virus)` → ТО `win`, `window(end-screen)` з нагородою.
- КОЛИ `hp_zero(megaman)` → ТО `lose`, `game_over`.
- КОЛИ `custom: «крок MegaMan по Мережі»` → ЯКЩО `prob(p)` → ТО `custom: «випадкова зустріч → бій»`; SubChip SneakRun знижує частоту (BN2+).
- КОЛИ `input(save_folder)` → ЯКЩО `custom: «рівно 30 чипів і ліміти копій виконано»` → ТО `custom: «папка активна»`; інакше `block`.
- КОЛИ `hp_zero(loser)` → ЯКЩО `mode(real_netbattle)` → ТО `take(loser, random_chip)`, `give(winner, chip)`; `mode(practice)` — без втрат.
- КОЛИ `input(run_navicust)` → ЯКЩО `custom: «порушено правило розкладки програм»` → ТО `set_state(megaman, bug)` (BN3+).
- КОЛИ `input(sacrifice, chip)` → ТО `set_state(megaman, soul_unison)` (BN4–5); `custom: «Cross — будь-коли»` (BN6).
- КОЛИ `contact(weak_element_attack, megaman)` → ЯКЩО `state(megaman, cross)` → ТО `clear_state(megaman, cross)` (BN6).
- КОЛИ `input(beast_out)` → ТО `set_state(megaman, beast, dur)` (BN6, обмежений час).
- Перемога: видалити всіх вірусів/боса · Поразка: HP MegaMan = 0 → game over · Рахунок: оцінка бою (Busting Level) і нагорода (?).

## Керування і ввід
- Хрестовина — рух на 1 панель у межах 3×3; B — бастер, утримання B — заряджений постріл; A — використати перший чип черги.
- L/R (коли Custom Gauge повна) — Custom Screen: курсором вибрати до 5 чипів за правилом «одна назва або один код», OK — у бій.
- Поза боєм: прямий рух аватара (Лан у місті / MegaMan у Мережі), PET-меню для папки, пошти, збереження.
- Rockman.EXE 4.5 Real Operation: GBA — це PET, гравець **дає команди** Navi, а не керує ним — режим непрямого керування.

## Вікна, меню, HUD
- `game-screen` (бій): поле 6×3, `hp-bar` MegaMan (число), `+ui:custom-gauge` угорі, `+ui:chip-queue` над головою MegaMan і назва поточного чипа, HP вірусів під ними (?).
- `+window:custom-screen`: 5 (з апгрейдами до 8–10) випадкових чипів з кодами, слоти вибраних, кнопка OK; у BN4 зі Search Soul — SHUFFLE.
- `+window:deck-builder` (Folder): папка 30 ↔ мішок; кілька папок з BN2, лише одна активна.
- `codex-window` (Chip Library): усі знайдені чипи за номерами; з BN4 чужі Mega-чипи з обміну — «Secret Chips».
- `game-screen` поза боєм: місто / Мережа (вузли й гілки); PET-меню; `shop-window` (крамниці, Chip Trader); `end-screen` бою з нагородою; game over.
- `lobby-window` / `match-setup` NetBattle: Practice / Real; поля Lightweight / Midweight / Heavyweight (BN3).
- `custom-window` Navi Customizer (BN3+): сітка, на яку кладуть програми-фігури.
- Переходи: Мережа → (випадкова зустріч) → Custom Screen → бій ↔ Custom Screen щоразу на повній шкалі → end-screen → Мережа; HP 0 → game over → останнє збереження.

## Фічі поза полем
- `card-collection` (`+feature:card-collection`): сотні чипів, бібліотека, торговці чипами (випадковий чип за кілька своїх), обмін через Link Cable.
- `+feature:ante-versus`: у Real NetBattle переможець забирає чип у переможеного (BN1), у BN3 — випадковий чип.
- Прогресія сюжетом через два світи; `save-game` у PET; зірки на титулі за великі завдання (BN2); Hard Mode з особливим чипом (BN2).
- Апгрейди: PowerUp для бастера (BN1–2), HP Memory, Navi Customizer (BN3+), Styles (BN2–3), Souls (BN4–5), Cross/Beast Out (BN6); дві версії гри з BN3 (ексклюзивні чипи й форми).
- `local-multiplayer`: два гравці — лише через Link Cable, кожен на своїй консолі.

## Варіації й родичі
- BN1 (2001): папка 30, ≤10 однакових, ≤5 Navi-чипів; MegaMan повністю лікується після бою.
- BN2: код `*` (джокер), 5 Styles з елементами замість броні, 3 папки, ≤5 копій і ≤5 Navi; HP не відновлюється між боями; SubChips поза боєм.
- BN3: Navi Customizer (сітка програм замість PowerUp), класи Standard (≤4 копії) / Mega (≤5, по 1) / Giga (1); PA з 3–4 чипів; поля NetBattle з тріщинами й «негативними» панелями; Virus Breeder.
- BN4–5: Double Soul — жертва чипа дає форму союзного Navi; Dark Chips; у BN5 кожен PA — раз за бій; Liberation Missions (покрокова карта панелей командою).
- BN6: Cross System (будь-коли; знімається атакою слабкого елемента), Beast Out на обмежений час.
- Rockman.EXE 4.5 Real Operation — команди замість прямого керування; Operate Shooting Star (DS, 2009) — порт BN1; Legacy Collection (2023) — усі 10 версій.
- Нащадки: One Step From Eden (роглайт-колода, поле теж поділене на дві половини) — та сама дуель половин поля (?).
- Родичі в корпусі: [plants-vs-zombies](plants-vs-zombies.md) і [crystal-defenders-vanguard-storm](crystal-defenders-vanguard-storm.md) (рядки, ворог справа/зліва), [clash-royale](clash-royale.md) (колода + реальний час + своя половина), [marvel-snap](marvel-snap.md), [inscryption](inscryption.md) (карти на смугах).
- **Осі варіацій**: поле — дві половини з фіксованою межею / межа рухома (AreaGrab) · рука — випадкові N з папки / колода по черзі · обмеження руки — «одна назва або один код» / мана / без обмежень · керування — пряме / командами (4.5).

## Цікавинки для курсу
- Поле 6×3 з власником кожної панелі й заборона ступати на чуже + чип, що перефарбовує стовпець, — 🥉 (стан панелі = сторона, а не лише тип).
- Рука з 5 карт і правило вибору «однакова назва або однаковий код, `*` — джокер» — 🥉 (валідація множини вибору, підсвітка недоступних).
- Program Advance: послідовність у черзі → одна суперкарта — 📎 (пошук підпослідовності за таблицею рецептів).
- Типи панелей як шар клітини (тріщина → дірка → відновлення за таймером, лід, отрута, трава ×2 від вогню) — 🥈 (таблиця «тип панелі × елемент атаки»).
- Custom Gauge: real-time бій, що зупиняється на «хід» вибору карт, — 🥉 (два режими одного ігрового циклу).
- Navi Customizer: поліоміно-програми на сітці з правилами сумісності, порушення → баг — 🥈.
- Валідатор колоди (30 карт, ліміти копій за класом) — 🌱.

## Мапа на каталог
- Є: `move-4dir` ↔ рух по 3×3 · `hp-damage` · `projectile-shot` + `shoot-forward` ↔ бастер · `line-of-sight-attack` ↔ удар першого в рядку · `floor-types` ↔ типи панелей · `inertia-slide` ↔ лід · `cell-transform` ↔ чипи зміни панелей · `impassable-cells` ↔ дірки/зламані/чужі панелі · `destroy-all-enemies` · `player-death` · `temporary-modes` ↔ Beast Out · `polyomino-placement` ↔ Navi Customizer · `world-map` ↔ Мережа з вузлами · `shop-catalog` · `codex-window` ↔ Chip Library · `save-game` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+deck-draw` — уже пропонувалась сімʼєю (Clash Royale); тут: 5 випадкових з 30 на кожен «хід».
  - `+hand-select-by-code` «Вибір карт з руки за спільною ознакою» · interface/input · 🥉 · слоти {keys: name|code, wildcard: *}.
  - `+program-advance` «Комбо-послідовність карт → суперкарта» · game-logic/score · 📎 · слот {recipes}.
  - `+split-field-halves` «Поле з власником кожної клітини, ступати лише на своє» · entities/legality · 📎 · слот {split: column}.
  - `+panel-steal` «Перехоплення клітин супротивника» · entities/interact · 📎.
  - `+charge-shot` «Заряджений постріл утриманням» · entities/combat · 🌱 · слот {charge}.
  - `+damage-type-wheel` «Коло елементів ×2» · entities/combat · 📎 — уже пропонувалась (Element TD 2).
  - `+folder-limits` «Валідатор колоди: розмір і ліміти копій» · game-logic/constraints · 🌱 · слоти {size, max_copies, per_class}.
  - `+random-encounter` «Бій як випадкова зустріч на кроці» · entities/spawn · 🌱 · слот {p}.
  - `+ante-chip-versus` «Ставка карткою у PvP» · game-logic/opponent · 📎.
  - `+panel-regen` «Клітина відновлюється за таймером» · entities/state · 🌱 · слот {delay}.
  - `+placement-bug-rule` «Порушення правил розкладки дає штраф-стан» · entities/legality · 📎.
  - `+form-change` «Форма персонажа зі своїми атаками й слабкістю» · entities/state · 📎.
  - `+chip-trader` «Автомат обміну N карт на випадкову» · game-logic/economy · 🌱.
  - `+indirect-command-mode` «Гравець командує, персонаж діє сам» · interface/input · 🥉 (4.5 Real Operation).

## Пропозиції до словників
- `+effect:draw_cards` — видати N випадкових карт з колоди в руку (назва `draw` уже зайнята нічиєю).
- `+trigger:gauge_full` — шкала (Custom Gauge, мана) заповнилась; зараз `counter(…, ==, full)`.
- `+cond:same_code` — карти мають ту саму літеру-код (з джокером `*`).
- `+role:card` — карта/чип як сутність поза полем (підтвердження Clash Royale); `+role:panel` — клітина з власником-стороною.
- `+window:custom-screen` — модал вибору карт з руки, що ставить real-time на паузу; `+window:deck-builder` — редактор папки/колоди (підтвердження).
- `+ui:custom-gauge` — шкала до наступної руки; `+ui:chip-queue` — черга вибраних карт над персонажем.
- `+feature:card-collection` (підтвердження), `+feature:ante-versus` — PvP на ставку картою.
- `+axis:field=split-halves` — поле поділене між сторонами, межа — частина стану.

## Джерела
- ⭐ [Wikipedia: Mega Man Battle Network (серія)](https://en.wikipedia.org/wiki/Mega_Man_Battle_Network) — поле 6×3 з половинами по 9, Custom Gauge, папка, класи чипів, PA, елементи ×2, Link Cable, відмінності сиквелів, платформи.
- [Wikipedia: Mega Man Battle Network (2001)](https://en.wikipedia.org/wiki/Mega_Man_Battle_Network_(video_game)) — 5 випадкових чипів, правило назви/коду, папка 30 і ліміти, мішок, 5 елементів, Test/Real battle.
- [Wikipedia: BN2](https://en.wikipedia.org/wiki/Mega_Man_Battle_Network_2) — код `*`, Styles, 3 папки, SubChips.
- [Wikipedia: BN3](https://en.wikipedia.org/wiki/Mega_Man_Battle_Network_3) — Navi Customizer, ліміти Standard/Mega/Giga, PA з 3–4 чипів, поля NetBattle.
- [Wikibooks: Combat Basics](https://en.wikibooks.org/wiki/Mega_Man_Battle_Network/Combat_Basics) — червоні/сині панелі, типи панелей з ефектами, бастер 1 шкоди і заряд.
- [Wikibooks: Printable version](https://en.wikibooks.org/wiki/Mega_Man_Battle_Network/Printable_version) — Custom+1/+2 (до 10 чипів у BN3, 8 у BN4–5), PA за порядком і кодами, раз за бій у BN5.
- YouTube: [пошук «Mega Man Battle Network gameplay»](https://www.youtube.com/results?search_query=Mega+Man+Battle+Network+gameplay).

## Непевне
- (?) Свята панель (×½ шкоди) і BN6-заморожування на льоду — лише зі сніпета пошуку (The Rockman EXE Zone), сторінку не відкрито.
- (?) Механіка AreaGrab/PanelGrab (захоплення стовпця/панелі) — у джерелах лише назви чипів, опис з памʼяті.
- (?) Busting Level, оцінка й нагорода за бій — у відкритих джерелах не описано.
- (?) Кнопка Add на Custom Screen (відмова від вибору заради більшої руки наступного разу) — з памʼяті.
- (?) Коло слабкостей (Fire → Wood → Elec → Aqua → Fire) — джерела кажуть лише «слабкість = ×2».
- (?) Як саме показані HP вірусів і назва чипа в HUD; точні таймінги Custom Gauge.
- (?) Lava: Wikibooks дає 10/20 шкоди і 50/100 з Wood Style — формулювання суперечливе, числа не взято в правила.
