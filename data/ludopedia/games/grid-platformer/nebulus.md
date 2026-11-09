---
title: Nebulus
slug: nebulus
aka: [Tower Toppler, Castelian, Kyorochan Land, Subline, Небулус]
family: grid-platformer
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: partial
  random: none
  goal: state
year: 1987
platforms: [ZX Spectrum, C64, Amstrad CPC, Amiga, Atari ST, Acorn Archimedes, MS-DOS, Atari 7800, NES, Game Boy, Wii VC]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Nebulus_(video_game)", best: true, note: "вісім веж, обертання вежі, виступи-сходи й ліфти, удар ворога скидає на виступ нижче, двері нагорі, підводний бонус"}
  - {kind: other, url: "https://www.c64-wiki.com/wiki/Nebulus", note: "C64: типи ворогів і очки за них, платформи, що кришаться й ковзають, тунелі, бонуси кінця вежі, клавіші, чіт"}
  - {kind: other, url: "https://dyn.manpages.debian.org/trixie/toppler/toppler.6.en.html", note: "man-сторінка відкритого клону Tower Toppler: двері, ліфти, сніжка/стрибок однією кнопкою, редактор місій"}
  - {kind: other, url: "https://www.oldgames.sk/en/game/nebulus/docs/", note: "огляд: циліндр без країв, Пого в центрі екрана"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Nebulus+C64+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-by-input, gravity-fall, wrap-edges, carrier-platform, floor-types, projectile-shot, shoot-forward, teleport, teleport-pair, enemy-patrol, environment-death, player-death, time-out, time-bonus, event-points, extra-life-threshold, reach-exit, sequential-levels, hot-seat, cheat-codes, game-pause, music-toggle, status-panel, game-screen, keyboard-controls, +crumbling-floor, +knockback, +cylinder-tower-view, +context-fire-jump, +height-score, +technique-bonus, +bonus-stage, +shot-stops-enemy]
proposes: ["+axis:field=cylinder", "+effect:knock_down(a, to)", "+trigger:landed", "+role:tunnel", "+feature:bonus-stage", "+ui:technique-counter", "+card:cylinder-tower-view", "+card:context-fire-jump", "+card:technique-bonus"]
author: opus
date: 2026-11-09
---

# Nebulus — Пого піднімається спіраллю виступів по циліндричній вежі, що обертається під ним, щоб на вершині ввійти у двері й обвалити її

## Суть
Жабоподібний Пого має вилізти на кожну з восьми веж, що стирчать з моря, і ввійти у двері на вершині — вежа після цього руйнується. Вежа — **сітка, загорнута в циліндр**: Пого завжди в центрі екрана, а ходьба ліворуч/праворуч обертає вежу. Виступи навколо вежі утворюють сходи, звʼязані ліфтами й тунелями крізь вежу. Вороги не вбивають, а **скидають з виступу вниз**; смерть — лише падіння в море або кінець часу. Між вежами — підводний бонус на субмарині.

## Поле і час
- Поле — стовпці навколо циліндра × поверхи-виступи; горизонтальна координата замкнена в кільце (`wrap`), вертикаль — від моря до вершини. Країв ліворуч/праворуч немає.
- Рендер: видно лише передню половину циліндра; Пого закріплений у центрі, вежа обертається й скролиться вертикально за ним. Задня половина вежі невидима — звідси `info: partial`.
- Шари: вежа (виступи-сходинки, ліфти, тунелі, двері), сутності (Пого, вороги, сніжка), море під вежею.
- Real-time; на кожну вежу — ліміт часу; вісім веж підряд, між ними бонус-етап.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Пого | player | життя; додаткове за кожні 5000 очок | ходить уздовж кільця, стрибає з розбігу, кидає сніжку зі стійки, їде ліфтом, входить у тунелі й двері |
| Виступ-сходинка | terrain | — | опора; горизонтальні виступи або сходи навколо вежі |
| Виступ, що кришиться | terrain | — | зникає, коли на нього стати |
| Слизький виступ | terrain | напрям | зносить Пого ліворуч або праворуч |
| Ліфт | platform | — | платформа вгору/вниз за джойстиком; трохи вужча за виступ (клон Toppler) |
| Тунель (двері в стіні) | static | — | вхід кнопкою «вгору»; виводить на протилежний бік вежі (?) |
| Двері на вершині | static | ціль | вхід запускає руйнування вежі |
| Сніжка | projectile | — | летить уздовж кільця; збиває частину ворогів |
| Миготливий блок | enemy | 50 очок | знищується пострілом |
| Стрибучий мʼяч | enemy | 100 очок | знищується пострілом |
| Сріблястий котючий мʼяч | enemy | — | постріл лише зупиняє на кілька секунд |
| Інші істоти (очі, фігури) | enemy | — | невразливі; лише ухилятись |
| Море | hazard | — | падіння у воду = втрата життя |
| Субмарина | player | лише бонус-етап | везе між вежами; торпеди |
| Риба | pickup | 30 на етап, 50–75 очок | торпеда ловить у бульбашку, потім підібрати |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(pogo, dir)`, `custom: «вежа обертається, Пого лишається в центрі екрана»`.
- КОЛИ `input(left|right)` → ЯКЩО `custom: «стовпець 0 / останній»` → ТО `wrap(pogo)` — кільце без країв.
- КОЛИ `tick` → ЯКЩО `not supported(pogo)` → ТО `fall(pogo)` до найближчого виступу нижче.
- КОЛИ `input(fire)` → ЯКЩО `moving(pogo, dir)` → ТО `custom: «стрибок уздовж кільця»`.
- КОЛИ `input(fire)` → ЯКЩО `not moving(pogo, dir)` → ТО `spawn_at(snowball, ahead)`.
- КОЛИ `input(up)` → ЯКЩО `cell(here, tunnel)` → ТО `teleport` на протилежний бік вежі (?).
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, lift)` → ТО `carry` — ліфт везе Пого на поверх вище/нижче.
- КОЛИ `enter(pogo, crumbling_ledge)` → ТО `set_cell(ledge, empty)` (?) затримка перед зникненням.
- КОЛИ `enter(pogo, slippery_ledge)` → ТО `slide(pogo, dir)`.
- КОЛИ `contact(snowball, flicker_block)` → ТО `disappear_both`, `score(50)`, `counter(extras, +2)`.
- КОЛИ `contact(snowball, jumping_ball)` → ТО `disappear_both`, `score(100)`, `counter(extras, +5)`.
- КОЛИ `contact(snowball, rolling_ball)` → ТО `disappear_a`, `freeze(rolling_ball, n)`.
- КОЛИ `contact(snowball, enemy)` → ЯКЩО `state(enemy, invulnerable)` → ТО `disappear_a`.
- КОЛИ `contact(pogo, enemy)` → ТО `custom: «Пого скинуто з виступу»`, `fall(pogo)`, `counter(technique, -2)`.
- КОЛИ `custom: «Пого впав нижче першого виступу»` → ТО `lives(-1)`, `respawn(pogo, base)` (?).
- КОЛИ `custom: «Пого вперше досяг нового поверху»` → ТО `score(n)` — очки за висоту, вище = більше.
- КОЛИ `timer(tower_limit)` → ТО `lives(-1)` (?).
- КОЛИ `contact(pogo, top_door)` → ТО `custom: «вежа руйнується»`, `score(time_left × 10)`, `score(technique × 10)`, `score(extras × 10)`, `next_level`.
- КОЛИ `counter(score, >=, 5000·k)` → ТО `lives(+1)`.
- Бонус-етап: КОЛИ `contact(torpedo, fish)` → ТО `set_state(fish, bubbled)`; КОЛИ `contact(submarine, fish)` → ЯКЩО `state(fish, bubbled)` → ТО `pickup`, `score(50..75)`.
- Перемога: вісім веж обвалено · Поразка: життя скінчились · Рахунок: висота + постріли + бонуси кінця вежі (час, «техніка», постріли) + риба.

## Керування і ввід
- Джойстик (C64 — порт 2): ліво/право — ходьба (обертання вежі); вгору — увійти в тунель/двері або підняти ліфт; вниз — опустити ліфт.
- Одна кнопка вогню з подвійним сенсом: на місці — кинути сніжку, у русі — стрибнути (так само в клоні Toppler: Space).
- C64: P — пауза (вогонь — продовжити), Run/Stop — перервати гру.

## Вікна, меню, HUD
- `main-menu` (C64): F1 — один гравець, F3 — двоє по черзі, F5 / F7 — музика і звук увімк./вимк.
- `game-screen`: обертова вежа з Пого в центрі, море внизу; HUD — `score`, `lives`, `timer-countdown`, номер вежі (?).
- `end-screen` вежі — підрахунок бонусів: час, техніка, постріли (?) як окремий екран.
- `custom-window` — підводний бонус-етап (субмарина, риба, бульбашки).
- `pause-menu` — пауза P; у паузі чит-комбінація (J + ліво + вгору) відкриває вибір вежі 1–8 клавішами.
- Переходи: меню → вежа 1 → двері → бонус-етап → вежа 2 → … → вежа 8; втрата всіх життів → меню.

## Фічі поза полем
- `levels-sequential`: вісім веж; клон Toppler — дві місії по вісім веж і редактор місій (`level-editor`).
- `hotseat` — двоє гравців по черзі (F3).
- `cheat-codes`: вибір вежі, безсмертя.
- `music-toggle` / `sound-toggle`.

## Варіації й родичі
- Порти: Tower Toppler (Atari 7800, США), Castelian (NES / Game Boy, Bits Studios), Kyorochan Land (Японія); бутлег Subline. Наступник — Nebulus 2: Pogo-a-Gogo (Amiga, 1991).
- Відкритий клон Tower Toppler (Linux) з редактором місій.
- Родичі в сімʼї: [kula-world](kula-world.md) (поле, що обертається під гравцем), [head-over-heels](head-over-heels.md) (непрямий погляд на клітинне поле), [manic-miner](manic-miner.md) (кришиться підлога, ліфти-платформи), [mario-and-wario](mario-and-wario.md) (рух без «смерті від дотику» — ворог лише заважає).
- Осі: **топологія** (плоский екран / кільце-циліндр / тор); **що робить ворог** (вбиває / скидає вниз / штовхає); **кнопка дії** (окремі стрибок і постріл / одна кнопка за контекстом).

## Цікавинки для курсу
- Циліндрична сітка: координата x за модулем N і рендер «передньої половини» з гравцем по центру — 🥈 (математика проєкції, а логіка звичайна).
- Удар ворога = падіння до виступу нижче замість смерті; ціна помилки — втрачена висота й час — 📎.
- Одна кнопка вогню: стоїш — постріл, біжиш — стрибок — 🌱.
- Тунель крізь вежу як телепорт на протилежний бік кільця (+N/2) — 🌱.
- Три класи ворогів за реакцією на постріл (гине / завмирає / не реагує) — 📎 (таблиця взаємодій).
- Бонус «техніка»: старт 100, −2 за кожен дотик ворога — 📎.
- Бонус-етап між рівнями як окремий міні-режим — 🥉.

## Мапа на каталог
- Є: `move-by-input` · `gravity-fall` · `wrap-edges` (кільце) · `carrier-platform` (ліфт) · `floor-types` (слизький виступ) · `projectile-shot` · `shoot-forward` · `teleport` · `teleport-pair` (тунель) · `enemy-patrol` · `environment-death` (море) · `player-death` · `time-out` · `time-bonus` · `event-points` · `extra-life-threshold` · `reach-exit` (двері нагорі) · `sequential-levels` · `hot-seat` · `cheat-codes` · `game-pause` · `music-toggle` · `status-panel` · `game-screen` · `keyboard-controls`.
- **Нема** → пропозиції карток:
  - `+crumbling-floor` «Підлога кришиться під ногами» · entities/interact · 🌱 (уже пропонована в manic-miner).
  - `+knockback` «Удар ворога скидає вниз замість смерті» · entities/combat · 📎.
  - `+cylinder-tower-view` «Сітка-циліндр з рендером передньої половини» · interface/render · 🥈 · слот {columns}.
  - `+context-fire-jump` «Одна кнопка: на місці — постріл, у русі — стрибок» · interface/input · 🌱.
  - `+height-score` «Очки за новий рекорд висоти» · game-logic/score · 🌱.
  - `+technique-bonus` «Бонус бездоганності: мінус за кожен дотик» · game-logic/score · 🌱 · слоти {start, penalty}.
  - `+bonus-stage` «Бонус-етап між рівнями» · game-logic/progress · 🥉.
  - `+shot-stops-enemy` «Постріл зупиняє невбивного ворога на N секунд» · entities/combat · 🌱.

## Пропозиції до словників
- `+axis:field=cylinder` — сітка, загорнута по горизонталі в кільце, без вертикального загортання (Nebulus); окремо від тору.
- `+effect:knock_down(a, to)` — скинути сутність з опори на нижчий рівень (без шкоди).
- `+trigger:landed(a)` — сутність приземлилась після падіння (вже пропоновано в manic-miner; тут — для очок висоти й смерті у воді).
- `+role:tunnel` — прохід крізь стіну на протилежний бік поля.
- `+feature:bonus-stage` — міні-гра між рівнями з окремими правилами.
- `+ui:technique-counter` — лічильник бездоганності, видимий у підсумку вежі.
- `+card:cylinder-tower-view`, `+card:context-fire-jump`, `+card:technique-bonus` — див. вище.

## Джерела
- ⭐ [Wikipedia: Nebulus](https://en.wikipedia.org/wiki/Nebulus_(video_game)) — мета, обертання вежі, виступи-сходи й ліфти, вороги-фігури (частину можна збити), удар = падіння на виступ нижче, утоплення, двері нагорі, субмарина, порти й назви.
- [C64-Wiki: Nebulus](https://www.c64-wiki.com/wiki/Nebulus) — вісім веж, тунелі за «вгору», платформи, що кришаться й ковзають, ліфти; три класи ворогів з очками; бонуси кінця вежі (час ×10, техніка 100 −2, постріли); життя за 5000; 30 риб по 50–75; клавіші F1–F7, P; чіт.
- [man toppler(6)](https://dyn.manpages.debian.org/trixie/toppler/toppler.6.en.html) — клон Tower Toppler: двері кнопкою «вгору», вужчі ліфти, сніжка на місці / стрибок у русі, бульбашка для риби, дві місії.
- [oldgames.sk: Nebulus](https://www.oldgames.sk/en/game/nebulus/docs/) — «вежа кругла, країв нема», Пого в центрі.
- YouTube: пошук «Nebulus C64 gameplay».

## Непевне
- (?) Тунель веде саме на протилежний бік вежі — лише з одного пошукового підсумку; C64-Wiki каже тільки «вгору — увійти в тунель».
- (?) Що стається, коли вичерпано час вежі (втрата життя чи кінець гри); де відроджується Пого після утоплення.
- (?) Затримка перед зникненням виступу, що кришиться; чи він відновлюється.
- (?) Кількість стовпців кільця й висота веж — не знайдено; поле, ймовірно, клітинне лише логічно (рух піксельний).
- (?) Перелік невразливих істот (очі, «молекули», літаючі фігури) і їхні траєкторії — джерела кажуть лише «basic geometric shapes», «disembodied eyeballs».
- (?) Підсумок вежі як окремий екран і склад HUD — з памʼяті.
- (?) ZX Spectrum-версія без бонус-етапу (Wikipedia); чи є він у NES/GB — не перевірено.
