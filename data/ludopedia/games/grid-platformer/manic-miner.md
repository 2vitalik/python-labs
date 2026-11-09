---
title: Manic Miner
slug: manic-miner
aka: [Miner Willy, Манік Майнер]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1983
platforms: [ZX Spectrum, C64, Amstrad CPC, MSX, Dragon 32, BBC Micro, SAM Coupé, Xbox 360]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Manic_Miner", best: true, note: "20 печер-екранів, предмети → портал, запас повітря, смерть від падіння, вороги на фіксованих маршрутах"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/entry/3012/ZX-Spectrum/Manic_Miner", note: "картка ZX: інструкції, інлеї, карта"}
  - {kind: other, url: "https://worldofspectrum.org/pub/sinclair/games-info/m/ManicMiner.txt", note: "оригінальна інструкція: клавіші, ключі, портал, nasties"}
  - {kind: other, url: "https://skoolkit.ca/disassemblies/manic_miner/reference/facts.html", note: "дизасемблер: промінь Solar Power, витрата повітря, конвеєр у кожній печері, чіт 6031769"}
  - {kind: other, url: "https://www.c64-wiki.com/wiki/Manic_Miner", note: "C64: клавіші, пауза, підлога, що руйнується"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Manic+Miner+ZX+Spectrum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, item-pickup, collect-all, reach-exit, key-and-door, enemy-patrol, touch-death, environment-death, player-death, time-out, carrier-platform, timed-despawn, button-toggle, extra-life-threshold, event-points, time-bonus, sequential-levels, cheat-codes, game-pause, music-toggle, status-panel, attract-demo, game-screen, keyboard-controls, +fall-height-kill, +crumbling-floor, +conveyor-locks-walk, +fixed-arc-jump, +beam-drains-resource, +guardian-blocks-exit]
proposes: ["+trigger:landed", "+card:crumbling-floor", "+card:conveyor-locks-walk", "+card:fixed-arc-jump", "+card:beam-drains-resource", "+card:guardian-blocks-exit"]
author: opus
date: 2026-11-09
---

# Manic Miner — шахтар Віллі на кожному з 20 екранів збирає миготливі предмети й біжить до порталу, поки не скінчилось повітря

## Суть
Канонічний британський платформер-«екран»: одна печера = один нескролений екран із платформ, конвеєрів, підлоги, що кришиться, смертельних рослин і ворогів-«guardians» на жорстких маршрутах. Треба зібрати всі миготливі предмети («ключі»), після чого портал починає блимати — у нього й треба зайти. Таймер — смуга повітря, яка весь час спадає. Стрибок має фіксовану дугу, а падіння з висоти вбиває: рівень — це головоломка таймінгу й маршруту.

## Поле і час
- Один екран на печеру, вигляд збоку; поле з клітин-тайлів (підлога, стіна, конвеєр, підлога, що кришиться, «nasty»). Вороги й Віллі рухаються піксельно, але маршрути — вздовж тайлових рядів/стовпців.
- 20 печер підряд; після останньої — гра з початку без підвищення складності (за Wikipedia).
- Real-time на кадрах; повітря спадає з кожним тіком; ворожі маршрути детерміновані.
- Гравітація: Віллі падає, доки нема опори; конвеєр везе його вбік.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Віллі | player | життя | ходить ліво/право, стрибає фіксованою дугою; без драбин |
| Підлога / платформа | terrain | — | опора |
| Стіна / цегла | static | — | блокує рух і стрибок |
| Підлога, що кришиться | terrain | стадії руйнування | осідає, поки на ній стоїш, і зникає |
| Конвеєр | terrain | напрямок | везе того, хто стоїть; іти проти нього не можна (?) |
| Nasty (отруйна квітка, шипи, сталактит) | hazard | — | смерть при дотику; нерухома |
| Guardian горизонтальний | enemy | швидкість, межі | туди-сюди по ряду між двома точками |
| Guardian вертикальний | enemy | швидкість, межі | вгору-вниз між двома точками |
| Eugene | boss | — | ходить вертикально; коли предмети зібрано — спускається й стереже портал (?) |
| Kong Beast | boss | — | стоїть угорі; дві кнопки-перемикачі: стіна відкривається, підлога під ним провалюється (?) |
| Skylab | enemy | — | падає згори, розбивається об підлогу, зʼявляється в іншому стовпці (?) |
| Промінь сонячного генератора | hazard | — | йде згори вниз, відбивається вліво від guardian-ів; дотик виснажує повітря |
| Предмет («ключ») | pickup | 100 очок (?) | миготить; зникає при дотику |
| Перемикач | switch | увімк/вимк | у печерах Kong Beast змінює клітини |
| Портал | gate | закритий / відкритий | відкривається, коли зібрано всі предмети; вхід = наступна печера |
| Повітря | resource | смуга | спадає щотік; 0 — смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` і `not cell(under, conveyor)` → ТО `move(willy, dir)`.
- КОЛИ `input(jump)` → ЯКЩО `custom: «стоїть на опорі»` → ТО `custom: «стрибок фіксованою дугою в напрямку руху; у повітрі керування нема»`.
- КОЛИ `tick` → ЯКЩО `not custom: «є опора знизу»` → ТО `fall(willy)`.
- КОЛИ `custom: «приземлився після падіння вище за поріг»` → ТО `lives(-1)` (`+trigger:landed`).
- КОЛИ `tick` → ЯКЩО `cell(under, conveyor)` → ТО `move(willy, conveyor_dir)`.
- КОЛИ `tick` → ЯКЩО `cell(under, crumbling)` → ТО `custom: «підлога осідає на стадію»`; на останній — `set_cell(under, empty)`.
- КОЛИ `contact(willy, nasty)` → ТО `lives(-1)`, `restart`.
- КОЛИ `contact(willy, guardian)` → ТО `lives(-1)`, `restart`.
- КОЛИ `tick` → ТО `custom: «guardian рухається на крок своїм маршрутом; на межі — розворот»`.
- КОЛИ `contact(willy, item)` → ТО `disappear_b`, `score(100)` (?).
- КОЛИ `all_gone(item)` → ТО `set_state(portal, open)`.
- КОЛИ `enter(willy, portal)` → ЯКЩО `state(portal, open)` → ТО `custom: «залишок повітря в очки»`, `next_level`.
- КОЛИ `timer(every)` → ТО `counter(air, -1)`; КОЛИ `counter(air, ==, 0)` → ТО `lives(-1)`, `restart`.
- КОЛИ `contact(willy, solar_beam)` → ТО `counter(air, -n)` — повітря тече у кілька разів швидше.
- КОЛИ `all_gone(item)` → ЯКЩО `level(==, eugenes_lair)` → ТО `custom: «Eugene спускається до порталу й стоїть на ньому»` (?).
- КОЛИ `contact(willy, switch)` → ТО `set_state(switch, on)`, `set_cell(wall|floor, empty)` — у печерах Kong Beast.
- КОЛИ `custom: «під Kong Beast зникла підлога»` → ТО `fall(kong)`, `score(n)` (?).
- КОЛИ `counter(score, >=, 10000·k)` → ТО `lives(+1)`.
- КОЛИ `input(cheat_code)` → ТО `custom: «режим чіту: стрибок у будь-яку печеру»`.
- Перемога: пройти 20 печер (далі цикл). Поразка: 0 життів. Рахунок: предмети + бонус за залишок повітря; життя кожні 10 000.

## Керування і ввід
- ZX Spectrum: ліворуч — Q/E/T/U/O, праворуч — W/R/Y/I/P, стрибок — нижній ряд (Shift…Space); Kempston-джойстик.
- C64: ті самі ряди, пауза A/S, музика L/K.
- Дві «осі» вводу: напрямок і стрибок; під час стрибка й падіння ввід ігнорується (?).

## Вікна, меню, HUD
- `splash-screen` / заголовок із музикою «Блакитний Дунай» і бігучим рядком.
- `attract-demo` — показ печер без вводу (?).
- `game-screen`: печера + назва печери, смуга повітря (`energy-bar`), `score`, `hi-score`, `lives` (фігурки Віллі внизу).
- `end-screen` — game over (чобіт, що розчавлює Віллі (?)); фінальний екран «на поверхні» після 20-ї печери.
- Переходи: заставка → печера 1 → (портал) наступна → … → поверхня → печера 1; (0 життів) → game over → заставка.

## Фічі поза полем
- `levels-sequential`: 20 печер у фіксованому порядку, без збережень і паролів.
- `cheat-codes`: 6031769 на Spectrum (вибір печери), «PENGUIN» на Dragon.
- `pause`, `music-toggle`.
- Порт SAM Coupé — +40 печер.

## Варіації й родичі
- Натхнення: Miner 2049er (див. [miner-2049er](miner-2049er.md)) — там фарбування платформ, тут — збирання ключів.
- Наступник: Jet Set Willy (відкритий маєток з кімнат замість лінійних печер).
- Родичі в корпусі: [lode-runner](lode-runner.md) (збирання золота → вихід), [space-panic](space-panic.md) (кисень як таймер), [kings-valley](kings-valley.md) (піраміди-екрани з виходом після збору).
- Осі: **як відкривається вихід** (зібрати все / квоту / ключ); **таймер** (повітря / нема); **підлога** (тверда / кришиться / везе); **ворог** (маршрут між точками / реакція на подію, як Eugene).

## Цікавинки для курсу
- Підлога, що кришиться по стадіях, поки на ній стоїш — 🌱 (лічильник на клітині).
- Конвеєр, що везе й блокує хід проти себе — 🌱.
- Портал, що відкривається після `all_gone(item)` — 🌱.
- Фіксована дуга стрибка + смерть від висоти падіння — 📎 (стан «у повітрі», лічильник висоти).
- Промінь, що трасується від стелі й відбивається від ворогів, виснажуючи ресурс — 🥉.
- Вороги «вимикач-реакція»: Eugene блокує вихід після збору, Kong падає від двох кнопок — 📎.

## Мапа на каталог
- Є: `gravity-fall` · `item-pickup` / `collect-all` · `reach-exit` + `key-and-door` (портал як двері з умовою) · `enemy-patrol` (guardians) · `touch-death`, `environment-death`, `player-death` · `time-out` (повітря) · `carrier-platform` (конвеєр) · `timed-despawn` (підлога) · `button-toggle` (перемикачі Kong) · `extra-life-threshold` · `event-points`, `time-bonus` · `sequential-levels` · `cheat-codes` · `game-pause`, `music-toggle` · `status-panel` · `attract-demo`, `game-screen` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+fall-height-kill` — як у Space Panic, тут для гравця.
  - `+crumbling-floor` «Підлога руйнується, поки на ній стоїш» · entities/interact · 🌱 · слот {stages}.
  - `+conveyor-locks-walk` «Конвеєр везе й не дає йти проти» · entities/move · 🌱.
  - `+fixed-arc-jump` «Стрибок фіксованою дугою без керування в повітрі» · entities/move · 📎.
  - `+beam-drains-resource` «Промінь, що відбивається і виснажує ресурс при дотику» · entities/combat · 🥉.
  - `+guardian-blocks-exit` «Ворог займає вихід після виконання цілі» · entities/move · 🌱.

## Пропозиції до словників
- `+trigger:landed(a, height)` — сутність приземлилась після падіння на N клітин (Manic Miner, Spelunker, Space Panic).
- `+card:crumbling-floor`, `+card:conveyor-locks-walk`, `+card:fixed-arc-jump`, `+card:beam-drains-resource`, `+card:guardian-blocks-exit` — див. вище.

## Джерела
- ⭐ [Wikipedia: Manic Miner](https://en.wikipedia.org/wiki/Manic_Miner) — 20 печер, предмети → портал, кисень, смерть від падіння, життя кожні 10 000, чіт Dragon, цикл після 20-ї.
- [Spectrum Computing](https://spectrumcomputing.co.uk/entry/3012/ZX-Spectrum/Manic_Miner) — інструкції, інлеї, карта.
- [WoS: інструкція](https://worldofspectrum.org/pub/sinclair/games-info/m/ManicMiner.txt) — клавіші, ключі/портал, nasties, «fallen heavily».
- [SkoolKit: факти](https://skoolkit.ca/disassemblies/manic_miner/reference/facts.html) — промінь Solar Power (вниз, вліво від guardian, +8/12 повітря за кадр), підлога в Warehouse, конвеєр у кожній печері, чіт 6031769.
- [C64-Wiki](https://www.c64-wiki.com/wiki/Manic_Miner) — клавіші C64, пауза/музика, підлога, що руйнується, впізнається за кольором.

## Непевне
- (?) Поведінка Eugene (спуск до порталу), Kong Beast (дві кнопки: стіна + провал підлоги), Skylab-ів — з памʼяті; джерела лише згадують їх.
- (?) Чи можна йти проти конвеєра, чи лише стрибати; чи є керування в повітрі.
- (?) Скільки життів на старті (інструкція: «fallen heavily three times» — ймовірно 3) і поріг висоти падіння.
- (?) 100 очок за предмет — за Retro Gamer (з пошуку), не перевірено в грі; очки за падіння Kong.
- (?) Вигляд game over (чобіт) і наявність demo-режиму.
