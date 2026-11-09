---
title: Bosconian
slug: bosconian
aka: [ボスコニアン, "Bosconian: Star Destroyer"]
family: maze-arcade
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 1981
platforms: [arcade, MSX, PC-8801, Sharp X1, FM-7]
links:
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%83%9C%E3%82%B9%E3%82%B3%E3%83%8B%E3%82%A2%E3%83%B3", best: true, note: "JA: керування, тор, радар, Condition, типи ворогів і очки, формації, шпигун, бази 6+1, астероїди й міни, AUTO-складність"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Bosconian", note: "EN: стрільба вперед-назад, радар, бази з 6 гарматами, формації, спай-шип"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=bosconian+arcade+namco+gameplay", note: "пошук; аркада"}
stage: v1
coverage: 60
mechanics: [move-8dir, move-auto, wrap-edges, player-camera, minimap-radar, projectile-shot, chase-player, destroy-all-enemies, chain-detonation, timeout-punisher, extra-life-threshold, game-over-continue, event-points, sound-warnings, difficulty-levels, sequential-levels, touch-death, +fire-front-back, +multi-part-base, +formation-leader, +spy-escape-alarm, +alert-level, +no-miss-bonus]
proposes: ["+ui:condition-indicator", "+feature:adaptive-level", "+effect:scatter"]
author: opus
date: 2026-11-09
---

# Bosconian — корабель у центрі тороїдального космосу руйнує бази з гарматами, поки тривога зростає до «Condition Red»

## Суть
Корабель завжди летить уперед і за мить розвертається у будь-який з 8 напрямків; стріляє одночасно вперед і назад. Мета раунду — знищити всі зелені бази на радарі: у кожної ядро і 6 гармат. Між ними — астероїди, міни-ланцюжки, ракети-переслідувачі, формації з командиром і шпигун, чия втеча піднімає тривогу. **Межа сімʼї:** поле вільне (не клітинне), лабіринту стін нема — «лабіринт» складають нерухомі астероїди й міни; у `maze-arcade` гра лише як родич `rally-x.md` (радар, рух уперед, скрол навколо гравця).

## Поле і час
- Вільне поле без країв: радар замкнений зверху-знизу і зліва-справа (тор); корабель нерухомий у центрі, світ скролить у 8 напрямках.
- Радар показує все поле: гравця (білий), бази (зелені), формації (червоні); інших ворогів — ні.
- Real-time; ліміт раунду ≈110 с (раунди 1–2) / ≈90 с (з 3-го) — після нього «Condition Red».
- Розстановка баз — до 17-го раунду, далі цикл 12–17; до 8 баз на раунд.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Starfighter | player | 3 життя; до 4 пострілів на екрані | летить уперед; 8 напрямків; постріл вперед і назад одночасно |
| База: ядро | spawner | 1500 за базу | укриття відкривається/закривається; з 4-го раунду пускає E-type |
| База: гармата (×6) | enemy | 200 кожна; 6 → 2700 разом | нерухома; некеровані постріли, що нищать і гравця, і ворогів, і перешкоди |
| I-type | enemy | 50 | переслідує корабель |
| P-type | enemy | 60 | кружляє навколо корабля |
| E-type | enemy | 70 | з ядра; летить прямо, швидша |
| Формація (5) | enemy | 4 + командир (×2 очок); 500/1000/1500 за всіх | летить на гравця, тарани |
| Шпигун (spy ship) | enemy | 200–800 | не таранить; втеча прискорює Condition Red; до 4 за раунд |
| Астероїд | hazard | 10 | нерухомий; контакт нищить гравця або ворога |
| Космо-міна | hazard | 20 | нерухома; вибухає від пострілу чи дотику, ланцюгом нищить сусідів |
| Постріл | projectile | — | після пострілу трохи слідує осі корабля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir, player)` → ТО `face(player, dir)`; КОЛИ `tick` → ТО `move(player, facing)`; КОЛИ `edge(any)` → ТО `wrap(any)`.
- КОЛИ `input(fire, player)` → ЯКЩО `count(shot, <, 4)` → ТО `spawn(shot, front)`, `spawn(shot, back)`.
- КОЛИ `contact(shot, cannon)` → ТО `disappear(cannon)`, `score(200)`; КОЛИ `all_gone(cannon_of_base)` → ТО `disappear(base)`.
- КОЛИ `contact(shot, core)` → ЯКЩО `state(core, open)` → ТО `disappear(base)`, `score(1500)` (гармати, що лишились, не рахуються).
- КОЛИ `contact(player, core)` → ТО `disappear(base)`, `lives(-1)`.
- КОЛИ `contact(enemy|asteroid|cannon_shot, player)` → ТО `lives(-1)`; ворог від астероїда/гармати теж гине і дає очки гравцю.
- КОЛИ `contact(shot|player|enemy, mine)` → ТО `explode(area, 1, none)` — ланцюгом підриває сусідів; гармати баз не зачіпає.
- КОЛИ `custom: «гравець далеко від усіх баз»` → ТО `spawn_at(formation, base)`; КОЛИ `contact(shot, commander)` → ТО `custom: «решта формації втрачає ціль і розлітається»`; КОЛИ `all_gone(formation)` → ТО `score(500|1000|1500)`.
- КОЛИ `timer(60 с | 40 с)` → ТО `spawn_at(spy, edge)`, `sound(«Spy ship sighted» (?))`; КОЛИ `custom: «шпигун пішов з екрана»` → ТО `custom: «час до Condition Red скорочується»`; КОЛИ `timer(10–15 с після збиття)` → ТО `spawn_at(spy, edge)`.
- КОЛИ `timer(round_limit)` → ТО `set_state(game, condition_red)` — масована атака до втрати життя або кінця раунду.
- КОЛИ `destroyed(base)` → ТО `custom: «атаки слабшають на кілька секунд»`.
- КОЛИ `all_gone(base)` → ТО `next_level`; AUTO: `score(min(no_miss, 10) × 100 × bases)`.
- КОЛИ `counter(score, >=, 20000 | 70000 | кожні 70000)` → ТО `lives(+1)`.
- КОЛИ `counter(lives, ==, 0)` → ТО `window(game-over-continue)` 15 с: рахунок → 0, знищені бази лишаються.
- Перемога: нема (раунди до 256). Поразка: життя вичерпано. Рахунок: бази, гармати, вороги, формації, шпигун, бонус без смертей.

## Керування і ввід
- 8-позиційна рукоятка: миттєвий розворот; корабель завжди летить уперед.
- Одна кнопка: два постріли (ніс і корма); NEW-версія — автострільба при утриманні.

## Вікна, меню, HUD
- `attract-demo` — аркадний атракт.
- `game-screen`: космос навколо корабля + правий бік — `minimap` (радар), `+ui:condition-indicator` (GREEN / YELLOW / RED), `score`, `hi-score`, `lives` (до 4), `level-number` (?).
- Голос: тривоги («Alert, alert», «Battle stations», «Condition red») (?).
- `game-over-continue` (15 с) → `leaderboard` (топ-5 з іменем).
- Переходи: атракт → гра → (усі бази) раунд+1 → … → життя 0 → continue → атракт.

## Фічі поза полем
- `operator-settings`: складність A/B/C/AUTO; `+feature:adaptive-level` — AUTO підлаштовує таблицю складності під гравця.
- `continue` з обнуленням рахунку.

## Варіації й родичі
- Родичі: `rally-x.md` (радар, рух уперед, скрол довкола гравця), Time Pilot, Sinistar (вільний космос з базою-ціллю).
- **Осі варіацій:** ціль (вороги / бази з частинами / предмети); тривога (таймер / подія-шпигун / обидва); поле (клітинний лабіринт Rally-X / вільний тор Bosconian).

## Цікавинки для курсу
- База як складена сутність: ядро + 6 гармат, два шляхи знищення з різною ціною — 📎.
- Шкала тривоги GREEN → YELLOW → RED від таймера і від втечі шпигуна — 🌱.
- Формація з командиром: убив лідера — решта розлітається — 📎.
- Постріл вперед і назад одночасно — 🌱.
- Міни з ланцюговою детонацією — 📎.

## Мапа на каталог
- Є: `move-8dir` · `move-auto` · `wrap-edges` · `player-camera` · `minimap-radar` · `projectile-shot` · `chase-player` · `destroy-all-enemies` (бази) · `chain-detonation` (міни) · `timeout-punisher` (Condition Red) · `extra-life-threshold` · `game-over-continue` · `event-points` · `sound-warnings` · `difficulty-levels` · `sequential-levels` · `touch-death`.
- **Нема** → пропозиції карток:
  - `+fire-front-back` «Постріл уперед і назад» · entities/combat · 🌱.
  - `+multi-part-base` «Ціль із частин: ядро або всі модулі» · entities/combat · 📎.
  - `+formation-leader` «Командир формації: убив — решта розлітається» · entities/move · 📎.
  - `+spy-escape-alarm` «Втеча розвідника піднімає тривогу» · game-logic/waves · 🌱.
  - `+alert-level` «Рівні тривоги ворогів» · game-logic/waves · 🌱.
  - `+no-miss-bonus` «Бонус за раунд без смертей» · game-logic/score · 🌱.

## Пропозиції до словників
- `+ui:condition-indicator` — табло рівня тривоги (GREEN / YELLOW / RED).
- `+feature:adaptive-level` — складність підлаштовується під гравця (AUTO; є в індексі ×1, Voltorb Flip).
- `+effect:scatter` — група втрачає ціль і розлітається (формація без командира).

## Джерела
- ⭐ [Wikipedia JA: ボスコニアン](https://ja.wikipedia.org/wiki/%E3%83%9C%E3%82%B9%E3%82%B3%E3%83%8B%E3%82%A2%E3%83%B3) — керування, тор, радар, Condition, I/P/E-type з очками, формації, шпигун, бази, астероїди, міни, життя, AUTO.
- [Wikipedia: Bosconian](https://en.wikipedia.org/wiki/Bosconian) — огляд механік англійською.
- YouTube: пошук «bosconian arcade namco gameplay».

## Непевне
- (?) Точні фрази голосу; чи YELLOW вмикається лише атакою.
- (?) Платформи портів (MSX підтверджено; PC-8801/X1/FM-7 — з памʼяті).
- (?) Чи будь-яка частина поля має клітинну розмітку — судячи з джерел, ні: гра як межа сімʼї.
- WebSearch-ліміт вичерпано; StrategyWiki 403, fandom 402.
