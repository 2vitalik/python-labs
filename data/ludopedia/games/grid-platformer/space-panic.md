---
title: Space Panic
slug: space-panic
aka: [Apple Panic (клон), Panic]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: score
year: 1980
platforms: [arcade (Universal), ColecoVision, Casio PV-1000]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Space_Panic", best: true, note: "суть: ями, лопата, кілька ям по вертикалі, кисень як таймер; порти й клони"}
  - {kind: other, url: "https://www.arcade-history.com/game/2551/", note: "кабінет: 4-позиційний джойстик, 2 кнопки, 2 гравці; DIP-налаштування; дати релізу"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Apple_Panic", note: "клон Apple II: сила ворогів = кількість поверхів падіння, втеча з ями ~17 с, бонус «ворог на ворога»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Space+Panic+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 60
mechanics: [move-4dir, ladder-climb, gravity-fall, dig-terrain, chase-player, touch-death, player-death, time-out, destroy-all-enemies, event-points, sequential-levels, status-panel, hot-seat, game-screen, +dig-hole, +fill-hole, +hole-refill, +trap-escape-timer, +fall-height-kill, +stack-kill-bonus]
proposes: ["+trigger:landed", "+effect:dig", "+card:fall-height-kill", "+card:stack-kill-bonus", "+card:knock-through-hole"]
author: opus
date: 2026-11-09
---

# Space Panic — космонавт копає ями в поверхах і лопатою скидає в них прибульців, поки не скінчився кисень

## Суть
Перший «платформер» без стрибка: космонавт бігає поверхами-платформами й лазить драбинами між ними. Зброя одна — лопата: нею **копають яму в підлозі**, чекають, доки прибулець у неї впаде, і **добивають його лопатою, скидаючи крізь яму вниз**. Сильніші прибульці гинуть лише від падіння через кілька поверхів — для них ями треба вирити одна над одною. Кисень спадає, тож рівень — гонка проти часу. Нащадок top-down пастки Heiankyo Alien, предок Lode Runner.

## Поле і час
- Один нескролений екран: кілька горизонтальних платформ-поверхів, зʼєднаних драбинами; вигляд збоку.
- Клітина платформи: ціла / яма (вирита) / яма з прибульцем.
- Real-time; таймер рівня — запас кисню, що спадає.
- Гравітація діє на прибульця, якого вибили з ями: він летить униз крізь усі ями під ним.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Космонавт | player | життя | ходить уліво/вправо, лазить драбинами; копає й засипає ями; не стрибає |
| Платформа (поверх) | terrain | ціла / яма | по ній ходять; лопатою стає ямою і навпаки |
| Драбина | terrain | — | вертикальний рух між поверхами |
| Яма | terrain | порожня / з прибульцем | пастка для прибульця; засипається лопатою або прибульцем, що вибрався |
| Прибулець слабкий | enemy | сила 1 поверх | переслідує гравця; гине, впавши на 1 поверх |
| Прибулець сильніший | enemy | сила 2 поверхи | так само, але треба 2 ями одна над одною |
| Прибулець найсильніший | enemy | сила 3 поверхи | треба 3 ями по вертикалі |
| Кисень | static | запас | спадає з часом; нуль — смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(player, dir)`; вгору/вниз — лише ЯКЩО `cell(here, ladder)`.
- КОЛИ `input(dig)` → ЯКЩО `cell(front, platform)` → ТО `set_cell(front, hole)`.
- КОЛИ `input(fill)` → ЯКЩО `cell(front, hole)` і `not occupied(front, alien)` → ТО `set_cell(front, platform)`.
- КОЛИ `enter(alien, hole)` → ТО `set_state(alien, trapped)`.
- КОЛИ `input(dig)` → ЯКЩО `occupied(front, alien)` і `state(alien, trapped)` → ТО `custom: «удар лопатою; після кількох ударів прибулець провалюється крізь яму»` → `fall(alien)`.
- КОЛИ `custom: «прибулець у падінні долетів до ями нижче»` → ТО `fall(alien)` далі — ями по вертикалі складають «шахту».
- КОЛИ `custom: «прибулець приземлився, пролетівши ≥ сила поверхів»` → ТО `disappear_a`, `score(n)`.
- КОЛИ `contact(falling_alien, alien)` → ТО `disappear_both`, `score(bonus)` — бонус «ворог на ворога» (за клоном Apple Panic).
- КОЛИ `timer(escape)` → ЯКЩО `state(alien, trapped)` → ТО `clear_state(alien, trapped)`, `set_cell(hole, platform)` — вибрався й засипав яму.
- КОЛИ `contact(player, alien)` → ЯКЩО `not state(alien, trapped)` → ТО `lives(-1)`.
- КОЛИ `timer(every)` → ТО `counter(oxygen, -1)`; КОЛИ `counter(oxygen, ==, 0)` → ТО `lives(-1)`.
- КОЛИ `all_gone(alien)` → ТО `win` рівня, `next_level`.
- Перемога: нема (аркадний цикл рівнів). Поразка: 0 життів. Рахунок: за кожного вбитого прибульця, бонус за «ворог на ворога» і, ймовірно, за залишок кисню (?).

## Керування і ввід
- 4-позиційний джойстик: ліво/право — хід, вгору/вниз — драбина.
- 2 кнопки: копати і засипати (у клоні Apple Panic — так само копання й засипання).
- Яма копається в клітині перед космонавтом у напрямку погляду.
- 2 гравці по черзі (hot-seat).

## Вікна, меню, HUD
- `attract-demo` — аркадний показ без вводу (?).
- `game-screen`: поверхи й драбини + HUD: `score`, `hi-score`, `lives`, смуга кисню (`energy-bar`), номер рівня.
- `end-screen` — game over.
- Переходи: монета → гра → (усіх прибульців знищено) наступний рівень → (0 життів) game over → атракт.

## Фічі поза полем
- `levels-sequential`: рівні з наростанням кількості й сили прибульців.
- `hotseat`: 2 гравці по черзі.
- `operator-settings`: DIP-перемикачі автомата (5 налаштувань за arcade-history).
- Збережень, меню, редактора нема.

## Варіації й родичі
- Предок: Heiankyo Alien (1979) — те саме «викопай-засип» зверху; Space Panic додав поверхи, драбини й гравітацію.
- Клони: Apple Panic (1981, Apple II), Cuthbert Goes Digging, Panic 64, Roland Goes Digging, Hektik та ін.
- Нащадки: Mr. Do's Castle (1983), Lode Runner (1983, ями заростають самі), Chuckie Egg.
- Осі: **як убивають ворога** (засипати в ямі / скинути на N поверхів / ворог на ворога); **хто засипає яму** (гравець / ворог, що втік / таймер); **таймер рівня** (кисень / нема / рій замість поразки).

## Цікавинки для курсу
- Сила ворога = кількість поверхів падіння; шахта з кількох ям — 📎 (лічильник висоти падіння).
- Двокрокова пастка: яма → удар лопатою, з таймером втечі ворога — 📎.
- Ворог, що вибрався, засипає яму — стан клітини змінює і ворог, і гравець — 🌱.
- Бонус «ворог на ворога»: падіння сутності як снаряд — 🌱.
- Кисень як таймер рівня в HUD-смузі — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `ladder-climb` · `gravity-fall` (падіння ворога) · `dig-terrain` (яма в платформі) · `chase-player` · `touch-death` · `player-death` · `time-out` (кисень) · `destroy-all-enemies` · `event-points` · `sequential-levels` · `status-panel` · `hot-seat` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+fall-height-kill` «Ворог гине від падіння на ≥ N поверхів» · entities/death · 📎 · слот {floors per type}.
  - `+stack-kill-bonus` «Падаюча сутність убиває ту, на яку впала» · entities/combat · 🌱.
  - `+knock-through-hole` «Вибити застряглу сутність крізь яму» · entities/interact · 📎.
  - `+dig-hole` / `+fill-hole` / `+hole-refill` / `+trap-escape-timer` — як у Heiankyo Alien і Lode Runner.

## Пропозиції до словників
- `+trigger:landed(a, floors)` — сутність приземлилась після падіння на N поверхів/клітин (Space Panic, Prince of Persia, Fire 'n Ice).
- `+effect:dig(cell)` — перетворити підлогу на яму (Heiankyo Alien, Lode Runner, Space Panic).
- `+card:fall-height-kill`, `+card:stack-kill-bonus`, `+card:knock-through-hole` — див. вище.

## Джерела
- ⭐ [Wikipedia: Space Panic](https://en.wikipedia.org/wiki/Space_Panic) — ями, удар лопатою, кілька ям по вертикалі, кисень-таймер; порти (ColecoVision, PV-1000), клони.
- [arcade-history: Space Panic](https://www.arcade-history.com/game/2551/) — джойстик 4-way, 2 кнопки, 2 гравці, DIP, дати JP 11.1980 / US 02.1981.
- [Wikipedia: Apple Panic](https://en.wikipedia.org/wiki/Apple_Panic) — клон: засипання ям, падіння через 1/2/3 поверхи за кольором, втеча ~17 с, бонус за падіння на іншого.
- YouTube: пошук «Space Panic arcade gameplay».

## Непевне
- (?) Сила ворогів за кольором (1/2/3 поверхи) і втеча з ями ~17 с — описано для клону Apple Panic; для оригіналу підтверджено лише «пізніше треба кілька ям по вертикалі».
- (?) Чи вистачає одного удару лопатою, чи треба кілька; що буває з сильним ворогом, що впав недостатньо низько (виживає?).
- (?) Чи стає прибулець, що втік з ями, сильнішим («мутація»).
- (?) Чи може космонавт сам провалитися в яму; призначення обох кнопок саме в оригіналі (за клоном — копати / засипати).
- (?) Бонус за залишок кисню; вигляд HUD і атракт-режиму — з памʼяті.
