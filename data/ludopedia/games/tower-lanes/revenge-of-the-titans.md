---
title: Revenge of the Titans
slug: revenge-of-the-titans
aka: [RotT]
family: tower-lanes
also: [build-sim]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: survive
year: 2010
platforms: [PC (Windows, Mac, Linux), PS5]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Revenge_of_the_Titans", best: true, note: "TD + RTS, вороги оминають вежі, захист командного центру, дерево досліджень, боси"}
  - {kind: steam, url: "https://store.steampowered.com/app/93200/Revenge_of_the_Titans/", note: "29 будівель, 40 технологій, кампанія 50 рівнів, Endless, Survival"}
  - {kind: official, url: "https://www.puppygames.net/revenge-of-the-titans/", note: "Puppy Games: список будівель, редактор рівнів і кампаній, Yeti Attack"}
  - {kind: other, url: "https://www.gamewatcher.com/reviews/revenge-of-the-titans-review/9303", note: "рецензія: кристали й рафінерії, екран покупок між рівнями, броньовані вороги"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=revenge+of+the+titans+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, enemy-waves, spawn-points, enemy-reached-base, round-currency, shop-between-levels, shop-catalog, in-round-upgrades, projectile-shot, explode-area, hp-damage, temporary-modes, coverage-area, impassable-cells, level-unlock, leaderboard, in-game-editor, achievements-window, +tech-tree, +resource-node-building, +manual-collect, +manual-reload, +adjacency-addon, +core-defense, +no-respec, +threat-forecast]
proposes: ["+trigger:research_done", "+effect:research", "+effect:upgrade", "+effect:reload", "+role:core", "+window:research-window", "+feature:mode-survival"]
author: opus
date: 2026-11-09
---

# Revenge of the Titans — TD-RTS: рафінерії біля кристалів годують вежі, а Титани йдуть до бази в обхід твоєї оборони

## Суть
Гібрид tower defense і RTS від Puppy Games (2010, Humble Indie Bundle 2). На кожному рівні гравець швидко ставить навколо командного центру вежі, барикади, міни й економічні будівлі; Титани хвилями йдуть до бази і, на відміну від класичного TD, **оминають або ігнорують вежі**. Гроші дає видобуток кристалів рафінеріями, тож кожен рівень — баланс «вежа чи рафінерія». Між рівнями — дослідження/покупки за деревом технологій без можливості переграти вибір.

## Поле і час
- Мапа рівня з кристалами, розкиданими по полю; будівлі ставляться на сітку (?) поруч з базою й родовищами.
- Real-time без паузи на хід; хвилі Титанів підходять до бази з країв мапи (?).
- Кампанія — 50 рівнів по світах (Земля, Місяць, Марс, Сатурн, Титан); прогрес (гроші, технології) переходить між рівнями.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Командний центр | static (`+role:core`) | HP | ціль Титанів; знищено → поразка |
| Кристал (родовище) | resource | запас | видобувається рафінерією, що стоїть поруч |
| Рафінерія / Collector / Reprocessor | object | — | рафінування: перетворює кристали на гроші; апгрейди підвищують вихід |
| Blaster turret (і важчі) | tower | шкода, дальність, боєзапас (?) | стріляє по Титанах у радіусі; апгрейдиться |
| Rocket launcher / Laser cannon | tower | — | сильніші турелі з досліджень |
| Capacitor | tower | — | керована гравцем турель: оглушує атакованих Титанів; єдина зброя проти Wraiths |
| Міна / вибухівка | hazard | — | вибухає під Титаном |
| Tangleweb | hazard | — | заплутує/сповільнює (?) |
| Барикада | static | HP | перешкода на шляху |
| Shield generator | object | броня | додає броню будівлям (не HP) |
| Scanner (add-on) | object | — | збільшує дальність виявлення сусідніх турелей |
| Reactor | object | — | add-on енергії для турелей поруч (?) |
| Droid / Tank factory | spawner | — | випускає бойових дроїдів/танки |
| Repair drones | ally | — | лагодять будівлі (?) |
| Титан | enemy | HP | іде хвилею до бази, оминаючи/ігноруючи вежі |
| Броньований Титан | enemy | броня | вимагає двічі прокачаних бластерів |
| Wraith | enemy | — | вразливий лише до Capacitor |
| Бос | boss | багато HP | змушує змінити стратегію |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, building, cell)` → ЯКЩО `has(money, cost)` and `free(cell)` and `custom: «будівля досліджена»` → ТО `place(building, cell)`, `currency(-cost)`.
- КОЛИ `input(place, refinery, cell)` → ЯКЩО `in_range(cell, crystal, n)` → ТО `place(refinery, cell)`; інакше `block`.
- КОЛИ `timer(every)` → ЯКЩО `custom: «рафінерія поруч з кристалом із запасом»` → ТО `custom: «гроші накопичуються в рафінерії»`.
- КОЛИ `input(click, refinery)` → ТО `currency(+stored)` — гроші збирає гравець вручну.
- КОЛИ `in_range(turret, titan, r)` → ЯКЩО `custom: «є боєзапас»` → ТО `damage(titan, n)`; КОЛИ `input(click, turret)` → ТО `custom: «effect reload»` (?).
- КОЛИ `contact(shot, titan)` → ЯКЩО `state(titan, armored)` and `custom: «бластер без двох апгрейдів»` → ТО `custom: «шкода не проходить»`.
- КОЛИ `input(fire, capacitor)` → ТО `stun(titan, n)`; Wraith — `damage` лише від Capacitor.
- КОЛИ `contact(titan, mine)` → ТО `explode(area, n)`, `disappear(mine)`.
- КОЛИ `custom: «add-on поруч з туреллю»` → ТО `set_state(turret, boosted)`: Scanner — +дальність; shield — +броня.
- КОЛИ `tick` → ТО титан `move(titan, toward_base)`, `custom: «оминає або ігнорує вежі»`.
- КОЛИ `contact(titan, building)` → ТО `damage(building, n)`; КОЛИ `hp_zero(building)` → ТО `disappear(building)`.
- КОЛИ `hp_zero(titan)` → ТО `disappear(titan)`, `currency(+n)` (?).
- КОЛИ `hp_zero(command_center)` → ТО `lose`.
- КОЛИ `all_gone(titan)` and `custom: «остання хвиля рівня»` → ТО `win`, `window(shop-window)`.
- КОЛИ `level_end` → ТО `choose(research | building | upgrade)`, `custom: «невитрачені гроші переходять далі»`; вибір незворотний.
- КОЛИ `custom: «наступний рівень має броньованих»` → ТО `message(text)` — попередження лише за рівень наперед.
- Перемога: знищити всі хвилі рівня / пройти кампанію · Поразка: командний центр знищено · Рахунок: ранги й медалі, онлайн-рекорди Survival.

## Керування і ввід
- Миша: вибір будівлі з панелі → клік по полю ставить; клік по рафінерії збирає гроші; клік по турелі — перезарядка (?).
- Capacitor — турель, що стріляє за командою гравця.
- Гарячі клавіші будівель (?).

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Campaign / Endless / Survival (/ Sandbox — DLC).
- `map-window`: світи кампанії (Земля → Титан) (?).
- `game-screen`: поле, панель будівель з цінами, `coins` (гроші), HP бази, хвилі.
- `shop-window` / `+window:research-window`: між рівнями — усі вежі, power-up-и й апгрейди; купівля відкриває нові гілки.
- `end-screen` з рангом/медаллю · `leaderboard` (Survival, Steam Friends hiscores) · `achievements-window` (47).
- `editor-window`: редактор рівнів і кампаній з публікацією онлайн.

## Фічі поза полем
- Режими: кампанія 50 рівнів · `mode-endless` («relaxed») · `+feature:mode-survival` (хвилі проти лімітів часу, онлайн-рекорди) · `mode-sandbox` (DLC).
- `+tech-tree`: 40 технологій, у деяких до 7 передумов; респеку нема — поганий вибір може змусити почати кампанію заново.
- `level-editor` + `level-sharing`: свої поля, Титани, набір зброї, брифінги.
- `cloud-save`, `achievements`; сезонні режими (Xmas), розширення Yeti Attack.
- Вихідний код гри відкрито після Humble Bundle.

## Варіації й родичі
- Попередник — Titan Attacks! (Puppy Games, shoot 'em up).
- Родичі в сімʼї: [they-are-billions](they-are-billions.md) (RTS-TD з економікою й стінами), [creeper-world](creeper-world.md) (база, енергія, ворог зусібіч), [pixeljunk-monsters](pixeljunk-monsters.md); економіка-будівлі — межа з `build-sim`.
- **Осі варіацій**: вороги — йдуть дорогою / по лабіринту з веж / в обхід веж до бази · гроші — за вбивства / з видобутку на полі / пасивний дохід · прогрес — у межах рівня / дерево технологій між рівнями (незворотне).

## Цікавинки для курсу
- Дерево технологій з передумовами (DAG, до 7 батьків) і незворотним вибором — 🥈.
- Рафінерія, що працює лише біля родовища, і ручний збір грошей — 📎.
- Add-on, що підсилює сусідні турелі (Scanner, shield) — 🥉 (сусідство + модифікатори).
- Ворог, що оминає вежі й іде до бази (pathfinding з вагами «небезпеки») — 🥈.
- Броня, яку пробиває лише прокачана зброя, + попередження за рівень наперед — 📎.

## Мапа на каталог
- Є: `tower-placement` + `tower-range` · `enemy-waves` + `spawn-points` · `enemy-reached-base` ↔ командний центр · `round-currency` ↔ гроші з рафінерій · `shop-between-levels` + `shop-catalog` ↔ екран покупок · `in-round-upgrades` · `projectile-shot` · `explode-area` ↔ міни · `hp-damage` · `temporary-modes` ↔ оглушення Capacitor · `coverage-area` ↔ add-on поруч · `impassable-cells` ↔ барикади · `level-unlock` · `leaderboard` · `in-game-editor` · `achievements-window`.
- **Нема** → пропозиції карток:
  - `+tech-tree` «Дерево технологій з передумовами» · game-logic/economy · 🥈 · слот {prereqs}.
  - `+resource-node-building` «Будівля лише біля родовища» · entities/legality · 📎 · слот {radius}.
  - `+manual-collect` «Ручний збір виробленого» · game-logic/economy · 🌱.
  - `+manual-reload` «Ручна перезарядка вежі» · entities/combat · 🌱.
  - `+adjacency-addon` «Add-on підсилює сусідні будівлі» · entities/state · 🥉.
  - `+core-defense` «Ядро-база як ціль ворогів» · game-logic/lose · 🌱.
  - `+no-respec` «Незворотний вибір апгрейдів» · game-logic/economy · 🌱.
  - `+threat-forecast` «Попередження про загрозу наступного рівня» · interface/hud · 🌱.

## Пропозиції до словників
- `+trigger:research_done` — завершено дослідження (відкриває будівлю).
- `+effect:research` — відкрити технологію/будівлю.
- `+effect:upgrade` — підтвердження з сімʼї.
- `+effect:reload` — поповнити боєзапас вежі.
- `+role:core` — база/ядро, яку захищають (як у Legion TD).
- `+window:research-window` — дерево досліджень між рівнями.
- `+feature:mode-survival` — хвилі проти ліміту часу з онлайн-рекордами.

## Джерела
- ⭐ [Wikipedia: Revenge of the Titans](https://en.wikipedia.org/wiki/Revenge_of_the_Titans) — жанр, вороги ігнорують вежі, захист командного центру, дослідження, боси, релізи, відкритий код.
- [Steam](https://store.steampowered.com/app/93200/Revenge_of_the_Titans/) — 29 будівель, 40 технологій, видобуток ресурсів, кампанія 50 рівнів, Endless, Survival, DLC Sandbox.
- [Puppy Games](https://www.puppygames.net/revenge-of-the-titans/) — список будівель (бластери, ракети, лазери, вибухівка, барикади, щити, рафінерії, реактори), редактор рівнів і кампаній, Yeti Attack.
- [GameWatcher: рецензія](https://www.gamewatcher.com/reviews/revenge-of-the-titans-review/9303) — кристали й рафінерії, екран покупок, броньовані вороги, режими.
- Фан-вікі rott.fandom.com (через пошук; сторінки не відкрились, 402) — категорії будівель, Capacitor, Scanner, передумови досліджень.

## Непевне
- (?) Чи будівлі ставляться строго на сітку; розмір мапи.
- (?) Чи Титани йдуть з країв мапи, чи з точок спавну; наскільки саме вони «оминають» вежі.
- (?) Як працює Reactor, Tangleweb, Repair drones; ручна перезарядка турелей (згадує одна рецензія).
- (?) Дослідження між рівнями: безкоштовне (одне за місію) чи за гроші — рецензії суперечать.
- (?) Чи дають гроші вбиті Титани.
- (?) Точна ціль рівня — знищити всі хвилі чи протриматись час.
