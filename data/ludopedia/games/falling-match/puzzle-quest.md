---
title: "Puzzle Quest: Challenge of the Warlords"
slug: puzzle-quest
aka: [Puzzle Quest, PQ, "Puzzle Quest: The Legend Returns", "Puzzle Quest: Immortal Edition"]
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
year: 2007
platforms: [Nintendo DS, PSP, PC, Xbox 360, Wii, PS2, PS3, mobile, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Quest:_Challenge_of_the_Warlords", best: true, note: "match-3 як покрокова дуель з AI на спільній дошці: мана, черепи, золото/досвід, wildcard, 4+ = додатковий хід, перемішування, закляття з cooldown, броня, класи, цитадель, мапа світу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Puzzle_Quest", note: "серія: Galactrix, PQ2, Marvel, Magic: The Gathering, PQ3 (2-секундне вікно матчів)"}
  - {kind: other, url: "https://www.pocketgamer.com/puzzle-quest-challenge-of-the-warlords/review/", note: "огляд DS: дошка 8×8, 4 кольори мани (земля, повітря, вогонь, вода), черепи, монети, фіолетові зірки, класи, атрибути, цитадель"}
  - {kind: other, url: "https://strategywiki.org/wiki/Puzzle_Quest%3A_Challenge_of_the_Warlords/Gameplay", note: "StrategyWiki — механіка (бачено в пошуку; WebFetch 403)"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=Puzzle+Quest", note: "пошук; The Legend Returns, Immortal Edition"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=puzzle+quest+challenge+of+the+warlords+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [line-match-clear, gravity-fall, chain-reaction, drag-drop-piece, cell-click, hp-damage, status-effects, ai-opponent, turn-enforcement, event-points, unit-xp-skills, character-select, world-map, map-window, shop-between-levels, shop-window, inventory-items, save-game, hot-seat, online-multiplayer, end-screen, +shared-board-duel, +mana-pool-spells, +active-skill-cooldown, +extra-turn-on-big-match, +cascade-refill, +no-moves-detection, +special-tiles, +armor-absorb, +minigame-variants, +capture-enemy-learn-skill, +citadel-buildings]
proposes: ["+trigger:spell_cast", "+effect:reshuffle", "+effect:cast", "+cond:cooldown", "+role:opponent-hero", "+window:battle-setup", "+window:citadel-window", "+feature:minigame-variants"]
author: opus
date: 2026-11-09
---

# Puzzle Quest — match-3 як покрокова дуель: обидва бійці по черзі свапають на одній дошці, кольори дають ману, черепи — урон

## Суть
Гравець і AI-супротивник **по черзі** міняють місцями два сусідні камені на спільній дошці 8×8, складаючи 3+ однакових. Кольорові камені наповнюють ману того, хто склав збіг; черепи бʼють супротивника напряму; монети й фіолетові зірки дають золото і досвід. Збіг 4+ дає **додатковий хід**, а мана витрачається на закляття (урон, зміна дошки, статуси). Над дуелями — RPG: клас, рівні, спорядження, мапа світу, квести, цитадель. Головне відкриття — дошка спільна: кожен твій хід лишає позицію супернику, тож гра — про те, що ти **не** відкриваєш йому. Клас `hybrid`: `cursor` на дошці + `avatar` (герой) на мапі світу.

## Поле і час
- Дошка 8×8 (PocketGamer), поповнюється згори після зникнень.
- Покрокова: хід = один свап (або закляття + свап); каскади, що виникли після ходу, зараховуються тому, хто ходив.
- Дві шкали в кожного бійця: HP, броня (поглинає урон першою) і 4 резервуари мани (червона, синя, зелена, жовта).
- Поза боєм — граф локацій на мапі світу (вузли й дороги), час не тече між ходами.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець (герой) | player | клас, рівень, HP, броня, мана×4, атрибути, закляття, спорядження | ходить по черзі з AI; свап або закляття |
| Супротивник | enemy | HP, мана, закляття, рівень | той самий набір дій, що й гравець, на тій самій дошці |
| Камінь мани ×4 кольори | tile | колір (земля, повітря, вогонь, вода) | збіг → мана кольору тому, хто склав |
| Череп | tile | — | збіг → прямий урон супернику |
| Череп +5 | tile | — | як череп, але сильніший |
| Монета | tile | — | збіг → золото |
| Фіолетова зірка | tile | — | збіг → досвід |
| Wildcard | tile | — | матчиться з будь-яким кольором; зʼявляється після збігу 5 |
| Закляття | — | ціна в мані, cooldown, ефект | урон, зміна дошки (прибрати всі камені типу), статус (stun = пропуск ходу суперника) |
| Броня | — | очки | поглинає урон до HP |
| Мапа світу | zone | локації, дороги | рух між вузлами; вороги на дорогах блокують прохід |
| Цитадель | — | будівлі за золото | кузня, бестіарій (вчити закляття з полонених), стайня (навчання маунтів) |
| Компаньйон | ally | бонус | дає бонуси в бою, впливає на сюжет |
| Маунт | pickup | бонус | приручений полонений; дає бонус у бою (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ЯКЩО `custom: «на дошці нема жодного ходу на 3»` → ТО `custom: «reshuffle — дошка скидається для обох»`.
- КОЛИ `input(swap(a, b))` → ЯКЩО `legal(swap)` (сусіди по горизонталі/вертикалі) → ТО `swap(a, b)`; без збігу хід не приймається (?).
- КОЛИ `pattern(match(color, 3+))` → ТО `clear(matched)`, `counter(mana[color], +n)` для `turn_of(side)`.
- КОЛИ `pattern(match(skull, 3+))` → ТО `clear`, `damage(opponent, n)`; +5-череп — більше.
- КОЛИ `pattern(match(coin, 3+))` → ТО `currency(+n)`; КОЛИ `pattern(match(star, 3+))` → ТО `counter(xp, +n)`.
- КОЛИ `pattern(line(4+))` → ТО `extra_move` тому, хто склав.
- КОЛИ `pattern(line(5))` → ТО `spawn_at(wildcard, board)`.
- КОЛИ `after(clear)` → ТО `fall(tiles_above)`, `spawn_at(random_tile, top)`; КОЛИ `settled` → ЯКЩО `pattern(match(3+))` → ТО ще збіги на рахунок того ж бійця, `combo(+1)`.
- КОЛИ `input(cast(spell))` → ЯКЩО `has(caster, mana ≥ cost)` і `custom: «закляття не на cooldown»` → ТО `custom: «cast — ефект закляття»`, `take(caster, mana)`, `set_state(spell, cooldown, n_turns)`.
- КОЛИ `custom: «cast(stun)»` → ТО `skip_turn(opponent)` (два ходи поспіль).
- КОЛИ `custom: «cast(board_spell)»` → ТО `clear(all_of_type)` або `transform(tiles)` (?).
- КОЛИ `custom: «отримано урон»` → ЯКЩО `has(target, armor)` → ТО `counter(armor, −n)`; решта → `hp(target, −n)`.
- КОЛИ `hp_zero(opponent)` → ТО `win`, `give(player, xp+gold)`.
- КОЛИ `hp_zero(player)` → ТО `lose` без штрафу (досвід лишається); бій можна переграти.
- КОЛИ `turn_end(side)` → ЯКЩО `not has(side, extra_move)` → ТО `pass_turn`.
- КОЛИ `counter(xp, ≥, threshold)` → ТО `counter(level, +1)`, `choose(attribute_points)`.
- КОЛИ `enter(player, road)` → ЯКЩО `occupied(road, enemy)` → ТО `window(battle)`.
- КОЛИ `enter(player, quest_location)` → ТО `window(battle)` (одна чи кілька дуелей); перемога → `unlock(next_locations)`.
- КОЛИ `input(capture)` → ЯКЩО `custom: «умова полону виконана»` → ТО `custom: «міні-гра-пазл; успіх → полонений у бестіарії»`.
- Цитадель: `input(build)` → ЯКЩО `has(gold, cost)` → ТО `take(gold)`, `unlock(building)`.
- Перемога в бою: HP ворога = 0. Поразка: твоє HP = 0. «Рахунок» — XP/золото й прогрес квестів.

## Керування і ввід
- DS: стилусом торкнутись і перетягнути камінь на сусіда; PC/консолі — курсор і кнопка або миша (клік-клік).
- Закляття — кнопки/іконки збоку від дошки; каст до свапу, тим самим ходом.
- AI ходить сам у свою чергу; гравець бачить його вибір (анімація свапу).

## Вікна, меню, HUD
- `main-menu`: Quest (кампанія) · Quick Battle (?) · Multiplayer · Options.
- `character-select` — клас (Druid, Knight, Warrior, Wizard; +Bard, Rogue, Ranger, Warlock у доповненні), стать/портрет (?).
- `map-window` — мапа світу Етерії: міста, дороги, квест-маркери; рух по вузлах.
- `custom: «battle-setup»` перед боєм: портрети, рівні, (?) вибір заклять.
- `game-screen` (бій): дошка 8×8 у центрі, по боках — портрети, `hp-bar`, броня, 4 шкали мани, `skill-bar` закляття з cooldown, `turn-indicator`, `popup-text` урону.
- `custom: «citadel-window»` — будівлі цитаделі: кузня, бестіарій, стайня, вежа магії.
- `shop-window` (міста), `inventory-window` (спорядження), `stats-window`/`stat-panel` (атрибути), `custom: «quest-log»`.
- `end-screen` бою: здобуті XP/золото → назад на мапу.

## Фічі поза полем
- Прогресія: `xp-level`, розподіл очок атрибутів (бойові, хитрість, мораль, 4 магії), спорядження, закляття за рівнем і з полонених.
- `world-map`, квести (основні й побічні), компаньйони.
- Міні-ігри-варіанти дошки (цитадель): полон ворога, навчання маунта, кування, вивчення заклять — `custom: «minigame-variants»`.
- `mode-versus` (DS/PSP локально, Xbox Live онлайн), бої дають досвід.
- `save-slots`/`autosave` (?).

## Варіації й родичі
- Challenge of the Warlords (2007, Infinite Interactive) → Revenge of the Plague Lord (доповнення: 4 класи, 50 заклять) → Galactrix (2009, sci-fi) → Puzzle Quest 2 (2010, атака/захист) → Marvel PQ (2013, загін з трьох героїв) → Magic: The Gathering – PQ (2015, колода карт за ману) → The Legend Returns (2019) → Puzzle Quest 3 (2022, реальний час: 2-секундне вікно) → Immortal Edition (2025).
- Родичі: Bejeweled (свап-матч), Puzzle & Dragons (матч → урон загону, але дошка не спільна), Gems of War, 10000000, You Must Build a Boat (раннер + матч).
- **Осі варіацій**: дошка (спільна з ворогом / своя) · хід (покроковий / таймер) · що дає колір (мана / урон / атрибут) · бонус за довгий збіг (додатковий хід / спецкамінь) · RPG-шар (немає / класи / колода).

## Цікавинки для курсу
- Спільна дошка двох бійців по черзі: збіги й каскади зараховуються тому, хто ходив — 🥉.
- Додатковий хід за 4+ (зміна черги ходу як ефект) — 🌱.
- AI-супротивник для match-3: жадібний пошук найкращого свапу з урахуванням того, що лишиться супернику — 🥇.
- Мана за кольорами + закляття з ціною і cooldown — 📎.
- Броня поглинає урон перед HP — 🌱.
- Перемішування дошки, коли нема ходів (детекція відсутності ходу) — 📎.
- Мапа світу з вузлами, вороги на дорогах — 🥉.

## Мапа на каталог
- Є: `line-match-clear` · `gravity-fall` · `chain-reaction` · `drag-drop-piece` (стилус) · `cell-click` · `hp-damage` · `status-effects` (stun тощо) · `ai-opponent` · `turn-enforcement` · `event-points` · `unit-xp-skills` · `character-select` · `world-map` · `map-window` · `shop-between-levels` · `shop-window` · `inventory-items` (спорядження) · `save-game` · `hot-seat` (локальний versus; найближча) · `online-multiplayer` (Xbox Live) · `end-screen`.
- **Нема** → пропозиції карток:
  - `+shared-board-duel` «Двоє по черзі на одній match-3 дошці» · game-logic/opponent · 🥉.
  - `+mana-pool-spells` «Кольори → мана → закляття» · entities/state · 📎.
  - `+active-skill-cooldown` (спільна з Puzzle & Dragons) · entities/state · 📎.
  - `+extra-turn-on-big-match` «Збіг 4+ дає додатковий хід» · game-logic/opponent · 🌱.
  - `+cascade-refill` (спільна з Bejeweled/Candy Crush) · entities/spawn · 📎.
  - `+no-moves-detection` (спільна з Bejeweled) · game-logic/legality · 📎.
  - `+special-tiles` (wildcard, +5-череп) · entities/interact · 📎.
  - `+armor-absorb` «Броня поглинає урон до HP» · entities/state · 🌱.
  - `+minigame-variants` «Ті самі правила дошки з іншою ціллю» · levels/progression · 🥉.
  - `+capture-enemy-learn-skill` «Полонений ворог дає його закляття» · game-logic/economy · 📎.
  - `+citadel-buildings` «База з будівлями за золото» · game-logic/economy · 📎.

## Пропозиції до словників
- `+trigger:spell_cast` — сторона застосувала закляття/здібність (для ланцюгів реакцій).
- `+effect:reshuffle` — перемішати дошку (нема ходів; Bejeweled, PQ).
- `+effect:cast` — застосувати закляття зі списку сутності (ефект за таблицею закляття).
- `+cond:cooldown` — здібність ще перезаряджається (N ходів).
- `+role:opponent-hero` — ворог із тим самим набором дій, що й гравець (дзеркальний супротивник), відмінне від `enemy`/`boss`.
- `+window:battle-setup` — екран перед боєм з портретами й параметрами сторін.
- `+window:citadel-window` — база з будівлями-функціями.
- `+feature:minigame-variants` — режими-варіанти основної механіки з іншою ціллю.

## Джерела
- ⭐ [Wikipedia: Puzzle Quest: Challenge of the Warlords](https://en.wikipedia.org/wiki/Puzzle_Quest:_Challenge_of_the_Warlords) — бій на дошці по черзі, типи каменів, 4+ = додатковий хід, перемішування, закляття з cooldown, броня, класи, цитадель, мапа, квести, доповнення.
- [Wikipedia: Puzzle Quest (серія)](https://en.wikipedia.org/wiki/Puzzle_Quest) — сиквели та їхні зміни (PQ3 — 2-секундне вікно).
- [PocketGamer: огляд DS](https://www.pocketgamer.com/puzzle-quest-challenge-of-the-warlords/review/) — 8×8, мана земля/повітря/вогонь/вода, черепи, монети, зірки, стилус, класи, атрибути, stun.
- [StrategyWiki: Gameplay](https://strategywiki.org/wiki/Puzzle_Quest%3A_Challenge_of_the_Warlords/Gameplay) — бачено в пошуку (+5-череп, wildcard за 5 у ряд); сторінка віддала 403.
- YouTube: пошук «puzzle quest challenge of the warlords gameplay».

## Непевне
- (?) Правила міні-ігор цитаделі (полон — пазл «очистити дошку», кування — збирати ковадла, маунти, вивчення заклять) — з памʼяті; джерела лише підтверджують, що вони є.
- (?) Скільки урону дає череп і +5-череп; множник wildcard (×2/×3?).
- (?) Чи можна зробити свап без збігу (у Bejeweled — ні).
- (?) Відповідність кольорів мани стихіям (червона = вогонь, синя = вода, зелена = земля, жовта = повітря).
- (?) Ліміт мани за кольором; чи мана переходить між боями (ні (?)).
- (?) Пункти головного меню; маунти — бонус у бою чи швидкість на мапі.
