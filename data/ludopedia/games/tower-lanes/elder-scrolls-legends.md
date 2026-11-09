---
title: "The Elder Scrolls: Legends"
slug: elder-scrolls-legends
aka: [TESL, "Elder Scrolls Legends"]
family: tower-lanes
also: []
klass: figure
axes:
  field: 1d
  time: turn
  opponent: online
  info: hidden
  random: both
  goal: state
year: 2017
platforms: [PC, macOS, iOS, Android]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Elder_Scrolls:_Legends", best: true, note: "правила: 30 HP, руна за кожні 5 шкоди → карта, Prophecy, магіка +1/хід до 12, перстень другого гравця, дві смуги й тіньова, типи карт, режими, закриття 2025"}
  - {kind: fandom, url: "https://elderscrollslegends.wiki.fextralife.com/Rules", note: "Fextralife: колода 50–70, ≤3 копії, Unique ×1, 1–2 атрибути, рука 3 + один перебір, Field/Shadow lane, руни й Prophecy"}
  - {kind: fandom, url: "https://elderscrollslegends.wiki.fextralife.com/Abilities", note: "12 ключових слів з точним текстом: Breakthrough, Charge, Drain, Guard, Last Gasp, Lethal, Pilfer, Prophecy, Regenerate, Shackle, Summon, Ward"}
  - {kind: fandom, url: "https://elderscrollslegends.wiki.fextralife.com/Glossary", note: "Cover, Silence, Wounded, Field/Shadow lane, 5 рун"}
  - {kind: fandom, url: "https://elderscrollslegends.wiki.fextralife.com/Attributes", note: "5 атрибутів + нейтральний, класи з двох атрибутів"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/The_Elder_Scrolls:_Legends", note: "RU: ≤4 істоти в смузі, на Арені смуги з іншими правилами й шириною 6:2 / 7:1, рівень 50, раса гравця"}
  - {kind: other, url: "https://store.steampowered.com/api/appdetails?appids=364470", note: "Steam (застосунок 364470, знятий з продажу): механіки за доповненнями — Invade, Pilfer, Wax/Wane, Consume, Plot, Exalt, Rally, Betray, Assemble, Treasure Hunt, Shout, Slay, подвійні карти"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Elder+Scrolls+Legends+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [drag-drop-piece, pocket, hp-damage, piece-capture, legal-move-highlight, status-effects, ai-opponent, online-multiplayer, rating-system, mode-select, tutorial-window, puzzle-select, shop-window, end-screen, +lane-grid, +deck-draw, +deck-builder, +card-collection, +card-keywords, +ramping-energy, +mulligan-redraw, +second-player-compensation, +retaliation, +taunt-targeting, +zone-capacity, +location-modifiers, +damage-threshold-draw, +free-play-on-draw, +untargetable-on-entry, +summoning-sickness, +excess-damage-through, +card-level-choice, +draft-mode, +rarity-copy-limit, +story-choices]
proposes: ["+trigger:card_played", "+trigger:rune_broken", "+effect:draw_card", "+effect:play_free", "+effect:silence", "+cond:in_lane", "+role:card", "+role:lane", "+ui:rune-ring", "+ui:magicka-gems", "+window:deck-builder", "+window:collection-window", "+window:draft-screen", "+feature:card-collection", "+card:damage-threshold-draw", "+card:free-play-on-draw", "+card:untargetable-on-entry"]
author: opus
date: 2026-11-09
---

# The Elder Scrolls: Legends — дві смуги, тіньова дає укриття на хід; кожні 5 втрачених HP ламають руну і можуть безкоштовно зіграти «пророцтво»

## Суть
Колекційна картярка Bethesda за всесвітом The Elder Scrolls: гравці по черзі кладуть істот у **одну з двох смуг** і атакують ними лише ворожих істот у тій самій смузі або ворожого героя. Права смуга — «тіньова»: істота, що в неї зайшла, на хід отримує Cover і не може бути атакована. Здоровʼя героя (30) поділене **рунами**: кожні 5 втраченої шкоди ламають руну, власник бере карту, і якщо вона має Prophecy — може зіграти її безкоштовно просто на ході суперника.

## Поле і час
- Поле — дві смуги (`field: 1d`): ліва Field lane без правил, права Shadow lane — Cover на хід для новоприбулих; у кожній смузі по своєму боці в кожного до 4 істот.
- Особливі смуги: в історії й на Арені одна зі смуг має свої правила (напр., Graveyard — загиблі встають скелетами); на Арені буває й інша ширина смуг (6:2, 7:1).
- Хід почерговий: взяти карту, +1 до максимуму магіки (до 12), зіграти карти, атакувати істотами, передати хід.
- Приховане: рука суперника, порядок колоди; руни — відкриті.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой (аватар) | player | 30 HP, 5 рун, раса | ціль атак; руни ламаються кожні 5 шкоди |
| Руна | mark | 1 на 5 HP | зламана — власник бере карту; Prophecy — безкоштовна гра |
| Істота | piece (`+role:card`) | ціна, атака, здоровʼя, атрибут, ключові слова | стоїть у смузі; атакує раз на хід, з наступного ходу |
| Дія (Action) | object (`+role:card`) | ціна | разовий ефект, потім у скид |
| Предмет (Item) | object (`+role:card`) | ціна, +атака/+здоровʼя | чіпляється до істоти; знищується з нею або Silence |
| Підтримка (Support) | object (`+role:card`) | ціна, використання (?) | лишається в грі з постійним або активованим ефектом |
| Подвійна карта (Isle of Madness) | object | — | тип карти з доповнення |
| Field lane | zone (`+role:lane`) | ≤ 4 істоти на бік | без правил |
| Shadow lane | zone (`+role:lane`) | ≤ 4 на бік | новоприбула істота отримує Cover на хід |
| Особлива смуга (Graveyard та ін.) | zone | правило смуги | напр., загибла істота встає скелетом |
| Магіка | resource | max +1 щоходу, до 12 | платить за карти; поновлюється щоходу |
| Перстень магіки | pickup | 3 заряди, раз на хід | +1 тимчасова магіка другому гравцю |
| Колода · рука · скид | zone | колода 50–70 (згодом до 100), рука 3 на старті | добір щоходу й за руни |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `game_start` → ТО `custom: «кожен бере 3 карти; один перебір (повернути частину й добрати)»`; другий гравець — `give(player2, ring_of_magicka)` з 3 зарядами.
- КОЛИ `turn_start(side)` → ТО `custom: «max магіки +1 (≤ 12), магіка поновлюється»`, `custom: «взяти карту»`.
- КОЛИ `input(use_ring)` → ЯКЩО `counter(ring_charges, >, 0)` and `custom: «цього ходу ще не вживали»` → ТО `counter(magicka, +1)`, `counter(ring_charges, -1)`.
- КОЛИ `input(play, creature, lane)` → ЯКЩО `counter(magicka, >=, cost)` and `count(own_creatures_in_lane, <, 4)` → ТО `place(player, creature)`, `counter(magicka, -cost)`, `set_state(creature, summoned, 1)`.
- КОЛИ `spawned(creature)` → ЯКЩО `custom: «смуга — Shadow»` and `not state(creature, guard)` → ТО `set_state(creature, cover, 1)`.
- КОЛИ `spawned(creature)` → ЯКЩО `custom: «зіграна з руки і має Summon»` → ТО `custom: «бонус-ефект карти»`.
- КОЛИ `input(attack, creature, target)` → ЯКЩО `not state(creature, summoned)` (або Charge) and `custom: «ціль — ворожа істота тієї ж смуги або ворожий герой»` and `not state(target, cover)` and `custom: «у смузі нема ворожого Guard, або ціль — Guard»` → ТО `damage(target, atk)`; ЯКЩО ціль — істота → ТО `damage(creature, target_atk)` (відповідь).
- КОЛИ `custom: «істота з Cover атакує»` → ТО `clear_state(creature, cover)`.
- КОЛИ `custom: «Breakthrough-істота атакою знищила істоту»` → ТО `damage(enemy_hero, надлишок)`.
- КОЛИ `custom: «карта з Drain завдала шкоди на своєму ході»` → ТО `heal(own_hero, ту саму кількість)`.
- КОЛИ `custom: «Lethal-істота завдала шкоди істоті»` → ТО `disappear(target)`.
- КОЛИ `custom: «істота з Ward вперше отримує шкоду»` → ТО `block`, `clear_state(creature, ward)` — разом з ефектами Lethal і Drain.
- КОЛИ `turn_start(side)` → ЯКЩО `state(creature, regenerate)` → ТО `heal(creature, повністю)`.
- КОЛИ `custom: «на істоту наклали Shackle»` → ТО `custom: «пропускає наступну атаку»`.
- КОЛИ `custom: «Silence»` → ТО `custom: «знищити всі предмети на істоті, зняти всі здібності й зміни статів»`.
- КОЛИ `hp_zero(creature)` → ТО `disappear(creature)`; ЯКЩО `custom: «має Last Gasp»` → ТО `custom: «бонус-ефект»`.
- КОЛИ `custom: «Pilfer-істота завдала шкоди ворожому героєві»` → ТО `custom: «бонус-ефект»`.
- КОЛИ `input(play, item, creature)` → ЯКЩО `counter(magicka, >=, cost)` → ТО `attach(item, creature)`, `custom: «+атака/+здоровʼя»`.
- КОЛИ `custom: «здоровʼя героя перетнуло поріг руни (25, 20, 15, 10, 5)»` → ТО `disappear(rune)`, `custom: «взяти карту»`.
- КОЛИ `custom: «карту взято з руни»` → ЯКЩО `custom: «карта має Prophecy»` → ТО `custom: «можна негайно зіграти безкоштовно, на ході суперника»`.
- КОЛИ `hp_zero(hero)` → ТО `lose`; суперник `win`.
- Збір колоди: 50–70 карт (згодом 50–100), ≤ 3 копії, Unique ×1, 1 або 2 атрибути (з Houses of Morrowind — три), двоатрибутні карти — лише в колоді свого класу.
- Перемога: здоровʼя суперника < 1 · Поразка: власне здоровʼя < 1 · Рахунок: ранг/рейтинг; Арена — перемоги до 9 (7 проти людей) або 3 поразки.

## Керування і ввід
- Миша/тач: перетягнути карту з руки в смугу (істота), на істоту (предмет) або в ціль (дія); перетягнути істоту на ціль — атака.
- Кнопка перстня магіки, кнопка кінця ходу; перебір стартової руки — вибір карт для заміни.
- Під час ламання руни — модальний вибір «зіграти Prophecy зараз / лишити в руці».

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Story, Battle (рейтингова, звичайна, тренування проти AI), Arena (соло проти AI / проти гравців), Gauntlet, Puzzle (виграти або вижити за один хід — `puzzle-select`).
- `game-screen`: дві смуги, рука, `+ui:magicka-gems`, перстень із зарядами, герой з `+ui:rune-ring`, лічильник колоди, `end-turn-button`, `legal-move-highlight` для дозволених цілей, `tooltip` ключових слів.
- `+window:deck-builder` — колода, атрибути, крива магіки; `+window:collection-window`; `shop-window` — бустери за золото.
- `+window:draft-screen` — драфт Арени; `map-window` / `dialogue-window` історії з виборами, що міняють нагородні карти (?).
- `profile-window` — рівень гравця (до 50) і раса; `end-screen` — нагороди; `tutorial-window` — історія як навчання.

## Фічі поза полем
- `xp-level`: рівень гравця дає карти за расою; деякі карти на рівні гравця пропонують вибір між двома версіями.
- `card-collection`, бустери за золото або гроші, щоденні завдання; `custom-rules` — особливі смуги в історії/Арені.
- `online-multiplayer` з рангами, `ai-opponent-levels` (тренувальні колоди), `puzzle-bank` — режим пазлів «за один хід».
- Доповнення: Heroes of Skyrim (Shout), Fall of the Dark Brotherhood (Slay), Return to Clockwork City (Assemble, Treasure Hunt), Houses of Morrowind (Plot, Exalt, Rally, Betray, три атрибути), Isle of Madness (подвійні карти, нові смуги), Moons of Elsweyr (Pilfer, Wax/Wane, Consume), Jaws of Oblivion (Invade).
- Закриття: розвиток зупинено 2019, сервери вимкнено 30.01.2025.

## Варіації й родичі
- Родичі в корпусі: [mythgard](mythgard.md) (7 смуг), [marvel-snap](marvel-snap.md) (3 локації з модифікаторами), [artifact](artifact.md) (3 дошки), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md) (смуги з типами), [gwent](gwent.md) (ряди), [solforge](solforge.md) (5 смуг навпроти), [eye-of-judgment](eye-of-judgment.md); поза сімʼєю — [faeria](../tactics/faeria.md), [duelyst](../tactics/duelyst.md) (карти на сітці).
- Поза корпусом: Hearthstone (каркас: магіка +1/хід, Guard ≈ Taunt, Charge, Ward ≈ Divine Shield).
- **Осі варіацій**: кількість смуг — 1 / 2 / 3–7 · смуга — без правил / з правилом (Cover, Graveyard) · здоровʼя — суцільне / з порогами-рунами, що дають карти · атака — будь-яку ціль / лише в смузі / навпроти.

## Цікавинки для курсу
- Руни: пороги здоровʼя, на кожному — добір карти і можлива безкоштовна гра в чужий хід — 📎 (переривання черги).
- Тіньова смуга: Cover на хід для новоприбулих, знімається атакою; Guard не може мати Cover — 🌱.
- Guard у межах смуги: атака героя дозволена лише без ворожого Guard у цій смузі — 🌱.
- Ward, що поглинає перший удар разом із Lethal і Drain — порядок застосування ефектів — 📎.
- Breakthrough: надлишок шкоди йде героєві — 🌱.
- Перстень магіки як компенсація ходу другим — 🌱.
- Збір колоди: 50–70, ≤ 3 копії, Unique ×1, атрибути класу — валідація колоди 📎.

## Мапа на каталог
- Є: `drag-drop-piece` ↔ карта в смугу · `pocket` ↔ рука · `hp-damage` · `piece-capture` ↔ загибель істоти · `legal-move-highlight` ↔ дозволені цілі · `status-effects` ↔ Cover, Shackle, Ward · `ai-opponent`, `online-multiplayer`, `rating-system` · `mode-select` · `tutorial-window` ↔ історія · `puzzle-select` ↔ режим пазлів · `shop-window` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection`, `+card-keywords`, `+ramping-energy`, `+mulligan-redraw`, `+second-player-compensation`, `+retaliation`, `+taunt-targeting`, `+zone-capacity`, `+location-modifiers`, `+draft-mode`, `+rarity-copy-limit`, `+story-choices` — уже в корпусі.
  - `+damage-threshold-draw` «Пороги здоровʼя (руни): за кожен — добір карти» · game-logic/economy · 📎.
  - `+free-play-on-draw` «Карта, взята в особливу мить, грається безкоштовно в чужий хід» · game-logic/opponent · 📎.
  - `+untargetable-on-entry` «Укриття на хід для щойно виставленої фігури» · entities/state · 🌱.
  - `+summoning-sickness` «Виставлена фігура атакує лише з наступного ходу (Charge — виняток)» · entities/legality · 🌱.
  - `+excess-damage-through` «Надлишок шкоди переходить на героя» · entities/combat · 🌱.
  - `+card-level-choice` «Карта на рівні гравця обирає одну з двох версій» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:card_played` — повтор; `+trigger:rune_broken(side)` — здоровʼя перетнуло поріг руни.
- `+effect:draw_card` — повтор; `+effect:play_free(card)` — зіграти без ціни поза чергою; `+effect:silence(a)` — зняти всі здібності й предмети.
- `+cond:in_lane(a, lane)` — сутність у вказаній смузі / та сама смуга, що в B.
- `+role:card` · `+role:lane` — повтори.
- `+ui:rune-ring` — здоровʼя з поділками-рунами; `+ui:magicka-gems` — кристали ресурсу (поточний/максимум).
- `+window:deck-builder`, `+window:collection-window`, `+window:draft-screen` — повтори.
- `+feature:card-collection` — повтор.
- `+card:damage-threshold-draw`, `+card:free-play-on-draw`, `+card:untargetable-on-entry`.

## Джерела
- ⭐ [Wikipedia: The Elder Scrolls: Legends](https://en.wikipedia.org/wiki/The_Elder_Scrolls:_Legends) — 30 HP, руна на 5 HP → карта, Prophecy, 3 карти на старті, магіка +1 до 12, перстень (3 рази), дві смуги й Shadow Lane, типи карт, відповідь у бою, режими Battle/Arena/Story/Puzzle/Gauntlet, дати й закриття.
- [Fextralife: Rules](https://elderscrollslegends.wiki.fextralife.com/Rules) — колода 50–70, 1–2 атрибути, ≤ 3 копії, Unique ×1, перебір руки, Field/Shadow lane, руни.
- [Fextralife: Abilities](https://elderscrollslegends.wiki.fextralife.com/Abilities) — точні тексти 12 ключових слів.
- [Fextralife: Glossary](https://elderscrollslegends.wiki.fextralife.com/Glossary) — Cover, Silence, Wounded, 5 рун · [Attributes](https://elderscrollslegends.wiki.fextralife.com/Attributes) — п'ять атрибутів і нейтральний.
- [Wikipedia RU](https://ru.wikipedia.org/wiki/The_Elder_Scrolls:_Legends) — ≤ 4 карти в смузі, смуги Арени, раса й рівень 50, доповнення.
- [Steam appdetails 364470](https://store.steampowered.com/api/appdetails?appids=364470) — механіки доповнень, режими.
- YouTube: пошук «Elder Scrolls Legends gameplay».

## Непевне
- (?) Межа руки (10?) і що буває з порожньою колодою — не знайшов у відкритих джерелах.
- (?) Правило «Guard не може мати Cover» — з уривка UESP у пошуковій видачі (сторінку не відкрито).
- (?) Повний список особливих смуг Арени й історії (Fextralife дає лише Cover і Graveyard).
- (?) Тексти Slay, Rally, Plot, Exalt, Betray, Assemble, Invade, Wax/Wane — бачив лише назви.
- (?) Чи Support має обмежену кількість використань — з памʼяті, не перевірено.
- (?) Деталі історії (карта, діалоги) — з опису «вибори впливають на сюжет і карти».
