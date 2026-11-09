---
title: Chuckie Egg
slug: chuckie-egg
aka: [Hen-House Harry, Чакі Ег]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1983
platforms: [ZX Spectrum, BBC Micro, Dragon 32/64, Acorn Electron, C64, Amstrad CPC, MSX, Atari 8-bit, Amiga, Atari ST, MS-DOS, VIC-20 (2021)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Chuckie_Egg", best: true, note: "12 яєць на екран, зерно зупиняє таймер, кури, качка в клітці, ліфти з загортанням, 8 екранів × 5 проходів"}
  - {kind: other, url: "https://spectrumcomputing.co.uk/zxsr.php?id=958", note: "огляди ZX-журналів: клавіші, 1–4 гравці, стрибок з розворотом, ліфти, бонус, послід курей"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Chuckie+Egg+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [move-by-input, gravity-fall, ladder-climb, carrier-platform, wrap-edges, collect-all, item-pickup, enemy-patrol, chase-player, touch-death, environment-death, player-death, time-out, time-bonus, event-points, extra-life-threshold, sequential-levels, progress-acceleration, hot-seat, score-records, leaderboard, controls-remap, game-pause, status-panel, keyboard-controls, +lift-crush-ceiling, +enemy-eats-pickup, +timer-freeze-pickup, +caged-enemy-release, +loop-passes-harder, +jump-reverse-midair]
proposes: ["+effect:eat(a, item)", "+effect:pause_timer(n)", "+trigger:pass_end", "+feature:pass-cycle", "+card:enemy-eats-pickup", "+card:timer-freeze-pickup", "+card:caged-enemy-release", "+card:loop-passes-harder"]
author: opus
date: 2026-11-09
---

# Chuckie Egg — Гаррі з курника збирає 12 яєць на екрані з платформ, драбин і ліфтів, поки кури патрулюють, а таймер спадає

## Суть
Однокадровий платформер: платформи, драбини й іноді ліфти. На кожному екрані — дванадцять яєць; зібрав усі — наступний екран. Кури ходять платформами й драбинами, дотик смертельний. Купки зерна дають очки й **зупиняють таймер**, але кури їх зʼїдають і на цей час стоять. Над рівнем у клітці сидить велика качка: після восьми екранів вона вилітає й полює на Гаррі.

## Поле і час
- Один нескролений екран, вигляд збоку; поле з клітин-тайлів: платформа, драбина, порожнеча, яйце, зерно; ліфти — рухомі платформи у вертикальній шахті.
- Real-time; таймер рівня спадає щотік; зібране зерно на час зупиняє його.
- Ліфт їде вгору й **загортається**: з верху екрана — знову знизу.
- Інформація повна; поведінка курей детермінована (?).
- 8 екранів утворюють прохід; п'ять проходів з різним набором ворогів — 40 рівнів, далі «рівень 41» = рівень 33 (цикл останнього проходу).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гаррі (Hen-House Harry) | player | 5 життів; +1 за кожні 10 000 | біг, стрибок (можна розвернутись у польоті), лазіння, падіння |
| Платформа | terrain | — | опора |
| Драбина | terrain | — | рух угору/вниз; точний вхід важкий |
| Ліфт | platform | рух угору | везе Гаррі; вгорі екрана — загортається вниз |
| Яйце | pickup | 12 на екран | треба зібрати всі |
| Купка зерна | pickup | — | очки + тимчасова зупинка таймера; їдять кури |
| Курка | enemy | швидкість росте на 5-му проході | патрулює платформи й драбини; дотик — смерть; зупиняється, щоб зʼїсти зерно |
| Качка | enemy | у клітці на проході 1 | з проходу 2 летить до Гаррі крізь рівень (?) |
| Клітка качки | static | — | лише декорація з качкою |
| Дірка в підлозі екрана | hazard | — | падіння за нижній край = втрата життя |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(harry, dir)`.
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, ladder)` → ТО `move(harry, dir)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок дугою; у польоті можна змінити напрям»`.
- КОЛИ `tick` → ЯКЩО `not supported(harry)` → ТО `fall(harry)`; падіння з великої висоти не вбиває (?).
- КОЛИ `edge(harry)` → ЯКЩО `custom: «нижній край — дірка в підлозі»` → ТО `lose`, `lives(-1)`.
- КОЛИ `tick` → ЯКЩО `occupied(here, lift)` → ТО `carry`; `move(lift, up)`; на верхньому краю `wrap(lift)`.
- КОЛИ `contact(harry, ceiling)` → ЯКЩО `state(harry, on_lift)` → ТО `lose`, `lives(-1)`.
- КОЛИ `contact(harry, egg)` → ТО `pickup`, `score(n)`, `counter(eggs_left, -1)`.
- КОЛИ `contact(harry, grain)` → ТО `pickup`, `score(n)`, `custom: «таймер стоїть кілька секунд»`.
- КОЛИ `contact(hen, grain)` → ТО `disappear_b`, `freeze(hen, n)` — курка їсть.
- КОЛИ `contact(harry, hen)` → ТО `lose`, `lives(-1)`, `restart` (?).
- КОЛИ `contact(harry, duck)` → ТО `lose`, `lives(-1)`.
- КОЛИ `tick` → ЯКЩО `level(>, 8)` → ТО `custom: «качка летить у бік Гаррі»` — переслідування.
- КОЛИ `counter(eggs_left, ==, 0)` → ТО `score(time_left)` (?), `next_level`.
- КОЛИ `timer(level)` → ЯКЩО `counter(time, ==, 0)` → ТО `lose`, `lives(-1)`.
- КОЛИ `counter(score, >=, 10000·k)` → ТО `lives(+1)`.
- КОЛИ `custom: «пройдено 8 екранів»` → ТО `custom: «новий прохід: склад ворогів змінюється»` — 2: без курей, качка на волі; 3: кури + качка; 4: більше курей; 5: качка й кури швидші.
- КОЛИ `died(harry)` → ЯКЩО `mode(multiplayer)` → ТО `pass_turn` — грає наступний із 1–4 гравців.
- Перемога: нема фіналу — після 40-го рівня гра крутить останній прохід · Поразка: життя скінчились · Рахунок: яйця, зерно, бонус за рівень.

## Керування і ввід
- Пʼять клавіш: ліво, право, вгору, вниз, стрибок; клавіші задає гравець (на деяких машинах частина клавіш заборонена); на ZX — набір за замовчуванням, курсорні або свої.
- ZX: Shift-H — пауза, Shift-A — перервати й перейти до таблиці рекордів.
- Прийом з оглядів: біжи на драбину з утримуваним «вгору»/«вниз» — Гаррі одразу лізе.

## Вікна, меню, HUD
- `main-menu`: кількість гравців 1–4, `options-controls` — перепризначення клавіш.
- `game-screen`: екран-рівень; HUD — `score` кожного гравця, номер гравця, `level-number`, бонус, `timer-countdown`, `lives` (?).
- `leaderboard` — таблиця рекордів; при кількох гравцях оновлюється лише в кінці.
- Переходи: меню → рівень 1 → (12 яєць) наступний → … → (життя скінчились) таблиця рекордів → меню.

## Фічі поза полем
- `hotseat` 1–4 гравці по черзі: хід передається після втрати життя.
- `remap-controls`, `pause`.
- `levels-sequential` 8 екранів × 5 проходів, без вибору рівня (?).
- `leaderboard-local` з іменами.

## Варіації й родичі
- Chuckie Egg 2 (1985, сиквел); Super Chuckie Egg (2017, мобільний ремейк); VIC-20-порт 2021 року (журнал Reset64).
- Родичі в сімʼї: [manic-miner](manic-miner.md) (збори на екрані, таймер, конвеєри), [miner-2049er](miner-2049er.md), [space-panic](space-panic.md) (драбини й вороги на поверхах), [lode-runner](lode-runner.md) (зібрати все на екрані без стрілянини).
- Осі: **таймер** (спадає / зупиняється предметом); **що вороги роблять з предметами** (ігнорують / їдять / несуть); **ескалація** (нові рівні / ті самі рівні з іншим складом ворогів).

## Цікавинки для курсу
- Зерно як ресурс, за який змагаються гравець і вороги: гравець — зупинка таймера, курка — зупинка самої курки — 📎.
- Ліфт, що загортається з верху вниз, і смерть від стелі на ліфті — 📎.
- Проходи-цикли: ті самі 8 мап, але таблиця «прохід → склад і швидкість ворогів» — 🌱 (дані замість нових рівнів).
- Качка-переслідувач, що летить без урахування платформ — 🌱 (жадібний рух у 8 напрямках).
- Стрибок з розворотом у польоті — 📎.
- Hot-seat на 4 гравців з передачею ходу після смерті — 🌱.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `ladder-climb` · `carrier-platform` (ліфт) · `wrap-edges` (ліфт загортається) · `collect-all` (12 яєць) · `item-pickup` (зерно) · `enemy-patrol` (кури) · `chase-player` (качка) · `touch-death` · `environment-death` (дірка, стеля) · `player-death` · `time-out` · `time-bonus` · `event-points` · `extra-life-threshold` · `sequential-levels` · `progress-acceleration` (5-й прохід швидший) · `hot-seat` · `score-records` · `leaderboard` · `controls-remap` · `game-pause` · `status-panel` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+lift-crush-ceiling` «Ліфт загортається, стеля вбиває пасажира» · entities/move · 📎.
  - `+enemy-eats-pickup` «Ворог зʼїдає предмет і на час стоїть» · entities/interact · 🌱.
  - `+timer-freeze-pickup` «Предмет зупиняє таймер рівня» · game-logic/lose · 🌱 · слот {duration}.
  - `+caged-enemy-release` «Ворог у клітці вилітає з певного рівня» · entities/spawn · 🌱.
  - `+loop-passes-harder` «Ті самі рівні по колу з таблицею ускладнень» · game-logic/progress · 🌱.
  - `+jump-reverse-midair` «Зміна напряму в польоті» · entities/move · 📎 (протилежність `+fixed-arc-jump` з manic-miner).

## Пропозиції до словників
- `+effect:eat(a, item)` — ворог прибирає предмет з поля собі (не в інвентар гравця).
- `+effect:pause_timer(n)` — зупинити таймер рівня на N тіків.
- `+trigger:pass_end` — завершено цикл рівнів (прохід), починається наступний з іншими параметрами.
- `+feature:pass-cycle` — гра крутить ту саму послідовність рівнів з наростанням складності.
- `+card:enemy-eats-pickup`, `+card:timer-freeze-pickup`, `+card:caged-enemy-release`, `+card:loop-passes-harder` — див. вище.

## Джерела
- ⭐ [Wikipedia: Chuckie Egg](https://en.wikipedia.org/wiki/Chuckie_Egg) — 12 яєць, зерно (очки, зупинка таймера, курка їсть і стоїть), качка в клітці → на волі, ліфти з загортанням і смерть від верхнього краю, дірка внизу, 5 проходів по 8 рівнів, рівень 41 = 33, 5 життів, +1 за 10 000.
- [Spectrum Computing: огляди Chuckie Egg](https://spectrumcomputing.co.uk/zxsr.php?id=958) — 5 клавіш з перепризначенням, Shift-A / Shift-H, 1–4 гравці по черзі, розворот у стрибку, вхід на драбину, ліфти, бонус, що спадає, послід курей.
- YouTube: пошук «Chuckie Egg gameplay».

## Непевне
- (?) Таймер і бонус: Wikipedia — один зворотний таймер; огляди — «бонус спадає до нуля = смерть». Можливо, на екрані два лічильники (бонус і час); точно не перевірено.
- (?) Очки за яйце й зерно, тривалість зупинки таймера — не знайдено.
- (?) Чи смертельне падіння з великої висоти: Crash каже, що «деякі великі падіння» можна пережити.
- (?) Качка летить крізь платформи до Гаррі — з памʼяті; Wikipedia каже лише «homing in».
- (?) Послід курей як окрема перешкода — згадка лише в одному огляді (Crash).
- (?) Після смерті — рестарт екрана чи продовження з тими самими зібраними яйцями.
- (?) Кількість життів: 5 (Wikipedia, Crash, PCG) проти «3 на рівень» (Sinclair User).
