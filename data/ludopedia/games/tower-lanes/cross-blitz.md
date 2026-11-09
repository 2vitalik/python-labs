---
title: Cross Blitz
slug: cross-blitz
aka: []
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2023
platforms: [PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Cross_Blitz", best: true, note: "два ряди по чотири клітини на бік, мана +1 щоходу, карти атакують самі з наступного ходу; Fables і Tusk Tales"}
  - {kind: steam, url: "https://store.steampowered.com/app/1619520/Cross_Blitz/", note: "поле 4×4, Blitz Burst, 500+ карт, 160 реліквій, 20 архетипів; скриншоти поля й HUD"}
  - {kind: official, url: "https://www.thearcadecrew.com/games/cross-blitz/", note: "сторінка видавця (з Вікіпедії)"}
  - {kind: other, url: "https://www.heypoorplayer.com/2025/12/13/cross-blitz-review-pc/", note: "огляд: блок у смузі, політ і лучники в обхід, Swiftstrike/Hothead, мана до 10, колода 30, втома, реліквії, Blitz Burst, обидва режими"}
  - {kind: other, url: "https://hardcoregamer.com/previews/cross-blitz-strikes-with-one-amazing-card-game/450668/", note: "превʼю: вісім клітин, стрілки ззаду, ближній бій спереду, кнопка BLITZ, Thorns, Plunder, смертні ефекти"}
  - {kind: other, url: "https://tryhardguides.com/cross-blitz-review/", note: "огляд: фаза бліцу — карта бʼє те, що перед нею, порожня смуга — гравця"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Cross+Blitz+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [hp-damage, melee-vs-ranged, status-effects, turn-enforcement, ai-opponent, round-currency, run-relics, shop-catalog, world-map, sequential-levels, leaderboard, +lane-grid, +deck-draw, +deck-builder, +card-collection, +card-keywords, +summoning-sickness, +ramping-energy, +flying-ignores-maze, +fatigue-pool, +crafting-recipes, +run-meta-carry, +charged-ultimate, +battle-accolades, +front-back-rows]
proposes: ["+role:card", "+role:lane", "+trigger:card_played", "+trigger:deck_empty", "+trigger:attacked", "+cond:lane_has", "+effect:summon", "+ui:blitz-button", "+ui:ultimate-meter", "+ui:accolades-panel", "+window:deck-window", "+feature:daily-hunts", "+card:charged-ultimate", "+card:front-back-rows"]
author: opus
date: 2026-11-09
---

# Cross Blitz — картковий дуель-RPG на полі 4×4: кожна сторона — 2 ряди × 4 смуги, міньйони б'ють по своїй смузі самі після кнопки BLITZ

## Суть
Однокористувацька колекційна карткова гра (Tako Boy Studios) на полі з чотирьох смуг: у кожного гравця два ряди по чотири клітини, що дивляться на суперника. Розігруєш міньйонів, закляття й пастки за ману, що росте щоходу; з наступного ходу міньйони атакують самі — по першому, хто стоїть у їхній смузі, а коли смуга порожня — по героєві суперника. Хто перший опустив HP героя до нуля — переміг. Навколо — дві оболонки: сюжетні кампанії Fables із мапою на гексах і роглайт Tusk Tales у дусі Slay the Spire.

## Поле і час
- Поле 4×4: по 2 ряди × 4 клітини на сторону; стовпці — смуги (lanes); карта ставиться в будь-яку вільну клітину своєї половини.
- Ряди не рівноцінні: стрілки — ззаду, ближній бій — спереду (Hardcore Gamer); передня карта в смузі закриває задню (?).
- Покроково: хід = розіграш карт за ману → натискання BLITZ → фаза бою (усі готові міньйони атакують) → хід суперника.
- Інформація прихована: рука суперника — сорочкою вгору; колоди тасуються (random runtime), мапа Tusk Tales — випадкова (setup).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой гравця (Redcroft, Violet, Quill, Seto, Mereena) | player | HP (30 на скриншоті), броня, мана x/y, рівень | отримує удари з порожніх смуг; має Blitz Burst |
| Герой суперника | enemy | HP, мана, рівень | те саме з іншого боку |
| Клітина поля | zone | ряд (передній/задній), смуга | місце для однієї карти-міньйона |
| Міньйон | piece | атака, HP, ключові слова | атакує по своїй смузі з наступного ходу |
| Міньйон зі Swiftstrike / Hothead | piece | — | атакує в той самий хід |
| Літун, лучник (direct) | piece | — | бʼє героя в обхід блокера |
| Закляття (spell) | supply | ціна мани | разовий ефект |
| Пастка (trap) | supply | умова | лежить до умови й спрацьовує |
| Реліквія | container | до 4: 1 епічна + 3 звичайні | пасивно міняє правила (імунітет до отрути, броня за смерть міньйона) |
| Колода | supply | рівно 30 карт | з неї тягнуть; порожня — втома |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(side)` → ТО `custom: «макс. мана +1 (до 10), мана відновлюється»`, `custom: «взяти карту з колоди»` (?).
- КОЛИ `input(play, card, cell)` → ЯКЩО `counter(mana, >=, cost)` and `free(cell)` → ТО `place(minion)`, `counter(mana, -cost)`, `set_state(minion, not_ready, 1)`.
- КОЛИ `input(play, spell)` → ЯКЩО `counter(mana, >=, cost)` → ТО `custom: «ефект закляття»`; пастка — `place(trap)`, спрацьовує КОЛИ `custom: «виконалась умова пастки»`.
- КОЛИ `input(blitz)` → ТО `custom: «почати фазу бою»`; КОЛИ `phase_start(combat)` → ЯКЩО `not state(minion, not_ready)` or `custom: «Swiftstrike / Hothead»` → ТО `custom: «міньйон атакує»`.
- Атака: КОЛИ `custom: «міньйон атакує»` → ЯКЩО `occupied(lane_ahead, enemy_minion)` → ТО `damage(first_in_lane, atk)`; інакше `damage(enemy_hero, atk)`.
- КОЛИ `custom: «атакує літун або лучник»` → ТО `damage(enemy_hero, atk)` в обхід блокера.
- КОЛИ `custom: «міньйон отримав удар»` → ЯКЩО `state(minion, thorns)` → ТО `damage(attacker, n)`.
- КОЛИ `custom: «міньйон завдав шкоди іншому міньйону»` → ЯКЩО `custom: «має Plunder»` → ТО `custom: «ефект грабунку»`.
- КОЛИ `hp_zero(minion)` → ТО `disappear`; ЯКЩО `custom: «має DEATH-ефект»` → ТО `custom: «смертний ефект, напр. викликати Haunted Crewmate»`.
- КОЛИ `custom: «удар міньйона з Poison»` → ТО `set_state(target, poison)`; КОЛИ `turn_start(side)` → ЯКЩО `state(minion, poison)` → ТО `damage(n)` (?).
- КОЛИ `custom: «спроба взяти карту з порожньої колоди»` → ТО `damage(hero, n)`, щоразу більше.
- КОЛИ `counter(burst_charge, >=, n)` (умова героя, напр. «витрать 15 мани на DEATH-міньйонів») → ТО `custom: «Blitz Burst готовий»`; КОЛИ `input(burst)` → ТО `custom: «ультимативний ефект героя»`.
- КОЛИ `hp_zero(enemy_hero)` → ТО `win`, `custom: «гроші, матеріали, зараховані Accolades»`; КОЛИ `hp_zero(hero)` → ТО `lose`.
- Перемога: HP героя суперника = 0 · Поразка: власне HP = 0 · Рахунок: Accolades (цілі бою) → Dawn Dollars; у Tusk Tales — Husks і таблиці щоденних/щотижневих полювань.

## Керування і ввід
- Миша: перетягнути карту з руки на клітину своєї половини; кнопка BLITZ запускає фазу бою й завершує хід (?).
- Кнопки DECK і HISTORY (колода, журнал ходів), шестерня налаштувань, перемикач швидкості анімацій (1.5×).
- Анімації початку ходу блокують руку (огляд).

## Вікна, меню, HUD
- `game-screen`: поле 4×4; ліворуч угорі — `turn-counter` («TURN 5» з пісковим годинником), `+ui:accolades-panel` (чотири цілі бою) і `objective-text` («DEFEAT THE ENEMY.»), кнопки DECK і HISTORY; ліворуч унизу — портрет героя з рівнем, HP, бронею, мана-пляшкою x/y, іконками реліквій і `+ui:ultimate-meter` (заряд Blitz Burst); праворуч — герой суперника з HP і маною, його рука сорочкою вгору, `+ui:blitz-button`; унизу — рука з цінами.
- Картка міньйона на полі: атака, HP, значок «ще не готовий» (пісковий годинник).
- Модал Blitz Burst: назва, прогрес заряду (0/15), умова й ефект.
- `map-window` Fables: гексова мапа з маршрутами, подіями-«візуальною новелою», боями; `shop-window` (картки за гроші), `custom-window` кузні (крафт/Meld з інгредієнтів), `+window:deck-window` (30 карт, архетипи героя).
- `mode-select`: Fables · Tusk Tales; у Tusk Tales — таверна найманців (`character-select`), мапа забігу, `leaderboard` полювань.

## Фічі поза полем
- Fables: 5 героїв × 3 акти, по 4 стилі колоди на героя (частина — за побічні квести з важкими боями й пазлами); прокачка героя підвищує HP.
- `deck-builder`: колода рівно 30 карт, ліміт копій на карту, перемикання колод між боями; 500+ карт, 20 архетипів, 5 фракцій.
- Колекція: купівля карт за гроші й Dawn Dollars, крафт (Meld) із матеріалів боїв.
- Tusk Tales: 20 найманців зі стартовими колодами, випадкові мапи, дрібнички (trinkets) модифікують окремі карти, `meta-progression` за Husks, Souls за щоденні полювання; `+feature:daily-hunts` з таблицями.
- `achievements`, `cloud-save`; мультиплеєр планували, але скасували.

## Варіації й родичі
- Родичі: [inscryption](inscryption.md) (смуги 4 + черга суперника), [plants-vs-zombies-heroes](plants-vs-zombies-heroes.md) (смуги з типами), [marvel-snap](marvel-snap.md), [queens-blood](queens-blood.md), [hearthstone-battlegrounds](hearthstone-battlegrounds.md), [elder-scrolls-legends](elder-scrolls-legends.md) (дві смуги), [gwent](gwent.md) (ряди ближній/дальній бій), [the-bazaar](the-bazaar.md).
- **Осі варіацій**: смуг 2 / 4 / 5 · рядів на бік 1 / 2 (передній закриває задній) · атака — вибір гравця / автоматична по смузі (тут) · хто бʼє героя — лише при порожній смузі / літуни й стрілки в обхід.

## Цікавинки для курсу
- Автобій по смугах: перший у стовпці отримує удар, порожня смуга — удар по герою — 🌱.
- Два ряди на сторону: передній/задній ряд і обхідні ключові слова (Flying, direct) — 📎.
- Мана, що росте на 1 щоходу до 10, і «втома» порожньої колоди — 🌱.
- Ключові слова як прапорці на картці (Swiftstrike, Thorns, Plunder, DEATH, Poison) з тригерами — 🥉 (система подій).
- Blitz Burst: ультимейт із власною умовою заряду, своєю для кожного героя — 📎.
- Гексова мапа кампанії з маршрутами й подіями поверх бойового ядра — 🥉.

## Мапа на каталог
- Є: `hp-damage` · `melee-vs-ranged` ↔ ряди · `status-effects` ↔ отрута · `turn-enforcement` · `ai-opponent` · `round-currency` ↔ мана · `run-relics` ↔ реліквії й дрібнички · `shop-catalog` · `world-map` ↔ гексова мапа Fables · `sequential-levels` ↔ акти · `leaderboard` ↔ полювання.
- **Нема** → пропозиції карток:
  - `+front-back-rows` «Два ряди на сторону: передній закриває задній, стрілки ззаду» · entities/legality · 📎.
  - `+charged-ultimate` «Ультимейт з умовою заряду» · game-logic/economy · 📎 · слот {charge_rule}.
  - `+battle-accolades` «Додаткові цілі бою з нагородою» · game-logic/score · 🌱.
  - уже вживані: `+lane-grid`, `+deck-draw`, `+deck-builder`, `+card-collection`, `+card-keywords`, `+summoning-sickness`, `+ramping-energy`, `+flying-ignores-maze` (тут — літун оминає блокер смуги), `+fatigue-pool`, `+crafting-recipes`, `+run-meta-carry`.

## Пропозиції до словників
- `+role:card` — карта в руці/колоді; `+role:lane` — смуга-стовпець поля.
- `+trigger:card_played` — карту розіграно; `+trigger:deck_empty` — спроба тягнути з порожньої колоди; `+trigger:attacked` — міньйон отримав удар (Thorns).
- `+cond:lane_has` — у смузі навпроти є міньйон.
- `+effect:summon` — викликати міньйона ефектом (DEATH: summon).
- `+ui:blitz-button` — кнопка «почати бій / завершити хід»; `+ui:ultimate-meter` — заряд ультимейта з умовою; `+ui:accolades-panel` — цілі бою.
- `+window:deck-window` — редактор колоди; `+feature:daily-hunts` — щоденні/щотижневі забіги з таблицями.
- `+card:charged-ultimate`, `+card:front-back-rows`.

## Джерела
- ⭐ [Wikipedia: Cross Blitz](https://en.wikipedia.org/wiki/Cross_Blitz) — «two rows of four spaces», будь-яка вільна клітина, мана +1 щоходу, атака з наступного ходу, крафт у кузні, Fables і Tusk Tales, дати (EA 2023, реліз 24.11.2025), скасований мультиплеєр.
- [Steam](https://store.steampowered.com/app/1619520/Cross_Blitz/) — поле 4×4, Blitz Burst, 500+ карт, 160 реліквій, 20 архетипів, 5 фракцій, 20 найманців, Husks, щоденні/щотижневі полювання; скриншоти HUD і модалу Blitz Burst.
- [Hey Poor Player: огляд](https://www.heypoorplayer.com/2025/12/13/cross-blitz-review-pc/) — блок у смузі, літуни й лучники в обхід, Swiftstrike/Hothead, мана до 10, колода 30, наростаюча шкода порожньої колоди, 4 реліквії, Blitz Burst, акти й Accolades, Tusk Tales.
- [Hardcore Gamer: превʼю](https://hardcoregamer.com/previews/cross-blitz-strikes-with-one-amazing-card-game/450668/) — вісім клітин, стрілки ззаду, кнопка BLITZ, удар по герою «if there's a clear shot», Thorns, Plunder, смертні ефекти, 1 епічна + 3 звичайні реліквії.
- [Try Hard Guides: огляд](https://tryhardguides.com/cross-blitz-review/) — фаза бліцу, «блокувати й бити в незахищені смуги».

## Непевне
- (?) Чи передній міньйон у смузі обовʼязково закриває задній свого ж боку, і по якому ряду суперника бʼє атака (перший зустрічний у стовпці — з оглядів, без деталей).
- (?) Добір карт: по одній на початку ходу — не перевірено; стартова рука.
- (?) Точні правила пасток (коли спрацьовують, чи видимі супернику), тривалість отрути.
- (?) Чи BLITZ завершує хід або ще можна грати карти після бою.
