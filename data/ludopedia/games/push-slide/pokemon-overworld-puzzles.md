---
title: Pokémon overworld puzzles (Gen I–II, лід, валуни Strength, спінери, телепорти)
slug: pokemon-overworld-puzzles
aka: [Pokémon ice puzzles, Strength boulders, Ice Path, головоломки Покемонів]
family: push-slide
also: [roguelike]
klass: avatar
axes:
  field: layers
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: 1996
platforms: [GB, GBC]
links:
  - {kind: other, url: "https://www.ludo.guide/guide/pokemon-gold-and-silver/rising-badge-route-44-and-ice-path", best: true, note: "Ice Path покроково: ковзання послідовностями напрямків, валуни B1F скидаються вниз і допомагають льоду нижче"}
  - {kind: other, url: "https://pokemondb.net/pokebase/51/what-moves-need-make-cross-enormous-sheet-pokemon-soulsilver", note: "PokéBase: на B2F валуни — точки зупинки ковзання"}
  - {kind: other, url: "https://www.serebii.net/pokearth/johto/icepath.shtml", note: "Serebii: Ice Path — 1F, B1F, B2F, B3F; Strength і Rock Smash"}
  - {kind: other, url: "https://www.serebii.net/pokearth/kanto/1st/seafoamislands.shtml", note: "Serebii: Seafoam Islands — 5 поверхів, Surf і Strength"}
  - {kind: other, url: "https://www.serebii.net/attackdex-dp/strength.shtml", note: "Serebii: Strength «can also be used to move boulders»"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Gold_and_Silver", note: "вид згори, печери/моря, годинник реального часу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pokemon+ice+path+puzzle", note: "пошук; льодові пазли"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pokemon+strength+boulder+puzzle", note: "пошук; валуни Strength"}
stage: v1
coverage: 60
mechanics: [move-4dir, keyboard-controls, push-object, inertia-slide, stop-cell, floor-types, impassable-cells, one-way-cell, teleport, teleport-pair, button-toggle, fill-hole, stairs-levels, reach-exit, inventory-items, line-of-sight-attack, player-camera, save-game, save-single-slot, +ability-gating, +strength-gate, +cross-floor-drop, +spinner-arrow, +hidden-switch-pair, +invisible-floor, +quiz-gate, +regrowing-obstacle, +sight-line-ambush, +room-memory]
proposes: ["+effect:layer_down", "+trigger:sighted", "+card:cross-floor-drop", "+card:spinner-arrow", "+card:hidden-switch-pair", "+card:invisible-floor", "+card:quiz-gate", "+card:regrowing-obstacle", "+card:sight-line-ambush", "+card:ability-gating"]
author: opus
date: 2026-11-09
---

# Pokémon overworld puzzles — клітинний світ RPG, де прохід далі закривають лід, валуни, спінери й приховані перемикачі

## Суть
У Pokémon Red/Blue (1996) і Gold/Silver/Crystal (1999) аватар ходить строго по клітинах, а печери й зали стадіонів — це вставні клітинні головоломки. Загальна парасолька («кімнати-пазли в RPG», правила льоду, валуна, плити) вже описана в [rpg-dungeon-puzzle-rooms](rpg-dungeon-puzzle-rooms.md) і [ice-sliding-puzzles](ice-sliding-puzzles.md). Цей файл — про те, що Pokémon додає понад них: **обʼєкти, що провалюються на поверх нижче і там змінюють пазл**, мережі телепортів, приховані перемикачі зі скиданням, невидимий міст, тренери з лінією зору як рухома перешкода і **гейтинг світу здібностями (HM + бейдж)**.

## Поле і час
- Карта — сітка тайлів; аватар робить крок рівно на клітину, NPC ходять у реальному часі; без вводу пазл не змінюється (`time: realtime`, але пазли — покрокові за суттю).
- **Кілька поверхів** однієї печери (Ice Path: 1F, B1F, B2F, B3F; Seafoam: 1F–B4F) — сходи й дірки з'єднують однакові координати різних поверхів (`field: layers`).
- Камера центрована на аватарі, видно частину карти; у темних печерах без Flash видно лише клітини довкола (`info: partial`) (?).
- Стан пазла живе, доки ти на карті: вийшов — валуни на старт, зрубані дерева виросли (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Аватар (Red, Gold) | player | бейджі, HM у покемонів команди | крок на 1 клітину в 4 напрямки; взаємодія кнопкою A з клітиною попереду |
| Лід (Ice Path, Mahogany Gym) | terrain | — | ступив → ковзаєш у напрямку руху до перешкоди; керування на льоду ігнорується |
| Валун Strength | object | — | штовхається на 1, лише коли Strength активовано; не тягнеться; ланцюгом не штовхається |
| Дірка в підлозі | terrain | — | валун падає в неї й **зʼявляється на поверсі нижче** в тій самій точці; одна дірка — один валун (HGSS (?)) |
| Валун-упор на льоду (B2F) | object | — | скинутий згори валун стає точкою зупинки ковзання — відкриває новий маршрут |
| Сильна течія (Seafoam B4F) | terrain | напрям | зносить аватара на Surf; скинуті згори валуни перекривають її (?) |
| Кнопка під валун (Victory Road, Gen I) | switch | постійна | валун на ній → барʼєр (скеля) зникає назавжди (?) |
| Спінер-стрілка (Rocket Hideout, Viridian Gym) | terrain | напрям | ступив → тебе несе в напрямку стрілки до стоп-клітини або перешкоди |
| Стоп-клітина | terrain | — | зупиняє рух спінера |
| Телепорт-плита (Saffron Gym, Silph Co.) | terrain | пара | ступив → переносить на парну плиту в іншій кімнаті; мережа кімнат = граф |
| Смітники з перемикачем (Vermilion Gym) | switch | прихований | 1-й перемикач у випадковому смітнику, 2-й — у сусідньому; помилка на 2-му → обидва скидаються (?) |
| Статуя-перемикач (Pokémon Mansion) | switch | 2 стани | «натиснути» → усі двері-ґрати поверху міняють стан відкрито/закрито (?) |
| Ґрати/двері | gate | відкрито / закрито | непрохідні, коли закриті |
| Невидимий міст (Ecruteak Gym) | terrain | видимий / ні | ступив повз міст → падіння, повернення на вхід (?) |
| Автомат-вікторина (Cinnabar Gym) | gate | питання | правильна відповідь → ворота відчинено; хибна → бій з тренером (?) |
| Дерево Cut / камінь Rock Smash | static | — | знищується здібністю; дерево відростає після виходу з карти (?) |
| Вода / водоспад / вир | terrain | потрібна здібність | Surf — плисти; Waterfall — підйом; Whirlpool — прибрати вир (Gen II) |
| Тренер | enemy | напрям погляду, дальність | побачив аватара на прямій без перешкод → підходить і починає бій; переможений більше не дивиться |
| Сходи / драбина | static | — | перехід на інший поверх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(player, dir)`; інакше `block`.
- КОЛИ `enter(player, ice)` → ТО `slide(player, dir)`; КОЛИ `blocked(player)` → ТО `custom: «ковзання завершено, ввід знову приймається»`.
- КОЛИ `input(use_strength)` → ЯКЩО `has(player, badge)` and `has(party, strength)` → ТО `set_state(player, strength_on)` до виходу з карти (?).
- КОЛИ `contact(player, boulder)` → ЯКЩО `state(player, strength_on)` and `free(cell_behind)` → ТО `push`; інакше `block`, `message(«великий валун»)`.
- КОЛИ `enter(boulder, hole)` → ТО `disappear_a`, `custom: «валун зʼявляється на поверсі нижче в тій самій координаті»`, `set_cell(hole, floor)` (?).
- КОЛИ `contact(player, boulder)` на льоду нижнього поверху → ТО `block` — валун працює як стоп-клітина для `slide`.
- КОЛИ `enter(boulder, boulder_switch)` → ТО `set_state(barrier, open)` (?).
- КОЛИ `enter(player, spinner)` → ТО `custom: «рух у напрямку стрілки, доки не стоп-клітина або перешкода»`; ввід ігнорується.
- КОЛИ `enter(player, stop_tile)` → ТО `custom: «зупинити примусовий рух»`.
- КОЛИ `enter(player, warp_tile)` → ТО `teleport` на парну плиту.
- КОЛИ `input(inspect, trash_can)` → ЯКЩО `state(switch1, found)` and `custom: «у цьому смітнику другий перемикач»` → ТО `set_state(gate, open)`; ЯКЩО `state(switch1, found)` і не той смітник → ТО `custom: «обидва перемикачі переставляються, пошук заново»` (?).
- КОЛИ `input(inspect, statue_switch)` → ТО `custom: «усі ґрати поверху інвертують стан»` (?).
- КОЛИ `custom: «аватар зійшов з невидимого мосту»` → ТО `respawn(player, gym_entrance)` (?).
- КОЛИ `input(answer, quiz)` → ЯКЩО `custom: «відповідь правильна»` → ТО `set_state(gate, open)`; інакше `custom: «починається бій з тренером»` (?).
- КОЛИ `input(use_cut, tree)` → ЯКЩО `has(player, badge)` → ТО `disappear_b`; КОЛИ `custom: «аватар залишив карту»` → ТО `spawn(tree)` на місці (?).
- КОЛИ `line_of_sight(trainer, player)` → ЯКЩО `not state(trainer, defeated)` → ТО `move(trainer, to)` до аватара, `window(dialogue-window)`, `custom: «бій»`.
- КОЛИ `custom: «аватар залишив карту»` → ТО `restart` пазла карти: валуни на старт (?).
- Перемога: дійти до виходу / лідера стадіону / предмета. · Поразка: у пазлі нема; програш бою → повернення в Pokémon Center. · Рахунок: нема.

## Керування і ввід
- D-pad — крок; утримання в бік валуна — поштовх (коли Strength активний).
- A — взаємодія з клітиною попереду (оглянути смітник/статую, рубати, розбити, говорити); здібність запускається з меню покемона (Start → Pokémon → HM).
- B — скасувати; Start — меню (Pokédex, Pokémon, Bag, Save).
- На льоду й спінерах ввід ігнорується до зупинки — ключ до «ковзай до упору».

## Вікна, меню, HUD
- `game-screen`: карта без HUD; повідомлення внизу (`dialogue-window`): «Великий валун…», «Перемикач!».
- `pause-menu` (Start): Pokédex · Pokémon (тут HM-здібності поза боєм) · Bag (`inventory-window`) · Save · Option.
- `save-slots` → один слот (`save-single-slot`).
- `confirm-dialog`: «Use Strength?» / «Cut this tree?» (?).
- Переходи: карта ↔ бій з тренером (окремий екран) ↔ меню; поверх ↔ поверх через сходи/дірку.

## Фічі поза полем
- `ability-gating`: бейдж + HM-здібність відкриває типи клітин (Cut, Surf, Strength, Flash; Gen II — Rock Smash, Whirlpool, Waterfall) — світ як граф з ключами-здібностями.
- `save-game`: збереження будь-де; пазл карти при цьому не фіксується окремо (?).
- `stairs-levels`: багатоповерхові печери з пазлами, що перетікають між поверхами.

## Варіації й родичі
- [rpg-dungeon-puzzle-rooms](rpg-dungeon-puzzle-rooms.md) — парасолька (Zelda, Golden Sun, Lufia II); тріснутий лід Gen III і повні правила кімнат — там.
- [ice-sliding-puzzles](ice-sliding-puzzles.md) — лід як ціла гра; [sokoban](sokoban.md) — валуни як ціла гра; [ricochet-robots](ricochet-robots.md) — ковзання до упору як ядро; [tomb-of-the-mask](tomb-of-the-mask.md) — ковзання в аркаді.
- Пізніші покоління (з памʼяті): обертові ворота Fortree Gym (Gen III, родич турнікетів [kwirk](kwirk.md)), тріснутий лід Sootopolis, тріснута підлога під Mach Bike (?).
- **Осі варіацій**: звʼязок поверхів — нема / дірка переносить обʼєкт / дірка переносить аватара · примусовий рух — лід (напрям від входу) / спінер (напрям від клітини) · перемикач — видимий / прихований зі скиданням / інвертує всі двері · дозвіл на взаємодію — завжди / за здібністю.

## Цікавинки для курсу
- Валун провалюється на поверх нижче й стає стопом для льоду: два шари поля, зміна одного відкриває пазл іншого — 🥉 (два рівні + перерахунок графа зупинок).
- Спінери + стоп-клітини: BFS по графу «клітина зупинки → клітина зупинки» — 📎.
- Мережа телепортів-пар: граф кімнат, найкоротший шлях до лідера — 🌱.
- Приховані перемикачі-пара зі скиданням (Vermilion): випадкова розстановка + перевірка сусідства — 📎.
- Тренер з лінією зору: промінь до першої перешкоди щокроку — 🌱.
- Гейтинг світу здібностями: які клітини доступні з набором {Cut, Surf, Strength} — flood fill з масками — 🥉.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок; `push-object` ↔ валун; `inertia-slide` + `floor-types` ↔ лід; `stop-cell` ↔ стоп-клітина спінерів, валун-упор; `impassable-cells` ↔ скелі, дерева; `one-way-cell` ↔ уступи (?); `teleport` + `teleport-pair` ↔ плити Saffron; `button-toggle` ↔ статуї, кнопки під валун; `fill-hole` ↔ дірка засипана валуном; `stairs-levels` ↔ поверхи печер; `reach-exit` ↔ прохід; `inventory-items` ↔ Bag/HM; `line-of-sight-attack` ↔ тренер бачить; `player-camera` ↔ камера; `save-game` + `save-single-slot`.
- **Нема** → пропозиції карток:
  - `+cross-floor-drop` «Обʼєкт провалюється на поверх нижче» · entities/interact · 🥉 · слоти {layer_map, keep_coords}.
  - `+spinner-arrow` «Плитка примусового руху до стоп-клітини» · entities/move · 🌱 · слоти {dir}.
  - `+hidden-switch-pair` «Прихований перемикач-пара зі скиданням» · entities/interact · 📎 · слоти {neighbor_rule}.
  - `+invisible-floor` «Невидимий міст, зійшов — на старт» · entities/interact · 🌱.
  - `+quiz-gate` «Ворота-вікторина: питання → прохід або штраф» · entities/interact · 🌱 · слоти {questions, penalty}.
  - `+regrowing-obstacle` «Перешкода відновлюється після виходу з карти» · entities/state · 🌱.
  - `+sight-line-ambush` «Ворог помічає на лінії зору й підходить» · entities/combat · 🌱 · слоти {range} (родич `line-of-sight-attack`).
  - `+ability-gating` «Здібність відкриває тип клітин» · levels/progression · 🥉 · слоти {abilities, cell_types}.
  - Повтор корпусу: `+strength-gate`, `+room-memory`.

## Пропозиції до словників
- `+effect:layer_down` — сутність переходить на шар/поверх нижче в тій самій координаті (валун у дірці Ice Path).
- `+trigger:sighted` — сутність потрапила в поле зору іншої (тренер Pokémon).
- `+card:cross-floor-drop`, `+card:spinner-arrow`, `+card:hidden-switch-pair`, `+card:invisible-floor`, `+card:quiz-gate`, `+card:regrowing-obstacle`, `+card:sight-line-ambush`, `+card:ability-gating` — див. «Мапа на каталог».

## Джерела
- ⭐ [ludo.guide: Route 44 і Ice Path](https://www.ludo.guide/guide/pokemon-gold-and-silver/rising-badge-route-44-and-ice-path) — ковзання послідовностями напрямків; «Push boulders onto the floor below to aid future ice puzzles»; HM07 на 1F.
- [PokéBase: Ice Path B2F](https://pokemondb.net/pokebase/51/what-moves-need-make-cross-enormous-sheet-pokemon-soulsilver) — «slide to the left so that you hit the boulder»: валуни як точки зупинки.
- [Serebii: Ice Path](https://www.serebii.net/pokearth/johto/icepath.shtml) — поверхи 1F–B3F, Strength і Rock Smash.
- [Serebii: Seafoam Islands](https://www.serebii.net/pokearth/kanto/1st/seafoamislands.shtml) — поверхи 1F–B4F, Surf і Strength.
- [Serebii: Strength](https://www.serebii.net/attackdex-dp/strength.shtml) — «can also be used to move boulders».
- [Wikipedia: Pokémon Gold and Silver](https://en.wikipedia.org/wiki/Pok%C3%A9mon_Gold_and_Silver) — вид згори, печери/моря, годинник.

## Непевне
- (?) Bulbapedia і StrategyWiki віддають 403, Pokémon Fandom — 402: більшість деталей поза Ice Path — з памʼяті.
- (?) Поведінка Seafoam (валуни перекривають течію), кнопки Victory Road, смітники Vermilion (випадковий 1-й, сусідній 2-й, скидання), статуї Mansion, невидимий міст Ecruteak, вікторина Cinnabar — з памʼяті, не перевірено.
- (?) Скидання валунів і відростання дерев після виходу з карти; тривалість Strength «до виходу з карти».
- (?) «Одна дірка — один валун» бачив лише як переказ StrategyWiki для HGSS; для оригіналу G/S не перевірено.
- (?) Затемнення печер без Flash як `info: partial` — з памʼяті.
