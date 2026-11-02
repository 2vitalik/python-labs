---
title: Heiankyo Alien (Digger)
slug: heiankyo-alien
family: maze-arcade
also: [dig-gravity]
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: full
  random: runtime
  goal: state
year: 1979
platforms: [arcade, PC-8000, Game Boy, Super Famicom, Windows, mobile, Steam, Famicom (NEO, 2017)]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Heiankyo_Alien", best: true, note: "правила: ями, засипання, втеча, таймер-розмноження, очки за швидкість; вплив на Lode Runner"}
  - {kind: other, url: "https://ja.wikipedia.org/wiki/平安京エイリアン", note: "найдетальніше: 5 стадій копання й засипання, правила втечі, кількість прибульців, техніка «Akiba dig»"}
  - {kind: steam, url: "https://store.steampowered.com/app/690710/HEIANKYO_ALIEN_平安京エイリアン/", note: "аркадна версія + режим 3671 (5-хвилинна score attack)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=heiankyo+alien+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 70
mechanics: [move-4dir, impassable-cells, touch-death, player-death, chase-player, random-walk, cell-transform, event-points, time-bonus, destroy-all-enemies, sequential-levels, progress-acceleration, reinforcements, game-screen, leaderboard, hot-seat, +dig-hole, +fill-hole, +hole-refill, +trap-stages, +trap-escape-timer, +ally-rescue, +timeout-swarm, +name-entry-on-field]
proposes: ["+effect:dig", "+effect:set_state", "+trigger:enter", "+cond:state", "+cond:stage", "+role:hazard", "+feature:mode-coop", "+card:trap-stages", "+card:ally-rescue"]
author: opus
date: 2026-11-02
---

# Heiankyo Alien — вирий яму, заманив прибульця, засип: двокрокова пастка 1979 року

## Суть
Стражник епохи Хейан ходить вулицями-коридорами Кіото і не має зброї — лише лопату. Він копає яму на вулиці, чекає, доки прибулець упаде в неї, і засипає її разом із ним. Обидві дії займають кілька натискань, а прибулець тим часом вибирається — це **двокрокова пастка з таймером**, з якої виріс жанр «trap 'em up» (Space Panic, Lode Runner). Рівень пройдено, коли знищено всіх прибульців.

## Поле і час
- Нерухомий екран: вулиці по горизонталі й вертикалі шириною в одну клітину, поле — спершу гратка дошки го, потім змінене під план міста (L-подібні вулиці, тупики, не повна гратка).
- Ні гравець, ні прибульці не сходять з вулиць; ями копаються лише на вулиці.
- Real-time. Таймер раунду: коли спливає, прибульців стає 16 — фактично timeout.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Стражник (Kebiishi) | player | 3 життя | рух 4 напрямки по вулицях; копає і засипає перед собою |
| Вулиця | terrain | — | прохідна клітина, де можна копати |
| Будинок/квартал | static | — | непрохідний |
| Яма | hazard | стадія 1–5 | росте з кожним копанням; лише повна (5) ловить; стражник через неї не ходить |
| Прибулець | enemy | 4 → 6 → 8 на рівнях | бродить/переслідує (?); ступив на повну яму — падає |
| Прибулець у ямі | object | таймер втечі | засипаний повністю → гине; час минув → вилазить, яма зникає |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` і `not cell(next, hole)` → ТО `move(guard, dir)`.
- КОЛИ `input(dig)` → ЯКЩО `cell(front, street|hole<5)` → ТО `custom: «стадія ями +1 (до 5)»`.
- КОЛИ `enter(alien, hole)` → ЯКЩО `custom: «стадія = 5»` → ТО `set_state(alien, trapped)`, таймер втечі; інакше `set_cell(hole, street)` — прибулець руйнує недокопану яму.
- КОЛИ `input(fill)` → ЯКЩО `cell(front, hole)` → ТО `custom: «стадія засипання +1 (до 5)»`; ЯКЩО `state(alien, trapped)` і засипано повністю → ТО `disappear_b`, `score(n)` — чим швидше після падіння, тим більше.
- КОЛИ `timer(escape)` → ЯКЩО `state(alien, trapped)` → ТО `clear_state(alien, trapped)`, `set_cell(hole, street)` — вилазить на вулицю.
- КОЛИ `contact(alien, trapped_alien)` → ТО `clear_state(trapped_alien, trapped)` — вільний прибулець миттєво рятує товариша.
- КОЛИ `contact(guard, alien)` → ТО `lose` (життя −1); рівень продовжується з тією ж кількістю прибульців.
- КОЛИ `timer(round_limit)` → ТО `spawn(alien)` до 16 — `custom: «рій замість програшу за часом»`.
- КОЛИ `all_gone(alien)` → ТО `win` рівня, `next_level`; після 9-го — знову 1-й.
- Перемога: нема (цикл із 9 рівнів). Поразка: 0 життів. Рахунок: за кожного засипаного прибульця, бонус за швидкість засипання.

## Керування і ввід
- 4-позиційний джойстик + дві кнопки: копати і засипати (у напрямку погляду).
- Обидві дії — **по кілька натискань** (5 стадій): ритм «копай-копай-копай, відступи, чекай, засипай».
- Тактика «Akiba dig» — ями від центрального перехрестя до сусідніх у 4 боки.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` (аркада).
- `game-screen` — план міста; HUD: `score`, `hi-score`, `lives`, `level-number`, таймер раунду (?).
- `leaderboard` — **ввід імені ходінням**: стражник ходить вулицями по буквах (`custom: «name-entry-on-field»`).
- Переходи: attract → game-screen → (усі знищені) наступний рівень → (0 життів) ввід імені → attract.

## Фічі поза полем
- `levels-sequential` (9 рівнів по колу), `progress-acceleration` (4 → 6 → 8 прибульців).
- `hotseat` — 2 гравці по черзі (Part 1); `mode-coop` — 2 одночасно (Part 2).
- Ранні PC-версії: кнопка «льодяник» — до 3 разів, діє як додаткове життя (`assist-mode`).
- Game Boy: режими OLD (аркада) і NEW (нові вороги й пастки, versus по кабелю) — `mode-select`.
- Steam (Mindware, 2017): аркада + Heiankyo Alien 3671 — 5-хвилинна score attack з нескінченними життями, 7 закопаних предметів, діамант ×2 очок, предмети за N убитих; `leaderboard-online`, кооператив.

## Варіації й родичі
- Space Panic (1980) — те саме з драбинами й поверхами; Lode Runner (1983) — копання вбік-униз, яма заростає сама; Doraemon Meikyū Daisakusen, Boomer's Adventure in ASMIK World; клон Super Alien (VIC-20).
- Ремейки: LSI-гра (1980), Game Boy (1990), SFC (Nichibutsu Arcade Classics 2, 1995), Windows freeware (1999), NEO Heiankyo Alien (Famicom, 2017), Cosmic Digger 3671 (до 4 гравців, 2021).
- Осі: **скільки дій на пастку** — 1 (Lode Runner: яма сама) / 2 з кількома стадіями (тут); **хто закриває пастку** — гравець (тут) / таймер (Lode Runner); **як ворог вибирається** — таймер / порятунок товаришем / руйнування недокопаної ями.

## Цікавинки для курсу
- Яма з 5 стадіями копання і 5 стадіями засипання — 📎 (стан клітини-лічильник).
- Двокрокова пастка: впасти → засипати, інакше вилізе за таймером — 🥉 (стан ворога `trapped` з таймером і кількома шляхами виходу).
- Вільний ворог рятує впійманого дотиком — 🌱, але змінює AI-тактику: заманювати поодинці.
- Ворог руйнує недокопану яму — 🌱; поле як ресурс, що його вороги «ремонтують».
- Timeout як рій ворогів замість програшу — 🌱.
- Очки, що падають з часом між падінням і засипанням — 🌱 (`time-bonus` на рівні однієї події).

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `touch-death` · `player-death` · `chase-player` / `random-walk` (рух прибульців, ?) · `cell-transform` (вулиця ↔ яма) · `event-points` · `time-bonus` · `destroy-all-enemies` · `sequential-levels` · `progress-acceleration` · `reinforcements` (рій до 16 за часом — найближче) · `game-screen` · `leaderboard` · `hot-seat`.
- **Нема** → пропозиції карток:
  - `+dig-hole` (вже Lode Runner) — копання перед собою.
  - `+fill-hole` (вже Kwirk) — тут засипає гравець, не блок.
  - `+hole-refill` (вже Lode Runner) — інший варіант: яма зникає, коли ворог вилазить.
  - `+trap-stages` «Пастка з N стадіями копання/засипання» · entities/interact · 📎 · слот {stages: 5}.
  - `+trap-escape-timer` «Впійманий ворог вибирається за таймером» · entities/state · 📎 · слот {delay}.
  - `+ally-rescue` «Ворог звільняє впійманого товариша дотиком» · entities/interact · 🌱.
  - `+timeout-swarm` «Після ліміту часу — рій ворогів» · game-logic/waves · 🌱.
  - `+name-entry-on-field` «Ввід імені рекорду ходінням по полю» · interface/results · 🌱.

## Пропозиції до словників
- `+effect:dig` (вже Lode Runner, NecroDancer) — тут з кроком стадії.
- `+effect:set_state` (🔥) / `+cond:state` (🔥) — `trapped` з таймером.
- `+trigger:enter` (🔥) — прибулець ступив на яму.
- `+cond:stage(cell, op, n)` — стадія клітини (яма 1–5).
- `+role:hazard` — яма.
- `+feature:mode-coop` (🔥) — одночасна гра двох (Part 2).
- `+card:trap-stages`, `+card:ally-rescue` — див. вище.

## Джерела
- ⭐ [Wikipedia: Heiankyo Alien](https://en.wikipedia.org/wiki/Heiankyo_Alien) — правила ям, втеча за часом або з допомогою товариша, таймер → більше прибульців, очки за швидкість, 9 рівнів, 2 гравці, ремейки, вплив.
- [Wikipedia JA: 平安京エイリアン](https://ja.wikipedia.org/wiki/平安京エイリアン) — 5 стадій копання/засипання, недокопана яма руйнується, 4/6/8 → 16 прибульців, «льодяник», Akiba dig, режими GB.
- [Steam: HEIANKYO ALIEN](https://store.steampowered.com/app/690710/HEIANKYO_ALIEN_平安京エイリアン/) — аркадна версія і режим 3671 (score attack, предмети, діамант ×2).
- YouTube: пошук «heiankyo alien arcade gameplay».

## Непевне
- (?) Поведінка прибульців — випадкове блукання чи переслідування; у джерелах не описано.
- (?) Точні очки, тривалість таймера втечі й ліміту раунду.
- (?) Чи прибулець «руйнує» недокопану яму, лише проходячи по ній, чи й повну, коли не падає.
- (?) Чи є таймер раунду на HUD.
