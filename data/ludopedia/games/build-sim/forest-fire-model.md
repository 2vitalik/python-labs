---
title: Forest-fire model (модель лісової пожежі Дроссель — Швабля)
slug: forest-fire-model
aka: [Drossel–Schwabl forest-fire model, DS-FFM, forest fire cellular automaton, «лісова пожежа»]
family: build-sim
also: []
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: runtime
  goal: none
year: 1992
platforms: [web, PC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Forest-fire_model", best: true, note: "3 стани, 4 правила, p і f, розділення масштабів часу, кластери, SOC і його межі"}
  - {kind: play, url: "http://aryan.app/randomstuff/forestfire.html", note: "HTML5-демо: Pgrowth, Plightning; дерева зелені, порожнеча чорна, вогонь червоний; сусідство Мура"}
  - {kind: play, url: "https://ccl.northwestern.edu/netlogo/models/Fire", note: "NetLogo Fire: варіант без росту — густина лісу й поріг перколяції ≈ 59 %"}
  - {kind: other, url: "https://www.math.ucdavis.edu/~gravner/papers/fgg.pdf", note: "Fisch–Gravner–Griffeath 1991: «forest fire»-рівноваги випадкових збудливих автоматів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=forest+fire+cellular+automaton", note: "пошук; симуляції"}
stage: v1
coverage: 80
mechanics: [game-loop, game-pause, state-as-data, game-settings, settings-elements, field-size-picker, rule-variants, connectivity-check, logic-render-split, gui-render, unit-tests, +fire-spread, +cellular-automaton-rule, +multi-state-cell, +stochastic-cell-rule, +step-run-speed, +percolation-threshold, +cluster-stats]
proposes: ["+card:stochastic-cell-rule", "+card:percolation-threshold", "+card:cluster-stats", "+ui:cluster-histogram", "+axis:neighbourhood"]
author: opus
date: 2026-11-09
---

# Forest-fire model — дерева ростуть з імовірністю p, блискавка б'є з імовірністю f, вогонь іде по сусідах і лишає згарище

## Суть
Тристановий клітинний автомат (порожньо / дерево / вогонь) з **випадковими** переходами: порожні клітини заростають, дерева зрідка запалюються від блискавки, вогонь за один тік перекидається на сусідні дерева, а палаюча клітина вигорає. Модель (Henley 1989; Drossel і Schwabl 1992) створювали не як реалістичну пожежу, а як приклад **самоорганізованої критичності**: ліс сам набирає густину, за якої пожежі бувають будь-якого розміру. Гравець задає p і f (у демо — поля вводу) і дивиться на поле; цілі нема.

## Поле і час
- Сітка L^d (зазвичай 2D, квадрат); сусідство — найчастіше фон Неймана (4 клітини); в HTML5-демо aryan.app — Мура (8).
- Тік: усі клітини оновлюються **одночасно** з повного старого стану; випадковість — на кожну клітину щотіку.
- Межа поля: у джерелах не уточнено (обмежене поле або тор) (?).
- Масштаби часу: потрібно f ≪ p ≪ 1/T_smax (T_smax — час горіння найбільшого кластера): перша нерівність дає лісу вирости у великі масиви, друга — щоб нові дерева не встигали вирости поруч із фронтом пожежі.
- Керівний параметр — p/f: скільки дерев у середньому садиться між двома ударами блискавки (на ілюстрації Вікіпедії p/f = 100).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Порожня клітина | terrain | стан empty | з імовірністю p на тік стає деревом |
| Дерево | tile | стан tree | загоряється, якщо є палаючий сусід; інакше — з імовірністю f (блискавка) |
| Вогонь | hazard | стан fire, 1 тік | наступного тіку стає порожньою клітиною |
| Блискавка | spawner | f | не окрема сутність, а випадкова подія на дереві |
| Кластер дерев | zone | розмір | емерджентний: звʼязна множина дерев; блискавка спалює його повністю |
| Фронт пожежі | object | швидкість 1 клітина/тік | емерджентний: кільце вогню, що розходиться кластером |
| Жарини (NetLogo Fire) | terrain | темнішають | вогонь → жарини; лише візуальний слід, далі не горять |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ЯКЩО `state(x, fire)` → ТО `set_cell(x, empty)`.
- КОЛИ `tick` → ЯКЩО `state(x, tree)` and `adjacent_count(x, fire, ≥, 1)` → ТО `set_cell(x, fire)`.
- КОЛИ `tick` → ЯКЩО `state(x, tree)` and `adjacent_count(x, fire, =, 0)` and `prob(f)` → ТО `set_cell(x, fire)` — удар блискавки.
- КОЛИ `tick` → ЯКЩО `state(x, empty)` and `prob(p)` → ТО `set_cell(x, tree)` — ріст.
- Усі чотири правила — з одного старого стану, застосовуються разом (подвійний буфер).
- КОЛИ `input(param)` → ТО `custom: «нове p або f діє з наступного тіку»` (поля Pgrowth / Plightning у демо).
- Спостереження: КОЛИ `all_gone(fire)` → ТО `custom: «записати розмір щойно згорілого кластера»` — за f ≪ p кластер горить до кінця, перш ніж поруч щось виросте.
- Варіант без росту й блискавок (NetLogo Fire, перколяція, горіння за 4 сусідами): КОЛИ `level_start` → ТО `custom: «кожна клітина — дерево з імовірністю density»`, `set_cell(left_column_trees, fire)`.
- NetLogo Fire: КОЛИ `tick` → ЯКЩО `state(x, fire)` → ТО `transform(fire, ember)` — жарини поступово темнішають.
- NetLogo Fire: КОЛИ `all_gone(fire)` → ТО `custom: «показати частку згорілих дерев»`.
- Наслідок варіанта: різкий перехід біля густини ≈ 59 % — при 55 % вогонь майже ніколи не доходить до правого краю, при 70 % майже завжди.
- Перемоги, поразки й рахунку нема.

## Керування і ввід
- aryan.app: два поля вводу Pgrowth і Plightning у блоці Controls; поле на canvas.
- NetLogo Fire: SETUP (дерева зелені, вогонь червоний зліва), GO (запуск), повзунок DENSITY — діє після наступного SETUP.
- Типова цифрова версія: Run/Pause, Step, швидкість, розмір поля; іноді клік — підпалити дерево (?).

## Вікна, меню, HUD
- `game-screen` (aryan.app): поле (зелене дерево / чорна порожнеча / червоний вогонь) + блок Controls з двома полями вводу ймовірностей.
- `game-screen` (NetLogo): поле, кнопки SETUP / GO, повзунок DENSITY; результат — `progress-bar` «відсоток згорілого».
- HUD (цифрова версія): кількість дерев / вогню (густина), `cluster-histogram` розмірів пожеж.
- Окремих вікон у демо нема.

## Фічі поза полем
- `custom-difficulty` ~ p, f, розмір поля; `speed-control`, `pause`, `step-mode`.
- Вимірювання: розподіл розмірів кластерів (за ідеєю — фрактальний, але, за Вікіпедією, масштабування «не просте»; Pruessner і Jensen показали, що на дуже великих масштабах модель не критична).
- Нема рахунку, рівнів, збережень.

## Варіації й родичі
- **Осі варіацій:** сусідство (4 / 8) · ріст (імовірність p / нема — перколяція) · запалення (блискавка f / підпал з краю) · згарище (одразу порожньо / жарини / кілька тіків горіння) · вимірювання (густина, розмір пожежі, чи дійшов вогонь до краю).
- Henley (1989) — ранній варіант; Bak, Chen, Tang (1990) — ще один попередник (у переліку джерел Вікіпедії; правила не перевіряв).
- Звʼязок із теорією перколяції (варіант NetLogo) і з випадковими збудливими автоматами: Fisch–Gravner–Griffeath описують «forest fire»-рівноваги випадкових моделей Ґрінберґа — Гастінґса; родичі — [cyclic-cellular-automaton](cyclic-cellular-automaton.md), [brians-brain-seeds](brians-brain-seeds.md) (рефрактерний стан ≈ «згарище»).
- Ландшафтна екологія використовує модель для ролі «мозаїки палива» у пожежних режимах.
- Ігрові нащадки поширення вогню в корпусі: [simcity-1989](simcity-1989.md), [terra-nil](terra-nil.md), [noita](../dig-gravity/noita.md), [brogue](../roguelike/brogue.md); SOC-сусід — [abelian-sandpile](abelian-sandpile.md).

## Цікавинки для курсу
- Тристановий автомат з `random()` на клітину й подвійним буфером — 🌱.
- Порівняти сусідство фон Неймана й Мура (ті самі p, f — інша картина) — 🌱.
- Розміри кластерів flood fill-ом / union-find і гістограма в лог-лог — 🥉.
- Перколяційний експеримент: 100 запусків на густину, крива «дійшов до краю», пошук порогу ≈ 59 % — 🥉.
- Ефективна реалізація малого f: не кидати монетку на кожну клітину, а пропускати геометрично розподілену кількість — 🥈.
- Пожежа як мінігра: гравець ставить просіки з обмеженим бюджетом, щоб урятувати частку лісу — 🥉.

## Мапа на каталог
- Є: `game-loop` + `game-pause` · `state-as-data` · `game-settings` + `settings-elements` (p, f) + `field-size-picker` · `rule-variants` (сусідство, перколяція) · `connectivity-check` (кластери BFS) · `logic-render-split` · `gui-render` · `unit-tests`.
- **Нема** → пропозиції карток:
  - `+stochastic-cell-rule` «Перехід клітини з імовірністю» · game-logic · 🌱 · слоти {p_per_state}.
  - `+percolation-threshold` «Пошук порогу перколяції серією запусків» · game-logic · 🥉 · слоти {density_step, runs}.
  - `+cluster-stats` «Розміри звʼязних кластерів і гістограма» · interface/results · 🥉 · слоти {neighbourhood}.
  - Перевикористано: `+fire-spread`, `+cellular-automaton-rule`, `+multi-state-cell`, `+step-run-speed`.

## Пропозиції до словників
- `+card:stochastic-cell-rule`, `+card:percolation-threshold`, `+card:cluster-stats` — див. «Мапа на каталог».
- `+ui:cluster-histogram` — розподіл розмірів кластерів/пожеж.
- `+axis:neighbourhood` — значення `von-neumann` / `moore` / `hex` / `kernel`: та сама модель у Вікіпедії (4) і в демо (8) поводиться по-різному.

## Джерела
- ⭐ [Wikipedia: Forest-fire model](https://en.wikipedia.org/wiki/Forest-fire_model) — стани, чотири правила Drossel–Schwabl, сусідство фон Неймана, p/f, нерівність масштабів, кластери, межі критичності, застосування.
- [aryan.app: HTML5 forest fire](http://aryan.app/randomstuff/forestfire.html) — Pgrowth, Plightning, кольори, сусідство Мура.
- [NetLogo Models Library: Fire](https://ccl.northwestern.edu/netlogo/models/Fire) — перколяційний варіант, DENSITY, SETUP/GO, поріг ≈ 59 %, жарини.
- [Fisch, Gravner, Griffeath (1991)](https://www.math.ucdavis.edu/~gravner/papers/fgg.pdf) — «forest fire»-рівноваги як родичі збудливих автоматів.
- YouTube: пошук «forest fire cellular automaton».

## Непевне
- (?) Межа поля (тор чи обрізане поле) і розмір сітки в демо — не вказані.
- (?) Значення p і f за замовчуванням у демо aryan.app — у тексті сторінки не видно.
- (?) Чи дає хоч одна типова версія підпалити дерево кліком — не бачив.
- (?) Правила моделі Bak–Chen–Tang 1990 (детермінований ріст?) — не перевірено.
