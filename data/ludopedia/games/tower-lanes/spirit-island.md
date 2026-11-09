---
title: Spirit Island
slug: spirit-island
aka: []
family: tower-lanes
also: [board-digital]
klass: cursor
axes:
  field: graph
  time: turn
  opponent: coop
  info: partial
  random: both
  goal: state
year: 2017
platforms: [board, digital, mobile]
links:
  - {kind: other, url: "https://rulespal.com/spirit-island/rulebook", best: true, note: "правила: 8 земель на дошку (по 2 кожного типу), прибережні, HP/шкода загарбників і даханів, Defend, Range, Push/Gather, присутність і треки, елементи, страх і рівні терору"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Spirit_Island_(board_game)", note: "R. Eric Reuss, Greater Than Games, 2017; 1–4 (до 6); Explore/Build/Ravage; блайт; умови поразки; доповнення; цифрова версія 2020"}
  - {kind: other, url: "https://www.ultraboardgames.com/spirit-island/game-rules.php", note: "фази ходу, Ravage/Build/Explore, каскад блайту, колода загарбників 3+4+5, страх 4 на гравця, умови перемоги й поразки"}
  - {kind: other, url: "https://rules.dized.com/game/_7rPptSyRn6_unBi4-2eVg/JX3j7ssvTxKQDLmk_5323w/fear-and-terror", note: "Dized: страх і рівні терору"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spirit+Island+how+to+play", note: "пошук; як грати"}
stage: v1
coverage: 55
mechanics: [hp-damage, spawn-schedule, telegraphed-intents, difficulty-levels, character-select, help-window, end-screen, tutorial-window, +graph-board, +modular-board, +coop-shared-win, +coop-shared-loss, +blight-spread, +variable-player-powers, +power-cards, +retaliation, +deck-as-timer, +invader-card-pipeline, +fear-lowers-win-condition, +blight-cascade, +elemental-thresholds, +fast-slow-phases, +presence-range-targeting, +presence-track-unlock, +draw-4-keep-1, +push-gather-pieces]
proposes: ["+role:card", "+role:building", "+trigger:round_end", "+effect:spread", "+effect:draw_card", "+effect:discard", "+effect:gather", "+cond:land_type", "+cond:element_threshold", "+ui:fear-track", "+ui:invader-slots", "+card:invader-card-pipeline", "+card:fear-lowers-win-condition"]
author: opus
date: 2026-11-09
---

# Spirit Island — духи острова проти колоністів: карта загарбників щоходу каже, в якому типі землі вони досліджують, будують і грабують, а ви відповідаєте силами з руки

## Суть
Кооперативна настільна гра R. Eric Reuss (Greater Than Games, 2017; 1–4 гравці, з Jagged Earth — до 6). Кожен гравець — дух зі своєю присутністю на острові, енергією, картами сил і вродженими силами за порогами елементів. Загарбники (дослідники, селища, міста) діють за **конвеєром карт**: одна й та сама карта типу землі спершу веде Explore, наступного ходу — Build, ще за хід — Ravage; грабіж лишає блайт. **Межова гра для сімʼї**: поле — граф земель, не сітка; спільне з tower defense — передбачувані «хвилі» з відомим напрямком і захист територій.

## Поле і час
- Острів з модульних дошок, по одній на гравця; на кожній 8 пронумерованих земель — по 2 Mountain, Jungle, Sands, Wetland. Землі, що торкаються Океану, — прибережні; решта — внутрішні. Суміжність — дотик, навіть кутом і через стик дошок (`field: graph`).
- Ресурси поза полем: дошка загарбників (слоти Explore/Build/Ravage, колода, страх, карта блайту), панелі духів (треки присутності енергії й розіграшів карт, зростання, вроджені сили).
- Хід — 5 фаз: Духи (одночасно) → Швидкі сили → Загарбники → Повільні сили → Час минає.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Земля ×8 на дошку | zone | тип: Mountain/Jungle/Sands/Wetland; прибережна / внутрішня | вершина графа; ціль сил і дій загарбників |
| Океан | zone | — | джерело дослідників: Explore у суміжну землю |
| Дослідник (Explorer) | enemy | HP 1, шкода 1 | зʼявляється за Explore |
| Селище (Town) | enemy (`+role:building`) | HP 2, шкода 2; знищення → 1 страх | будується за Build |
| Місто (City) | enemy (`+role:building`) | HP 3, шкода 3; знищення → 2 страхи | будується, якщо селищ більше за міста |
| Дахан | neutral | HP 2; 1 шкоди → «поранений» до кінця ходу | після Ravage кожен уцілілий завдає 2 шкоди загарбникам |
| Блайт | hazard | запас на карті блайту | +1 у землю при ≥ 2 шкоди за Ravage; знищує 1 присутність кожного духа там |
| Присутність | piece | 13 дисків на духа | знята з треку відкриває більше енергії / розіграшів; 2+ у землі — святе місце |
| Карта сили | piece (`+role:card`) | вартість, Fast/Slow, дальність, ціль, елементи | грається з руки за енергію; ефект — у свою фазу |
| Вроджена сила | static | пороги елементів | діє, якщо цього ходу набрано потрібні елементи |
| Карта загарбників | spawner | стадія I/II/III, тип землі | рухається слотами Explore → Build → Ravage → скид |
| Карта страху | piece | ефект для рівня терору 1/2/3 | заробляється, коли пул страху спорожнів |
| Карта блайту | static | Healthy / Blighted Island | запас блайту; перевертається, коли спорожніє |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «phase_start(spirit)»` → ТО `choose(одна опція Growth)`, `currency(+energy_track)`, `custom: «зіграти до card_plays карт, сплатити енергію, отримати елементи»`.
- КОЛИ `input(growth, add_presence)` → ЯКЩО `in_range(presence, land, 2)` → ТО `place(spirit, presence)` — диск із треку на землю; відкрите число треку діє з цього ходу.
- КОЛИ `input(power, land)` → ЯКЩО `in_range(presence, land, range)` → ТО ефект сили — у фазі Fast або Slow; Range 0 — земля з власною присутністю.
- КОЛИ `custom: «вроджена сила»` → ЯКЩО `custom: «element_threshold: елементів цього ходу ≥ порогу»` → ТО ефект рівня; елементи перевіряються, не витрачаються.
- КОЛИ `custom: «здобуття сили»` → ТО `custom: «draw 4 з колоди Minor або Major, лишити 1»`; ЯКЩО `custom: «Major»` → ТО `custom: «забути 1 карту сили»`.
- КОЛИ `custom: «phase_start(invader): Ravage»` → ЯКЩО `custom: «land_type: тип землі = тип карти в слоті Ravage»` and `occupied(land, invader)` → ТО `damage(land_and_dahan, 1×explorer + 2×town + 3×city)` мінус Defend.
- КОЛИ `custom: «Ravage завдав землі ≥ 2 шкоди»` → ТО `spawn(blight, land)`, `custom: «знищити по 1 присутності кожного духа там»`.
- КОЛИ `custom: «після Ravage»` → ЯКЩО `occupied(land, dahan)` → ТО `damage(invaders, 2×dahan)` — навіть якщо загарбники не шкодили.
- КОЛИ `spawned(blight)` → ЯКЩО `custom: «у землі вже був блайт»` → ТО `custom: «spread: +1 блайт у суміжну землю (каскад триває)»`.
- КОЛИ `custom: «Build»` → ЯКЩО `custom: «тип землі = карта Build»` and `occupied(land, invader)` → ТО `spawn(city, land)`, якщо селищ більше за міста, інакше `spawn(town, land)`.
- КОЛИ `custom: «Explore»` → ТО `custom: «відкрити верхню карту загарбників»`; ЯКЩО `custom: «тип землі збігся»` and (`occupied(land, town|city)` or `custom: «суміжна з селищем, містом або Океаном»`) → ТО `spawn(explorer, land)` — по 1 на землю.
- КОЛИ `custom: «кінець дій загарбників»` → ТО `custom: «карти зсуваються: Ravage → скид, Build → Ravage, Explore → Build»`.
- КОЛИ `destroyed(town)` → ТО `counter(fear, +1)`; КОЛИ `destroyed(city)` → ТО `counter(fear, +2)`; Remove/Replace страху не дає.
- КОЛИ `counter(fear_pool, ==, 0)` → ТО `custom: «заробити верхню карту страху, маркери — назад у пул»`; карта діє в наступній фазі загарбників.
- КОЛИ `custom: «відкрито роздільник рівня терору»` → ТО `custom: «умова перемоги: рівень 1 — нема загарбників; 2 — нема селищ і міст; 3 — нема міст»`.
- КОЛИ `custom: «поточну умову перемоги виконано»` → ТО `win` — одразу.
- КОЛИ `counter(blight_pool, ==, 0)` → ЯКЩО `custom: «карта ще Healthy»` → ТО `custom: «перевернути на Blighted Island, додати блайт»`; інакше `lose`.
- КОЛИ `custom: «дух утратив усю присутність на полі»` → ТО `lose`; КОЛИ `custom: «колода загарбників скінчилась»` → ТО `lose`.
- КОЛИ `custom: «Time Passes»` → ТО `custom: «скинути зіграні карти, обнулити елементи, зняти шкоду»`.
- Перемога: умова поточного рівня терору · Поразка: блайт вичерпано на Blighted Island, дух без присутності або колода загарбників скінчилась · Рахунок: — (кооператив).

## Керування і ввід
- Фаза духів одночасна: кожен обирає Growth, грає карти закрито/відкрито, платить енергію; хтось може задати таймер фази.
- Цілі сил — земля в межах дальності від присутності; Push (з землі в суміжні) і Gather (із суміжних у ціль) рухають шматки графом.
- Цифрова версія (2020): вибір земель і цілей мишею/тачем, безкоштовна мобільна «free to learn» з туторіалом.

## Вікна, меню, HUD
- `game-screen`: граф земель з фігурками, `+ui:invader-slots` (Explore/Build/Ravage), `+ui:fear-track` (пул і заробленні карти), запас блайту, панелі духів з треками.
- `character-select` — вибір духів; `difficulty-select` — супротивник (Adversary) і рівень, сценарій.
- `tutorial-window` — навчальна гра (Teaching Game, «free to learn» у цифровій).
- `end-screen` — перемога/поразка з причиною; `help-window`.

## Фічі поза полем
- `difficulty-presets`: супротивники з рівнями й ескалацією на стадії II; сценарії.
- Доповнення: Branch & Claw, Jagged Earth (до 6 гравців), Feather and Flame, Nature Incarnate; спрощений спін-оф Horizons of Spirit Island (2022).

## Варіації й родичі
- Родичі в корпусі: [ghost-stories](ghost-stories.md) (кооператив проти прибуття ворогів у селище 3×3), [pandemic](../board-digital/pandemic.md) (граф міст, спалахи-каскади), [they-are-billions](they-are-billions.md) і [plants-vs-zombies](plants-vs-zombies.md) — сіткові родичі «захисту території від хвиль».
- **Осі варіацій**: напрям хвиль — смуга / випадкова клітина / за типом землі з картою · попередження — нема / наступна хвиля видна / конвеєр на 2 ходи вперед · умова перемоги — знищити все / послаблюється страхом.

## Цікавинки для курсу
- Конвеєр карт загарбників: одна карта проходить 3 слоти й 3 дії — 📎.
- Блайт-каскад на графі з вибором сусіда гравцем — 📎.
- Рівні терору: умова перемоги слабшає з накопиченим страхом — 🌱.
- Вроджені сили з порогами елементів (мультимножина ≥ поріг) — 🌱.
- Треки присутності: знятий диск відкриває більший дохід — 📎.

## Мапа на каталог
- Є: `hp-damage` · `spawn-schedule` ↔ Explore за картою · `telegraphed-intents` ↔ слоти Build/Ravage показують наступні дії · `difficulty-levels` ↔ супротивники · `character-select` ↔ духи · `tutorial-window`, `end-screen`, `help-window`.
- **Нема** → пропозиції карток:
  - `+graph-board`, `+modular-board`, `+coop-shared-win`, `+coop-shared-loss`, `+blight-spread`, `+variable-player-powers`, `+power-cards`, `+retaliation`, `+deck-as-timer` — уже в корпусі.
  - `+invader-card-pipeline` «Карта ворогів проходить слоти Explore → Build → Ravage» · game-logic/waves · 📎.
  - `+fear-lowers-win-condition` «Накопичений страх послаблює умову перемоги» · game-logic/win · 🌱.
  - `+blight-cascade` «Шкода в ураженій зоні перекидається на сусіда» · entities/state · 📎.
  - `+elemental-thresholds`, `+fast-slow-phases`, `+presence-range-targeting`, `+presence-track-unlock`, `+draw-4-keep-1`, `+push-gather-pieces` — по 🌱–📎.

## Пропозиції до словників
- `+role:card`, `+role:building`, `+trigger:round_end`, `+effect:spread`, `+effect:draw_card`, `+effect:discard` — повтори з корпусу.
- `+effect:gather` — затягнути шматки з суміжних земель у ціль.
- `+cond:land_type` — тип землі збігається з картою загарбників; `+cond:element_threshold` — набрано елементів ≥ порогу.
- `+ui:fear-track`, `+ui:invader-slots`.
- `+card:invader-card-pipeline`, `+card:fear-lowers-win-condition`.

## Джерела
- ⭐ [RulesPal: Spirit Island rulebook](https://rulespal.com/spirit-island/rulebook) — типи земель, прибережні, HP і шкода, Defend, Range, Push/Gather, треки присутності, елементи, здобуття сил, страх і рівні терору.
- [Wikipedia: Spirit Island](https://en.wikipedia.org/wiki/Spirit_Island_(board_game)) — автор, рік, гравці, конвеєр Explore/Build/Ravage, умови поразки, доповнення, цифрова версія.
- [UltraBoardGames: правила](https://www.ultraboardgames.com/spirit-island/game-rules.php) — фази, Ravage/Build/Explore, каскад, колода загарбників 3+4+5, страх.
- [Dized: Fear and Terror](https://rules.dized.com/game/_7rPptSyRn6_unBi4-2eVg/JX3j7ssvTxKQDLmk_5323w/fear-and-terror) — рівні терору й умови перемоги (з результатів пошуку).
- YouTube: пошук «Spirit Island how to play».

## Непевне
- (?) Карта «Coastal Lands» на стадії II і її правила — у RulesPal не описано.
- (?) Скільки блайту на гравця кладеться на карту блайту — залежить від карти, чисел не бачив.
- (?) Платформи цифрової версії (ПК, консолі) — Wikipedia каже лише «multiple platforms».
