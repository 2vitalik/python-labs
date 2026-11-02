---
title: Loco-Motion (Guttang Gottong)
slug: loco-motion
family: maze-arcade
also: [push-slide, connect-rotate]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: collect
year: 1982
platforms: [arcade, Intellivision, Tomy Tutor, MSX (Crazy Train), Game Boy (Konami GB Collection), Switch/PS4 (Arcade Archives)]
links:
  - {kind: play, url: "https://archive.org/details/arcade_locomotn", best: true, note: "Internet Arcade — грати аркаду; опис accelerator/panic, Crazy Trains, Loop Sweepers, Crazy Tracks"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Loco-Motion_(video_game)", note: "правила: тупики, Loop Sweeper, таймери станцій, спецплитки, порти"}
  - {kind: official, url: "https://www.nintendo.com/us/store/products/arcade-archives-guttang-gottong-switch/", note: "Arcade Archives — дві версії з різними правилами"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=loco-motion+1982+arcade+gameplay", note: "пошук; геймплей аркади"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=guttang+gottong+arcade+archives", note: "пошук; перевидання Hamster"}
stage: v1
coverage: 60
mechanics: [move-auto, environment-death, player-death, spawn-schedule, event-points, time-bonus, collect-all, sequential-levels, progress-acceleration, difficulty-levels, game-screen, status-panel, leaderboard, hot-seat, +sliding-tile-board, +path-preview, +track-follow, +station-countdown, +loop-punisher, +enemy-collision-destroy, +random-exit-junction, +panic-reroll, +extra-life-threshold, +boost-button]
proposes: ["+effect:slide_tile", "+effect:reroll_tile", "+trigger:loop_closed", "+trigger:collide", "+cond:ports_match", "+role:conduit", "+role:hazard", "+ui:path-preview", "+ui:station-timer", "+feature:operator-settings", "+card:sliding-tile-board", "+card:loop-punisher"]
author: opus
date: 2026-11-02
---

# Loco-Motion — «пʼятнашки» з колією під потягом, що ніколи не зупиняється

## Суть
Поле — рамка з плиток-колій і однією порожньою клітиною, як у «пʼятнашках». Гравець зсуває плитки в дірку, а потяг тим часом **безупинно їде** по колії; треба встигати добудовувати шлях перед ним і провезти його через усі станції по краях. Гравець не керує потягом напряму — він керує полем під ним (лише прискорює). Небезпеки — тупики, край дірки, божевільні потяги й «підмітач» замкнених петель.

## Поле і час
- Прямокутна рамка з плиток колії (розмір змінюється від рівня до рівня — «більша або менша»), одна клітина порожня. Станції — по зовнішніх краях рамки.
- Real-time: потяг рухається з постійною швидкістю (кнопка прискорює); зсув плитки — миттєвий крок гравця.
- Колія від потяга до найближчого тупика підсвічується жовтим — це превʼю маршруту, що оновлюється при кожному зсуві.
- 4 швидкості гри — налаштування оператора (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Потяг | player | життя | їде по колії сам, не зупиняється; кнопка — прискорення |
| Плитка колії | conduit | форма (пряма, поворот, хрест…) | зсувається в сусідню порожню клітину |
| Порожня клітина | static | 1 на полі | куди зсуваються плитки; край дірки — смертельний для потяга |
| Тупик-барикада | hazard | — | потяг у неї — втрата життя |
| Барʼєр на краю поля | hazard | — | так само |
| Станція | pickup | пасажири, таймер (іноді) | зібрати пасажирів = проїхати крізь неї |
| Бонус-таймер станції | static (HUD у полі) | відлік від ~2470 | залишок → очки; 0 → Crazy Train або вибух станції |
| Crazy Train | enemy | — | з'являється з прострочених станцій, їде колією, зіткнення — смерть |
| Loop Sweeper | enemy | — | зʼявляється, якщо потяг кілька секунд кружляє по замкненій петлі; наздоганяє потяг |
| Спецплитка (Crazy Track) | conduit | 1 вхід, 3 виходи | вихід випадковий; бонус за проїзд |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `custom: «сусідня до дірки плитка у напрямку dir»` → ТО `custom: «slide_tile — плитка переходить у дірку»`.
- КОЛИ `tick` → ТО `move(train, track_dir)` — потяг іде за формою плитки, на якій стоїть.
- КОЛИ `input(button)` → ТО `speed(train, ×k)` поки натиснуто (?).
- КОЛИ `contact(train, dead_end|edge_barrier)` → ТО `lose` (життя −1).
- КОЛИ `custom: «потяг виїжджає на ребро порожньої клітини»` → ТО `lose`.
- КОЛИ `contact(train, station)` → ТО `pickup(passengers)`; ЯКЩО `state(station, countdown)` → ТО `score(timer_left)`.
- КОЛИ `counter(station_timer, ==, 0)` → ЯКЩО `occupied(station, passengers)` → ТО `spawn_at(crazy_train, station)`; інакше `set_cell(station, barrier×2)`.
- КОЛИ `custom: «потяг кілька секунд їде по замкненій петлі»` → ТО `spawn(loop_sweeper)` позаду; `contact(sweeper, train)` → `lose`.
- КОЛИ `contact(crazy_train|sweeper, crazy_train|sweeper)` → ТО `disappear_both`, `set_cell(here, dead_end)`; у станції — станція знищена.
- КОЛИ `contact(train, crazy_track)` → ТО `move(train, rng(3 exits))`, `score(n)`.
- КОЛИ `input(panic)` → ТО `custom: «плитку під потягом замінено випадковою»` (за описом Internet Arcade).
- КОЛИ `all_gone(passengers)` → ТО `win` рівня, `next_level` (новий розмір рамки, більше тупиків, частіші бонус-станції, на старті можуть бути Crazy Trains).
- Перемога: нема (нескінченна аркада). Поразка: 0 життів. Рахунок: бонус станцій + спецплитки; життя +1 на 10 000.

## Керування і ввід
- 4-позиційний джойстик: напрямок = яку плитку засунути в дірку (зсув «до дірки»), а не рух аватара.
- Кнопка Accelerate — прискорити потяг (зупинити не можна).
- Кнопка Panic (за описом Internet Arcade) — випадкова заміна плитки під потягом (?).
- Ключова навичка — тримати жовтий превʼю-шлях довшим, ніж час до тупика.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` — демо і таблиця рекордів (аркада).
- `game-screen` — рамка з плитками, станції по краях; HUD: `score`, `hi-score`, `lives`, `level-number`, `path-preview` (жовта підсвітка маршруту), таймери над станціями (`custom: «station-timer»`).
- `leaderboard` — ввід ініціалів після GAME OVER.
- Переходи: attract → (монета) game-screen → (усі пасажири) наступний рівень → (0 життів) ініціали → attract.

## Фічі поза полем
- `levels-sequential` + `progress-acceleration` (розмір рамки, тупики, Crazy Trains на старті).
- `hotseat` — 2 гравці по черзі; `operator-settings` — 4 швидкості гри (?).
- `leaderboard-local`; Arcade Archives: `leaderboard-online`, налаштування складності, дві версії правил (`custom-rules`).

## Варіації й родичі
- Порти: Intellivision (Mattel), Tomy Tutor, MSX під назвою Crazy Train, Game Boy у Konami GB Collection; клон Happy Trails (Activision, Carol Shaw); сиквел Cue Brick (1989).
- Родичі: «пʼятнашки» (зсув у дірку), Pipe Mania (будуй трубу перед потоком), Railbound/Cosmic Express (колія + пасажири, але покроково), Labyrinth (зсув колони плиток).
- Осі: **хто керує рухом** — аватар (Pac-Man) / поле під автоматичним актором (тут) / програма (Railbound); **як змінюється поле** — зсув у дірку / поворот плитки / вставка ряду; **що карає за «безпечне кружляння»** — Loop Sweeper, Enrage, таймер.

## Цікавинки для курсу
- Пʼятнашки + автоматичний актор, що йде по з'єднаннях плиток: пазл у real-time — 🥉 (рух за портами плитки + зсув у дірку).
- Превʼю маршруту до першого тупика (обхід колії від потяга) — 📎, гарне завдання на трасування графа.
- Таймер станції з двома наслідками (є пасажири → ворог; нема → станція руйнується в барʼєри) — 📎.
- Loop Sweeper: детекція «кружляє по замкненому циклу N секунд» і покарання — 🥉 (виявлення циклу в шляху).
- Зіткнення двох ворогів знищує обох і лишає тупик — поле деградує від подій — 🌱.
- Спецплитка з випадковим виходом — 🌱.

## Мапа на каталог
- Є: `move-auto` (потяг) · `environment-death` (тупик, край дірки) · `player-death` · `spawn-schedule` (Crazy Train за таймером станції) · `event-points` · `time-bonus` (залишок таймера) · `collect-all` (усі пасажири) · `sequential-levels` · `progress-acceleration` · `difficulty-levels` · `game-screen` · `status-panel` · `leaderboard` · `hot-seat`.
- **Нема** → пропозиції карток:
  - `+sliding-tile-board` «Пʼятнашки: зсув плитки в порожню клітину» · entities/legality · 🥉 · слот {holes: n}.
  - `+track-follow` «Сутність їде за зʼєднаннями плитки під собою» · entities/move · 🥉 (родич `+flow-propagation` Pipe Mania).
  - `+path-preview` «Підсвітка шляху до першого тупика» · interface/hud · 📎.
  - `+station-countdown` «Ціль із таймером: бонус або покарання» · game-logic/score · 📎 · слот {on_expire: spawn|destroy}.
  - `+loop-punisher` «Ворог за кружляння по петлі» · game-logic/waves · 🥉 · слот {seconds}.
  - `+enemy-collision-destroy` «Вороги знищують один одного при зіткненні» · entities/combat · 🌱.
  - `+random-exit-junction` «Розвилка з випадковим виходом» · entities/move · 🌱.
  - `+panic-reroll` «Кнопка-паніка: випадкова заміна плитки» · entities/interact · 🌱.
  - `+boost-button` «Прискорення поки натиснуто» · entities/state · 🌱.
  - `+extra-life-threshold` (вже пропонована Pac-Man) — життя на 10 000.

## Пропозиції до словників
- `+effect:slide_tile` — плитка переходить у сусідню порожню клітину (≠ `shift` ряду, ≠ `push`).
- `+effect:reroll_tile` — замінити плитку випадковою (Panic).
- `+trigger:loop_closed` — актор N тіків рухається по замкненому циклу.
- `+trigger:collide` (вже пропонована Railbound) — зіткнення двох рухомих сутностей.
- `+cond:ports_match` (вже Pipe Mania) — вихід плитки стикується з входом сусідньої.
- `+role:conduit` (🔥 корпус) — плитка колії; `+role:hazard` — тупик/барʼєр.
- `+ui:path-preview` — жовта підсвітка маршруту; `+ui:station-timer` — таймер просто над обʼєктом поля.
- `+feature:operator-settings` — швидкість гри DIP-перемикачами.
- `+card:sliding-tile-board`, `+card:loop-punisher` — див. вище.

## Джерела
- ⭐ [Internet Arcade: Loco-Motion](https://archive.org/details/arcade_locomotn) — грати в браузері; accelerator і panic, Crazy Trains, Loop Sweepers, Crazy Tracks, 4 швидкості.
- [Wikipedia: Loco-Motion](https://en.wikipedia.org/wiki/Loco-Motion_(video_game)) — жовтий превʼю-маршрут, тупики й край дірки, Loop Sweeper, таймери станцій (бонус від 2470), станція → 2 барʼєри, спецплитки 1→3, порти, Cue Brick.
- [Arcade Archives Guttang Gottong (Nintendo)](https://www.nintendo.com/us/store/products/arcade-archives-guttang-gottong-switch/) — офіційне перевидання, дві версії з різними правилами, онлайн-рекорди.
- YouTube: пошуки «loco-motion 1982 arcade gameplay», «guttang gottong arcade archives».

## Непевне
- (?) Розмір рамки в плитках і повний набір форм плиток (пряма/поворот/хрест) — у джерелах не названо.
- (?) Кнопка Panic: є в описі Internet Arcade, але Wikipedia згадує лише accelerator, а метадані — одну кнопку; можливо, лише в одній із версій.
- (?) Хто саме з'являється з прострочених станцій — Crazy Train (Wikipedia) чи також Loop Sweeper (Internet Arcade).
- (?) Чи прискорення — утримання кнопки чи перемикач; «4 швидкості» — режим гри чи DIP оператора.
- (?) Різниця правил між Guttang Gottong і Loco-Motion у збірці Arcade Archives.
