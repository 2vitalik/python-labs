---
title: Beglitched
slug: beglitched
aka: []
family: falling-match
also: [hidden-deduction]
klass: cursor
axes:
  field: square
  time: turn
  opponent: ai
  info: hidden
  random: both
  goal: state
year: 2016
platforms: [PC, Mac, Linux, iOS]
links:
  - {kind: other, url: "https://www.148apps.com/reviews/beglitched-review/", best: true, note: "огляд: плитки компас/гроші/компʼютер/батарея/бомба, енергія з батарей, пошук схованого ворога, бомба на його клітину, мапа-ОС з моніторами"}
  - {kind: other, url: "https://www.pocketgamer.com/beglitched/review/", note: "огляд: компас = напрям, екран = відстань, ліміт ходів, ворог атакує, бомба згори на ворога, вузли мапи попереджають про сусідні секції"}
  - {kind: steam, url: "https://store.steampowered.com/app/461220/Beglitched/", note: "опис, теги Match 3 / Hacking, Hexecutable"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Beglitched", note: "інфобокс, IGF 2016 Best Student Game"}
  - {kind: other, url: "https://lofi-gaming.org.uk/diary/2024/05/beglitched-steam-deck-completed", note: "щоденник проходження: ліміт ходів, певні символи дають ходи, теки-світи зі зміною правил"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=beglitched+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [line-match-clear, gravity-fall, chain-reaction, cell-click, fog-of-war, hp-damage, move-limit, round-currency, shop-window, map-window, world-map, enemy-patrol, sequential-levels, tutorial-window, game-screen, +hidden-target-hunt, +clue-tiles, +energy-from-match, +bomb-on-target, +fail-reset-chain]
proposes: ["+effect:clue(kind, target)", "+effect:reshuffle", "+feature:fail-reset-chain"]
author: opus
date: 2026-11-09
---

# Beglitched — match-3 як полювання на схованого хакера: батареї дають енергію, компас і монітор — підказки, бомба — постріл

## Суть
Бій — дошка match-3, під якою десь схований ворог-хакер. Збіги батарей дають енергію; її витрачаєш, торкаючись плиток-підказок: компас показує напрям до ворога, монітор — відстань у клітинах. Звузивши місце, як у сапері, гравець переводить бомбу на клітину ворога й підриває. Ходів обмаль: не встиг — ворог атакує. Клас `cursor`; поза боєм — мапа мережі-ОС, де вузли теж попереджають, що за ними.

## Поле і час
- Квадратна дошка плиток; ворог займає невидиму клітину під плиткою.
- Покроково: хід = свап/збіг (?) або активація плитки; ліміт ходів на бій (PocketGamer, lofi).
- Після збігу — осідання й досипання (?).
- Поза боєм — граф моніторів/вузлів мережі; секції відкриваються по одній.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Батарея | tile | — | збіг → +енергія |
| Компас | tile | ціна в енергії | торкнутись → напрям до ворога |
| Компʼютер / екран | tile | ціна в енергії | торкнутись → відстань до ворога в клітинах |
| Гроші | tile | — | збіг → валюта (?) |
| Бомба | tile | ціна в енергії | перевести на клітину ворога й активувати → урон |
| Схований ворог (хакер) | enemy | HP (буває >1), поведінка | невидимий; атакує, коли скінчились ходи |
| Рухливий ворог | enemy | — | переміщується по дошці |
| Ворог-руйнівник | enemy | — | прибирає певні плитки |
| Невразливий / «не можна знищувати» ворог | enemy | — | бомба не допомагає або шкодить (148apps, lofi) |
| Плитка під захистом | tile | — | ціль рівня — зберегти її (148apps) |
| Монітор (вузол мапи) | zone | подія | вхід → подія: гроші, яйце, бій |
| Яйце | hazard | — | перемішує мережу (148apps) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(swap(a, b))` → ЯКЩО `pattern(match(type, 3))` → ТО `clear(matched)`, `counter(moves, −1)` (?).
- КОЛИ `pattern(match(battery, 3))` → ТО `counter(energy, +n)`.
- КОЛИ `pattern(match(money, 3))` → ТО `currency(+n)` (?).
- КОЛИ `pattern(match(type, 3))` → ЯКЩО `custom: «тип дає ходи»` → ТО `counter(moves, +n)` (lofi: «matching certain symbols gives you more moves»).
- КОЛИ `input(tap(compass))` → ЯКЩО `counter(energy, ≥, cost)` → ТО `counter(energy, −cost)`, `custom: «clue — стрілка в бік ворога»`.
- КОЛИ `input(tap(computer))` → ЯКЩО `counter(energy, ≥, cost)` → ТО `counter(energy, −cost)`, `custom: «clue — відстань до ворога в клітинах»`.
- КОЛИ `input(tap(bomb))` → ЯКЩО `counter(energy, ≥, cost)` → ТО `explode(bomb_cell)`; ЯКЩО `occupied(bomb_cell, enemy)` → ТО `damage(enemy, 1)`.
- КОЛИ `hp_zero(enemy)` → ТО `reveal(enemy)`, `win`.
- КОЛИ `counter(moves, =, 0)` → ЯКЩО `count(enemy, >, 0)` → ТО `damage(player, n)` (?) / `lose`.
- КОЛИ `turn_end(player)` → ЯКЩО `state(enemy, mobile)` → ТО `move(enemy, random)`.
- КОЛИ `turn_end(player)` → ЯКЩО `state(enemy, eraser)` → ТО `disappear(tiles_of_type)`.
- КОЛИ `destroyed(protected_tile)` → ТО `lose`.
- КОЛИ `enter(player, node)` → ТО `custom: «подія вузла»`: `currency(+n)` / `custom: «яйце — reshuffle мережі»` / `window(battle)`.
- КОЛИ `enter(player, node)` → ТО `custom: «вузол показує, що в сусідніх секціях»` (PocketGamer: «each node warns what's in the section it connects to»).
- КОЛИ `custom: «кілька хибних кроків у мережі»` → ТО `custom: «повернення на початок мережі»` (148apps).
- КОЛИ `all_gone(enemy)` (у мережі) → ТО `unlock(next_folder)`.
- Перемога (бій): ворог знищений · Поразка: скінчились ходи / знищена захищена плитка / помилки в мережі · Рахунку нема, прогрес — теки-світи.

## Керування і ввід
- Миша / тач: збіг плиток (свап, ?), тап по плитці-інструменту — активувати за енергію.
- Переміщення бомби на потрібну клітину — збігами/свапами навколо неї (PocketGamer: «maneuver bombs into position») (?).
- Мапа: клік по сусідньому монітору — перейти.

## Вікна, меню, HUD
- `map-window` — мапа в стилі ОС з моніторами, теками й вузлами.
- `game-screen` (бій): дошка, `energy-bar`, `move-counter`, підказки компаса й екрана на полі (`hint-marker`), HP ворога (?).
- `shop-window` — купівля предметів (PocketGamer «buying items»).
- `dialogue-window` — персонажі пояснюють механіку (148apps: «character dialogue prompts»).
- `end-screen` — результат бою (?).

## Фічі поза полем
- Прогресія: теки на компʼютері відкриваються послідовно; кожна тека — світ зі своєю зміною правил (lofi) — `world-map`.
- Скарби й валюта, крамниця предметів (power-ups, деталей нема).
- `onboarding-hints` — навчання діалогами.
- `custom: «fail-reset-chain»` — кілька помилок відкидають на початок мережі пазлів.

## Варіації й родичі
- Родичі: Minesweeper і сімʼя `hidden-deduction` (підказки про сховане), Battleship (пошук і постріл), [puzzle-quest](puzzle-quest.md) і [10000000](10000000.md) (збіги як ресурс для дій), [dungeon-raid](dungeon-raid.md).
- **Осі варіацій**: що дає збіг (урон / ресурс для інструментів) · що сховане (міни / ворог / вихід) · тип підказки (кількість сусідів / напрям / відстань) · ворог (стоїть / рухається / шкодить плиткам).

## Цікавинки для курсу
- Схована ціль + підказки «напрям» і «відстань» — дедукція перетином множин клітин — 📎.
- Збіги як джерело енергії, енергія як ціна інструментів — дві валюти дії — 🌱.
- Рухливий схований ворог: множина кандидатів оновлюється щоходу — 🥉.
- Бомба, яку треба довести до клітини збігами навколо — 🥉.
- Мапа-мережа, де вузол попереджає про сусідні секції (сапер на графі) — 📎.

## Мапа на каталог
- Є: `line-match-clear` · `gravity-fall` · `chain-reaction` · `cell-click` · `fog-of-war` (ворог невидимий, найближче) · `hp-damage` (ворог з кількома HP) · `move-limit` · `round-currency` · `shop-window` · `map-window`/`world-map` · `enemy-patrol` (рухливий ворог, найближче) · `sequential-levels` · `tutorial-window`.
- **Нема** → пропозиції карток:
  - `+hidden-target-hunt` «Знайти схованого ворога на полі» · game-logic/win · 📎.
  - `+clue-tiles` «Плитка дає підказку: напрям / відстань» · entities/interact · 📎.
  - `+energy-from-match` «Збіг дає енергію для інструментів» · game-logic/economy · 🌱.
  - `+bomb-on-target` «Підірвати на клітині цілі» · entities/combat · 🌱.
  - `+fail-reset-chain` «Помилки відкидають на початок серії» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:clue(kind, target)` — показати підказку про сховану ціль: напрям, відстань (Beglitched; узагальнює число сапера).
- `+effect:reshuffle` — перемішати поле/мережу (яйце Beglitched; є і в Puzzle Quest).
- `+feature:fail-reset-chain` — після N помилок прогрес серії рівнів скидається.

## Джерела
- ⭐ [148Apps: огляд](https://www.148apps.com/reviews/beglitched-review/) — перелік плиток, енергія, бомба, захищені плитки, невразливі вороги, мапа-ОС, яйце, скидання мережі.
- [PocketGamer: огляд](https://www.pocketgamer.com/beglitched/review/) — компас = напрям, екран = відстань, ліміт ходів, атака ворога, рухливі вороги з кількома HP, вузли попереджають.
- [Lofi Gaming: щоденник](https://lofi-gaming.org.uk/diary/2024/05/beglitched-steam-deck-completed) — ходи за символи, теки-світи зі зміною правил.
- [Steam](https://store.steampowered.com/app/461220/Beglitched/) — опис і теги.
- [Wikipedia](https://en.wikipedia.org/wiki/Beglitched) — інфобокс, нагорода IGF.

## Непевне
- (?) Тип ходу на дошці — свап сусідів чи інше; чи є осідання й досипання.
- (?) Що дає збіг грошей; ціни інструментів у енергії; розмір дошки.
- (?) Що саме стається, коли скінчились ходи: урон гравцю чи поразка бою.
- (?) Механіка мапи: чи вузли показують число ворогів поруч (як сапер) чи лише тип загрози.
- (?) Список предметів крамниці й пізніх плиток, що «заважають дошці».
