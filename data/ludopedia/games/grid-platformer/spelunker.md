---
title: Spelunker
slug: spelunker
aka: [スペランカー, Спелеолог]
family: grid-platformer
also: [maze-arcade]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: runtime
  goal: score
year: 1983
platforms: [Atari 8-bit, C64, NES, MSX, arcade, PS3]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Spelunker_(video_game)", best: true, note: "печера з 6 рівнів на одній мапі, повітря, привид і повітряний постріл, кажани, динаміт, ракети, ключі; версії"}
  - {kind: other, url: "https://www.c64-wiki.com/wiki/Spelunker", note: "C64: клавіші, ліфт, батареї бластера, 2 типи ключів, пара з тріщин, 5 життів, таблиця очок"}
  - {kind: other, url: "https://www.mocagh.org/broderbund/spelunker-manual.pdf", note: "скан мануалу Broderbund (без текстового шару)"}
  - {kind: other, url: "https://tcrf.net/Spelunker_(NES)", note: "TCRF: вирізане й приховане у NES-версії (не відкривав)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Spelunker+1983+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [gravity-fall, ladder-climb, carrier-platform, key-and-door, item-pickup, inventory-items, destructible-blocks, bomb-fuse, projectile-shot, touch-death, environment-death, player-death, time-out, enemy-patrol, spawn-random-cell, temporary-modes, event-points, sequential-levels, progress-acceleration, score-records, status-panel, game-screen, splash-screen, game-pause, +fall-height-kill, +weapon-drains-resource, +rope-climb-release, +light-repels-enemy, +loop-harder]
proposes: ["+trigger:landed", "+effect:immobile", "+card:weapon-drains-resource", "+card:rope-climb-release", "+card:light-repels-enemy", "+card:loop-harder"]
author: opus
date: 2026-11-09
---

# Spelunker — спелеолог спускається величезною печерою на ліфтах і мотузках, де вбиває будь-яке падіння, а повітря весь час тече

## Суть
Шахта-печера, складена з шести рівнів, зшитих в одну безперервну мапу: гравець спускається ліфтом, лазить драбинами й мотузками, підриває завали динамітом, відганяє кажанів ракетами-флеєрами і привида — пострілом повітря. Головне — крихкість: падіння навіть з невеликої висоти смертельне, тож кожен стрибок і схід з мотузки — точний маневр. Запас повітря (енергії) спадає з часом і від пострілів по привиду; його поповнюють предмети. Пройдена печера починається знову — та сама мапа, але важча.

## Поле і час
- Одна велика печера: 6 рівнів, зʼєднаних безшовно; камера переходить між секціями (?) — у NES/MSX рівні значно менші, ніж на Atari/C64.
- Вигляд збоку; рух по тайлових платформах, драбинах, мотузках, ліфтових шахтах.
- Real-time; повітря спадає щотік.
- Після 6-го рівня — нова печера з тим самим планом і вищою складністю; усього 6 печер (за Wikipedia).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Спелеолог | player | 5 життів (C64) | ходить, стрибає в напрямку руху, лазить драбинами й мотузками; гине від падіння |
| Ліфт | platform | — | гравець їздить на ньому вгору/вниз джойстиком; старт гри — у ліфті |
| Драбина | terrain | — | вертикальний рух |
| Мотузка | terrain | — | лізти вгору/вниз; ліво/право без стрибка — відпустити й упасти (NES) |
| Платформа | terrain | — | опора; будь-яка щілина під ногами — падіння |
| Завал (купа каміння) | object | — | руйнується динамітом |
| Динаміт | pickup | 1005 очок | лягає в запас; ставиться, вибухає — треба відійти |
| Флеєр | pickup | 1005 очок | у запас; постріл відганяє кажанів на час |
| Ключ (2 типи) | pickup | 3000 очок | відкриває лише двері свого типу |
| Двері | gate | тип | відкриваються ключем того ж типу |
| Батарея / балон повітря | pickup | — | поповнює енергію (повітря) |
| Скарб / інструмент | pickup | 750–3825 очок | рідкісніші — дорожчі |
| Чарівний пил | pickup | 3510 очок | перетворюється на динаміт або флеєр, або відновлює життя (?) |
| Привид | enemy | — | зʼявляється випадково, переслідує й затягує у «світ тіней»; знищується пострілом повітря |
| Кажан | enemy | 750 очок | сидить у темряві, кидає гуано; тікає від світла |
| Тріщина з парою | hazard | — | періодично викидає пару; дотик — смерть |
| Повітря (енергія) | resource | смуга | спадає з часом і від пострілу; 0 — смерть |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(left|right)` → ЯКЩО `free(next)` → ТО `move(spelunker, dir)`.
- КОЛИ `input(jump)` → ТО `custom: «стрибок у напрямку ходьби»`.
- КОЛИ `tick` → ЯКЩО `not custom: «є опора»` → ТО `fall(spelunker)`.
- КОЛИ `custom: «приземлився з висоти понад малий поріг»` → ТО `lives(-1)` (`+trigger:landed`).
- КОЛИ `input(up|down)` → ЯКЩО `cell(here, ladder|rope)` → ТО `move(spelunker, up|down)`.
- КОЛИ `input(left|right)` → ЯКЩО `cell(here, rope)` і `not input(jump)` → ТО `fall(spelunker)` — відпустив мотузку (NES).
- КОЛИ `input(up|down)` → ЯКЩО `occupied(here, elevator)` → ТО `move(elevator, up|down)`, `custom: «везе гравця»`.
- КОЛИ `contact(spelunker, item)` → ТО `pickup`, `score(n)`.
- КОЛИ `input(dynamite)` → ЯКЩО `has(spelunker, dynamite)` → ТО `place(spelunker, dynamite)`; КОЛИ `timer(fuse)` → ТО `explode(small, empty)`, `disappear(rubble)`.
- КОЛИ `custom: «гравець у радіусі вибуху»` → ТО `lives(-1)`.
- КОЛИ `input(flare)` → ЯКЩО `has(spelunker, flare)` → ТО `custom: «кажани тікають від світла, доки флеєр горить»`.
- КОЛИ `contact(spelunker, guano|bat)` → ТО `lives(-1)`.
- КОЛИ `rng(p)` → ТО `spawn_at(ghost, near_player)`; музика попереджає про наближення.
- КОЛИ `input(air_blast)` → ЯКЩО `in_range(spelunker, ghost, n)` → ТО `disappear(ghost)`, `counter(air, -n)`, `stun(spelunker, n)` — гравець кілька секунд нерухомий (`+effect:immobile`).
- КОЛИ `contact(spelunker, ghost)` → ТО `lives(-1)`.
- КОЛИ `contact(spelunker, door)` → ЯКЩО `has(spelunker, key_same_type)` → ТО `disappear_b`; інакше `block`.
- КОЛИ `contact(spelunker, steam)` → ЯКЩО `state(vent, active)` → ТО `lives(-1)`.
- КОЛИ `timer(every)` → ТО `counter(air, -1)`; КОЛИ `counter(air, ==, 0)` → ТО `lives(-1)`, `custom: «повітря знову повне»`.
- КОЛИ `contact(spelunker, air_refill)` → ТО `counter(air, +n)`.
- КОЛИ `reach(spelunker, next_level)` → ТО `message(level_name)`, `lives(+1)`, `score(10000·level)`.
- КОЛИ `custom: «пройдено 6-й рівень»` → ТО `custom: «нова печера з тим самим планом, важча»`.
- Перемога: пройти 6 печер (?). Поразка: 0 життів. Рахунок: предмети, кажани, бонус за рівень; таблиця рекордів (4 найкращі з іменем, C64).

## Керування і ввід
- C64: джойстик (лише 4 напрямки, без діагоналей); кнопка — стрибок у напрямку ходьби; SPACE — постріл повітрям («Phantom-Blaster»), D — динаміт, F — флеєр; RUN/STOP — пауза, RESTORE — вихід.
- NES: B — постріл повітрям; стрибок і предмети — інші кнопки (?).
- Ліфт керується тим самим джойстиком, доки гравець на ньому.

## Вікна, меню, HUD
- `splash-screen` з музикою (Мусоргський, «Картинки з виставки» на Atari).
- `game-screen`: печера + HUD: смуга повітря/енергії (`energy-bar`), `score`, `lives`, запас динаміту й флеєрів (`inventory-bar`), ключі.
- `message`: назва рівня при переході.
- `leaderboard` — 4 найкращі з іменем (C64).
- `end-screen` — game over.

## Фічі поза полем
- `levels-sequential` + петля: 6 рівнів → нова печера, важча.
- `pause`, `leaderboard-local`.
- Аркадна версія (1985) додає стрільбу й пірнання з аквалангом і свій дизайн рівнів; Spelunker HD — 10 печер по 10 рівнів.

## Варіації й родичі
- Сиквели: Spelunker II (аркада 1986, NES 1987), Spelunker World (2015), Spelunker Party! (2017).
- Родичі в корпусі: [montezumas-revenge](montezumas-revenge.md) (ключі/двері, смерть від падіння), [manic-miner](manic-miner.md) (повітря-таймер), [space-panic](space-panic.md) (кисень), [spelunky](../dig-gravity/spelunky.md) — наступник за ідеєю.
- Осі: **поріг падіння** (будь-яке / N клітин / без шкоди); **ресурс-таймер** (повітря тече само + витрачається зброєю); **зброя проти ворога** (постріл / світло / вибух — кожна проти свого ворога).

## Цікавинки для курсу
- Смерть від висоти падіння з дуже малим порогом — 🌱 (лічильник висоти).
- Зброя, що витрачає той самий ресурс, що й таймер життя — 📎.
- Ліфт, яким гравець керує сам, і перехід на ліфт/з нього — 📎.
- Кожен ворог має свою «контру»: привид — повітря, кажани — світло, завали — динаміт — 🌱.
- Випадковий привид із попередженням музикою — 🌱.
- Петля печер з підвищенням складності на тій самій мапі — 🌱.

## Мапа на каталог
- Є: `gravity-fall` · `ladder-climb` · `carrier-platform` (ліфт) · `key-and-door` · `item-pickup`, `inventory-items` · `destructible-blocks` (завали) · `bomb-fuse` (динаміт) · `projectile-shot` (повітря, флеєр) · `touch-death`, `environment-death`, `player-death` · `time-out` (повітря) · `enemy-patrol` (кажани) · `spawn-random-cell` (привид) · `temporary-modes` (флеєр) · `event-points` · `sequential-levels`, `progress-acceleration` · `score-records` · `status-panel`, `game-screen`, `splash-screen` · `game-pause`.
- **Нема** → пропозиції карток:
  - `+fall-height-kill` — як у Space Panic; тут поріг майже нульовий.
  - `+weapon-drains-resource` «Постріл витрачає ресурс-таймер і знерухомлює стрільця» · entities/combat · 📎.
  - `+rope-climb-release` «Мотузка: лізти, відпустити — падіння» · entities/move · 🌱 (поряд із `ladder-climb`).
  - `+light-repels-enemy` «Світло на час відганяє ворогів» · entities/interact · 🌱.
  - `+loop-harder` «Після останнього рівня — та сама мапа важче» · levels/progression · 🌱.

## Пропозиції до словників
- `+trigger:landed(a, height)` — приземлення після падіння на N клітин (Spelunker, Manic Miner, Montezuma).
- `+effect:immobile(a, n)` — сутність нерухома N тіків після власної дії (відмінне від `stun` від ворога) — Spelunker.
- `+card:weapon-drains-resource`, `+card:rope-climb-release`, `+card:light-repels-enemy`, `+card:loop-harder` — див. вище.

## Джерела
- ⭐ [Wikipedia: Spelunker](https://en.wikipedia.org/wiki/Spelunker_(video_game)) — повітря, привид і постріл повітря (нерухомість), кажани з гуано, динаміт/флеєри/ключі, 6 рівнів однією мапою, петля печер, версії й сиквели.
- [C64-Wiki: Spelunker](https://www.c64-wiki.com/wiki/Spelunker) — клавіші, старт у ліфті, батареї бластера, 2 типи ключів, пара з тріщин, 5 життів, очки за все, +життя за рівень.
- [Мануал Broderbund (скан)](https://www.mocagh.org/broderbund/spelunker-manual.pdf) — текст не читається; лише як джерело.

## Непевне
- (?) Поріг висоти падіння в клітинах; чи вбиває падіння «на будь-який піксель» (так кажуть огляди NES).
- (?) Що саме відновлює повітря (батареї на C64, балони в NES); чарівний пил — життя чи предмет.
- (?) Кнопки NES-версії; як камера показує секції печери.
- (?) Чи є фінал після 6-ї печери, чи гра нескінченна.
- (?) Вагонетки й водоспади (згадані в сюжеті C64-Wiki: «бочка, щоб пройти водоспад») — механіка не підтверджена.
