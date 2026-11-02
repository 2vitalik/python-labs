---
title: Wizard of Wor
slug: wizard-of-wor
family: maze-arcade
also: []
klass: avatar
axes:
  field: square
  time: realtime
  opponent: coop
  info: partial
  random: runtime
  goal: score
year: 1980
platforms: [arcade, Atari 2600, Atari 8-bit, Commodore 64, Bally Astrocade]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Wizard_of_Wor", best: true, note: "правила, вороги, Worluk і Wizard, радар, тунелі, кооп/змагання"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=wizard+of+wor+arcade+gameplay", note: "пошук; геймплей"}
  - {kind: steam, url: "https://store.steampowered.com/search/?term=wizard+of+wor", note: "пошук"}
stage: v1
coverage: 60
mechanics: [move-4dir, impassable-cells, projectile-shot, shoot-forward, destroy-all-enemies, touch-death, player-death, chase-player, minimap-radar, spawn-points, speed-per-type, progress-acceleration, sequential-levels, event-points, score-records, +wrap-edges, +invisible-enemy, +escape-bonus-enemy, +double-score-next, +friendly-fire, +door-cooldown, +entry-cage, +speed-by-remaining, +open-arena-level, +extra-life-threshold]
proposes: ["+trigger:all_gone", "+trigger:line_of_sight", "+trigger:timer", "+trigger:counter", "+cond:line_of_sight", "+cond:in_range", "+effect:reveal", "+effect:hide", "+effect:teleport", "+effect:multiplier", "+effect:set_state", "+effect:wrap", "+role:projectile", "+role:boss", "+ui:radar", "+window:attract-demo", "+feature:mode-coop", "+axis:opponent"]
author: opus
date: 2026-11-02
---

# Wizard of Wor — зачисти підземелля від монстрів, частина з яких невидима, удвох або один проти одного

## Суть
Один чи два «Worrior»-и виходять у невеликий лабіринт-підземелля й розстрілюють монстрів, що полюють на них і стріляють у відповідь. Частина монстрів стає невидимою; їх видно лише на **радарі** під полем. Після всіх монстрів зʼявляється Worluk — якщо вбити його до втечі, наступне підземелля дає подвійні очки; далі може прийти сам Чарівник, що телепортується. Двоє гравців діють разом, але можуть стріляти одне в одного за очки.

## Поле і час
- Невелике підземелля-лабіринт на весь екран (клітини-коридори; точний розмір не перевірено (?)), зовнішня стіна з двома бічними дверима-тунелями посередині.
- Бічні двері — тор: вийшов праворуч → зʼявився ліворуч; після проходу двері тимчасово закриваються для всіх.
- Клітини старту гравців — «клітки» в нижніх кутах; монстри зʼявляються у випадкових точках лабіринту.
- Під полем — радар (мініатюра лабіринту з позиціями монстрів), по боках — запасні Worrior-и.
- Real-time; з часом у підземеллі монстри прискорюються (?), з номером підземелля — лабіринти відкритіші, вороги агресивніші.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Worrior (жовтий / синій) | player | життя (?) | рух 4 напрямки, 1 постріл у напрямку погляду |
| Постріл | projectile | — | летить по коридору; вбиває монстра або іншого Worrior-а |
| Burwor (синій «вовк») | enemy | 100 (?) | завжди видимий; переслідує гравця |
| Garwor (жовтий) | enemy | 200 (?) | невидимий, коли не поруч / не на лінії; видно на радарі |
| Thorwor (червоний «скорпіон») | enemy | 500 (?) | як Garwor, швидший |
| Worluk | enemy | 1000 (?) | зʼявляється після всіх монстрів, біжить до тунелю; вбивство → подвійні очки наступного підземелля |
| Wizard of Wor | boss | 2500 (?) | телепортується лабіринтом, стріляє; лишається до вбивства чи смерті гравця |
| Бічні двері | terrain | стан відкрито/закрито | `wrap` на протилежний бік; після проходу закриваються на час |
| Клітка | static | таймер виходу | гравець стоїть у ній до руху або до примусового виходу (?) |
| Стіна | static | — | непрохідна для всіх |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(fire)` → ЯКЩО `count(own_shot, ==, 0)` → ТО `spawn(shot, facing)`.
- КОЛИ `contact(shot, monster)` → ТО `disappear_both`, `score(value × multiplier)`.
- КОЛИ `contact(monster|monster_shot, worrior)` → ТО `lose` (мінус Worrior).
- КОЛИ `contact(shot_of_A, worrior_B)` → ТО `lose(B)`, `score(A, 1000)` (?) — дружній вогонь як частина змагання.
- КОЛИ `line_of_sight(garwor|thorwor, worrior)` або `in_range(…, near)` → ТО `reveal(monster)`; інакше `hide(monster)` — на радарі видно завжди.
- КОЛИ `died(burwor)` → ТО `custom: «на заміну частини Burwor-ів зʼявляються Garwor, далі Thorwor»` (?) — точна схема не перевірена.
- КОЛИ `count(monsters, <, n)` → ТО `speed(monsters, ↑)` (?) — останні монстри швидші.
- КОЛИ `all_gone(monsters)` → ТО `spawn(worluk)`; КОЛИ `reach(worluk, side_door)` → ТО `disappear_a` (утік).
- КОЛИ `contact(shot, worluk)` → ТО `score(1000)`, `multiplier(×2, next_dungeon)`, і може зʼявитись Wizard (?).
- КОЛИ `timer(wizard)` → ТО `teleport(wizard, random_cell)`, стріляє; КОЛИ `contact(shot, wizard)` → ТО `score(2500)`.
- КОЛИ `contact(a, side_door)` → ЯКЩО `state(door, open)` → ТО `wrap(a)`, `set_state(doors, closed, t)`.
- КОЛИ `timer(cage)` → ТО `move(worrior, into_maze)` — гравець не може сидіти в клітці вічно (?).
- КОЛИ `all_gone(monsters+worluk+wizard)` → ТО `next_level`; певні підземелля — особливі: **Arena** (?) і **The Pit** — без внутрішніх стін.
- Перемога: нема (рекорд), звання «Worlord» за глибокі підземелля (?). Поразка: втрачено всіх Worrior-ів. Рахунок: монстри 100–2500, інший гравець, ×2 після Worluk.

## Керування і ввід
- Джойстик 4 напрямки з гашеткою на рукоятці (по одному на гравця); кнопки 1P/2P.
- Два гравці грають **одночасно** (кооп + змагання) — жовтий і синій Worrior; у грі на одного — лише проти монстрів (?).

## Вікна, меню, HUD
- `splash-screen` / атракт: представлення монстрів з очками, демо (`+window:attract-demo`), синтезована мова Чарівника.
- `game-screen` — лабіринт; під ним `+ui:radar` (мінікарта з монстрами), `score` обох гравців, `lives` — запасні Worrior-и по боках поля, назва підземелля («DOUBLE SCORE DUNGEON», «THE ARENA», «THE PIT», «WORLORD DUNGEON») (?).
- Перехід між підземеллями — заставка з назвою і мелодією (5 нот «Dragnet»; п'ята — лише якщо Worluk убитий).
- «GAME OVER» → атракт.

## Фічі поза полем
- `mode-coop` / `mode-versus` одночасно: одна партія, де гравці і союзники, і суперники (`+feature:mode-coop`).
- `+feature:operator-settings` (DIP): кількість Worrior-ів, бонусний Worrior (?).
- `score-records` — hi-score; збережень, паузи нема.
- Синтез мови — Чарівник насміхається з гравців.

## Варіації й родичі
- Порти Atari 2600/C64 — менші лабіринти, ті самі монстри; Gorf (той самий розробник, Midway) — мова й кілька «місій».
- Родичі: Pac-Man (лабіринт, тунель-тор), Berzerk (стрільба в лабіринті), Gauntlet (кооп у лабіринті), Bomberman (друг = суперник).
- **Осі варіацій:** видимість ворогів (завжди / лише поруч / лише на радарі); бонусний ворог (тікає — втрачено / вбито — множник); стосунки гравців (кооп / змагання / обидва одразу).

## Цікавинки для курсу
- Невидимий ворог + радар: дві проєкції одного стану (поле з туманом, мінікарта повна) — 🥉.
- Бонусний ворог, що тікає до виходу, з нагородою-множником на наступний рівень — 📎.
- Бічні двері-тор, що закриваються після проходу (cooldown) — 📎.
- Бос, що телепортується і стріляє — 🥉.
- Дружній вогонь з очками за суперника в кооп-грі — 📎.
- Рівень без стін (The Pit) як «екзамен» на ту саму логіку — 🌱.

## Мапа на каталог
- Є: `move-4dir` · `impassable-cells` · `projectile-shot` · `shoot-forward` · `destroy-all-enemies` · `touch-death` · `player-death` · `chase-player` · `minimap-radar` (радар) · `spawn-points` · `speed-per-type` · `progress-acceleration` · `sequential-levels` · `event-points` · `status-panel` · `score-records` · `game-screen` · `splash-screen`.
- **Нема** → пропозиції карток:
  - `+wrap-edges` «Тор по краях» · entities/move · 🌱 (Snake, Pac-Man).
  - `+door-cooldown` «Прохід закривається на час після використання» · entities/legality · 📎 (споріднено з `teleport-cooldown`).
  - `+invisible-enemy` «Ворог видимий лише поруч / на радарі» · entities/state · 🥉 · слот {reveal: near|line|never}.
  - `+escape-bonus-enemy` «Бонусний ворог тікає до виходу» · entities/spawn · 📎.
  - `+double-score-next` «Множник очок на наступний рівень» · game-logic/score · 🌱.
  - `+friendly-fire` «Гравці можуть уразити одне одного» · entities/combat · 📎 · слот {points}.
  - `+entry-cage` «Клітка старту з таймером виходу» · entities/spawn · 🌱.
  - `+speed-by-remaining` «Темп росте, коли ворогів меншає» · game-logic/waves · 📎 (Space Invaders).
  - `+open-arena-level` «Особливий рівень без стін» · levels/progression · 🌱.
  - `+extra-life-threshold` «Додаткове життя за очки» · game-logic/score · 🌱.

## Пропозиції до словників
- `+trigger:all_gone` — усі монстри знищені (Worluk); `+trigger:line_of_sight` / `+cond:line_of_sight` — невидимий монстр проявляється на лінії; `+cond:in_range` — проявлення поруч; `+trigger:timer` — телепорт Чарівника, закриття дверей; `+trigger:counter`.
- `+effect:reveal` / `+effect:hide` — видимість окремої сутності (не клітин); `+effect:teleport` (є ✅) — Чарівник; `+effect:multiplier` — ×2 на наступне підземелля; `+effect:set_state` — двері закрито; `+effect:wrap`.
- `+role:projectile`; `+role:boss` — Чарівник.
- `+ui:radar` — мінікарта, що показує приховане (ширше за `minimap`).
- `+window:attract-demo`; `+feature:mode-coop` — кооп і змагання в одній партії.
- `+axis:opponent` — значення `coop+versus` (союзник, у якого можна стріляти): сьогодні вісь не дозволяє обидва.

## Джерела
- ⭐ [Wikipedia](https://en.wikipedia.org/wiki/Wizard_of_Wor) — мета, Burwor/Garwor/Thorwor, Worluk і подвійні очки, Чарівник, тунелі, що тимчасово закриваються, радар, два гравці, мова, «Dragnet».
- YouTube: пошук «wizard of wor arcade gameplay».
- Steam: пошук «wizard of wor».

## Непевне
- (?) Очки за монстрів (100/200/500/1000/2500) і 1000 за іншого гравця — з памʼяті, Wikipedia не наводить.
- (?) Умова невидимості Garwor/Thorwor (поруч чи на лінії), схема появи Garwor/Thorwor після Burwor-ів — з памʼяті.
- (?) Номери підземель Arena / The Pit / Worlord і бонусний Worrior — не перевірено (StrategyWiki 403, ліміт пошуку вичерпано).
- (?) Таймер клітки старту і прискорення монстрів з часом — з памʼяті.
- (?) Розмір лабіринту в клітинах — не перевірено.
