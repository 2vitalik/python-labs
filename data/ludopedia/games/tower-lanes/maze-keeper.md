---
title: Maze Keeper
slug: maze-keeper
aka: []
family: tower-lanes
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: both
  goal: survive
year: 2024
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2940990/Maze_Keeper/", best: true, note: "реверс-кроулер: TD + роглайк + автобатлер; процедурний лабіринт з реролом, карти монстрів і спецкарти, тотеми, авантюрист повертається сильнішим"}
  - {kind: other, url: "https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2940990&count=15&maxlength=0", note: "патчноти Steam (JSON): гнів і страх авантюриста, пастки, турелі, зілля, торговець, режими й складності, серця, Grimoire і ключі"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Maze+Keeper+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 45
mechanics: [maze-generation, hp-damage, unit-xp-skills, drop-on-death, round-currency, shop-catalog, difficulty-levels, permadeath, leaderboard, codex-window, mode-select, game-screen, end-screen, +reverse-td, +deck-draw, +auto-battle, +level-regenerate, +hero-retry-scaling, +placement-conditions, +monster-families, +run-relics-on-board, +anger-meter, +repeat-tile-falloff, +knockback, +poison-per-step, +turret-upkeep, +monster-evolve-potion, +travelling-merchant, +lives-by-difficulty, +meta-unlock-keys]
proposes: ["+trigger:run_start", "+trigger:hero_exit", "+cond:placement_rule", "+cond:higher_agility", "+effect:push_back", "+effect:reroll", "+role:hero", "+role:totem", "+ui:anger-meter", "+window:grimoire", "+window:card-pick", "+card:anger-meter", "+card:repeat-tile-falloff"]
author: opus
date: 2026-11-09
---

# Maze Keeper — ти охоронець лабіринту: став монстрів картами на клітини шляху, а авантюрист щоразу повертається сильнішим

## Суть
Реверс-кроулер: гравець не герой, а охоронець процедурного лабіринту; авантюрист сам іде від входу до виходу й автоматично бʼється з монстрами на клітинах шляху. Між забігами охоронець грає картами — ставить монстрів (що сильніший монстр, то складніша умова розміщення), пастки, підсилення й тотеми з пасивними ефектами. Авантюрист після кожної спроби набирає рівні; мета — протриматися якомога більше рівнів. Поверх TD — система «гніву»: якщо постійно вбивати його одним монстром чи на одній клітині, він лютішає.

## Поле і час
- Лабіринт — процедурна мережа клітин-тайлів шляху від входу до виходу; перед забігом розкладку можна перегенерувати скільки завгодно.
- На клітині — монстр, пастка чи тотем; поруч зі шляхом — турелі (бʼють «з-поза шляху»).
- Хід (turn) = одна спроба авантюриста: він проходить лабіринт, бʼючись з кожним монстром на шляху, може ходити по тих самих клітинах кілька разів.
- Між ходами — фаза охоронця: карти, крамниця, торговець. Бій — автоматичний.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Авантюрист | enemy (`+role:hero`) | рівень, HP, Agility, енергія, гнів | іде лабіринтом до виходу; бʼється з монстрами; між спробами росте |
| Монстр (стартові: вогонь, вода, рослина) | ally | вартість, стати, сімʼя, умова розміщення | стоїть на клітині; бʼється з авантюристом у автобою |
| Монстр підтримки | ally | — | лікує або підсилює інших монстрів |
| Дорогий монстр | ally | висока вартість | «дуже важко викликати» — сувора умова розміщення |
| Сімʼя монстрів (Mole, Mercenary, Pig, …) | — | спеціалізація | фільтр у Grimoire; Morphing Roll міняє на монстра тієї ж сімʼї |
| Тотем | pickup (`+role:totem`) | пасив на частину чи всіх монстрів | лежить на шляху; Medium — зсувається на клітину, Hard/Extreme — випадково вздовж шляху |
| Trap / TNT / Tactical Nuke | hazard | ціна | пастки на клітинах |
| Jack-in-the-box | hazard | −3 клітини | відкидає авантюриста на 3 клітини назад |
| Push Trap | hazard | −3 клітини, шкода | відкидає на 3 клітини і ранить поштовхом |
| Poisoned Trap | hazard | 2 отрути | 2 шкоди отрутою за кожен його крок |
| Лава | terrain | шкода | шкода при проході; Lava Extractor створює лаву під драконом |
| Турель | static | потребує обслуговування | атакує авантюриста з-поза шляху |
| Runic Magnet | object | — | на початку ходу авантюриста забирає випадковий тотем; ламається, коли тотем повертають |
| Slot Machine | object | 90 % програшу для авантюриста | кожне використання дає Free Spin |
| Торговець (Traveling Merchant) | neutral | охоронці | ходить лабіринтом; купує збережені дії, продає карти; охоронцями можна командувати кілька ходів |
| Вихід | static | — | дійшов авантюрист — охоронець втрачає серце |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(play_monster_card, tile)` → ЯКЩО `custom: «виконано умову розміщення монстра»` and `free(tile)` → ТО `place(keeper, monster)`; інакше `block`.
- КОЛИ `input(pack_up_tile, tile)` → ЯКЩО `custom: «є місце в запасі»` → ТО `custom: «монстр повертається в запас; далі ставиться без умови»`.
- КОЛИ `input(special_card, monster)` → ТО `custom: «посилити клітину / перемістити монстра / підняти стати»`.
- КОЛИ `contact(hero, monster)` → ТО `custom: «автобій: першим бʼє той, у кого вища Agility»`, обмін `damage(n)` до `hp_zero`.
- КОЛИ `custom: «атака без шкоди»` → ТО `custom: «вартість енергії атаки росте до кінця бою»`; нижча енергія авантюриста → Agility до −90 %.
- КОЛИ `died(monster)` → ТО `custom: «авантюрист отримує XP за поточні стати монстра»`; Catalysis Potion — лут без смерті монстра.
- КОЛИ `enter(hero, poison_trap)` → ТО `set_state(hero, poisoned)`; КОЛИ `custom: «крок отруєного»` → ТО `damage(hero, 2)`.
- КОЛИ `enter(hero, jack_in_the_box)` → ТО `custom: «push_back на 3 клітини»`; Push Trap — те саме + `damage(n)`.
- КОЛИ `enter(hero, tile_with_effect)` → ЯКЩО `custom: «клітину вже перетинали цього ходу»` → ТО `custom: «шкода клітини −10 % на 2-й раз, −20 % на 3-й»` (страх), `counter(anger, +1)`.
- КОЛИ `died(hero)` → ЯКЩО `custom: «той самий монстр / та сама клітина вбивають знову»` → ТО `counter(anger, +1)`: авантюрист сильніший, більше XP, золото до +500 %; Tranquilizer Dart — гнів ×½.
- КОЛИ `reach(hero, exit)` → ТО `lives(-1)`, `custom: «наступний хід»`.
- КОЛИ `custom: «run_start (хід авантюриста)»` → ТО `custom: «авантюрист вийшов з новим рівнем»`; Runic Magnet — `take(board, random_totem)`.
- КОЛИ `custom: «run_start»` → ЯКЩО `difficulty(medium)` → ТО `move(totem, 1)`; ЯКЩО `difficulty(hard|extreme)` → ТО `custom: «тотем — у випадкову клітину шляху»`.
- КОЛИ `custom: «потенційна шкода на шляху > HP авантюриста»` → ТО `custom: «динамічний бонус XP авантюристу»`.
- КОЛИ `input(upgrade_potion, monster)` → ТО `transform(monster, evolved)` (Cocoon → Scarachnee / Spider Queen, Gobilain → Ogrilain); Stat Bottle — назавжди +стат.
- КОЛИ `input(reroll_card)` → ТО `choose(options)` (Roll of Plenty — 18 карт на вибір; Morphing Roll — монстр тієї ж сімʼї).
- КОЛИ `counter(lives, ==, 0)` → ТО `lose`, `window(end-screen)`; Hard/Extreme — без запасних сердець (Easy +2, Medium +1).
- Перемога: нема — пережити якомога більше рівнів авантюриста (Story — цілі етапів, фінал — бій з Maze Demon) · Поразка: скінчились серця · Рахунок: рівень/очки забігу → таблиця SCORE.

## Керування і ввід
- Мишею: вибрати карту → клітину лабіринту; рерол розкладки до старту; купівля в крамниці й у торговця; запас дій (купити наперед).
- Бій і рух авантюриста — без вводу (автобатлер).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Classic · Story; `difficulty-select`: Easy / Medium / Hard / Extreme.
- `custom-window` — генерація лабіринту з кнопкою реролу перед забігом.
- `game-screen`: лабіринт, рука карт, золото (`coins`), серця (`lives`), рівень і стати авантюриста, `+ui:anger-meter`, запас дій.
- `+window:card-pick` — вибір з N карт (Roll of Plenty — 18); `shop-window` — крамниця й торговець.
- `+window:grimoire` (`codex-window`) — бестіарій монстрів з фільтрами сімей, розблокування ключами.
- `end-screen` — рівень/очки забігу; `leaderboard` SCORE.

## Фічі поза полем
- `difficulty-presets` ×4: золото, лікування, реролі, XP авантюриста, ціни, стартовий набір дій (3 / 2 / 1 / 0), поведінка тотемів, запасні серця; досягнення вимкнені на Easy.
- Story: 8 етапів з цілями, вівтарі (гарантовано після 10 реролів без них), Demon Tokens за ламання предметів.
- `meta-progression`: Keeper's Keys за високі очки → відкрити монстра в Grimoire; монстри також за умовами розміщення, вівтарями, сюжетом.
- `leaderboard-online` (SCORE), `cloud-save`, досягнення.

## Варіації й родичі
- Maze Keeper Arena (анонс, 2026) — симетричний PvP: кожен будує лабіринт і колоду, герої одночасно йдуть у чужі лабіринти.
- Родичі в сімʼї: [legend-of-keepers](legend-of-keepers.md) (реверс-кроулер, кімнати й покроковий бій), [dungeon-warfare](dungeon-warfare.md) (пастки в коридорах), [dungeon-keeper](dungeon-keeper.md), [unstoppable-gorg](unstoppable-gorg.md); за картами — [emberward](emberward.md).
- **Осі варіацій**: хто наступає — хвиля ворогів / один герой, що росте / загін героїв · як шлях — фіксований / процедурний з реролом / будуєш сам · реакція на «фарм» — нема / гнів героя (Maze Keeper) / втома.

## Цікавинки для курсу
- Герой, що повертається сильнішим після кожної спроби: крива рівнів проти економіки охоронця — 📎.
- Умови розміщення монстрів (що сильніший — то суворіша умова) — 🥉 (валідатор правил на сітці).
- Гнів за повтор «той самий монстр/клітина» + спад шкоди за повторний перетин клітини — 🥉 (антифарм-механіка).
- Автобій з ініціативою за Agility і енергією, що дорожчає без шкоди — 📎.
- Пастки-відкидання на N клітин назад шляхом і отрута за крок — 🌱 кожна.
- Тотеми, що повзуть шляхом залежно від складності — 🌱.

## Мапа на каталог
- Є: `maze-generation` ↔ процедурний лабіринт; `hp-damage`; `unit-xp-skills` ↔ рівні авантюриста; `drop-on-death` ↔ лут; `round-currency` + `shop-catalog` ↔ золото, крамниця; `difficulty-levels`; `permadeath` ↔ Hard/Extreme; `leaderboard`; `codex-window` ↔ Grimoire; `mode-select`, `game-screen`, `end-screen`.
- Уже в корпусі як `+`: `+reverse-td`, `+deck-draw`, `+auto-battle`, `+level-regenerate`, `+knockback`.
- **Нема** → пропозиції карток:
  - `+hero-retry-scaling` «Той самий ворог повертається сильнішим після кожної спроби» · game-logic/difficulty · 📎.
  - `+placement-conditions` «Умова розміщення юніта на клітині» · entities/legality · 🥉.
  - `+monster-families` «Сімʼї юнітів зі спеціалізацією» · entities/state · 🌱.
  - `+run-relics-on-board` «Реліквії-тотеми лежать на полі й можуть рухатись» · entities/state · 📎.
  - `+anger-meter` «Ворог лютішає від повторних поразок в одному місці» · game-logic/difficulty · 🥉.
  - `+repeat-tile-falloff` «Шкода клітини спадає за повторні перетини» · entities/combat · 🌱.
  - `+poison-per-step` «Отрута шкодить за кожен крок» · entities/state · 🌱.
  - `+turret-upkeep` «Вежа потребує обслуговування» · game-logic/economy · 📎.
  - `+monster-evolve-potion` «Зілля перетворює юніта на сильнішого» · entities/state · 🌱.
  - `+travelling-merchant` «Торговець ходить полем» · game-logic/economy · 📎.
  - `+lives-by-difficulty` «Запасні серця залежать від складності» · game-logic/difficulty · 🌱.
  - `+meta-unlock-keys` «Ключі за очки відкривають юнітів» · game-logic/progression · 🌱.

## Пропозиції до словників
- `+trigger:run_start` — герой починає нову спробу; `+trigger:hero_exit` — герой дійшов виходу (варіант `reach`, але з наслідком «наступна спроба»).
- `+cond:placement_rule` — виконано умову розміщення юніта; `+cond:higher_agility` — хто бʼє першим.
- `+effect:push_back` — відкинути на N клітин назад шляхом; `+effect:reroll` — перегенерувати розкладку / пропозицію карт.
- `+role:hero` — ворог-герой, що росте між спробами; `+role:totem` — реліквія на полі з пасивом.
- `+ui:anger-meter` — шкала гніву героя.
- `+window:grimoire` — бестіарій з розблокуванням; `+window:card-pick` — вибір з N карт.
- `+card:anger-meter`, `+card:repeat-tile-falloff`.

## Джерела
- ⭐ [Steam: Maze Keeper](https://store.steampowered.com/app/2940990/Maze_Keeper/) — опис жанру, процедурний лабіринт з реролом, карти монстрів і спецкарти, сімʼї, тотеми, авантюрист росте; Spaceward Games, 24.09.2024.
- [Steam News API](https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=2940990&count=15&maxlength=0) — патчноти Anger / Merchant / Toolkit / Bestiary: гнів і страх, пастки й турелі, зілля, торговець, складності, серця, Grimoire, Keeper's Keys, Arena.
- YouTube: пошук «Maze Keeper gameplay».

## Непевне
- (?) Чи лабіринт — квадратна сітка, чи граф тайлів; у джерелах лише «тайли» й «на 3 клітини назад».
- (?) Як авантюрист обирає шлях на розвилках і чи може повертатися (згадано «ходить по тих самих клітинах кілька разів за хід»).
- (?) Конкретні умови розміщення монстрів, розмір руки, джерело карт (крамниця чи добір), ціни.
- (?) Що саме роблять тотеми й як авантюрист з ними взаємодіє.
- (?) Як виглядає фаза охоронця між спробами і що відбувається, коли авантюрист гине (лише «пробує знову»).
