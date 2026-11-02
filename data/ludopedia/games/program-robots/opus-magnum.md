---
title: Opus Magnum
slug: opus-magnum
family: program-robots
also: [build-sim, thinky]
klass: cursor
axes:
  field: hex
  time: programmed
  opponent: none
  info: full
  random: none
  goal: state
year: 2017
platforms: [PC, Mac, Linux, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Opus_Magnum_(video_game)", best: true, note: "ядро: руки на гекс-сітці, гліфи, зіткнення зупиняють, метрики cost/cycles/area, GIF, Workshop"}
  - {kind: official, url: "https://www.zachtronics.com/opus-magnum/", note: "сайт Zachtronics: фічі, редактор пазлів, Sigmar's Garden"}
  - {kind: steam, url: "https://store.steampowered.com/app/558990/Opus_Magnum/", note: "Steam: Van Berlo's wheel, Glyph of Animismus, Journal of Alchemical Engineering"}
  - {kind: steam, url: "https://store.steampowered.com/app/3107410/Opus_Magnum_De_Re_Metallica/", note: "DLC De Re Metallica (2026)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=opus+magnum+zachtronics+gameplay", note: "пошук; геймплей і GIF-розвʼязки"}
stage: v1
coverage: 65
mechanics: [multi-cell-size, stick-together, cell-transform, drag-drop-piece, hover-highlight, sequential-levels, level-unlock, level-select, in-game-editor, editor-playtest, level-exchange, replay, leaderboard, game-screen, end-screen, help-window, +swarm-separate-programs, +instruction-timeline, +arm-grab-rotate, +piston-extend, +track-path, +glyph-transform, +bond-unbond, +molecule-match-output, +input-respawn, +collision-halt, +solution-metrics, +metric-histograms, +gif-export, +step-execution, +code-editor-window, +solitaire-minigame]
proposes: ["+trigger:exec(cmd)", "+trigger:cycle_end", "+trigger:enter", "+cond:free", "+cond:held(a, kind|value)", "+effect:grab", "+effect:release", "+effect:rotate", "+effect:extend", "+effect:attach", "+effect:detach", "+effect:transform", "+effect:crash", "+role:resource", "+role:terrain", "+window:code-editor", "+window:metric-histograms", "+window:journal", "+ui:instruction-timeline", "+ui:instruction-highlight", "+ui:metric-panel", "+feature:solution-metrics", "+feature:gif-export", "+feature:workshop", "+axis:control", "+axis:actors"]
author: opus
date: 2026-11-02
---

# Opus Magnum — алхімічна машина з механічних рук на гекс-сітці, оптимізована за ціною, тактами й площею

## Суть
Гравець будує на гексагональній сітці машину з механічних рук, рейок і **гліфів** (клітин-трансмутаторів), щоб із вхідних реагентів-атомів зібрати молекулу-продукт і подати її на вихід. Кожна рука має власний рядок інструкцій на спільній часовій шкалі (захопити, повернути, висунути, відпустити…), усі руки працюють одночасно й циклічно. Розвʼязків безліч; після проходження гра показує **гістограми** трьох метрик (ціна, такти, площа) серед інших гравців — справжня гра починається з оптимізації.

## Поле і час
- Гекс-сітка, нескінченна (?) у межах робочої зони; реагенти/продукти — фіксовані багатоклітинні фігури на полі.
- Шари: підлога-гліфи й рейки (знизу) · атоми й молекули (зверху) · руки (основа + захват на відстані 1–3 гекси).
- Час `programmed`: такт (cycle) — кожна рука виконує одну інструкцію своєї доріжки; програма повторюється, доки не здано потрібну кількість продуктів.
- Детермінізм повний; зіткнення або неможлива дія — машина зупиняється з позначкою місця.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Рука (arm) | player | основа, довжина 1–3, 1 захват | обертається навколо основи, хапає/відпускає атом |
| Бі-/три-/гекса-рука | player | 2/3/6 захватів | як рука, кілька захватів одночасно |
| Поршнева рука | player | змінна довжина | `extend`/`retract` змінює довжину |
| Рейка (track) | terrain | шлях з гексів | основа руки їде вздовж рейки (+/−) |
| Колесо Ван Берло | player | 6 стихій по колу | обертається; працює з гліфом дублювання (?) |
| Вхід (reagent) | spawner | молекула-шаблон | щойно місце вільне — зʼявляється нова копія |
| Вихід (product) | static | молекула-шаблон, квота (зазвичай 6) | приймає молекулу, що точно збігається, зараховує |
| Атом | object | елемент | рухається лише з рукою; звʼязаний — разом з молекулою |
| Звʼязок | mark | — | склеює два сусідні атоми в молекулу |
| Гліф звʼязування (bonding) | terrain | 2 гекси | атоми на обох гексах звʼязуються |
| Гліф розвʼязування (unbonding) | terrain | 2 гекси | звʼязок між атомами на ньому розривається |
| Гліф кальцинації (calcification) | terrain | 1 гекс | стихія (повітря/земля/вогонь/вода) → сіль |
| Гліф проєкції (projection) | terrain | 2 гекси | ртуть + метал → метал вищого ступеня, ртуть зникає |
| Гліф очищення (purification) | terrain | 3 гекси (?) | два однакові метали → один вищого ступеня |
| Гліф дублювання (duplication) | terrain | 2 гекси (?) | сіль копіює стихію сусіднього атома (?) |
| Гліф анімізму (animismus) | terrain | 4 гекси (?) | дві солі → vitae + mors |
| Гліф утилізації (disposal) | terrain | — | знищує атом (?) |
| Гліфи пізніх розділів: multi-bond, triplex, unification, dispersion | terrain | — | множинні звʼязки; 4 стихії ↔ квінтесенція (?) |
| Елементи | — | сіль; повітря, земля, вогонь, вода; ртуть; свинець→олово→залізо→мідь→срібло→золото; vitae, mors; квінтесенція (?) | матеріал реакцій |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `exec(grab)` → ЯКЩО `occupied(gripper, atom)` → ТО `grab(atom)` (тримається вся звʼязана молекула).
- КОЛИ `exec(drop)` → ТО `release(molecule)`.
- КОЛИ `exec(rotate cw|ccw)` → ТО `rotate(arm, ±60°)`; утримувана молекула описує дугу навколо основи.
- КОЛИ `exec(pivot cw|ccw)` → ТО `rotate(molecule, ±60°)` навколо захвату (?).
- КОЛИ `exec(extend|retract)` → ЯКЩО рука поршнева → ТО довжина ±1.
- КОЛИ `exec(track +|−)` → ТО `move(arm_base, along_track)`.
- КОЛИ `exec(reset)` → ТО рука повертається у стартову позу (?); `exec(repeat)` → ТО повтор попередньої послідовності (?).
- КОЛИ `custom: «кінець такту»` → ЯКЩО атоми на обох гексах гліфа звʼязування → ТО `attach(a, b)`; гліф розвʼязування → `detach(a, b)`.
- КОЛИ `custom: «кінець такту»` → ЯКЩО стихія на гліфі кальцинації → ТО `transform(atom, salt)`.
- КОЛИ `custom: «кінець такту»` → ЯКЩО ртуть і метал на гліфі проєкції → ТО `transform(metal, next_metal)`, `disappear(quicksilver)`.
- КОЛИ `custom: «кінець такту»` → ЯКЩО два однакові метали на гліфі очищення → ТО `spawn(next_metal)` на вихідному гексі, обидва зникають (?).
- КОЛИ `custom: «дві частини машини в одній клітині»` → ТО `crash` — машина зупиняється, місце підсвічено.
- КОЛИ `custom: «на вході вільне місце»` → ТО `spawn(reagent)`.
- КОЛИ `custom: «на виході молекула з точним збігом атомів і звʼязків»` → ТО `disappear`, `counter(produced, +1)`.
- КОЛИ `counter(produced, ==, quota)` → ТО `win`, показати метрики й гістограми.
- Перемога: квота продуктів (зазвичай 6) · Поразка: нема — зіткнення лише зупиняє симуляцію · Рахунок: **Cost** (золото за деталі), **Cycles** (такти до квоти), **Area** (гекси, яких торкалась машина); неофіційно — «sum».

## Керування і ввід
- Палітра деталей (руки, рейки, гліфи) → drag на гекс; поворот деталі (колесо/клавіші); правка рейки малюванням.
- Часова шкала знизу: рядок на кожну руку, клітина = такт; перетягування інструкцій з палітри; клавіатурні скорочення для інструкцій (?).
- Програми можна копіювати й зсувати блоками; позначка початку циклу (?).
- Запуск: Play, Step (один такт), Fast/Fastest, Stop → повернення до розстановки.

## Вікна, меню, HUD
- `level-select` — «журнал»/книга розділів з пазлами; після розділу відкривається наступний.
- `game-screen`: гекс-поле; `tool-palette` деталей зліва; `instruction-timeline` знизу; `objective-text` (реагенти → продукт, квота); `metric-panel` (cost, cycles, area поточної машини); кнопки Play/Step/Fast/Stop.
- `end-screen` + `metric-histograms`: три гістограми з позицією гравця серед друзів/усіх; кнопки «записати GIF», «далі».
- `replay-window` / запис: експорт анімованого GIF з безшовною петлею.
- `editor-window`: редактор пазлів для Steam Workshop (публікація з доведеним розвʼязком).
- `journal` (custom): «Journal of Alchemical Engineering» — добірка пазлів спільноти від Zachtronics.
- `dialogue-window` — сюжет (дім Ван Тассен) між пазлами; `codex-window` / `help-window` — довідник (?).
- `custom-window`: пасьянс Sigmar's Garden.
- `settings-window`: звук, графіка (?).
- Переходи: журнал → пазл → (Play) симуляція → (квота) гістограми → журнал; пазл → GIF; журнал → Sigmar's Garden.

## Фічі поза полем
- `solution-metrics` у трьох незалежних вимірах + гістограми спільноти — оптимізація як головна повторна гра.
- `leaderboard-online` / друзі; спільнота веде рекорди Парето-фронтів (?).
- `gif-export` — шеринг розвʼязку однією анімацією.
- `level-editor` + Workshop (`level-sharing`, `user-levels-browser`); Journal — кураторська добірка.
- `step-mode`, `speed-control`, кілька слотів розвʼязків на пазл (?).
- Пасьянс Sigmar's Garden (кожна роздача розвʼязна); DLC De Re Metallica (2026).

## Варіації й родичі
- Zachtronics: SpaceChem (вальдо на прямокутній сітці, реактори), Infinifactory, TIS-100, Shenzhen I/O, Exapunks; Zach-like як жанр.
- Родичі: Manufactoria (просторова програма), 7 Billion Humans (паралельні актори, метрики), Factorio (маніпулятори).
- Осі варіацій: **програма** (спільна на всіх / окрема доріжка на руку); **поле** (квадрат / гекс); **метрики** (1 / 2 / 3 + гістограми); **трансформація** (клітини-гліфи / вузли-реактори); **помилка** (крах / тиха).

## Цікавинки для курсу
- Синхронна симуляція кількох акторів з окремими доріжками інструкцій і виявленням зіткнень — 🥇.
- Обертання молекули навколо основи руки на гекс-сітці (кубічні координати) — 🥈.
- Гліфи як таблиця «рецептів» клітин, що перевіряються наприкінці такту — 🥉.
- Звʼязки атомів: граф молекули, рух як ціле, звірка з шаблоном з точністю до положення — 🥈.
- Три метрики + гістограма розподілу розвʼязків — 📎 (дані) / 🥉 (з графіком).
- Експорт анімації рішення в GIF — 🥉.

## Мапа на каталог
- Є: `multi-cell-size` (молекули) · `stick-together` (звʼязки) · `cell-transform` (гліфи) · `drag-drop-piece` · `hover-highlight` · `sequential-levels` / `level-unlock` / `level-select` (розділи) · `in-game-editor` / `editor-playtest` / `level-exchange` (Workshop) · `replay` (GIF) · `leaderboard` · `game-screen` · `end-screen` · `help-window`.
- **Нема** → пропозиції карток:
  - `+swarm-separate-programs` «Кілька акторів з власними доріжками в спільному такті» · entities/move · 🥇.
  - `+instruction-timeline` «Програма як таймлайн тактів» · interface/input · 🥈.
  - `+arm-grab-rotate` · entities/interact · 🥉; `+piston-extend` · entities/move · 📎; `+track-path` · entities/move · 📎.
  - `+glyph-transform` «Клітина-рецепт перетворює атоми» · entities/interact · 🥉 · слот {recipe}.
  - `+bond-unbond` «Склеювання/розклеювання сусідів» · entities/interact · 🥉.
  - `+molecule-match-output` «Вихід приймає точну фігуру» · game-logic/win · 🥉.
  - `+input-respawn` «Джерело відновлюється, коли вільне» · entities/spawn · 🌱.
  - `+collision-halt` «Зіткнення зупиняє симуляцію» · game-logic · 📎.
  - `+solution-metrics` · 📎; `+metric-histograms` «Гістограма метрик спільноти» · interface/results · 🥉; `+gif-export` · interface/results · 🥉.
  - `+step-execution` · 🥉; `+code-editor-window` · 🥉; `+solitaire-minigame` · 🥉.

## Пропозиції до словників
- `+trigger:exec(cmd)`; `+trigger:cycle_end` — точка, де спрацьовують гліфи й перевіряються виходи.
- `+effect:grab` / `+effect:release` — тримання обʼєкта маніпулятором (ширше за `pickup`); `+effect:extend`; `+effect:attach`/`+effect:detach` (⏳ є — вживати); `+effect:crash`.
- `+role:resource` (атом), `+role:terrain` (гліф, рейка).
- `+window:code-editor`, `+window:metric-histograms`, `+window:journal`.
- `+ui:instruction-timeline`, `+ui:instruction-highlight`, `+ui:metric-panel`.
- `+feature:solution-metrics`, `+feature:gif-export`, `+feature:workshop`.
- `+axis:control` = `programmed`; `+axis:actors` = `party` (кілька рук, кожна зі своєю програмою).

## Джерела
- ⭐ [Wikipedia: Opus Magnum](https://en.wikipedia.org/wiki/Opus_Magnum_(video_game)) — руки, інструкції, гліфи bonding/calcification/projection, зіткнення зупиняють, cost/cycles/area, GIF, Workshop.
- [Zachtronics: Opus Magnum](https://www.zachtronics.com/opus-magnum/) — фічі, редактор, Sigmar's Garden.
- [Steam](https://store.steampowered.com/app/558990/Opus_Magnum/) — Van Berlo's wheel, Glyph of Animismus, Journal of Alchemical Engineering.
- [Steam: De Re Metallica](https://store.steampowered.com/app/3107410/Opus_Magnum_De_Re_Metallica/) — DLC.
- YouTube: пошук «opus magnum zachtronics gameplay».

## Непевне
- (?) Фан-вікі (402), StrategyWiki (403), Thinky Games (403) недоступні; повний список гліфів (purification, duplication, animismus, disposal, multi-bond, triplex, unification, dispersion), їхні розміри й точна семантика — з памʼяті.
- (?) Набір інструкцій (pivot, reset, repeat, no-op), клавіші — з памʼяті.
- (?) Гістограми після розвʼязку — з памʼяті (офіційні сторінки кажуть лише «змагайтесь з друзями й світом»).
- (?) Чи вихід приймає молекулу в будь-якій орієнтації — ймовірно, лише точну позицію шаблону.
- (?) Колесо Ван Берло: точна роль у дублюванні — з памʼяті.
