---
title: Random Dice (+ Rush Royale)
slug: random-dice
family: tower-lanes
also: [falling-match]
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: runtime
  goal: survive
year: 2019
platforms: [Android, iOS, PC (Rush Royale)]
links:
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=random+dice+pvp+gameplay", best: true, note: "пошук; 10 хв відео пояснюють злиття й економіку краще за текст"}
  - {kind: official, url: "https://apps.apple.com/us/app/random-dice-pvp-defense/id1462877149", note: "App Store: 111%, колода з 5 кубиків, PvP, co-op Boss Raid, Solo, Crew Battle, Mirror"}
  - {kind: other, url: "https://play.google.com/store/apps/details?id=com.percent.royaldice", note: "Google Play"}
  - {kind: wiki, url: "https://ko.wikipedia.org/wiki/랜덤_다이스", note: "старт 28.08.2019 як Royal Dice, перейменування 18.12.2019; походить від Just Dice"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Rush_Royale", note: "Rush Royale (2020): поле 3×5, мана, злиття двох → випадковий юніт колоди"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=rush+royale+gameplay", note: "пошук; Rush Royale"}
stage: v1
coverage: 75
mechanics: [tile-merge, drag-drop-piece, spawn-random-cell, round-currency, in-round-upgrades, enemy-waves, spawn-schedule, enemy-reached-base, hp-damage, projectile-shot, shoot-cooldown, blast-wave, temporary-modes, speed-per-type, player-death, ai-opponent, leaderboard, save-progress, shop-between-levels, +tower-range, +cost-escalation, +merge-random-upgrade, +pips-as-shots, +loadout-select, +aura-buff, +boss-fight, +garbage-attack, +mirror-lanes, +deck-of-types, +crit-meta-stat, +growth-over-time, +copy-neighbor]
proposes: ["+trigger:merge", "+cond:same", "+effect:merge", "+effect:spawn_random", "+effect:power_up", "+role:tower", "+role:tile", "+ui:summon-button", "+ui:power-up-bar", "+ui:opponent-boards", "+ui:sp-counter", "+window:loadout-select", "+window:lobby-window", "+feature:mode-versus", "+feature:mode-coop", "+feature:rank-tiers", "+feature:gacha", "+axis:session=match"]
author: opus
date: 2026-11-02
---

# Random Dice — TD злиттям на сітці 3×5: два однакові кубики → випадковий кубик на крапку вищий

## Суть
Гравець має поле 5×3 і колоду з 5 видів кубиків; кнопка «призвати» за SP ставить **випадковий кубик колоди з 1 крапкою** у випадкову вільну клітину. Кубики-вежі стріляють по ворогах, що біжать смугою довкола поля; кількість крапок = кількість «стволів». Перетягнути кубик на **такий самий вид із тією самою кількістю крапок** — вони зливаються в **випадковий вид колоди з крапками +1**. Ядро — керування випадковістю: злиття дає силу, але може зламати розстановку; призов дорожчає з кожним разом. У PvP два гравці на окремих полях отримують однакові хвилі; хто перший втратить 3 життя — програв.

## Поле і час
- Поле гравця — 5 стовпців × 3 рядки = 15 слотів; вороги рухаються **смугою-доріжкою навколо поля** (П-подібний маршрут) від старту до бази (?).
- Real-time, хвилі з таймером; між хвилями нема паузи, бос — у кінці хвилі (?).
- PvP: екран поділено — твоє поле знизу, поле суперника згори (дзеркально), видно його кубики й ворогів.
- Co-op: двоє гравців на одній спільній доріжці, кожен зі своїм полем (?).
- Rush Royale: той самий принцип, поле 3×5, вороги йдуть доріжкою з порталу до воріт замку.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Кубик (die) | tower (+role) / tile | вид, крапки 1–7, рівень класу, power-up | стріляє в ціль доріжки; крапки = кількість снарядів за постріл |
| Fire | tower | сплеск | вогняний снаряд з шкодою по області |
| Electric | tower | ланцюг | блискавка перескакує на сусідніх ворогів |
| Wind | tower | швидкість атаки | стріляє швидше |
| Poison | tower | DoT | отрута, шкода з часом |
| Ice | tower | сповільнення | сповільнює ціль |
| Iron | tower | ×шкода босам | сильний проти боса |
| Light | tower | аура | прискорює атаку сусідніх кубиків |
| Growth | tower | таймер | сам +1 крапка через час |
| Joker | tower | — | при злитті копіює вид іншого кубика (?) |
| Mimic | tower | — | зливається з будь-яким видом з тими ж крапками (?) |
| Sacrifice | tower | — | при злитті дає SP |
| Інші види (Gamble, Lock, Mine, Moon, Sun, Crack, Combo, Critical…) | tower | — | десятки видів з власною ціллю/ефектом |
| Звичайний ворог | enemy | HP росте з хвилею | біжить доріжкою |
| Швидкий ворог | enemy | висока швидкість | менше HP |
| Великий ворог | enemy | багато HP | при смерті дає більше SP (?) |
| Бос (Snake, Knight, Silence, Magician, Dark Mage…) | boss | вміння | Silence блокує кубики; Magician перетворює кубики; Knight — висока броня (?) |
| База (життя) | static | 3 життя (PvP) | ворог дійшов → −1 |
| SP | resource | — | дається за вбивства й з часом; витрачається на призов і power-up |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(summon)` → ЯКЩО `has(sp, cost)` and `count(dice, <, 15)` → ТО `custom: «effect spawn_random: вид = випадковий з колоди, крапки = 1, клітина = випадкова вільна»`, `currency(-cost)`, `custom: «cost += 10»` (`cost-escalation`).
- КОЛИ `input(drag, die_a, die_b)` → ЯКЩО `same(a, b, kind)` and `same(a, b, pips)` and `custom: «pips < 7»` → ТО `merge(a, b → c)`: `c` у клітині `b`, `c.kind = random(deck)`, `c.pips = pips+1`; клітина `a` звільняється. Інакше `block` (кубик повертається).
- Винятки злиття: Joker — `transform(joker, kind_of(target))` замість злиття (?); Mimic — зливається з будь-яким видом (?); Sacrifice — `currency(+sp)` при злитті.
- КОЛИ `timer(every)` → кубик `custom: «обирає ціль: за замовчуванням передній ворог на доріжці (найдалі просунутий); деякі види — випадковий/найсильніший»` → `spawn(projectile) × pips`.
- КОЛИ `contact(projectile, enemy)` → ТО `damage(n × class_level × power_up)`; `rng(crit_chance)` → `damage × crit`; Fire — `damage(area)`; Electric — `custom: «ланцюг на k сусідів»`; Ice — `speed(enemy, ×k)` стек до ліміту; Poison — `custom: «DoT»`.
- КОЛИ `adjacent(light, die)` → ТО `custom: «аура: speed атаки сусіда +x%»` (`+aura-buff`).
- КОЛИ `timer(growth_t)` → Growth `set_value(pips, +1)`.
- КОЛИ `input(power_up, kind)` → ЯКЩО `has(sp, price[level])` → ТО `custom: «effect power_up: усі кубики виду +шкода в цьому матчі»`, ціна росте (100, 200, 400, 700 (?)).
- КОЛИ `hp_zero(enemy)` → ТО `disappear_a`, `currency(+sp)`.
- КОЛИ `reach(enemy, end_of_lane)` → ТО `lives(-1)`, `disappear_a`.
- КОЛИ `schedule(boss_wave)` → ТО `spawn_at(boss, lane_start)`; Silence — `set_state(random_dice, silenced, t)`; Magician — `transform(random_dice, random_kind)` (?).
- КОЛИ `counter(lives, ==, 0)` → ТО `lose` (PvP: суперник `win`).
- Rush Royale: злиття двох однакових юнітів одного рангу → випадковий юніт колоди рангу +1 (те саме правило); у PvP убиті тобою монстри **переходять на доріжку суперника** (`garbage-attack`).
- Co-op: хвилі босів нескінченні; рахунок — номер досягнутої хвилі.
- Перемога: PvP — суперник втратив 3 життя · Поразка: твої 3 життя · Рахунок: трофеї/рейтинг (PvP), хвиля (co-op).

## Керування і ввід
- Тап по кнопці Summon — призов (місце випадкове, гравець не обирає).
- Drag кубика на інший — злиття; відпустив не на пару — повернення на місце (`drag-drop-piece`).
- Тап по іконці виду в нижній панелі — power-up виду за SP.
- Емоції/реакції суперникові (?); жодного керування ціллю — лише розстановка через злиття.

## Вікна, меню, HUD
- `main-menu` / лобі з вкладками: Battle (PvP), Co-op, Deck, Shop, Clan/Crew (?).
- `loadout-select` (⏳): колода з 5 видів, кілька збережених колод; рівень класу кожного кубика.
- `shop-window`: скрині, кубики за золото/діаманти; `+feature:gacha` (випадкові скрині).
- `game-screen`: твоє поле 5×3, доріжка з ворогами, `+ui:sp-counter`, `+ui:summon-button` з ціною, `+ui:power-up-bar` (5 видів колоди з цінами), `lives` (3 серця), `wave-counter`, таймер хвилі; у PvP згори — `+ui:opponent-boards` (поле й колода суперника).
- `end-screen` — перемога/поразка, трофеї, нагорода.
- `leaderboard` / `rank-tiers` — ліги PvP; `lobby-window` (⏳) — пошук суперника/друга.
- Переходи: main-menu → (Battle) пошук суперника → game-screen → end-screen → main-menu; main-menu → Deck → loadout-select.

## Фічі поза полем
- `meta-progression`: рівні класу кубиків (копії з скринь → апгрейд), загальний % критичної шкоди росте від апгрейдів (`+crit-meta-stat`).
- `mode-versus` (PvP за трофеї), `mode-coop` (нескінченні боси), Solo, Crew Battles, Mirror mode (обидва гравці з однаковими колодами (?)).
- `rank-tiers`, `achievements`, `streaks`/щоденні квести (?), `gacha`, `online-multiplayer`, `invite-link` (гра з другом).
- Rush Royale: герої з активним вмінням, 5 фракцій, 4 рідкості карт.

## Варіації й родичі
- Rush Royale (IT Territory, 2020) — найближчий родич: юніти замість кубиків, мана, герой, смуга з порталу до замку, у PvP — убиті монстри йдуть супернику.
- Just Dice (джерело Random Dice), Merge Defense, Clash Royale (колода й PvP-ліги), auto chess (`star-up-merge` — три копії → зірка).
- **Осі варіацій**: результат злиття — той самий вид +1 (2048) / **випадковий вид +1** (Random Dice) / вища зірка з 3 копій (TFT) · призов — у випадкову клітину / за вибором гравця · PvP — дзеркальні хвилі / вбиті вороги йдуть супернику.

## Цікавинки для курсу
- Злиття з випадковим результатом: та сама пара → `random(deck)` з крапками +1 — 🥉 (2048 + випадковість, тест на інваріанти).
- Призов у випадкову вільну клітину з ціною, що росте на 10 — 🌱.
- Крапки = кількість снарядів, вибір цілі «передній на доріжці» (позиція по довжині шляху) — 🥉.
- Аури сусідства (Light, Moon) на сітці 5×3 — 📎.
- Бос Magician перетворює кубики, Silence вимикає — 📎 (ефект на поле гравця).
- PvP з дзеркальними хвилями або «вбите — супернику» (Rush Royale) — 🥈 (два поля, синхронізація).

## Мапа на каталог
- Є: `tile-merge` ↔ злиття (тут з випадковим видом) · `drag-drop-piece` · `spawn-random-cell` ↔ призов · `round-currency` ↔ SP · `in-round-upgrades` ↔ power-up · `enemy-waves` + `spawn-schedule` · `enemy-reached-base` · `hp-damage` · `projectile-shot` + `shoot-cooldown` · `blast-wave` ↔ Fire · `temporary-modes` ↔ Ice/Silence · `speed-per-type` · `player-death` ↔ 3 життя · `ai-opponent` (Solo) · `leaderboard` · `save-progress` · `shop-between-levels` ↔ скрині/апгрейд класу.
- **Нема** → пропозиції карток:
  - `+tower-range` (спільна) — тут ціль «передній на доріжці».
  - `+cost-escalation` (є, Arknights) — ціна призову +10.
  - `+merge-random-upgrade` «Злиття двох однакових → випадковий тип рівнем вище» · entities/legality · 🥉 (дитина `tile-merge`).
  - `+pips-as-shots` «Рівень = кількість одночасних снарядів» · entities/combat · 🌱.
  - `+loadout-select` (є) — колода з 5 типів перед матчем.
  - `+aura-buff` (є) — Light/Moon.
  - `+boss-fight` (є) — боси з вміннями проти поля гравця.
  - `+garbage-attack` (є, Tetris) — Rush Royale: убиті вороги йдуть супернику.
  - `+mirror-lanes` «Обидва гравці отримують ті самі хвилі» · game-logic/opponent · 🥉.
  - `+deck-of-types` «Колода визначає пул випадкових спавнів» · game-logic/economy · 🌱.
  - `+crit-meta-stat` «Мета-стат з прогресії діє в кожному матчі» · game-logic/economy · 🌱.
  - `+growth-over-time` «Сутність сама підвищує рівень з часом» · entities/state · 🌱.
  - `+copy-neighbor` «Сутність копіює тип іншої» · entities/interact · 📎.

## Пропозиції до словників
- `+trigger:merge` — відбулось злиття (Sacrifice дає SP).
- `+cond:same` — уже 🔥; тут дві властивості разом (вид і крапки).
- `+effect:merge` — уже ⏳; підтвердження з випадковим продуктом; `+effect:spawn_random` — спавн випадкового типу з пулу у випадкову вільну клітину; `+effect:power_up` — підсилення всіх сутностей типу на матч.
- `+role:tower` (підтвердження), `+role:tile` — кубик одночасно вежа і плитка злиття.
- `+ui:summon-button` (з ціною, що росте), `+ui:power-up-bar`, `+ui:opponent-boards` (є 🔥), `+ui:sp-counter`.
- `+window:loadout-select` (вибір колоди), `+window:lobby-window`.
- `+feature:mode-versus`, `+feature:mode-coop`, `+feature:rank-tiers`, `+feature:gacha`.
- `+axis:session=match`.

## Джерела
- ⭐ YouTube: пошук «random dice pvp gameplay» — найшвидше видно злиття, призов і дзеркальні хвилі.
- [App Store: Random Dice: Defense](https://apps.apple.com/us/app/random-dice-pvp-defense/id1462877149) — 111%, колода з 5 кубиків, злиття й рівні, PvP, co-op Boss Raid, Solo, Crew Battles, Mirror mode.
- [ko.wikipedia: 랜덤 다이스](https://ko.wikipedia.org/wiki/랜덤_다이스) — запуск 28.08.2019 як Royal Dice, перейменування 18.12.2019, походження від Just Dice.
- [Wikipedia: Rush Royale](https://en.wikipedia.org/wiki/Rush_Royale) — поле 3×5, мана за вбивства, злиття двох однакових → випадковий юніт з колоди, бос після хвилі, у PvP убиті монстри йдуть супернику.
- [Google Play](https://play.google.com/store/apps/details?id=com.percent.royaldice) — сторінка застосунку (вміст не прочитано).

## Непевне
- (?) Форма доріжки, розмір 5×3 саме в Random Dice (Rush Royale 3×5 підтверджено).
- (?) Стартова ціна призову 10 SP і крок +10; ціни power-up 100/200/400/700; максимум 7 крапок — з памʼяті.
- (?) Список босів і їхні вміння; правила Joker/Mimic.
- (?) Як влаштовано co-op (спільна доріжка?) і Mirror mode.
- (?) Чи великі вороги дають більше SP; SP з часом окрім вбивств.
