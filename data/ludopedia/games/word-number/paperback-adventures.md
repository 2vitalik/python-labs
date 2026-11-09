---
title: Paperback Adventures
slug: paperback-adventures
aka: [Paperback Adventures (Fowers Games), Paperback 2]
family: word-number
also: [roguelike, board-digital]
klass: cursor
axes:
  field: 1d
  time: turn
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 2023
platforms: [PC, board]
links:
  - {kind: other, url: "https://c.tabletopia.com/games/paperback-adventures/rules/paperback-adventure-rulebook/en", best: true, note: "повний рулбук (PDF, 13 с.): фази ходу, splay, верхня карта, fatigue, wild і голосна-слабкість ворога, hex/boon, предмети, McGuffin, нагороди, 3 книги"}
  - {kind: steam, url: "https://store.steampowered.com/app/2095080/Paperback_Adventures/", note: "цифрова версія, Early Access з 30.01.2023: 3 книги (9 боїв), 3 персонажі, досягнення, Steam Cloud"}
  - {kind: official, url: "https://www.fowers.games/pages/paperback-adventures", note: "FAQ: голосна ворога йде у fatigue; wild не можна «втомити» ефектами (з пошукового фрагмента)"}
  - {kind: other, url: "https://www.meeplemountain.com/reviews/paperback-adventures/", note: "огляд настільної: бібліотека 60 карт, wild щоходу, довгі двосторонні боси (з пошукового фрагмента)"}
  - {kind: other, url: "https://coopgestalt.com/2022/11/24/a-review-of-paperback-adventures-a-solo-and-cooperative-word-game/", note: "огляд: штрафні карти забивають колоду (з пошукового фрагмента)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=paperback+adventures+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [word-validation, hp-damage, status-effects, telegraphed-intents, telegraph-marker, inventory-items, run-relics, in-round-upgrades, sequential-levels, character-select, permadeath, save-progress, achievements-window, game-screen, end-screen, main-menu, help-window, +letter-deckbuilding, +splay-direction, +top-card-ability, +fatigue-pile, +wild-letter, +enemy-weak-vowel, +two-stage-enemy, +penalty-letter-cards, +card-upgrade-flip, +reward-choice-two-sides, +double-sided-mcguffin]
proposes: ["+effect:draw_cards", "+effect:exhaust", "+effect:discard", "+effect:add_card(deck, card)", "+effect:upgrade_card", "+cond:top_card(c)", "+cond:splay(dir)", "+trigger:card_unplayed(c)", "+ui:card-hand", "+ui:deck-counter", "+ui:discard-pile", "+ui:mana-counter", "+ui:hex-boon-track", "+window:reward-choice"]
author: opus
date: 2026-11-09
---

# Paperback Adventures — словесний deckbuilder-роглайк: з руки з 4 карт-літер склади слово, розклади його ліворуч чи праворуч — і лише видимі краї карт б'ють, блокують і дають ману

## Суть
Соло-забіг через 3 «книги» (2 звичайні вороги + бос у кожній, разом 9 боїв). Щоходу на руці 4 карти-літери; гравець складає з них слово і обирає, у який бік його «розкласти» (splay): ліворуч рахуються ліві краї карт, праворуч — праві. На краях — значки удару, блоку і мани, а текстова здібність спрацьовує лише в «верхньої» карти, яка після ходу йде у fatigue до кінця бою. Ворог наперед показує дію (intent); у кожного є слабка голосна, яку можна безкоштовно вставити в слово. На відміну від Wordatro (`wordatro.md`) тут колода, бій з HP і геометрія «який край видно», а не множник довжини.

## Поле і час
- Поля-сітки нема: «поле» — рядок карт слова (1d) + рука, колода, скид, fatigue; поруч — трекери гравця й ворога.
- Хід = 3 фази: Prep (план слова, предмети, wild, вибір напрямку) → Clash (здібність верхньої карти → удари мінус блок ворога → блоки й мана → дія ворога) → Cleanup (верхня карта у fatigue, решта у скид, intent далі, добір 4).
- Бій триває, доки ворог не впаде у 2-й стадії. Забіг: Book 1 → 2 → 3; між боями — Character Development.
- Цифрова версія (Steam) повторює настільну; там 3 персонажі, у рулбуку прототипу — 2.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Протагоніст (Ex Machina, Damsel, …) | player | HP 20 (макс.), mana, hex, boon | власні стартова колода (10 карт), колода росту (50), 3 core-предмети |
| Карта-літера | tile | літера; значки hits/blocks/mana на лівому і правому краї; текст-здібність; бік «upgraded» | рахується лише край з боку splay; здібність — лише на верхній карті |
| Рідкісна карта | tile | позначка-самоцвіт | сильніша карта колоди росту |
| Wild Card (core) | pickup | 1 літера на вибір або +1 mana за хід | після апгрейда — до 2 суміжних літер «??» |
| Карта «?» | tile | будь-яка літера | без значків і здібності; якщо зверху — верхньою вважається карта під нею |
| Голосна ворога | tile | слабка голосна (виділена в імені ворога) | доступна щоходу; верхня здібність — зсув intent ворога на наступну дію; може піти у fatigue і тоді зникає |
| Штрафна карта | tile | літера + негатив | забиває колоду; якщо не зіграна з руки — негативний ефект; більшість повертається в штрафну колоду після зіграння |
| Ворог | enemy | HP стадії 1 і 2, список дій, блок, Special Rules, слабка голосна | дії по черзі зверху вниз за intent; HP 0 у стадії 1 → переворот |
| Бос | boss | двостороння карта, свої правила | кінець кожної книги; бос Book 3 — фінальний |
| Intent-індикатор | mark | вказує дію ворога цього ходу | після ходу зсувається вниз, з кінця — на початок |
| Hex-лічильник | mark | рівень на треку | негатив для носія (гравця чи ворога), тримається між ходами |
| Boon-лічильник | mark | рівень на треку | позитив для носія, тримається між ходами |
| Предмет | pickup | ціна в mana; Reactive / Single Use | раз на хід у Prep; Reactive — за умовою; Single Use — раз на бій |
| Core-предмети | pickup | 3 двосторонні (wild, hex-предмет, boon-предмет) | після боса один перевертається на сильніший бік |
| McGuffin | pickup | двосторонній, без ціни; рідкісний коштує 2 штрафні карти | обраний бік спрацьовує автоматично за своєю умовою |
| Нагорода | pickup | 2 варіанти на боках карти | звичайна — заміна карт колоди; бос — додавання карт |
| Колода / скид / fatigue | zone | — | порожня колода → перетасувати скид; fatigue повертається лише після бою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` (бій) → ТО `custom: «ворог стадії 1, intent на першу дію»`, `custom: «добрати 4 карти»`.
- КОЛИ `input(play word)` → ЯКЩО `in_dictionary(word)` → ТО `custom: «слово йде в Clash»`; інакше `block`.
- КОЛИ `input(wild)` → ЯКЩО `first_time` (цього ходу) → ТО `give(player, letter ?)` або `currency(+1 mana)`.
- КОЛИ `input(splay)` → ЯКЩО `custom: «обрано splay ліворуч»` → ТО `custom: «верхня карта = остання літера; рахуються ліві краї»`.
- КОЛИ `input(splay)` → ЯКЩО `custom: «обрано splay праворуч»` → ТО `custom: «верхня карта = перша літера; рахуються праві краї»`.
- КОЛИ `phase_start(clash)` → ЯКЩО `custom: «верхня карта — звичайна карта-літера»` → ТО `custom: «здібність верхньої карти»`.
- КОЛИ `phase_start(clash)` → ЯКЩО `custom: «верхня карта — ?»` → ТО `custom: «верхньою стає карта під нею: її здібність і її fatigue»`.
- КОЛИ `after(ability)` → ТО `damage(enemy, hits − enemy_block)`; блок ворога не зменшує втрату HP від предметів і McGuffin.
- КОЛИ `after(damage)` → ТО `custom: «blocks на цей хід»`, `currency(+mana)` (mana переходить між ходами).
- КОЛИ `after(blocks)` → ЯКЩО `not state(enemy, stunned)` → ТО `custom: «дія ворога за intent»`; атака → `damage(player, attack − blocks)`.
- КОЛИ `turn_end` → ТО `custom: «верхня карта у fatigue; решта слова й руки у скид; intent на наступну дію; добрати 4»`.
- КОЛИ `counter(deck, ==, 0)` → ЯКЩО `custom: «треба добрати карту»` → ТО `custom: «перетасувати скид у колоду»`; fatigue не повертається.
- КОЛИ `hp_zero(enemy)` → ЯКЩО `state(enemy, stage1)` → ТО `transform(enemy stage2)`, `set_state(enemy, stunned, 1 turn)`, `custom: «надлишок шкоди переходить на стадію 2»`.
- КОЛИ `hp_zero(enemy)` → ЯКЩО `state(enemy, stage2)` → ТО `custom: «бій виграно → Character Development»`.
- КОЛИ `input(play word)` → ЯКЩО `custom: «верхня карта — голосна ворога»` → ТО `custom: «intent ворога зсувається на наступну дію; голосна у fatigue — слабкість більше не доступна»`.
- КОЛИ `turn_end` → ЯКЩО `custom: «штрафна карта лишилась на руці»` → ТО `custom: «негативний ефект штрафної карти; карта у скид»`.
- КОЛИ `input(play word)` → ЯКЩО `custom: «у слові є штрафна карта»` → ТО `custom: «повернути в штрафну колоду»` (якщо так написано на карті).
- КОЛИ `input(item)` → ЯКЩО `has(player, mana >= cost)` and `first_time` (цей предмет цього ходу) → ТО `currency(−cost)`, `custom: «ефект предмета»`; mana, отримана цього ходу, — лише з наступного.
- КОЛИ `custom: «умова Reactive-предмета»` → ЯКЩО `has(player, mana >= cost)` → ТО `custom: «ефект»`.
- Hex/boon: КОЛИ `custom: «здібність / дія ворога»` → ТО `set_state(target, hex, +n)` або `set_state(target, boon, +n)`.
- КОЛИ `level_end` (бій) → ТО `clear_state(player, hex)`, `clear_state(player, boon)`, `custom: «mana = 0; усі карти — в одну колоду; HP лишається»`.
- КОЛИ `level_end` → ЯКЩО `not state(enemy, boss)` → ТО `choose(reward side)`: `custom: «замінити карти колоди / посилити карту / предмет / McGuffin»`.
- КОЛИ `level_end` → ЯКЩО `state(enemy, boss)` → ТО `choose(boss reward side)`, `custom: «додати карти в колоду; перевернути один core-предмет»`.
- КОЛИ `custom: «взяти рідкісний McGuffin»` → ТО `custom: «додати 2 штрафні карти в колоду»`.
- КОЛИ `hp_zero(player)` → ТО `lose`, `game_over` — забіг з початку.
- Перемога: перемогти фінального боса Book 3 · Поразка: HP гравця 0 · Рахунку нема; HP між боями не відновлюється сам.

## Керування і ввід
- (цифрова версія) Клік/drag карт з руки в рядок слова; кнопки wild (літера на вибір / mana), голосна ворога, перемикач напрямку splay, предмети, «зіграти» (?).
- Обирати треба одночасно три речі: яке слово, яку карту зробити верхньою (через порядок літер і напрямок) і який край рахувати.
- Між боями — вибір боку нагороди, боку McGuffin, карти для заміни чи апгрейда.

## Вікна, меню, HUD
- `game-screen`: рядок слова з видимими краями, `card-hand` (4 карти), `deck-counter`, `discard-pile`, fatigue-стос, `hp-bar` гравця і ворога, `mana-counter`, `hex-boon-track`, `telegraph-marker` (intent ворога), список дій ворога, слабка голосна, предмети й McGuffin.
- `reward-choice`: двостороння карта нагороди — обрати бік.
- `character-select`: протагоніст зі своїм набором карт.
- `map-window` (?): прогрес книги — 2 вороги + бос.
- `main-menu` → нова гра / продовжити (Steam Cloud) / `achievements-window` (Steam) / `help-window`.
- `end-screen`: перемога над фінальним босом або поразка.

## Фічі поза полем
- `meta-progression` / `unlockables`: нові опції персонажа відкриваються з проходженнями (Steam).
- `save-slots` / `autosave` між боями (рулбук: «фінальна гра матиме збереження після бою»).
- `achievements`, `cloud-save` (Steam).
- Рандом забігу: порядок ворогів, нагороди, предмети, McGuffin.

## Варіації й родичі
- Paperback (2014, Tim Fowers) — настільний deckbuilder на словах, предок: ті самі літери-карти й покупка карт.
- Bookworm Adventures (`bookworm-adventures.md`) — бій словами з сітки, шкода від довжини й рідкості; тут — від країв карт.
- Wordatro (`wordatro.md`) і Letterlike (2025, Puzzlelike) — Balatro-подібні: ціль очок, без ворожого HP.
- Words Can Kill — ще один словесний роглайк хвилі 2020-х (?).
- Slay the Spire — шаблон: intent ворога, exhaust, нагорода після бою.
- **Осі варіацій:** ресурс слова (вартість літери / край карти / довжина) · ворог (ціль очок / HP з intent) · модифікатори (реліквії / предмети за mana / McGuffin) · колода (мішок літер / deckbuilding із заміною) · спецлітери (wild / голосна ворога / штрафні).

## Цікавинки для курсу
- Splay: одне слово дає два різні результати залежно від напрямку; вибір кращого — 📎 (порівняти дві суми і верхню карту).
- Верхня карта = здібність + fatigue: «одноразовість» здібностей через стос — 🥉.
- Колода / скид / fatigue з перетасуванням і добором 4 — 📎: класичний цикл deckbuilder.
- Intent ворога за списком дій + голосна, що зсуває intent — 📎.
- Двостадійний ворог з переносом надлишку шкоди і станом stun — 🌱.
- Штрафна карта, що шкодить, якщо її не зіграти, — 🌱.
- Підказник «найкраще слово з руки + wild + голосна з урахуванням splay» — 🥈 (перебір по словнику з метрикою).

## Мапа на каталог
- Є: `word-validation` · `hp-damage` ↔ HP гравця й ворога · `status-effects` ↔ hex/boon · `telegraphed-intents` · `telegraph-marker` ↔ intent-індикатор · `inventory-items` ↔ предмети · `run-relics` ↔ McGuffin · `in-round-upgrades` ↔ апгрейд карт між боями · `sequential-levels` ↔ 9 боїв · `character-select` · `permadeath` · `save-progress` · `achievements-window` · `game-screen` · `end-screen` · `main-menu` · `help-window`.
- **Нема** → пропозиції карток:
  - `+letter-deckbuilding` «Колода карт-літер з добором руки» · game-logic/economy · 📎.
  - `+splay-direction` «Напрямок розкладу вирішує, які значки рахуються» · game-logic/score · 📎.
  - `+top-card-ability` «Здібність лише крайньої карти комбінації» · game-logic/score · 🌱.
  - `+fatigue-pile` «Зіграна карта вибуває до кінця бою (exhaust)» · entities/state · 🌱.
  - `+wild-letter` «Літера на вибір / ресурс замість неї» · game-logic/constraints · 🌱.
  - `+enemy-weak-vowel` «Безкоштовна голосна від ворога» · game-logic/opponent · 🌱.
  - `+two-stage-enemy` «Ворог з двома стадіями і переносом шкоди» · entities/state · 🌱.
  - `+penalty-letter-cards` «Штрафні карти в колоді» · game-logic/economy · 🌱.
  - `+card-upgrade-flip` «Апгрейд карти = інший бік» · game-logic/economy · 🌱.
  - `+reward-choice-two-sides` «Нагорода: обрати один з двох пакетів» · game-logic/economy · 🌱.
  - `+double-sided-mcguffin` «Пасивка з вибором боку при отриманні» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+effect:draw_cards` — добрати N карт у руку (Paperback Adventures, Monster Train, Cobalt Core).
- `+effect:exhaust` — карта вибуває до кінця бою (fatigue; Cobalt Core, Slay the Spire).
- `+effect:discard` — карта/рука у скид.
- `+effect:add_card(deck, card)` — додати карту в колоду (штрафна, нагорода).
- `+effect:upgrade_card` — перевернути карту на посилений бік.
- `+cond:top_card(c)` — карта є крайньою («верхньою») в комбінації.
- `+cond:splay(dir)` — обраний напрямок розкладу слова.
- `+trigger:card_unplayed(c)` — карта лишилась на руці наприкінці ходу.
- `+ui:card-hand` · `+ui:deck-counter` · `+ui:discard-pile` · `+ui:mana-counter` — стандартні віджети deckbuilder.
- `+ui:hex-boon-track` — два треки лічильників-станів у гравця й ворога.
- `+window:reward-choice` — вибір одного з двох боків нагороди після бою.

## Джерела
- ⭐ [Рулбук Paperback Adventures (Tabletopia, PDF)](https://c.tabletopia.com/games/paperback-adventures/rules/paperback-adventure-rulebook/en) — компоненти, підготовка, 3 фази ходу, splay, верхня карта, fatigue, wild і «??», голосна ворога, штрафні карти, hex/boon, предмети (Reactive, Single Use), McGuffin, нагороди, апгрейд карт, структура 3 книг.
- [Steam: Paperback Adventures](https://store.steampowered.com/app/2095080/Paperback_Adventures/) — Early Access 30.01.2023, 3 книги (9 боїв), 3 персонажі, предмети й McGuffin, досягнення, Steam Cloud; Fowers Games.
- [Fowers Games: сторінка гри](https://www.fowers.games/pages/paperback-adventures) — FAQ (бачив лише пошуковий фрагмент).
- [Meeple Mountain: огляд](https://www.meeplemountain.com/reviews/paperback-adventures/) · [Co-op Gestalt: огляд](https://coopgestalt.com/2022/11/24/a-review-of-paperback-adventures-a-solo-and-cooperative-word-game/) — пошукові фрагменти.
- YouTube: пошук «paperback adventures gameplay».

## Непевне
- (?) Рулбук — прототип настільної версії; цифрова Steam-версія може відрізнятись деталями (3 персонажі проти 2, інтерфейс, мета-прогресія).
- (?) Вікна цифрової версії (карта книги, меню, екран нагороди) — реконструкція, скриншотів не бачив.
- (?) Як цифрова версія перевіряє слово (словник, мінімальна довжина) — рулбук мовчить.
- (?) Words Can Kill — назва з черги, не перевіряв; Letterlike — лише Steam-опис (мішок літер, боси, самоцвіти для постійних апгрейдів, NG+).
- (?) Рік: Steam — 2023 (Early Access); настільна версія — 2022 (за датою огляду Co-op Gestalt).
</content>
</invoke>
