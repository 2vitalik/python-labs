---
title: Inscryption (Act 1)
slug: inscryption
family: tower-lanes
also: [roguelike]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: score
year: 2021
platforms: [PC, Mac, Linux, PS4, PS5, Switch, Xbox]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Inscryption", best: true, note: "поле 3×4, черга суперника, ваги, жертви кровʼю, сигіли, death cards"}
  - {kind: steam, url: "https://store.steampowered.com/app/1092790/Inscryption/"}
  - {kind: play, url: "https://dmullinsgames.itch.io/sacrifices-must-be-made", note: "безкоштовний прототип Sacrifices Must Be Made"}
  - {kind: fandom, url: "https://inscryption.fandom.com/wiki/Sigils", note: "список сигілів; сервер не відкрився (402)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=inscryption+act+1+gameplay", note: "пошук; геймплей Act 1"}
stage: v1
coverage: 60
mechanics: [hp-damage, piece-capture, turn-enforcement, ai-opponent, telegraphed-intents, round-currency, inventory-items, inventory-limit, shop-catalog, spawn-schedule, event-points, dungeon-generation, save-progress, +lane-grid, +opponent-queue-row, +sacrifice-cost, +scale-tug-of-war, +card-sigils, +deck-draw, +death-card]
proposes: ["+trigger:card_played", "+trigger:attacked", "+cond:lane_has", "+effect:sacrifice", "+effect:advance_queue", "+effect:scale_shift", "+effect:draw", "+effect:jump_over", "+role:card", "+role:lane", "+ui:scale-meter", "+ui:queue-row", "+ui:bell-button", "+window:map-window", "+window:deck-window", "+window:choice-window", "+feature:run-map", "+axis:session"]
author: opus
date: 2026-11-02
---

# Inscryption (Act 1) — карткова битва на 4 смугах: жертвуй істотами, перехили ваги на 5 зубів

## Суть
Гравець грає карти-істоти в нижній ряд поля 3×4; суперник Leshy спершу кладе свої карти в **задній ряд-чергу**, і наступного ходу вони висуваються вперед. Кожна карта бʼє карту навпроти в своїй колонці, а якщо там порожньо — по вагах: шкода стає «зубами» на шальці, і хто перехилить ваги на 5 — виграв. Ціна карт — кров (пожертвувати свої істоти з поля) або кістки (накопичуються від смертей). Колонки поводяться як смуги PvZ, а черга суперника — як `telegraphed-intents`.

## Поле і час
- Поле 3 ряди × 4 колонки: нижній — гравця, середній — атакуючий ряд Leshy, верхній — **черга** Leshy (видно, що прийде). (Act 3 — 3×5.)
- Колонка = смуга: атака йде лише навпроти; сигіли змінюють колонки удару.
- Покрокова гра: хід гравця (взяти карту → зіграти скільки завгодно → дзвіночок) → атака карт гравця зліва направо → хід Leshy (черга висувається, нові карти в чергу) → атака карт Leshy.
- Між битвами — карта забігу з вузлами-подіями (роглайк-мапа).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Карта-істота | piece (`+role:card`) | power, health, ціна (кров 0–4 / кістки), сигіли, плем'я | б'є колонку навпроти після дзвоника |
| Білка (side deck) | piece | 0/1, ціна 0 | паливо для жертв; окрема колода |
| Ваги | static | баланс −5…+5 | шкода «в обличчя» кладе зуби на шальку; ±5 — перемога/поразка |
| Кістки | resource | лічильник | +1 за кожну свою смерть (Bone King +4) |
| Кров | resource | на вимогу | = кількість пожертвуваних карт (Worthy Sacrifice = 3) |
| Черга Leshy | zone | 4 слоти | карти чекають, на початку його ходу висуваються в порожні клітини переднього ряду |
| Свічки | static | 2 полумʼя | програш битви гасить одне; обидва — кінець забігу |
| Предмети | pickup | ≤3 слоти | одноразові: кліщі (вирвати свій зуб → +1 на ваги), ножиці (знищити карту суперника), пісочний годинник (пропустити хід суперника), пляшка з білкою, гачок (забрати карту суперника) (?) |
| Leshy (дилер) | boss | — | ставить карти за сценарієм бою; боси — 2 фази |
| Death card | piece | ціна однієї карти + стати іншої + сигіли третьої | твориться після смерті персонажа, зʼявляється в наступних забігах |
| Pelts / Trapper-Trader | resource / neutral | — | шкури обмінюються на карти (?) |

Сигіли (здібності, частина Act 1):
| Сигіл | Ефект |
|---|---|
| Airborne | атакує ваги напряму, ігноруючи істоту навпроти |
| Mighty Leap | блокує Airborne-атаку |
| Bifurcated Strike | б'є дві діагональні колонки замість навпроти |
| Trifurcated Strike | б'є три колонки |
| Touch of Death | убиває будь-яку істоту, якій завдав шкоди |
| Sprinter | після атаки переходить у сусідню колонку |
| Fledgling | через хід перетворюється на дорослу форму |
| Many Lives | не гине при жертві (кіт) |
| Unkillable | після смерті повертається в руку |
| Bees Within | коли б'ють — у руку приходить Бджола |
| Burrower | переходить у порожню колонку, по якій б'ють ваги |
| Sharp Quills | шкодить 1 тому, хто її атакував |
| Stinky | істота навпроти −1 power |
| Worthy Sacrifice | рахується як 3 крові |
| Bone King | дає 4 кістки замість 1 при смерті |
| Waterborne | у хід суперника пірнає — атака йде у ваги |
| Guardian | переходить навпроти щойно зіграної карти суперника |
| Leader | сусіди +1 power |
| Corpse Eater | сама виходить у колонку, де загинула твоя істота |
| Ant Spawner · Rabbit Hole · Dam Builder | при грі дає Мураху / Кролика / ставить греблі в сусідні колонки |
| Loose Tail | коли атакують — відбігає, лишаючи хвіст |
| Hefty | рухається, штовхаючи інших |
| Made of Stone | імунна до Touch of Death і Stinky |
| Хвіст-«стати» | power = к-сть мурах (Ant) / дзеркало навпроти (Mirror) / карт у руці (Hand) / відстань до дзвоника (Bell) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «effect draw: 1 карта з основної АБО з білячої колоди — на вибір»`; на старті битви — 3 основні + 1 білка (?).
- КОЛИ `input(play, card, cell)` → ЯКЩО ціна кровʼю → ТО `custom: «effect sacrifice: вибрати свої карти на суму крові»`, вони `disappear`, `counter(bones, +n)`, карта `spawn` у вільну (чи щойно звільнену) клітину; ціна кістками → `counter(bones, -n)`.
- КОЛИ `input(bell)` → ТО для кожної карти гравця зліва направо: ЯКЩО `cond:lane_has(enemy, opposite)` and `not` сигіл Airborne → ТО `damage(enemy, power)`; інакше `custom: «effect scale_shift(+power)»`.
- КОЛИ `hp_zero(card)` → ТО `disappear_a`, власник `counter(bones, +1)`; сигіли смерті (Unkillable, Frozen Away) — `trigger`.
- КОЛИ `turn_start(leshy)` → ТО `custom: «effect advance_queue: карта з черги стає в передню клітину колонки, якщо та порожня»`, нові карти `spawn` у чергу за сценарієм.
- Далі карти Leshy атакують за тим самим правилом у бік гравця (`scale_shift(-power)`).
- КОЛИ `counter(scale, >=, +5)` → ТО `win` (битва); надлишок шкоди → зуби як валюта (?) · КОЛИ `counter(scale, <=, -5)` → ТО `custom: «згасити свічку»`, `restart` битви чи вихід.
- КОЛИ `custom: «згасли обидві свічки»` → ТО `lose` (кінець забігу), `custom: «створити death card»`.
- КОЛИ `contact(attacker, sharp_quills)` → ТО `damage(attacker, 1)`; Touch of Death → `disappear_b` при будь-якій шкоді, крім Made of Stone.
- КОЛИ `card_played(enemy)` → ЯКЩО `has(player, guardian)` → ТО `move(guardian, opposite)`.
- Предмети: КОЛИ `input(use, item)` → ТО ефект предмета (`damage`, `skip_turn`, `custom: «вирвати зуб»` = `scale_shift(+1)`), `take(item)`.
- Вузли мапи: вибір 1 з 3 карт; багаття (+power/+health з ризиком втратити карту); камені (перенести сигіл жертвою іншої карти); мікологи (злиття двох однакових); тотем (сигіл усьому племені); торгівля шкурами (?).
- Перемога: пройти 3 мапи з босами + Leshy · Поразка: обидві свічки згасли · Рахунок: баланс ваг у битві.

## Керування і ввід
- Від першої особи за столом: клік по колоді для добору, drag/клік карти → клік по клітині; клік по своїх картах на полі — вибір жертв (ножем).
- Дзвоник — кінець ходу; клік по предмету — використати; огляд (вгору/вбік) — кімната хатини з пазлами escape-room.
- Наведення на карту/сигіл — підказка з описом.

## Вікна, меню, HUD
- `game-screen` (стіл): поле 3×4, ваги з зубами (`+ui:scale-meter`), дзвоник (`+ui:bell-button`), колоди (основна і біляча), рука, лічильник кісток, слоти предметів, свічки.
- `map-window` (⏳) — розкладена на столі мапа вузлів: битва, вибір карт, багаття, камені, торговець, бос; фігурка гравця.
- `custom-window` вибору карти (`+window:choice-window`): 3 карти лицем / за ціною / за плем'ям (?).
- `custom-window` колоди (`+window:deck-window`) — переглянути всі карти.
- `custom-window` створення death card: вибрати ціну, стати й сигіли з трьох карт.
- `pause-menu`, `settings-window` (звук, відео, доступність (?)).
- Переходи: мапа → битва (стіл) → нагорода/мапа; поразка → створення death card → нова мапа забігу.

## Фічі поза полем
- Роглайк-забіг: `dungeon-generation`-подібна мапа вузлів, `meta-progression` через death cards і відкриття хатини (escape-room-пазли).
- `inventory-limit` 3 предмети; `save-progress` (автозбереження забігу (?)).
- Kaycee's Mod (оновлення 2022) — `mode-hardcore`-подібний режим з «викликами»-модифікаторами (?).

## Варіації й родичі
- Act 2 (піксельний, 4 школи карт), Act 3 (P03, 3×5), Kaycee's Mod.
- Родичі: Slay the Spire (мапа забігу), Hearthstone (карти з атакою/здоровʼям, але без колонок), Plants vs. Zombies (смуги), Duelyst, Marvel Snap (локації замість колонок), Wildfrost (смуги + таймери атак), Card Crawl.
- **Осі варіацій**: поле — без поля / колонки / сітка · ціна — мана / жертва / кістки / енергія · перемога — HP / ваги «перетягування» / очки локацій · наміри суперника — приховані / черга-ряд / іконки-наміри.

## Цікавинки для курсу
- Колонки + ряд черги суперника = видимі наміри без окремого UI — 🥉.
- Ваги як одна шкала «перетягування каната» замість двох HP — 🌱, зате вчить моделювати перемогу числом зі знаком.
- Ціна кровʼю: вибір жертв як частина вводу (двокроковий ввід) — 🥉.
- Сигіли як модифікатори атаки/смерті/гри (подієва система тригерів) — 🥈; Bifurcated/Trifurcated як зміна колонок удару — 📎 кожен.
- Death card: збірка нової карти з частин трьох — 📎.
- AI Leshy як сценарій черги за ходами (`spawn-schedule`) — 📎; справжній AI — 🥇.

## Мапа на каталог
- Є: `hp-damage` ↔ health карт · `piece-capture` (приблизно) ↔ знищення карти навпроти · `turn-enforcement` · `ai-opponent` ↔ Leshy · `telegraphed-intents` ↔ ряд черги · `round-currency` ↔ кістки · `inventory-items` + `inventory-limit` ↔ предмети, 3 слоти · `shop-catalog` ↔ торговець · `spawn-schedule` ↔ сценарій карт суперника · `event-points` ↔ зуби · `dungeon-generation` (як мапа вузлів) · `save-progress`.
- **Нема** → пропозиції карток:
  - `+lane-grid` — див. plants-vs-zombies.
  - `+opponent-queue-row` «Ряд черги суперника» · interface/hud · 🥉 — наступні юніти суперника видно на полі.
  - `+sacrifice-cost` «Ціна жертвою своїх юнітів» · game-logic/economy · 🥉.
  - `+scale-tug-of-war` «Шкала перетягування» · game-logic/win · 🌱 · слот {threshold: 5}.
  - `+card-sigils` «Модифікатори-здібності на юнітах» · entities/combat · 🥈 · слот {sigils: list}.
  - `+deck-draw` «Колода, добір, рука» · game-logic/economy · 🥉 · слот {side_deck}.
  - `+death-card` «Юніт з частин трьох» · entities/state · 📎.

## Пропозиції до словників
- `+trigger:card_played` — зіграно карту (Guardian, Rabbit Hole, Ant Spawner); `+trigger:attacked` — сутність стала ціллю (Bees Within, Sharp Quills, Loose Tail).
- `+cond:lane_has` — див. plants-vs-zombies (атака по карті чи по вагах).
- `+effect:sacrifice` — знищити свої сутності як плату · `+effect:advance_queue` — висунути юніт з черги · `+effect:scale_shift` — зсунути шкалу перемоги · `+effect:draw` — взяти карту · `+effect:jump_over` — Airborne бʼє «через голову» (див. PvZ).
- `+role:card` — карта-юніт зі статами й сигілами; `+role:lane` — колонка.
- `+ui:scale-meter` — шкала-ваги; `+ui:queue-row` — ряд черги суперника; `+ui:bell-button` — кінець ходу як предмет світу (≈ `end-turn-button`).
- `+window:map-window` ⏳ (мапа забігу) · `+window:deck-window` · `+window:choice-window` — вибір 1 з N нагород.
- `+feature:run-map` — карта вузлів забігу (Slay the Spire-подібна).
- `+axis:session` — `match` (битва) у складі `run` (забіг); пропоную значення `run`.

## Джерела
- ⭐ [Wikipedia: Inscryption](https://en.wikipedia.org/wiki/Inscryption) — поле 3×4 (3×5 в Act 3), черга Leshy у верхньому ряду, атака навпроти або по гравцю, ваги з зубами до 5, сигіли, кров-жертви, death cards, релізи.
- [Steam: Inscryption](https://store.steampowered.com/app/1092790/Inscryption/) — деки «by draft, surgery, and self mutilation», escape-room.
- [Sacrifices Must Be Made (itch.io)](https://dmullinsgames.itch.io/sacrifices-must-be-made) — безкоштовний прототип механіки.
- [Inscryption Wiki: Sigils](https://inscryption.fandom.com/wiki/Sigils) — повний список сигілів (не відкрилась, 402).
- YouTube: пошук «inscryption act 1 gameplay».

## Непевне
- (?) Тексти сигілів — з памʼяті (фан-вікі не відкрилась); Wikipedia підтверджує лише «flying past a blocker» і «attacking multiple columns».
- (?) Стартова рука (3 + білка), надлишкова шкода → зуби як валюта, механіка свічок у битвах з босом.
- (?) Повний перелік предметів і вузлів мапи; торгівля шкурами (Trapper/Trader).
- (?) Порядок атаки зліва направо і поведінка Waterborne/Burrower у деталях.
