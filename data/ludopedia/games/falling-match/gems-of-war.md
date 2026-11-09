---
title: Gems of War (і Marvel Puzzle Quest)
slug: gems-of-war
aka: [GoW, Gems of War – Puzzle RPG]
family: falling-match
also: []
klass: hybrid
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 2014
platforms: [PC, iOS, Android, PS4, Xbox One, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Gems_of_War", best: true, note: "стаб: free-to-play match-3 RPG, спін-оф Puzzle Quest, Infinity Plus Two"}
  - {kind: other, url: "https://infinityplus2.freshdesk.com/support/solutions/articles/150000208326", note: "офіційна довідка: мана, Mana Surge (×2), Gem Mastery, формула шансу сплеску"}
  - {kind: other, url: "https://infinityplus2.freshdesk.com/support/solutions/articles/150000208267", note: "офіційний глосарій: Troops, Hero, Weapons, Skulls, Doomskulls, Souls, Kingdoms, Keys, Chests, Guilds"}
  - {kind: other, url: "https://community.gemsofwar.com/t/card-term-glossary-how-to-read-spells/349", note: "форум: Destroy, Explode (3×3, 70% мани), Create, Extra turn, броня/життя, Entangle, Poison"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Marvel_Puzzle_Quest", note: "Marvel PQ: загін з 3 героїв, 6 кольорів → AP, Team-Ups, обкладинки, ранги 1–6★"}
  - {kind: official, url: "https://gemsofwar.com/", note: "офіційний сайт, новини, патчі"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Gems+of+War", note: "пошук; також Marvel Puzzle Quest"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=gems+of+war+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [line-match-clear, gravity-fall, chain-reaction, cell-click, drag-drop-piece, hp-damage, status-effects, ai-opponent, turn-enforcement, explode-area, cell-transform, unit-xp-skills, character-select, world-map, map-window, round-currency, shop-window, inventory-items, online-multiplayer, async-multiplayer, end-screen, +team-loadout, +mana-pool-spells, +lead-unit-takes-hits, +mana-routing-by-order, +mana-surge-chance, +extra-turn-on-big-match, +shared-board-duel, +special-tiles, +armor-absorb, +gacha-draw, +passive-traits, +tile-countdown-threat]
proposes: ["+effect:route_mana(color)", "+effect:surge(×2)", "+effect:cast", "+cond:position(a, n)", "+cond:cooldown", "+role:troop", "+ui:troop-cards", "+ui:countdown-on-tile", "+window:team-builder", "+window:kingdom-map", "+feature:guild-events", "+feature:gacha-chests"]
author: opus
date: 2026-11-09
---

# Gems of War — Puzzle Quest з загоном: колір гему йде першому бійцю, що його потребує, черепи б'ють лідера ворога

## Суть
Покрокова дуель на спільній match-3 дошці, як у [Puzzle Quest](puzzle-quest.md); тут — лише відмінності. Замість одного героя з чотирма резервуарами мани у кожної сторони **загін бійців-карток**, кожен зі своїм кольором мани й одним закляттям. Мана від збігу йде **першому за порядком** бійцю, якому потрібен цей колір; черепи б'ють ворожого бійця на першій позиції силою атаки твого першого бійця. Тому гра — про порядок у загоні й про те, кому зараз «наливається» мана. Marvel Puzzle Quest (2013) — та сама ідея з іншим розподілом: описано в «Варіаціях». Клас `hybrid`: `cursor` на дошці + менеджмент колекції загонів.

## Поле і час
- Дошка 8×8 (?), гем шести кольорів + черепи; поповнення згори, каскади зараховуються тому, хто ходив (як PQ).
- Хід = один свап або каст закляття бійця з повною маною; збіг 4+ — додатковий хід.
- Дві лінійки бійців (твоя й ворожа) по боках дошки; у кожного бійця 4 навички: атака, броня, життя, магія.
- Поза боєм — мапа королівств, режими (квести, PvP, події гільдії), колекція карток.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Боєць (Troop) | ally | колір(и) мани, ціна закляття, атака, броня, життя, магія, трейти, рідкість | набирає ману свого кольору; повна → можна кастувати закляття |
| Герой | player | клас, рівень, зброя | боєць, якого можна поставити в загін; лише він носить зброю |
| Зброя | — | закляття | дає герою закляття замість власного |
| Ворожий загін | enemy | ті самі параметри | ходить за тими ж правилами на тій самій дошці |
| Гем кольору ×6 | tile | колір | збіг N → N мани першому бійцю з цим кольором |
| Череп | tile | — | збіг → урон ворожому першому бійцю = атака твого першого; мани не дає |
| Doomskull | tile | пульсує | череп з бонус-уроном; при збігу першим бійцем вибухає |
| Душі (Souls) | resource | — | падають з загиблих бійців; прокачка й крафт |
| Королівство | zone | рівень, сила | дає Tribute (золото), +Mastery одного кольору |
| Ключ / Скриня | pickup | тип (Gem, Gold, VIP, Glory, Event, Guild) | ключ відкриває скриню → випадкові бійці |
| Статус | — | тривалість | Entangle (черепи не б'ють, крім 4+), Poison (50% −1 життя на хід), Hunter's mark (×2 урону від черепів), Curse (гем → череп на початку ходу) |
| Гільдія | zone | статуї кольорів | статуя рівня L → +L Mastery кольору кожному члену |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swap(a, b))` → ЯКЩО `legal(swap)` → ТО `swap(a, b)` (як PQ).
- КОЛИ `pattern(match(color, n))` → ТО `clear(matched)`, `custom: «route_mana — n мани першому за порядком бійцю, що має цей колір і ще не повний»`.
- КОЛИ `pattern(match(color, n))` → ЯКЩО `not custom: «збіг рівно 4»` і `prob(surge_chance)` → ТО `custom: «Mana Surge — мана ×2»`; шанс = Mastery × 0.73 / (Mastery + 62).
- КОЛИ `pattern(match(skull, 3+))` → ТО `clear`, `damage(enemy_first, attack(own_first))`.
- КОЛИ `pattern(match(doomskull))` → ЯКЩО `custom: «збіг зроблено першим бійцем»` → ТО `explode(3x3)`, `damage(+bonus)`.
- КОЛИ `pattern(line(4+))` → ТО `extra_move`.
- КОЛИ `custom: «отримано урон»` → ТО `counter(armor, −n)`, решта → `hp(target, −n)`; «true damage» оминає броню (?).
- КОЛИ `input(cast(troop))` → ЯКЩО `custom: «мана бійця повна»` → ТО `custom: «cast — ефект закляття»`, `custom: «мана бійця = 0»`.
- Типові ефекти заклять: `clear(gems)` (Destroy — мана за знищені геми дається), `explode(3x3)` (70% мани), `spawn_at(gems, random)` (Create), `transform(color_a → color_b)`, `damage`, `heal`, `set_state(enemy, entangle|poison|hunters_mark|curse)`, `extra_move`.
- КОЛИ `turn_start(side)` → ЯКЩО `state(troop, poison)` → ТО `prob(0.5)` → `hp(troop, −1)`.
- КОЛИ `turn_start(troop)` → ЯКЩО `state(troop, curse)` → ТО `transform(random_gem → skull)`.
- КОЛИ `pattern(match(skull))` → ЯКЩО `state(attacker, entangle)` → ТО `custom: «урон 0, якщо збіг не 4+»`.
- КОЛИ `hp_zero(troop)` → ТО `disappear_a`, `custom: «наступний боєць стає першим»`, `spawn(souls)`.
- КОЛИ `all_gone(enemy_troops)` → ТО `win`, нагороди (золото, душі, ключі, слава); КОЛИ `all_gone(own_troops)` → ТО `lose`.
- КОЛИ `custom: «нема ходів»` → ТО `custom: «reshuffle»` (як PQ).
- Мета: `custom: «Tribute — королівства періодично дають золото»`; КОЛИ `input(open_chest)` → ЯКЩО `has(key)` → ТО `take(key)`, `give(random_troop)`.
- Перемога: знищено весь ворожий загін. Поразка: знищено весь свій. Рахунок: нагороди й рейтинг PvP.

## Керування і ввід
- Свайп/drag гему на сусіда (мобільні, Switch), клік-клік мишею (PC), курсор на геймпаді.
- Тап по картці бійця з повною маною → каст; ціль для заклять, що потребують її, — тап по ворогу.
- Поза боєм: drag карток у слоти загону (порядок важливий).

## Вікна, меню, HUD
- `game-screen` (бій): дошка в центрі, по боках `custom: «troop-cards»` — стовпці карток з шкалами мани, броні й життя, іконками статусів; `turn-indicator`, `popup-text` урону й «Extra Turn».
- `custom: «team-builder»` — колекція бійців, 4 слоти (?), банер, вибір зброї героя.
- `custom: «kingdom-map»` — мапа королівств з квестами й челенджами; `map-window`.
- `shop-window` (скрині, ключі), `inventory-window` (колекція), `stats-window` героя (Mastery за кольорами).
- `leaderboard` PvP, `lobby-window` гільдії, `end-screen` з нагородами.

## Фічі поза полем
- Колекція бійців 7 рідкостей (Common → Doomed), прокачка душами, крафт у Soulforge, трейти через Traitstones.
- Mastery кольорів: рівень героя (до 1 000), клас героя (до 20), статуї гільдії, королівства (до +10), пети.
- `online-multiplayer` асинхронний: PvP проти чужих загонів під керуванням AI (?); гільдійні події.
- `custom: «gacha-chests»` — ключі й скрині; `round-currency` → золото, душі, слава, геми.

## Варіації й родичі
- [puzzle-quest](puzzle-quest.md) — батько: спільна дошка, черепи, 4+ = додатковий хід, мана → закляття. [puzzle-and-dragons](puzzle-and-dragons.md) — загін і кольори, але своя дошка. [clash-of-heroes](clash-of-heroes.md), [10000000](10000000.md).
- **Marvel Puzzle Quest** (2013, Demiurge Studios): загін з 3 героїв проти до 3 ворогів; збіг кольору шкодить ворогу і дає AP (action points) свого кольору — АР спільні для загону, а не по бійцю; 6 кольорів; з 2014 — Team-Ups: одноразові здібності героїв поза загоном. Обкладинки (covers) відкривають і качають героїв; дубль героя = обкладинка рівня; ранги 1–6★. Відомо з пам'яті: б'є той член загону, у кого найбільший урон цього кольору (?); спецплитки Attack/Protect/Strike/Countdown — лічильник на гемі, що спрацює через N ходів (?); збіг 5 створює «критичну» плитку (?).
- **Осі варіацій**: куди йде мана (резервуари героя / перший боєць кольору / спільні AP загону) · хто б'є і кого (перший → першого / найсильніший кольору) · розмір загону (1 / 3 / 4) · ворог (AI / асинхронний PvP) · мета (кампанія / колекція-гача).

## Цікавинки для курсу
- Маршрутизація ресурсу за порядком загону: «перший, кому треба й хто не повний» — 🌱.
- Черепи б'ють лідера, загиблий — наступний стає першим (черга бійців) — 📎.
- Mana Surge з формулою шансу зі спадною віддачею — 🌱.
- Статуси, що змінюють дошку (Curse перетворює гем на череп щоходу) — 📎.
- Explode 3×3 з частковою маною — 🌱.
- AI, що обирає свап з урахуванням, кому піде мана і чи лишиться супернику 4+ — 🥇.
- Countdown-плитки MPQ: ворожа загроза як лічильник на гемі, що його можна зняти збігом — 🥉.

## Мапа на каталог
- Є: `line-match-clear` · `gravity-fall` · `chain-reaction` · `cell-click` · `drag-drop-piece` · `hp-damage` · `status-effects` · `ai-opponent` · `turn-enforcement` · `explode-area` (3×3) · `cell-transform` (Curse, закляття перетворення) · `unit-xp-skills` · `character-select` · `world-map` · `map-window` · `round-currency` · `shop-window` · `inventory-items` · `online-multiplayer` · `async-multiplayer` (PvP проти збережених загонів) · `end-screen`.
- **Нема** → пропозиції карток:
  - `+team-loadout` (спільна з P&D) · entities/state · 📎.
  - `+mana-pool-spells`, `+extra-turn-on-big-match`, `+shared-board-duel`, `+special-tiles`, `+armor-absorb` (спільні з PQ).
  - `+lead-unit-takes-hits` «Урон іде першому в черзі, загиблий звільняє місце» · entities/state · 📎.
  - `+mana-routing-by-order` «Ресурс кольору — першому за порядком, кому треба» · game-logic/economy · 🌱.
  - `+mana-surge-chance` «Випадкове подвоєння з шансом від прокачки» · game-logic/score · 🌱.
  - `+gacha-draw` (спільна з P&D) · game-logic/economy · 📎.
  - `+passive-traits` «Пасивні властивості бійця» · entities/state · 📎.
  - `+tile-countdown-threat` «Ворожа плитка з лічильником ходів» (MPQ) · entities/state · 🥉 (родич `+countdown-tile` Bejeweled).

## Пропозиції до словників
- `+effect:route_mana(color)` — віддати ресурс першому підхожому члену загону.
- `+effect:surge(×2)` — випадкове подвоєння ресурсу збігу.
- `+effect:cast` — повтор із PQ (закляття сутності).
- `+cond:position(a, n)` — сутність на N-й позиції загону (перший — бере урон, дає атаку).
- `+cond:cooldown` — повтор із PQ (тут як «мана не повна»).
- `+role:troop` — боєць загону-картки поза полем (не `piece`, не `ally` на клітині).
- `+ui:troop-cards` — стовпець карток загону з шкалами; `+ui:countdown-on-tile` — повтор із Bejeweled (MPQ).
- `+window:team-builder` — повтор із P&D; `+window:kingdom-map` — мапа королівств з даниною.
- `+feature:guild-events` — спільні цілі гільдії; `+feature:gacha-chests` — ключі → скрині → випадкові бійці.

## Джерела
- ⭐ [Wikipedia: Gems of War](https://en.wikipedia.org/wiki/Gems_of_War) — стаб: жанр, розробник, спін-оф PQ, консольні релізи 2015.
- [Довідка: Mana, Gem Mastery and Mana Surge](https://infinityplus2.freshdesk.com/support/solutions/articles/150000208326) — мана першому бійцю, 3/5 мани за 3/5 гемів, Surge ×2 (не для 4), формула шансу, джерела Mastery.
- [Довідка: Glossary of Terms](https://infinityplus2.freshdesk.com/support/solutions/articles/150000208267) — Troops, Hero, Weapons, Skulls (урон по першому за атакою першого), Doomskulls, Souls, Kingdoms, Keys, Chests, Guilds.
- [Форум: Card Term Glossary](https://community.gemsofwar.com/t/card-term-glossary-how-to-read-spells/349) — Destroy, Explode (3×3, 70%), Create, Extra turn, 4 навички, броня → життя, Entangle, Poison.
- [Wikipedia: Marvel Puzzle Quest](https://en.wikipedia.org/wiki/Marvel_Puzzle_Quest) — загін 3, 6 кольорів → AP, Team-Ups, обкладинки, 1–6★.
- Пошукова видача (WebSearch): Hunter's mark ×2, Curse → череп, 7 рідкостей, 4+ = додатковий хід.

## Непевне
- (?) Розмір загону 4 і дошка 8×8 — з пам'яті; джерела не дали.
- (?) Рік ПК/мобільної версії — 2014 за чергою; Wikipedia дає лише консолі 2015.
- (?) Чи мана від збігу, коли повних усіх бійців цього кольору, згорає.
- (?) PvP — бій проти AI, що керує чужим загоном (асинхронно) — з пам'яті.
- (?) MPQ: хто «на точці» за кольором, спецплитки, критична плитка за 5 — з пам'яті, Wikipedia не описує.
- (?) True damage і точні цифри доомчерепа не знайдено.
