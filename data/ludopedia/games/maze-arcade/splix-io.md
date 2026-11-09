---
title: Splix.io
slug: splix-io
aka: [splix, Сплікс]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: online
  info: partial
  random: runtime
  goal: territory
year: 2016
platforms: [web, mobile]
links:
  - {kind: play, url: "https://splix.io", best: true, note: "грати в браузері; на головній — керування, пауза P, статистика, сервери, скіни"}
  - {kind: other, url: "https://github.com/Jespertheend/splix", note: "відкритий код (MIT, Deno): клієнт, ігровий сервер, адмінка"}
  - {kind: other, url: "https://raw.githubusercontent.com/Jespertheend/splix/main/gameServer/src/gameplay/Player.js", note: "правила вбивств, паузи, сліду, очок, лаг-відкату"}
  - {kind: other, url: "https://raw.githubusercontent.com/Jespertheend/splix/main/gameServer/src/gameplay/arenaWorker/updateCapturedArea.js", note: "алгоритм заливки захопленої області"}
  - {kind: other, url: "https://raw.githubusercontent.com/Jespertheend/splix/main/gameServer/src/config.js", note: "константи: швидкість, спавн, відкат, мінікарта, лідерборд, режими"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=splix.io+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-auto, move-4dir, no-reverse-turn, touch-death, player-death, self-collision, online-multiplayer, simultaneous-versus, spawn-random-cell, player-camera, minimap-radar, leaderboard, score-records, profile-stats, end-screen, main-menu, game-screen, avatar-picker, theme-select, game-pause, keyboard-controls, event-points, undo-step, +territory-capture, +region-fill, +trail-vulnerable, +death-drops-territory, +lag-rewind, +pause-vulnerable, +no-encircle-player, +spectator-mode, +kill-arena-mode]
proposes: ["+effect:leave_trail", "+effect:clear_trail", "+trigger:return_home", "+cond:in_own_zone", "+role:trail", "+ui:live-ranking", "+card:lag-rewind", "+card:pause-vulnerable", "+card:no-encircle-player", "+card:spectator-mode", "+card:kill-arena-mode", "+feature:honk", "+cond:trailing"]
author: opus
date: 2026-11-09
---

# Splix.io — Paper.io на квадратній сітці: виїжджай зі своєї землі, обводь, повертайся; заморозься — і стань мішенню

## Суть
Квадратик на великій клітинній мапі з сотнями клітин і десятками гравців. Поки він на своїй землі — безпечний; поза нею лишає слід, і будь-хто, хто наїде на цей слід, убиває власника. Повернення додому заливає все обведене (включно з чужою землею). Відмінність від `paper-io`: строга 4-напрямна сітка, пауза-«заморожування», що робить вразливим навіть удома, заборона обвести іншого гравця і відкритий код серверa з лаг-відкатом ходів.

## Поле і час
- Квадратна сітка 600×600 клітин (за замовчуванням у коді); край мапи — смертельна межа.
- Стан клітини: `-1` межа · `0` нічия · `id` власника; слід — окремий список вершин у гравця, не в клітинах.
- Камера за гравцем: гарантовано видно квадрат 20×20 клітин навколо + `minimap` усієї мапи (оновлюється чвертями щосекунди).
- Real-time: швидкість 0,006 клітини/мс (≈6 клітин/с); крок — цілою клітиною.
- Режим arena: у центрі «яма» 16×16, межа ями вбиває й не заливається.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | колір, візерунок, імʼя | безперервний рух 4 напрямки; поза своєю землею лишає слід |
| Інший гравець | enemy | — | та сама фізика; ботів у коді нема |
| Територія | zone | власник | безпечна для власника в русі; обведена — переходить до того, хто обвів |
| Слід | hazard | власник, вершини | дотик іншого — смерть власника; дотик власника — самогубство |
| Стартова ділянка | zone | 5×5 | видається при спавні |
| Межа мапи | static | — | вихід на неї — смерть без кредиту вбивці |
| Яма (arena) | hazard | 16×16 | межа ями вбиває, не заливається |
| Глядач | neutral | — | бачить мапу, не грає, не має землі |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(player, facing)` на 1 клітину, коли накопичено прогрес ≥ 1.
- КОЛИ `input(dir)` → ЯКЩО `not custom: «та сама вісь, що й зараз»` → ТО `face(player, dir)`; розворот і повтор — ігноруються.
- КОЛИ `leave(player, own_zone)` → ТО `custom: «починає слід»` (`+effect:leave_trail`).
- КОЛИ `enter(player, own_zone)` → ЯКЩО `custom: «має слід»` → ТО `fill(region)`, `set_side(region_cells, player)`, `clear_trail`.
- Заливка: `custom: «BFS ззовні рамки + від сусідів кожного іншого гравця; недосяжне — твоє»` — не можна обвести клітину, де стоїть інший гравець, і перший вузол його сліду.
- КОЛИ `contact(a, trail_of_b)` → ЯКЩО `state(b, trailing) or state(b, paused)` → ТО `custom: «b гине»`, `counter(kills_a, +1)`.
- КОЛИ `contact(player, own_trail)` → ТО `custom: «самогубство»`, `lose` (останні сегменти біля голови не рахуються).
- КОЛИ `contact(a, b)` в одній клітині → ЯКЩО `state(a, trailing) and state(b, trailing)` → ТО гинуть обидва.
- КОЛИ `contact(a, b)` → ЯКЩО `state(b, paused)` → ТО `custom: «b гине навіть на своїй землі»`.
- КОЛИ `edge(player)` → ТО `lose` без кредиту вбивці; arena: `contact(player, pit_border)` → `lose`.
- КОЛИ `input(pause)` → ТО `set_state(player, paused)`, `freeze(player)`; знову — рух далі; з паузи на сліді не можна розвернутися назад у слід.
- КОЛИ `died(b)` → ЯКЩО `timer(>, 600ms)` → ТО `custom: «уся земля b стає нічиєю»`, `game_over` для b; раніше — смерть можна відкотити (лаг).
- КОЛИ `custom: «клієнт повідомив позицію з минулого»` → ЯКЩО `custom: «≤ 5 клітин і ≤ 600 мс»` → ТО `undo` подій (вбивств, старту сліду).
- Arena/drawing: КОЛИ `custom: «гравець повернув назад по своєму сліду»` → ТО `clear_trail` — скасування сліду без заливки.
- КОЛИ `spawned(player)` → ТО `spawn_at(player, random)`, `fill(5×5)`; default — напрям за стінами (?); arena — стоїть на паузі.
- Рахунок: `score = клітини + 500 × вбивства`; arena — рейтинг за вбивствами; drawing — без вбивств.
- Перемога: нема (нескінченна сесія; ранг #1) · Поразка: чужий хід по твоєму сліду, свій слід, межа, лоб у лоб на слідах, удар у замороженого.

## Керування і ввід
- Стрілки / WASD (?) — абсолютний напрям; утримати одну стрілку й натиснути другу — друга запамʼятовується і спрацює на наступній клітині (черга ходу).
- `P` — пауза-заморожування; `O` — сховати лідерборд; `M` — сховати інших глядачів.
- «Гудок» (honk) — звук для гравців поруч.
- Мобільні: свайпи (?).

## Вікна, меню, HUD
- `main-menu`: поле імені, вибір кольору й візерунку (`skin-select`), список серверів (офіційні, Legacy, неофіційні), «Last game» / «Best game», новини й changelog, перемикачі Quality / Ugly mode / Spectator mode.
- `game-screen`: камера за гравцем, `minimap`, `+ui:live-ranking` (топ-10 і загальна кількість гравців, щотри секунди).
- `end-screen`: Kills, Blocks captured, Score, Rank, час на першому місці, макс. слід.
- `leaderboard`: глобальні рекорди (/leaderboards) — рахуються лише при ≥ 10 гравцях на сервері; локальні рекорди.
- Переходи: main-menu → game-screen → (смерть) end-screen → main-menu.

## Фічі поза полем
- `online-multiplayer` з вибором сервера; власний сервер з відкритого коду (`ws://localhost:8080`).
- Режими сервера: default (очки), arena (яма, рейтинг за вбивствами, старт на паузі), drawing (без вбивств, скасування сліду); командний режим прибрано як зламаний.
- `spectator` — режим глядача.
- `custom-skins`: 12 безкоштовних кольорів (випадкові, якщо збігаються з чужими), платний візерунок і колір за підписку.
- `leaderboard-online` + `leaderboard-local`; `stats` на end-screen.

## Варіації й родичі
- Paper.io (див. `paper-io`) — та сама ідея, але Paper.io 2 з вільним кутом і ботами; Splix — строга сітка й живі гравці.
- Xonix / Qix (див. `xonix`) — заливка відрізаного, вразливий слід; там вороги-мʼячі.
- Tron Light Cycles (див. `tron-light-cycles`) — слід як небезпека; там уже коротко згадано Splix.
- **Осі варіацій:**
  - хто гине при дотику сліду: власник (тут) / той, хто вʼїхав (Tron);
  - заливка: усе обведене / без клітин з іншими гравцями (тут) / без ворогів (Xonix);
  - удома безпечно: завжди / лише в русі (тут: пауза = вразливість);
  - мета сесії: % поля / очки з вбивствами / вбивства (arena).

## Цікавинки для курсу
- Заливка через інвертований BFS: заливаєш «зовнішнє» від кута рамки, решта — твоє; власні клітини — стіни — 🥈.
- Інші гравці як додаткові «зовнішні» насіння BFS — не можна обвести живого — 🥉: один рядок змінює гру.
- Слід як список вершин (лише повороти) замість клітин; перевірка «точка на ламаній» — 📎.
- Лаг-відкат: історія подій гравця, відкат вбивств у вікні 600 мс / 5 клітин — 👑.
- Пауза як ризик (заморожений гине навіть удома) — 🌱.
- Черга одного наступного повороту — 🌱.

## Мапа на каталог
- Є: `move-auto` · `move-4dir` · `no-reverse-turn` · `touch-death` · `player-death` · `self-collision` · `online-multiplayer` · `simultaneous-versus` · `spawn-random-cell` · `player-camera` + `minimap-radar` · `leaderboard` + `score-records` + `profile-stats` · `end-screen` · `main-menu` · `game-screen` · `avatar-picker` + `theme-select` (колір/візерунок) · `game-pause` (пауза-заморожування) · `keyboard-controls` · `event-points` · `undo-step` (лаг-відкат — лише як аналог).
- **Нема** → пропозиції карток:
  - `+territory-capture`, `+trail-vulnerable`, `+region-fill`, `+death-drops-territory` (запропоновано в `tron-light-cycles`, `xonix`, `paper-io`).
  - `+lag-rewind` «Відкат подій на сервері за запізнілим вводом» · game-logic/history · 👑 · слоти {max_ms, max_tiles}.
  - `+pause-vulnerable` «Пауза = вразливість» · game-logic/difficulty · 🌱.
  - `+no-encircle-player` «Не можна обвести іншого гравця» · entities/interact · 🥉.
  - `+spectator-mode` «Режим глядача» · game-logic/opponent · 📎.
  - `+kill-arena-mode` «Режим-арена: рейтинг за вбивствами» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:leave_trail`, `+effect:clear_trail`, `+trigger:return_home`, `+cond:in_own_zone`, `+role:trail`, `+ui:live-ranking` — підтверджую з `paper-io` / `tron-light-cycles`.
- `+cond:trailing` — сутність зараз поза своєю землею з відкритим слідом (у реченнях — `state(b, trailing)`).
- `+feature:honk` — звуковий сигнал іншим гравцям поруч.
- `+card:lag-rewind`, `+card:pause-vulnerable`, `+card:no-encircle-player`, `+card:spectator-mode`, `+card:kill-arena-mode`.

## Джерела
- ⭐ [splix.io](https://splix.io) — грати; керування (стрілки, запамʼятовування напряму, P, O, M), статистика, сервери, скіни, changelog (open source, прибрано Teams).
- [GitHub: Jespertheend/splix](https://github.com/Jespertheend/splix) — MIT, Deno, клієнт + сервер + адмінка, запуск власного сервера.
- [Player.js](https://raw.githubusercontent.com/Jespertheend/splix/main/gameServer/src/gameplay/Player.js) — заборона розвороту, слід, вбивства (лише trailing/paused), лоб у лоб, самогубство, межа, смерть знищує землю, очки `клітини + 500 × вбивства`, відкат.
- [updateCapturedArea.js](https://raw.githubusercontent.com/Jespertheend/splix/main/gameServer/src/gameplay/arenaWorker/updateCapturedArea.js) — BFS заливки ззовні з насінням від інших гравців, чужа земля всередині захоплюється, упаковка в прямокутники.
- [config.js](https://raw.githubusercontent.com/Jespertheend/splix/main/gameServer/src/config.js) — 0,006 клітини/мс, спавн-радіус 2, відкат 600 мс / 5 клітин, мінікарта 4×250 мс, лідерборд 3 с, ≥ 10 гравців для глобального, режими default/arena/drawing.
- YouTube: пошук «splix.io gameplay».

## Непевне
- (?) Початковий напрям у default: код рахує відстані до чотирьох стін, але чи бере найближчу чи найдальшу — неясно.
- (?) WASD і свайпи на мобільних — головна сторінка називає лише стрілки.
- (?) Розмір 600×600 — дефолт конструктора `Game`; реальні сервери можуть мати інший.
- (?) Режим drawing — лише «без вбивств» і скасування сліду; інше не перевірено.
