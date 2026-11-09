---
title: Plumber / Pipes / Water Connect (мобільний жанр)
slug: plumber-pipe-rotation
aka: [Plumber, Pipes, Water Connect, Water Pipes, Pipe Connect, «Сантехнік», «Труби»]
family: connect-rotate
also: [pencil-logic]
klass: cursor
axes:
  field: square
  time: static
  opponent: none
  info: full
  random: setup
  goal: state
year: 2010
platforms: [mobile, web]
links:
  - {kind: official, url: "https://apps.apple.com/us/app/id1341680606", best: true, note: "Water pipes: pipeline (Creative Soft): тап крутить трубу, шлях від вентиля до резервуара; режими Classic, Firefighter, Pressure, Multicolor; 500+ рівнів, підказки за золото, щоденні"}
  - {kind: other, url: "https://phaser.io/news/2018/01/plumber", note: "Plumber (Phaser, 2018): труби закріплені, їх можна лише крутити; вода — на інший бік; режими рівнів і на час"}
  - {kind: other, url: "https://appgoblin.info/apps/com.durusoft.pipepuzzlewaterconnect", note: "Pipe Puzzle: Water Connect (DuruSoft, 2025): 250+ рівнів, пауза"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Pipe_Mania", note: "контекст: клони Pipe Mania, Canal Control на Nokia, злам у BioShock"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=pipes+plumber+puzzle+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [tile-rotate, pipe-connectors, cell-click, connectivity-check, reachability-check, completion-detection, sequential-levels, level-unlock, level-select, time-out, daily-puzzle, difficulty-levels, game-screen, end-screen, main-menu, mode-select, +lit-from-source, +commit-then-flow, +source-to-sink-path, +decoy-tiles, +multi-source-color-match, +all-sources-to-sink, +scramble-solution-rotations, +flow-animation]
proposes: ["+trigger:valve_open", "+effect:flow_fill", "+feature:hint-for-currency", "+card:commit-then-flow", "+card:decoy-tiles", "+card:scramble-solution-rotations", "+card:multi-source-color-match"]
author: opus
date: 2026-11-09
---

# Plumber / Pipes / Water Connect — тапом крутиш закріплені труби, щоб вода дійшла від вентиля до резервуара

## Суть
Масовий мобільний жанр 2010-х, нащадок Pipe Mania і Net: труби вже стоять на полі, їх не можна ні класти, ні переставляти — лише крутити тапом. На відміну від `infinity-loop.md`, мета не «усі стики закриті», а **шлях від джерела (вентиль) до приймача (резервуар, будинок, що горить)**; частина труб — зайві, обманки. Часто є окрема кнопка «відкрити вентиль»: вода біжить трубами анімацією, і тоді видно, де шлях рветься. Цей файл — сімейний опис жанру як бази для порівняння з `pipe-mania.md` (черга й таймер потоку) та `infinity-loop.md` (усі стики, дерево).

## Поле і час
- Квадратна сітка; кожна клітина — труба (кінцівка, пряма, коліно, трійник, хрест) або порожня/перешкода; джерело й приймач — на краю або всередині поля.
- Час: статичний пазл; у частині ігор — режим на час (таймер рівня) або бали/досвід за швидкість.
- Генерація або ручні рівні; сотні рівнів зі зростанням розміру поля.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Труба (пряма/коліно/трійник/хрест) | conduit | маска портів, орієнтація | тап — поворот на 90° |
| Вентиль / кран | source | колір (у Multicolor) | звідси йде вода |
| Резервуар / будинок / пристрій тиску | sink | колір, потрібна кількість джерел | має отримати воду |
| Вода | object | колір, фронт | після відкриття вентиля тече лише стиками, що збігаються |
| Зайва труба (обманка) | conduit | — | не входить у розвʼязок; її стан не важливий |
| Закріплена труба | static | — | не обертається (?) |
| Перешкода / порожня клітина | static | — | без портів |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(tap, pipe)` → ЯКЩО `not state(pipe, fixed)` → ТО `rotate(pipe, 90)`.
- КОЛИ `after(rotate)` → ТО `custom: «перерахувати компоненту, звʼязану з джерелом, і підсвітити її (вода "вже в трубах")»` — варіант жанру з миттєвою підсвіткою.
- КОЛИ `input(open_valve)` → ТО `custom: «вода тече від джерела стиками з однаковими портами, клітина за клітиною (анімація)»`.
- КОЛИ `custom: «вода дійшла до приймача»` → ЯКЩО `path_exists(source, sink)` → ТО `win`, `next_level`.
- КОЛИ `custom: «вода дійшла до відкритого кінця труби»` → ТО `custom: «витік; рівень не пройдено, можна крутити далі»` (?).
- Multicolor: КОЛИ `custom: «перевірка»` → ЯКЩО `custom: «кожен вентиль зʼєднано з резервуаром свого кольору»` and `custom: «мережі різних кольорів не перетинаються»` → ТО `win`.
- Pressure: КОЛИ `custom: «перевірка»` → ЯКЩО `count(connected_sources, ==, all)` → ТО `win` — усі вентилі мають дійти до одного пристрою тиску.
- Режим на час: КОЛИ `counter(time_left, ==, 0)` → ТО `lose`, `window(end-screen)`.
- КОЛИ `input(hint)` → ЯКЩО `has(player, coins)` → ТО `take(player, coins)`, `custom: «одна труба стає в правильну орієнтацію»` (?).
- КОЛИ `level_end` → ЯКЩО `timer(<, n)` → ТО `score(+speed_bonus)` — досвід за швидкість (Water pipes).
- Перемога: шлях джерело → приймач (або всі джерела → приймачі) · Поразка: лише в режимі на час · Рахунок: досвід/зірки за швидкість (?).

## Керування і ввід
- Тап по трубі — поворот на 90° (за годинниковою (?)); кнопка «відкрити вентиль» у варіантах із перевіркою за запитом.
- Жодного drag чи вибору фігури: уся складність — у порядку поворотів і відкиданні обманок.

## Вікна, меню, HUD
- `main-menu` → `mode-select` (Classic · Firefighter · Pressure · Multicolor; у Plumber — рівні / на час) → `level-select` (сітка рівнів з прогресом).
- `game-screen`: поле, кнопка вентиля, `hint-button` (за монети), `timer-countdown` у режимі на час, `level-number`.
- `end-screen`: рівень пройдено → наступний (часто після реклами); `daily-window` — щоденні виклики.
- `shop-window`: монети, «Remove Ads».
- `settings-window`: звук, музика, вібрація.

## Фічі поза полем
- `levels-sequential` + `level-unlock`, сотні рівнів; `mode-daily`; `mode-time-attack`.
- `hint` за ігрову валюту; монетизація рекламою між рівнями.
- `xp-level` — досвід за швидкі розвʼязки (Water pipes).

## Варіації й родичі
- `pipe-mania.md` — труби з черги, кладуться гравцем, потік біжить за таймером; `infinity-loop.md` — те саме обертання, але мета «усі стики» / одне дерево від джерела; `flow-free.md` — кольорові пари, але шлях малюється, а не крутиться; `zenji.md` — обертання з джерелом і кінцевими точками.
- Злам у BioShock — Pipe Mania-подібна міні-гра; Canal Control на Nokia.
- **Осі варіацій:** хід — поворот / зсув рядка / обмін / класти з черги · мета — джерело→приймач / усі стики / всі джерела→один приймач / кольорові пари · перевірка — постійна підсвітка / кнопка «відкрити вентиль» · зайві труби — є / нема · час — нема / таймер рівня.

## Цікавинки для курсу
- Генерація: випадковий самонеперетинний шлях від джерела до приймача (DFS з поверненням) → розставити по ньому труби з потрібними портами → решту клітин заповнити випадковими обманками → перемішати орієнтації всіх труб випадковими поворотами — 🥉.
- Перевірка після кожного тапу: BFS від джерела по сусідах, у яких порти збігаються з обох боків; приймач у компоненті → перемога — 🌱.
- Анімація потоку «клітина за клітиною» за тією ж BFS (фронт хвилі = рівень у BFS) — 📎.
- Multicolor: кілька BFS з різних джерел і перевірка, що компоненти не перетинаються — 📎.
- Гарантія, що згенерований рівень не розвʼязується «випадково» на старті (перемішування не повернуло розвʼязок) — 🌱; оцінка мінімальної кількості тапів (сума поворотів до розвʼязку по кожній трубі) — 📎 для «зірок за ходи».
- Підказка «постав одну трубу правильно» з відомого розвʼязку генератора — 🌱.

## Мапа на каталог
- Є: `tile-rotate` · `pipe-connectors` · `cell-click` · `connectivity-check` · `reachability-check` (шлях джерело→приймач) · `completion-detection` · `sequential-levels` · `level-unlock` · `level-select` · `time-out` · `daily-puzzle` · `difficulty-levels` · `game-screen` · `end-screen` · `main-menu` · `mode-select`.
- **Нема** → пропозиції карток:
  - `+commit-then-flow` «Перевірка за кнопкою з анімацією потоку» · game-logic/win · 📎.
  - `+source-to-sink-path` «Мета — шлях від джерела до приймача, не всі клітини» · game-logic/win · 🌱.
  - `+decoy-tiles` «Зайві плитки, що не входять у розвʼязок» · levels/generation · 🌱.
  - `+scramble-solution-rotations` «Генерація: розвʼязок → випадкові повороти» · levels/generation · 🥉.
  - `+multi-source-color-match` «Кожне джерело — до приймача свого кольору» · game-logic/constraints · 📎.
  - `+all-sources-to-sink` «Усі джерела до одного приймача» · game-logic/constraints · 🌱.
  - `+lit-from-source` (з Infinity Loop/Net) · `+flow-animation` «Анімація фронту потоку» · interface/graphics · 📎.

## Пропозиції до словників
- `+trigger:valve_open` — гравець запустив перевірку потоку (кнопка вентиля).
- `+effect:flow_fill(source)` — заповнити трубопровід від джерела фронтом (BFS-хвиля); родич `advance_flow` з Pipe Mania.
- `+feature:hint-for-currency` — підказка за ігрову валюту.

## Джерела
- ⭐ [App Store: Water pipes: pipeline](https://apps.apple.com/us/app/id1341680606) — тап крутить трубу, шлях вентиль → резервуар, чотири режими (Classic, Firefighter, Pressure, Multicolor), 500+ рівнів, досвід за швидкість, підказки, щоденні виклики, таймер (зі скарг у відгуках).
- [Phaser.io: Plumber](https://phaser.io/news/2018/01/plumber) — труби закріплені, лише поворот; вода на інший бік; рівні без часу й режим на час.
- [AppGoblin: Pipe Puzzle: Water Connect](https://appgoblin.info/apps/com.durusoft.pipepuzzlewaterconnect) — типовий сучасний представник: 250+ рівнів, налаштування звуку/вібрації, пауза.
- [Wikipedia: Pipe Mania](https://en.wikipedia.org/wiki/Pipe_Mania) — клони, Canal Control на Nokia, злам у BioShock.
- YouTube: пошук «pipes plumber puzzle gameplay».

## Непевне
- (?) Рік «2010» — умовний старт жанру на смартфонах; конкретної першої гри не встановлено.
- (?) Що буде з витоком води у відкритий кінець (поразка / просто «не пройдено») — залежить від гри, не перевірено.
- (?) Закріплені нерухомі труби, зірки за кількість тапів, напрям повороту — типові для жанру, але в жодному відкритому джерелі не підтверджено.
- (?) Модель підказки «одна труба правильно» — з памʼяті; Water pipes підтверджує лише, що підказки коштують золото.
- (?) Multicolor: що відбувається при змішуванні кольорів — не описано.
