---
title: Neon Noodles
slug: neon-noodles
aka: ["Neon Noodles - Cyberpunk Kitchen Automation"]
family: program-robots
also: [build-sim]
klass: hybrid
axes:
  field: square
  time: programmed
  opponent: none
  info: full
  random: none
  goal: collect
year: 2023
platforms: [PC, Mac, Linux, Switch, PS4, PS5, Xbox One, Xbox Series]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/990900/Neon_Noodles/", best: true, note: "Vivid Helix; ранній доступ 29.11.2019, реліз 03.08.2023; роботи-кухарі програмуються записом власних дій, 250 рецептів і 400 інгредієнтів, гістограми й таблиці друзів; знімки: сітка кухні, таймлайн ботів, метрики Cycles / Program Size / Bot Area / Sum"}
  - {kind: official, url: "http://neonnoodles.com", note: "сайт: «deliciously dark zach-like»; Steam, Switch, PS4/PS5, Xbox"}
  - {kind: itch, url: "https://vividhelix.itch.io/neon-noodles", note: "записуєш власний ввід, бот його повторює, запис можна правити; станції-телепорти"}
  - {kind: other, url: "https://gamespace.com/featured/neon-noodles-pc-hands-on-preview-too-early-to-feast/", note: "превʼю раннього доступу: три етапи рівня (розстановка → код → відтворення), обмежені ресурси на сітці, одна загальна команда взяти/покласти, графік порівняння з іншими"}
  - {kind: other, url: "https://www.nintendo.com/us/store/products/neon-noodles-switch/", note: "Switch 16.07.2025 (eastasiasoft): «build cooking machines by recording and replaying actions»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Neon+Noodles+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [command-program, step-execution, code-editor-window, drag-drop-piece, cursor-place, cell-transform, row-conveyor, teleport, collect-quota, undo-redo, game-pause, sequential-levels, level-select, leaderboard, save-multi-slot, mode-indicator, goal-counter, status-panel, keyboard-controls, controls-remap, game-screen, end-screen, +record-replay-programming, +instruction-timeline, +swarm-separate-programs, +auto-padding-sync, +program-linking, +loop-markers, +craft-at-station, +item-filter-sort, +station-double-use-error, +solution-metrics, +metric-histograms, +gif-export, +bot-movement-models, +run-to-cursor]
proposes: ["+effect:record(cmd)", "+effect:grab", "+effect:release", "+effect:wait", "+cond:station_busy(station)", "+role:device", "+ui:instruction-timeline", "+ui:recipe-list", "+ui:undo-history", "+window:companion", "+feature:design-slots", "+feature:gif-export", "+axis:control"]
author: opus
date: 2026-11-19
---

# Neon Noodles — кіберпанк-кухня на сітці: проведи бота через рецепт власними руками, і він повторюватиме запис, доки не наготує квоту страв

## Суть
Zach-like про автоматизацію кухні: на сітці стоять продюсери інгредієнтів, станції (ніж, блендер, каструля, сковорода, миска) і клітини-цілі, а страви готують роботи-кухарі. Головна особливість — **програмування записом**: гравець сам керує ботом (як аватаром), гра пише кожну дію в рядок таймлайну, а потім бот повторює запис по колу; рядок можна правити — вставляти, видаляти, замінювати команди. Ботів кілька, у кожного своя програма, і їх треба синхронізувати. Після квоти страв — чотири метрики й гістограми серед друзів і всього світу. Клас `hybrid`: курсор для розстановки, аватар — для запису.

## Поле і час
- Кухня — квадратна сітка з пунктирною межею ігрової зони; у пізніх рівнях зона більша (#14). Станції, продюсери й цілі займають по клітині.
- Шари: підлога · станції, конвеєри, столи · предмети (інгредієнти, напівфабрикати, страви) · боти; дрони літають над столами.
- Етапи рівня (превʼю): розстановка станцій і ботів → запис і правка програм → відтворення до квоти.
- Час `programmed`: такт = одна команда в рядку кожного бота; програми циклічні; Cycles рахує такти до квоти.
- Детерміновано; випадковості нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Звичайний бот (Regular Bot) | player | займає 1 клітину | на знімку «Maple Beans» стоїть у центрі хреста станцій, повертається ↰ / ↱ і бере чи кладе предмети на сусідніх клітинах |
| Рейковий бот (Rail Bot) | player | «танкове» керування | їде по прямій; ліво/право — відносно самого бота (#7, #9) |
| Дрон (Drone Bot) | player | рух відносно камери | літає над кухнею й сідає на клітини; патчі згадують посадку, виліт за межі й зіткнення дронів |
| Продюсер інгредієнта | spawner | вид (риба, авокадо, перець, кленовий сироп…) | дає інгредієнт для рецептів |
| Станція рецепта | container | інструмент: ніж, блендер, каструля, сковорода, миска | приймає інгредієнти й робить продукт за рецептом зі списку RECIPES |
| Конвеєр | terrain | напрямок; авто-подача й фільтр (#13) | везе предмет до станції |
| Станція-телепорт | terrain | — | переносить предмети (зʼявилась у рівні 18 «Jollof Rice», #9) |
| Zero Table | static | — | не приймає предметів; ділить рівень на окремі частини |
| Станція переробки | sink | — | приймає зайве; замінила смітник у v1.0.2 |
| Клітина-ціль | sink | страва, квота 6 / 12 / 24 | готова страва зараховується в «GOALS 0/12» |
| Інгредієнт, напівфабрикат, страва | object | вид | несуть боти; станції перетворюють |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place)` → ЯКЩО `free(cell)` і `custom: «у межах ігрової зони»` → ТО `place(player, station|bot)`; переміщення й видалення пишуться в історію UNDO («Move Maple Syrup Producer», «Remove Rail Bot»).
- КОЛИ `input(dir)` під час запису → ТО `move(bot, dir)` (звичайний і рейковий бот — `rotate(bot, 90)` для ↰ / ↱) і `custom: «команда дописується в рядок бота на таймлайні»`.
- КОЛИ `input(action)` → ЯКЩО `occupied(target_cell, item)` → ТО `pickup(bot, item)`.
- КОЛИ `input(action)` → ЯКЩО `has(bot, item)` → ТО `place(bot, item)` — взяти й покласти — одна загальна команда.
- КОЛИ `custom: «на станції зібрано всі інгредієнти рецепта»` → ТО `transform(ingredients, product)`; рецепт з кількома виходами — `spawn(product)` кілька разів (#13).
- КОЛИ `input(play)` → ТО `timer(start)`.
- КОЛИ `tick` → ТО `custom: «кожен бот виконує наступну команду свого рядка»`, `counter(cycles, +1)`.
- КОЛИ `exec(wait)` → ТО `custom: «бот стоїть такт»`; auto-padding сам дописує очікування, щоб програми лишались синхронні (#5, #7; у пізній грі — вимикається, #14).
- КОЛИ `exec(loop_end)` → ТО `custom: «стрибок до мітки loop start»`.
- КОЛИ `custom: «дві команди використовують одну станцію в той самий такт»` → ТО `crash` — помилка double-use, позначка на таймлайні (#14, #16).
- КОЛИ `input(alt_click, cell)` → ТО `move(bot, cell)` — бот сам іде до курсора (v1.1).
- КОЛИ `enter(dish, goal_cell)` → ТО `counter(dishes, +1)`.
- КОЛИ `counter(dishes, ==, quota)` → ТО `win`, `window(end-screen)` з гістограмами.
- Перемога: квота страв кожного виду (напр. 12 + 12 поке-боулів) · Поразка: нема — помилка зупиняє відтворення й показує місце на таймлайні · Рахунок: Cycles — такти до квоти; Program Size — сума довжин програм усіх ботів (знімки: 10 × 59 = 590, 4 × 92 = 368, 1 × 15 = 15); Bot Area — площа, яку займають боти; Sum — четверта метрика (#15).

## Керування і ввід
- Клавіатура, миша і геймпад (DualShock / DualSense, Steam Deck); перепризначення клавіш — з Community Update #3.
- Панель CONTROLS: Ctrl+Z / Ctrl+Y — undo / redo; Bksp / Del — стерти команду; W A S D — рух; Q — очікування (␣); E, R (✓), F (⊗), G (💬), T (🎬) — інші дії; Z / X / C / V — назад / стоп / пуск / вперед у відтворенні; Esc.
- Мишею: розставити й перетягнути станції та ботів; клік по клітині таймлайну — правка посеред програми; перетягування — посунути предмет (#14); Alt-клік — бот іде до курсора.
- Таймлайн: вставити / видалити мітки loop start і loop; звʼязати програми ботів; прокрутка й перетягування під час відтворення; крок уперед і назад.

## Вікна, меню, HUD
- `level-select`: вкладки розділів I–VII, список замовлень (Fried Rice, Chicken Mole, Goulash…), бриф клієнта з портретом (Dalyx), слоти дизайнів «Design1», «Design1 (copy)», «<New Design>» з чотирма метриками й кнопками OPEN / COPY / RENAME / DELETE, під ними — 4 гістограми.
- `game-screen`: панелі CONTROLS (клавіші), STATS (`custom: «Cycles / Program Size / Bot Area / Sum»`), UNDO (`custom: «історія дій»`), GOALS (`goal-counter` «Salmon Poke Bowl 0/12»), RECIPES (`custom: «інструмент + інгредієнти ▸ продукт»`); сітка кухні; знизу таймлайн — рядок на бота «6 [59]» з іконками команд (стрілки, повороти, предмети з ▲ / ▼, `*`, ␣); `mode-indicator` EDITING / PAUSED.
- `end-screen`: гістограми з білою лінією найкращого результату (і по всіх збереженнях), метрика Sum, експорт GIF.
- `custom-window` «компаньйон»: гістограми, результати друзів Steam (#11, #15, #16).
- `dialogue-window`: сюжет — безіменний працівник, клієнти-аристократи й пограбування Neon Noodles.
- `settings-window`: підказки, перепризначення клавіш, розкладки; `tutorial-window` — навчальні рівні (на них зроблено демо).
- Переходи: level-select → OPEN → game-screen (EDITING) → запис / правка → ▶ → квота → end-screen → level-select.

## Фічі поза полем
- 250 рецептів кухонь світу, 400 інгредієнтів; розділи I–VII; 5 неонових локацій (#13).
- `save-slots`: кілька дизайнів на рівень — створити, копіювати, перейменувати, видалити; `cloud-save`.
- `leaderboard-online` + друзі; гістограми розподілу результатів за кожною метрикою.
- Експорт анімованого GIF з екрана гістограм (#7, #8).
- `undo` / `redo` правок; `step-mode` вперед і назад; `gamepad-support`, `remap-controls`, Steam Deck.
- Досягнення Steam; демо; порти на Switch (2025), PlayStation і Xbox.

## Варіації й родичі
- [opus-magnum](opus-magnum.md), [infinifactory](infinifactory.md) — прямі натхненники (так у Steam): руки, метрики, гістограми, GIF.
- [kaizen-a-factory-story](kaizen-a-factory-story.md) — таймлайн команд і гістограми, але програму ставлять клітинками, а не записом.
- [spacechem](spacechem.md) — кілька виконавців, яких треба синхронізувати.
- [plateup](../build-sim/plateup.md) — автоматизація кухні без програм; [meet-me-at-noon](../thinky/meet-me-at-noon.md) — запис власних ходів, які потім повторює двійник.
- Осі варіацій: **як задати програму** (записати демонстрацією / покласти команди на таймлайн / текст); **кінематика бота** (поворотна рука на місці / рейка з «танковим» керуванням / дрон відносно камери); **метрики** (такти / розмір програми / площа / сума).

## Цікавинки для курсу
- Програмування демонстрацією: ввід пишеться в рядок таймлайну, потім правка вставкою / видаленням / заміною — 🥉.
- Кілька ботів, кожен з власною циклічною програмою, і вирівнювання очікуваннями (auto-padding) — 🥈.
- Таблиця рецептів «інструмент + інгредієнти → продукт(и)» з кількома входами й виходами — 📎.
- Виявлення double-use: дві команди на одну станцію в одному такті — 📎.
- Три моделі руху ботів на одній сітці — 🥉.
- Чотири метрики (Program Size = сума довжин), гістограми з лінією рекорду, GIF — 📎 / 🥉.

## Мапа на каталог
- Є: `command-program` ↔ програма бота · `step-execution` ↔ відтворення, кроки вперед/назад · `code-editor-window` ↔ таймлайн · `drag-drop-piece` / `cursor-place` ↔ розстановка станцій · `cell-transform` ↔ станції рецептів · `row-conveyor` ↔ конвеєри · `teleport` ↔ станції-телепорти · `collect-quota` ↔ GOALS 0/12 · `undo-redo` · `game-pause` · `sequential-levels` / `level-select` ↔ розділи I–VII · `leaderboard` · `save-multi-slot` ↔ дизайни · `mode-indicator` ↔ EDITING / PAUSED · `goal-counter` · `status-panel` ↔ STATS · `keyboard-controls` / `controls-remap` · `game-screen` / `end-screen`.
- **Нема** → пропозиції карток:
  - `+record-replay-programming` «Програма = записаний ввід гравця» · game-logic/program · 🥉 · слот {edit: insert|delete|replace}.
  - `+auto-padding-sync` «Очікування дописуються, щоб програми йшли в ногу» · game-logic/program · 🥈.
  - `+program-linking` «Звʼязати програми кількох ботів» · game-logic/program · 📎; `+loop-markers` «Мітки початку й кінця циклу» · game-logic/program · 🌱.
  - `+station-double-use-error` «Дві дії на одній станції в такті — помилка» · game-logic · 📎.
  - `+bot-movement-models` «Боти з різною кінематикою» · entities/move · 🥉 · слот {model: arm|rail|drone}.
  - `+run-to-cursor` «Бот сам іде до клітини під курсором» · interface/input · 📎.
  - Повтори: `+instruction-timeline`, `+swarm-separate-programs`, `+craft-at-station`, `+item-filter-sort`, `+solution-metrics`, `+metric-histograms`, `+gif-export`.

## Пропозиції до словників
- `+effect:record(cmd)` — дія гравця дописується в програму активного бота.
- `+effect:grab` / `+effect:release` — тримати предмет маніпулятором (ширше за `pickup`); `+effect:wait` — такт без дії.
- `+cond:station_busy(station)` — станцію вже використовують у цьому такті.
- `+role:device` — станція з рецептом (інструмент + інгредієнти → продукт).
- `+ui:instruction-timeline` — рядки команд ботів на часовій шкалі; `+ui:recipe-list` — список рецептів іконками; `+ui:undo-history` — видима історія правок.
- `+window:companion` — бічна панель з гістограмами й друзями.
- `+feature:design-slots` — кілька розвʼязків на рівень з метриками; `+feature:gif-export`.
- `+axis:control` — `programmed`, але програма записується прямим керуванням (`direct` → запис).

## Джерела
- ⭐ [Steam: Neon Noodles](https://store.steampowered.com/app/990900/Neon_Noodles/) — опис і фічі (record-and-replay, редагування запису, телепорти, 250 рецептів, гістограми), дати, платформи; знімки: CONTROLS / STATS / UNDO / GOALS / RECIPES, сітка кухні, таймлайн «6 [59]», вікно вибору рівня з дизайнами й 4 гістограмами, рівні «Maple Beans» і «Jollof Rice Plate».
- Steam News (ISteamNews API, 40 записів 2019–2025): відкриті бети (керування, гістограми, метрики Cycles / Program Size / staleness), оновлення #5–#16, v1.0–1.2 — типи ботів, auto-padding, Zero Table, Teleport Station, конвеєри з авто-подачею й фільтром, double-use, GIF, компаньйон, метрики Bot Area і Sum.
- [neonnoodles.com](http://neonnoodles.com) — сайт і платформи.
- [itch.io: Neon Noodles](https://vividhelix.itch.io/neon-noodles) — запис власного вводу й правка.
- [Gamespace: превʼю](https://gamespace.com/featured/neon-noodles-pc-hands-on-preview-too-early-to-feast/) — етапи рівня, загальні команди, звʼязування ботів, графік порівняння.
- [Nintendo eShop](https://www.nintendo.com/us/store/products/neon-noodles-switch/) — Switch-версія.
- YouTube: пошук «Neon Noodles gameplay».

## Непевне
- (?) Bot Area: площа, яку займають чи проходять боти, — з назви й знімків (1 для бота, що стоїть на місці); формула Sum (сума трьох?) не перевірена.
- (?) Що саме роблять клавіші E, R, F, G, T і універсальна дія `*` на таймлайні (запуск станції?) — з іконок, без джерела.
- (?) Чи звичайний бот завжди стоїть на місці й лише повертається — висновок з одного знімка.
- (?) Станції-телепорти парні чи мережа; як саме конвеєр «фільтрує».
- (?) Що відбувається при зіткненні дронів — краш чи блок; патчі кажуть лише про виправлення зіткнень.
- (?) Метрику staleness (скільки їжа лежить відкрито) обговорювали в беті; у релізі її нема серед чотирьох.
- (?) Кількість рівнів і звʼязок «5 локацій» із розділами I–VII.
