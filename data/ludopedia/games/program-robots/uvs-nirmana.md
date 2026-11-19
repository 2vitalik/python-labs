---
title: U.V.S. Nirmana
slug: uvs-nirmana
aka: [UVS Nirmana, Unreturning Void Ship Nirmana]
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
year: 2026
platforms: [PC, Mac, Linux]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/2536720/UVS_Nirmana/", best: true, note: "Coincidence (Зак Барт) / Klei Publishing, 04.05.2026: мережі труб несуть енергію від vega drive, поведінку задає матриця керування, мета — мінімізувати flux; 30 пазлів, 12 інструментів, власні пазли, гістограми й таблиці, пасьянс Eternal Solitaire за мотивами оваре; знімки: палітра PIPE / SENSE / VALVE / MUX / DEMUX / RELAY / DRIVER, матриця під полем, ряди IN / OUT, WIDTH / HEIGHT / FLUX"}
  - {kind: official, url: "https://coincidence.games/uvs-nirmana/", note: "сайт студії: «an engineering puzzle game about conduits and the energies that flow through them»; автори"}
  - {kind: other, url: "https://www.gamingonlinux.com/2026/05/engineering-puzzle-game-u-v-s-nirmana-arrives-from-the-zachtronics-team-at-coincidence/", note: "новина: труби, матриця керування, flux, 30 пазлів, власні пазли після кампанії"}
  - {kind: other, url: "https://signaldecay.substack.com/p/uvs-nirmana", note: "відгук: входи ліворуч, виходи праворуч, сенсор керує потоком однієї труби за потоком іншої, нижня панель — реакції елементів на потік, «physical programming, building logic gates»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=U.V.S.+Nirmana+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 40
mechanics: [cell-click, drag-drop-piece, cursor-place, pipe-connectors, step-execution, sequential-levels, level-select, leaderboard, save-multi-slot, in-game-editor, level-exchange, game-settings, help-window, game-screen, +flow-propagation, +io-test-streams, +signal-matrix, +sensor-signal-wire, +flow-valve, +mux-demux-routing, +color-mixing, +expected-output-diff, +special-tools-per-level, +solution-metrics, +metric-histograms, +gif-export, +solitaire-minigame, +sowing]
proposes: ["+trigger:signal(row)", "+cond:signal(row)", "+cond:flow(pipe, color)", "+effect:route(flow, port)", "+effect:mix(a, b)", "+role:sensor", "+role:device", "+window:control-matrix", "+ui:io-timeline", "+ui:show-expected", "+feature:custom-puzzles", "+axis:signal"]
author: opus
date: 2026-11-19
---

# U.V.S. Nirmana — труби з кольоровими потоками енергії на сітці, а під ними — матриця керування, що вмикає клапани й перемикачі за сигналами сенсорів

## Суть
Інженерний Zach-like від Coincidence (Зак Барт, автори Kaizen; видавець Klei): корабель-монастир U.V.S. Nirmana летить до краю всесвіту й допомагає цивілізаціям. Кожен пазл — порожнє поле з іменованими входами енергії ліворуч і виходами праворуч; гравець будує між ними мережу з труб, сенсорів, клапанів і мультиплексорів. Потоки на входах змінюються в часі, і виходи мають видати еталонні ряди. Керування винесене в окрему **матрицю** під полем: стовпчик кожної деталі перетинається з рядками-сигналами, а реле й драйвери на перетинах вирішують, хто чим керує. Огляд називає це «фізичним програмуванням, складанням логічних вентилів». Метрики — ширина, висота й flux; у грі ще є пасьянс Eternal Solitaire.

## Поле і час
- Поле — квадратна сітка (на знімках приблизно 13 × 7 клітин); порти-підписи входів на лівому краї, виходів — на правому; деталі займають кілька клітин, зʼєднання між портами йдуть «кабелями» з кольоровим потоком.
- Під полем — матриця керування: стовпчики продовжують стовпчики поля (від кожної деталі вниз іде лінія), рядки — сигнали; частина рядків має назви вхідних сигналів (AMEN, SVAHA), решта вільні.
- Праворуч — ряди IN і OUT у часі: кожен вхід і вихід — вертикальна смуга кольорових відрізків, горизонтальна лінія показує поточний тік.
- Час `programmed`: розставляєш у спокої, PLAY / STEP проганяють цикл тіків; гравці пишуть про «останній тік циклу».
- Детерміновано; випадковості в пазлах нема.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вхід енергії (DEXTRO, LEVO, WORDS, WEALTH, FAME, POWER, FORM, MIND…) | source | назва, колір, ряд у часі | щотіку подає потік свого кольору або нічого — за розкладом IN |
| Вихід (DOSE, FORM, MIND, WEALTH…) | sink | еталонний ряд | приймає потік; ряд звіряють з еталоном (OUT, Show Expected) |
| Сигнальний вхід (рядки AMEN, SVAHA…) | source | ряд у часі | подає сигнал у свій рядок матриці |
| PIPE | conduit | відрізок | проводить потік |
| SENSE | switch | — | бачить потік у своїй трубі й дає сигнал у матрицю |
| VALVE | gate | відкритий / закритий | за сигналом пропускає або перекриває потік |
| MUX | switch | кілька входів → вихід | сигнал вибирає вхід (?) |
| DEMUX | switch | вхід → кілька виходів | сигнал вибирає вихід; без сигналу закритий (гайд: «сенсор тримає demux закритим») |
| RELAY ◇ | mark | клітина матриці | (?) переносить сигнал зі стовпчика деталі в рядок |
| DRIVER ◆ | mark | клітина матриці | (?) подає сигнал рядка на деталь свого стовпчика |
| Спецінструменти (MIXER, GREEN, BUFFER, NEGATE; YELLOW — для власних пазлів) | switch | 1–2 на пазл | на знімках: MIXER з виходом MIXED, GREEN — сенсор кольору, BUFFER з лічильником «0000», NEGATE у пазлі «Negated Civilization» |
| Перемикач ↕ біля деталі | mark | — | (?) віддзеркалює деталь |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(drag, tool)` → ЯКЩО `free(cells)` → ТО `place(player, tool)`; від деталі вниз іде лінія її стовпчика в матриці.
- КОЛИ `input(click, matrix_cell)` → ТО `place(player, relay|driver)` на перетині рядка й стовпчика.
- КОЛИ `input(play|step)` → ТО щотіку `custom: «кожен вхід подає наступне значення свого ряду»`.
- КОЛИ `tick` → ТО `custom: «потік іде трубами й деталями від входу до виходу»`.
- КОЛИ `custom: «через сенсор іде потік»` → ТО `custom: «сенсор дає сигнал»`; через матрицю сигнал доходить до деталі в іншому стовпчику («матриця зʼєднує інструменти з різних стовпчиків» — транскрипт відео).
- КОЛИ `custom: «на клапан приходить сигнал»` → ТО `set_state(valve, open|closed)` — клапан вирішує, чи пропускає труба потік.
- КОЛИ `custom: «на MUX / DEMUX приходить сигнал»` → ТО `custom: «перемкнути активний вхід чи вихід»` (?).
- КОЛИ `custom: «два потоки сходяться в MIXER»` → ТО `merge(a, b → mixed)` (?).
- КОЛИ `custom: «цикл тіків скінчився»` → ЯКЩО `custom: «ряд на кожному виході = еталонному»` → ТО `win`, метрики й гістограми; інакше розбіжність видно в стовпчиках OUT і за кнопкою Show Expected.
- Бонусні місії (червень 2026): `custom: «відновити плин часу»`, `custom: «аномалія псує сигнали матриці»`.
- Перемога: усі виходи видали еталонні ряди · Поразка: нема — розбіжність показано, правиш схему · Рахунок: WIDTH і HEIGHT — розміри побудови в клітинах (?), FLUX — третя метрика, яку гра просить мінімізувати; гравці записують рішення як «ширина / висота / flux» (напр. 1/2/0 у першому пазлі, 10/11/2 у Z0 Yani).

Eternal Solitaire (за мотивами оваре; правила з гайду гравця):
- КОЛИ `input(click, pit)` → ЯКЩО `count(seeds_in_pit, >, 0)` → ТО `custom: «посіяти всі насінини по одній за годинниковою стрілкою; понад 12 — нове коло, і порожня лунка теж отримує»`.
- КОЛИ `custom: «остання насінина зробила в лунці 2 або 3»` → ТО `score(n)`, `clear(pit)`; далі каскад проти годинникової: кожна суміжна лунка з 2 або 3 → `score(n²)`, `clear`; каскад обривається на першій іншій лунці.
- КОЛИ `custom: «хід без очок»` → ЯКЩО `state(player, peril)` → ТО `lose`; інакше `set_state(player, peril)`; хід з очками → `clear_state(player, peril)`.
- Мета — очистити кільце з найбільшим рахунком; одинока насінина не береться ніколи.

## Керування і ввід
- Миша (є режим «лише миша») і дотик на Windows: перетягнути інструмент з палітри на поле, клік по клітині матриці — реле чи драйвер.
- Вирізати / копіювати / вставляти рішення, зокрема між слотами дизайну (оновлення 08.05.2026).
- PLAY, PAUSE / STEP, STOP; Show Expected; ≡ — меню, ? — довідка.
- Приховане налаштування в config.cfg — назви кольорів у підказках над трубами й сигналами.

## Вікна, меню, HUD
- `game-screen`: ліворуч `tool-palette` — PIPE, SENSE, VALVE, MUX, DEMUX, 1–2 спецінструменти, нижче RELAY і DRIVER; посередині поле з портами-підписами; під ним `custom: «матриця керування»`; праворуч назва й місце пазла («J9 TAKKA — INFECTED TRANSFER STATION»), `custom: «стовпчики IN / OUT у часі з курсором тіку»`, кнопка SHOW EXPECTED, `custom: «WIDTH / HEIGHT / FLUX»`, PLAY / PAUSE або STEP / STOP.
- `level-select` — «місток» корабля: іконки місій, наведення на розвʼязану показує гістограми й таблиці (14.05.2026); у дзвони мостика можна дзвонити.
- `dialogue-window` — брифінги з медитаціями («When antimemes are made to observe themselves…»), сцени з ченцями-ренунціантами на тлі світів.
- `editor-window` — редактор місій: брифінги, до 6 спецінструментів, вставка пазла з буфера.
- `custom-window` Eternal Solitaire — кільце з 12 лунок, SCORE у центрі, спливні «+4 / +3», WIN COUNT, HIGH SCORE, NEW GAME, сувій INSTRUCTIONS.
- `settings-window` — кольорові альтернативи, окрема гучність, лише миша.
- Переходи: місток → пазл (брифінг) → game-screen → PLAY → збіг → гістограми → місток; місток → пасьянс.

## Фічі поза полем
- 30 пазлів кампанії (4–6 годин) + 10 бонусних місій (11.06.2026, досягнення «Vajra Cakravartin»).
- `level-editor` і `level-sharing`: власні пазли після кампанії — «створи й подивись, як інші розвʼяжуть».
- `leaderboard-online` + гістограми рішень; експорт анімованого GIF (25.05.2026).
- Слоти дизайнів на пазл із буфером вирізати / копіювати / вставити.
- `colorblind-palette` (Color Alternatives), лише миша, гра без таймінгу, збереження будь-коли; 9 мов з повною озвучкою.
- Пасьянс Eternal Solitaire з лічильником перемог і рекордом.

## Варіації й родичі
- [kaizen-a-factory-story](kaizen-a-factory-story.md) — попередня гра студії: метрики, гістограми, GIF, пасьянс-мінігра.
- [opus-magnum](opus-magnum.md), [spacechem](spacechem.md), [tis-100](tis-100.md) — Zach-like лінія тих самих авторів.
- [infinifactory](infinifactory.md) — сенсори й сигнальні дроти на тому ж полі; [factorio-circuit-network](factorio-circuit-network.md) — сигнали керують машинами.
- [pipe-mania](../connect-rotate/pipe-mania.md) — труби й потік без керування; [oware](../chess-abstract/oware.md) — прототип пасьянсу.
- Осі варіацій: **де живе керування** (окрема матриця під полем / дроти на тому ж полі / код); **що тече** (кольорові потоки / предмети / числа); **перевірка** (ряд у часі / квота предметів / таблиця істинності).

## Цікавинки для курсу
- Покрокова симуляція кольорових потоків трубами з клапанами й мультиплексорами — 🥈.
- Матриця керування «рядки-сигнали × стовпчики-деталі» з реле й драйверами на перетинах — 🥉: окремий шар керування від шару «сантехніки».
- Ряди входів і виходів у часі та порівняння з еталоном — 📎.
- Метрики ширина / висота / flux і гістограми — 📎.
- Eternal Solitaire: сівба по кільцю, каскад із квадратами, правило двох порожніх ходів — 🥉; пошук найкращої партії — 🥇.

## Мапа на каталог
- Є: `cell-click` · `drag-drop-piece` / `cursor-place` ↔ розстановка деталей · `pipe-connectors` ↔ порти труб і деталей · `step-execution` ↔ PLAY / STEP / STOP · `sequential-levels` / `level-select` ↔ місток · `leaderboard` · `save-multi-slot` ↔ слоти дизайнів · `in-game-editor` / `level-exchange` ↔ власні пазли · `game-settings` ↔ доступність · `help-window` ↔ ? · `game-screen`.
- **Нема** → пропозиції карток:
  - `+signal-matrix` «Матриця керування: рядки-сигнали × стовпчики-деталі» · game-logic/program · 🥉 · слоти {rows, cells: relay|driver}.
  - `+flow-valve` «Клапан пропускає потік за сигналом» · entities/interact · 📎.
  - `+mux-demux-routing` «Перемикач входу чи виходу за сигналом» · entities/interact · 📎.
  - `+expected-output-diff` «Ряд виходу поруч з еталоном» · interface/hud · 📎.
  - `+special-tools-per-level` «1–2 особливі інструменти пазла» · levels · 🌱.
  - Повтори: `+flow-propagation` (Pipe Mania), `+io-test-streams`, `+sensor-signal-wire` (Infinifactory), `+color-mixing`, `+solution-metrics`, `+metric-histograms`, `+gif-export`, `+solitaire-minigame`, `+sowing` (оваре).

## Пропозиції до словників
- `+trigger:signal(row)` — у рядку матриці зʼявився або зник сигнал; `+cond:signal(row)` — рядок під сигналом.
- `+cond:flow(pipe, color)` — трубою йде потік кольору.
- `+effect:route(flow, port)` — спрямувати потік у порт (DEMUX); `+effect:mix(a, b)` — змішати потоки (MIXER).
- `+role:sensor` — деталь, що читає потік і дає сигнал; `+role:device` — деталь з портами (MUX, DEMUX, BUFFER).
- `+window:control-matrix` — нижня панель керування під полем.
- `+ui:io-timeline` — стовпчики IN / OUT у часі з курсором тіку; `+ui:show-expected` — кнопка показу еталона.
- `+feature:custom-puzzles` — власні пазли з брифінгом і набором спецінструментів.
- `+axis:signal` — сигнал керування окремим шаром (матриця), а не дротами на полі.

## Джерела
- ⭐ [Steam: U.V.S. Nirmana](https://store.steampowered.com/app/2536720/UVS_Nirmana/) — опис (труби, vega drive, матриця керування, flux, 30 пазлів, 12 інструментів, власні пазли, Eternal Solitaire, гістограми), категорії доступності; 7 знімків: пазли J9 Takka, N2 Kurana, Tamra Occidens, Kamarupa з палітрою, матрицею, рядами IN / OUT і метриками; пасьянс.
- Steam News (ISteamNews API, 17 записів, квітень–червень 2026) — жовтий сенсор кольору, гістограми на містку, GIF, вирізати / копіювати / вставити, слоти дизайнів, бонусні місії, назви кольорів у config.cfg.
- [Coincidence: U.V.S. Nirmana](https://coincidence.games/uvs-nirmana/) — опис і автори (Зак Барт — дизайн і код).
- [GamingOnLinux](https://www.gamingonlinux.com/2026/05/engineering-puzzle-game-u-v-s-nirmana-arrives-from-the-zachtronics-team-at-coincidence/) — новина й коментарі гравців.
- [Signal Decay](https://signaldecay.substack.com/p/uvs-nirmana) — враження від механіки, брифінги, міні-гра манкала.
- Гайди Steam: «WIP — Minimum Solutions» (нотація ширина / висота / flux і значення по пазлах), «All Solutions» (коментар про сенсор і demux, «останній тік циклу»), «Eternal Solitaire Analysis» (правила пасьянсу); сторінки позначені як приховані.
- Результат пошуку з транскриптом відео «I Played The New ZACHTRONICS Game»: «клапан визначає, чи пропускає труба вміст», «матриця зʼєднує інструменти з різних стовпчиків».
- YouTube: пошук «U.V.S. Nirmana gameplay».

## Непевне
- (?) Точна роль RELAY і DRIVER: зі знімків — реле (◇) пише сигнал стовпчика в рядок, драйвер (◆) віддає сигнал рядка деталі свого стовпчика; текстом це ніде не підтверджено.
- (?) Що саме рахує FLUX (кількість перемикань? «зайвий» потік?) — гра лише просить його мінімізувати; WIDTH / HEIGHT як рамка побудови — з назв і нотації гравців.
- (?) Поведінка MUX, MIXER, BUFFER, NEGATE, GREEN — з назв і вигляду на знімках; повний список 12 інструментів не бачив.
- (?) Що означають червоний хрест на полі й кнопки ↕ біля деталей.
- (?) Як у пасьянсі розкладено 50 насінин на старті — випадково чи фіксовано (гайд вважає будь-який розклад допустимим).
- (?) Черга описує матрицю як «керування сигналами в часі»; на знімках матриця — просторова сітка звʼязків, а час живе в рядах IN / OUT.
