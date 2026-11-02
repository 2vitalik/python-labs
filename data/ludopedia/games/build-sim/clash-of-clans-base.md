---
title: Clash of Clans — розстановка бази на сітці
slug: clash-of-clans-base
family: build-sim
also: [tower-lanes]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: none
  goal: score
year: 2012
platforms: [iOS, Android, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Clash_of_Clans", best: true, note: "геймплей, зірки (50 % / ратуша / 100 %), 3 хвилини атаки, клани, Builder Base"}
  - {kind: official, url: "https://supercell.com/en/games/clashofclans/", note: "офіційна сторінка Supercell"}
  - {kind: fandom, url: "https://clashofclans.fandom.com/wiki/Clash_of_Clans_Wiki", note: "фан-вікі: розміри будівель, радіуси, цілі військ (WebFetch повертав 402, не прочитано)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=clash+of+clans+base+layout+funneling+explained", note: "пошук; розбори планування й фанелінгу"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=clash+of+clans+attack+replay", note: "пошук; повтори атак"}
stage: v1
coverage: 60
mechanics: [multi-cell-size, impassable-cells, drag-drop-piece, cell-click, hover-highlight, chase-greedy, chase-bfs, hp-damage, projectile-shot, blast-wave, round-currency, shop-window, in-round-upgrades, replay, leaderboard, time-out, event-points, player-camera, field-scaling, +coverage-area, +range-blind-spot, +target-preference, +wall-path-cost, +hidden-trap, +build-zone, +deploy-zone, +destruction-stars, +layout-slots, +async-pvp, +drag-build-line, +context-tile-rules, +facing-arc]
proposes: ["+trigger:in_range", "+trigger:destroyed", "+trigger:counter", "+trigger:input", "+cond:in_range", "+cond:free", "+cond:path_exists", "+cond:count", "+effect:place", "+effect:move", "+effect:damage", "+effect:reveal", "+effect:spawn_at", "+effect:throw", "+effect:explode", "+role:tower", "+role:hazard", "+role:zone", "+role:supply", "+ui:threat-range", "+ui:progress-bar", "+ui:timer-countdown", "+ui:inventory-bar", "+window:editor-window", "+window:replay-window", "+window:log-window", "+window:map-window", "+feature:replay", "+feature:share-code", "+feature:online-multiplayer", "+axis:control", "+axis:opponent=async", "+card:target-preference"]
author: opus
date: 2026-11-02
---

# Clash of Clans (база) — сітка 44×44, де розстановка будівель і стін — це програма для AI захисту й пастка для AI атакувальних військ

## Суть
Описано **лише шар розстановки бази й атаки на неї**: гравець ставить будівлі різних розмірів (1×1 стіна … 4×4/5×5) на сітку 44×44, а інший гравець асинхронно атакує цю розстановку, висаджуючи війська з краю. Ні оборона, ні війська не керуються під час бою: башти стріляють за радіусами, війська самі обирають ціль за своїм пріоритетом (найближча будівля / лише оборона / стіни / ресурси) і шукають шлях крізь лабіринт стін. Розстановка = статична програма, атака = вибір, де і коли висадити агентів. Клас `hybrid`: `cursor` (редактор бази) + `cursor` з `indirect`-агентами (атака). Економіка, клан, герої-прогресія — поза описом.

## Поле і час
- Будівельна сітка **44×44** клітини; навколо — смуга-облямівка, куди нічого не ставлять (там висаджують війська); на полі ще перешкоди (дерева, камені), які гравець прибирає.
- Будівлі займають N×N клітин (стіна 1×1, пастки 1×1/2×2, більшість оборон 3×3, ратуша 4×4, табір армії 5×5 (?)); навколо кожної будівлі — **заборонена для висадки** смуга (червона/біла зона), тож висадка можлива лише на певній відстані від забудови.
- Війська рухаються **вільно** (субклітинні координати), але шукають шлях по сітці, де стіни — перешкоди; башти мають круглі радіуси в клітинах.
- Два часи: розстановка — статика без ліміту; атака — real-time **3 хв** (+ ~30 с розвідки до першої висадки).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стіна | static | 1×1, HP, рівень | перекриває шлях наземним; сусідні стіни зʼєднуються візуально; можна руйнувати |
| Ратуша (Town Hall) | static | 4×4, HP | знищення = зірка; рівень відкриває будівлі |
| Ресурсні будівлі (шахти, сховища) | resource | 3×3 тощо | ціль Гоблінів; лут атакувальнику |
| Гармата (Cannon) | tower | 3×3, радіус ≈9, лише наземні | один постріл у найближчу наземну ціль |
| Башта лучників | tower | 3×3, радіус ≈10, земля+повітря | одиночні постріли |
| Мортира | tower | 3×3, радіус ≈4–11 | сплеш-шкода; **сліпа зона** ближче мінімального радіуса |
| Чарівна вежа | tower | 3×3, радіус ≈7 | сплеш навколо цілі |
| ППО (Air Defense) | tower | 3×3, радіус ≈10, лише повітря | висока шкода по повітряних |
| Повітряний підмітач (Air Sweeper) | tower | 2×2, напрям, сектор | відштовхує повітряних у секторі; **орієнтацію** задає гравець |
| Прихована Тесла | tower | 2×2 | невидима, доки ціль не ввійде в радіус спрацювання |
| X-Bow / Inferno / Eagle | tower | режим (земля / земля+повітря; одна/багато цілей) | режим вибирає власник бази |
| Замок клану | spawner | 3×3, радіус спрацювання | випускає війська-захисники, коли атакувальник у радіусі |
| Бомба / Гігантська бомба | hazard | 1×1 / 2×2, прихована | вибух по області, коли наземні в радіусі |
| Пружина (Spring Trap) | hazard | 1×1, ліміт місткості | викидає наземних за поле |
| Повітряна бомба / Шукаюча міна | hazard | 1×1 | по повітряних |
| Пастка-скелети | spawner | 1×1, режим земля/повітря | випускає скелетів |
| Варвар, Лучник, Дракон | enemy | HP, DPS, радіус | ціль — **найближча будь-яка** будівля |
| Гігант, Повітряна куля, Вершник на кабані | enemy | — | ціль — **лише оборона**; кабан перестрибує стіни |
| Гоблін | enemy | ×2 шкода по ресурсах | ціль — ресурсні будівлі |
| Стінолом (Wall Breaker) | enemy | — | ціль — стіни (за ними будівля); вибух по області |
| Цілитель (Healer) | ally | — | лікує інші війська, не атакує |
| Зона висадки | zone | — | клітини поза смугою навколо будівель |

## Правила (КОЛИ → ЯКЩО → ТО)
- Розстановка: КОЛИ `input(drag, building)` → ЯКЩО всі N×N клітин у межах 44×44 і `free` → ТО `place`; інакше будівля підсвічена червоним, не ставиться.
- КОЛИ `input(tap, deploy_cell)` під час атаки → ЯКЩО `cell(x, deploy_zone)` і `has(attacker, troop)` → ТО `spawn_at(troop, x)`, `take(attacker, troop)`; інакше `message(«не можна висадити тут»)`.
- КОЛИ `spawned(troop)` або `destroyed(current_target)` → ТО `custom: «обрати найближчу будівлю серед своїх пріоритетних типів (усі / оборона / ресурси / стіни); пріоритетних нема — будь-яку»`.
- КОЛИ ціль обрано → ЯКЩО `path_exists(без стін)` → ТО `move` найкоротшим шляхом; інакше `custom: «шлях зі штрафом за стіни; бʼє першу стіну на маршруті»` (кабан — ігнорує стіни).
- КОЛИ `in_range(troop, target, r)` → ТО `damage(dps)` щотік до `hp_zero(target)` → `disappear_b`, `counter(destruction, +%)`.
- КОЛИ `in_range(tower, troop, r_max)` і `not in_range(tower, troop, r_min)` → ЯКЩО тип цілі підходить (земля/повітря) → ТО `projectile` / `damage` (сплеш — по області).
- КОЛИ `in_range(trap, troop, trigger_r)` → ЯКЩО тип підходить → ТО `reveal(trap)`, `explode(area)` / `throw(troop, off_field)` / `spawn(skeletons)`; пастка одноразова.
- КОЛИ `in_range(clan_castle, troop, trigger_r)` → ТО `spawn_at(defenders, castle)`; захисники біжать до найближчого атакувальника.
- КОЛИ `in_range(hidden_tesla, troop, reveal_r)` → ТО `reveal`, далі як башта.
- Air Sweeper: КОЛИ повітряна ціль у секторі `facing` → ТО `push(air_troop, away)` (шкоди нема).
- Зірки: `counter(destruction, ≥, 50%)` → ⭐; `destroyed(town_hall)` → ⭐; `counter(destruction, ==, 100%)` → ⭐.
- КОЛИ `timer(3 min) == 0` або всі війська мертві й не висаджені → ТО `end-screen` з % і зірками.
- Рахунок: зірки + % руйнування; лут; трофеї ± за результат.

## Керування і ввід
- Редактор бази: drag будівлі; тап — вибір (апгрейд, інфо, поворот Air Sweeper, режим X-Bow/Inferno); інструмент «вибрати ряд стін» — тягнути/повертати лінію стін цілком.
- Атака: вибрати військо в нижньому барі → тап/утримання на клітині зони висадки (утримання — висадка по одному щотік); заклинання — тап у будь-яку точку (область дії).
- Під час бою війська не керуються (крім героїв: здібність кнопкою) — `axis:control = indirect`.

## Вікна, меню, HUD
- `game-screen` (село): поле 44×44 з камерою (pan/zoom), ресурси вгорі, кнопки Attack, Shop, Clan, Settings.
- `shop-window`: категорії (оборона, ресурси, армія, пастки, декор) — звідси перетягують на поле.
- `editor-window` (режим «Edit Layout»): порожня сітка + «лоток» прибраних будівель знизу; кнопки Remove All, Save, кілька слотів розстановок (село / війна / ліга), копіювання розстановки за посиланням (?).
- Пошук суперника (`custom-window`, «Next» за ресурси) → бойовий `game-screen`: `timer-countdown`, `progress-bar` руйнування %, зірки, `inventory-bar` військ із кількістю, кнопка «End Battle».
- `end-screen` бою: зірки, %, лут, трофеї; кнопка «Return Home».
- `log-window` (Attack Log / Defense Log): список атак із кнопкою Replay → `replay-window` (прискорення, пауза (?), поширити в клан).
- `map-window` (Clan War: мапа баз суперників), `leaderboard`, чат клану.
- Переходи: село → Shop → (drag) село; село → Edit → editor → Save → село; Attack → пошук → бій → end-screen → село; Log → Replay.

## Фічі поза полем
- `replay` усіх атак/захистів (огляд власних дір у розстановці — головний цикл «програмування» бази), `share-code` / посилання на розстановку (?), `layout slots` (кілька збережених планів).
- `online-multiplayer` асинхронний: атакують «знімок» бази, власник офлайн.
- Тренувальні мапи кампанії гоблінів (`mode-puzzle`-аналог), дружні виклики в клані (атака на базу соклановця без втрат).
- Прогресія: рівні будівель і ратуші (`meta-progression`), будівельники як черга будівництва за часом.

## Варіації й родичі
- Builder Base (2017) — друге село з одночасними атаками; Boom Beach (Supercell) — острів, гарматний корабель; Clash Royale — смугова тактика.
- Родичі: tower defense навпаки (гравець проектує лабіринт, AI атакує), Dungeon Keeper (будуєш пастки для героїв), Kingdom Rush, Rimworld-«killbox».
- **Осі варіацій**: хто атакує (AI хвилі / жива людина асинхронно) · пріоритет цілі військ (найближча / тип / найслабша) · чи блокують стіни (повністю / шлях зі штрафом / перестрибуються) · видимість пасток (приховані / видимі) · розмір будівлі (1×1 / N×N).

## Цікавинки для курсу
- Розміщення N×N будівель із перевіркою меж і перетинів — 📎 (картка `multi-cell-size` є, тут без руху).
- Пріоритет цілі для різних військ («найближча з типу X, інакше будь-яка») — 🥉 — сімʼя поведінок одним параметром.
- Пошук шляху з «вагою» стін: пройти обхід чи пробити стіну — 🥇 (A*, де стіна = прохідна з ціною, а не непрохідна).
- Кільце радіуса зі сліпою зоною (мортира) і сектор (Air Sweeper) — 📎 (геометрія відстані + кут).
- Приховані пастки з радіусом спрацювання й типом цілі — 📎.
- Зона висадки = поле мінус «розмиті» будівлі (дилатація маски на 1 клітину) — 🥉.
- Replay бою з детермінованої симуляції (зберегти лише висадки + seed) — 🥈 (картка `replay`).

## Мапа на каталог
- Є: `multi-cell-size` · `impassable-cells` (стіни для наземних) · `drag-drop-piece` · `cell-click` · `hover-highlight` · `chase-greedy` (найближча ціль) · `chase-bfs` (шлях крізь лабіринт) · `hp-damage` · `projectile-shot` · `blast-wave` (сплеш/бомби) · `round-currency` · `shop-window` · `in-round-upgrades` (заклинання/герої) · `replay` · `leaderboard` · `time-out` (3 хв) · `event-points` (зірки) · `player-camera` · `field-scaling`.
- **Нема** → пропозиції карток:
  - `+range-blind-spot` «Радіус дії з мінімумом (сліпа зона)» · entities/combat · 📎 · слоти {r_min, r_max} — дитина `+coverage-area`.
  - `+target-preference` «Пріоритет цілі за типом» · entities/move · 🥉 · слот {prefer: any|defense|resource|wall} — дитина `chase-player`.
  - `+wall-path-cost` «Шлях зі штрафом за руйнування перешкод» · entities/move · 🥇 — дитина `chase-bfs`.
  - `+hidden-trap` «Прихована пастка з радіусом спрацювання» · entities/interact · 📎 · слоти {trigger_r, target_type, once}.
  - `+deploy-zone` «Зона висадки як дилатація забудови» · game-logic · 🥉 (дитина `+build-zone`).
  - `+destruction-stars` «Зірки за % руйнування + ключова ціль» · game-logic/score · 🌱.
  - `+layout-slots` «Кілька збережених розстановок» · game-logic/save · 📎.
  - `+async-pvp` «Атака на знімок чужої бази під AI» · game-logic/opponent · 🥈.
  - `+facing-arc` «Сектор дії за орієнтацією» · entities/combat · 📎 (Air Sweeper).
  - `+coverage-area`, `+build-zone`, `+drag-build-line` (ряд стін), `+context-tile-rules` (зʼєднання стін) — повторно.

## Пропозиції до словників
- `+trigger:in_range` (башта/пастка/замок), `+trigger:destroyed` (ціль зникла → нова ціль), `+trigger:counter` (% руйнування), `+trigger:input`.
- `+cond:in_range`, `+cond:free`, `+cond:path_exists`, `+cond:count`.
- `+effect:place`, `+effect:move`, `+effect:damage`, `+effect:reveal` (пастка/тесла), `+effect:spawn_at` (висадка), `+effect:throw` (пружина), `+effect:explode`.
- `+role:tower` (оборонні будівлі), `+role:hazard` (пастки), `+role:zone` (зона висадки), `+role:supply` (армія в барі поза полем).
- `+ui:threat-range` (радіус башти при виборі), `+ui:progress-bar` (%), `+ui:timer-countdown`, `+ui:inventory-bar` (війська).
- `+window:editor-window` (Edit Layout), `+window:replay-window`, `+window:log-window` (журнал атак), `+window:map-window` (мапа війни).
- `+feature:replay`, `+feature:share-code` (посилання на розстановку), `+feature:online-multiplayer`.
- `+axis:control` = `indirect` (висадив — далі AI); `+axis:opponent=async` (?) — суперник офлайн, його база керується AI.
- `+card:target-preference` — див. вище.

## Джерела
- ⭐ [Wikipedia: Clash of Clans](https://en.wikipedia.org/wiki/Clash_of_Clans) — геймплей, оборони й пастки, 3-зіркова система (50 % / ратуша / 100 %), 3 хв атаки, Builder Base.
- [Supercell: Clash of Clans](https://supercell.com/en/games/clashofclans/) — офіційна сторінка.
- [Clash of Clans Wiki (fandom)](https://clashofclans.fandom.com/wiki/Clash_of_Clans_Wiki) — довідник будівель і військ (не прочитано: 402).
- YouTube: пошуки «base layout funneling explained» і «attack replay».

## Непевне
- (?) Розміри будівель (табір армії 5×5, ратуша 4×4, Air Sweeper 2×2) і радіуси башт — з памʼяті, фан-вікі недоступна (402), WebSearch вичерпано.
- (?) Точний алгоритм «пробити стіну чи обійти» — у спільноті описують як шлях зі штрафом за стіни; офіційно не задокументовано.
- (?) Копіювання розстановки за посиланням і кількість слотів розстановок — є в сучасних версіях, деталі не перевірено.
- (?) Пауза в повторі; «смуга заборони висадки» шириною 1 клітина навколо будівель.
