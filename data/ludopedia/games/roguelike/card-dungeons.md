---
title: Card dungeons (Dungelot, Card Crawl, Card Thief, Mini Rogue, Scoundrel)
slug: card-dungeons
family: roguelike
also: [hidden-deduction, board-digital]
klass: cursor
axes:
  field: square
  time: turn
  opponent: none
  info: hidden
  random: both
  goal: survive
year: 2011
platforms: [paper, web, iOS, Android, PC]
links:
  - {kind: other, url: "http://www.stfj.net/art/2011/Scoundrel.pdf", best: true, note: "правила Scoundrel (Zach Gage, Kurt Bieg) — 1 сторінка, звичайна колода; WebFetch: прострочений сертифікат, вміст не перечитано"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Dungelot", note: "Dungelot: розкривати плитки, ворог із ключем, двері, перки персонажів"}
  - {kind: steam, url: "https://store.steampowered.com/app/745000/Card_Crawl/", note: "Card Crawl: пасьянс-данж, 5 карт здібностей на забіг"}
  - {kind: steam, url: "https://store.steampowered.com/app/2190260/Card_Crawl_Adventure/", note: "наступник Card Crawl"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=card+thief", note: "пошук; Card Thief у видачі Steam не знайшовся"}
  - {kind: other, url: "https://boardgamegeek.com/geeksearch.php?action=search&q=mini+rogue", note: "пошук BGG; Mini Rogue (BGG віддав 403)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=scoundrel+card+game+rules", note: "пошук; правила Scoundrel"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=card+crawl+gameplay", note: "пошук; геймплей Card Crawl"}
stage: v1
coverage: 65
mechanics: [cell-click, drag-drop-piece, hp-damage, item-pickup, inventory-limit, key-and-door, reach-exit, player-death, round-currency, score-records, sequential-levels, shop-catalog, mines-after-first-click, event-points, +permadeath, +deck-as-dungeon, +room-of-cards, +flip-reveal, +weapon-degrade, +skip-room, +hand-slots, +ability-deck, +stealth-points, +key-holder-enemy, +dice-encounter, +card-layout-path, +adjacent-lock]
proposes: ["+trigger:room_dealt", "+trigger:revealed", "+trigger:card_played(card, slot)", "+cond:suit(card, s)", "+cond:last_kill(weapon, op, v)", "+cond:skipped_last", "+effect:deal(n)", "+effect:discard", "+effect:equip(card, slot)", "+effect:stack(card, on)", "+effect:to_bottom(cards)", "+role:card", "+role:supply", "+ui:deck-counter", "+ui:hand-slots", "+ui:discard-pile", "+window:ability-deck", "+window:character-select", "+feature:permadeath", "+axis:field=row", "+axis:session=run"]
author: opus
date: 2026-11-02
---

# Card dungeons — роглайк на маленькій сітці карт: переверни, виріши, чи бʼєшся, і доживи до кінця колоди

## Суть
Збірна картка моделі «**данж = колода, кімната = кілька відкритих карт**». Гравець не ходить мапою: перед ним маленька сітка або ряд карт (2×2…5×6), кожна — монстр, зброя, щит, зілля, ключ чи золото; хід = вибрати карту й розіграти її проти свого HP і слотів. Ядро — **порядок розіграшу** і управління ресурсами (HP, «зношена» зброя, обмежені слоти), а не тактика простору. Еталони: Scoundrel (2011, паперовий пасьянс), Dungelot (2012, сітка закритих плиток), Card Crawl (2015) і Card Thief (2017) від Tinytouchtales, Mini Rogue (2016, 9-картковий PnP).

## Поле і час
- **Три форми поля** (вісь варіації):
  - *Ряд-кімната з колоди* — Scoundrel, Card Crawl: 4 відкриті карти; розіграв 3 — четверта лишається, доздають до 4. `field` по суті `1d`-ряд + слоти героя.
  - *Сітка закритих плиток* — Dungelot (і клон Runestone Keeper): поверх — прямокутник закритих плиток (5×6 (?)), клік відкриває; вміст на поверсі фіксований після генерації.
  - *Сітка з аватаром-картою* — Card Thief: 3×3 карт, злодій — одна з карт, ходить на сусідню (?); Mini Rogue: 9 карт кімнат ромбом 1-2-3-2-1 (?), шлях згори вниз.
- Час — покроковий, хід = розіграш однієї карти/плитки. Ворожих ходів нема: монстр «відповідає» лише на розіграш (Dungelot — удар у відповідь, поки ворог живий).
- Інформація: колода закрита, кімната відкрита (Scoundrel/Card Crawl) або все закрито до кліку (Dungelot) — `info: hidden`. Випадковість — тасування; у Mini Rogue ще й кубики (`random: both`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | HP (Scoundrel 20, Card Crawl 13 (?)), слоти | не на полі (крім Card Thief) — стан у панелі |
| Колода данжу | supply | 44 карти (Scoundrel), 54 (Card Crawl (?)) | з неї доздаються кімнати; скінчилась — перемога |
| Монстр ♣♠ (Scoundrel) | enemy | значення 2–14 (J=11 … A=14) | шкода = значення мінус зброя; голіруч — повна |
| Зброя ♦ | pickup | значення 2–10 | екіпірується; бʼє лише монстрів, слабших за останнього вбитого нею |
| Зілля ♥ | pickup | значення | лікує до максимуму 20; друге в тій самій кімнаті — скидається без ефекту |
| Щит (Card Crawl) | pickup | значення | у руці поглинає шкоду монстра (?) |
| Монета (Card Crawl) | pickup | значення | +золото = рахунок забігу |
| Карта здібності (Card Crawl) | pickup | 5 на забіг з 40 | разова дія (лікування, обмін, знищення) |
| Закрита плитка (Dungelot) | tile | — | клік → `reveal`: монстр/предмет/пастка/порожньо |
| Монстр з ключем (Dungelot) | enemy | HP, атака | убити → ключ |
| Двері поверху (Dungelot) | gate | — | з ключем → наступний поверх |
| Скриня / зілля / пастка (Dungelot) | container / pickup / hazard | — | дає предмет / лікує / шкодить при відкритті (?) |
| Злодій (Card Thief) | player | очки скритності | ходить по сусідніх картах (?) |
| Вартовий (Card Thief) | enemy | значення | прохід повз — мінус скритність (?) |
| Смолоскип (Card Thief) | hazard | — | освітлює сусідні карти, вартові «бачать» (?) |
| Кімната Mini Rogue | zone | тип: монстр/скарб/пастка/торговець/відпочинок/подія/бос | розігрується кидком кубиків (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
Scoundrel (найповніше, джерело — правила авторів):
- КОЛИ `game_start` → ТО колода 52 без джокерів, червоних фігур і червоних тузів = 44 карти; HP 20.
- КОЛИ `room_dealt` → ТО `deal(4 − leftover)` → кімната з 4 відкритих карт.
- КОЛИ `input(avoid room)` → ЯКЩО `not skipped_last` → ТО `to_bottom(all 4)`, нова кімната; двічі поспіль не можна.
- КОЛИ `input(play card)` → ЯКЩО розіграно 3 з 4 → ТО четверта лишається, `room_dealt`.
- КОЛИ `card_played(♦)` → ТО `equip(weapon)`, `discard(old weapon + monsters on it)`.
- КОЛИ `card_played(♥)` → ЯКЩО перше зілля в кімнаті → ТО `heal(hero, value)` (max 20); інакше `discard`.
- КОЛИ `card_played(♣♠)` → ЯКЩО обрано «зброєю» і `last_kill(weapon, >, value)` (або зброя ще не вбивала) → ТО `damage(max(0, value − weapon))`, `stack(monster, on weapon)`; інакше «голіруч» → `damage(value)`.
- КОЛИ `hp_zero(hero)` → ТО `lose`, рахунок = HP − сума монстрів у колоді (відʼємний).
- КОЛИ колода й кімната порожні → ТО `win`, рахунок = HP (+ значення зілля, якщо HP 20 і остання карта — зілля).
Card Crawl (?):
- КОЛИ кімната зменшилась до 1 карти → ТО `deal(3)`.
- КОЛИ `card_played(monster → hero)` → ТО `damage(value)`; `card_played(monster → sword)` → `damage(monster, sword)`; щит у руці — поглинає.
- КОЛИ `card_played(card → coins counter)` → ТО `custom: «продати карту за золото»` (?).
- КОЛИ колоду розіграно → ТО `win`, рахунок = золото.
Dungelot:
- КОЛИ `input(click tile)` → ЯКЩО `not adjacent_lock(tile)` (?) → ТО `reveal(tile)`.
- КОЛИ `input(click monster)` → ТО `damage(monster, atk 1–3)`; ЯКЩО монстр живий → ТО `damage(hero)` у відповідь.
- КОЛИ `died(key_holder)` → ТО `give(hero, key)`; КОЛИ `contact(hero, door)` → ЯКЩО `has(key)` → ТО `next_level`.
- КОЛИ `hp_zero(hero)` → ТО `lose`, рестарт з поверху 1.
Card Thief / Mini Rogue (?):
- КОЛИ `input(move thief → adjacent card)` → ЯКЩО на карті вартовий → ТО `counter(stealth, −value)`; `counter(stealth, ==, 0)` → провал крадіжки.
- КОЛИ `enter(room)` (Mini Rogue) → ТО `custom: «кидок кубиків визначає бій/знахідку/пастку»`; рух лише на сусідню карту нижнього ряду.
- Перемога: розіграти колоду / дійти до виходу / вбити боса. Поразка: HP = 0. Рахунок: HP (Scoundrel), золото (Card Crawl), глибина/поверх (Dungelot).

## Керування і ввід
- Папір (Scoundrel, Mini Rogue): руки й колода, кубики.
- Тач/миша: Card Crawl — **drag-and-drop** карти на героя / в руку / в рюкзак / на монстра (`drag-drop-piece`); Dungelot — тап по плитці (`cell-click`); Card Thief — перетягнути злодія на сусідню карту (?).
- Вибір режиму удару в Scoundrel (зброєю чи голіруч) — окреме рішення гравця.

## Вікна, меню, HUD
- `game-screen` — ряд/сітка карт + `hp-bar`, `deck-counter` (скільки лишилось у колоді), `hand-slots` (ліва/права рука, рюкзак — Card Crawl), `discard-pile`, золото (`coins`).
- `ability-deck` (Card Crawl) — вибір 5 карт здібностей перед забігом.
- `character-select` (Dungelot) — персонажі з перками, відкриваються поверхами.
- `shop-window` (Dungelot, Mini Rogue-торговець) (?).
- `end-screen` — рахунок/поверх; `leaderboard` (Game Center (?)); `main-menu`, `settings-window`.
- Переходи: `main-menu` → (`ability-deck` | `character-select`) → `game-screen` → `end-screen`.

## Фічі поза полем
- `permadeath` і короткий забіг (5–10 хв); `meta-progression` — відкриття здібностей (Card Crawl) і персонажів (Dungelot).
- `leaderboard-online`, `mode-daily` (?), `achievements`.
- Паперові: правила на одній сторінці, звичайна колода — `rules-page`.

## Варіації й родичі
- Donsol (Scoundrel з іншою колодою), Dungeon Solitaire, Runestone Keeper (клон Dungelot), Card Crawl Adventure, Ring of Pain (коло карт), Dragonsweeper / Minesweeper (закриті клітини з числами), Desktop Dungeons (розкриття як ресурс).
- Осі варіацій: **поле** (ряд з колоди / закрита сітка / сітка з аватаром) · **що лишається між кімнатами** (одна карта / нічого / весь поверх) · **зброя** (вічна / зношується порогом / розряджається) · **втеча** (пропуск кімнати з обмеженням / нема) · **випадковість** (лише тасування / ще й кубики).

## Цікавинки для курсу
- Scoundrel повністю: колода → кімнати по 4, пропуск без повтору, зношування зброї порогом — 🥉 (вся гра — один файл, ідеальний консольний роглайк).
- Зброя, що бʼє лише слабших за останнього вбитого (монотонний стек) — 📎.
- Ряд-кімната «розіграй 3, четверта лишається» — 🌱 (черга з переносом).
- Сітка закритих плиток із ворогом-ключником і дверима (Dungelot) — 📎; з блокуванням сусідніх плиток монстром — 🥉.
- Розвʼязувач Scoundrel: «чи виграшна ця колода» — перебір порядку розіграшу з мемоізацією — 🥇.
- Drag-and-drop розіграш у слоти (рука/рюкзак/герой) — 🥉 (GUI з цілями скидання).

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` · `hp-damage` · `item-pickup` · `inventory-limit` (руки + рюкзак) · `key-and-door` · `reach-exit` · `player-death` · `round-currency` · `score-records` · `sequential-levels` (поверхи Dungelot) · `shop-catalog` · `event-points` · `mines-after-first-click` (близько: вміст фіксується при генерації поверху (?)).
- **Нема** → пропозиції карток:
  - `+deck-as-dungeon` «Данж — це колода» · levels/generation · 📎 · слот {deck}.
  - `+room-of-cards` «Кімната з N карт, одна переходить далі» · game-logic/waves · 🌱 · слоти {n, carry}.
  - `+flip-reveal` «Перевернути закриту карту/плитку» · interface/input · 🌱.
  - `+weapon-degrade` «Зброя слабшає/обмежується після вбивства» · entities/combat · 📎.
  - `+skip-room` «Пропустити кімнату з обмеженням» · game-logic/difficulty · 🌱.
  - `+hand-slots` «Слоти рук і рюкзака для карт» · entities/state · 📎.
  - `+ability-deck` «Колода здібностей на забіг» · game-logic/economy · 📎.
  - `+stealth-points` «Скритність як ресурс проходу повз ворогів» · entities/state · 📎.
  - `+key-holder-enemy` «Ключ у конкретного ворога» · entities/interact · 🌱.
  - `+dice-encounter` «Подія кімнати визначається кидком» · game-logic/score · 🌱.
  - `+card-layout-path` «Шлях по розкладці карт (ромб, ряди)» · levels/progression · 📎.
  - `+adjacent-lock` «Відкритий ворог блокує сусідні плитки» · entities/legality · 📎.
  - `+permadeath` — як у Rogue.

## Пропозиції до словників
- `+trigger:room_dealt` — доздано кімнату; `+trigger:revealed` (як у Rogue); `+trigger:card_played(card, slot)` — карту розіграно в ціль.
- `+cond:suit(card, s)` — масть/тип карти; `+cond:last_kill(weapon, op, v)` — значення останнього вбитого зброєю; `+cond:skipped_last` — минулу кімнату пропущено.
- `+effect:deal(n)` · `+effect:discard` · `+effect:equip(card, slot)` · `+effect:stack(card, on)` · `+effect:to_bottom(cards)` — карткові дії, яких нема в клітинному словнику.
- `+role:card` — сутність-карта з мастю/значенням (не `tile`: не зливається, розігрується); `+role:supply` (🔥) — колода.
- `+ui:deck-counter` · `+ui:hand-slots` · `+ui:discard-pile`.
- `+window:ability-deck` — вибір карт здібностей; `+window:character-select` (⏳).
- `+feature:permadeath`.
- `+axis:field=row` — поле-ряд з N відкритих слотів (не `1d`-смуга руху); `+axis:session=run`.

## Джерела
- ⭐ [Scoundrel — правила (PDF)](http://www.stfj.net/art/2011/Scoundrel.pdf) — авторська сторінка правил; цифри вище — з неї за памʼяттю (WebFetch: прострочений сертифікат).
- [Wikipedia: Dungelot](https://en.wikipedia.org/wiki/Dungelot) — розкриття плиток, атака 1–3, ворог-ключник, двері, перки, рестарт з поверху 1, клон Runestone Keeper.
- [Steam: Card Crawl](https://store.steampowered.com/app/745000/Card_Crawl/) — пасьянс-данж, 5 карт здібностей з 40, Arnold Rauers.
- [Steam: Card Crawl Adventure](https://store.steampowered.com/app/2190260/Card_Crawl_Adventure/).
- [Steam: пошук Card Thief](https://store.steampowered.com/search/?term=card+thief) · [BGG: пошук Mini Rogue](https://boardgamegeek.com/geeksearch.php?action=search&q=mini+rogue).
- YouTube: пошук «scoundrel card game rules», «card crawl gameplay».

## Непевне
- (?) Card Crawl: 54 карти, 13 HP, «доздати 3, коли лишилась 1», продаж карт за золото — з памʼяті; Steam-опис цього не каже (і дата Steam 2018 — порт, мобільна версія 2015).
- (?) Card Thief: механіка скритності, вартових і смолоскипів — з памʼяті, сторінки не знайшов.
- (?) Mini Rogue: ромб 1-2-3-2-1 з 9 карт і кубикові події — з памʼяті.
- (?) Dungelot: розмір сітки 5×6 і блокування сусідніх плиток монстром (можливо, це правило Runestone Keeper).
- (?) Scoundrel: чи зброя бʼє монстрів «менших» чи «менших або рівних» за останнього — у переказах розходяться.
