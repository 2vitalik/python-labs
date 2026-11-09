---
title: Stoneshard
slug: stoneshard
aka: []
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: survive
year: 2020
platforms: [Windows, Linux (SteamOS)]
links:
  - {kind: fandom, url: "https://stoneshard.com/wiki/Injuries_%26_Pain", best: true, note: "офіційна вікі: частини тіла, стадії травм, стабілізація, біль і ліміт болю, кровотеча — головна механіка гри за 10 хвилин"}
  - {kind: steam, url: "https://store.steampowered.com/app/625960/Stoneshard/", note: "опис: покрокові тактичні бої, біль, мораль, розсудливість, караван, Ironman"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Combat_Formulas", note: "кожен хід гравця = хід усіх ворогів; влучність, fumble, крит, блок, захист по частині тіла, атаки з нагоди"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Psyche", note: "мораль × розсудливість, компоненти 50/35/15, 12 станів психіки"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Hunger,_Thirst_%26_Intoxication", note: "пороги 25/50/75 %, темп у ходах, ситість, нудота, інтоксикація"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Fatigue_%26_Resting", note: "втома, сон лише в ліжку, збереження сном, Rest Mode"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Caravan_%26_Followers", note: "караван-база на глобальній мапі, фураж, апгрейди, склад, послідовники"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Global_Map", note: "глобальна мапа 38×35 клітин під туманом, випадкові дороги й точки інтересу"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Noise_%26_Stealth", note: "шум, поле зору ворогів, стани Unaware/Suspicious/Hostile"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Athletics_(skill_tree)", note: "ривок до клітини, підсічка трьох сусідніх клітин, атаки з нагоди"}
  - {kind: fandom, url: "https://stoneshard.com/wiki/Basic_Skills_(skill_tree)", note: "Set Aflame: підпал клітини, огляд пасток і таємних проходів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=stoneshard+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, status-effects, hunger-clock, inventory, inventory-items, inventory-limit, item-pickup, dungeon-generation, fog-of-war, map-window, shop-catalog, round-currency, permadeath, unit-xp-skills, destructible-blocks, character-select, +body-part-targeting, +limb-disable, +injury-stages, +pain-meter, +morale-states, +sanity-meter, +psyche-quadrant-states, +intoxication-meter, +fatigue-pool, +attack-of-opportunity, +fumble-crit-roll, +block-power-pool, +damage-type-resistances, +tile-ignite, +dash-charge, +stealth-alertness, +noise-lure, +mobile-base-caravan, +follower-perks, +save-at-bed, +rest-mode, +classless-skill-trees]
proposes: ["+role:body-part", "+role:vehicle", "+trigger:noise", "+cond:alert(a, level)", "+effect:stabilize(part)", "+effect:stumble", "+window:health-tab", "+window:skills-window", "+window:crafting-window", "+window:sleep-dialog", "+window:stash-window", "+ui:paper-doll", "+ui:fatigue-bar", "+feature:save-at-bed", "+axis:injury-model"]
author: opus
date: 2026-11-09
---

# Stoneshard — покроковий роглайк відкритого світу, де кожен удар ранить конкретну частину тіла, а психіка — окрема гра

## Суть
Найманець мандрує середньовічним королівством: виконує контракти, чистить підземелля, торгує, ночує в тавернах. Бої — покрокові на клітинах: кожен хід гравця — хід усіх ворогів. Особливість — **тіло й психіка як набір окремих шкал**: кожен удар знімає загальне HP і HP випадкової частини тіла (голова, торс, руки, ноги) з трьома стадіями травм; поверх — біль, мораль і розсудливість (їх поєднання дає 12 станів психіки), голод, спрага, інтоксикація, втома. Пересувна база — **караван**, який можна відправити на відвідану клітину глобальної мапи. Класів нема: 20 гілок умінь (216+ умінь) відкриті кожному.

## Поле і час
- Два масштаби: локації (поселення, глушина, процедурні підземелля) на квадратній сітці клітин і **глобальна мапа** 38×35 клітин: поселення фіксовані, дороги, ріки, точки інтересу й підземелля — випадкові для кожного сейву; мапа відкривається лише відвіданими клітинами.
- Покроково: «за кожен хід персонажа всі вороги теж ходять»; додаткових ходів нема ні в кого. Уміння мають дальність у клітинах і перезарядку в ходах.
- Шкали росту в ходах: голод +1 % за 100 ходів руху поза боєм (за 200 — якщо пропускати хід), спрага +1 % приблизно за 50 ходів.
- Сон перемотує години (світ заморожено, крім скриптових подій), Rest Mode пришвидшує ходи для відновлення.
- Видимість: вороги помічають лише в межах свого поля зору; глобальна мапа — під туманом.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Найманець | player | HP, енергія, атрибути, біль, мораль, розсудливість, голод, спрага, інтоксикація, втома, імунітет | рух клітинами, атаки, уміння за енергію з перезарядкою |
| Частина тіла (голова, торс, 2 руки, 2 ноги) | body-part (+) | власне HP, захист, 1 травма на частину | удар влучає у випадкову частину; стадії 50/25/0 %; у звірів — лапи замість рук |
| Люди, нежить, прозеліти | enemy | поле зору, стан тривоги | Unaware → Suspicious (іде туди, де бачив/чув) → Hostile (атакує, доки не загине або не втратить з поля зору) |
| Територіальні звірі (ведмеді, кабани, вовки) | enemy | — | спершу попереджають; ворожі, якщо стоїш довго або близько |
| Бос | boss | — | не робить і не отримує атак з нагоди |
| Палаюча клітина | hazard | 2 ходи | займається від Set Aflame |
| Пастка, таємний прохід | hazard / static | прихована | відкривається вмінням Examine Surroundings у межах зору |
| Ящик, двері, бочка | object | — | ламаються; злам завжди шумить |
| Ліжко (таверна, табір, спальник) | static | ціна, −втоми за годину | сон і збереження |
| Караван | vehicle (+) | дальність, швидкість, перезарядка, склад 200–800 слотів | їде на відвідану клітину глобальної мапи за фураж |
| Послідовник (Darrel, Alda, Leif) | ally | перки, торгівля | живе при каравані, до 3, у підземелля не ходить |
| Поселення | zone | — | торгівля зі складу каравану — табір у межах 2 клітин |
| Фураж | resource | — | витрачається на переїзд каравану |
| Зілля, алкоголь, трави | pickup | +інтоксикація / ± біль / ± мораль | лікують, знімають біль ціною інтоксикації |
| Протиотрута, антитоксин, ланцет | pickup | −інтоксикація | знижують інтоксикацію |
| Шина, цілюща мазь | pickup | — | пришвидшують одужання травм |
| Їжа, напої | pickup | −голод/спрага, мораль від різноманіття | переїдання дає ситість, їжа під ситістю — нудоту |
| Паперова мапа | pickup | — | показує частину глобальної мапи, але не відкриває клітини |

## Правила (КОЛИ → ЯКЩО → ТО)
Хід і бій:
- КОЛИ `turn_end(player)` → ТО `custom: «кожен ворог на мапі робить хід»`.
- КОЛИ `input(attack, target)` → ЯКЩО `prob(accuracy)` → ТО `custom: «перевірка fumble, потім крит»`, `damage(target, n)`; fumble → `custom: «½ шкоди, без вторинних ефектів»`; крит → `custom: «× Crit Efficiency + бонус зброї»`.
- КОЛИ `custom: «влучання»` → ТО `damage(target, n)` і `damage(random_body_part, n)`; захист — `custom: «лише захист ураженої частини (голова/груди/руки/ноги) за типом шкоди»`.
- КОЛИ `custom: «атака по тому, хто блокує»` → ЯКЩО `prob(block_chance)` → ТО `custom: «Block Power поглинає фізичну шкоду 1:1, магію/природу — 0.66»`; щит втрачає міцність.
- КОЛИ `custom: «отримав / ухилився / заблокував удар впритул»` → ЯКЩО `prob(counter_chance)` → ТО `damage(attacker, basic)`.
- КОЛИ `leave(player, cell)` → ЯКЩО `adjacent_count(player, melee_enemy, >=, 1)` and `prob(50)` → ТО `damage(player, n)` (атака з нагоди; Disengage — 25 %; лише звичайний рух; боси не беруть участі).
- КОЛИ `input(dash, tile)` → ЯКЩО `custom: «дальність 4 − кількість сусідніх ворогів, мінімум 2»` → ТО `move(player, tile)`; ЯКЩО `adjacent_count(player, enemy, >=, 1)` → ТО `set_state(player, dodge_counter_up, 2)`.
- КОЛИ `input(leg_sweep)` → ТО `damage(three_adjacent_cells, 7)`, ЯКЩО `prob(85)` → ТО `set_state(target, immobilized)`; далі `move(player, adjacent)`.
- КОЛИ `input(set_aflame, tile)` → ЯКЩО `occupied(tile, target)` → ТО `damage(target, 8 fire + 8 crushing)`, ЯКЩО `prob(15)` → ТО `set_state(tile, burning, 2)`; ЯКЩО `free(tile)` → ТО `set_state(tile, burning, 2)`; не підпалило → `custom: «перезарядка −2 ходи»`.
- КОЛИ `input(attack, target)` → ЯКЩО `state(target, unaware)` → ТО `custom: «+33 % шкоди зброєю»` (Element of Surprise).

Травми і біль:
- КОЛИ `counter(part_hp, <=, 50%)` → ТО `set_state(part, mild_injury)`; `<= 25%` → `set_state(part, injury)`; `<= 0` → `set_state(part, severe_injury)` (одна травма на частину).
- Ноги: −опір руху, −ухилення, −енергія, +ліміт болю; тяжка — броню на нозі не зняти, 25 % знерухомлення. Руки: −влучність, −контратака, +fumble; тяжка — `take(player, item_in_hand)` і зброю в цю руку не взяти. Голова тяжка — `custom: «без заклять, без регенерації енергії, шанс коми»`. Торс тяжкий — КОЛИ `turn_end(player)` → ЯКЩО `prob(p)` → ТО `set_state(player, bleeding)`.
- КОЛИ `custom: «удар по вже пораненій частині»` → ЯКЩО `prob(bleed − resistance)` → ТО `set_state(target, bleeding)` (так само для ворогів); Cauterize Wounds → `clear_state(player, bleeding)`, `custom: «частина −5 %, +10 % болю на 240 ходів»`.
- КОЛИ `counter(part_hp, >=, 60% | 35% | 10%)` → ТО `custom: «травма стадії mild | medium | severe стабілізується»`; стабілізована тяжка на 25 % стає «injury», на 50 % — «mild»; на 90 % травма зникає.
- КОЛИ `custom: «будь-яке лікування»` → ТО `heal(player, n)`, `custom: «спершу загальне HP до порогу, решта — порівну між пошкодженими частинами»`; пошкоджені частини знижують максимум HP.
- КОЛИ `custom: «шкода або нестабілізована травма»` → ТО `counter(pain, +n)`; ліміт болю — невидима стеля (25 % при повному HP, +0.75 % за кожен відсоток втраченого HP, + травми).
- КОЛИ `counter(pain, >=, 25% | 50% | 75%)` → ТО `set_state(player, pain | strong_pain | pain_shock)`: + fumble, + отримана шкода, − лікування, щотіку − розсудливість і мораль.
- КОЛИ `input(move, dir)` → ЯКЩО `state(player, pain_shock)` and `prob(p)` → ТО `move(player, random_tile)` (спотикання); Near Death — `custom: «макс. HP падає раз на кілька ходів»`.

Потреби і психіка:
- КОЛИ `timer(100)` → ЯКЩО `custom: «рух поза боєм»` → ТО `counter(hunger, +1)`; пороги 25/50/75 % → `set_state(player, hunger | terrible_hunger | starvation)`; спрага — так само з темпом ~50 ходів.
- КОЛИ `input(eat, food)` → ЯКЩО `custom: «їжа знімає більше голоду, ніж є»` → ТО `set_state(player, satiety, dur)` (голод не росте); ЯКЩО `state(player, satiety)` → ТО `set_state(player, nausea)`.
- КОЛИ `input(drink, potion | alcohol)` → ТО `counter(intoxication, +n)`; КОЛИ `turn_end(player)` → ЯКЩО `counter(immunity, >, 0)` → ТО `counter(intoxication, -n)`; пороги 25/50/75 %.
- КОЛИ `custom: «рух клітиною, атака, блок, ухилення, вміння»` → ТО `counter(fatigue, +n)` (вміння +1.5 % від вартості енергії, закляття +2.5 %); кожен 1 % втоми → −0.75 % стелі енергії; пороги 25/50/75 %.
- КОЛИ `custom: «умова стану психіки триває (квадрант морал × розсудливість і ситуація)»` → ТО `counter(psyche_progress, +n)`; КОЛИ `counter(psyche_progress, >=, full)` → ТО `set_state(player, psyche_state)` з бафами/дебафами.
- Квадранти: висока мораль + висока розсудливість → Optimism / Heroism / Second Wind; висока + низька → Megalomania / Frenzy / Death Wish; низька + низька → Paranoia / Delirium / Catharsis; низька + висока → Pessimism / Anxiety / Panic (стовпці: нема ворогів · високе HP і кілька ворогів · низьке HP і ворог поруч).
- КОЛИ `custom: «вбив людину»` → ТО `counter(sanity, -n)`; вбив нежить → `counter(sanity, +n)`; одноманітна їжа → `counter(morale, -n)`.

Тривога, сон, караван:
- КОЛИ `in_range(enemy, player, vision)` → ЯКЩО `prob(spot)` (броня, стелс, укриття) → ТО `set_state(enemy, suspicious | hostile)`; suspicious → `move(enemy, last_seen_or_heard)`.
- КОЛИ `input(sleep, bed)` → ТО `custom: «+N годин, світ заморожено»`, `counter(fatigue, -6..-18% за годину)`, `custom: «збереження гри»`; голод і спрага ростуть далі; спати на землі не можна.
- КОЛИ `input(send_caravan, tile)` → ЯКЩО `custom: «клітина відвідана; не підземелля, не POI, не дорога, не вода»` and `has(player, fodder)` → ТО `teleport(caravan, tile)`, `take(player, fodder)` (за відстанню й біомами), `timer(cooldown)`.
- КОЛИ `input(trade, stash)` → ЯКЩО `in_range(caravan, settlement, 2)` → ТО `window(shop-window)`.
- КОЛИ `enter(player, map_tile)` (пішки) → ЯКЩО `prob(p)` → ТО `custom: «випадкова подія: вовки, засідка»`.
- Перемога: нема фіналу пісочниці (сюжетна лінія — в розробці). Поразка: HP = 0 → смерть; в Ironman — остаточна. Рахунок: нема.

## Керування і ввід
- Покроковий ввід: крок на сусідню клітину, атака по цілі, вміння з типом цілі — **Target Tile** (клітина), **Target Object** (сутність), **Target Area** (зона), **No Target**.
- `M` — глобальна мапа; Rest Mode — швидкий відпочинок після бою; сон — вибір кількості годин у ліжку.
- Розкладка клавіш і миші — див. «Непевне».

## Вікна, меню, HUD
- `main-menu` → `character-select` (готові персонажі) → `game-screen`.
- `game-screen`: локація, HP, енергія, стани (біль, травми, психіка, голод тощо).
- Вікно персонажа з вкладкою **Health** (`+window:health-tab`): смуги здоровʼя кожної частини тіла (`+ui:paper-doll`).
- `+window:skills-window` — 20 гілок умінь; `+window:crafting-window` (відкриває вміння Crafting); `inventory-window`.
- `map-window` (`M`) — глобальна мапа з туманом, знаками питання від чуток NPC.
- `shop-window` — торгівля з NPC і послідовниками; `+window:stash-window` — склад каравану; `upgrade-window` — книга апгрейдів каравану (4 вкладки: Provision, Restoration, Traveling, Communication).
- `+window:sleep-dialog` — скільки годин спати (максимум росте з годинами без сну й утомою).
- `end-screen` — смерть.
- Переходи: game-screen ⇄ map-window / inventory / health-tab / skills; ліжко → sleep-dialog → збереження → game-screen.

## Фічі поза полем
- `+feature:save-at-bed`: зберегтись можна лише сном у ліжку; «Save and exit» робить швидкий сейв, що видаляється після завантаження.
- `mode-hardcore` — Ironman: рішення незворотні, смерть остаточна.
- Караван: 25 апгрейдів (24 реалізовані), склад 200 → 400 → 600 → 800 слотів, послідовники (до 3, найм 1000 крон) з перками (розвідка точок інтересу в радіусі 6 клітин кожні 5 днів, −10 % фуражу, ремонт тощо).
- Контракти, репутація, торгівля з попитом/пропозицією, злочини й покарання, полювання на скарби; early access з 2020 (глобальна мапа за описом Steam — ~40 % готова).

## Варіації й родичі
- Родичі в корпусі: [ivan](ivan.md) (тіло з частин), [cataclysm-dark-days-ahead](cataclysm-dark-days-ahead.md) (частини тіла, переломи, потреби), [quasimorph](quasimorph.md) (рани кінцівок, інфекція), [adom](adom.md) і [caves-of-qud](caves-of-qud.md) (глобальна мапа + локації), [dungeon-crawl-stone-soup](dungeon-crawl-stone-soup.md) (класичний бій).
- Осі варіацій: **модель тіла** (одне HP / HP + випадкова частина / прицільна частина) · **психіка** (нема / одна шкала / дві шкали × ситуація → стан) · **збереження** (будь-де / лише в ліжку / Ironman) · **база** (місто / пересувний караван).

## Цікавинки для курсу
- Удар = шкода загальному HP + випадковій частині тіла; стадії 50/25/0 % з **гістерезисом** стабілізації (60/35/10 %, зникнення на 90 %) — 🥉.
- Біль як % від стелі з невидимим лімітом; Pain Shock — «спотикання» на випадкову клітину під час руху — 📎.
- Психіка: дві шкали × три зважені компоненти (50/35/15 %), стан = квадрант × ситуація (12 станів) через невидимий лічильник прогресу — 🥈 (машина станів таблицею).
- Атака з нагоди: 50 % при виході з сусідства ворога ближнього бою, 25 % з Disengage — 🌱.
- Set Aflame: підпал клітини на 2 ходи (15 % по цілі, гарантовано на порожній), невдача скорочує перезарядку — 📎.
- Караван-база: переїзд на відвідану клітину мапи за фураж (відстань, біоми), перезарядка — 🥉.
- Збереження лише сном у ліжку — 🌱.

## Мапа на каталог
- Є: `hp-damage` · `status-effects` (кровотеча, знерухомлення, бафи психіки) · `hunger-clock` · `inventory` + `inventory-items` + `inventory-limit` (склад у слотах) · `item-pickup` · `dungeon-generation` · `fog-of-war` (глобальна мапа) · `map-window` · `shop-catalog` + `round-currency` (крони) · `permadeath` (Ironman) · `unit-xp-skills` (досвід за вбивства) · `destructible-blocks` (ящики, двері, бочки) · `character-select`.
- **Нема** → пропозиції карток:
  - `+body-part-targeting` «Удар влучає в частину тіла» · entities/combat · 🥉 · слот {pick: random|aimed}; `+limb-disable` «Тяжка травма вимикає функцію частини» · entities/state · 🥉.
  - `+injury-stages` «Стадії травм із гістерезисом стабілізації» · entities/state · 🥉 · слоти {thresholds, stabilize}.
  - `+pain-meter` «Біль як окрема шкала з ефектами» · entities/state · 📎; `+intoxication-meter` · 📎; `+fatigue-pool` · 📎.
  - `+morale-states`, `+sanity-meter`, `+psyche-quadrant-states` «Стан психіки за квадрантом двох шкал і ситуацією» · entities/state · 🥈.
  - `+attack-of-opportunity` «Удар, коли виходиш із сусідства» · entities/combat · 🌱 · слот {chance}.
  - `+fumble-crit-roll` «Послідовність кидків: влучання → fumble → крит» · entities/combat · 📎; `+block-power-pool` · 📎; `+damage-type-resistances` · 🥉.
  - `+tile-ignite` «Підпал клітини на N ходів» · entities/interact · 📎; `+dash-charge` «Ривок до клітини з дальністю, що падає від сусідів» · entities/move · 🌱.
  - `+stealth-alertness` «Стани тривоги ворога: не помітив → підозрює → ворожий» · entities/move · 🥉; `+noise-lure` · 📎.
  - `+mobile-base-caravan` «Пересувна база на мапі світу» · levels/progression · 🥉; `+follower-perks` · 📎.
  - `+save-at-bed` «Збереження лише в ліжку» · game-logic/save · 🌱; `+rest-mode` «Прискорений відпочинок» · game-logic/save · 🌱; `+classless-skill-trees` · 🥉.

## Пропозиції до словників
- `+role:body-part` — частина тіла з власним HP, захистом і травмою.
- `+role:vehicle` — караван: пересувна база-сутність на мапі світу.
- `+trigger:noise` — дія створила шум (злам, бій, крик), ворог чує.
- `+cond:alert(a, level)` — рівень тривоги ворога (unaware / suspicious / hostile).
- `+effect:stabilize(part)` — травма перестає давати біль і стадію (поріг стабілізації).
- `+effect:stumble` — рух у випадкову клітину замість обраної.
- `+window:health-tab`, `+window:skills-window`, `+window:crafting-window`, `+window:sleep-dialog`, `+window:stash-window` — див. «Вікна».
- `+ui:paper-doll` — смуги частин тіла; `+ui:fatigue-bar` — шкала втоми.
- `+feature:save-at-bed` — збереження лише сном.
- `+axis:injury-model` — single-hp · hp+random-part · hp+aimed-part.

## Джерела
- ⭐ [Stoneshard Wiki: Injuries & Pain](https://stoneshard.com/wiki/Injuries_%26_Pain) — частини тіла, стадії й ефекти травм, стабілізація, біль, ліміт болю, лікування, кровотеча.
- [Steam](https://store.steampowered.com/app/625960/Stoneshard/) — покрокові «Tactical Battles», біль/інтоксикація, мораль/розсудливість, караван, Ironman, 216+ умінь, early access 6.02.2020, Ink Stains Games / HypeTrain Digital.
- [Combat Formulas](https://stoneshard.com/wiki/Combat_Formulas) — порядок ходів, влучність, fumble/крит, блок, захист по частинах, 13 типів шкоди, атаки з нагоди.
- [Psyche](https://stoneshard.com/wiki/Psyche) · [Hunger, Thirst & Intoxication](https://stoneshard.com/wiki/Hunger,_Thirst_%26_Intoxication) · [Fatigue & Resting](https://stoneshard.com/wiki/Fatigue_%26_Resting) — шкали, пороги, сон і збереження.
- [Caravan & Followers](https://stoneshard.com/wiki/Caravan_%26_Followers) · [Global Map](https://stoneshard.com/wiki/Global_Map) · [Noise & Stealth](https://stoneshard.com/wiki/Noise_%26_Stealth) — караван, мапа 38×35, тривога ворогів.
- [Athletics](https://stoneshard.com/wiki/Athletics_(skill_tree)) · [Basic Skills](https://stoneshard.com/wiki/Basic_Skills_(skill_tree)) — уміння з ціллю «клітина», дальність, перезарядка.

## Непевне
- (?) Сітка: вікі підтверджує клітини (Target Tile, дальність 1–4, «3 сусідні клітини», «випадкова клітина» при спотиканні), але не каже прямо, чи рух 8-напрямковий (вважаю квадратну сітку з діагоналями).
- (?) Розкладка керування (миша/клавіатура, гарячі клавіші вмінь) — відкриті сторінки не описують, крім `M`.
- (?) Ефекти станів голоду/спраги/інтоксикації на порогах 50–75 % — вікі лише називає стани.
- (?) Числові пороги моралі й розсудливості для квадрантів — вікі їх не дає (лише «починаються близько 100 %»).
- (?) Повний реліз 1.0 — у джерелах лише early access з 2020.
- (?) Суперечність вікі: торгівля зі складу в межах 2 клітин від поселення (і +2 від перка) проти «3 клітин» у розділі складу.
