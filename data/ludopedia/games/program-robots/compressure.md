---
title: ComPressure
slug: compressure
aka: [Com Pressure]
family: program-robots
also: [connect-rotate]
klass: cursor
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1528120/ComPressure/", best: true, note: "суть, керування трубами, тиск 0–100, клапан «+»/«−», тести з допуском 5 %, дизайни → компоненти; скриншоти UI"}
  - {kind: official, url: "https://github.com/brejc8/ComPressure", note: "вихідний код гри (C++/SDL): сітка 9×9, типи елементів, фізика тиску, ціни, рівні"}
  - {kind: other, url: "https://raw.githubusercontent.com/brejc8/ComPressure/master/lang.json", note: "довідка F1 (24 сторінки): клапан Openness = P − N, дільник S/(S+V), режими очок, експеримент, редактор рівнів"}
  - {kind: other, url: "https://raw.githubusercontent.com/brejc8/ComPressure/master/Level.json", note: "42 рівні від Cross до Steamputer: порти, тести, кроки"}
  - {kind: other, url: "https://steamcommunity.com/app/1528120/guides/", note: "гайди спільноти: формула S/(S+V), прості розвʼязки від автора"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=ComPressure+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [pipe-connectors, path-drawing, tile-rotate, piece-rotate-flip, cell-click, user-procedures, sequential-levels, level-unlock, level-select, game-screen, help-window, tutorial-window, pause-menu, undo-redo, undo-unlimited, redo, save-multi-slot, state-string, level-exchange, in-game-editor, editor-playtest, language-picker, volume-control, background-music, sound-effects, +analog-pressure-diffusion, +pressure-valve, +pressure-divider, +port-spec-tests, +test-phases, +worst-test-score, +score-modes, +design-as-component, +component-inherits-quality, +experiment-sliders, +global-score-graph, +friend-design-inspect, +customize-local-copy, +signs-comments, +crossing-pipe-tile]
proposes: ["+effect:equalize(a, b)", "+effect:flow(a, b, k)", "+effect:vent(a)", "+cond:greater(a, b, prop)", "+trigger:test_step", "+window:experiment", "+window:metric-histograms", "+ui:port-slider", "+ui:waveform-chart", "+feature:score-modes", "+feature:design-slots", "+axis:signal"]
author: opus
date: 2026-11-09
---

# ComPressure — компʼютер на тиску пари: труби на сітці 9×9 і клапан, що відкритий настільки, наскільки «+» вищий за «−»

## Суть
Паровий «транзисторний» пазл Charlie Brej: на полі 9×9 гравець прокладає труби, ставить інжектори пари (100) і клапани, щоб вихідний порт видавав потрібний тиск як функцію тисків на інших портах. Сигнал **аналоговий** (0–100), а не біт: тиск між інжектором і відкритим кінцем ділиться, як напруга в дільнику; клапан — керований опір. Розвʼязок проходить серію тестів з допуском 5 %; кожен пройдений дизайн стає компонентом наступних (буфер → інвертор → суматор → защіпка → лічильник → ROM → парокомпʼютер). Слабкий ранній дизайн робить слабкими всі схеми, що його використовують.

## Поле і час
- Квадратна сітка **9×9** клітин (у коді `elements[9][9]`); на кожному боці поля — порт N/E/S/W з кольором; рівень визначає, які порти входи, а який — вихід.
- Клітина містить один елемент: трубу (14 конфігурацій), клапан, інжектор, підсхему (готовий дизайн) або порожнечу; у користувацьких рівнях — заблоковані клітини.
- Тиск живе в **точках зʼєднання** між клітинами (числа на стиках труб); елементи щотіку переносять пару між своїми точками.
- Час `programmed`: симуляція покроково (сотні–тисячі підкроків на фазу тесту); тест — послідовність фаз із заданими тисками входів; вихід порівнюється в кінці фази.
- Детерміновано; динаміка неперервна — тиск наростає кривою (графік у панелі тесту).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Труба | conduit | 2/3/4 порти; варіанти «перехрестя без зʼєднання» (NS+WE, NW+ES, NE+WS) | щотік вирівнює тиск між своїми портами (½, ⅓, ¼ різниці) — має малий опір |
| Відкритий кінець | sink | — | стравлює в атмосферу: тиск точки прямує до 0 |
| Інжектор пари | source | 100; напрямок; ціна £5 | тримає свою точку на 100 |
| Клапан | switch | сторони «+», «−» (керування), проходи W–E; опір 8 труб; ціна £10 | відкритість = P(+) − P(−); ≤ 0 — закритий; пара на «+»/«−» не витрачається |
| Підсхема | container | готовий дизайн рівня; ціна £4 + вміст | симулює свою схему 9×9, порти = 4 точки клітини |
| Порт-вхід | source | значення з тесту або повзунка | примусово задає тиск на краю поля |
| Порт-вихід | sink | ціль тесту | записує тиск; порівнюється з ціллю |
| Табличка (sign) | mark | текст | коментар на полі, без фізики |
| Заблокована клітина | static | лише в редакторі рівнів | не можна будувати |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag_pipe)` → ТО `place(player, pipe)` по клітинах шляху; КОЛИ `input(click)` → ТО труба подовжується на клітину в бік курсора.
- КОЛИ `input(drag_pipe)` → ЯКЩО `custom: «нова труба лягає поверх старої впоперек»` → ТО `custom: «перехрестя без зʼєднання»`; ЯКЩО `custom: «подовжено в бік наявної труби»` → ТО `attach(new_pipe, pipe)` (T або хрест).
- КОЛИ `input(hold_rmb)` → ТО `disappear(element)`; `input(Q|E)` → ТО `rotate(element, 90)`; кнопки віддзеркалення — `custom: «відбити по вертикалі/горизонталі»`.
- КОЛИ `tick` → ТО `custom: «кожна труба переносить між своїми точками ½ (2 порти), ⅓ (T) або ¼ (хрест) різниці тисків»`.
- КОЛИ `tick` → ЯКЩО `custom: «кінець труби ні з чим не зʼєднаний»` → ТО `custom: «тиск точки −½ — стравлювання до 0»`.
- КОЛИ `tick` → ТО `custom: «інжектор підтягує свою точку до 100»`.
- КОЛИ `tick` → ЯКЩО `custom: «P(+) > P(−)»` → ТО `custom: «клапан переносить W↔E потік = (P_W − P_E) · (P(+) − P(−)) / (2 · 100 · 8)»`; ЯКЩО `custom: «P(+) ≤ P(−)»` → ТО `block` (закритий).
- КОЛИ `tick` → ЯКЩО `custom: «елемент — підсхема»` → ТО `custom: «симулюється її вміст; змінений оригінал оновлюється в усіх місцях використання»`.
- КОЛИ `phase_start(test_step)` → ТО `set_value(input_ports, step_values)`; `custom: «можна скинути дизайн на початку тесту»`.
- КОЛИ `custom: «кінець фази»` → ТО `custom: «вихід порівнюється з ціллю: 100 очок за точний збіг, лінійно до 0 при відхиленні 5 %»`.
- КОЛИ `custom: «усі тести пройдено»` → ЯКЩО `custom: «найгірший тест > 0»` → ТО `score(worst_test)`, `custom: «відкривається наступний рівень, дизайн додається в меню компонентів»`.
- КОЛИ `input(customize)` під час інспекції компонента → ТО `clone(component)` — локальна копія (червона), більше не оновлюється з оригіналу.
- КОЛИ `input(slider, port)` у режимі експерименту → ТО `set_value(port, v)`; горизонтальний повзунок — сила подачі; крайнє ліве положення → `custom: «порт стає виходом»`.
- Перемога (рівня): усі тести з очками > 0 · Поразка: нема (тест просто 0) · Рахунок: Accuracy — найгірший тест (0–100); Price — £1 за порт труби, £10 клапан, £5 інжектор, +£4 за підсхему; Steam — кількість поданої інжекторами пари.

## Керування і ввід
- ЛКМ — тягти трубу від початку до кінця або клацати, подовжуючи в бік курсора; ПКМ — вийти з режиму; утримання ПКМ — видаляти.
- Build-меню: інжектор, клапан, готові компоненти; Q/E або колесо — поворот перед розміщенням; Tab / СКМ — перемикання клапан ↔ інжектор.
- Виділення: Ctrl+клік або Shift+drag; WASD — зсув виділеного, Q/E — поворот, C/X/V — копіювати/вирізати/вставити, Delete; Z — undo, Y або Shift+Z — redo (також ПКМ+ЛКМ).
- Тести: 1 — пауза, 2 — повтор одного тесту, 3 — усі тести; Space — до наступної фази; F1 — довідка; Esc — меню.
- Подвійний клік по компоненту — зайти всередину; іконка дизайну зліва вгорі — назад по стеку.

## Вікна, меню, HUD
- `level-select`: сітка рівнів; нижня панель — вимоги (вихід через інші порти, кольорові позначки портів); клік по вимозі — підказка.
- `game-screen`: поле 9×9 з 4 портами; числа тиску на стиках; праворуч вкладки: дизайн (wrench), тест, експеримент, очки; `speed-slider` (балон з »»»); `help-window` «?».
- `tool-palette` (build-меню): інжектор, клапан і всі пройдені дизайни з їхніми очками на іконці.
- Панель тесту: кнопки пауза / повтор 1 / усі; ряд очок кожного тесту + ряд найкращого дизайну + підсумок (найгірший); послідовність входів і цілей поточного тесту з підсвіткою фази; `waveform-chart` (custom) — графік виходу в останній фазі з блідою лінією найкращого дизайну.
- `experiment` (custom): вертикальні повзунки значень портів, горизонтальні — сила; графік історії всіх портів.
- `metric-histograms` (custom): глобальний графік очок, позиція гравця й друзів; дизайни друзів можна відкрити.
- `dialogue-window`: портрет і текст (Charles Chavvington, Nicola…); кнопки «Repeat dialogue», «Hint», «Reveal a solution».
- `pause-menu` (Esc): вихід, повноекранний режим, Discord, титри, гучність звуку й музики; вибір мови; «Number resolution».
- `editor-window`: користувацькі рівні — іконка, тести й кроки (+/−), тривалість кроку, вибір портів-входів і виходів, скидання дизайну, обмін через буфер; список «User levels».
- `tutorial-window`: довідка F1 у 24 сторінках з анімованими прикладами (?).
- Переходи: level-select → game-screen (дизайн) ⇄ тест ⇄ експеримент; game-screen → очки → дизайн друга; Esc → pause-menu.

## Фічі поза полем
- Три режими оцінки (`score-modes`): точність, ціна, витрата пари — одна задача, три різні оптимуми.
- 4 слоти дизайнів на рівень + автоматично збережений найкращий; експорт/імпорт дизайну рядком у буфер обміну.
- Дизайн-як-компонент: зміна оригіналу оновлює всі використання; «Customize» відʼєднує копію.
- Підказки, «показати розвʼязок», Discord-спільнота «High Pressure Steam Society»; досягнення й статистика Steam.
- Редактор користувацьких рівнів з обміном через буфер; 9 мов інтерфейсу.

## Варіації й родичі
- Автор: [Infinite Turtles](infinite-turtles.md) (2022) — той самий інтерфейс, але токени-числа й рекурсія замість аналогового тиску.
- Корпус: [turing-complete](turing-complete.md) і [kohctpyktop](kohctpyktop.md) (логіка з елементів на сітці), [factorio-circuit-network](factorio-circuit-network.md) (сигнали-числа), [tis-100](tis-100.md) (тести з потоками даних), [turing-tumble](turing-tumble.md) (механічні біти).
- Осі варіацій: **сигнал** (біт / число-токен / аналоговий тиск); **ключ** (транзистор із геометрії — KOHCTPYKTOP / клапан з двома керуючими портами — ComPressure / реле); **оцінка** (точність з допуском / ціна / ресурс); **повторне використання** (дизайн як компонент з оновленням / копія).

## Цікавинки для курсу
- Дифузія тиску по трубах (½ / ⅓ / ¼ різниці щотік) + стравлювання відкритих кінців — 🥉 (клітинний автомат з числами).
- Клапан як аналоговий ключ: потік ∝ (P(+) − P(−)) × різниця тисків — 🥈 (і дільник S/(S+V) як вправа).
- Тести з фазами, допуском 5 % і очками «найгірший тест» — 🥉.
- Дизайн-як-компонент: стек вкладених схем, оновлення всіх використань, «customize» як копія — 🥇.
- Три режими оцінки одного розвʼязку (точність, ціна, пара) з глобальним графіком — 🥉.
- Режим експерименту: повзунки портів + графік історії — 📎.

## Мапа на каталог
- Є: `pipe-connectors` (труби з портами) · `path-drawing` (протягування труби) · `tile-rotate` / `piece-rotate-flip` (поворот, віддзеркалення) · `cell-click` · `user-procedures` (пройдені дизайни як функції) · `sequential-levels` / `level-unlock` / `level-select` · `game-screen` · `help-window` · `tutorial-window` · `pause-menu` · `undo-redo` / `undo-unlimited` / `redo` · `save-multi-slot` (4 слоти) · `state-string` (дизайн рядком) · `level-exchange` · `in-game-editor` / `editor-playtest` · `language-picker` · `volume-control` · `background-music` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+analog-pressure-diffusion` «Аналоговий тиск вирівнюється по трубах» · entities/interact · 🥉.
  - `+pressure-valve` «Клапан: відкритість = P(+) − P(−)» · entities/interact · 🥈; `+pressure-divider` «Дільник S/(S+V)» · 📎.
  - `+crossing-pipe-tile` «Перехрестя без зʼєднання» · entities/state · 🌱.
  - `+port-spec-tests` / `+test-phases` «Тести: фази входів і ціль виходу з допуском» · game-logic/win · 🥉; `+worst-test-score` · 📎.
  - `+score-modes` «Кілька режимів оцінки розвʼязку» · game-logic/score · 📎; `+global-score-graph` · interface/results · 🥉.
  - `+design-as-component` «Пройдений дизайн — компонент наступних» · game-logic/program · 🥈; `+component-inherits-quality` · 📎; `+customize-local-copy` · 📎.
  - `+experiment-sliders` «Ручні повзунки портів + графік» · interface/input · 🥉; `+friend-design-inspect` · 📎; `+signs-comments` · 🌱.

## Пропозиції до словників
- `+effect:equalize(a, b)` — вирівняти значення між сусідніми точками на частку різниці (тиск, тепло).
- `+effect:flow(a, b, k)` — перенести кількість з A в B з коефіцієнтом (клапан); `+effect:vent(a)` — стравити до фонового значення.
- `+cond:greater(a, b, prop)` — A більше за B за властивістю (P(+) > P(−)).
- `+trigger:test_step` — почалась фаза тесту з новими значеннями входів (ComPressure, TIS-100, KOHCTPYKTOP).
- `+window:experiment` — пісочниця з ручними значеннями портів; `+window:metric-histograms` — глобальний розподіл очок.
- `+ui:port-slider` — повзунок значення порту; `+ui:waveform-chart` — графік сигналу в часі.
- `+feature:score-modes` — кілька незалежних метрик одного розвʼязку; `+feature:design-slots` — слоти дизайнів на рівень + найкращий.
- `+axis:signal` — `bit | number-token | analog` — тип сигналу в програмних іграх.

## Джерела
- ⭐ [Steam: ComPressure](https://store.steampowered.com/app/1528120/ComPressure/) — опис, керування, тиск, клапан, тести 5 %, реліз 3 травня 2021, скриншоти (поле 9×9, панелі тесту й експерименту).
- [GitHub brejc8/ComPressure](https://github.com/brejc8/ComPressure) — код: `Circuit.h/.cpp` (9×9, типи труб, клапан, інжектор, підсхема, ціни, опір 8), `Level.json` (42 рівні), `lang.json` (довідка, діалоги, 9 мов).
- [Steam-гайди](https://steamcommunity.com/app/1528120/guides/) — «A guide to accuracy: the S/(S+V) formula», «Simple implementation guide» від автора (сторінки гайдів віддали 429).
- YouTube: пошук «ComPressure gameplay».

## Непевне
- (?) Точний вигляд tutorial-вікна F1 — бачив лише тексти довідки, не сам екран.
- (?) Як саме інжектор «тримає» 100 і як порт-вхід застосовує «силу» (код `apply(vol, drive)`) — прочитав поверхово; формули труб і клапана — з коду.
- (?) Скільки підкроків на фазу (у Level.json `substep_count` 2000 для першого рівня) — для інших рівнів не дивився.
- (?) Чи можна вкласти дизайн сам у себе — у коді є перевірка `contains_subcircuit_level`, схоже, рекурсія заборонена (на відміну від Infinite Turtles).
