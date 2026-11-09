---
title: "Robotron: 2084"
slug: robotron-2084
aka: [Robotron, Роботрон 2084]
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
year: 1982
platforms: [arcade, Apple II, Atari 2600, Atari 5200, Atari 7800, Atari 8-bit, Atari Lynx, Atari ST, BBC Micro, Commodore 64, VIC-20, PC (DOS), Xbox 360]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Robotron:_2084", best: true, note: "два джойстики, хвиля = екран, типи роботів і їхня поведінка, родина людей, життя"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=robotron+2084+arcade+gameplay", note: "пошук; геймплей аркади"}
stage: v1
coverage: 60
mechanics: [move-8dir, projectile-shot, shoot-forward, touch-death, environment-death, player-death, chase-greedy, random-walk, realtime-ai, spawner-entity, destroy-all-enemies, enemy-waves, event-points, extra-life-threshold, score-records, attract-demo, game-screen, status-panel, +twin-stick-aim, +rescue-npc, +rescue-bonus-chain, +invulnerable-enemy, +shot-knockback, +npc-to-enemy-convert, +homing-zigzag-missile, +bouncing-shot, +aim-jitter]
proposes: ["+trigger:rescued(a)", "+effect:convert(a, kind)", "+effect:knockback(a, dir)", "+role:rescuee", "+ui:twin-stick", "+card:rescue-bonus-chain", "+card:npc-to-enemy-convert"]
author: opus
date: 2026-11-09
---

# Robotron: 2084 — арена-екран, хвиля роботів, два джойстики: біжи одним, стріляй іншим і рятуй людей

## Суть
Генетичний мутант-рятівник стоїть посеред одного екрана, з усіх боків на нього сунуть сотні роботів. Лівий джойстик — рух у 8 напрямках, правий — постріл у 8 напрямках, **незалежно від руху** (twin-stick). Хвиля закінчується, коли знищено всіх **вразливих** роботів; по полю блукає «остання людська родина», за дотик до кожного — бонус. Межа сімʼї: на відміну від [Berzerk](berzerk.md), нема стін і виходів — арена відкрита, а лабіринтом стає сам натовп.

## Поле і час
- Один екран-арена без стін, вільні координати (`field: free`); межа екрана — рамка, за яку не вийти.
- Хвиля = екран з набором ворогів і перешкод; вороги згруповані за темою хвилі (хвилі мозків, танків тощо).
- Real-time; ранні хвилі прості, складність росте швидко; на тестах на екрані було понад сотню ворогів.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Мутант (гравець) | player | життя | рух 8 напрямків; стріляє в 8 напрямків окремим джойстиком |
| Постріл гравця | projectile | — | летить прямо до межі екрана або цілі |
| Людина (родина: тато, мама, дитина) | neutral | бонус | блукає; дотик гравця рятує; Hulk убиває, Brain перетворює на Prog |
| Electrode | hazard | нерухомий | смертельний при дотику |
| Grunt | enemy | натовп | женеться найкоротшим шляхом (жадібно) до гравця |
| Hulk | enemy | невразливий | блукає, топче людей; постріл лише гальмує/відштовхує |
| Enforcer | enemy | стрілець | стріляє в точку біля гравця з розкидом, снаряд вигинається |
| Spheroid | spawner | — | безперервно породжує Enforcer-ів |
| Brain | enemy | — | ловить людей і промиває мізки → Prog; запускає крилаті ракети |
| Prog | enemy | колишня людина | женеться за гравцем |
| Cruise missile | projectile | самонавідна | летить до гравця зигзагом, важко збити |
| Quark | spawner | — | породжує Tank-и |
| Tank | enemy | стрілець | снаряди відбиваються від країв екрана |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(move_dir)` → ТО `move(player, dir)` (8 напрямків).
- КОЛИ `input(fire_dir)` → ТО `custom: «постріл у напрямку fire_dir незалежно від руху»` (`+card:twin-stick-aim`).
- КОЛИ `contact(player_shot, enemy)` → ЯКЩО `not state(enemy, invulnerable)` → ТО `disappear_both`, `score(n)`.
- КОЛИ `contact(player_shot, hulk)` → ТО `disappear_a`, `custom: «Hulk відштовхується і гальмує»` (`+effect:knockback`).
- КОЛИ `contact(player, enemy)` або `contact(player, electrode)` або `contact(enemy_shot, player)` → ТО `lives(-1)`.
- КОЛИ `contact(player, human)` → ТО `disappear_b`, `score(bonus)`, `custom: «бонус за наступну людину зростає»` (`+card:rescue-bonus-chain`).
- КОЛИ `contact(hulk, human)` → ТО `disappear_b`.
- КОЛИ `contact(brain, human)` → ТО `custom: «людина перетворюється на Prog»` (`transform(prog)`, `+effect:convert`).
- КОЛИ `tick` → ТО Grunt: `custom: «крок до гравця найкоротшим шляхом»` (`chase-greedy`); Hulk, людина: `custom: «випадкове блукання»`.
- КОЛИ `timer(spawn_period)` → ТО `spawn(enforcer)` біля Spheroid; `spawn(tank)` біля Quark.
- КОЛИ `timer(fire_period)` → ЯКЩО `prob(p)` → ТО Enforcer: `custom: «постріл у випадкову точку в радіусі 10 px від гравця з випадковим прискоренням»`.
- КОЛИ `contact(tank_shot, edge)` → ТО `bounce(tank_shot)`.
- КОЛИ `tick` → ТО Cruise missile: `custom: «рух до гравця випадковим зигзагом»`.
- КОЛИ `all_gone(vulnerable_enemy)` → ТО `next_level` (наступна хвиля; Hulk-и не рахуються).
- КОЛИ `counter(score, >=, threshold)` → ТО `lives(+1)` (поріг задає оператор).
- КОЛИ `counter(lives, ==, 0)` → ТО `game_over`.
- Перемога: нема — рекорд. Поразка: скінчились життя. Рахунок: за роботів і за врятованих людей.

## Керування і ввід
- Два 8-позиційні джойстики: лівий — рух, правий — напрям вогню (утримання = безперервна стрільба (?)).
- Кнопок вогню нема: схему Джарвіс вигадав після травми, через яку не міг користуватись джойстиком з кнопкою.
- 1P / 2P Start.

## Вікна, меню, HUD
- `attract-demo` — демо і таблиця рекордів по черзі.
- `game-screen` — арена; HUD угорі ліворуч: `score`, `lives`.
- `leaderboard` — таблиця рекордів (?).
- `end-screen` — GAME OVER.
- Переходи: атракт → (монета, Start) → хвиля 1 → (зачищено) хвиля N+1 → … → (0 життів) GAME OVER → атракт.

## Фічі поза полем
- `operator-settings` — поріг додаткового життя налаштовує власник автомата.
- `hotseat` — двоє гравців по черзі (?).

## Варіації й родичі
- [Berzerk](berzerk.md) — стрільба у 8 напрямків, але в кімнаті з електричними стінами, вихід і Evil Otto; Robotron прибирає стіни і додає людей та генератори ворогів.
- [Wizard of Wor](wizard-of-wor.md) — стрілянина в лабіринті з невидимими ворогами; [Gauntlet](gauntlet.md) — генератори ворогів у лабіринті.
- Smash TV (1990, теж Джарвіс), Llamatron, Robotron X, Robotron 64 — наступники; від Robotron веде лінія twin-stick шутерів (Geometry Wars).
- **Осі варіацій:** арена (порожня / зі стінами / з виходами); вогонь (у бік руху / окремий напрям); NPC (нема / рятувати / вороги їх псують); вороги (вразливі всі / є невразливі, що лише гальмуються).

## Цікавинки для курсу
- Twin-stick: рух і приціл — два незалежні вектори вводу — 🌱.
- Рятування людей зі зростаючим бонусом і скиданням при смерті (?) — 📎 (лічильник ланцюга).
- Brain перетворює людину на ворога — 📎 (transform NPC → enemy, загроза бонусу).
- Hulk невразливий, постріл лише відштовхує — 🌱 (ще одна гілка таблиці «снаряд × сутність»).
- Генератори (Spheroid, Quark) — вороги, що народжують ворогів: пріоритет цілей — 📎.
- Прицілювання Enforcer-а з розкидом і криві снаряди; відбивні снаряди Tank — 🥉 (кілька моделей снарядів).
- Сотня сутностей на екрані без лагів — 🥉 (ефективний цикл оновлення/колізій).

## Мапа на каталог
- Є: `move-8dir` · `projectile-shot` · `shoot-forward` · `touch-death` · `environment-death` (Electrode) · `player-death` · `chase-greedy` (Grunt) · `random-walk` (Hulk, люди) · `realtime-ai` · `spawner-entity` (Spheroid, Quark) · `destroy-all-enemies` · `enemy-waves` · `event-points` · `extra-life-threshold` · `score-records` · `attract-demo` · `game-screen` · `status-panel`.
- **Нема** → пропозиції карток:
  - `+twin-stick-aim` «Рух і постріл окремими напрямками» · interface/input · 🌱.
  - `+rescue-npc` «Врятувати NPC дотиком» · entities/interaction · 🌱.
  - `+rescue-bonus-chain` «Бонус за кожного наступного врятованого зростає» · game-logic/score · 📎 · слоти {step, max}.
  - `+invulnerable-enemy` «Ворог, якого не вбити, лише стримати» · entities/combat · 🌱.
  - `+shot-knockback` «Постріл відштовхує ціль» · entities/combat · 🌱.
  - `+npc-to-enemy-convert` «Ворог перетворює NPC на ворога» · entities/state · 📎.
  - `+homing-zigzag-missile` «Самонавідний снаряд із зигзагом» · entities/combat · 📎.
  - `+bouncing-shot` «Снаряд відбивається від країв» · entities/combat · 🌱.
  - `+aim-jitter` «Прицілювання з випадковим розкидом» · entities/ai · 🌱 · слот {radius}.

## Пропозиції до словників
- `+trigger:rescued(a)` — NPC врятовано (Robotron, Choplifter (?)).
- `+effect:convert(a, kind)` — сутність переходить на бік ворога зі зміною типу (Brain → Prog); ширше за `transform` наміром.
- `+effect:knockback(a, dir)` — відштовхнути без шкоди (Hulk).
- `+role:rescuee` — NPC, якого рятують (родина Robotron, заручники).
- `+ui:twin-stick` — схема вводу з двома стіками.
- `+card:rescue-bonus-chain`, `+card:npc-to-enemy-convert` — див. вище.

## Джерела
- ⭐ [Wikipedia: Robotron: 2084](https://en.wikipedia.org/wiki/Robotron:_2084) — два джойстики, хвиля-екран, типи роботів і їхня поведінка (Grunt, Hulk, Enforcer, Spheroid, Brain, Prog, Cruise missile, Tank, Quark, Electrode), родина, життя за очки (налаштовує оператор), порти, наступники.
- YouTube: пошук «robotron 2084 arcade gameplay».

## Непевне
- (?) Очки за типи роботів і прогресія бонусу за людей (з памʼяті: 1000 → 2000 → … → 5000 за хвилю, скидання після смерті) — Wikipedia чисел не дає; WebSearch вичерпано.
- (?) Поріг додаткового життя за замовчуванням (з памʼяті 25 000).
- (?) Чи гине Grunt від Electrode; чи руйнує постріл Electrode; чи прискорюються Grunt-и з часом.
- (?) Імена родини (Mommy, Daddy, Mikey) — лише з назви журнальної статті в посиланнях.
- (?) Кількість хвиль і зациклення.
