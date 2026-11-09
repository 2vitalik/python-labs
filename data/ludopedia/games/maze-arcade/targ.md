---
title: Targ / Spectar
slug: targ
aka: [Spectar, Attack Force, Crystal City]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: score
year: 1980
platforms: [arcade, TRS-80 (клон Attack Force)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Targ_(video_game)", best: true, note: "Crystal City 10×10, Wummel, Targ-и таранять, Spectar Smuggler, прискорення при затримці"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Spectar", note: "сиквел: блокади, точки й зірки, Smuggler стріляє, бонус 1000×рівень"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Attack_Force_(video_game)", note: "клон для TRS-80 (Big Five, 1980)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=targ+exidy+1980+arcade+gameplay", note: "пошук; Targ"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=spectar+exidy+arcade+gameplay", note: "пошук; Spectar"}
stage: v1
coverage: 55
mechanics: [impassable-cells, projectile-shot, touch-death, chase-player, destroy-all-enemies, collect-all, progress-acceleration, event-points, sequential-levels, hot-seat, player-death, +stall-speedup, +bonus-visitor, +ram-only-enemy, +level-bonus-cap, +reskin-per-level]
proposes: ["+trigger:stall"]
author: opus
date: 2026-11-09
---

# Targ / Spectar — машинка в сітці вулиць «Кришталевого міста» відстрілює зграю таранів

## Суть
Гравець веде машинку Wummel по сітці вулиць між квадратними будинками і стріляє по ворожих Targ-ах (червоні клини). Вороги не стріляють — їхня єдина зброя таран. Знищив усіх — бонус і новий раунд; тягнеш час — Targ-и прискорюються і стають швидшими за тебе. Spectar (1980) додає блокади, точки для збору і Smuggler-а, що стріляє.

## Поле і час
- «Crystal City» — сітка 10×10 доріг, розділених квадратними будинками (рух лише по вулицях-коридорах).
- Весь лабіринт на одному екрані, видно все.
- Real-time; темп ворогів росте, якщо раунд затягується.
- Spectar: у сітці зʼявляються блокади, у центрі — зірки; форма блоків-будинків змінюється з рівнем (коло, хрест, ромб, піраміда…), з 9-го рівня — одна.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Wummel | player | життя | їде вулицями, стріляє |
| Targ | enemy | швидкість росте з часом | ганяється й таранить; не стріляє |
| Spectar Smuggler | enemy | великий бонус | зʼявляється зрідка; Targ — не стріляє, Spectar — стріляє |
| Будинок | static | — | непрохідний блок між вулицями |
| Блокада (Spectar) | static | — | перекриває частину вулиці |
| Точка (Spectar) | pickup | — | збір усіх закриває раунд |
| Зірка (Spectar) | pickup | — | мерехтить у центрі; бонус |
| Постріл | projectile | — | знищує ворога |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire, wummel)` → ТО `spawn(shot, facing)`.
- КОЛИ `contact(shot, targ)` → ТО `disappear(targ)`, `score(n)` (Spectar: n росте з рівнем).
- КОЛИ `contact(shot, smuggler)` → ТО `disappear(smuggler)`, `score(big_bonus)`.
- КОЛИ `contact(targ|smuggler, wummel)` → ТО `lives(-1)`.
- КОЛИ `contact(smuggler_shot, wummel)` → ТО `lives(-1)` (Spectar).
- КОЛИ `custom: «раунд триває задовго»` → ТО `speed(targ, +n)` — аж до швидшого за Wummel.
- КОЛИ `rng(p)` → ТО `spawn_at(smuggler, edge)` (Targ); Spectar: КОЛИ `schedule(5 с, 10 с)` → ТО `spawn_at(smuggler, edge)`, `sound(тривога, до знищення всіх)`.
- КОЛИ `contact(wummel, dot|star)` → ТО `pickup(wummel, dot|star)`, `score(n)` (Spectar).
- КОЛИ `all_gone(targ)` → ТО `score(bonus)`, `next_level`; Spectar: також КОЛИ `all_gone(dot)` → ТО `next_level`.
- КОЛИ `level_end` → ТО `score(1000 × min(level, 9))` (Spectar).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: нема (нескінченні раунди). Поразка: життя вичерпано. Рахунок: вороги, Smuggler, бонус раунду.

## Керування і ввід
- Джойстик керує машинкою по вулицях + кнопка пострілу (?).
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `attract-demo` — аркадний атракт (?).
- `game-screen`: уся сітка міста, `score`, `hi-score`, `lives`, `level-number` (?).
- Переходи: атракт → монета → раунд → (усі знищені) бонус → раунд → … → життя 0 → атракт.

## Фічі поза полем
- `hotseat`: два гравці по черзі.
- Spectar отримав ROM-апгрейд (квітень 1981); коктейль-кабінет Centuri.
- `operator-settings` — DIP-налаштування (?).

## Варіації й родичі
- Spectar (Exidy, 1980) — сиквел: блокади, точки, зірки, Smuggler стріляє, вороги змінюють форму щораунду.
- Attack Force (Big Five, TRS-80, 1980) — клон з «ram-ships»; порт для Atari 2600 (CBS) не вийшов.
- Родичі: `head-on.md` (той самий виробничий час, машинки в сітці), `rally-x.md` (машина в лабіринті вулиць), `berzerk.md`, `wizard-of-wor.md` (відстріл у лабіринті).
- **Осі варіацій:** вороги (лише таран / таран + постріл); кінець раунду (всі вороги / всі точки / що раніше); тиск часу (прискорення ворогів / карателі / таймер).

## Цікавинки для курсу
- Вороги без пострілу: уся загроза — переслідування і таран — 🌱.
- Прискорення ворогів, якщо гравець «тягне» раунд (антикемпінг) — 🌱.
- Подвійна умова кінця раунду (знищити всіх АБО зібрати всі точки) — 🌱.
- Бонусний гість, що зʼявляється за розкладом (5 с і 10 с) — 🌱.
- Сітка вулиць 10×10 як граф перехресть для AI погоні — 🥉.

## Мапа на каталог
- Є: `impassable-cells` · `projectile-shot` · `touch-death` · `chase-player` · `destroy-all-enemies` · `collect-all` (Spectar) · `progress-acceleration` · `event-points` · `sequential-levels` · `hot-seat` · `player-death`.
- **Нема** → пропозиції карток:
  - `+stall-speedup` «Затягнув раунд — вороги прискорюються» · game-logic/waves · 🌱.
  - `+bonus-visitor` «Бонусний гість за розкладом» · entities/spawn · 🌱 (Smuggler, фрукти Pac-Man).
  - `+ram-only-enemy` «Ворог без зброї, лише таран» · entities/combat · 🌱.
  - `+level-bonus-cap` «Бонус раунду росте до стелі» · game-logic/score · 🌱.
  - `+reskin-per-level` «Вигляд перешкод змінюється з рівнем» · interface/render · 🌱.

## Пропозиції до словників
- `+trigger:stall` — гравець надто довго не завершує раунд (тиск на кемпінг; споріднений з `idle`, але про прогрес, не про ввід).

## Джерела
- ⭐ [Wikipedia: Targ](https://en.wikipedia.org/wiki/Targ_(video_game)) — сітка 10×10, Wummel, Targ-и таранять, Smuggler, прискорення, порти й клони.
- [Wikipedia: Spectar](https://en.wikipedia.org/wiki/Spectar) — блокади, точки, зірки, Smuggler на 5 і 10 с, бонус 1000×рівень до 9, форми блоків.
- [Wikipedia: Attack Force](https://en.wikipedia.org/wiki/Attack_Force_(video_game)) — клон TRS-80.
- YouTube: пошуки «targ exidy 1980 arcade gameplay», «spectar exidy arcade gameplay».

## Непевне
- (?) Керування: чи Wummel їде безперервно, чи стоїть без вводу; напрям пострілу (вперед за рухом?) — у джерелах нема.
- (?) Чи є обгортання країв (тунелі) у сітці.
- (?) Очки за Targ-ів і Smuggler-а, кількість ворогів у раунді, стартові життя, поріг «задовго» — не знайдено.
- (?) Як Targ-и обирають шлях (жадібна погоня / випадково).
- (?) Що дає зірка в Spectar.
- WebSearch-ліміт вичерпано; лише Wikipedia.
