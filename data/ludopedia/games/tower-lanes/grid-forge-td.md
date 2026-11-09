---
title: Grid Forge TD
slug: grid-forge-td
aka: []
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: setup
  goal: survive
year: 2025
platforms: [web, PC]
links:
  - {kind: itch, url: "https://yarrichar.itch.io/grid-forge-td", best: true, note: "грати в браузері; тетроміно-стіни, курсор-вежа з AoE, лава, дерево навичок, endless, коментарі розробника"}
  - {kind: steam, url: "https://store.steampowered.com/app/4099130/Grid_Forge_TD_Demo", note: "демо: 3 вежі, самоцвіти Lightning/Cold, хвилі з паузою 10 с, research points, перелік апгрейдів"}
  - {kind: other, url: "https://yarrichar.itch.io/grid-forge-td/devlog", note: "девлог: 10 золота на старті, бонус стопки тетроміно, перерахунок шляху, клавіші"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=grid+forge+td+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [tower-placement, tower-range, polyomino-placement, piece-rotate-flip, cursor-place, enemy-waves, spawn-schedule, hp-damage, explode-area, status-effects, reachability-check, path-preview, in-round-upgrades, game-pause, +maze-by-towers, +path-recompute, +tower-on-wall, +random-blocked-cells, +cursor-aoe-click, +gem-socket, +stack-bonus, +call-wave-early, +fast-forward, +research-unlock, +meta-progression-tree, +targeting-priority, +mode-endless]
proposes: ["+role:wall", "+trigger:path_changed", "+effect:recompute_path", "+effect:socket", "+ui:piece-hotbar", "+ui:next-wave-button", "+ui:range-circle", "+window:skill-tree"]
author: opus
date: 2026-11-09
---

# Grid Forge TD — лабіринт із тетроміно поверх випадкової лави, вежі на стінах і курсор, що сам бʼє по площі

## Суть
Інкрементальний tower defense з роглайт-прогресією. Ворожий шлях не заданий: гравець викладає тетроміно, і кожна фігура — стіна, яку вороги мусять обходити, і водночас фундамент для веж. Лава-клітини генеруються випадково на кожен забіг і ламають звичні лабіринти; курсор гравця — сам по собі мобільна вежа з шкодою по площі. Між забігами research points купують постійні апгрейди в гексагональному дереві навичок.

## Поле і час
- Квадратна сітка; шари: підлога · випадкові лава-клітини · тетроміно (стіна) · вежі й самоцвіти на клітинах тетроміно · вороги.
- Шлях ворога — найкоротший прохід навколо стін від входу до виходу (точки, ймовірно, фіксовані) (?).
- Час — realtime; хвилі йдуть безперервно з паузою 10 с між ними, наступну можна викликати раніше; є прискорення.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Тетроміно | static (`+role:wall`) | форма з 4 клітин, поворот | стіна для шляху й основа для веж; стопка тетроміно дає бонус |
| Лава-клітина | terrain | випадкова на забіг | обмежує розстановку; тетроміно можна класти поверх лави (?) |
| Basic Tower | tower | надійна й ефективна | стріляє по ворогах у дальності |
| Sniper Tower | tower | висока шкода, низька скорострільність | — |
| Cannon Tower | tower | шкода по площі | — |
| Самоцвіт Lightning | pickup | — | у клітині: шкода ланцюгом на сусідніх ворогів |
| Самоцвіт Cold | pickup | — | у клітині: сповільнення ворогів |
| Курсор-вежа | player | AoE | клік будь-де по сітці — шкода по площі |
| Ворог | enemy | HP | іде найкоротшим шляхом; при зміні шляху ще кілька клітин іде старим |
| Золото | resource | 10 на старті | на тетроміно й вежі (?) |
| Research points | resource | за забіг | постійні апгрейди |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tetromino, cells)` → ЯКЩО `fits(tetromino, cells)` and `custom: «шлях від входу до виходу лишається»` → ТО `place(tetromino, cells)`, `custom: «ворожий шлях перераховується»`.
- КОЛИ `input(rotate)` → ТО `rotate(tetromino, 90)`; КОЛИ `input(key_1..n)` → ТО `custom: «вибрати наступну фігуру з запасу»`.
- КОЛИ `custom: «шлях змінився»` → ТО `custom: «вороги проходять ще кілька клітин і перемаршрутизуються»`.
- КОЛИ `input(place, tower, cell)` → ЯКЩО `occupied(cell, tetromino)` and `has(gold, cost)` → ТО `currency(-cost)`, `place(tower, cell)`.
- КОЛИ `custom: «тетроміно покладено на тетроміно»` → ТО `custom: «бонус стопки для веж на ньому»`.
- КОЛИ `in_range(tower, enemy, range)` → ТО `damage(n)` (Cannon — `explode(circle, n)`).
- КОЛИ `custom: «влучання з Lightning»` → ТО `custom: «шкода перескакує на сусідніх ворогів»`; з Cold → `speed(enemy, -n)`.
- КОЛИ `input(click, cell)` → ТО `explode(circle, n)` у точці кліку (курсор-вежа).
- КОЛИ `timer(10 s)` after `wave_cleared` → ТО `wave_start`; КОЛИ `input(next_wave)` → ЯКЩО `custom: «попередня хвиля доспавнилась»` → ТО `wave_start`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`, `currency(+n)` (?).
- КОЛИ `reach(enemy, exit)` → ТО `custom: «шкода базі / втрата життя»` (?).
- КОЛИ `level_end` → ТО `counter(research_points, +n)`.
- КОЛИ `input(buy_node, skill)` → ЯКЩО `has(research_points, cost)` → ТО `unlock(skill)`: шкода веж, швидша генерація тетроміно, більше стартового золота, елементальні ефекти, ширше поле.
- Перемога — нема (інкрементальна гра, endless) · Поразка — забіг закінчується (?) · Рахунок — номер хвилі.

## Керування і ввід
- Миша: клік — поставити фігуру/вежу або вдарити курсором; поворот тетроміно — клавіша (?); цифри — швидкий вибір наступної фігури.
- F — наступна хвиля; утримувати Space або клік по кнопці — прискорення.
- Пріоритет цілей можна задати одній вежі, усім або групі веж.

## Вікна, меню, HUD
- `main-menu` → забіг; режим endless; рівень престижу/складності (у демо — лише перший).
- `game-screen`: сітка з лавою, `+ui:piece-hotbar` (тетроміно на вибір), вибір веж, `coins`, `wave-counter`, `+ui:next-wave-button`, `fast-forward`, `+ui:range-circle`, підсвітка дозволених/заборонених клітин (`legal-move-highlight`), `path-preview` (?).
- `+window:skill-tree` — гексагональні вузли апгрейдів за research points.
- `end-screen` — підсумок забігу, зароблені очки (?).

## Фічі поза полем
- `meta-progression` — дерево навичок між забігами.
- `mode-endless`; рекорди «скоро».
- Браузер (HTML5, Godot) і Steam-демо.

## Варіації й родичі
- У сімʼї: [desktop-tower-defense](desktop-tower-defense.md) і [fieldrunners](fieldrunners.md) (лабіринт з веж), [emberward](emberward.md) (стіни-поліоміно формують шлях), [rogue-tower](rogue-tower.md) (роглайт-TD), [gemcraft](gemcraft.md) (самоцвіти у вежах). Натхнення — Nodebuster (курсор-атака, інкрементальність).
- **Осі варіацій**: шлях — заданий / з веж / зі стін-поліоміно · перешкоди — нема / випадкова лава · вежа — окремо / лише на стіні · гравець — пасивний / курсор бʼє сам.

## Цікавинки для курсу
- Тетроміно як стіна з перевіркою, що шлях лишається (BFS після кожної фігури) — 🥉.
- Перерахунок шляху з «інерцією»: ворог іде ще кілька клітин старим шляхом — 📎.
- Випадкові заблоковані клітини на старті забігу — 🌱.
- Курсор-AoE: клік по сітці б'є по площі — 🌱.
- Самоцвіти-модифікатори в клітині (ланцюг, сповільнення) — 📎.
- Дерево постійних апгрейдів між забігами — 📎.

## Мапа на каталог
- Є: `tower-placement` · `tower-range` · `polyomino-placement` ↔ тетроміно · `piece-rotate-flip` · `cursor-place` · `enemy-waves` + `spawn-schedule` ↔ хвилі з паузою 10 с · `hp-damage` · `explode-area` ↔ Cannon і курсор · `status-effects` ↔ Cold · `reachability-check` ↔ шлях існує · `path-preview` · `in-round-upgrades` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+random-blocked-cells` «Випадкові непридатні клітини на забіг» · levels/generation · 🌱.
  - `+cursor-aoe-click` «Клік гравця як атака по площі» · interface/input · 🌱.
  - `+gem-socket` «Модифікатор у клітині змінює вежу» · entities/state · 📎.
  - `+stack-bonus` «Бонус за накладання фігур одна на одну» · entities/legality · 📎.
  - `+meta-progression-tree` «Дерево постійних апгрейдів» · game-logic/progression · 📎.
  - `+targeting-priority` «Пріоритет цілей вежі / групи веж» · entities/combat · 📎.

## Пропозиції до словників
- `+role:wall` (стіна, яку поставив гравець і на якій будують).
- `+trigger:path_changed` · `+effect:recompute_path` · `+effect:socket` (вставити модифікатор у клітину).
- `+ui:piece-hotbar` · `+ui:next-wave-button` · `+ui:range-circle`.
- `+window:skill-tree`.

## Джерела
- ⭐ [itch.io: Grid Forge TD](https://yarrichar.itch.io/grid-forge-td) — грати в браузері; тетроміно-стіни й основа для веж, курсор-вежа з AoE, лава, дерево з гексагональних вузлів, endless, демо на першому рівні престижу.
- [Steam: Grid Forge TD Demo](https://store.steampowered.com/app/4099130/Grid_Forge_TD_Demo) — «ви створюєте шлях», випадкова лава, Basic/Sniper/Cannon, Lightning/Cold, пауза 10 с між хвилями, research points і перелік апгрейдів; реліз демо 21.10.2025, Yarrichar Studios.
- [itch.io: девлог](https://yarrichar.itch.io/grid-forge-td/devlog) — 10 золота на старті, бонус стопки, перемаршрутизація за кілька клітин, клавіші хвилі/прискорення, пріоритет цілей.

## Непевне
- (?) Чи можна блокувати шлях повністю (ймовірно, ні — як у maze-TD); точки входу й виходу.
- (?) Як саме лава взаємодіє з фігурами: розробник каже «тетроміно можна класти поверх лави», Steam — «обходити лаву» — суперечність.
- (?) Що відбувається, коли ворог доходить до виходу (життя / HP бази), і за що дають золото.
- (?) Як генеруються тетроміно (черга/таймер — апгрейд «швидша генерація» натякає на таймер).
