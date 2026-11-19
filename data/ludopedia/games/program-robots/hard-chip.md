---
title: Hard Chip
slug: hard-chip
aka: []
family: program-robots
also: [build-sim]
klass: cursor
axes:
  field: 3d
  time: programmed
  opponent: none
  info: full
  random: none
  goal: constraints
year: 2024
platforms: [PC]
links:
  - {kind: official, url: "https://hardchip.io/", best: true, note: "суть за хвилину: транзистори й дроти руками, сигнал іде з затримкою, метрики ticks / volume / blocks / MOS, кампанія 2 з 8 розділів, gauntlets, sandbox, галерея; лінки на вікі й live demo"}
  - {kind: steam, url: "https://store.steampowered.com/app/2844290/Hard_Chip/", note: "Elorth, ранній доступ з 22.11.2024: від транзистора до NAND/NOR, компонентів і 8-бітного ALU; «Every wire has length. Every gate has delay.»"}
  - {kind: wiki, url: "https://hardchip.wiki.gg/wiki/Mechanics", note: "сигнали 0 / 1 / нейтральний, поширення щотіку, тест-вектори й стабільність, коротке замикання, плаваючий затвор, фаза PWR"}
  - {kind: wiki, url: "https://hardchip.wiki.gg/wiki/Blocks", note: "Substrate, Metal (траси й via), Zero/One, Input, NMOS/PMOS: wells-channel-gate, затримки 3 і 4 тіки; Clock, Boot Clear, Puller"}
  - {kind: wiki, url: "https://hardchip.wiki.gg/wiki/Grades", note: "4 метрики blocks / volume / ticks / MOS, 5 оцінок, пороги 1.3× і 0.9×, Masterpiece"}
  - {kind: wiki, url: "https://hardchip.wiki.gg/wiki/Component_Editor", note: "панелі, режими Edit / Select / Delete / Blueprints / Probes / Toolbox, гарячі клавіші, 5 слотів, координати кристала"}
  - {kind: wiki, url: "https://hardchip.wiki.gg/wiki/Labels", note: "мітки входів і виходів Bit / Value, проби до 32 біт з точкою зупинки"}
  - {kind: wiki, url: "https://hardchip.wiki.gg/wiki/Campaign", note: "розділ 1: термінали status → modelchip → fabricate → reboot; Bypass, Inverter, Adder, ALU"}
  - {kind: youtube, url: "https://www.youtube.com/channel/UCm1uoPjHeGYf6sYXE2k--DQ", note: "канал розробника: девлоги й розбори схем (лінк з hardchip.io)"}
stage: v1
coverage: 70
mechanics: [cell-click, multi-select, editor-draw-tools, undo-redo, step-execution, save-multi-slot, save-autosave, sequential-levels, level-unlock, level-select, leaderboard, game-screen, tutorial-window, player-camera, keyboard-controls, controls-remap, language-picker, +signal-propagation, +transistor-crossing, +layer-via, +edge-io-pins, +io-test-streams, +propagation-delay, +short-circuit-error, +floating-gate-decay, +stable-state-check, +solution-metrics, +metric-grades, +blueprints, +probe-breakpoint, +sandbox-mode, +clock-source, +power-up-phase, +terminal-commands, +reference-schematic, +weekly-gauntlet, +auto-resize-die]
proposes: ["+trigger:signal(net)", "+trigger:short(net)", "+cond:signal(net, v)", "+effect:power(net, v)", "+role:pin", "+window:truth-table", "+window:schematic", "+window:terminal", "+ui:probe-overlay", "+ui:die-size", "+feature:metric-grades", "+feature:weekly-gauntlet", "+feature:breakpoint", "+axis:signal"]
author: opus
date: 2026-11-19
---

# Hard Chip — процесор з окремих транзисторів на 3D-сітці кристала, де кожна клітина дроту — це тік затримки

## Суть
Гравець проєктує мікросхеми «знизу вгору»: кладе на воксельний кристал металеві доріжки й складає з блоків NMOS і PMOS транзистори, з них — NAND, NOR, суматор, а наприкінці розділу 1 — 8-бітне ALU. Готових вентилів нема: «No abstraction layers. No drag-and-drop logic blocks». Сигнал іде провідником по одній клітині за тік, а транзистор вмикається з затримкою, тому довгий дріт і зайвий каскад прямо погіршують метрику тіків. Стадію перевіряє таблиця істинності: виходи мають збігтись і схема має стабілізуватись. Навколо — сюжетний 3D-комплекс з мертвими терміналами: «You are new_user, trapped».

## Поле і час
- Кристал (die) — воксельна сітка X×Y×Z (ширина × висота × глибина), напр. «14 x 9 x 9»; шар Y = 0 — непровідний субстрат. Будівництво за межами розширює кристал, після валідації він стискається до мінімуму (вимикається в Toolbox).
- Сторони: мітки входів лише ліворуч, виходів — праворуч, обидві на рівні субстрату; константи Zero (висота 6) і One (висота 8) стоять у кутку X = 0, Z = 0.
- Час `programmed`: схема статична, симуляція йде тіками (за замовчуванням 25 тіків/с); є пуск, пауза, крок на тік, швидкість і скидання.
- Детермінізм повний; випадковості нема.
- Мета-шар кампанії — 3D-комплекс з машинами й терміналами (стазис-камера, Generator, Workstation, Fabricator, банки матеріалів).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Substrate | static | шар Y = 0 | непровідна основа, на ній будують |
| Metal | conduit | 1 клітина | провідник: траси на субстраті, стовпчик угору — via; повністю займає клітину |
| Zero | source | висота 6, кут (0, 0) | завжди 0 (синій, «земля») |
| One | source | висота 8, кут (0, 0) | завжди 1 (червоний, «живлення») |
| Input | source | керується міткою або пробою | подає сигнал тесту; ручна зміна зупиняє валідацію |
| NMOS | switch | 6 well + 3 channel + 3 gate на клітину вище, поперек каналу; 3 тіки | канал пропускає лише 0, коли на затворі 1 |
| PMOS | switch | та сама будова; 4 тіки | канал пропускає лише 1, коли на затворі 0 |
| Clock | source | період, шпаруватість (Clock Control) | коливається 0 ↔ 1; лише в Library |
| Boot Clear | source | слабкий 0 у фазі PWR | ініціалізує комірки памʼяті; сигнал 1 перекриває його без замикання |
| Puller | switch | 100 тіків (прибрано до релізу) | між двома сегментами: якщо один нейтральний, проводить після затримки |
| Мітка Input / Output | mark | Bit або Value (крок 2–5 клітин) | вхідна подає тест-вектор, вихідна читає блоки й порівнює |
| Проба | mark | 8 / 16 / 32 біти | показує ціле число, знак питання — якщо якийсь біт нейтральний; на Input — задає біти; може ставити паузу |
| Термінал | switch | машина, до якої підʼєднано | команди status, reboot, modelchip, fabricate, help, exit |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(click, cell)` → ЯКЩО `free(cell)` → ТО `place(player, block)`; ЯКЩО клітина поза кристалом → ТО `custom: «кристал розширюється»`.
- КОЛИ `input(hold_drag)` → ТО `place(player, metal)` лінією або «Г» між початком і кінцем (права кнопка чи LCtrl віддзеркалює «Г»; з LCtrl — угору).
- КОЛИ `input(alt_click)` → ТО `disappear(block)`; з рамкою — площина, з LCtrl — куб.
- КОЛИ `pattern(custom: «6 well + 3 channel + 3 gate поперек каналу на клітину вище»)` → ТО `spawn(mos)`; блоки MOS поза правильною фігурою — `custom: «блимає хрестик»`. Сусідні MOS одного типу можуть ділити блоки: кут (1), затвор (3 + 1), канал (3), канал і затвор (4 + 1).
- КОЛИ `tick` → ЯКЩО `custom: «сусідній провідний блок має 0 або 1»` → ТО `set_value(block, той самий)` — сигнал проходить одну клітину за тік.
- КОЛИ `tick` → ЯКЩО `not connected(segment, source)` → ТО `custom: «сегмент розряджається з кінців і поступово стає нейтральним»`.
- КОЛИ `contact(signal_0, signal_1)` → ТО `set_state(blocks, error)` — жовте коротке замикання, `counter(loss, +N)`; поки є замикання, валідація не йде.
- КОЛИ `state_on(gate_nmos, 1)` → ТО через 3 тіки `set_state(nmos, open)`: канал пропускає 0.
- КОЛИ `state_on(gate_pmos, 0)` → ТО через 4 тіки `set_state(pmos, open)`: канал пропускає 1.
- КОЛИ `custom: «затвор активного MOS набув протилежного значення»` → ТО `clear_state(mos, open)` без затримки.
- КОЛИ `custom: «затвор активного MOS став нейтральним»` → ТО через 100 тіків `clear_state(mos, open)`, `counter(float, +1)` — плаваючий затвор заважає стабільності.
- КОЛИ `timer(period)` → ТО `set_value(clock, протилежне)` (лише Library).
- КОЛИ `phase_start(PWR)` → ТО `custom: «константи поширюються, тіки не зараховуються»`; Boot Clear подає слабкий 0 (лише деякі стадії, напр. Memory Cells).
- КОЛИ `input(validate)` → ТО `custom: «рядки таблиці істинності по черзі подаються на мітки входів»`.
- КОЛИ `settled` → ЯКЩО `custom: «кожен вихід = очікуваному, рядки з any не перевіряються»` → ТО `counter(passed, +1)`, наступний рядок; інакше `custom: «тест провалено, валідацію зупинено»`.
- КОЛИ `input(edit)` під час валідації → ТО `custom: «валідацію зупинено й провалено»`; те саме при ручній зміні сигналу проби.
- КОЛИ `counter(passed, ==, rows)` → ТО `win`, `custom: «оцінки за 4 метриками»`, `next_level`; кристал стискається до мінімуму.
- КОЛИ `custom: «біт проби набув 0 / 1 / - / error»` → ЯКЩО `state(probe, stop_on_value)` → ТО `custom: «пауза симуляції»` — точка зупинки за даними.
- КОЛИ `input(terminal, status)` → ЯКЩО `custom: «машині потрібен новий чип»` → ТО `custom: «вимоги йдуть на Workstation»`.
- КОЛИ `input(terminal, modelchip)` → ТО `window(level-select)` — лише на Workstation.
- КОЛИ `input(terminal, fabricate)` → ЯКЩО `custom: «дизайн прийнято»` → ТО `spawn(chip)` на Fabricator.
- КОЛИ `input(terminal, reboot)` → ЯКЩО `custom: «новий чип встановлено»` → ТО `unlock(next_room)`.
- Перемога: усі рядки таблиці пройдено зі стабільним станом · Поразка: нема — провалена валідація лише зупиняється, правиш схему · Рахунок: Blocks (без субстрату), Volume (грубо — добуток розмірів кристала), Ticks (час валідації), MOS (кількість транзисторів); кожна метрика — одна з 5 оцінок (Functional < Satisfactory = 1.3× бази < Streamlined = база стадії < Advanced = 0.9× < Masterpiece = найкраще відоме), оцінка чипа — середнє, округлене вниз; loss і float рахуються, але на оцінку не впливають.

## Керування і ввід
- Миша: ЛКМ — блок; утримання — лінія «Г»; права кнопка — режим Select (подвійна — назад у Edit); Left Alt — видалення; Left Ctrl — будувати, виділяти чи видаляти вгору (куб).
- Буфер: Ctrl+A / C / X / V, Ctrl+Z / Y (undo не чіпає мітки); під час вставки X і Z віддзеркалюють, R повертає по діагоналі; T — виділити весь електрично звʼязаний сегмент.
- Симуляція: U — валідація, I — пуск/пауза, O — крок на тік, P — скидання, ] / [ — швидше/повільніше.
- Камера: права кнопка тягне, середня обертає, WASD / стрілки — рух, Q / E — поворот, колесо — зум, Space — скинути, F7 — вільна камера, F6 — «драматичні» рухи; F8 ховає панелі, F9 — налагоджувальний оверлей.
- Слоти: F1–F5 або Tab; +/- розсувають біти міток Value.
- У кампанії — ходьба 3D-комплексом і текстові команди терміналів.

## Вікна, меню, HUD
- `game-screen` (Component Editor): кристал у 3D; зверху посередині `custom: «Truth Table»` — входи й очікувані виходи по рядках, лічильник «0/4», кнопка Validate; знизу ліворуч Level Info (файл, «14 x 9 x 9 (cur:13,0,8)», слот S2, undo/redo), Mode Select, Simulation Control («Ticks 0 at 25T/s», ▶ ‖ ⏭, повзунок, ⏮); знизу посередині `tool-palette` «Blocks» (Metal, NMOS, PMOS); знизу праворуч Camera; плаваючі мітки «A (_)», «A NAND B=1, now=_».
- `custom-window` «Schematic» — еталонна схема стадії (NAND: 2 PMOS паралельно, 2 NMOS послідовно).
- `custom-window` терміналу — текстова консоль машини.
- `level-select` — стадії через `modelchip`, відкриваються послідовно; також Bonus Stages і Community Stages (Playtest).
- `custom-window` Blueprint Library — перейменувати, дублювати, видалити; вкладка SCHEMATICS з відкритими схемами.
- `custom-window` Clock Control (Library) і Toolbox (розмір кристала, auto-shrink, експериментальні опції).
- `settings-window` — клавіші (частина змінна), 8 мов.
- Головне меню показує кнопку Gauntlet, поки триває турнір.
- Переходи: комплекс → термінал `status` → Workstation `modelchip` → level-select → game-screen → Validate → оцінки → Fabricator `fabricate` → встановити чип → `reboot`.

## Фічі поза полем
- Кампанія: розділ 1 (Bypass → Inverter → Adder → ALU), розділ 2 (регістри й ALU); ще 6 розділів у розробці, мета — 8-бітний процесор. На сайті — 70+ стадій і 190K+ надісланих рішень.
- Library — `mode-sandbox` з Clock і константами будь-де; Bonus Stages.
- Gauntlet — тижневі турнірні стадії: Rev-0 (4 тижні з 24.05.2025: Majority Function 3Bit, Priority Encoder 4-2Bit, Power of 2 Detector 3Bit, Magnitude Comparator 2Bit), 0–100 балів за метрику між динамічними референсами, 400 за стадію, 1600 разом; сайт описує ваги ticks 40 %, blocks / volume / transistors по 20 %.
- `save-slots`: 5 на стадію, `autosave` кожні 60 с, після валідації й на виході.
- Blueprints (вибране чи весь рівень), проби з точками зупинки, `step-mode`, `speed-control`, `undo` / `redo`.
- `leaderboard-online`: рейтинги, галерея й статистика стадій на hardchip.io.
- `localization` 8 мов (переклад спільнотою на GitHub); демо; досягнення Steam.

## Варіації й родичі
- [kohctpyktop](kohctpyktop.md) — 2D-шари кремнію n/p і металу, транзистор з перетину смуг; Hard Chip — те саме в 3D з явною фігурою MOS і затримками.
- [turing-complete](turing-complete.md) — від NAND до CPU, але з готових вентилів і без затримки дроту.
- [robot-odyssey](robot-odyssey.md), [virtual-circuit-board](virtual-circuit-board.md) — логіка з вентилів і дротів.
- [wireworld](../build-sim/wireworld.md) — сигнал як клітинний автомат; [minecraft-redstone](../build-sim/minecraft-redstone.md) — 3D-воксельні сигнали з тіками затримки.
- Осі варіацій: **абстракція** (транзистор / вентиль / компонент / мікроконтролер); **затримка** (нема / на вентиль / на кожну клітину дроту); **перевірка** (таблиця істинності зі стабільністю / хвилі в часі / програма); **простір** (2D-шари / 3D-воксель).

## Цікавинки для курсу
- Три стани сигналу, поширення на клітину за тік, розряд відʼєднаного сегмента й коротке замикання — 🥈: флуд із конфліктом джерел.
- Розпізнавання MOS як 3D-шаблону зі спільними блоками сусідів — 🥇.
- Затримки 3 / 4 / 100 тіків і перевірка «схема стабільна» перед порівнянням — 🥉.
- Валідатор таблиці істинності з `any` і фазою PWR — 📎.
- Чотири метрики, пʼять оцінок з порогами 1.3× / 0.9× / рекорд, оцінка чипа = floor(середнього) — 📎.
- Проба як точка зупинки за даними — 🥉.
- Blueprints: копіювання з віддзеркаленням X / Z і поворотом R на 3D-сітці — 🥉.
- Термінали з командами status / modelchip / fabricate / reboot як мета-шар — 🌱.

## Мапа на каталог
- Є: `cell-click` ↔ блок кліком · `multi-select` ↔ рамка й куб · `editor-draw-tools` ↔ лінія «Г», площина · `undo-redo` · `step-execution` ↔ пуск / крок / швидкість · `save-multi-slot` ↔ 5 слотів · `save-autosave` ↔ кожні 60 с · `sequential-levels` / `level-unlock` / `level-select` ↔ modelchip · `leaderboard` ↔ рейтинги сайту · `game-screen` · `tutorial-window` ↔ навчальні стадії · `player-camera` ↔ камера кристала · `keyboard-controls` / `controls-remap` · `language-picker` ↔ 8 мов.
- **Нема** → пропозиції карток:
  - `+propagation-delay` «Сигнал іде на клітину за тік, ключ вмикається з затримкою» · entities/interact · 🥉 · слоти {wire: 1 тік/клітина, nmos: 3, pmos: 4}.
  - `+short-circuit-error` «Зіткнення 0 і 1 — стан помилки» · game-logic/constraints · 📎.
  - `+floating-gate-decay` «Нейтральний затвор гасне за N тіків» · entities/state · 📎 · слот {decay: 100}.
  - `+stable-state-check` «Перевірка лише після стабілізації» · game-logic/win · 📎.
  - `+metric-grades` «Пʼять оцінок за метрикою з порогами» · game-logic/score · 🌱.
  - `+probe-breakpoint` «Проба-індикатор із паузою за значенням» · interface/hud · 🥉.
  - `+clock-source` «Генератор тактового сигналу» · entities/spawn · 🌱; `+power-up-phase` «Фаза ініціалізації до тесту» · game-logic · 📎.
  - `+terminal-commands` «Текстові команди машин у світі» · interface/input · 📎; `+reference-schematic` «Еталонна схема поруч» · interface/hud · 🌱.
  - `+weekly-gauntlet` «Тижневий турнір з динамічними порогами» · interface/results · 🥉; `+auto-resize-die` «Поле росте при будові, стискається після» · entities/legality · 🌱.
  - Повтори: `+signal-propagation`, `+transistor-crossing`, `+layer-via`, `+edge-io-pins` (KOHCTPYKTOP), `+io-test-streams`, `+solution-metrics`, `+blueprints`, `+sandbox-mode`.

## Пропозиції до словників
- `+trigger:signal(net)` — у мережі змінилось значення; `+trigger:short(net)` — зустрілись 0 і 1.
- `+cond:signal(net, v)` — мережа має значення v ∈ {0, 1, нейтральне}; `+effect:power(net, v)` — подати значення в мережу (тут і 0, і 1 — активні рівні).
- `+role:pin` — мітка входу/виходу на краю кристала.
- `+window:truth-table` (як у Turing Complete), `+window:schematic` — еталонна схема, `+window:terminal` — консоль машини в світі гри.
- `+ui:probe-overlay` — число з вибраних бітів просто над кристалом; `+ui:die-size` — розмір X×Y×Z і координати курсора.
- `+feature:metric-grades`, `+feature:weekly-gauntlet`, `+feature:breakpoint`.
- `+axis:signal` — тут: три стани, одна клітина за тік, конфлікт джерел = помилка.

## Джерела
- ⭐ [hardchip.io](https://hardchip.io/) — суть, метрики, ваги Gauntlet, кампанія 2 з 8 розділів, 70+ стадій, лінки на вікі, Steam, Discord, YouTube.
- [Steam: Hard Chip](https://store.steampowered.com/app/2844290/Hard_Chip/) — ранній доступ, від транзистора до ALU, «Every wire has length. Every gate has delay.», «You are new_user, trapped. The terminals are dead.», ~5 год і 55 компонентів на старті, теги; знімки: таблиця істинності «0/4», Validate, вікно Schematic (NAND), палітра Blocks, панель тіків «25T/s», розмір «14 x 9 x 9».
- [Вікі: Mechanics](https://hardchip.wiki.gg/wiki/Mechanics) — сигнали, валідація, замикання, плаваючий затвор, PWR.
- [Вікі: Blocks](https://hardchip.wiki.gg/wiki/Blocks) — усі блоки, будова й затримки MOS, спільні блоки, Clock, Boot Clear, Puller.
- [Вікі: Grades](https://hardchip.wiki.gg/wiki/Grades) — метрики й оцінки.
- [Вікі: Component Editor](https://hardchip.wiki.gg/wiki/Component_Editor) — панелі, режими, клавіші, слоти, координати.
- [Вікі: Labels](https://hardchip.wiki.gg/wiki/Labels) — мітки й проби.
- [Вікі: Campaign](https://hardchip.wiki.gg/wiki/Campaign) і [Terminals](https://hardchip.wiki.gg/wiki/Terminals) — цикл ремонту, команди терміналів.
- [Вікі: Gauntlet](https://hardchip.wiki.gg/wiki/Gauntlet) — турнір Rev-0.
- [YouTube: канал розробника](https://www.youtube.com/channel/UCm1uoPjHeGYf6sYXE2k--DQ) — девлоги.

## Непевне
- (?) Чи є гістограми розподілу рішень у грі: сайт показує рейтинги, галерею й статистику стадій, гістограм я не бачив.
- (?) Ваги Gauntlet 40 / 20 / 20 / 20 (сайт) і опис Rev-0 у вікі (лінійна інтерполяція між динамічними референсами, без ваг) — можливо, різні сезони правил.
- (?) Від першої чи третьої особи 3D-комплекс і як гравець у ньому рухається — вікі мовчить (сторінки-заготовки).
- (?) Як середнє чотирьох оцінок переходить у назву оцінки чипа й числові бази стадій — у вікі нема.
- (?) Вікі пише «Activation works by replacing the middle channel block with a well block» — формулювання неясне, у правила не переносив.
- (?) Які стадії, крім Memory Cells, мають фазу PWR і Boot Clear.
- (?) Live demo на hardchip.io не відкривав.
