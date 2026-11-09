---
title: Agricola — сітка ферми (Агрікола)
slug: agricola-farm-grid
aka: [Agricola, Агрікола, Agricola farmyard]
family: board-digital
also: [build-sim]
klass: cursor
axes:
  field: square
  time: turn
  opponent: hotseat
  info: partial
  random: runtime
  goal: score
year: 2007
platforms: [board, iOS]
links:
  - {kind: other, url: "https://www.ultraboardgames.com/agricola/actions.php", best: true, note: "дії ферми: кімнати, реновація, стайні, оранка й сівба, паркани й пасовища, ємність, улюбленець, ріст родини"}
  - {kind: other, url: "https://www.ultraboardgames.com/agricola/game-rules.php", note: "базові правила: раунди, фази, урожай, годування, жебрацтво, розміщення робітників"}
  - {kind: other, url: "https://www.ultraboardgames.com/agricola/scoring.php", note: "таблиця очок за категоріями, -1 за невикористану клітину"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Agricola_(board_game)", note: "огляд: 14 раундів, урожаї, видання, iOS-версія Playdek, All Creatures Big & Small"}
  - {kind: bgg, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=Agricola", note: "пошук BGG"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Agricola+farmyard+fences+pastures+rules", note: "пошук; паркани й пасовища"}
stage: v1
coverage: 55
mechanics: [cell-click, hover-highlight, legal-move-highlight, edge-marking, connectivity-check, inventory-limit, event-points, leftover-penalty, turn-enforcement, hot-seat, ai-opponent, match-setup, end-screen, help-window, save-game, +worker-placement, +fence-enclosure, +pasture-capacity, +stable-doubles-capacity, +one-type-per-pasture, +orthogonal-growth, +subdivide-region, +animal-breeding, +feeding-phase, +begging-penalty, +category-score-table, +unused-cell-penalty, +room-material-upgrade, +harvest-schedule]
proposes: ["+trigger:harvest", "+cond:enclosed(region)", "+cond:capacity(region, op, n)", "+cond:orth_adjacent(cell, kind)", "+effect:build_fence(edge)", "+effect:breed(kind)", "+effect:feed(n)", "+effect:renovate(material)", "+role:pasture", "+role:fence", "+ui:capacity-badge", "+ui:fence-counter", "+window:farm-rearrange", "+window:harvest-summary", "+card:fence-enclosure", "+card:pasture-capacity", "+card:unused-cell-penalty"]
author: opus
date: 2026-11-09
---

# Agricola (сітка ферми) — паркани на ребрах сітки замикають пасовища; ємність пасовища = площа × стайні

## Суть
Витяг з Agricola лише про особисту ферму-сітку. Робітники гравця на спільному полі дій беруть дії «будувати кімнату», «орати», «ставити паркани», «стайні» — а результат з'являється на власній фермі: кімнати ростуть ортогонально від хати, поля — від полів, паркани кладуться на **ребра** між клітинами й мусять повністю замкнути пасовище. Тварини живуть лише в пасовищах (одна порода на пасовище, 2 на клітину, стайня подвоює), у стайні без паркану (1) або в хаті (1 улюбленець). Фінальний рахунок карає за порожні клітини й за відсутні категорії — ферма має бути збалансована.

## Поле і час
- Особиста ферма — прямокутна сітка клітин (розмір — у «Непевне»); на старті дві клітини зайняті дерев'яною хатою (2 кімнати).
- Два шари: **клітини** (кімната / поле / стайня / порожня) і **ребра** між клітинами (паркан або нічого). Край ферми не вважається парканом — по краю паркан теж потрібен.
- Пасовище = звʼязна група клітин, повністю обведена парканами; поля й кімнати обвести не можна.
- Час: 14 раундів у 6 етапах; урожай після раундів 4, 7, 9, 11, 13, 14. Раунд: відкрити картку дії → поповнити товари → робота (по одному робітнику по черзі) → повернення додому.
- Інформація: ферма й ресурси відкриті; картки занять і поліпшень у руці приховані; порядок нових дій у межах етапу випадковий.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітина | terrain | — | наприкінці −1 очко, якщо не огороджена |
| Кімната | static | матеріал wood/clay/stone | ортогонально до наявних кімнат; усі одного матеріалу; 0/1/2 очки |
| Поле | terrain | засіяне / під паром | ортогонально до наявних полів; урожай забирає 1 зерно/овоч |
| Зерно на полі | resource | 3 після сівби | 1 зі свого запасу + 2 з банку |
| Овоч на полі | resource | 2 після сівби | 1 зі свого запасу + 1 з банку |
| Паркан | static | ≤15 на гравця, 1 дерево | лежить на ребрі; не знімається |
| Стайня | static | ≤4, 2 дерева | одна на клітину без кімнати й поля; без паркану тримає 1 тварину, у пасовищі подвоює ємність |
| Пасовище | zone | клітин k, стаєнь s | ємність 2·k·2^s (?) — див. «Непевне»; одна порода |
| Вівця / кабан / корова | object | порода | лише в пасовищі, стайні або 1 у хаті; ≥2 однієї породи → +1 приплід, якщо є місце |
| Член родини | player | ≤5 | робітник: займає поле дії; на урожаї їсть 2 їжі (новонароджений 1) |
| Поле дії | zone | 1 робітник за раунд | спільне поле: зайняте не можна взяти |
| Картка жебрацтва | hazard | −3 очки | за кожну нестачу їжі |
| Улюбленець | object | 1 | тварина в хаті, кімнати не займає |

## Правила (КОЛИ → ЯКЩО → ТО)
- Робота: КОЛИ `input(place(worker, action_space))` → ЯКЩО `free(action_space)` and `turn_of(p)` → ТО `place(worker)` + `custom: «виконати дію поля»`; зайняти поле без дії не можна.
- Кімната: КОЛИ `input(custom: «будувати кімнату на клітині»)` → ЯКЩО `free(cell)` and `adjacent_count(cell, room, >=, 1)` and `has(p, 5 material + 2 reed)` → ТО `set_cell(cell, room)` + `take(p, materials)`; матеріал — як у решти хати.
- Реновація: КОЛИ `input(custom: «реновація»)` → ЯКЩО `has(p, 1 clay|stone per room + 1 reed)` → ТО `transform(rooms, clay|stone)` — усі кімнати разом, дерево → глина → камінь.
- Оранка: КОЛИ `input(custom: «орати клітину»)` → ЯКЩО `free(cell)` and (`count(field, =, 0)` or `adjacent_count(cell, field, >=, 1)`) → ТО `set_cell(cell, field)`.
- Сівба: КОЛИ `input(custom: «сіяти зерно на порожнє поле»)` → ЯКЩО `has(p, grain)` → ТО `take(p, grain)` + `custom: «на поле 3 зерна»`; овоч → 2 овочі; поле після збору засівається без нової оранки.
- Стайня: КОЛИ `input(custom: «ставити стайню»)` → ЯКЩО `not occupied(cell, room|field|stable)` and `has(p, 2 wood)` and `counter(stables, <, 4)` → ТО `set_cell(cell, stable)`.
- Паркан: КОЛИ `input(custom: «покласти паркани на ребра»)` → ЯКЩО `has(p, 1 wood per fence)` and `counter(fences, <=, 15)` and `custom: «після дії кожне пасовище повністю замкнене»` → ТО `custom: «паркани стають на ребра»`; незамкнений контур — недійсний.
- Розширення: ЯКЩО `custom: «нове пасовище межує з наявним»` or `custom: «пасовищ ще нема»` → ТО дозволено; наявне пасовище можна `custom: «розділити внутрішнім парканом»`.
- Заборона: ЯКЩО `custom: «замкнена область містить кімнату або поле»` → ТО `block`.
- Ємність: КОЛИ `input(custom: «розмістити тварин»)` → ЯКЩО `same(animals, pasture, kind)` and `custom: «тварин ≤ 2 × клітин, подвоєно за кожну стайню в пасовищі»` → ТО `place(animal)`; стайня без паркану — 1 тварина; хата — 1 улюбленець.
- Тварини без місця: КОЛИ `custom: «нова тварина без місця»` → ТО `custom: «повернути в банк або приготувати (якщо є поліпшення)»`; тримати в запасі не можна; переставляти можна будь-коли.
- Ріст родини: КОЛИ `input(custom: «ріст родини»)` → ЯКЩО `custom: «кімнат більше, ніж членів родини»` (або дія «без кімнати» з 5-го етапу) and `counter(family, <, 5)` → ТО `spawn(family_member)`; діє з наступного раунду.
- Урожай — поля: КОЛИ `custom: «урожай після раундів 4, 7, 9, 11, 13, 14»` → ТО `take(field, 1 grain|vegetable)` з кожного засіяного поля в запас.
- Урожай — годування: ТО `custom: «2 їжі на члена родини, новонароджений — 1»`; зерно/овоч = 1 їжа будь-коли; ЯКЩО `custom: «їжі бракує»` → ТО `give(p, begging_card)` за кожну одиницю.
- Урожай — приплід: ЯКЩО `count(animal_kind, >=, 2)` and `custom: «є місце для приплоду»` → ТО `spawn(animal)` +1 тієї породи; немає місця — тікає.
- Рахунок: КОЛИ `game_over` → ТО `score(n)` за таблицями: поля, пасовища (за кількістю пасовищ, не клітин), зерно, овочі, вівці, кабани, корови (0 у категорії = −1; максимум +4); `score(+1)` за огороджену стайню; `score(+1|+2)` за глиняну/камʼяну кімнату; `score(+3)` за члена родини.
- Штрафи: `score(−1)` за кожну порожню неогороджену клітину; `score(−3)` за картку жебрацтва.
- Перемога: найбільше очок (тай-брейк — у «Непевне»).

## Керування і ввід
- Цифрова версія: спільне поле дій — клік по вільній дії ставить робітника; далі — режим ферми для цієї дії.
- Режим «Паркани»: клік по ребрах сітки (`edge-marking`), лічильник парканів і дерева, підсвітка замкнених областей і помилки «контур відкритий»; підтвердження лише коли всі контури замкнені.
- Кімнати / поля / стайні — клік по клітині з підсвіткою легальних (`legal-move-highlight`: ортогональна суміжність, вільність).
- Тварини — перетягування між пасовищами, стайнями й хатою; бейдж «місце / ємність» на кожному пасовищі.

## Вікна, меню, HUD
(цифрова версія)
- `main-menu`: Нова гра → `match-setup` · Продовжити · Правила → `help-window`.
- `match-setup`: 1–4/5 гравців, люди/AI, сімейний варіант (без карток) / повний.
- `game-screen`: поле дій (раунд, етап, наступний урожай), ферма активного гравця, `turn-indicator`, запас ресурсів, `fence-counter` (кандидат: лишилось з 15), `capacity-badge` (кандидат) на пасовищах.
- `farm-rearrange` (кандидат): переставити тварин після приплоду / нових тварин, що не влазять.
- `harvest-summary` (кандидат): поля → годування (жебрацтво) → приплід.
- `opponent-boards` — ферми суперників.
- `end-screen`: таблиця категорій × гравці.
- Переходи: main-menu → match-setup → game-screen ⇄ farm-rearrange / harvest-summary → end-screen.

## Фічі поза полем
- `hotseat` (1–5 гравців, ревізія 2016 — 1–4); соло-гра на одного.
- `custom-rules`: сімейний варіант без занять і поліпшень; колоди карток за виданням.
- `autosave` / `continue` — партія довга; iOS-версія Playdek (2013).

## Варіації й родичі
- Agricola: All Creatures Big & Small (2012, на двох) — лише тварини й ферма; ревізія 2016; розширення на 5–6 гравців.
- Родичі «особиста сітка + огородження»: [a-feast-for-odin-polyomino](a-feast-for-odin-polyomino.md) (той самий автор, поліоміно замість парканів), [the-castles-of-burgundy](the-castles-of-burgundy.md), [cartographers](cartographers.md); ферма в цифрі — [stardew-farm](../build-sim/stardew-farm.md).
- Огородження ребрами — [dots-and-boxes](../chess-abstract/dots-and-boxes.md) (замкнена клітина), [slitherlink](../pencil-logic/slitherlink.md) (замкнений контур).
- **Осі варіацій**: що обмежує (паркани на ребрах / плитки на клітинах) · ємність (за площею / фіксована / множник стаєнь) · ріст (ортогонально до свого / вільно) · штраф (порожні клітини / відсутня категорія) · рахунок (таблиці насичення до +4 / лінійно).

## Цікавинки для курсу
- Паркани на ребрах і пошук пасовищ: замкнені області як компоненти звʼязності клітин, які не перетинають паркан; область, що дотикається краю без паркану, — не пасовище — 🥉.
- Валідація дії «паркани»: після додавання ребер кожна область або повністю замкнена, або без жодного паркану; заборона обводити кімнати й поля — 🥈.
- Ємність пасовища з подвоєнням стаєнь і розміщення тварин трьох порід як задача пакування (жадібно / перебір) — 🥉.
- Ортогональний ріст кімнат і полів від наявних — 🌱.
- Фінальна таблиця «насичення» по категоріях з −1 за нуль і −1 за порожню клітину — 🌱.
- Розміщення робітників на спільних полях дій з поповненням ресурсів — 📎 (поза сіткою).
- AI для Agricola — 👑 (довгий горизонт, приховані картки).

## Мапа на каталог
- Є: `cell-click` · `hover-highlight` · `legal-move-highlight` · `edge-marking` (паркани на ребрах) · `connectivity-check` (пасовище) · `inventory-limit` (ємність) · `event-points` · `leftover-penalty` · `turn-enforcement` · `hot-seat` · `ai-opponent` · `match-setup` · `end-screen` · `help-window` · `save-game`.
- Уже в корпусі: `+worker-placement` (A Feast for Odin).
- **Нема** → пропозиції карток:
  - `+fence-enclosure` «Паркани на ребрах сітки замикають області» · game-logic/constraints · 🥈 · слоти {edge_counts_as_fence: false, max_fences: 15}.
  - `+pasture-capacity` «Ємність області за площею» · entities/state · 📎 · слоти {per_cell: 2}.
  - `+stable-doubles-capacity` «Будівля в області множить ємність» · entities/state · 🌱.
  - `+one-type-per-pasture` «В області — лише один вид» · game-logic/constraints · 🌱.
  - `+orthogonal-growth` «Нове — лише ортогонально до наявного того ж типу» · entities/legality · 🌱.
  - `+subdivide-region` «Розділити наявну область внутрішньою межею» · game-logic/constraints · 📎.
  - `+animal-breeding` «≥2 одного виду → +1, якщо є місце» · entities/state · 🌱.
  - `+feeding-phase` «Періодичне годування робітників, нестача → штраф» · game-logic/economy · 📎.
  - `+begging-penalty` «Картка-штраф за кожну нестачу» · game-logic/score · 🌱.
  - `+category-score-table` «Очки за кожну категорію з насиченням і −1 за нуль» · game-logic/score · 🌱.
  - `+unused-cell-penalty` «−1 за кожну порожню клітину особистого поля» · game-logic/score · 🌱.
  - `+room-material-upgrade` «Поліпшення всіх будівель разом за матеріалом» · entities/state · 🌱.
  - `+harvest-schedule` «Події за розкладом раундів» · game-logic/economy · 🌱.

## Пропозиції до словників
- `+trigger:harvest` — подія за розкладом раундів (урожай, годування, приплід); родич `schedule`.
- `+cond:enclosed(region)` — область повністю обведена межами.
- `+cond:capacity(region, op, n)` — вміст області порівняно з її ємністю.
- `+cond:orth_adjacent(cell, kind)` — клітина ортогонально сусідить з типом (точніше за `adjacent_count`, що допускає 8-сусідство).
- `+effect:build_fence(edge)` — покласти межу на ребро між клітинами.
- `+effect:breed(kind)` · `+effect:feed(n)` · `+effect:renovate(material)`.
- `+role:pasture` · `+role:fence` — область і ребро-межа як сутності.
- `+ui:capacity-badge` · `+ui:fence-counter`.
- `+window:farm-rearrange` · `+window:harvest-summary`.
- `+card:fence-enclosure` · `+card:pasture-capacity` · `+card:unused-cell-penalty`.

## Джерела
- ⭐ [UltraBoardGames: Agricola Actions](https://www.ultraboardgames.com/agricola/actions.php) — кімнати й ціни, реновація, стайні, оранка й сівба, паркани (15, по дереву, край не рахується, розширення й поділ), ємність 2 на клітину, стайня подвоює, улюбленець, ріст родини.
- [UBG: Basic Game Rules](https://www.ultraboardgames.com/agricola/game-rules.php) — раунди й етапи, урожаї, годування, жебрацтво, приплід, розміщення робітників.
- [UBG: Scoring](https://www.ultraboardgames.com/agricola/scoring.php) — таблиця очок, −1 за порожню клітину, огороджені стайні, кімнати, родина.
- [Wikipedia: Agricola (board game)](https://en.wikipedia.org/wiki/Agricola_(board_game)) — огляд, видання, iOS Playdek, All Creatures Big & Small.
- BGG: [пошук](https://boardgamegeek.com/geeksearch.php?action=search&q=Agricola); YouTube: пошук про паркани й пасовища.

## Непевне
- (?) Розмір ферми 3×5 (15 клітин) — з черги й памʼяті; відкриті сторінки UBG і Wikipedia його не називають.
- (?) Формула ємності з кількома стайнями: UBG — «стайня в пасовищі подвоює ємність»; чи подвоює кожна стайня (×2 за кожну) — з памʼяті, так.
- (?) Тай-брейк при рівних очках — на сторінках не наведено.
- (?) Чи може клітина зі стайнею бути в пасовищі як «використана» для −1 — UBG: стайня без паркану рахується використаною, огороджена — +1.
- (?) Цифрові версії після iOS 2013 (Steam-видання) — не перевіряв; вікна гіпотетичні.
