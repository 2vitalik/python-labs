---
title: Element TD 2
slug: element-td-2
aka: [ETD2, Element TD 2 - Tower Defense, Element TD]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: coop
  info: full
  random: none
  goal: survive
year: 2020
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1018830", best: true, note: "6 стихій → 59 веж, кампанія 28 місій, co-op 8, FFA і 1v1, 55 хвиль + нескінченний бос"}
  - {kind: steam, url: "https://store.steampowered.com/app/2177070/Element_TD_2_Mazing_Expansion/", note: "Mazing: блокери на шляху, вежі на блокерах, безкоштовна перебудова лабіринту"}
  - {kind: official, url: "https://eletd.com/", note: "сайт студії: 26 мап, 10 модифікаторів"}
  - {kind: other, url: "https://steamcommunity.com/sharedfiles/filedetails/?id=2360427994", note: "гайд новачка: піки кожні 5 хвиль, боси стихій, відсотки 2 %/15 с, essence, periodic"}
  - {kind: other, url: "https://forums.eletd.com/topic/2879-mazing-basics", note: "форум: мейзинг у WC3/SC2-версіях, вейпоінти WP1/WP2, «три проходи»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=element+td+2+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, player-death, tower-placement, tower-range, round-currency, in-round-upgrades, shop-buyback, shop-catalog, projectile-shot, shoot-cooldown, explode-area, status-effects, hp-damage, speed-per-type, chase-bfs, reachability-check, level-select, level-unlock, difficulty-levels, leaderboard, online-multiplayer, keyboard-controls, status-panel, +maze-by-towers, +path-recompute, +interest-economy, +element-combo-tower, +element-pick-boss, +damage-type-wheel, +tower-recipe-table, +waypoint-route, +blocker-tiles, +endless-boss, +game-modifiers]
proposes: ["+trigger:path_changed", "+effect:recompute_path", "+effect:sell", "+effect:upgrade", "+effect:interest", "+role:tower", "+role:blocker", "+role:waypoint", "+ui:range-circle", "+ui:element-wheel", "+ui:recipe-table", "+ui:wave-strip", "+feature:game-modifiers"]
author: opus
date: 2026-11-09
---

# Element TD 2 — стихії набираються «піками» кожні 5 хвиль, вежі — рецепти з 1–3 стихій; лабіринт — окремим розширенням

## Суть
Нащадок WC3-мапи Element TD: кріпи йдуть шляхом через вейпоінти, гравець будує базові вежі (Arrow, Cannon) і апгрейдить їх у стихійні. Стихію треба «вибрати» — кожні 5 хвиль гравець бере пік: стихію (зʼявляється бос цієї стихії, вбив — стихія твоя), відсотки або (пізно) essence. Вежа = рецепт: одна стихія — single, дві — dual, три — triple, усі шість + essence — periodic. Відмінність від Desktop TD і Fieldrunners: глибина не в лабіринті, а в **дереві рецептів і порядку піків**; власне мейзинг — окремий режим із блокерами на шляху (Mazing Expansion, 2022).

## Поле і час
- Мапа-сітка: шлях кріпів (з поворотами й вейпоінтами) і будівельні клітини обабіч; вигідні місця — де шлях проходить двічі («double pass»).
- Mazing: на шляху ставлять **блокери** — кріпи обходять їх, вежі будуються поверх блокерів; блокери можна переставляти безкоштовно, кожна мапа має свої межі й розмір.
- Real-time: 55 хвиль, далі нескінченні боси (Doom Lords), що врешті вбивають; відсотки нараховуються кожні 15 с.
- Інформація повна: смуга хвиль угорі — наведення показує здібності й слабкості хвилі.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вхід | spawner | — | хвиля виходить |
| Вейпоінти | zone | WP1, WP2… (?) | кріп проходить їх по черзі |
| Вихід | static | — | кріп дійшов → −життя |
| Будівельна клітина | terrain | — | місце для вежі |
| Блокер (Mazing) | object | безкоштовний | ставиться на шлях, кріпи обходять; на ньому будують вежу |
| Arrow, Cannon | tower | базові | завжди доступні; апгрейдяться в стихійну вежу |
| Single-вежа | tower | 1 стихія | рівні 1–3, з essence — рівень 4 |
| Dual-вежа | tower | 2 стихії | напр. Light + Fire = Lightning; далі гілки (Nova, Runic, Windstorm, Money) |
| Triple-вежа | tower | 3 стихії | найсильніші за рецептом |
| Periodic | tower | усі 6 + essence | композитна шкода без сильних і слабких сторін |
| Стихії | custom | Light, Dark, Water, Fire, Nature, Earth | коло: кожна сильна проти сусіда праворуч і слабка проти лівого |
| Кріп | enemy | HP, стихія, здібності | іде шляхом; має слабкість/стійкість за стихією |
| Бос стихії | boss | — | викликається піком; убитий — відкриває стихію |
| Композитний бос | boss | — | викликається піком «діамант»; убитий — essence |
| Doom Lord | boss | нескінченні | після хвилі 55, ростуть до неминучої поразки |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tower, cell)` → ЯКЩО `free(cell)` and `has(player, gold)` → ТО `place(player, tower)`, `currency(-cost)`; інакше `block`.
- (Mazing) КОЛИ `input(place, blocker, cell)` → ЯКЩО `free(cell)` and `path_exists(spawn, exit)` (?) → ТО `place(player, blocker)`, `custom: «effect recompute_path»`; ціна 0.
- (Mazing) КОЛИ `input(place, tower, blocker)` → ЯКЩО `has(player, gold)` → ТО `place(player, tower)` поверх блокера.
- КОЛИ `tick` → кріп `move(a, next_on_path)` до наступного вейпоінта, потім до виходу.
- КОЛИ `counter(wave, %, 5)` and `custom: «хвиля ≤ 50»` → ТО `choose(options)`: стихія / Interest / діамант (essence) — 11 піків за гру.
- КОЛИ `input(pick, element)` → ЯКЩО `not first_time` → ТО `spawn_at(element_boss, entrance)`; перший пік — стихія одразу (?).
- КОЛИ `hp_zero(element_boss)` → ТО `unlock(element)`.
- КОЛИ `input(pick, interest)` → ТО `custom: «ставка відсотків +0.6 %»` замість стихії.
- КОЛИ `hp_zero(composite_boss)` → ТО `counter(essence, +1)`.
- КОЛИ `timer(15s)` → ТО `custom: «effect interest: +2 % від золота»`.
- КОЛИ `input(upgrade, tower, element)` → ЯКЩО `custom: «рецепт вежі виконано: потрібні стихії відкриті»` and `has(player, gold)` → ТО `transform(tower, element_tower)`, `currency(-cost)`.
- КОЛИ `input(upgrade, single, lvl4)` → ЯКЩО `counter(essence, >=, 1)` → ТО `transform(single, single_lvl4)`; essence також будує Periodic.
- КОЛИ `in_range(tower, creep, r)` → ТО `spawn(projectile)` з періодом `shoot-cooldown`.
- КОЛИ `contact(projectile, creep)` → ТО `damage(n × k)`, де `k` — за колом стихій: сильна проти стихії кріпа — більше, слабка — менше; Periodic — без модифікатора.
- КОЛИ `contact(projectile, creep)` → ЯКЩО `custom: «вежа має ефект»` → ТО `explode(area, n)` / `set_state(creep, slow|poison, dur)` / `currency(+n)` (Money-вежа) (?).
- КОЛИ `hp_zero(creep)` → ТО `disappear(creep)`, `currency(+bounty)`.
- КОЛИ `reach(creep, exit)` → ТО `lives(-n)`, `disappear(creep)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `lose`.
- КОЛИ `wave_cleared` → ЯКЩО `counter(wave, ==, 55)` → ТО `custom: «почалися нескінченні Doom Lords; рахунок — скільки протримався»`.
- КОЛИ `input(sell, tower)` → ТО `custom: «effect sell»`, `disappear(tower)`.
- Перемога: кампанія — пройти місію (зірки за складність (?)) · Поразка: життя = 0 · Рахунок: очки за хвилі й ендгейм, таблиці лідерів.

## Керування і ввід
- Миша: вибір вежі з панелі → клітина; клік по вежі — апгрейд у стихійну гілку / продаж.
- `Ctrl` при виборі/посадці — одразу найвищий рівень, на який вистачає золота.
- Таблиця рецептів (Tower Table) — будувати вежу будь-якого рівня прямо з неї, якщо є золото.
- Наведення на хвилю в смузі вгорі — здібності й слабкості.
- Мультиплеєр: кожен гравець має власну смугу/мапу (?), спільна чи змагальна мета залежно від режиму.

## Вікна, меню, HUD
- `main-menu` → `mode-select` (кампанія, survival, co-op, FFA, 1v1 ranked, Mazing) → `lobby-window` (мультиплеєр) або `level-select` (28 місій кампанії, 14 Mazing-місій).
- `game-screen`: мапа, `+ui:wave-strip` (хвилі з підказками), `+ui:element-wheel` (коло стихій, відкриті піки), `coins`, `lives`, `wave-counter`, лічильник essence, `+ui:range-circle`.
- `+ui:recipe-table` — таблиця рецептів веж (окреме вікно/панель).
- `upgrade-window` (⏳) — вибір піку кожні 5 хвиль: стихія / Interest / діамант.
- `end-screen` + `leaderboard` (глобальні таблиці).

## Фічі поза полем
- `mode-coop` (до 8 гравців проти 55 хвиль), `mode-versus` (FFA на 8, 1v1 ranked; «turtle or rush»), `online-multiplayer` з глобальними серверами, LAN.
- Кампанія: 28 місій з унікальними мапами, ворогами й босами; Mazing — 14 місій, 10 мап + 6 co-op мап.
- `+feature:game-modifiers` — 10 модифікаторів, що змінюють правила гри.
- `leaderboard-online`, 26 мап різних біомів.

## Варіації й родичі
- Родовід: WC3-мапа Element TD (2006) → `flash-element-td` (3 стихії, фіксована дорога) → SC2-версія → Element TD 2. Сусіди: `gemcraft` (комбінування самоцвітів), `legion-td` (той самий WC3-корінь, але юніти й обмін хвилями), `desktop-tower-defense` (мейзинг).
- **Осі варіацій**: доступ до стихій — купівля / пік з босом / випадково · рецепт — лінійний апгрейд / комбінація 2–3 стихій / усі · шлях — фіксований з вейпоінтами / лабіринт з блокерів · кінець — фінальна хвиля / нескінченні боси.

## Цікавинки для курсу
- Дерево рецептів веж (1 → 2 → 3 стихії, periodic за всі 6) як граф передумов — 🥉.
- Коло стихій (кожна сильна проти сусіда) — таблиця множників шкоди — 🌱.
- Пік-система: кожні 5 хвиль вибір «сила / економіка», за силу — бос-іспит — 📎.
- Блокери, які можна переставляти безкоштовно, з перерахунком шляху й вейпоінтами — 🥈 (BFS через послідовність точок).
- Нескінченні боси після фіналу як шкала рахунку — 🌱.

## Мапа на каталог
- Є: `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` + `player-death` · `tower-placement` + `tower-range` · `round-currency` · `in-round-upgrades` · `shop-buyback` · `shop-catalog` · `projectile-shot` + `shoot-cooldown` · `explode-area` · `status-effects` · `hp-damage` · `speed-per-type` · `chase-bfs` + `reachability-check` (Mazing) · `level-select` + `level-unlock` · `difficulty-levels` · `leaderboard` · `online-multiplayer` · `keyboard-controls` (Ctrl-апгрейд).
- **Нема** → пропозиції карток:
  - `+element-pick-boss` «Пік стихії з босом-іспитом» · game-logic/economy · 📎 · слоти {every, max_picks}.
  - `+damage-type-wheel` «Коло типів шкоди» · entities/combat · 🌱 · слот {matrix}.
  - `+tower-recipe-table` «Таблиця рецептів веж» · game-logic/economy · 🥉.
  - `+waypoint-route` «Маршрут через вейпоінти» · entities/move · 📎.
  - `+blocker-tiles` «Безкоштовні блокери-лабіринт» · entities/legality · 🥈.
  - `+endless-boss` «Нескінченні боси після фіналу» · game-logic/waves · 🌱.
  - `+game-modifiers` «Модифікатори правил партії» · game-logic/difficulty · 📎.
  - `+maze-by-towers`, `+path-recompute`, `+interest-economy`, `+element-combo-tower` — див. родину й flash-element-td.

## Пропозиції до словників
- `+trigger:path_changed`, `+effect:recompute_path`, `+effect:sell`, `+effect:upgrade`, `+effect:interest`, `+role:tower`, `+ui:range-circle` — підтвердження з родини.
- `+role:blocker` — дешевий обʼєкт-стіна, на якому стоїть вежа.
- `+role:waypoint` — точка, яку ворог мусить пройти по черзі.
- `+ui:element-wheel`, `+ui:recipe-table`, `+ui:wave-strip`.
- `+feature:game-modifiers` — набір модифікаторів правил партії (`mode-coop`, `mode-versus` уже ⏳).

## Джерела
- ⭐ [Steam: Element TD 2](https://store.steampowered.com/app/1018830) — 6 стихій, 59 веж, кампанія 28 місій, co-op 8 / FFA / 1v1 ranked, 55 хвиль + нескінченний бос, Early Access 28.02.2020, реліз 02.04.2021.
- [Steam: Mazing Expansion](https://store.steampowered.com/app/2177070/Element_TD_2_Mazing_Expansion/) — блокери на шляху, вежі поверх, безкоштовна перебудова, 14 місій, 10 + 6 co-op мап (02.12.2022).
- [eletd.com](https://eletd.com/) — 26 мап, 10 модифікаторів.
- [Steam-гайд новачка](https://steamcommunity.com/sharedfiles/filedetails/?id=2360427994) — коло стихій, 11 піків, боси стихій, Interest-пік +0.6 %, відсотки 2 %/15 с, essence, periodic, Ctrl-апгрейд, Tower Table, Doom Lords (гайд знято зі Steam, але текст відкрився).
- [Форум eletd: Mazing Basics](https://forums.eletd.com/topic/2879-mazing-basics) — мейзинг у SC2-версії: вейпоінти, «Spawn → WP2 → Maze → WP1 → … → Exit».
- YouTube: пошук «element td 2 gameplay».

## Непевне
- (?) Чи в Mazing заборонено повністю перекрити шлях; скільки блокерів дозволено.
- (?) Перший пік: стихія одразу без боса — так виходить з «кожен пік після першого викликає боса».
- (?) Назви шести стихій узято з опису Element TD (Light, Darkness, Water, Fire, Nature, Earth); гайд для ETD2 явно називає лише Light, Fire, Earth, Dark.
- (?) Як саме працює змагальний режим (чи посилають кріпів суперникам) і «turtle or rush».
- (?) Ефекти окремих веж (сповільнення, отрута, Money-вежа дає золото) — з памʼяті жанру, не з джерела.
- Рік у шапці — старт Early Access 2020; повний реліз — 2021.
