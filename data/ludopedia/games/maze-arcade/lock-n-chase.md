---
title: Lock 'n' Chase
slug: lock-n-chase
aka: [Lock'n'Chase, ロックンチェイス]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: collect
year: 1981
platforms: [arcade, Intellivision, Atari 2600, Apple II, Game Boy, Wii, PSN, 3DS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Lock_%27n%27_Chase", best: true, note: "двері (до 2 одночасно, відчиняються самі), мішки грошей, скарби, порти"}
  - {kind: other, url: "https://www.arcade-museum.com/Videogame/lock-n-chase", note: "KLOV: джойстик 4 напрямки + кнопка Lock, 1–2 гравці по черзі"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/ロックンチェイス", note: "JA: двері в щойно пройденому проході, діамант у Game Boy-версії"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=lock+n+chase+arcade+1981+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [move-4dir, collect-all, reach-exit, touch-death, player-death, chase-player, temporary-modes, event-points, sequential-levels, status-panel, game-screen, +player-placed-door, +limited-active-doors, +self-opening-door, +auto-cycling-door, +center-bonus-item, +escalating-bonus-item]
proposes: ["+effect:lock", "+effect:unlock", "+card:player-placed-door", "+card:limited-active-doors", "+card:auto-cycling-door"]
author: opus
date: 2026-11-09
---

# Lock 'n' Chase — злодій у сховищі банку: збери монети і зачиняй двері за собою, поки поліція не загнала в кут

## Суть
Злодій Lupin збирає золоті монети в лабіринті банківського сховища, тікаючи від чотирьох поліцейських. Його зброя — **двері**: кнопкою він зачиняє прохід, який щойно пройшов, і поліція за ним застрягає або опиняється в пастці. Одночасно зачиненими можуть бути лише двоє дверей, і вони самі відчиняються за кілька секунд; погано поставлені двері відрізають і власний шлях утечі.

## Поле і час
- Клітинний лабіринт одного екрана (сховище); біля центру — двері, що відчиняються й зачиняються самі.
- У центрі періодично зʼявляються мішки грошей і скарб рівня.
- Real-time; зачинені двері — тимчасова стіна на кілька секунд.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Lupin (злодій) | player | життя | рух 4 напрямки; кнопкою зачиняє двері позаду |
| Монета | pickup | 20 очок | усі зібрано → вихід (?) / рівень пройдено |
| Двері гравця | gate | ≤ 2 зачинені; кілька секунд | зачиняються кнопкою, відчиняються самі |
| Двері біля центру | gate | — | відчиняються й зачиняються автоматично |
| Поліцейський (Stiffy / Scaredy / Smarty / Silly) | enemy | 4; характер | переслідують; дотик — арешт |
| Мішок грошей | pickup | 500 → 1000 → 2000 → 4000 | у центрі; ненадовго оглушує поліцію |
| Скарб (циліндр, корона, портфель, телефон) | pickup | 200 / 300 / 500 / ? | біля центру; вид змінюється з рівнями |
| Вихід | static | верх / низ поля (?) | утеча після збору монет (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next)` → ТО `move(lupin, dir)`.
- КОЛИ `input(lock)` → ЯКЩО `count(closed_door, <, 2)` → ТО `custom: «зачинити двері в проході, який щойно пройшов злодій»`.
- КОЛИ `timer(door_time)` → ТО `custom: «зачинені двері відчиняються»`.
- КОЛИ `timer(every)` → ТО `custom: «двері біля центру перемикаються самі»`.
- КОЛИ `blocked(police)` → ТО `custom: «поліцейський шукає інший шлях або застрягає»`.
- КОЛИ `contact(lupin, coin)` → ТО `pickup`, `score(20)`.
- КОЛИ `rng(p)` → ТО `spawn_at(money_bag, center)`.
- КОЛИ `contact(lupin, money_bag)` → ТО `score(500 → 1000 → 2000 → 4000)` за порядком появи, `stun(police, n)`.
- КОЛИ `contact(lupin, treasure)` → ТО `pickup`, `score(200 | 300 | 500)`.
- КОЛИ `contact(lupin, police)` → ТО `lose` (життя −1).
- КОЛИ `all_gone(coin)` → ТО `custom: «відкрито вихід»` (?); КОЛИ `reach(lupin, exit)` → ТО `next_level`.
- КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)` — одне на гру (?).
- Перемога: нема (нескінченна аркада). Поразка: 0 життів. Рахунок: монети, мішки за зростанням, скарби.

## Керування і ввід
- Джойстик 4 напрямки + 1 кнопка «Lock».
- Ключове рішення — коли тиснути: двері мають відрізати переслідувача, а не власну дорогу; ліміт 2 змушує «перезаряджати» двері.
- 1–2 гравці по черзі.

## Вікна, меню, HUD
- `splash-screen` / атракт (?).
- `game-screen` — сховище; HUD: `score`, `hi-score` (?), `lives`, `level-number` або скарб рівня (?).
- Переходи: атракт → (монета) game-screen → (монети + вихід) наступний рівень → (0 життів) атракт.

## Фічі поза полем
- `levels-sequential`: від рівня залежить вид скарбу.
- 2 гравці по черзі (`hotseat`).
- Game Boy (1990): 6 етапів по 3 екрани; діамант дає тимчасову невразливість (злодій розкидає поліцію); бонус-раунд «слот-машина», кількість обертів = зібрані діаманти, призи — життя.

## Варіації й родичі
- Порти: Intellivision і Atari 2600 (Mattel, 1982), Apple II (1983), Game Boy (оновлена, 1990), Data East Arcade Classics (Wii), PSN, 3DS VC.
- Родичі: Pac-Man (монети, бонус у центрі), Mouse Trap (двері кнопками кольору), Lady Bug (турнікети проходом), Heiankyo Alien (гравець змінює поле — копає ями).
- Осі: **хто ставить перешкоду** (гравець позаду себе / гравець кнопкою групи / рух аватара); **скільки перешкод** (ліміт активних); **скільки живе перешкода** (назавжди / N секунд).

## Цікавинки для курсу
- Двері, що гравець ставить у щойно пройдений прохід, — 📎: памʼять останнього проходу + тимчасова стіна.
- Ліміт активних дверей (≤ 2) і таймер на кожні — 🌱: черга перешкод.
- Автоматичні двері біля центру за таймером — 🌱.
- Мішок грошей зі зростанням ціни за порядком появи і оглушенням поліції — 🌱.
- Ризик самопастки: перевірка, чи двері не відрізали злодія від монет/виходу — 🥉 (BFS досяжності).

## Мапа на каталог
- Є: `move-4dir` · `collect-all` · `reach-exit` (?) · `touch-death` · `player-death` · `chase-player` · `temporary-modes` (оглушена поліція) · `event-points` · `sequential-levels` · `status-panel` · `game-screen`.
- **Нема** → пропозиції карток:
  - `+player-placed-door` «Гравець зачиняє прохід позаду» · entities/interact · 📎.
  - `+limited-active-doors` «Ліміт одночасних перешкод» · entities/legality · 🌱 · слот {max: 2}.
  - `+self-opening-door` «Тимчасова стіна відчиняється сама» · entities/state · 🌱 · слот {duration}.
  - `+auto-cycling-door` «Двері за таймером» · entities/state · 🌱.
  - `+center-bonus-item` (є в Lady Bug) · `+escalating-bonus-item` «Ціна бонусу росте з кожною появою» · game-logic/score · 🌱.

## Пропозиції до словників
- `+effect:lock` — зачинити двері/прохід (стає стіною зі станом).
- `+effect:unlock` — відчинити двері (за таймером або ключем).
- `+card:player-placed-door`, `+card:limited-active-doors`, `+card:auto-cycling-door` — див. вище.

## Джерела
- ⭐ [Wikipedia: Lock 'n' Chase](https://en.wikipedia.org/wiki/Lock_%27n%27_Chase) — монети 20, двері ≤ 2 і самі відчиняються, автодвері біля центру, мішки 500…4000, скарби 200/300/500, імена поліцейських, порти.
- [KLOV: Lock 'n' Chase](https://www.arcade-museum.com/Videogame/lock-n-chase) — джойстик 4 напрямки, кнопка «1 – Lock», 1–2 гравці по черзі.
- [Wikipedia JA: ロックンチェイス](https://ja.wikipedia.org/wiki/ロックンチェイス) — двері зачиняють щойно пройдений прохід, ризик відрізати собі втечу; Game Boy: діамант, слот-бонус, 6 × 3 екрани.
- YouTube: пошук «lock n chase arcade 1981 gameplay».

## Непевне
- (?) Вихід: за відгуком у пошуку — після збору монет злодій тікає через виходи вгорі або внизу; у відкритих джерелах прямо не підтверджено.
- (?) Імʼя поліцейського: Stiffy (Wikipedia) чи Spiffy (ExoticA у пошуковому сніпеті); поведінка кожного не описана.
- (?) Тривалість зачинених дверей («кілька секунд»), період автодверей, тривалість оглушення.
- (?) Бонусне життя: «лише одне на гру» (пошуковий сніпет), поріг невідомий; стартові життя.
- (?) Чи двері зачиняються саме в останньому пройденому проході чи в найближчому до злодія.
- (?) Ціна скарбу «телефон»; кількість рівнів до повтору.
