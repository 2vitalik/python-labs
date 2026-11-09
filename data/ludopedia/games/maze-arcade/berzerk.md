---
title: Berzerk
slug: berzerk
aka: [Берзерк, Frenzy]
family: maze-arcade
also: []
klass: avatar
axes:
  field: free
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1980
platforms: [arcade, Atari 2600, Atari 5200, Vectrex]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Berzerk_(video_game)", best: true, note: "кімнати, роботи за кольорами, Evil Otto, мова, версії"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Evil_Otto", note: "Evil Otto: навіщо його придумали"}
  - {kind: other, url: "https://www.arcade-museum.com/manuals-videogames/B/Berzerk-Instruction-Cards-FGENNL.pdf", note: "інструкційна картка автомата: 50 очок, бонус, Otto, життя за 5000"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=berzerk+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 65
mechanics: [move-8dir, projectile-shot, shoot-forward, touch-death, environment-death, player-death, chase-greedy, realtime-ai, event-points, extra-life-threshold, score-records, attract-demo, game-screen, sound-effects, +electric-walls, +fire-stops-movement, +room-exits, +invincible-pursuer, +enemy-friendly-fire, +clear-room-bonus, +robot-color-tiers, +taunt-speech, +seeded-rooms]
proposes: ["+effect:shoot", "+trigger:room_exit", "+effect:next_room", "+role:pursuer", "+card:invincible-pursuer", "+card:taunt-speech"]
author: opus
date: 2026-11-09
---

# Berzerk — тікай з кімнати-лабіринту, відстрілюючи роботів, поки не прийшов безсмертний Evil Otto

## Суть
Гуманоїд потрапляє в кімнату з електричними стінами, де стоять роботи; треба вийти через інший вихід — бажано, розстрілявши всіх. Стіни вбивають від дотику, роботи стріляють у 8 напрямках і гинуть також від стін і власних пострілів. Якщо гравець затримується, у кімнату входить невразливий стрибаючий смайлик **Evil Otto**, що проходить крізь стіни і женеться за гравцем, — головний «таймер» гри. Роботи говорять синтезованим голосом (погрози й образи), одна з перших ігор зі мовленням.

## Поле і час
- Кожна кімната — один екран: зовнішня стіна з виходами посередині сторін і внутрішні стіни-відрізки на прихованій сітці; рух сутностей — вільний (піксельний), тому `field: free`.
- Кімнати утворюють нескінченну «карту»: вихід через бік веде в сусідню кімнату; планування стін генерується з seed за координатами кімнати, а не цілком випадково.
- Гравець входить посередині однієї сторони і має вийти через **іншу** сторону (вхід позаду закритий (?)).
- Real-time; роботи повільні, Evil Otto зʼявляється після затримки і рухається крізь усе.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Гуманоїд (Humanoid) | player | життя (3 (?)) | рух 8 напрямків; під час пострілу стоїть |
| Постріл гравця | projectile | — | летить прямо в одному з 8 напрямків до стіни/цілі |
| Стіна | hazard | електрична | дотик гравця або робота → смерть |
| Вихід | static | на 3 інших сторонах | прохід у сусідню кімнату |
| Робот | enemy | колір = набір пострілів | повільно йде до гравця, іноді стріляє в 8 напрямках; гине від стіни, від пострілу, від зіткнення з роботом |
| Постріл робота | projectile | 1–5 на робота залежно від кольору | летить прямо; вбиває гравця (і робота (?)) |
| Evil Otto | enemy | невразливий | стрибає, проходить крізь стіни, переслідує гравця |

Кольори роботів (перша модель автомата): жовті не стріляють, червоні — 1 постріл за раз, білі — 2. Пізніша ревізія додає фіолетових (3 або 5 пострілів), жовтих з 4 пострілами і білого з одним дуже швидким пострілом. Колір змінюється з поступом гравця (?).

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `not input(fire)` → ТО `move(humanoid, dir)` (8 напрямків).
- КОЛИ `input(fire + dir)` → ЯКЩО `count(own_shot, <, max)` (?) → ТО `custom: «постріл у напрямку dir»` (`+effect:shoot`), `freeze(humanoid, while_firing)` — гравець стоїть, доки стріляє.
- КОЛИ `contact(humanoid, wall)` → ТО `lose` (мінус життя; гравця «бʼє струмом»).
- КОЛИ `contact(robot_shot, humanoid)` або `contact(humanoid, robot)` або `contact(humanoid, otto)` → ТО `lose`.
- КОЛИ `contact(player_shot, robot)` → ТО `disappear_both`, `score(50)`.
- КОЛИ `contact(robot, wall)` → ТО `disappear_a`, `custom: «зараховується як знищений»`.
- КОЛИ `contact(robot, robot)` → ТО `disappear_both`; КОЛИ `contact(robot_shot, robot)` → ТО `disappear_b` (?) — роботи знищують одне одного, і це рахується в бонус.
- КОЛИ `contact(shot, wall)` → ТО `disappear_a`.
- КОЛИ `tick` → ТО робот: `custom: «крок у бік гравця»` (`chase-greedy`); КОЛИ `line_of_sight(robot, humanoid)` → ЯКЩО `prob(p)` `and count(robot_shot, <, color_limit)` → ТО `custom: «стріляє в напрямку гравця (8 напрямків)»`.
- КОЛИ `timer(room_delay)` → ТО `spawn_at(otto, entry_side)`.
- КОЛИ `tick` → ТО Otto: `custom: «стрибає і рухається до гравця крізь стіни»`; `contact(player_shot, otto)` → `custom: «без ефекту»`.
- КОЛИ `all_gone(robot)` → ТО `score(10 × robots_in_room)` (бонус, навіть якщо роботи вбили себе самі).
- КОЛИ `reach(humanoid, exit)` → ТО `custom: «перехід у сусідню кімнату»`; ЯКЩО `count(robot, >, 0)` → ТО `message(«Chicken!»)` (?).
- КОЛИ `counter(score, >=, 5000)` → ТО `lives(+1)` (DIP: 5000 / 10000 / нема).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Мова: КОЛИ `level_start` (кімната) → ТО `sound(«Intruder alert!»)` (?); КОЛИ `died(humanoid)` → ТО `sound(«Got the humanoid…»)` (?).
- Перемога: нема — рекорд. Поразка: скінчились життя. Рахунок: 50 за робота, бонус 10 × роботів за повністю зачищену кімнату.

## Керування і ввід
- 8-позиційний джойстик — рух.
- Кнопка Fire + напрям джойстика — постріл у цей бік; поки кнопку тримають, гравець не рухається (стрільба і рух взаємовиключні).
- 1P / 2P Start; двоє грають по черзі (?).

## Вікна, меню, HUD
- `attract-demo` — демо-гра з фразами роботів (мова звучить і в атракті).
- `game-screen` — кімната; `score`, `lives` (фігурки гуманоїда), `hi-score`.
- `leaderboard` — таблиця рекордів з ініціалами (?).
- `end-screen` — GAME OVER → атракт.
- Переходи: атракт → (монета, Start) → кімната → (вихід) наступна кімната → … → (0 життів) GAME OVER → [ініціали] → атракт.

## Фічі поза полем
- `operator-settings` — DIP: поріг додаткового життя (5000 / 10000 / нема).
- Нескінченна карта кімнат, детермінована за координатами (повернувся — та сама кімната).
- `hotseat` 2 гравці по черзі (?).

## Варіації й родичі
- **Frenzy (1982)** — сиквел від Алана Макніла: більше розмаїття (відбивні й руйнівні стіни (?)).
- **Atari 2600** — інші лабіринти, кілька варіацій гри; **Berzerk: Enhanced** (2023) — діагональна стрільба роботів, як в аркаді; **Berzerk: Recharged** (2023) — сучасне переосмислення.
- Vectrex і Atari 5200 — порти.
- Родичі: Wizard of Wor (стрільба в лабіринті, вороги-стрільці), Robotron: 2084 (стрільба у 8 напрямків проти натовпу роботів), Gauntlet, Battle City (снаряди в лабіринті), Smash TV; Evil Otto — предок «таймер-переслідувачів» (Bubble Bobble «Baron von Blubba», Spelunky-привид).
- **Осі варіацій:** стіни (просто непрохідні / вбивають / руйнуються / відбивають); переслідувач-таймер (нема / невразливий / вразливий); вихід (будь-який / не той, звідки зайшов); тир ворогів за кольором (скільки пострілів).

## Цікавинки для курсу
- Стіни-вбивці для всіх: роботи гинуть від них теж — 📎 (одна таблиця взаємодій «сутність × стіна»).
- Evil Otto: невразливий переслідувач, що проходить крізь стіни і зʼявляється за таймером, — 📎 (просте переслідування без колізій зі стінами, але змінює стиль гри).
- Роботи вбивають одне одного (зіткнення, постріли) і це зараховується в бонус — 🥉 (friendly fire ворогів + підрахунок «усіх знищено» незалежно від причини).
- Стрільба в 8 напрямків, під час пострілу рух заблоковано — 🌱.
- Тири ворогів за кольором (кількість одночасних пострілів) — 📎 (дані замість коду).
- Кімнати з seed за координатами: нескінченна, але відтворювана мапа — 🥉 (детермінована генерація).
- Синтезовані фрази як реакція на події (вхід, смерть, втеча) — 🌱.

## Мапа на каталог
- Є: `move-8dir` · `projectile-shot` · `shoot-forward` · `touch-death` (робот, Otto) · `environment-death` (стіна) · `player-death` · `chase-greedy` (роботи, Otto) · `realtime-ai` · `event-points` · `extra-life-threshold` · `score-records` · `attract-demo` · `game-screen` · `sound-effects`.
- **Нема** → пропозиції карток:
  - `+electric-walls` «Стіни вбивають усіх, хто торкнеться» · entities/death · 🌱.
  - `+fire-stops-movement` «Постріл зупиняє аватара» · entities/combat · 🌱.
  - `+room-exits` «Кімната-екран з виходами в сусідні» · levels/progression · 📎.
  - `+invincible-pursuer` «Невразливий переслідувач за таймером» · entities/spawn · 📎 · слоти {delay, through_walls}.
  - `+enemy-friendly-fire` «Вороги знищують одне одного» · entities/combat · 📎.
  - `+clear-room-bonus` «Бонус за повну зачистку кімнати» · game-logic/score · 🌱 · слот {per_enemy}.
  - `+robot-color-tiers` «Тир ворога за кольором» · entities/state · 📎 · слот {shots}.
  - `+taunt-speech` «Голосові фрази на події» · interface/sound · 🌱.
  - `+seeded-rooms` «Кімната генерується з seed за координатами» · levels/generation · 🥉.

## Пропозиції до словників
- `+effect:shoot` — випустити снаряд у напрямку (Berzerk, Battle City).
- `+trigger:room_exit` — аватар пройшов через вихід кімнати-екрана (Berzerk, Wizard of Wor, Atari Adventure); `+effect:next_room` — перейти в сусідню кімнату.
- `+role:pursuer` — невразливий переслідувач-таймер (Evil Otto, привид Spelunky).
- `+card:invincible-pursuer`, `+card:taunt-speech` — див. вище.

## Джерела
- ⭐ [Wikipedia: Berzerk](https://en.wikipedia.org/wiki/Berzerk_(video_game)) — вхід/вихід, рух і стрільба 8 напрямків, кольори роботів двох ревізій, Evil Otto, причини смерті, DIP життя, seed кімнат, версії.
- [Wikipedia: Evil Otto](https://en.wikipedia.org/wiki/Evil_Otto) — навіщо Макніл додав Otto (виганяти з зачищених кімнат).
- [Інструкційна картка автомата (PDF)](https://www.arcade-museum.com/manuals-videogames/B/Berzerk-Instruction-Cards-FGENNL.pdf) — 50 очок за робота, бонус «навіть якщо роботи знищили себе самі», Otto невразливий і проходить стіни, життя за 5000.
- YouTube: пошук «berzerk arcade gameplay».

## Непевне
- (?) Бонус 10 × роботів — з кількох пошукових фрагментів, картка каже лише «бонус».
- (?) Фрази «Intruder alert!», «Got the humanoid», «Chicken, fight like a robot» і коли саме звучать — з памʼяті; Wikipedia фраз не наводить.
- (?) Чи закривається вхід позаду гравця; чи вбиває Otto роботів; чи прискорюється Otto.
- (?) Ліміт пострілів гравця на екрані, стартові життя, ініціали в таблиці рекордів.
- (?) Деталі Frenzy (відбивні/руйнівні стіни) — Wikipedia каже лише «більше розмаїття».
