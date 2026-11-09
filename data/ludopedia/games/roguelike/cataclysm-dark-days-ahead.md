---
title: "Cataclysm: Dark Days Ahead"
slug: cataclysm-dark-days-ahead
aka: [CDDA, "C:DDA", Cataclysm DDA, "Cataclysm (Whales, 2010)"]
family: roguelike
also: [build-sim]
klass: avatar
axes:
  field: layers
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: survive
year: 2013
platforms: [Linux, macOS, Windows, Android, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cataclysm:_Dark_Days_Ahead", best: true, note: "огляд систем: потреби, крафт, будівництво, авто, ферма, сезони, мутації, біоніка, зомбі, що повстають і еволюціонують"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/data/core/help.json", note: "внутрішньоігрова довідка: 100 очок руху на крок, 8 напрямків, safe mode, біль, морал/фокус, рани, крафт, пастки, водіння, плавучість"}
  - {kind: official, url: "https://github.com/CleverRaven/Cataclysm-DDA", note: "репозиторій гри (CC BY-SA), README, doc/"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/design-balance-lore/design-gameplay.md", note: "дизайн-документ: пісочниця, «пасивно ворожий світ», етапи першого року, зима"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/design-balance-lore/GAME_BALANCE.md", note: "шкали швидкості й HP монстрів, статів, навичок"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/MUTATIONS.md", note: "мутаген, праймер, категорії, поріг, cancels/changes_to, нестабільність"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/OVERMAP.md", note: "оверкарта 180×180×21, mapgen локальної карти"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/VEHICLES_JSON.md", note: "транспорт = частини на сітці (x, y), порядок встановлення"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/JSON_INFO.md", note: "vehicle_part: location (одна частина на місце), durability, breaks_into; частини тіла"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/data/json/vehicleparts/vp_flags.json", note: "значення прапорців WHEEL, ENGINE, CONTROLS, SEAT, CARGO, TURRET, ARMOR, ROOF"}
  - {kind: other, url: "https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/data/json/vehicleparts/frames.json", note: "рама: location structure, durability 400, встановлення Mechanics 1 + зварювання"}
  - {kind: other, url: "https://discourse.cataclysmdda.org", note: "форум спільноти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=cataclysm+dark+days+ahead+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [move-8dir, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, hunger-clock, status-effects, environment-death, permadeath, destructible-blocks, cell-transform, projectile-shot, shoot-burst, fog-of-war, player-camera, map-window, message-log, status-panel, console-render, gui-render, keyboard-controls, cell-click, game-settings, save-game, help-window, +speed-turn-order, +limb-disable, +crafting-recipes, +construction-menu, +vehicle-grid-builder, +center-of-mass-drive, +season-cycle, +crop-growth, +mutation-tree, +mutation-threshold, +bionic-implants, +morale-states, +focus-learning, +skill-by-practice, +corpse-revive, +enemy-mutation, +addiction, +weather-modifiers, +safe-mode-stop, +persistent-world]
proposes: ["+role:body-part", "+role:vehicle", "+trigger:season_change", "+effect:craft", "+effect:install(part, tile)", "+effect:mutate", "+cond:skill(name, op, n)", "+cond:location_free(tile, slot)", "+window:crafting-window", "+window:construction-menu", "+window:vehicle-window", "+window:character-creation", "+window:world-gen", "+ui:body-status", "+ui:monster-compass", "+feature:safe-mode", "+axis:session=character-in-world"]
author: opus
date: 2026-11-09
---

# Cataclysm: Dark Days Ahead — пісочниця виживання після апокаліпсису: зомбі повстають, авто збирається з деталей по клітинах

## Суть
Покроковий роглайк-пісочниця: персонаж виживає в процедурному світі після катастрофи — шукає їжу, воду, ліки, ховається від зомбі й мутантів, вчиться ремеслам і будує базу або машину. Універсальної мети нема, крім виживання: дизайн-документ називає світ «пасивно ворожим» — він не реагує на гравця, просто вбиває необережних. Для корпусу ядро — **система систем на клітинах**: тіло з частинами й ранами, потреби (голод, спрага, сон, температура, морал), крафт за рецептом/інструментами/навичкою, будівництво, що змінює терен, і **транспорт, зібраний частинами на власній сітці**. Відкритий код (CC BY-SA), спільнотний форк гри Cataclysm (Whales, 2010).

## Поле і час
- Квадратна сітка, рух у 8 напрямків + «чекати на місці»; більшість терену руйнується. Локальна карта генерується з **оверкарти** 180×180 клітин-«зон» і 21 рівня глибини (z-рівні: підвали, лабораторії, шахти, багатоповерхові будівлі) — тому `field: layers`.
- Оверкарта — абстрактний шар (де місто, дорога, лабораторія); вміст кожної зони робить її mapgen при першому відвідуванні, далі світ зберігається.
- Час покроковий з **очками руху**: крок коштує 100 очок (більше на складному терені), атака — за вагою й розміром зброї. Швидкість монстрів — за шкалою відносно базової 100 (повзучий зомбі 20, середня тварина 70, «дуже швидкий» ~200, ліміт балансу 300): швидший ходить частіше.
- Добовий цикл, сезони (тривалість налаштовується при створенні світу), погода, температура. Зима сповільнює подорожі снігом і ховає сплячих зомбі під снігом.
- Видимість: побачене лишається на карті під туманом війни; предмети в контейнерах невидимі, доки не підійдеш.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Виживальник | player | стати (сила, спритність, інтелект, сприйняття), навички 0–10, частини тіла з HP, потреби, морал, фокус, енергія біоніки | рух 8 напрямків; атака = рух у ворога; крафт, будівництво, водіння |
| Частина тіла (голова, торс, руки, ноги…) | body-part (+) | HP, статус, encumbrance | голова/торс на нулі — смерть; кінцівка на нулі — перелом, потрібна шина |
| Зомбі | enemy | швидкість, HP | основна загроза; сплячі лежать як трупи, доки їх не потурбувати; повстає через час, якщо тіло не розрубати/не розтрощити |
| Спец-зомбі та їх еволюції | enemy | — | зʼявляються з часом; монстри мутують у сильніші форми |
| Здичавілі люди | enemy | — | ворожі до гравця, зомбі їх не чіпають |
| Тварини (білки, щури, вовки, ведмеді) | neutral | — | дичина: мʼясо, хутро, кістки, органи; можуть бути заміщені зомбі-/мутант-версіями |
| Mi-go, трифіди, грибкові, позавимірні істоти | enemy | — | окремі фракції чудовиськ; портальні шторми приносять «nether»-монстрів |
| NPC-виживальники, фракції | ally / neutral | лояльність, довіра | супутники, торгівля, місії фракцій; ворожнеча з суперниками |
| Двері, вікна, стіни | static / gate | міцність | двері відчиняються/зачиняються, замкнені — розбити; вікна можна забити дошками |
| Яма, ведмежий капкан, бульбашкова плівка | hazard | — | капкан шкодить, шумить і тримає; плівка шумить і будить |
| Опромінена зона | zone | рівень радіації | радіація накопичується, невидима без лічильника |
| Верстак | static | — | прискорює крафт |
| Рама транспорту | object | location structure, durability 400 | старт будови машини; на неї монтуються інші частини |
| Частини транспорту (двигун, колесо, сидіння, керування, бак, вантаж, турель, броня, дах) | vehicle (+) | location, durability, breaks_into | кожна займає «місце» в клітині машини; зруйнована — розсипається уламками навколо |
| Труп | object | — | розібрати (мʼясо, кістки) або розтрощити, щоб зомбі не повстав |
| Їжа, вода | pickup | ситість/поживність, вітаміни | природну воду треба кипʼятити/очищати |
| Ліки (знеболення, бинти, антибіотики, шина, стимулятори) | pickup | затримка дії, звикання | знімають біль/кровотечу/інфекцію; деякі викликають залежність |
| Мутаген, праймер | pickup | категорія | мутаген запускає мутацію, праймер задає напрям |
| CBM (біонічний модуль) | pickup | вимоги до навичок | встановлення в автодоку/лікарем |
| Книги | pickup | навичка, рецепти | вчать навичку й рецепти; розважальні — підіймають морал |
| Насіння, рослина | resource | сезон, температура | росте з пізньої весни до ранньої осені; урожай від навички виживання |

## Правила (КОЛИ → ЯКЩО → ТО)
Рух і бій:
- КОЛИ `input(move, dir)` → ЯКЩО `free(cell)` → ТО `move(player, dir)`, `counter(moves, -100)` (більше на складному терені).
- КОЛИ `input(move, dir)` → ЯКЩО `occupied(cell, monster)` → ТО `damage(monster, n)`, `counter(moves, -attack_cost)`.
- КОЛИ `input(smash, dir)` → ЯКЩО `custom: «сила удару > міцність терену/дверей»` → ТО `set_cell(cell, broken)`, `sound(noise)`.
- КОЛИ `line_of_sight(player, monster)` → ЯКЩО `mode(safe)` → ТО `custom: «перервати рух/довгу дію»`, `message(text)`.
- КОЛИ `input(fire, burst)` → ТО `custom: «кожен наступний постріл черги — нижча точність»`; перезаряджання — `counter(moves, -reload_time)`.
- КОЛИ `died(zombie)` → ЯКЩО `not custom: «труп розрубано або розтрощено»` → ТО `custom: «через час»` `transform(corpse, zombie)`.
- КОЛИ `timer(evolve)` → ТО `transform(monster, stronger_form)` (зомбі «рівняються» до майстрів-немезид).
- КОЛИ `custom: «зону очищено, монстри не повстають»` → ТО `custom: «нових монстрів тут не зʼявляється»` (ліміт на зону).

Тіло і рани:
- КОЛИ `custom: «влучання по частині тіла»` → ТО `hp(body_part, -n)`, `custom: «статус частини в боковій панелі»`.
- КОЛИ `hp_zero(head|torso)` → ТО `lose` (персонаж мертвий назавжди).
- КОЛИ `hp_zero(arm|leg)` → ТО `set_state(limb, broken)`; КОЛИ `input(use, splint)` → ЯКЩО `state(limb, broken)` → ТО `custom: «довге загоєння під шиною»`.
- КОЛИ `tick` → ЯКЩО `state(body_part, bleeding)` → ТО `hp(body_part, -n)`; КОЛИ `input(use, bandage)` → ТО `clear_state(body_part, bleeding)`.
- КОЛИ `tick` → ЯКЩО `state(wound, untreated)` and `prob(p)` → ТО `set_state(body_part, infected)`; пізня інфекція — лише антибіотики й час.
- КОЛИ `input(sleep)` → ТО `heal(player, n)` (сон відновлює HP; ліжко в приміщенні — краще).

Потреби і стани:
- КОЛИ `tick` → ТО `counter(hunger, +n)`, `counter(thirst, +n)`, `counter(fatigue, +n)`; спрага вбиває швидше за голод.
- КОЛИ `input(eat, food)` → ТО `take(player, food)`, `counter(hunger, -n)`; ЯКЩО `custom: «шлунок переповнений»` → ТО `set_state(player, overfull)`.
- КОЛИ `counter(fatigue, >=, sleepy)` → ТО `set_state(player, tired)` (`custom: «штрафи статів і руху»`).
- КОЛИ `state_on(player, pain)` → ТО `speed(player, -n)`, `custom: «−стати»`; знеболення діє із затримкою — `custom: «друга доза до дії першої = ризик передозування»`.
- КОЛИ `input(use, drug)` → ЯКЩО `prob(addiction)` → ТО `set_state(player, addicted)`; без дози — `set_state(player, withdrawal)`; нова доза → `clear_state(player, withdrawal)` і сильніша залежність.
- КОЛИ `counter(morale, <, very_low)` → ТО `custom: «крафт неможливий»`; КОЛИ `custom: «практика / читання»` → ТО `counter(focus, -n)`; фокус тяжіє до точки рівноваги (природно 100), її зсувають морал і біль.

Крафт, будівництво, транспорт:
- КОЛИ `input(craft, recipe)` → ЯКЩО `custom: «рецепт відомий»` and `has(player, tools)` and `has(player, components)` → ТО `take(player, components)`, `give(player, item)`, `counter(skill, +xp)`; ЯКЩО `prob(fail)` → ТО `custom: «частину матеріалів зіпсовано»`.
- Успіх крафту: орієнтир «навичка ≈ 1.5 × складність»; штрафи — низька мораль, пошкоджені кінцівки, погане світло, нема рівної поверхні / верстака.
- КОЛИ `input(construct, what, cell)` → ЯКЩО `has(player, materials)` and `has(player, tools)` → ТО `set_cell(cell, what)` (забите вікно, яма, стіна, колодязь, підвал).
- КОЛИ `input(start_vehicle)` → ЯКЩО `has(player, frame)` → ТО `place(player, frame)` (нова машина з однієї клітини).
- КОЛИ `input(install, part, tile)` → ЯКЩО `custom: «місце (location) частини в цій клітині вільне»` and `has(player, tools)` and `custom: «навичка Mechanics ≥ вимоги»` → ТО `custom: «частина додається до клітини машини»`.
- КОЛИ `input(drive, dir)` → ЯКЩО `custom: «центр мас між усіма колесами»` and `has(engine, fuel)` → ТО `move(vehicle, dir)`; двигун сам бере пальне з баку.
- КОЛИ `hp_zero(vehicle_part)` → ТО `disappear(vehicle_part)`, `spawn_at(debris, around)`.
- КОЛИ `enter(vehicle, deep_water)` → ЯКЩО `custom: «маса в тоннах < ¼ · довжина · ширина і корпус достатньо високий»` → ТО `custom: «пливе»`; інакше `custom: «тоне»`.

Світ:
- КОЛИ `timer(day)` → ЯКЩО `custom: «сезон і температура придатні»` → ТО `transform(seed, plant)`; збір — `give(player, crop)` пропорційно навичці виживання; добрива пришвидшують.
- КОЛИ `enter(player, irradiated_zone)` → ТО `counter(radiation, +n)`; у чистій зоні — повільно спадає.
- КОЛИ `counter(radiation, >=, high)` або `input(use, mutagen)` → ЯКЩО `prob(p)` → ТО `custom: «мутація в категорію з найбільшим праймером»` (більшість — погані, частина — корисні).
- КОЛИ `custom: «мутація конфліктує з наявною (той самий types)»` → ТО `custom: «стару знято або понижено, і більше нічого»` — одна зміна за спробу.
- КОЛИ `counter(primer, >=, 2200)` → ЯКЩО `prob(p)` → ТО `set_state(player, threshold_crossed)` — назавжди, інші пороги закриті.
- КОЛИ `input(install, cbm)` → ЯКЩО `prob(skill, int)` → ТО `give(player, bionic)`; інакше `custom: «каліцтво»`.
- КОЛИ `enter(a, bear_trap)` → ТО `damage(a, n)`, `sound(noise)`, `set_state(a, held)`; КОЛИ `input(disarm, trap)` → ЯКЩО `prob(devices, dex)` → ТО `pickup`; інакше `custom: «пастка спрацьовує»`.
- Перемога: нема (пісочниця). Поразка: смерть персонажа (голова/торс, кровотеча, голод, спрага, інфекція, монстри) — назавжди; світ може лишитись для нового персонажа. Рахунок: нема.

## Керування і ввід
- Цифрова клавіатура / vi-клавіші / стрілки / миша — 8 напрямків і «чекати»; для стрілок — режими діагоналей (Numpad Emulation, CW/CCW, L/R Tilt, Diagonal Lock).
- Окремі клавіші: відчинити/зачинити двері, розбити, огляд («look around» зі скролом), список предметів поруч, крафт, будівництво, застосувати предмет (з вибором напрямку для пасток), `?` — довідка.
- Транспорт: на сидінні з робочим керуванням — клавіша керування, далі цифрова клавіатура / vi-клавіші; `s` — ручне гальмо.
- Safe mode — автостоп руху, щойно видно ворога; довгі дії (крафт, читання) перериваються й продовжуються.

## Вікна, меню, HUD
- `main-menu` → створення світу (`+window:world-gen`: налаштування й моди) → створення персонажа (`+window:character-creation`: сценарій, професія, риси, стати) → `game-screen`.
- `game-screen`: карта (ASCII або тайлсет) + бічна панель: статус частин тіла кольором (червоний — кровотеча, синій/зелений — інфекція), голод/спрага, енергія біоніки під здоровʼям, `+ui:monster-compass` — список і компас видимих монстрів, `message-log`.
- `map-window` — оверкарта з позначками й туманом.
- `inventory-window` — інвентар; `+window:crafting-window` — 10 категорій (Weapon, Ammo, Food, Chem, Electronic, Armor, Appliance, Other, Animals, Practice); `+window:construction-menu` — список будов, звідси «Start Vehicle Construction».
- `+window:vehicle-window` — огляд машини: частини по клітинах, швидкості, опір (повітря, вода, кочення, статичний), оцінка пального.
- `help-window` (`?`) — розділи довідки; `settings-window` (опції, клавіші), `end-screen` — смерть.
- Переходи: main-menu → world-gen → character-creation → game-screen ⇄ map-window / inventory / crafting / construction / vehicle-window; смерть → end-screen → новий персонаж у тому самому світі або новий світ.

## Фічі поза полем
- `permadeath` персонажа + `+axis:session=character-in-world`: світ зберігається між персонажами (документація радить не зловживати).
- `custom-rules` / `mod-support`: налаштування й моди світу при генерації (тривалість сезонів тощо); моди в репозиторії.
- Два фронтенди — текстовий (ncurses) і графічний (SDL з тайлсетами) — `console-render` + `gui-render`; `localization` (25 мов); `remap-controls`.
- Довідка `?`; туторіал у меню Special (може працювати неповністю); стабільні знімки й щоденна experimental-гілка.
- Етапи першого року як дизайн-прогресія: «Terrified and Wet» (перші дні) → «New Scavenger» → «Wasteland Scavenger» → «Preparation» → перша зима → мід/лейт-гейм; прогрес — спорядження, навички, союзники, а не стрибки рівнів.

## Варіації й родичі
- Cataclysm (Whales, 2010, код під CC BY-SA) → спільнотний форк DDA (2013; 0.1 — 26 лютого 2013) → стабільні знімки 0.A…0.I.
- Родичі в корпусі: [caves-of-qud](caves-of-qud.md) (клітинна фізика, мутації, кібернетика), [nethack](nethack.md) і [dungeon-crawl-stone-soup](dungeon-crawl-stone-soup.md) (класична роглайк-основа), [cogmind](cogmind.md) (тіло з частин — у роботі), [stoneshard](stoneshard.md) (рани по частинах тіла, біль, сп'яніння), [quasimorph](quasimorph.md) (рани кінцівок, голод), [gearhead](gearhead.md) (машини з частин).
- Осі варіацій: **тіло** (одне HP / частини з HP і критичними частинами) · **час** (хід = крок / очки руху зі швидкістю) · **транспорт** (нема / готовий / збирається з частин на сітці) · **світ** (рівні / персистентна оверкарта з z-рівнями) · **смерть ворога** (остаточна / повстання з трупа).

## Цікавинки для курсу
- Транспорт як **власна сітка частин**: у клітині кілька «місць» (рама, двигун, колесо, сидіння, дах), одна частина на місце; рух можливий, коли центр мас між колесами — 🥇 (структура даних + перевірки встановлення + фізика руху).
- Очки руху: крок 100, атака за вагою, швидкість монстра 20–300 — хто ходить наступним — 🥉 (черга подій/енергії замість «хід за хід»).
- Тіло з частин: HP на голові, торсі, кінцівках; критичні частини = смерть, кінцівки = перелом і шина; кровотеча й інфекція як стани з тіком — 🥉.
- Зомбі повстає через час, якщо труп не розтрощено/не розібрано — 📎 (стан трупа + таймер).
- Мутації: мутаген + праймер категорії, поріг на 2200 праймеру, `cancels`/`changes_to`/`types` — дерево правил як дані — 🥈.
- Крафт: рецепт + інструменти + компоненти + навичка ≈ 1.5 × складність, штрафи за світло й мораль — 🥉 (таблиця рецептів, перевірка вимог).
- Плавучість: маса < ¼ · довжина · ширина — 🌱 (одна формула поверх сітки машини).

## Мапа на каталог
- Є: `move-8dir` · `hp-damage` (частини тіла) · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `hunger-clock` (голод і спрага) · `status-effects` (кровотеча, інфекція, біль, ломка) · `environment-death` · `permadeath` · `destructible-blocks` (терен руйнується) · `cell-transform` (будівництво змінює клітини) · `projectile-shot` + `shoot-burst` (черга знижує точність) · `fog-of-war` (запамʼятована карта) · `player-camera` · `map-window` · `message-log` · `status-panel` · `console-render` + `gui-render` · `keyboard-controls` + `cell-click` · `game-settings` · `save-game` · `help-window`.
- **Нема** → пропозиції карток:
  - `+speed-turn-order` «Очки руху й швидкість визначають, хто ходить» · game-logic/opponent · 🥉 · слот {cost_per_action}.
  - `+limb-disable` «Частина тіла на нулі вимикає функцію» · entities/state · 🥉 · слот {critical: [head, torso]}.
  - `+crafting-recipes` «Рецепт: інструменти + компоненти + навичка» · game-logic/economy · 🥉.
  - `+construction-menu` «Будівництво змінює терен з матеріалів» · entities/interact · 📎.
  - `+vehicle-grid-builder` «Машина з частин на власній сітці, одна частина на місце» · entities/state · 🥇.
  - `+center-of-mass-drive` «Рух лише якщо центр мас між колесами» · entities/move · 🥈.
  - `+season-cycle` «Сезони змінюють світ» · levels/progression · 📎; `+crop-growth` «Посів росте за сезоном/температурою» · entities/state · 📎.
  - `+mutation-tree` / `+mutation-threshold` «Мутації категорій, поріг назавжди» · entities/state · 🥈.
  - `+bionic-implants` «Імплант-модулі з ризиком встановлення» · entities/state · 🥉.
  - `+morale-states`, `+focus-learning`, `+skill-by-practice` «Навичка росте від дії, швидкість навчання — фокус» · entities/state · 📎.
  - `+corpse-revive` «Труп повстає, якщо не знищити» · entities/death · 📎; `+enemy-mutation` «Монстри еволюціонують з часом» · entities/spawn · 📎.
  - `+addiction` «Залежність і ломка» · entities/state · 📎; `+weather-modifiers` · 🥉; `+safe-mode-stop` «Автостоп, коли видно ворога» · interface/input · 🌱; `+persistent-world` «Світ переживає персонажа» · game-logic/save · 🥉.

## Пропозиції до словників
- `+role:body-part` — частина тіла як сутність зі своїм HP і станом (голова, торс, кінцівки).
- `+role:vehicle` — збірна сутність з частин, що їде як ціле і має власну сітку.
- `+trigger:season_change` — зміна сезону (ріст рослин, сніг, поведінка орд).
- `+effect:craft` — створити предмет за рецептом (атомарно: забрати компоненти, дати результат, досвід).
- `+effect:install(part, tile)` — додати частину до клітини збірної сутності (машини).
- `+effect:mutate` — отримати/змінити мутацію за правилами дерева.
- `+cond:skill(name, op, n)` — рівень навички порівняно з вимогою (крафт, механіка, знешкодження).
- `+cond:location_free(tile, slot)` — у клітині збірної сутності вільне місце потрібного типу.
- `+window:crafting-window`, `+window:construction-menu`, `+window:vehicle-window`, `+window:character-creation`, `+window:world-gen` — див. «Вікна».
- `+ui:body-status` — статус частин тіла кольором; `+ui:monster-compass` — список і напрямки видимих монстрів.
- `+feature:safe-mode` — автостоп дій при появі ворога (моди світу — наявне `mod-support`).
- `+axis:session=character-in-world` — персонаж помирає назавжди, світ лишається.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Cataclysm:_Dark_Days_Ahead) — огляд систем: потреби, хвороби, мутації, біоніка, крафт, будівництво, авто, ферма, сезони, зомбі, що повстають і мутують; історія форку.
- [help.json](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/data/core/help.json) — довідка гри: рух і очки руху, safe mode, туман, голод/спрага/сон, біль, рани й переломи, залежність, морал і фокус, радіація й мутації, біоніка, крафт (10 категорій, 1.5×), пастки, бій, водіння, плавучість.
- [design-gameplay.md](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/design-balance-lore/design-gameplay.md) — етапи першого року, зима, фракції, «Superhero, not demigod».
- [GAME_BALANCE.md](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/design-balance-lore/GAME_BALANCE.md) — швидкість/HP монстрів, стати, навички.
- [MUTATIONS.md](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/MUTATIONS.md) — мутаген, праймер, поріг 2200, cancels/changes_to, нестабільність.
- [OVERMAP.md](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/OVERMAP.md) · [VEHICLES_JSON.md](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/VEHICLES_JSON.md) · [JSON_INFO.md](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/doc/JSON/JSON_INFO.md) · [vp_flags.json](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/data/json/vehicleparts/vp_flags.json) · [frames.json](https://raw.githubusercontent.com/CleverRaven/Cataclysm-DDA/master/data/json/vehicleparts/frames.json) — оверкарта, сітка машини, місця частин, прапорці.
- [GitHub](https://github.com/CleverRaven/Cataclysm-DDA) — код, README, моди.

## Непевне
- (?) Розмір однієї зони оверкарти в клітинах локальної карти і «бульбашка реальності» (де симулюється світ) — у відкритих документах не знайдено.
- (?) Точний список частин тіла гравця (є типи head, torso, sensor, mouth, arm, hand, leg, foot) і їх HP; `base_hp 60` у JSON_INFO — приклад для лівої руки, не обовʼязково актуальне значення.
- (?) Перелік «місць» частин машини, крім `structure` і `fuel_source`, — з `vehicle_part_locations.json`, який не відкрився; приклади в таблиці (двигун, дах, броня) — за прапорцями vp_flags.
- (?) Прапорець `INITIAL_PART` у рам — за назвою «може почати будову машини»; документацію не знайдено.
- (?) Темп голоду/спраги/втоми в ходах і пороги станів — довідка дає лише якісний опис («кожні десяток годин хочеться спати»).
- (?) Чи `field: layers` точніше за `3d`: z-рівні — стопка 2D-сіток, будівлі тривимірні з останніх версій.
