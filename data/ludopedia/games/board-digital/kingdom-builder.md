---
title: Kingdom Builder
slug: kingdom-builder
aka: [Будівничий королівства, KB]
family: board-digital
also: []
klass: cursor
axes:
  field: hex
  time: turn
  opponent: hotseat
  info: partial
  random: both
  goal: score
year: 2011
platforms: [board, web, mobile, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Kingdom_Builder", best: true, note: "огляд: модульна гекс-мапа, хід, локації, замки, кінець, розширення, Spiel des Jahres 2012"}
  - {kind: other, url: "https://www.ultraboardgames.com/kingdom-builder/game-rules.php", note: "правила: 40 поселень, правило сусідства, локації, кінець"}
  - {kind: other, url: "https://www.ultraboardgames.com/kingdom-builder/extra-location-tiles.php", note: "8 тайлів локацій базової гри з діями"}
  - {kind: other, url: "https://rulespal.com/kingdom-builder/rulebook", note: "10 карт Kingdom Builder з точним підрахунком; 25 карт терену; 2 тайли на локацію"}
  - {kind: play, url: "https://en.boardgamearena.com/gamepanel?game=kingdombuilder", note: "грати в браузері (BGA), 2–5 гравців"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Kingdom+Builder+how+to+play", note: "пошук; правила"}
stage: v1
coverage: 75
mechanics: [cell-click, hover-highlight, legal-move-highlight, impassable-cells, connectivity-check, event-points, hot-seat, turn-enforcement, ai-opponent, online-multiplayer, rule-variants, game-settings, game-screen, end-screen, help-window, match-setup, +hex-grid-render, +connected-placement, +modular-board, +random-scoring-goals, +public-objectives, +area-majority, +location-powers, +connected-group-scoring, +line-scoring, +last-round-trigger]
proposes: ["+trigger:card_drawn", "+cond:adjacent_to_own", "+cond:terrain", "+effect:discard", "+effect:take_tile", "+effect:lose_tile", "+role:location", "+role:hand", "+ui:goal-cards", "+ui:supply-counter", "+card:location-powers", "+card:area-majority"]
author: opus
date: 2026-11-09
---

# Kingdom Builder — 3 поселення на гекси терену з карти, обовʼязково поруч зі своїми; очки задають 3 випадкові карти цілей

## Суть
Гравці будують королівства з 40 дерев'яних поселень на спільній гекс-мапі. Хід майже без вибору «що»: відкрита карта терену каже, на якому типі гексів поставити 3 поселення, а правило сусідства змушує ставити поруч зі своїми, якщо можливо. Глибина — у «як»: 3 випадкові карти Kingdom Builder (з 10) змінюють, що приносить золото цієї партії, а тайли локацій дають додаткові дії (ще одне поселення або переміщення). Spiel des Jahres 2012.

## Поле і час
- Мапа = 4 з 8 двобічних секторів по 100 гексів, складені прямокутником 2×2 у випадковому порядку → модульна підготовка.
- Терени для будівництва: трава, каньйон, пустеля, квітковий луг, ліс; не можна: гори, вода (лише через Гавань), замок, локація.
- Сектор — окрема зона для карт Lords і Farmers; горизонтальний рядок гексів — лінія для Discoverers і Knights.
- Покроково за годинниковою стрілкою; хід = зіграти свою карту терену → 3 поселення (обовʼязково) → дії тайлів (до чи після) → добрати карту.
- Кінець: хтось поставив останнє поселення → коло дограють до гравця праворуч від першого.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Поселення | piece | власник; 40 на гравця | одне на гекс; ставиться за картою й правилом сусідства |
| Гекс терену | terrain | 5 будівних типів | приймає 1 поселення |
| Гори | static | — | не будуються; ціль карти Miners |
| Вода | terrain | — | будується лише дією Гавані; ціль Fishermen |
| Замок | static | — | не будується; +3 золота за кожен замок поруч зі своїм поселенням |
| Гекс локації | static | 2 тайли на ньому | збудувався поруч → взяти 1 тайл (раз з кожної локації) |
| Тайл локації | pickup | дія, раз за хід | використовується з наступного ходу; губиться, якщо поруч не лишилось своїх поселень |
| Карта терену | resource | 25 карт: 5 типів × 5 | одна на руці; визначає терен ходу |
| Карта Kingdom Builder | zone | 3 з 10 на партію | правило підрахунку золота |
| Сектор | zone | 100 гексів | одиниця для Lords і Farmers |
| Золото | resource | трек | очки, рахуються лише наприкінці |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_start(player)` → ТО `custom: «зіграти карту терену»`.
- Обовʼязково: КОЛИ `input(place(settlement, hex))` → ЯКЩО `same(hex, card, terrain)` і `free(hex)` і (`adjacent_count(hex, own_settlement, >=, 1)` або `custom: «на цьому терені нема вільного гексу поруч зі своїми»`) → ТО `place(settlement, hex)`; повторити 3 рази.
- Перший хід: сусідства ще нема — будь-який гекс терену карти.
- КОЛИ `custom: «на терені карти нема жодного вільного гексу»` → ТО `custom: «карту з гри, добирати, доки не знайдеться придатна»`.
- КОЛИ `adjacent(settlement, location)` → ЯКЩО `custom: «на локації лишився тайл»` і `custom: «з цієї локації ще не брав»` → ТО `give(player, location_tile)` (`+effect:take_tile`).
- КОЛИ `input(use(location_tile))` → ЯКЩО `first_time` (за хід) і `custom: «тайл отримано не цього ходу»` → ТО дія тайла.
- Oracle: `place(settlement, hex)` на терені зіграної карти, поруч якщо можна · Farm — на траві · Oasis — у пустелі · Tower — на краю мапи (будь-який будівний терен) · Tavern — на кінці прямої з ≥3 своїх поселень.
- Barn: `move(settlement, hex)` на терен зіграної карти, поруч якщо можна · Harbor — `move` на воду (єдиний спосіб) · Paddock — `move` на 2 гекси по прямій, перестрибуючи будь-що, сусідство не потрібне.
- КОЛИ `custom: «після переміщення поруч з локацією нема своїх поселень»` → ТО `custom: «тайл скидається»` (`+effect:lose_tile`).
- КОЛИ `turn_end(player)` → ТО `custom: «скинути карту, добрати нову»` (`+trigger:card_drawn` для наступних правил).
- КОЛИ `counter(supply, ==, 0)` → ТО `custom: «доіграти коло»` → `game_over`.
- Рахунок (наприкінці, по черзі 3 карти, потім замки): Fishermen — 1 за поселення біля води · Merchants — 4 за кожну локацію/замок, звʼязані ланцюгом поселень з іншими · Discoverers — 1 за рядок з ≥1 поселенням · Hermits — 1 за кожну окрему групу (і одиночне) · Citizens — 1 за 2 поселення найбільшої групи · Miners — 1 за поселення біля гір · Workers — 1 за поселення біля локації чи замку · Knights — 2 за поселення в рядку, де їх найбільше · Lords — у кожному секторі 12 найбільшому, 6 другому · Farmers — 3 за поселення в секторі, де їх найменше (треба бути в кожному).
- Замки: `score(+3)` за кожен замок з ≥1 своїм поселенням поруч.
- Нічия — спільна перемога.
- Перемога: найбільше золота · Поразка: — .

## Керування і ввід
- (цифрова версія) Карта терену видна в куті; легальні гекси підсвічено — клік ставить поселення; лічильник «лишилось 3/2/1».
- Тайли локацій — кнопки; клік → підсвітка легальних гексів дії (для Barn/Harbor/Paddock — спершу вибір свого поселення).
- Порядок «тайли до / після обовʼязкової дії» — вільний; кнопка «завершити хід».

## Вікна, меню, HUD
(цифрова версія — BGA і застосунок)
- `main-menu` → `match-setup`: 2–4 (з Nomads 5) гравці, вибір секторів (випадково / вручну), карти Kingdom Builder (випадково / вручну), розширення.
- `game-screen`: гекс-мапа 2×2 сектори; `goal-cards` — 3 карти цілей партії; своя карта терену; тайли локацій зі станом (використано цього ходу / нове); `supply-counter` — поселень лишилось; `score-preview` (поточне золото за картами); `turn-indicator`; `opponent-boards` (їхні тайли, лічильники).
- `tooltip` над тайлом / картою цілі — повний текст правила.
- `end-screen`: розклад золота за кожною картою і замками.
- `help-window`: 8 локацій і 10 карт.
- Переходи: main-menu → match-setup → game-screen → end-screen.

## Фічі поза полем
- `custom-rules`: вибір секторів і карт цілей, розширення (Nomads, Crossroads, Marshlands, Harvest, Capitol, Caves, Island) — нові сектори, локації, карти.
- `online-multiplayer` (BGA: реальний час і асинхронно), `hotseat`, `ai-opponent-levels` (?) у застосунку.
- `rules-page`, `tooltip`-довідка.

## Варіації й родичі
- Розширення: Nomads (2012), Crossroads (2013), Marshlands (2016), Harvest (2017); «Queenie» — Capitol (2011), Caves (2012), Island (2014); Big Box (2014), 2-ге видання (2017).
- Родичі: Carcassonne (`carcassonne.md`), Cascadia (`cascadia-calico.md`, гекси й цілі), Five Tribes (`five-tribes.md`), Dominion (той самий автор — змінні карти правил кожної партії).
- **Осі варіацій**: вибір місця (вільний / терен з карти / терен + сусідство) · очки (фіксовані / випадкові 3 з 10) · спецдії (нема / тайли локацій, що можна втратити) · мапа (фіксована / 4 з 8 секторів).

## Цікавинки для курсу
- Правило «поруч зі своїми, якщо можливо» — множина легальних гексів з фолбеком — 📎.
- Гекс-мапа з 4 секторів (склеювання, координати, сусіди на гексах) — 🥉.
- 10 функцій підрахунку як плагіни, 3 випадкові на партію — 🥉 (групи — BFS/union-find, рядки, більшість у секторі).
- Merchants: які локації/замки звʼязані ланцюгом своїх поселень — 🥉 (компоненти графа).
- Tavern: кінець прямої з ≥3 своїх на гекс-сітці (3 осі) — 📎.
- Paddock: стрибок на 2 гекси по прямій через будь-що — 🌱.
- Тайл, що губиться, коли поруч не лишилось своїх — 🌱 (перерахунок після кожного move).
- AI під конкретні 3 карти цілей — 🥇.

## Мапа на каталог
- Є: `cell-click` · `hover-highlight`, `legal-move-highlight` · `impassable-cells` ↔ гори/замки/вода · `connectivity-check` ↔ групи поселень (Hermits, Citizens, Merchants) · `event-points` · `hot-seat`, `turn-enforcement`, `ai-opponent`, `online-multiplayer` · `rule-variants`, `game-settings` · `game-screen`, `end-screen`, `help-window`, `match-setup`.
- **Нема** → пропозиції карток:
  - `+hex-grid-render` · `+connected-placement` · `+public-objectives` · `+connected-group-scoring` — як в інших файлах сімʼї.
  - `+modular-board` «Мапа з випадкових секторів» · levels/generation · 📎 · слоти {sectors: 4 of 8}.
  - `+random-scoring-goals` «Випадкові 3 з N правил підрахунку» · game-logic/score · 🥉.
  - `+area-majority` «Більшість у зоні: 1-ше і 2-ге місце» · game-logic/score · 📎 · слоти {1st: 12, 2nd: 6}.
  - `+location-powers` «Тайли спецдій, що губляться без сусідства» · entities/interact · 📎.
  - `+line-scoring` «Очки за рядки поля» · game-logic/score · 🌱.
  - `+last-round-trigger` (як у Bärenpark).

## Пропозиції до словників
- `+trigger:card_drawn` — гравець добрав карту (визначає наступний хід).
- `+cond:adjacent_to_own` — гекс поруч з власною сутністю (ширше за `adjacent_count`: з фолбеком «якщо можливо» — головне правило гри).
- `+cond:terrain(hex, t)` — тип терену клітини збігається з картою.
- `+effect:discard` — скинути карту · `+effect:take_tile` — взяти тайл у запас · `+effect:lose_tile` — втратити тайл, коли умова володіння зникла.
- `+role:location` — клітина-джерело спецдій; `+role:hand` — рука карт.
- `+ui:goal-cards` — панель карт цілей партії; `+ui:supply-counter` — скільки фішок лишилось.
- `+card:location-powers` · `+card:area-majority` — див. «Мапа на каталог».

## Джерела
- ⭐ [Wikipedia: Kingdom Builder](https://en.wikipedia.org/wiki/Kingdom_Builder) — 8 секторів по 100 гексів, 5+4 терени, 3 карти цілей, хід, локації, замки, кінець, розширення, нагороди.
- [UltraBoardGames: правила](https://www.ultraboardgames.com/kingdom-builder/game-rules.php) і [тайли локацій](https://www.ultraboardgames.com/kingdom-builder/extra-location-tiles.php) — 40 поселень, правило сусідства з фолбеками, 8 локацій, кінець.
- [RulesPal: Kingdom Builder rulebook](https://rulespal.com/kingdom-builder/rulebook) — 10 карт з точним підрахунком, 25 карт терену, 2 тайли на локацію, тайл — з наступного ходу.
- [BGA: Kingdom Builder](https://en.boardgamearena.com/gamepanel?game=kingdombuilder) — 2–5 гравців, опис, гра в браузері.
- YouTube: пошук «Kingdom Builder how to play».

## Непевне
- (?) Офіційний застосунок Queen Games (iOS/Android/Steam) і чи є там AI — з памʼяті, не відкривав.
- (?) Розмір сектора 10×10 гексів — Wikipedia каже «100 гексів», форма — з памʼяті.
- (?) Для Hermits RulesPal каже «за кожне окреме поселення і кожну окрему групу» — тобто одиночне поселення теж група; так і записано.
- (?) Деталі розширень (нові локації, карти) не досліджено.
