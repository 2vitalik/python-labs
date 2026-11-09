---
title: Paper.io (Пейпер-іо) і Paper.io 2
slug: paper-io
aka: [Paper io, Paper.io 2, Пейпер іо]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: territory
year: 2016
platforms: [iOS, Android, web]
links:
  - {kind: play, url: "https://www.crazygames.com/game/paper-io-2", best: true, note: "грати в браузері + правила: захоплення, вразливий хвіст, власний хвіст = кінець, керування"}
  - {kind: official, url: "https://voodoo.io/paper2", note: "Voodoo: Paper.io 2 (paper-io.com переадресовує сюди); правил не містить"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Voodoo_(company)", note: "Paper.io 2016, Paper.io 2 2018, 266 млн завантажень"}
  - {kind: other, url: "https://www.pocketgamer.com/paper-io/paper-io-beginners-tips-how-to-survive-your-early-moments/", note: "гайд: квадрати зі сліду, удар у хвіст, лідер втрачає все"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=paper.io+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 70
mechanics: [move-auto, move-4dir, touch-death, player-death, ai-opponent, realtime-ai, spawn-random-cell, swipe-gestures, keyboard-controls, player-camera, leaderboard, avatar-picker, theme-select, game-screen, end-screen, main-menu, event-points, +territory-capture, +region-fill, +trail-vulnerable, +self-collision, +percent-goal, +death-drops-territory, +skin-unlocks, +free-angle-steering]
proposes: ["+effect:leave_trail", "+effect:clear_trail", "+trigger:return_home", "+cond:in_own_zone", "+role:trail", "+ui:territory-percent", "+ui:live-ranking", "+card:death-drops-territory", "+card:skin-unlocks"]
author: opus
date: 2026-11-09
---

# Paper.io — Xonix-онлайн: вийди зі своєї землі, обведи шматок, повернись живим

## Суть
Гравець — квадратик зі стартовою ділянкою свого кольору на великій арені з іншими гравцями. Поки він на своїй землі — безпечний; щойно виходить, за ним тягнеться хвіст, і будь-хто, хто наїде на цей хвіст, вбиває його. Повернувшись на свою землю, гравець замикає контур: усе обведене (включно з чужою фарбою) стає його. Мета — якнайбільший відсоток мапи; смерть забирає всю набрану землю.

## Поле і час
- Paper.io: квадратна арена-сітка з межею; рух клітинами в 4 напрямки (?). Paper.io 2: вільний напрям (див. `free-angle-steering`), арена може бути круглою (?).
- Камера слідує за гравцем, видно лише частину мапи (тому `info: partial`); мінікарти нема (?).
- Real-time: усі рухаються безперервно; зупинитись не можна.
- Стан клітини: нічия / територія гравця X / хвіст гравця X.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гравець | player | колір/скін | безперервний рух; поза своєю землею лишає хвіст |
| Суперник (бот або гравець) | enemy | колір | та сама фізика; полює на хвости, захоплює землю |
| Територія | zone | власник, площа | безпечна для власника; можна перефарбувати, обвівши |
| Хвіст | hazard | власник | вразливий слід поза своєю землею; дотик іншого — смерть власника; дотик власника — теж смерть |
| Межа арени | static | — | непрохідна; у Paper.io 2 вбиває лише при лобовому вʼїзді |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `tick` → ТО `move(player, dir)`; КОЛИ `input(dir)` → ТО `face(player, dir)`.
- КОЛИ `leave(player, own_zone)` → ТО `custom: «починає лишати хвіст»` (`+effect:leave_trail`).
- КОЛИ `enter(player, own_zone)` → ЯКЩО `custom: «є хвіст»` → ТО `fill(region)`, `set_side(region_cells, player)`, `custom: «хвіст стає територією»`.
- КОЛИ `contact(a, trail_of_b)` → ЯКЩО `not same(a, b, owner)` → ТО `custom: «b гине»`, `score(+kill)` для a.
- КОЛИ `contact(player, own_trail)` → ТО `lose` (game over).
- КОЛИ `died(b)` → ТО `custom: «уся територія b стає нічиєю»`, `clear_trail(b)`.
- КОЛИ `contact(a, b)` лоб у лоб → ЯКЩО `custom: «a на своїй землі»` → ТО гине b (?).
- КОЛИ `contact(player, border)` → ЯКЩО `moving(player, into_border)` → ТО `lose` (Paper.io 2).
- КОЛИ `counter(territory_percent, ==, 100)` → ТО `win`.
- КОЛИ `died(enemy)` → ТО `spawn_at(new_enemy, random)` (?) — арена не порожніє.
- Перемога: захопити всю мапу (рідко) · Поразка: хтось перетнув твій хвіст, ти перетнув власний, вʼїхав у межу · Рахунок: % території; вбивства як ціль завдань.

## Керування і ввід
- Мобільні: свайп/drag задає напрям.
- Браузер (Paper.io 2): утримати ліву кнопку миші й тягнути, або WASD / стрілки, або просто рух миші.
- Paper.io 1: 4 напрямки свайпом (?); Paper.io 2: вільний кут.

## Вікна, меню, HUD
- `main-menu`: Play, вибір скіна (`skin-select`), режими (?).
- `game-screen`: арена з камерою за гравцем; HUD — `+ui:territory-percent` (свій відсоток), `+ui:live-ranking` (топ гравців з відсотками), `popup-text` за вбивства (?).
- `end-screen`: відсоток, вбивства, місце; кнопка «ще раз»; пропозиція продовжити за рекламу (?).
- Переходи: main-menu → game-screen → (смерть) end-screen → main-menu / game-screen.

## Фічі поза полем
- `custom-skins` / `unlockables`: скіни відкриваються виконанням завдань і вбивствами.
- Завдання (objectives) — ціль на сесію (захопити %, вбити N).
- Paper.io 2: «завоювати всі країни» — мапа країн/рівнів як прогресія (?).
- Мультиплеєр: опис каже «kill other players», але чи це живі гравці, чи боти — непевно.

## Варіації й родичі
- Xonix / Qix (див. `xonix`) — обведення території слідом, вразливий незамкнений слід; там вороги — кульки, тут — інші гравці.
- Tron Light Cycles (див. `tron-light-cycles`) — слід як небезпека; там коротко згадано й Paper.io.
- Splix.io — клітинний .io-аналог; Paper.io 2 (2018) — вільний рух.
- **Осі варіацій:**
  - рух: сітка 4 напрямки / вільний кут;
  - смерть: від чужого хвоста / від свого / від межі / лоб у лоб;
  - захоплення: лише нічия земля / чужа теж перефарбовується;
  - смерть власника: територія зникає / переходить вбивці.

## Цікавинки для курсу
- Замкнення контуру й заливка області, що «всередині» сліду + своєї землі (flood fill з зовнішнього краю) — 🥈.
- Три стани клітини з власником (нічия / земля / хвіст) і перефарбування чужої — 📎.
- Вразливий хвіст: смерть того, чий хвіст, а не того, хто наїхав — 📎.
- Боти, що вирішують «скільки відійти від дому» за відстанню до ворогів — 🥇 (ризик vs винагорода в real-time AI).
- Живий рейтинг відсотків на HUD — 🌱.

## Мапа на каталог
- Є: `move-auto` · `move-4dir` · `touch-death` · `player-death` · `ai-opponent` + `realtime-ai` · `spawn-random-cell` · `swipe-gestures` · `keyboard-controls` · `player-camera` · `leaderboard` · `avatar-picker` + `theme-select` (скіни) · `game-screen` · `end-screen` · `main-menu` · `event-points`.
- **Нема** → пропозиції карток:
  - `+territory-capture`, `+trail-vulnerable` (запропоновано в `tron-light-cycles`).
  - `+region-fill`, `+percent-goal` (запропоновано в `xonix`).
  - `+self-collision` (запропоновано в `snake`).
  - `+free-angle-steering` (запропоновано в `achtung-die-kurve`) — Paper.io 2.
  - `+death-drops-territory` «Смерть знищує всю територію власника» · entities/death · 📎.
  - `+skin-unlocks` «Скіни за завдання й вбивства» · levels/progression · 🌱.

## Пропозиції до словників
- `+effect:leave_trail`, `+effect:clear_trail` — підтверджую (Tron, Xonix, Blockade, Kurve).
- `+trigger:return_home` — підтверджую з `tron-light-cycles`: повернення на свою зону з хвостом запускає заливку.
- `+cond:in_own_zone` — сутність на своїй території (безпека, лоб у лоб).
- `+role:trail` — хвіст як окрема сутність з власником (вразливий, не стіна); `hazard` не передає «шкодить власнику, коли його торкнуться».
- `+ui:territory-percent` — підтверджую; `+ui:live-ranking` — живий топ гравців поруч із полем.
- `+card:death-drops-territory`, `+card:skin-unlocks`.

## Джерела
- ⭐ [CrazyGames: Paper.io 2](https://www.crazygames.com/game/paper-io-2) — грати; правила захоплення, хвіст, власний хвіст = game over, вбивства, керування мишею/WASD, скіни.
- [Voodoo: Paper.io 2](https://voodoo.io/paper2) — офіційна сторінка (куди веде paper-io.com), лише промо.
- [Wikipedia: Voodoo](https://en.wikipedia.org/wiki/Voodoo_(company)) — Paper.io 2016, Paper.io 2 2018, 266 млн завантажень.
- [Pocket Gamer: Paper.io beginner's tips](https://www.pocketgamer.com/paper-io/paper-io-beginners-tips-how-to-survive-your-early-moments/) — квадрати зі сліду, вбивство через хвіст, лідер втрачає все.
- YouTube: пошук «paper.io gameplay».

## Непевне
- (?) Paper.io 1 — сітка 4 напрямки, Paper.io 2 — вільний кут: з памʼяті; `field: square` за першою версією.
- (?) Суперники — боти чи живі гравці (вважається, що переважно боти; офіційно не підтверджено).
- (?) Лоб у лоб: на своїй землі виживаєш, на чужій гинеш — лише з пошукових сніпетів.
- (?) Перефарбування чужої землі при обведенні — CrazyGames каже «glide over other players' paint», деталі (чи забирається вся чужа ділянка) непевні.
- (?) Круглa арена Paper.io 2, режими, мапа країн, «продовжити за рекламу» — не перевірено.
