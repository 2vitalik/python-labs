---
title: Pawnbarian
slug: pawnbarian
aka: [Pawnbarian Classic]
family: roguelike
also: [chess-abstract, tactics]
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2021
platforms: [Windows, macOS, Linux, Android, iOS]
links:
  - {kind: other, url: "https://www.pocketgamer.com/pawnbarian/mobile-review/", best: true, note: "огляд: поле 5×5, 6 героїв, червоні позначки шкоди на клітинах, Blight, золото за швидкість"}
  - {kind: steam, url: "https://store.steampowered.com/app/1142080/Pawnbarian", note: "Steam: колода фігур, 6 героїв, 3 підземелля, Gauntlet, Chains, реліз 24.09.2021"}
  - {kind: official, url: "https://j4nw.com/pawnbarian", note: "сайт автора (j4nw): платформи, демо"}
  - {kind: itch, url: "https://j4nw.itch.io/pawnbarian", note: "itch.io: теги, джем-прототип Pawnbarian Classic"}
  - {kind: other, url: "https://gideonsgaming.com/pawnbarian-review-working-knights-in-a-dungeon/", note: "огляд: 3 карти на хід, контур клітин зі шкодою, апгрейди карт, герої"}
  - {kind: other, url: "http://www.148apps.com/reviews/pawnbarian-review/", note: "огляд: дві карти на хід, хід на ворога = вбивство"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Pawnbarian+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [piece-move-patterns, piece-capture, pawn-promotion, telegraphed-intents, telegraph-marker, threat-range, reachable-highlight, hover-highlight, cell-click, hp-damage, status-effects, destroy-all-enemies, sequential-levels, time-bonus, round-currency, shop-between-levels, character-select, difficulty-levels, permadeath, +move-cards, +hand-draw-play-two, +end-turn-square-damage, +blight-spread, +card-upgrade, +fixed-deck-size, +ascension-chains]
proposes: ["+role:card", "+trigger:card_played(card)", "+cond:card_allows(move)", "+effect:draw(n)", "+effect:discard(hand)", "+ui:card-hand", "+ui:damage-notches", "+feature:ascension", "+card:move-cards", "+card:end-turn-square-damage"]
author: opus
date: 2026-11-09
---

# Pawnbarian — герой ходить картами-фігурами: кінь, тура, слон — і кінчай хід там, куди не бʼють

## Суть
Тактичний роглайк-пазл j4nw. Герой стоїть на маленькій шаховій дошці серед монстрів; щоходу набираєш **3 карти з колоди фігур** і граєш **дві**: карта «кінь» — стрибок буквою Г, «тура» — по прямій тощо. Стати на клітину ворога — убити його. Наприкінці ходу отримуєш стільки шкоди, скільки **червоних позначок** на клітині, де стоїш, — вороги заздалегідь показують, куди вдарять. Поверх — апгрейди карт (щит, додаткова дія, удари по сусідах), золото за швидкість і 6 героїв з різними колодами.

## Поле і час
- Шахова дошка 5×5 (за Pocket Gamer; 148Apps пише «чверть шахівниці», 4×4 — див. «Непевне»).
- Хід: добір 3 карт → зіграти 2 → нерозіграні скидаються → шкода з позначок на твоїй клітині → вороги атакують і рухаються.
- Поверх (stage) = одна дошка з ворогами; чистиш усіх — наступний; 3 підземелля, у кінці бос.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | серця (HP), колода фіксованого розміру | рухається патерном зіграної карти |
| Карта-фігура | supply | фігура (пішак, кінь, слон, тура, ферзь, король), апгрейди | задає хід героя; може нести щит, кантрип, удар по сусідах, Purify |
| Пішак (Pawnbarian) | supply | — | дійшов до краю — стає ферзем до кінця бою |
| Монстр | enemy | власні правила, наміри | показує клітини атаки; бʼє й рухається після ходу гравця |
| Монстр «невразливий поруч» | enemy | — | не вбивається, поки герой у сусідній клітині |
| Монстр з Blight (капібар та ін.) | enemy | — | лишає Blight на клітинах |
| Goblin Zapper | enemy | — | (?) дистанційна атака |
| Бос | boss | — | у кінці підземелля |
| Blight | hazard | — | шкода, якщо стоїш на ній |
| Ward | terrain | — | слід Mystic: перший хід за хід лишає Ward (?) захист |
| Червона позначка | mark | кількість = кількість ударів | шкода в кінці ходу, якщо стоїш тут |
| Золото | resource | — | дається після поверху, більше за швидкість |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «добрати 3 карти з колоди»`.
- КОЛИ `input(card, cell)` → ЯКЩО `legal(move)` за фігурою карти → ТО `move(hero, cell)`; `counter(plays, +1)`.
- КОЛИ `input(card, cell)` → ЯКЩО `occupied(cell, enemy)` і `not state(enemy, invulnerable)` → ТО `disappear_b` (взяття).
- КОЛИ `counter(plays, ==, 2)` → ТО `custom: «решта руки скидається»`, `end_turn`.
- КОЛИ `turn_end(player)` → ЯКЩО `custom: «на клітині героя k червоних позначок»` → ТО `damage(k)`; ЯКЩО `state(hero, shield)` → ТО `custom: «−1 шкода»`.
- КОЛИ `turn_end(player)` → ТО `custom: «вороги виконують атаки, рухаються, показують нові позначки»`.
- КОЛИ `turn_end(player)` → ЯКЩО `cell(hero, blight)` → ТО `damage(1)` (?).
- КОЛИ `adjacent(hero, enemy)` → ЯКЩО `custom: «тип ворога — невразливий поруч»` → ТО `set_state(enemy, invulnerable)`.
- КОЛИ `input(card with shield)` → ТО `set_state(hero, shield, 1 turn)`.
- КОЛИ `input(card with strike)` → ТО `custom: «удар по ортогонально / діагонально сусідніх клітинах»`.
- КОЛИ `input(card with cantrip)` → ТО `extra_move` (?).
- КОЛИ `input(card with purify)` → ТО `set_cell(cell_under_hero, floor)` (знімає Blight).
- КОЛИ `reach(pawn_hero, last_row)` → ЯКЩО `mode(hero = Pawnbarian)` → ТО `transform(queen)` до кінця бою.
- КОЛИ `input(knight)` → ЯКЩО `custom: «попередня карта — теж кінь»` і `mode(hero = Knight Templar)` → ТО `extra_move`.
- КОЛИ `input(first move this turn)` → ЯКЩО `mode(hero = Mystic)` → ТО `place(ward, prev_cell)`.
- КОЛИ `all_gone(enemy)` → ТО `currency(+gold − за кожен зайвий хід)`, `heal(hero, 1)`, `next_level`.
- КОЛИ `input(buy)` → ЯКЩО `has(hero, gold ≥ price)` → ТО `custom: «апгрейд карти»` або `heal(hero, 1)` / `custom: «+1 серце макс.»`.
- КОЛИ `hp_zero(hero)` → ТО `lose` (забіг закінчено; постійних апгрейдів нема).
- КОЛИ `died(boss)` → ЯКЩО `level(==, last dungeon)` → ТО `win`; відкривається Gauntlet і Chains.

## Керування і ввід
- Миша або тач: обрати карту з руки → клітина підсвічується за патерном → клік/відпустити на клітину.
- Довге натискання / наведення на ворога — його клітини атаки; на свою карту — властивості й досяжні клітини.
- Пастка вводу (Pocket Gamer): відпустивши палець над клітиною, можна випадково зіграти карту.

## Вікна, меню, HUD
- `main-menu` → `character-select` (6 героїв, решта відкривається проходженням) → вибір підземелля (3) і Chains.
- `game-screen`: дошка; `card-hand` (3 карти); `damage-notches` на клітинах; `threat-range` при наведенні на ворога; `reachable-highlight` для обраної карти; серця; золото.
- `shop-window` між поверхами: апгрейди карт, серце / 1 HP.
- `upgrade-window`: накласти властивість на карту (щит, кантрип, удар, Purify).
- `end-screen`: смерть або перемога над босом.
- Вступна сторінка підземелля (мальована) — `custom-window`.

## Фічі поза полем
- `mode-endless`: Gauntlet — скільки поверхів поспіль утримаєшся.
- `ascension`: Chains — додаткові ускладнення після проходження (як Ascension у Slay the Spire).
- Забіг 15–30 хв; без мета-апгрейдів між забігами.
- Безкоштовне демо (1 герой, 1 підземелля), повна версія — одна покупка.

## Варіації й родичі
- `chess-abstract/chess` — патерни фігур; `chess-abstract/onitama` — хід визначає карта, а не фігура.
- Shotgun King (шахи-роглайк з іншого боку: король проти фігур); `tactics/hoplite` (маленька арена, наміри ворогів); `tactics/into-the-breach` (позначки удару).
- `868-hack` — та сама «broughlike»-школа: маленька сітка, повна інформація про загрози.
- **Осі варіацій**: хто обирає патерн (карта / фігура / вільно); скільки карт на хід (1 / 2 з 3 / вся рука); що загрожує (клітина в кінці ходу / дотик / намір ворога); колода (фіксований розмір / росте).

## Цікавинки для курсу
- Хід картою з патерном фігури: та сама функція `piece_moves`, але фігуру вибирає роздача — 🌱.
- «Шкода там, де закінчив хід»: позначки загроз як агрегована мапа — 📎.
- Рука 3 / зіграти 2 / скинути решту — 🌱.
- Апгрейди як властивості на карті (щит, удар по сусідах, кантрип) — 🥉 (композиція ефектів).
- Герої = інші колоди й одне правило-виняток (перетворення пішака, ланцюг коней, Ward) — 📎.
- Золото, що падає з кожним ходом, — 🌱.

## Мапа на каталог
- Є: `piece-move-patterns` · `piece-capture` · `pawn-promotion` · `telegraphed-intents`, `telegraph-marker` (позначки), `threat-range` · `reachable-highlight` · `hover-highlight` · `cell-click` · `hp-damage` · `status-effects` (Blight, щит, Ward) · `destroy-all-enemies` · `sequential-levels` · `time-bonus` (золото за швидкість) · `round-currency` · `shop-between-levels` · `character-select` · `difficulty-levels` (Chains) · `permadeath`.
- **Нема** → пропозиції карток:
  - `+move-cards` «Хід задає зіграна карта з патерном» · entities/movement · 📎 · слоти {hand, plays}.
  - `+hand-draw-play-two` «Добір N, зіграти M, решту скинути» · game-logic/turns · 🌱.
  - `+end-turn-square-damage` «Шкода за позначками клітини, де закінчив хід» · entities/combat · 🌱.
  - `+blight-spread` «Вороги лишають шкідливу підлогу» · entities/state · 📎.
  - `+card-upgrade` «Властивості на картці колоди» · game-logic/progression · 🥉.
  - `+fixed-deck-size` «Колода незмінного розміру, змінюються лише карти» · game-logic/progression · 🌱.
  - `+ascension-chains` «Рівні ускладнення після перемоги» · game-logic/progression · 🌱.

## Пропозиції до словників
- `+role:card` — карта як сутність колоди (також у Onitama).
- `+trigger:card_played(card)` · `+cond:card_allows(move)` — зіграна карта і її патерн.
- `+effect:draw(n)` · `+effect:discard(hand)` — добір і скидання.
- `+ui:card-hand` — рука карт; `+ui:damage-notches` — число ударів на клітині.
- `+feature:ascension` — сходинки ускладнення (Chains).
- `+card:move-cards` · `+card:end-turn-square-damage`.

## Джерела
- ⭐ [Pocket Gamer: mobile review](https://www.pocketgamer.com/pawnbarian/mobile-review/) — 5×5, 6 героїв, червоні позначки, Blight, золото за швидкість, крамниця.
- [Steam](https://store.steampowered.com/app/1142080/Pawnbarian) — колода фігур, 6 героїв, 3 підземелля, Gauntlet, Chains, без мета-апгрейдів.
- [Gideon's Gaming: огляд](https://gideonsgaming.com/pawnbarian-review-working-knights-in-a-dungeon/) — 3 карти на хід, підсвітка шкоди, апгрейди, Pawnbarian і Templar.
- [148Apps: огляд](http://www.148apps.com/reviews/pawnbarian-review/) — дві карти на хід, вбивство ходом на ворога.
- [j4nw.com](https://j4nw.com/pawnbarian) · [itch.io](https://j4nw.itch.io/pawnbarian).
- YouTube: [пошук «Pawnbarian gameplay»](https://www.youtube.com/results?search_query=Pawnbarian+gameplay).

## Непевне
- (?) Розмір дошки: 5×5 (Pocket Gamer, пошукові підсумки) проти «чверті шахівниці» 4×4 (148Apps) — можливо, у підземеллях різний.
- (?) «3 карти, зіграти 2» — зведено з кількох оглядів; чи кантрип додає третій хід — не перевірено.
- (?) Як саме шкодить Blight (на кінці ходу / при вході) і що дає Ward.
- (?) Рік: черга каже 2020 (ймовірно, джем-прототип Pawnbarian Classic), Steam-реліз — 24.09.2021.
- (?) Умова відкриття героїв і Chains — «пройти Pawnbarian-ом» за Pocket Gamer; точні умови не бачив.
- (?) Типи ворогів, окрім названих (капібари, огри, големи, гоблін-зеппери), — не перевірено.
