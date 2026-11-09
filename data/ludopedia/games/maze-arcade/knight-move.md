---
title: Knight Move
slug: knight-move
aka: [ナイトムーブ, Naito Mūbu]
family: maze-arcade
also: [chess-abstract]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1990
platforms: [Famicom Disk System]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Knight_Move", best: true, note: "поле 4×8, безупинні стрибки з вибором приземлення, плитки біла → світла → темна → дірка, серця, A/B-type, versus"}
  - {kind: official, url: "https://www.nintendo.com/jp/famicom/software/fmc-kmv/index.html", note: "сторінка Nintendo за оригінальним мануалом: 50 очок за плитку, ланцюг дірок до 100 000, B-type 3+ сердець, 2P — прапорці"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ナイトムーブ", note: "JA: 32 клітини, кольори плиток, кнопка A — прискорення з очками, B-type — 3 серця, серце переїжджає кожні 6 кроків"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Knight+Move+Famicom+Disk+System+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [piece-move-patterns, legal-move-highlight, move-auto, environment-death, player-death, item-pickup, event-points, combo-multiplier, sequential-levels, progress-acceleration, mode-select, game-screen, end-screen, +crumbling-floor, +hover-choose-landing, +pickup-restores-floor, +moving-goal-countdown, +hold-speed-bonus, +round-wins-match, +shared-field-versus]
proposes: ["+cond:airborne", "+ui:relocation-countdown", "+card:hover-choose-landing", "+card:pickup-restores-floor", "+card:moving-goal-countdown", "+card:hold-speed-bonus"]
author: opus
date: 2026-11-09
---

# Knight Move — шаховий кінь безупинно стрибає полем 4×8; кожне третє приземлення на клітину лишає дірку, серце латає підлогу

## Суть
Екшн-головоломка Олексія Пажитнова для Famicom Disk System. Кінь сам безперервно стрибає буквою «Г»; поки він висить у повітрі, гравець вибирає курсором одну з легальних клітин приземлення. Кожна клітина витримує три приземлення: біла → світла → темна → дірка, а приземлення в дірку означає падіння й кінець гри. Взяте серце відновлює всі дірки й веде в наступний раунд, де кінь стрибає швидше; очки — за зруйновані плитки, з бонусом за ланцюг дірок поспіль.

## Поле і час
- Дошка 4×8 = 32 клітини; топологія звичайна, без тора.
- Шари: плитка (стан 0/1/2 приземлення або дірка) + серце на клітині + кінь.
- Real-time: стрибки йдуть самі в темпі раунду, вибір треба встигнути за час зависання. Утримання A пришвидшує стрибки (за очки).
- Темп росте з кожним раундом (серцем). Видно все поле (`info: full`).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кінь | player | 1 життя; швидкість росте з раундом | безупинно стрибає ходом коня; приземлення обирає гравець |
| Курсор приземлення | mark | лише легальні клітини | показує, куди можна приземлитися з поточної клітини |
| Біла плитка | terrain | 0 приземлень | після приземлення → світла |
| Світла плитка | terrain | 1 приземлення | після приземлення → темна |
| Темна плитка | terrain | 2 приземлення | третє приземлення: +очки, далі — дірка |
| Дірка | hazard | — | приземлення в неї = падіння, кінець гри |
| Серце | pickup | A-type: одне, нерухоме; B-type: переїжджає кожні 6 кроків, число над ним — скільки лишилось | узяти → усі дірки знову білі, раунд +1, кінь швидшає |
| Жовтий і червоний кінь (2P) | player | контролер I / II, у кожного свій курсор | змагаються на одній дошці (?) |
| Прапорець (2P) | — | лічильник | за 5 сердець або падіння суперника; хто перший набрав 4 — переміг |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `custom: «кінь відштовхнувся»` → ТО `custom: «курсор показує легальні клітини ходу конем»` (`legal-move-highlight`).
- КОЛИ `input(choose_cell)` → ЯКЩО `custom: «кінь у повітрі»` (`+cond:airborne`) and `legal(knight_move)` → ТО `custom: «ціль приземлення = обрана клітина»`.
- КОЛИ `timer(hop)` → ТО `move(knight, target)` — приземлення за темпом раунду.
- КОЛИ `enter(knight, white)` → ТО `set_cell(cell, light)`.
- КОЛИ `enter(knight, light)` → ТО `set_cell(cell, dark)`.
- КОЛИ `enter(knight, dark)` → ТО `score(50)`, `combo(+1)`, `custom: «клітина стає діркою»` (`set_cell(cell, hole)`).
- КОЛИ `custom: «дірка зроблена»` → ЯКЩО `chain(n)` → ТО `score(growing)` — ланцюг дірок поспіль дає дедалі більше, до 100 000 за плитку (мануал).
- КОЛИ `enter(knight, light|white)` → ТО `reset_combo` (?).
- КОЛИ `enter(knight, hole)` → ТО `fall(knight)`, `game_over`.
- КОЛИ `contact(knight, heart)` → ЯКЩО `mode(A)` → ТО `set_cell(all_holes, white)`, `speed(knight, +n)`, `next_level`.
- КОЛИ `contact(knight, heart)` → ЯКЩО `mode(B)` → ТО `set_cell(all_holes, white)`, `counter(hearts, +1)`.
- КОЛИ `counter(knight_moves, ==, 6)` → ЯКЩО `mode(B)` → ТО `teleport(heart, other_cell)`, `custom: «лічильник над серцем знову 6»`.
- КОЛИ `counter(hearts, >=, quota)` → ЯКЩО `mode(B)` → ТО `next_level`, `speed(knight, +n)`, `custom: «квота росте з 3»`.
- КОЛИ `input(hold_A)` → ТО `speed(knight, ×k)`, `score(+n)` поки утримується.
- 2P: КОЛИ `counter(hearts_p, ==, 5)` → ТО `custom: «гравцю прапорець»`; КОЛИ `died(opponent)` → ТО `custom: «гравцю прапорець»`; КОЛИ `counter(flags_p, ==, 4)` → ТО `win`.
- Перемога: нема (1P — на очки) · Поразка: приземлення в дірку · Рахунок: 50 за зруйновану плитку, ланцюг дірок, бонус за прискорення кнопкою A.

## Керування і ввід
- Хрестовина — вибір однієї з легальних клітин курсором, поки кінь у повітрі (?). Кінь не стоїть: не встиг вибрати — він однаково приземлиться (куди саме — (?)).
- A (утримання) — прискорити стрибки, очки за ризик.
- 2P: кожен гравець зі свого контролера керує своїм курсором одночасно.

## Вікна, меню, HUD
- `mode-select`: A TYPE · B TYPE · 2-PLAYER.
- `game-screen`: дошка 4×8, кінь, курсор, серце; `score`, `level-number` (раунд); у B-type — `+ui:relocation-countdown` (число над серцем) і лічильник сердець до квоти (?).
- `end-screen` — падіння коня, Game Over.
- 2P-екран: два коні, рахунок прапорців.
- `splash-screen` / титул FDS (?).

## Фічі поза полем
- `mode-classic` (A TYPE), режим квоти з рухомою ціллю (B TYPE), `mode-versus` (2-PLAYER).
- `levels-sequential` раундами зі зростанням темпу; нескінченна гра на рекорд.
- Збереження рекордів на диск FDS — (?).

## Варіації й родичі
- Не плутати з `grid-platformer/knight-lore` (ізометрична пригода Ultimate) — автоматика черги зіставила хибно.
- Той самий автор: `falling-match/tetris` і `falling-match/welltris`, `falling-match/hatris`.
- Шаховий корінь: `pencil-logic/n-queens-knights-tour` — тур коня як задача; тут той самий хід, але проти часу й з руйнуванням клітин.
- Родичі за підлогою, що кришиться: `grid-platformer/manic-miner`, `push-slide/hitman-go`, `thinky/drod`; за зміною стану клітини при приземленні — `qbert`.
- **Осі варіацій:** скільки витримує клітина: 1 (crumble) / N стадій (Knight Move — 3) · що лікує підлогу: нічого / предмет-серце / таймер · хто рухає аватара: гравець / сам, гравець лише обирає ціль (Knight Move) · ціль раунду: одна нерухома / кілька, що переїжджають.

## Цікавинки для курсу
- Безупинні стрибки з вибором приземлення у вікні зависання: real-time поверх покрокового ходу — 📎.
- Хід коня як генератор легальних клітин + підсвітка — 🌱 (картка `piece-move-patterns`).
- Плитка з 3 стадіями зносу і дірка-пастка — 🌱; ланцюг дірок поспіль як комбо — 🌱.
- Серце-«ремонт»: одна подія скидає стан усіх зруйнованих клітин — 🌱.
- B-type: ціль переїжджає кожні 6 ходів, лічильник над нею — 🌱.
- Versus на одній дошці: дві незалежні черги вводу й прапорці за 5 сердець або падіння суперника — 🥉.
- Евристика «не замкнути себе»: чи лишиться з клітини хоч один хід без дірки — 📎 (пошук на 1–2 ходи вперед).

## Мапа на каталог
- Є: `piece-move-patterns` (кінь) · `legal-move-highlight` (курсор приземлення) · `move-auto` (стрибає сам, ввід обирає ціль) · `environment-death` (дірка) · `player-death` · `item-pickup` (серце) · `event-points` · `combo-multiplier` (ланцюг дірок) · `sequential-levels` · `progress-acceleration` · `mode-select` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+crumbling-floor` (вже Manic Miner, Nebulus, Hitman GO) — тут слот {stages: 3}, дірка — смерть.
  - `+round-wins-match` (вже `pac-man-battle-royale`) — 2P до 4 прапорців.
  - `+shared-field-versus` (вже `blockade`) — два коні на одній дошці.
  - `+hover-choose-landing` «Безупинні стрибки: ціль приземлення обирається в польоті» · entities/move · 📎 · слоти {pattern: knight, hover_ticks}.
  - `+pickup-restores-floor` «Предмет відновлює зруйновані клітини» · entities/interact · 🌱.
  - `+moving-goal-countdown` «Ціль переїжджає кожні N ходів, лічильник на ній» · entities/spawn · 🌱 · слот {every: 6}.
  - `+hold-speed-bonus` «Утримання кнопки пришвидшує темп за бонус-очки» · game-logic/score · 🌱.

## Пропозиції до словників
- `+cond:airborne` — сутність у повітрі / у фазі стрибка (Knight Move, Zoo Keeper).
- `+ui:relocation-countdown` — число на цілі: скільки ходів до її переїзду (B-type).
- `+card:hover-choose-landing`, `+card:pickup-restores-floor`, `+card:moving-goal-countdown`, `+card:hold-speed-bonus` — див. «Мапу на каталог».

## Джерела
- ⭐ [Wikipedia: Knight Move](https://en.wikipedia.org/wiki/Knight_Move) — поле 4×8, кінь зависає, курсор показує легальні приземлення, три стани плитки й дірка, серця, A/B-type, versus, кнопка A.
- [Nintendo: ナイトムーブ](https://www.nintendo.com/jp/famicom/software/fmc-kmv/index.html) — офіційна сторінка за мануалом: 50 очок за плитку, ланцюг дірок (максимум 100 000), B-type (3+ сердець, переїзд кожні 6 кроків, число над серцем), 2P — жовтий і червоний кінь, прапорці.
- [Wikipedia JA: ナイトムーブ](https://ja.wikipedia.org/wiki/ナイトムーブ) — 32 клітини, кольори плиток, A — прискорення з очками, серце скидає дірки, раунди швидшають.
- YouTube: пошук «Knight Move Famicom Disk System gameplay».

## Непевне
- (?) Як саме хрестовина обирає приземлення (перебір легальних клітин чи напрямок) і що стається, якщо не вибрати нічого.
- (?) Дірка виникає вже при третьому приземленні чи лише коли кінь відстрибне (за Wikipedia — третє приземлення «руйнує плитку»).
- (?) Чи обриває ланцюг дірок приземлення на білу/світлу плитку; точна прогресія очок ланцюга не знайдена.
- (?) Де зʼявляється нове серце в A-type і куди переїжджає в B-type — випадково чи за схемою.
- (?) 2P: Wikipedia — «перший до 5 сердець виграє», офіційна сторінка — 5 сердець або падіння суперника дають прапорець, до 4 прапорців; чи коні ділять одну дошку й чи можуть приземлитись на одну клітину.
- (?) Чи зберігаються рекорди на диск і чи є в 1P скінченна кількість раундів.
