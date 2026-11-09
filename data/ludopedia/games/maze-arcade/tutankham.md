---
title: Tutankham
slug: tutankham
aka: [ツタンカーム, Тутанхамон]
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: ai
  info: partial
  random: runtime
  goal: state
year: 1982
platforms: [arcade, Atari 2600, ColecoVision, Intellivision, VIC-20, PV-1000, PC-6001, PS4, Switch]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Tutankham", best: true, note: "лазер лише вліво-вправо, флеш-бомба, один ключ, варп-зони, таймер, порти"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/%E3%83%84%E3%82%BF%E3%83%B3%E3%82%AB%E3%83%BC%E3%83%A0", note: "JA: дві рукоятки (рух / постріл+флеш), кілька замків на етапі, таймер без смерті, Arcade Archives"}
  - {kind: other, url: "https://atariage.com/software_page.php?SoftwareLabelID=572", note: "AtariAge: порт 2600 (Parker Brothers), скани мануала"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=tutankham+arcade+konami+gameplay", note: "пошук; аркада"}
stage: v1
coverage: 65
mechanics: [projectile-shot, key-and-door, inventory-limit, item-pickup, reach-exit, teleport, player-camera, time-bonus, extra-life-threshold, touch-death, player-death, sequential-levels, event-points, status-panel, impassable-cells, +shoot-sideways-only, +smart-bomb, +timer-disarms, +twin-stick-fire, +backtrack-keys, +enemy-proof-teleport]
proposes: ["+trigger:timer_zero", "+ui:flash-stock", "+feature:twin-stick-option"]
author: opus
date: 2026-11-09
---

# Tutankham — лабіринт гробниці зі скролом убік, де стріляти можна лише ліворуч і праворуч

## Суть
Дослідник проходить горизонтально скролений лабіринт гробниці: бере ключ, несе його до замкнених дверей, збирає скарби і врешті відчиняє запечатані двері в кінці зони, за якими скарб і вихід. Лазер стріляє тільки вліво або вправо — вертикальних атак нема, тож вертикальні коридори стають пасткою, коли вороги заходять з двох боків. Таймер не вбиває, а відбирає зброю; одна флеш-бомба на рівень/життя чистить екран.

## Поле і час
- Рівень — довгий клітинний лабіринт ширший за екран; камера скролить горизонтально за гравцем.
- Real-time; таймер зони (TIME) спадає; на нулі — лазер вимикається, але гравець живий.
- Варп-зони всередині рівня переносять гравця в інше місце того ж рівня; вороги ними не користуються.
- Пізні етапи мають кілька замків — після кожного треба повертатись по наступний ключ.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Дослідник | player | життя; 1 флеш | рух лабіринтом; лазер лише ← / → |
| Аспід (asp) | enemy | — | дотик вбиває |
| Гриф (vulture) | enemy | — | дотик вбиває |
| Папуга (parrot) | enemy | — | дотик вбиває |
| Кажан (bat) | enemy | — | дотик вбиває |
| Дракон | enemy | — | дотик вбиває |
| Прокляття (curse) | enemy | — | дотик вбиває |
| Лазерний постріл | projectile | лише горизонталь | вбиває ворога при контакті |
| Стіна | static | — | непрохідна |
| Ключ | pickup | несеш максимум 1 | відмикає один замок |
| Замкнені двері / замок | gate | — | відкриваються ключем |
| Скарб | pickup | очки | бонус |
| Варп-зона | terrain | — | телепорт гравця в іншу точку рівня; вороги не входять |
| Запечатані двері з фінальним скарбом | gate | — | у кінці зони; відчинив і пройшов → кінець рівня |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire_left|fire_right, explorer)` → ЯКЩО `timer(>, 0)` → ТО `spawn(laser, left|right)`; інакше `block`.
- КОЛИ `contact(laser, enemy)` → ТО `disappear(enemy)`, `score(n)`.
- КОЛИ `contact(enemy, explorer)` → ТО `lives(-1)`.
- КОЛИ `input(flash, explorer)` → ЯКЩО `has(explorer, flash)` → ТО `take(explorer, flash)`, `custom: «знищити всіх ворогів на екрані»`.
- КОЛИ `contact(explorer, key)` → ЯКЩО `not has(explorer, key)` → ТО `pickup(explorer, key)`; інакше ключ лишається.
- КОЛИ `contact(explorer, door)` → ЯКЩО `has(explorer, key)` → ТО `take(explorer, key)`, `set_cell(door, floor)`; інакше `block`.
- КОЛИ `contact(explorer, treasure)` → ТО `score(n)`, `disappear(treasure)`.
- КОЛИ `enter(explorer, warp)` → ТО `teleport(explorer, linked_point)`; КОЛИ `contact(enemy, warp)` → ТО `block`.
- КОЛИ `timer(every_second)` → ТО `counter(time, -1)`; КОЛИ `counter(time, ==, 0)` → ТО `custom: «лазер вимкнено до кінця рівня; життя не втрачається»`.
- КОЛИ `reach(explorer, exit_door)` → ТО `score(time_left)`, `next_level`.
- КОЛИ `counter(score, >=, 30000)` → ТО `lives(+1)`.
- КОЛИ `died(explorer)` → ЯКЩО `counter(lives, ==, 0)` → ТО `game_over`; інакше `respawn(explorer, checkpoint)` (?).
- Перемога: пройти рівні до скарбу Тутанхамона. Поразка: життя вичерпано. Рахунок: вороги, скарби, залишок часу.

## Керування і ввід
- Аркада: дві рукоятки. Ліва — рух. Права — вправо = постріл вправо, вліво = постріл вліво, вгору = флеш-бомба.
- Arcade Archives (2024): опції швидкості гри, правий стік 1P через лівий стік 2P, поворот стіка.

## Вікна, меню, HUD
- `attract-demo` / `splash-screen` — аркадний атракт (?).
- `game-screen`: лабіринт зі скролом, `score`, `hi-score`, `timer-countdown` (TIME), `lives`, `+ui:flash-stock` (запас флешів), значок ключа в руках (`inventory-bar`).
- `end-screen` / `leaderboard` — рекорди з ініціалами (?).
- Переходи: атракт → монета → гра → двері зони → наступний рівень → … → життя 0 → атракт.

## Фічі поза полем
- 1–2 гравці по черзі (`hotseat`) (?).
- `operator-settings` — DIP (життя, бонус) (?).
- Сучасний реліз: `speed-control`, `+feature:twin-stick-option` — схема на дві рукоятки на одному геймпаді.

## Варіації й родичі
- Порти Parker Brothers (1983): 2600, ColecoVision, Intellivision, VIC-20; також PV-1000, PC-6001; LCD-версія Bandai (лише 15 пострілів), VFD-версія Bandai/Konami.
- Родичі: `berzerk.md` (стрільба з обмеженням напрямків, вороги-лабіринт), `venture.md` (кімнати зі скарбами й монстрами), `atari-adventure.md` (несеш один предмет), `dandy.md` (ключі й двері, бомба на екран).
- **Осі варіацій:** напрямки стрільби (4/8 / лише горизонталь / вперед); таймер (смерть / вимкнення зброї / карателі як у `timeout-punisher`); ключі (будь-яка кількість / один на руках).

## Цікавинки для курсу
- Стрільба лише вліво-вправо — 🌱: одна умова на напрямок, а геймплей змінюється (вертикальні коридори небезпечні).
- Таймер, що забирає зброю, а не життя, + залишок часу як бонус — 🌱.
- Носиш один ключ: доводиться повертатися (backtracking) — 🌱.
- Варп-зона, якою не можуть ходити вороги (рятівний вихід) — 📎.
- Флеш-бомба «раз на життя» — 🌱.
- Горизонтальна камера по довгому лабіринту — 🥉.

## Мапа на каталог
- Є: `projectile-shot` · `key-and-door` · `inventory-limit` (capacity 1) · `item-pickup` · `reach-exit` · `teleport` · `player-camera` · `time-bonus` · `extra-life-threshold` · `touch-death` · `player-death` · `sequential-levels` · `event-points` · `status-panel` · `impassable-cells`.
- **Нема** → пропозиції карток:
  - `+shoot-sideways-only` «Стрільба лише по горизонталі» · entities/combat · 🌱 (дочірня до `shoot-modes`).
  - `+smart-bomb` «Очистити екран від ворогів» · entities/combat · 📎.
  - `+timer-disarms` «Час вичерпано → зброя вимкнена» · game-logic/lose · 🌱.
  - `+twin-stick-fire` «Друга рукоятка — напрям пострілу» · interface/input · 📎.
  - `+backtrack-keys` «Кілька замків, один ключ на руках» · entities/interact · 🌱.
  - `+enemy-proof-teleport` «Телепорт лише для гравця» · entities/interact · 🌱.

## Пропозиції до словників
- `+trigger:timer_zero` — таймер рівня дійшов нуля (зручніше за `counter(time, ==, 0)`).
- `+ui:flash-stock` — іконки запасу «розумних бомб».
- `+feature:twin-stick-option` — опція схеми керування на дві рукоятки.

## Джерела
- ⭐ [Wikipedia: Tutankham](https://en.wikipedia.org/wiki/Tutankham) — лазер лише вбік, флеш-бомба, один ключ, варп-зони, таймер і бонус часу, життя за 30 000, порти.
- [Wikipedia JA: ツタンカーム](https://ja.wikipedia.org/wiki/%E3%83%84%E3%82%BF%E3%83%B3%E3%82%AB%E3%83%BC%E3%83%A0) — дві рукоятки, флеш на рукоятці вгору, таймер не вбиває, кілька замків, Arcade Archives.
- [AtariAge: Tutankham 2600](https://atariage.com/software_page.php?SoftwareLabelID=572) — порт Parker Brothers.
- YouTube: пошук «tutankham arcade konami gameplay».

## Непевне
- (?) Флеш: EN — «один на рівень або життя», JA — «раз на гравця»; що саме поновлює запас.
- (?) Кількість рівнів (з памʼяті — 4 зони, кожна з кількох частин) і чим зони відрізняються — не перевірено.
- (?) Звідки беруться вороги (гнізда в стінах, з памʼяті) і чи вони відроджуються — не перевірено; поведінка кожного виду не описана в джерелах.
- (?) Де відроджується гравець після смерті (чекпойнт у зоні?); стартові життя.
- (?) Очки за ворогів і скарби не знайдено.
- (?) Аркадний режим на двох — по черзі чи ні; DIP-налаштування.
- WebSearch-ліміт вичерпано, StrategyWiki 403, fandom 402.
