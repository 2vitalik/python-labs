---
title: "Mario & Wario"
slug: mario-and-wario
family: grid-platformer
also: [thinky]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1993
platforms: ["Super Famicom + SFC Mouse (1993 Японія)", Nintendo Classics / Switch Online (2025)]
links:
  - {kind: fandom, url: "https://www.mariowiki.com/Mario_%26_Wario", best: true, note: "Super Mario Wiki — блоки, предмети, вороги, світи, бонус із літаком Варіо"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mario_%26_Wario", note: "ядро: сліпий Маріо, фея Ванда, миша, клік розвертає, 100 рівнів / 10 світів"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Mario+%26+Wario+SNES+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 65
mechanics: [cell-click, move-auto, gravity-fall, touch-death, environment-death, player-death, time-out, time-bonus, reach-exit, item-pickup, event-points, speed-per-type, level-unlock, sequential-levels, status-panel, +auto-walker-guide, +click-solidify-block, +click-turn-walker, +click-defeat-enemy, +button-toggle, +sticky-block, +periodic-block, +turn-when-blocked, +extra-life-threshold, +extra-life-pickup, +bonus-hit-minigame]
proposes: ["+effect:toggle_block", "+effect:face", "+effect:set_state", "+trigger:input", "+role:ally", "+role:terrain", "+role:hazard", "+window:character-select", "+window:map-window", "+ui:time-gauge", "+axis:control", "+card:click-solidify-block"]
author: opus
date: 2026-11-02
---

# Mario & Wario — мишею-феєю веди сліпого Маріо з відром на голові до Луїджі

## Суть
Варіо скидає Маріо на голову відро (чи інший предмет), і той, нічого не бачачи, сам іде ліворуч-праворуч. Гравець керує не героєм, а феєю Вандою через мишу Super Famicom: клік по контуру блока робить його твердим (міст чи стіна), клік по герою — розвертає його, клік по ворогу — прибирає ворога. Мета — довести героя до Луїджі, який зніме відро, поки не скінчився час. Чисте **непряме керування сліпим ходцем** на клітинному рівні.

## Поле і час
- Бічний вигляд, тайлова сітка блоків; рівень ширший за екран, прокрутка за героєм (?).
- Real-time: герой іде з постійною швидкістю (Пітч — повільно, Маріо — середньо, Йоші — швидко), блоки з таймером і «дихаючі» блоки живуть своїм циклом.
- Таймер рівня (Time Gauge); залишок часу → бонусні очки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Ванда (фея) | player | курсор миші | літає за мишею; клік діє на обʼєкт під нею |
| Маріо / Пітч / Йоші | ally | швидкість: середня / повільна / швидка | іде сам; у стіну — розвертається (?); без опори — падає |
| Луїджі | static | — | ціль: герой дійшов → відро знято, рівень пройдено |
| Контур блока | terrain | порожній ↔ твердий | клік → стає твердим блоком (міст/стіна) |
| Flip-Flop блок | terrain | — | клік перемикає твердий ↔ прохідний |
| Switch-блок | terrain | червоний / синій | перемикається між твердим червоним і прозорим синім |
| Timer-блок | terrain | тривалість | клік → твердий на короткий час, потім знову порожній |
| Rock-блок (тріснутий) | object | — | клік руйнує |
| Coin-блок | object | — | клік → монета |
| Jump-блок | terrain | — | пружина: підкидає героя |
| Nebaneba (липкий) | terrain | — | тримає і героя, і ворогів |
| Fūsen (кулька) | terrain | період | час від часу роздувається |
| Toge (шипи) | hazard | напрям 1 з 4 | шипи на всю клітину |
| Ліфт | terrain | — | везе; герой мусить чекати |
| Монета | pickup | 100 → +1 життя | очки |
| Зірка | pickup | 4 за рівень → +1 життя | найчастіший предмет |
| 1-Up гриб | pickup | — | +1 життя |
| Time-гриб | pickup | рідкісний | додає часу |
| Dodorigesu Jr. | enemy | нерухомий | знищується кліком |
| Guriguri | enemy | — | вогник, повзе вздовж стін і підлоги |
| Komorin | enemy | групи по 4 | кажани |
| Tsubōn | enemy | — | горщик на стіні, дихає вогнем |
| Unibo | enemy | синій ↕ / жовтий ↔ | їжак, патрулює вісь |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(hero, facing)`; КОЛИ `blocked(hero)` → ТО `face(hero, reverse)` (?).
- КОЛИ `input(click, hero)` → ТО `face(hero, reverse)`.
- КОЛИ `input(click, outline)` → ТО `set_cell(outline, solid)`.
- КОЛИ `input(click, flip_flop)` → ТО `custom: «toggle_block»` (твердий ↔ прохідний).
- КОЛИ `input(click, timer_block)` → ТО `set_state(block, solid, duration)`; після — порожній.
- КОЛИ `input(click, switch_block)` → ТО `set_state(switch_blocks, flip)` червоний ↔ синій (?: усі блоки разом чи один).
- КОЛИ `input(click, rock_block)` → ТО `disappear_b`; КОЛИ `input(click, coin_block)` → ТО `counter(coins, +1)`.
- КОЛИ `input(click, enemy)` → ЯКЩО ворог «клікабельний» → ТО `disappear_b` / `stun` (?).
- КОЛИ `enter(hero, jump_block)` → ТО `custom: «підкинути»`; КОЛИ `enter(any, sticky)` → ТО `freeze(a)` (?: назавжди чи на час).
- КОЛИ `custom: «нема опори»` → ТО `fall(hero)`; у прірву / воду / лаву → `lose` (?).
- КОЛИ `contact(hero, enemy|spikes|fire)` → ТО `lives(-1)`, `restart` (?).
- КОЛИ `contact(hero, star|coin|mushroom)` → ТО `pickup`; `counter(stars, ==, 4)` → `lives(+1)`; `counter(coins, ==, 100)` → `lives(+1)`; time-гриб → `timer(+n)`.
- КОЛИ `contact(hero, luigi)` → ТО `win`, `score(time_left × k)`, `next_level`.
- КОЛИ `counter(time, ==, 0)` → ТО `lose` (?).
- Після світу: бонус — Ванда молотом б'є літак Варіо: `input(click, plane)` → `counter(coins, +1)`; 40 влучань → літак ламається, Варіо тікає.
- Перемога: герой дійшов до Луїджі. Поразка: час, смерть героя (?). Рахунок: вороги, предмети, залишок часу; життя з монет/зірок/грибів.

## Керування і ввід
- Лише миша SFC: рух курсора-Ванди + клік по обʼєкту (контекстна дія за типом обʼєкта під курсором).
- Героєм напряму не керуєш: лише «розвернути» кліком по ньому.
- Права кнопка миші — (?).

## Вікна, меню, HUD
- `splash-screen` — титул.
- `character-select` — вибір героя: Пітч / Маріо / Йоші (швидкість = складність).
- `map-window` / вибір світу: на старті доступні 8 світів, 9-й і 10-й відкриваються по черзі, потім EXTRA (?: це карта чи список).
- `game-screen` — рівень; HUD: `ui:time-gauge` (шкала часу), `score`, `coins`, зірки, `lives` (?).
- `custom-window` — бонус «бий літак Варіо» (лічильник влучань і монет).
- `dialogue-window` — інтро (Варіо скидає відро) і фінал (герой скидає бочку на Варіо).
- `end-screen` — Game Over / рівень пройдено з підрахунком часу.

## Фічі поза полем
- `character-select` як `difficulty-presets` (повільна Пітч = легше встигати клікати).
- `level-unlock`: 10 світів × 10 рівнів + EXTRA × 10 після 10-го світу.
- Збереження прогресу — (?). `mouse-and-keyboard`: гра лише під мишу.

## Варіації й родичі
- Lemmings (автоходці), Troddlers (блоки на шляху автоходців, але через аватар), Mario vs. Donkey Kong: March of the Minis (міні-Маріо йдуть самі, стилус ставить блоки), Toki Tori.
- **Осі варіацій:** як впливаєш на ходця (будуєш середовище / розвертаєш його / прибираєш ворогів) · блок (постійний / таймерний / перемикач групи) · ходець (один / натовп) · швидкість ходця як складність.

## Цікавинки для курсу
- Ходець, що йде сам і розвертається від стін, + курсор, який змінює клітини — 🥉 (непряме керування: real-time ввід мишею по клітинах).
- Таймерний блок: твердий на N секунд після кліку — 📎 (стан клітини з тривалістю).
- Switch-блоки: клік перемикає всю групу кольору — 📎 (повтор `+button-toggle`).
- Липкий і «дихаючий» блоки — 🌱 кожен; гарні «дані» в таблиці типів клітин.
- Вибір героя-швидкості як складність без зміни рівнів — 🌱.

## Мапа на каталог
- Є: `cell-click` · `move-auto` (герой іде сам, ввід лише розвертає) · `gravity-fall` · `touch-death` · `environment-death` · `player-death` · `time-out` · `time-bonus` · `reach-exit` (Луїджі) · `item-pickup` · `event-points` · `speed-per-type` (Пітч/Маріо/Йоші) · `level-unlock` · `sequential-levels` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+auto-walker-guide` (як Troddlers) — вести автоходця до виходу.
  - `+click-solidify-block` «Клік робить контур твердим» · entities/interact · 📎 · слот {duration: forever|timed|toggle}.
  - `+click-turn-walker` «Клік розвертає ходця» · interface/input · 🌱.
  - `+click-defeat-enemy` «Клік прибирає ворога» · entities/combat · 🌱.
  - `+button-toggle` (повтор) — switch-блоки кольору.
  - `+sticky-block` «Липка клітина тримає всіх» · entities/interact · 🌱.
  - `+periodic-block` «Блок, що циклічно росте/зникає» · entities/state · 📎 — родич `+toggle-spikes`.
  - `+turn-when-blocked` (повтор Chip's Challenge) · слот {turn: reverse}.
  - `+extra-life-threshold` (100 монет, 4 зірки), `+extra-life-pickup` (1-Up) — повтори.
  - `+bonus-hit-minigame` «Бонус: клікай по цілі на час» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:toggle_block(cell)` (повтор Solomon's Key) — Flip-Flop; `+effect:set_state(block, solid, duration)` — таймерний блок.
- `+effect:face(hero, reverse)` — клік по герою.
- `+trigger:input(click, target)` — дія залежить від типу клітини під курсором.
- `+role:ally` (сліпий герой — головна «фігура», але не підконтрольна), `+role:terrain` (блоки), `+role:hazard` (шипи).
- `+window:character-select`, `+window:map-window` (вибір світу).
- `+ui:time-gauge` — шкала часу замість цифр.
- `+axis:control` = `indirect`: гравець — курсор, герой іде сам.
- `+card:click-solidify-block` — див. вище.

## Джерела
- ⭐ [Super Mario Wiki: Mario & Wario](https://www.mariowiki.com/Mario_%26_Wario) — 10 типів блоків, предмети й пороги життів, вороги, 10 світів + EXTRA, швидкості героїв, бонус із літаком.
- [Wikipedia: Mario & Wario](https://en.wikipedia.org/wiki/Mario_%26_Wario) — сліпий Маріо, Ванда, миша, клік по контуру/герою/ворогу, 100 рівнів, Game Freak / Тадзірі, перевидання 2025.
- YouTube: пошук «Mario & Wario SNES gameplay».

## Непевне
- (?) Чи герой розвертається, впершись у стіну, чи стоїть — Wikipedia каже лише «іде сам», розворот кліком; з памʼяті — розвертається.
- (?) Від чого саме гине герой (прірва, шипи, вороги, час) — джерела прямо не описують; тут — з памʼяті й логіки предметів (`Toge`, життя).
- (?) Switch-блок: перемикається один чи вся група кольору; Nebaneba — тримає назавжди чи на час.
- (?) Права кнопка миші, вигляд вибору світів (карта чи список), наявність збереження/паролів, склад HUD.
- (?) Рівень ширший за екран (прокрутка) — з памʼяті.
