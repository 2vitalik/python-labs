---
title: Age of War / Stick War
slug: age-of-war-stick-war
aka: [Age of War, Stick War, Stick War Legacy, Епоха війни, lane battler]
family: tower-lanes
also: []
klass: hybrid
axes:
  field: 1d
  time: realtime
  opponent: ai
  info: full
  random: none
  goal: state
year: 2007
platforms: [web, Flash, iOS, Android]
links:
  - {kind: other, url: "https://www.crazygames.com/game/age-of-war", best: true, note: "Age of War: 5 епох (Stone…Future), XP за вбивства → нова епоха, турелі й нові слоти, спецатака; Louissi, жовтень 2007"}
  - {kind: play, url: "https://www.kongregate.com/games/Louissi/age-of-war", note: "Kongregate 2008: 16 юнітів і 15 турелей, кнопки вгорі, лише миша"}
  - {kind: other, url: "https://www.crazygames.com/game/stick-war", note: "Stick War: серпень 2009, Jason Whitham і Brock White, керування окремим стікменом A/D + пробіл, знищити статую"}
  - {kind: other, url: "https://apps.apple.com/us/app/stick-war-legacy/id1001780528", note: "Stick War: Legacy (Max Games): золото копають, формації або ручне керування, режими й складності"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=age+of+war+flash+gameplay", note: "пошук; геймплей Age of War"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=stick+war+flash+gameplay", note: "пошук; геймплей Stick War"}
stage: v1
coverage: 55
mechanics: [round-currency, hp-damage, melee-vs-ranged, explode-area, move-auto, chase-greedy, enemy-reached-base, ai-opponent, tower-placement, tower-range, in-round-upgrades, difficulty-levels, difficulty-select, game-screen, main-menu, end-screen, mode-select, sequential-levels, world-map, +lane-grid, +auto-march-units, +worker-economy, +age-evolution, +xp-from-kills, +special-attack-cooldown, +turret-slots, +army-formation-command, +possess-unit]
proposes: ["+trigger:produced", "+effect:produce", "+effect:evolve_age", "+effect:set_formation", "+effect:possess", "+ui:build-bar", "+ui:xp-bar", "+ui:special-meter", "+axis:control=possess", "+feature:formation-commands"]
author: opus
date: 2026-11-09
---

# Age of War / Stick War — Flash-битви на одній лінії між двома базами: купи юніта, він іде сам; еволюціонуй або візьми бійця в руки

## Суть
Два флеш-хіти жанру «lane battler»: поле — горизонтальна смуга, на лівому кінці твоя база, на правому — ворожа; куплені юніти самі марширують і бʼються з першим зустрічним. **Age of War** (Louissi, 2007) додає еволюцію: досвід за вбивства переводить базу в наступну епоху з новими юнітами й турелями, а спецатака раз у кілька хвилин чистить лінію. **Stick War** (2009) додає економіку шахтарів, команди всьому війську (формації) і змогу взяти будь-якого стікмена під пряме керування.

## Поле і час
- Поле — 1D-смуга, вид збоку; камера прокручується вздовж лінії (Stick War — ширша мапа з золотими копальнями між базами (?)).
- Обидві сторони діють одночасно в realtime; тік — кадр анімації; темп задає вартість і швидкість юнітів.
- Age of War: юніти йдуть **колоною** — передній бʼється, задні стоять у черзі за ним (дальні стріляють через голови (?)).
- Stick War: юніти можуть стояти групою, відходити до бази або наступати (формація), шахтарі ходять копальня ↔ статуя.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| База / печера (AoW) | static | HP, епоха | точка найму; HP 0 = кінець бою |
| Статуя (SW) | static | HP | ціль ворога; знищити ворожу = підкорити націю |
| Юніт ближнього бою | ally | ціна, HP, шкода | марширує до ворожої бази, бʼє впритул першого ворога |
| Юніт дальнього бою | ally | ціна, HP, шкода, дальність | зупиняється на дистанції й стріляє |
| Важкий юніт (AoW) | ally | дорожчий, HP більше | танк епохи (катапульта/кавалерія/танк) (?) |
| Суперюніт (AoW, Future) | ally | дуже дорогий | 16-й юніт поверх 5×3 епохових (?) |
| Турель (AoW) | tower | ціна, дальність, епоха | ставиться в слот на базі, стріляє по ворогах у дальності; продається (?) |
| Слот турелі (AoW) | zone | ціна відкриття | місце під турель; додаткові слоти купуються |
| Спецатака (AoW) | projectile | перезарядка | дощ снарядів по всій лінії (каміння, стріли, артилерія, лазери (?)) |
| Шахтар (SW) | ally | ціна | копає золото в копальні й несе до статуї |
| Золота копальня (SW) | resource | запас (?) | джерело золота для шахтарів |
| Swordwrath / Archidon / Spearton / Magikill / Giant (SW) | ally | ціна в золоті (і мані (?)) | мечник, лучник, спірмен зі щитом, маг з площинними чарами, гігант |
| Ворожі юніти й турелі | enemy | ті самі | дзеркальна поведінка, AI купує й еволюціонує сам |
| Золото | resource | — | на найм, турелі, слоти, апгрейди |
| Досвід (AoW) | resource | поріг епохи | накопичується від вбивств і бою |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(buy, unit)` → ЯКЩО `has(gold, price)` → ТО `currency(-price)`, `custom: «юніт стає в чергу виробництва»`; КОЛИ `custom: «черга видала юніта»` → ТО `spawn_at(unit, base)` (?).
- КОЛИ `spawned(unit)` → ТО `move(unit, toward_enemy_base)` щотіку (без керування гравцем).
- КОЛИ `blocked(unit)` → ЯКЩО `custom: «попереду свій юніт»` → ТО `custom: «стоїть у колоні»` (AoW).
- КОЛИ `in_range(unit, enemy, range)` → ТО `custom: «зупиняється»`, `damage(n)` за перезарядкою атаки.
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`, `currency(+bounty)`, `counter(xp, +n)` (AoW: гроші й досвід за вбивство; точні суми — (?)).
- КОЛИ `counter(xp, >=, threshold)` → ЯКЩО `custom: «епоха < 5»` → ТО `custom: «кнопка «Evolve» активна»`; КОЛИ `input(evolve)` → ТО `custom: «нова епоха: інші юніти, турелі, спецатака; база змінює вигляд»`.
- КОЛИ `input(buy_slot)` → ЯКЩО `has(gold, price)` → ТО `currency(-price)`, `unlock(turret_slot)`.
- КОЛИ `input(place, turret, slot)` → ЯКЩО `has(gold, price)` and `free(slot)` → ТО `place(player, turret)`; КОЛИ `in_range(turret, enemy, range)` → ТО `damage(n)`.
- КОЛИ `input(sell, turret)` → ТО `disappear_a`, `currency(+part)` (?).
- КОЛИ `input(special)` → ЯКЩО `timer(<=, 0)` → ТО `custom: «залп снарядами по лінії»`, `damage(n)` кожному ворогу під ударом, `timer(start)` перезарядки.
- КОЛИ `input(buy, miner)` → ЯКЩО `has(gold, price)` → ТО `spawn_at(miner, statue)` (SW).
- КОЛИ `reach(miner, mine)` → ТО `custom: «копає порцію золота»`; КОЛИ `reach(miner, statue)` → ТО `currency(+n)`.
- КОЛИ `input(command, garrison|defend|attack)` → ТО `custom: «усе військо: сховатись у статую / стати строєм перед нею / наступати»` (SW).
- КОЛИ `input(select, unit)` → ТО `custom: «юніт під прямим керуванням: A/D — рух, пробіл — дія»`; решта армії діє за формацією (SW).
- КОЛИ `reach(enemy, base)` → ТО `damage(base, n)`.
- КОЛИ `destroyed(enemy_base)` → ТО `win`; КОЛИ `destroyed(own_base)` → ТО `lose`.
- Перемога: знести ворожу базу (AoW) / статую й підкорити націю, далі наступна (SW) · Поразка: своя база/статуя впала · Рахунок: у AoW — нема (?), прогрес — епоха.

## Керування і ввід
- Age of War: лише миша — ряд кнопок угорі: юніти поточної епохи, турелі, слоти, спецатака, Evolve; клік по слоту для турелі.
- Stick War: миша — кнопки найму внизу (?) і три кнопки формацій; клік по стікмену — пряме керування, A/D або стрілки — рух, пробіл — атака/дія.
- Камера: прокрутка вздовж лінії (миша до краю або стрілки (?)).

## Вікна, меню, HUD
- `main-menu` — Play / вибір складності (AoW: серед рівнів є «Impossible»), у SW — Campaign.
- `difficulty-select` (AoW; у Stick War Legacy — Normal, Hard, Insane).
- `game-screen`: лінія, дві бази з `hp-bar`, `coins` (золото), `+ui:xp-bar`, `+ui:build-bar` з цінами, `+ui:special-meter` (заряд спецатаки), підсвітка доступної кнопки Evolve.
- SW: `world-map` / мапа націй (Legacy: «захопити всі території»), кнопки формацій, виділений юніт підсвічено (`selection-highlight`).
- `end-screen` — перемога/поразка.
- Legacy: `mode-select` — Classic Campaign, Missions, Endless Deads (зомбі-виживання), Tournament; магазин скінів (`shop-window`).

## Фічі поза полем
- AoW: `difficulty-presets`; одна партія без збережень (?).
- SW: кампанія націй послідовно, апгрейди між боями (?); Legacy — щотижневі місії, турнір, нескінченний режим виживання, скіни з перками.

## Варіації й родичі
- Age of War 2 і Stick War 2: Order Empire — сиквели з ширшим набором юнітів (?).
- У корпусі: [swords-and-soldiers](swords-and-soldiers.md) (та сама лінія, шахтарі, заклинання), [plants-vs-zombies](plants-vs-zombies.md) (смуги замість однієї лінії, оборона без бази ворога), [clash-royale](clash-royale.md) (висадка юніта, що діє сам), [loop-hero](../build-sim/loop-hero.md) (герой сам іде, гравець будує довкола).
- Мобільні наступники жанру: The Battle Cats, Cartoon Wars, Kingdom Wars (?).
- **Осі варіацій**: дохід — за вбивства / пасивний / шахтарі · прогрес — еволюція епохи / дослідження / між боями · контроль — нуль / формації / пряме керування одним · оборона — турелі в слотах / вежі на лінії / нема.

## Цікавинки для курсу
- 1D-бій колоною: передній бʼється, решта чекає, дальні бʼють через голови — 🌱.
- Гроші й досвід за вбивство + кнопка еволюції, що міняє набір юнітів і турелей — 📎.
- Спецатака з перезарядкою, що бʼє всіх ворогів на лінії — 🌱.
- Слоти турелей на базі: купити слот → поставити турель → продати — 📎.
- Шахтарі-економіка + три формації армії — 📎.
- «Вселитись» у будь-якого юніта: перемикання AI ↔ ручне керування на ходу — 🥉 (два режими одного актора).
- AI-суперник, що теж купує й еволюціонує за таймером/грошима — 🥉.

## Мапа на каталог
- Є: `round-currency` ↔ золото · `hp-damage` · `melee-vs-ranged` · `explode-area` ↔ спецатака/маги · `move-auto` / `chase-greedy` ↔ марш до ворога · `enemy-reached-base` · `ai-opponent` · `tower-placement` / `tower-range` ↔ турелі · `in-round-upgrades` ↔ епоха, слоти · `difficulty-levels` / `difficulty-select` · `world-map` ↔ нації SW · `mode-select` (Legacy).
- **Нема** → пропозиції карток:
  - `+lane-grid`, `+auto-march-units`, `+worker-economy` — див. `swords-and-soldiers.md`.
  - `+age-evolution` «Еволюція епохи: новий набір юнітів/веж за поріг досвіду» · game-logic/economy · 📎.
  - `+xp-from-kills` «Досвід і гроші за вбивство» · game-logic/score · 🌱.
  - `+special-attack-cooldown` «Глобальна атака з перезарядкою» · entities/combat · 🌱.
  - `+turret-slots` «Обмежені слоти під вежі, що докуповуються» · entities/combat · 📎.
  - `+army-formation-command` «Одна команда всьому війську: сховатись / оборона / атака» · entities/move · 📎.
  - `+possess-unit` «Взяти будь-якого AI-юніта під ручне керування» · interface/input · 🥉.

## Пропозиції до словників
- `+trigger:produced` · `+effect:produce` — черга виробництва (як у Swords & Soldiers).
- `+effect:evolve_age` — перехід у наступну епоху з заміною набору сутностей.
- `+effect:set_formation` — задати поведінку всім юнітам сторони.
- `+effect:possess` — передати юніта під пряме керування гравця.
- `+ui:build-bar` · `+ui:xp-bar` · `+ui:special-meter`.
- `+axis:control=possess` — гравець керує одним юнітом з армії на вибір.
- `+feature:formation-commands`.

## Джерела
- ⭐ [CrazyGames: Age of War](https://www.crazygames.com/game/age-of-war) — 5 епох (Stone, Castle, Renaissance, Modern, Future), XP за вбивства, турелі й нові слоти, спецатака, Louissi, 2007.
- [Kongregate: Age of War](https://www.kongregate.com/games/Louissi/age-of-war) — 16 юнітів, 15 турелей, кнопки вгорі, лише миша, 2008.
- [CrazyGames: Stick War](https://www.crazygames.com/game/stick-war) — 2009, автори, класи юнітів, керування окремим стікменом, ціль — статуя.
- [App Store: Stick War: Legacy](https://apps.apple.com/us/app/stick-war-legacy/id1001780528) — золото копають, формації або ручне керування, режими, складності.
- YouTube: пошук «age of war flash gameplay», «stick war flash gameplay».

## Непевне
- (?) Дохід AoW: лише за вбивства чи ще пасивний; суми золота/XP, пороги епох, частка повернення за продаж турелі.
- (?) Розклад 16 = 5×3 + суперюніт і 15 = 5×3 турелей — виведено з чисел Kongregate, не перевірено.
- (?) Назви формацій SW (Garrison / Defend / Attack) — з памʼяті й брифа куратора; чи є мана в першій Stick War і хто її витрачає (Magikill?).
- (?) Чи є в AoW черга виробництва з часом, чи юніт виходить одразу.
- (?) Сиквели Age of War 2 / Stick War 2 і мобільні родичі — з памʼяті.
- Wikipedia-статей про обидві гри не знайдено; Newgrounds віддає 403, fandom — 402.
