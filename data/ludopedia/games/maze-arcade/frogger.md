---
title: Frogger (Жабка) / Crossy Road
slug: frogger
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 1981
platforms: [arcade (Konami/Sega), Atari 2600, PC, mobile (Crossy Road 2014), Apple TV]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Frogger", best: true, note: "правила аркади: дорога, річка, 5 будиночків, таймер 30 с, усі очки"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crossy_Road", note: "нескінченний «Frogger»: персонажі, монети, лотерея"}
  - {kind: official, url: "https://www.crossyroad.com/", note: "офіційний сайт Hipster Whale: режими, Crossy Road Rush"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=frogger+arcade+1981+gameplay", note: "пошук; аркада"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=crossy+road+gameplay", note: "пошук; Crossy Road"}
stage: v1
coverage: 70
mechanics: [move-4dir, row-conveyor, environment-death, touch-death, time-out, time-bonus, event-points, collect-all, player-death, sequential-levels, progress-acceleration, infinite-field, item-pickup, score-records, swipe-gestures, round-currency, avatar-picker, +carrier-platform, +periodic-sink, +home-slots, +idle-punisher, +lane-generator, +prize-machine]
proposes: ["+effect:carry", "+role:platform", "+trigger:idle", "+cond:on_top", "+card:carrier-platform", "+card:periodic-sink", "+card:idle-punisher", "+card:prize-machine", "+window:prize-machine", "+feature:free-gift-timer"]
author: opus
date: 2026-11-02
---

# Frogger — перестрибни дорогу з машинами й річку по колодах до будиночка

## Суть
Жабка стрибає по клітинах знизу вгору через дві смуги небезпек: дорогу, де машини вбивають, і річку, де вбиває сама вода, а колоди й черепахи — єдина опора, що ще й несе жабку вбік. Кожен рядок поля — конвеєр зі своєю швидкістю й напрямком, тож уся гра — читання ритму смуг. Crossy Road (2014) прибрав будиночки й зробив поле нескінченним уперед, додавши кару за бездіяльність і колекцію персонажів.

## Поле і час
- Аркада: один екран, рядки-смуги: старт (тротуар) → дорога (кілька смуг) → розділювальна смуга (безпечна) → річка (кілька смуг) → берег з 5 будиночками.
- Кожна смуга рухається горизонтально з власною швидкістю й напрямком; сусідні річкові смуги — у протилежні боки.
- Real-time: жабка стрибає на 1 клітину за натискання; таймер — 30 секунд на одну жабку.
- Crossy Road: «isometric»-камера, поле нескінченне вперед, ширина обмежена; смуги генеруються на льоту: дорога, річка, залізниця, трава з деревами (перешкоди).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жабка | player | 3/5/7 життів (налаштування) | стрибок 4 напрямки на 1 клітину |
| Машина / вантажівка / бульдозер / баггі | enemy | смуга, швидкість, довжина | їде вздовж смуги, виїжджає з краю й заїжджає з іншого |
| Колода | terrain (platform) | смуга, швидкість, довжина | несе жабку вздовж смуги |
| Черепахи | terrain (platform) | групи, режим пірнання | несуть; деякі групи періодично пірнають — жабка тоне |
| Алігатор (у річці) | terrain / enemy | — | спина несе як колода, паща вбиває |
| Вода | hazard | — | жабка без опори — смерть |
| Змія | enemy | — | повзає по розділювальній смузі / по колоді, дотик — смерть |
| Видра | enemy | — | у річці, нападає на жабку на опорі (?) |
| Будиночок ×5 | gate | порожній / зайнятий | жабка заходить — фіксується там; зайнятий — смерть |
| Муха | pickup | 200 очок | зʼявляється в порожньому будиночку на час |
| Алігатор у будиночку | hazard | — | займає будиночок на час; вхід — смерть |
| Леді-жабка | pickup | 200 очок | їде на колоді; якщо доставити її додому — бонус |
| Кущі між будиночками | static | — | стрибок у них — смерть |
| Потяг (Crossy Road) | enemy | дуже швидкий | проноситься колією; попереджувальний сигнал (?) |
| Латаття (Crossy Road) | terrain | нерухоме | безпечна клітина на річці (?) |
| Дерево / камінь (Crossy Road) | static | — | непрохідна клітина на траві |
| Монета (Crossy Road) | pickup | 1 (червона = 5 з Piggy Bank) | збирається на полі |
| Орел (Crossy Road) | enemy | — | хапає героя при бездіяльності/відступі назад (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(frog, dir)` на 1 клітину; КОЛИ `move(frog, up)` у новий рядок → `score(+10)`.
- КОЛИ `tick` → ТО `custom: «кожна смуга зсувається на свою швидкість і напрям; обʼєкти, що виїхали, повертаються з протилежного краю»` (`row-conveyor`).
- КОЛИ `contact(vehicle, frog)` → ТО `lose` (життя −1).
- КОЛИ `enter(frog, water)` → ЯКЩО `not on_top(frog, log|turtle|gator_back)` → ТО `lose`.
- КОЛИ `tick` → ЯКЩО `on_top(frog, platform)` → ТО `carry(frog, platform_dir)`.
- КОЛИ `edge(frog)` (винесло платформою за край) → ТО `lose`.
- КОЛИ `timer(dive_cycle)` → ТО `set_state(turtles, under)`; ЯКЩО `on_top(frog, turtles)` → ТО `lose`; потім `clear_state`.
- КОЛИ `contact(frog, gator_jaws|snake|otter)` → ТО `lose`.
- КОЛИ `reach(frog, home)` → ЯКЩО `state(home, empty)` → ТО `set_state(home, filled)`, `score(+50)`, `score(+10 × unused_half_seconds)`, `respawn(frog, start)`, таймер з початку.
- КОЛИ `reach(frog, home)` → ЯКЩО `state(home, filled|gator)` → ТО `lose`; кущ між будиночками → `lose`.
- КОЛИ `contact(frog, fly)` в будиночку → ТО `score(+200)`; КОЛИ `reach(frog+lady, home)` → ТО `score(+200)`.
- КОЛИ `all_on(frog, homes)` → ТО `score(+1000)`, `next_level` (швидші смуги, більше небезпек; після 5 рівнів коротке полегшення).
- КОЛИ `counter(time, ==, 0)` (30 с) → ТО `lose`.
- КОЛИ `counter(score, ≥, 20000)` → ТО `lives(+1)`.
- Crossy Road: КОЛИ `tick` → ТО `custom: «генерувати нові смуги попереду камери, стирати позаду»`; рахунок = найдальший рядок.
- Crossy Road: КОЛИ `idle(n)` або відступ назад на кілька рядків → ТО `spawn(eagle)`, `lose` (?).
- Crossy Road: КОЛИ `contact(hero, coin)` → ТО `currency(+1)`; 100 монет → `window(prize_machine)` → випадковий персонаж.
- Перемога: заповнити 5 будиночків (рівень), гра нескінченна по рівнях / Crossy Road — без перемоги, рекорд. Поразка: 0 життів (аркада), перша смерть (Crossy Road). Рахунок: 10 за крок уперед, 50 за дім, 10 за кожні півсекунди залишку, 200 за муху/леді, 1000 за рівень; максимум 99 990 на оригіналі.

## Керування і ввід
- Аркада: 4-напрямний джойстик, один стрибок на одне відхилення; два гравці по черзі.
- Crossy Road: тап — стрибок уперед, свайп — убік/назад; смуги не чекають на гравця.

## Вікна, меню, HUD
- Аркада: `splash-screen`/attract mode → `game-screen`: `score`, `hi-score`, `lives` (жабки знизу), `timer-countdown` смугою «TIME», `level-number` (?).
- Між рівнями — короткий екран/анімація (?); `end-screen` GAME OVER; `leaderboard` з ініціалами (?).
- Crossy Road: `main-menu` = сама гра на старті (тап — пішли), кнопки персонажів → `character-select`, `prize-machine` (лотерея за 100 монет), `shop-window` (персонажі за гроші), `end-screen` з рахунком, рекордом і «Free gift»/відео за монети.
- HUD Crossy Road: `score` (рядки), `hi-score`, `coins`.
- Переходи: game-screen → (смерть) end-screen → (тап) game-screen; end-screen → character-select / prize-machine.

## Фічі поза полем
- Аркада: `levels-sequential` з наростанням складності, налаштування оператора (3/5/7 життів), двоє гравців по черзі (`hotseat`).
- Crossy Road: `unlockables` (сотні персонажів, деякі змінюють світ: Astronaut — космос з астероїдами), `round-currency` → мета-валюта, `free-gift-timer` (подарунок кожні кілька годин), рекламні монети, IAP, `leaderboard-online` (?), multiplayer на tvOS.

## Варіації й родичі
- Frogger 2 (1984), Frogger 3D, Frogger: Hyper Arcade; клони Freeway (Atari 2600, лише дорога, на час, на двох).
- Crossy Road (2014), Disney Crossy Road, Crossy Road Castle, Crossy Road Rush; Pac-Man 256 від тих самих авторів позичив ідею нескінченного поля.
- Родичі за механікою: Chip's Challenge (силова підлога як «несе»), Lode Runner — ні; тут ключова — платформа, що везе.
- **Осі варіацій:**
  - поле: фіксований екран з будиночками / нескінченне вперед;
  - вода: смерть без опори / плавання;
  - опора: нерухома (латаття) / везе (колода) / зникає періодично (черепахи) / частково смертельна (алігатор);
  - кара за повільність: таймер на жабку / орел за бездіяльність;
  - мета: заповнити слоти-будиночки / пройти якнайдалі.

## Цікавинки для курсу
- Смуги-конвеєри з різною швидкістю й напрямком (обгортання по краю) — 🥉: картка `row-conveyor`, швидкість як «тіки через раз».
- Платформа, що везе гравця, і смерть від виносу за край — 📎: двошарова клітина «вода + колода».
- Черепахи, що пірнають за циклом — 🌱: стан з таймером.
- 5 будиночків-слотів із бонусами й пастками (муха, алігатор) — 📎.
- Нескінченна генерація смуг з гарантією прохідності (не два потяги поспіль без паузи, не вода без колод) — 🥇: картка `infinite-field` + `reachability-check`.
- Орел за бездіяльність — 🌱: `idle(n)` → смерть, найпростіший антикемпінг.
- Лотерея персонажів за монети — 📎: мета-економіка поза полем.

## Мапа на каталог
- Є: `move-4dir` · `row-conveyor` · `environment-death` («вода без колоди» — дослівно) · `touch-death` · `time-out` · `time-bonus` · `event-points` · `collect-all` (5 будиночків) · `player-death` · `sequential-levels` · `progress-acceleration` · `infinite-field` («Crossy Road» — дослівно) · `item-pickup` · `score-records` · `swipe-gestures` · `round-currency` · `avatar-picker`.
- **Нема** → пропозиції карток:
  - `+carrier-platform` «Платформа, що везе» · entities/move · 📎 · слот {fall_off_edge: death|wrap}.
  - `+periodic-sink` «Опора, що зникає за циклом» · entities/state · 🌱 · слот {up, down}.
  - `+home-slots` «Слоти-цілі, кожен раз» · game-logic/win · 🌱 — заповнити N гнізд, повторний вхід — смерть.
  - `+idle-punisher` «Кара за бездіяльність» · game-logic/lose · 🌱 · слот {idle_ticks}.
  - `+lane-generator` «Генератор смуг» · levels/generation · 🥈 — дитина `infinite-field`: типи смуг з правилами сусідства.
  - `+prize-machine` «Лотерея за валюту» · game-logic/economy · 📎 — випадкова розблокування.

## Пропозиції до словників
- `+effect:carry` — платформа переносить того, хто на ній стоїть, разом із собою (Frogger, ліфти/конвеєри в платформерах).
- `+role:platform` — рухома опора над небезпечною підлогою; ні `terrain` (рухається), ні `object` (на ній стоять).
- `+trigger:idle` — уже кандидат `idle(n)`; підтверджую (орел у Crossy Road).
- `+cond:on_top` — A стоїть на B (опора над водою); `occupied` описує клітину, а не відношення «на».
- `+card:carrier-platform`, `+card:periodic-sink`, `+card:idle-punisher`, `+card:prize-machine`.
- `+window:prize-machine` — екран лотереї/гачі з анімацією видачі.
- `+feature:free-gift-timer` — подарунок раз на N годин реального часу.

## Джерела
- ⭐ [Wikipedia: Frogger](https://en.wikipedia.org/wiki/Frogger) — повні правила аркади: смуги, колоди, черепахи, що тонуть, алігатори, змії, видри, 5 будиночків з мухою/алігатором, леді-жабка, 30 с, таблиця очок, життя 3/5/7.
- [Wikipedia: Crossy Road](https://en.wikipedia.org/wiki/Crossy_Road) — нескінченний шлях, тап/свайп, персонажі й світи, монети, лотерея 100 монет, Piggy Bank, free gift.
- [crossyroad.com](https://www.crossyroad.com/) — офіційний сайт, споріднені ігри.
- YouTube: пошук «frogger arcade 1981 gameplay», «crossy road gameplay».

## Непевне
- (?) Орел у Crossy Road за бездіяльність / відступ назад — загальновідомо, але в перевірених джерелах не описано; поріг часу невідомий.
- (?) Попереджувальні вогні залізниці й латаття в Crossy Road — з памʼяті.
- (?) Поведінка видри (нападає на жабку з води) і де саме повзає змія — Wikipedia лише перелічує їх як небезпеки.
- (?) Точна кількість смуг (5 дорожніх, 5 річкових) — Wikipedia не вказує.
- (?) Екрани між рівнями і таблиця рекордів в аркаді.
