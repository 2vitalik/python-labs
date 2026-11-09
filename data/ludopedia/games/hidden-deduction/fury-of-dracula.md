---
title: The Fury of Dracula
slug: fury-of-dracula
aka: [Fury of Dracula, "Fury of Dracula: Digital Edition"]
family: hidden-deduction
also: [board-digital]
klass: hybrid
axes:
  field: graph
  time: turn
  opponent: hotseat
  info: hidden
  random: both
  goal: race
year: 1987
platforms: [board (Games Workshop 1987, Fantasy Flight 2006 / 2015, WizKids 2019), PC (Nomad Games 2020)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/The_Fury_of_Dracula", best: true, note: "історія 4 редакцій, прихований рух Дракули, стрічка з 6 місць, дозрівання зустрічей, мисливці, укуси, день/ніч, бій, умови перемоги"}
  - {kind: other, url: "https://www.ultraboardgames.com/fury-of-dracula/game-rules.php", note: "базові правила 3-ї редакції: компоненти, фази, дії мисливців, хід Дракули, стрічка, перемога 13 / 15"}
  - {kind: other, url: "https://www.ultraboardgames.com/fury-of-dracula/additional-rules.php", note: "розкриття схованок, засідка, пошук, дозрівання, бій, укуси, час і відчай, блокпости, шторми"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=fury+of+dracula+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 65
mechanics: [turn-enforcement, hot-seat, fog-of-war, hp-damage, inventory, inventory-items, hidden-under-block, spawn-schedule, timed-despawn, move-notation, message-log, remaining-counter, objective-text, game-screen, end-screen, main-menu, help-window, match-setup, character-select, pass-device, ai-opponent, +hidden-movement, +trail-of-locations, +encounter-trap-placement, +encounter-maturing, +trail-reveal-on-visit, +influence-track, +day-night-phases, +simultaneous-card-combat, +team-vs-one, +belief-set-tracking, +transport-by-ticket]
proposes: ["+effect:secret_move", "+effect:mature", "+cond:edge_type", "+role:trail", "+ui:trail-strip", "+ui:time-track", "+ui:influence-track", "+window:combat-window", "+card:trail-of-locations", "+card:encounter-trap-placement", "+card:encounter-maturing", "+card:trail-reveal-on-visit", "+card:influence-track", "+card:day-night-phases", "+card:simultaneous-card-combat"]
author: opus
date: 2026-11-09
---

# The Fury of Dracula — Дракула таємно рухається Європою, лишаючи стрічку з шести карт місць, і мінує їх зустрічами; мисливці йдуть по сліду

## Суть
Один гравець — Дракула, решта (до 4) — мисливці. Дракула ходить приховано: кожен хід кладе лицем донизу карту нового сусіднього місця в початок **стрічки з 6 позицій**, і на неї — карту зустрічі (пастка, вовки, новий вампір). Мисливці, ставши в місто зі стрічки, відкривають його карту — так видно слід і напрям руху. Старі місця зсуваються по стрічці й **дозрівають**: вампір, що дійшов до кінця, дає Дракулі вплив. `klass: hybrid`: Дракула — **avatar** прихований, мисливці — **figure** (команда з 4 фігур зі здібностями). Описую 3-тю редакцію (FFG 2015), відмінності — у «Варіаціях».

## Поле і час
- Граф Європи 1898 р.: великі й малі міста, морські зони, порти; ребра — дороги, залізниці, морські шляхи. Замок Дракули — окреме місце.
- Раунд: фаза мисливців (кожен — денна дія, потім кожен — нічна дія) → фаза Дракули.
- Трек часу: день/ніч, тиждень; на світанку / смерканні — бій, якщо Дракула відкритий; з неділі на понеділок — жетон відчаю (до 3).
- Видимість: мисливці відкриті; Дракула — лише перша позиція стрічки «під фішкою»; морські карти мають іншу сорочку (видно, що він у морі).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дракула | player | 15 шкоди = смерть; рука 5 зустрічей; карти бою | таємно ходить дорогою чи морем, ніколи залізницею |
| Мисливці (Godalming, Seward, Mina Harker, Van Helsing) | piece | здоров'я, порядок ходу, здібність | день/ніч — по одній дії; Mina падає від першого укусу, Van Helsing — від третього |
| Місто велике / мале | static | — | вузол; лише у великому — постачання предметів |
| Морська зона / порт | terrain | — | вдень у морі мусиш рухатись, уночі — пас; Дракулі море коштує шкоди |
| Залізниця | terrain | значення квитка | лише мисливці, з квитком; квиток визначає кількість залізниць |
| Карта місця | mark | місто, сорочка суша/море | кладеться в стрічку лицем донизу |
| Стрічка (trail) | zone | 6 позицій | схованки зсуваються вправо щоходу Дракули |
| Карта зустрічі | hazard | ефект засідки, ефект дозрівання | лежить на схованці; засідка або дозрівання |
| Вампір (New / Aristocratic / Reckless) | hazard | число впливу | дозріває → `+influence`, чистить схованки |
| Предмети мисливців | pickup | 38 карт | зброя й спорядження; обмін у місті |
| Події | pickup | 75 карт | день — з верху колоди, ніч — з низу; іконка Дракули → до Дракули (вночі) або в скид |
| Квиток | supply | значення; ≤2 у руці | для залізниці |
| Блокпост / шторм / туман / кажан | hazard | жетони | блокпост закриває дорогу/залізницю, шторм — морську зону, туман — пошук |
| Лікарня (Madrid, Rome, Budapest) | zone | — | куди йде переможений мисливець |
| Трек впливу | zone | 0…13 | 13 — перемога Дракули |

## Правила (КОЛИ → ЯКЩО → ТО)
- Старт: КОЛИ `game_start` → ТО `custom: «Дракула таємно обирає місто (не море, не замок, не місто мисливця) і кладе його карту на 1-шу позицію стрічки»`; рука 5 зустрічей.
- КОЛИ `turn_start(dracula)` → ТО `custom: «усі схованки зсуваються на 1 вправо»`, `custom: «нова карта сусіднього місця лицем донизу на позицію 1»` — прихований хід.
- КОЛИ `custom: «Дракула ходить морем»` → ТО `damage(dracula, 2)` порт→море або `damage(dracula, 1)` море→море; сорочка морської карти видима.
- КОЛИ `custom: «Дракула став у місто мисливця»` → ТО `reveal(dracula)`.
- КОЛИ `custom: «новий хід на суші, Дракула не відкритий»` → ТО `place(dracula, encounter)` на нову схованку; КОЛИ `count(hand, <, 5)` → ТО `custom: «добрати до 5»`.
- КОЛИ `custom: «схованка дійшла до 6-ї позиції»` → ТО `choose(mature | discard)`; дозрілий вампір → `counter(influence, +n)`, карта місця повертається в колоду.
- КОЛИ `enter(hunter, city)` → ЯКЩО `custom: «місто є в стрічці»` → ТО `reveal(location_card)` — слід видно до повернення карти в колоду.
- КОЛИ `enter(hunter, city)` → ЯКЩО `custom: «місто — 1-ша позиція стрічки»` → ТО `reveal(dracula)`, бій на найближчому світанку / смерканні.
- КОЛИ `enter(hunter, hideout)` → ЯКЩО `custom: «на схованці зустріч»` → ТО `choose(ambush)` Дракули: розіграти одну зустріч без ефекту дозрівання і скинути.
- КОЛИ `input(search)` → ЯКЩО `occupied(cell, encounter)` and `not state(city, fog)` → ТО `reveal(encounters)` і розіграти їх без дозрівання.
- КОЛИ `input(move)` → ЯКЩО `custom: «день»` → ТО `move(hunter, road|sea)`; ЯКЩО `has(hunter, ticket)` → залізницею на значення квитка; ЯКЩО `occupied(edge, roadblock)` → `block`.
- КОЛИ `input(supply)` → ЯКЩО `cell(city, large)` → ТО `give(hunter, item)`; потім подія: день — з верху, ніч — з низу; іконка Дракули вночі → `give(dracula, event)`.
- КОЛИ `input(rest)` → ТО `heal(hunter, 1)`; `input(trade)` → обмін предметами й квитками в одному місті; `input(reserve_ticket)` → `give(hunter, ticket)` (≤2).
- КОЛИ `custom: «світанок або смеркання»` → ЯКЩО `custom: «мисливець і відкритий Дракула в одному місті»` → ТО `window(combat-window)`.
- Бій: КОЛИ `turn_start(combat_round)` → ТО `custom: «обидві сторони таємно кладуть карту, відкривають разом»`; ЯКЩО `same(hunter_card, dracula_card, icon)` → ТО `custom: «карту Дракули скасовано»`; далі ефект Дракули, ефект мисливця; до 6 карт Дракули або до втечі (Escape as Bat / Mist) чи смерті.
- КОЛИ `custom: «Fangs проти загіпнотизованого мисливця»` → ТО `counter(influence, +1)`, `give(hunter, bite)`.
- КОЛИ `state(hunter, bitten)` → ТО `custom: «тримати одну подію й один предмет відкритими»`.
- КОЛИ `hp_zero(hunter)` → ТО `custom: «на світанку — до найближчої лікарні, скинути карти й жетони»`, `counter(influence, +2 + despair)`.
- КОЛИ `custom: «неділя → понеділок»` → ТО `place(despair_token)`; КОЛИ `count(despair, =, 3)` → ТО `custom: «здібність The Fury of Dracula»`.
- КОЛИ `custom: «смеркання»` → ТО `custom: «зняти один блокпост і один шторм»`.
- КОЛИ `counter(influence, ≥, 13)` → ТО `win` (Дракула).
- КОЛИ `counter(dracula_damage, ≥, 15)` → ТО `win` (мисливці).
- Перемога Дракули: вплив 13 · Перемога мисливців: 15 шкоди Дракулі · Рахунок: трек впливу.

## Керування і ввід
- Дракула: таємно обирає карту місця з колоди і зустріч з руки; на розкриття — перевертає карти стрічки; в бою — закрита карта бою.
- Мисливці: радяться відкрито, кожен обирає дію за порядком; в бою — закрита карта з предметів + Dodge / Punch / Escape.
- 1–3 гравці-мисливці керують кількома мисливцями.
- Цифрова версія (Nomad Games): клік по фігурі → досяжні вузли; дії кнопками; Дракула — окремий прихований інтерфейс з передачею пристрою або проти AI (?).

## Вікна, меню, HUD
- `main-menu` / `match-setup` (цифрова версія): хто Дракула (людина/AI), скільки гравців, базова / розширена гра.
- `character-select` (цифрова версія): розподіл мисливців між гравцями; у розширеній грі — стартові міста.
- `game-screen` (цифрова версія): граф Європи, фігури мисливців; `trail-strip` — 6 позицій стрічки (закриті/відкриті карти, морська сорочка, зустрічі на схованках); `time-track` (день/ніч, тиждень, відчай); `influence-track`; планшети мисливців (здоров'я, укуси, предмети, події, квитки); `turn-indicator`.
- `combat-window` (цифрова версія): руки карт, одночасне відкриття, кидання/скасування.
- `pass-device` (цифрова версія) — коли за одним екраном ходить Дракула.
- `end-screen` (цифрова версія): хто виграв, повний маршрут Дракули (`replay-window`) (?).
- Переходи: setup → game-screen ↔ combat-window ↔ pass-device → end-screen.

## Фічі поза полем
- Розширена гра (advanced rules): вибір стартових міст тощо (?).
- `ai-opponent-levels` (?) — AI за Дракулу в цифровій версії.
- `tutorial` (цифрова версія) (?).

## Варіації й родичі
- 1-ша (GW 1987): прихований рух на окремій дошці Дракули, бій жетонами, кидок кубика на час доби, крові 12 + Blood Death, великі/малі перемоги; 3 мисливці.
- 2-га (FFG 2006): Mina, трек вампірів (перемога на 6), карти стрічки, 15 крові.
- 3-тя (FFG 2015): Дракула діє лише вночі, жетони чуток, трек впливу (13). 4-та (WizKids 2019): фарбовані фігури, більші карти бою; цифрова (2020) — на основі 4-ї.
- Родичі: [scotland-yard.md](scotland-yard.md) — прихований рух графом з журналом; Letters from Whitechapel (?); [hunt-the-wumpus.md](hunt-the-wumpus.md).
- **Осі варіацій**: слід «журнал номерів (Scotland Yard) / стрічка карт, що відкриваються при відвідуванні (тут)»; прихований гравець «лише тікає / ще й мінує слід»; таймер «кінець журналу / трек впливу, що росте від дозрівань і перемог»; бій «нема / одночасні закриті карти».

## Цікавинки для курсу
- Стрічка з 6 позицій як черга (deque): push у голову, зсув, «дозрівання» на хвості — 🌱.
- Розкриття схованки при відвідуванні мисливцем + множина можливих позицій Дракули з відкритих карт і сорочок — 🥈.
- Зустріч-пастка на схованці з двома ефектами (засідка зараз / дозрівання потім) — 📎.
- Одночасний бій закритими картами зі скасуванням за іконкою — 📎.
- Дві фази на хід (день / ніч) і різні правила моря вдень і вночі — 🌱.
- AI за Дракулу: максимізувати невизначеність і час до дозрівання — 🥇.

## Мапа на каталог
- Є: `turn-enforcement` / `hot-seat` · `fog-of-war` ↔ позиція Дракули · `hp-damage` · `inventory` / `inventory-items` ↔ предмети · `hidden-under-block` ↔ зустріч під картою місця · `spawn-schedule` ↔ жетони відчаю щотижня · `timed-despawn` ↔ схованка йде зі стрічки · `move-notation` / `message-log` ↔ стрічка · `remaining-counter` / `objective-text` · `game-screen` / `end-screen` / `main-menu` / `help-window` / `match-setup` / `character-select` / `pass-device` · `ai-opponent`.
- **Нема** → пропозиції карток:
  - `+trail-of-locations` «Стрічка N останніх прихованих місць» · game-logic/info · 📎 · слот {length: 6}.
  - `+encounter-trap-placement` «Прихований гравець мінує свій слід» · entities/spawn · 📎.
  - `+encounter-maturing` «Пастка дозріває, дійшовши до кінця стрічки» · game-logic/rules · 🌱.
  - `+trail-reveal-on-visit` «Відвідане місто відкриває карту сліду» · game-logic/info · 🌱.
  - `+influence-track` «Трек очок прихованої сторони до порогу» · game-logic/goals · 🌱 · слот {target: 13}.
  - `+day-night-phases` «Хід ділиться на денну й нічну дію» · game-logic/turns · 🌱.
  - `+simultaneous-card-combat` «Бій одночасними закритими картами» · entities/combat · 📎.
  - Також: `+hidden-movement`, `+team-vs-one`, `+belief-set-tracking`, `+transport-by-ticket` (див. Scotland Yard).

## Пропозиції до словників
- `+effect:secret_move` — повтор (Scotland Yard): прихований хід із записом у стрічку.
- `+effect:mature` — прихована зустріч спрацьовує з окремим ефектом, дійшовши до кінця стрічки.
- `+cond:edge_type` — повтор: ребро потрібного виду (дорога / залізниця / море).
- `+role:trail` — черга прихованих позицій, що зсувається щоходу.
- `+ui:trail-strip` — стрічка з N слотів з закритими/відкритими картами.
- `+ui:time-track` — трек день/ніч і тижнів; `+ui:influence-track` — шкала очок до порогу перемоги.
- `+window:combat-window` — окремий екран бою картами.

## Джерела
- ⭐ [Wikipedia: The Fury of Dracula](https://en.wikipedia.org/wiki/The_Fury_of_Dracula) — 4 редакції з відмінностями, прихований рух, стрічка з 6 місць і 7-ма позиція в 2-й редакції, мисливці, укуси, день/ніч, бій, перемога.
- [UltraBoardGames: базові правила](https://www.ultraboardgames.com/fury-of-dracula/game-rules.php) — компоненти, стартові міста, фази, 7 дій мисливців, хід Дракули, море, стрічка, вплив 13 / шкода 15.
- [UltraBoardGames: додаткові правила](https://www.ultraboardgames.com/fury-of-dracula/additional-rules.php) — розкриття, засідка, пошук, дозрівання, вампіри, бій у 6 кроків, лікарні, укуси, відчай, блокпости, шторми.

## Непевне
- (?) П'ять карт сил Дракули (Hide, Double Back, Feed, Wolf Form, Dark Call) і катакомби — названі в компонентах, ефекти в джерелах не описані; правил не пишу.
- (?) Чи на 3-й редакції дозрівання на 6-й позиції (ultraboardgames) проти 7-ї (WP про 2-гу) — записано за 3-ю.
- (?) Цифрова версія: AI, туторіал, екран бою, показ маршруту — не бачив.
- (?) Жетони чуток (3-тя редакція) — лише згадка в WP.
- (?) Рух Дракули в 3-й редакції «лише вночі» (WP) проти фазової схеми ultraboardgames — не звів.
