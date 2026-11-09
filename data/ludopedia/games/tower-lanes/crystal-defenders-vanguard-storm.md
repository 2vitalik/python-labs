---
title: "Crystal Defenders: Vanguard Storm"
slug: crystal-defenders-vanguard-storm
aka: [Vanguard Storm, クリスタルディフェンダーズ ヴァンガードストーム, Crystal Defenders VS]
family: tower-lanes
also: [tactics]
klass: figure
axes:
  field: square
  time: turn
  opponent: ai
  info: full
  random: none
  goal: survive
year: 2009
platforms: [iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Crystal_Defenders", best: true, note: "розділ Vanguard Storm: 4×8, війська лише справа, ворог на клітинку за хід, підкріплення, рівень = номер хвилі; плюс база серії"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/クリスタルディフェンダーズ", note: "JA: два поля 4×4 поруч, юніт з 0 HP падає й встає після хвилі; механіки W-серії (кристали, призови, польові кристали)"}
  - {kind: other, url: "https://www.pocketgamer.com/crystal-defenders-vanguard-storm/review/", note: "огляд Pocket Gamer: кілька секунд на перестановку, ворог бʼє клітину праворуч, 8 класів, лікування"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Crystal+Defenders+Vanguard+Storm+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [enemy-waves, enemy-reached-base, hp-damage, melee-vs-ranged, tower-range, drag-drop-piece, move-timer, world-map, sequential-levels, +lane-grid, +half-field-placement, +reposition-each-turn, +reinforcement-pick, +wave-level-up, +revive-after-wave, +loadout-select, +blocker-unit, +heal-ally, +flying-enemy-type, +physical-resist, +class-unlock-draft]
proposes: ["+role:unit", "+trigger:turn_timer_end", "+cond:in_zone", "+effect:level_up", "+window:loadout-select", "+window:choice-window", "+ui:phase-timer", "+axis:time=timed-turn"]
author: opus
date: 2026-11-09
---

# Crystal Defenders: Vanguard Storm — оборона рядками 4×8 по ходах: ворог крокує на клітинку, ти за кілька секунд переставляєш загін

## Суть
Покрокове відгалуження TD-серії Square Enix на сюжеті Final Fantasy Tactics A2. Поле 4 рядки × 8 стовпців: вороги входять зліва й щоходу роблять крок праворуч, а загін гравця стоїть лише на правій половині 4×4. Між кроками є кілька секунд, щоб перетягнути юнітів: підставити Black Mage під стійкого до фізики, Archer — під летючого, пораненого — під цілителя. Варто уваги як гібрид PvZ-рядків і тактики: «вежі» тут рухомі фігури зі своїми формами атаки, а пропустити не можна жодного ворога.

## Поле і час
- Сітка 4×8 = два поля 4×4 поруч: ліве — коридор ворогів, праве — зона розстановки; рядки працюють як смуги PvZ.
- Хід: фаза перестановки з таймером «кілька секунд» → кінець ходу → юніти атакують, вороги роблять крок на одну клітину праворуч.
- Стадія = серія хвиль; між хвилями — підсилення й вибір підкріплення.
- Вигляд згори, усе поле видно; сюжет і карта світу — як у Wii-версії Crystal Defenders.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Юніт загону | ally (`+role:unit`) | клас, HP, атака, рівень = номер хвилі | стоїть у правій 4×4; наприкінці ходу атакує ворогів у своїй формі дії |
| Soldier | ally | фізична атака | бʼє впритул (?) |
| Archer | ally | дальня атака | дістає летючих |
| Dragoon | ally | — | атакує кілька клітин по лінії (?) |
| Black Mage | ally | магічна атака | шкодить стійким до фізики |
| White Mage / Bishop | ally | лікування | відновлює HP союзникам у радіусі |
| Paladin | ally | високий HP | блокує ворогів |
| Flintlock | ally | дальня атака | стріляє по лінії (?) |
| Наземний ворог | enemy | HP, атака | крок праворуч за хід; бʼє юніта в клітині праворуч від себе |
| Стійкий до фізики | enemy | — | фізична шкода не діє або слабка |
| Летючий | enemy | — | досяжний лише для частини класів (Archer) |
| Права межа поля | static | — | ворог дійшов → поразка |
| Підкріплення | ally | 1 з 2 кандидатів | додається до загону після певних хвиль |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `level_start` → ТО `choose(склад загону)`, `place(unit, right_half)`.
- КОЛИ `turn_start(player)` → ТО `timer(start, few_seconds)`.
- КОЛИ `input(drag, unit, cell)` → ЯКЩО `custom: «cond in_zone: клітина в правій 4×4»` and `free(cell)` → ТО `move(unit, cell)`; ЯКЩО `occupied(cell, unit2)` → ТО `swap(unit, unit2)`; поза зоною — `block`.
- КОЛИ `custom: «trigger turn_timer_end: таймер перестановки вичерпано»` → ТО `end_turn`.
- КОЛИ `turn_end(player)` → ЯКЩО `in_range(unit, enemy, shape)` → ТО `damage(enemy, atk)` — форма дії за класом (клітина / лінія / група).
- КОЛИ `turn_end(player)` → ЯКЩО `state(enemy, flying)` and `not custom: «клас дістає летючих»` → ТО `block` (атака не влучає).
- КОЛИ `turn_end(player)` → ЯКЩО `state(enemy, phys_resist)` and `custom: «атака фізична»` → ТО `custom: «шкода не проходить (?)»`.
- КОЛИ `turn_end(player)` → ЯКЩО `in_range(healer, ally, r)` → ТО `heal(ally, n)`.
- КОЛИ `turn_end(player)` → ЯКЩО `free(cell_right_of_enemy)` → ТО `move(enemy, right)`.
- КОЛИ `turn_end(player)` → ЯКЩО `occupied(cell_right_of_enemy, unit)` → ТО `damage(unit, enemy_atk)`; ЯКЩО `state(unit, paladin)` → ТО `block` (ворог стоїть).
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`.
- КОЛИ `hp_zero(unit)` → ТО `set_state(unit, fallen)` — не атакує до кінця хвилі.
- КОЛИ `wave_cleared` → ТО `clear_state(unit, fallen)`, `custom: «effect level_up: усі юніти +рівень, +HP і атака»`.
- КОЛИ `wave_cleared` → ЯКЩО `custom: «хвиля з підкріпленням»` → ТО `choose(1 з 2 юнітів)`, `place(unit)`.
- КОЛИ `wave_cleared` → ЯКЩО `custom: «кожні кілька хвиль»` → ТО `choose(новий клас з набору)`.
- КОЛИ `reach(enemy, right_edge)` → ТО `lose`.
- КОЛИ `wave_cleared` → ЯКЩО `counter(wave, ==, last)` → ТО `win`, `next_level`.
- Перемога: пережити всі хвилі стадії · Поразка: будь-який ворог дійшов до правого краю · Рахунок: — (?).

## Керування і ввід
- Тач: перетягнути юніта пальцем на іншу клітину правої 4×4 (обмін місцями, якщо зайнято); юніти не виходять за межі зони.
- Лише в короткому вікні між кроками ворогів; атаки й кроки — автоматично.
- Вибір загону на старті стадії, вибір підкріплення й нового класу між хвилями — тапом по варіанту.

## Вікна, меню, HUD
- `map-window`: карта світу зі стадіями (як у Wii-версії).
- `+window:loadout-select`: склад загону перед стадією.
- `game-screen`: поле 4×8, HP юнітів, `wave-counter`, `+ui:phase-timer` (?).
- `+window:choice-window`: «1 з 2 підкріплень» / новий клас між хвилями.
- `end-screen`: стадію пройдено / поразка.
- `dialogue-window`: сюжетні сцени між стадіями (?).

## Фічі поза полем
- `levels-sequential` стадій на `world-map` з сюжетом FFT A2.
- Прогресія всередині стадії: рівень юнітів = номер хвилі, підкріплення, нові класи — без мета-прогресії між стадіями (?).
- Гра знята з App Store у серпні 2017.

## Варіації й родичі
- База серії — Crystal Defenders W1/W2/W3 (моб. 2008, iOS, Xbox 360, WiiWare R1/R2, PS3, PSP, Android): real-time TD на звивистій дорозі, 31 хвиля, 20 вкрадених кристалів = поразка, найм і апгрейд за gil, Thief дає ×gil за вбивство поруч.
  - Призов Esper коштує кристали (5, Chocobo — 2), один за хвилю, бʼє весь екран.
  - З W2 — польові кристали: Red +50 % атаки, Blue +50 % дальності, Yellow +50 % швидкості атаки сусідам, стек до +400 %.
- Vanguard Storm міняє дорогу на рядки, real-time на ходи з таймером, gil на рівень = номер хвилі.
- Родичі: [plants-vs-zombies](plants-vs-zombies.md) (рядки, ворог іде до краю), [mega-man-battle-network](mega-man-battle-network.md) (дві половини поля), [arknights](arknights.md) (блокування ворогів юнітом), [the-battle-cats](the-battle-cats.md).
- **Осі варіацій**: час — real-time / хід з таймером перестановки · загін — нерухомі вежі / фігури, які щоходу переставляєш · рівень — за гроші / автоматично за хвилю · поле — дорога / рядки 4×N з зоною розстановки.

## Цікавинки для курсу
- Хід з таймером перестановки: real-time вікно планування + детерміноване виконання — 🥉.
- Зона розстановки = права половина, перестановка drag-ом з обміном — 📎.
- Порядок фази виконання (атаки юнітів → крок ворогів → удар у клітину праворуч) — 📎; гарне завдання на явні фази тіку.
- Форми атаки класів (клітина / лінія / група) + летючі й стійкі до фізики вороги — 🥉 (матриця «клас × тип ворога»).
- «Падіння» юніта до кінця хвилі й автопідйом — 🌱.
- Вибір 1 з 2 підкріплень між хвилями — 🌱.

## Мапа на каталог
- Є: `enemy-waves` · `enemy-reached-base` ↔ правий край · `hp-damage` · `melee-vs-ranged` ↔ класи · `tower-range` ↔ форма дії класу (слот shape) · `drag-drop-piece` ↔ перестановка · `move-timer` ↔ таймер фази перестановки · `world-map` · `sequential-levels`.
- **Нема** → пропозиції карток:
  - `+lane-grid` — уже пропонувалась (PvZ, Clash Royale).
  - `+half-field-placement` «Зона розстановки — частина поля» · entities/legality · 🌱 · слот {zone}.
  - `+reposition-each-turn` «Перестановка своїх фігур щоходу з таймером» · interface/input · 📎 · слот {seconds}.
  - `+reinforcement-pick` «Вибір 1 з N нових юнітів між хвилями» · game-logic/waves · 🌱 · слот {n}.
  - `+wave-level-up` «Рівень загону = номер хвилі» · entities/state · 🌱.
  - `+revive-after-wave` «Полеглий юніт встає після хвилі» · entities/death · 🌱.
  - `+blocker-unit` «Юніт зупиняє ворога» · entities/combat · 📎.
  - `+heal-ally` «Лікування союзників у радіусі» · entities/combat · 🌱.
  - `+flying-enemy-type` / `+physical-resist` «Тип ворога обмежує, хто може його бити» · entities/combat · 📎.
  - `+class-unlock-draft` «Новий клас у пул кожні N хвиль» · game-logic/waves · 🌱.
  - `+loadout-select` — уже пропонувалась (PvZ, Random Dice).

## Пропозиції до словників
- `+role:unit` — рухомий юніт загону гравця (підтвердження Legion TD).
- `+trigger:turn_timer_end` — вичерпано час фази гравця (хід з таймером).
- `+cond:in_zone` — клітина в зоні розстановки (підтвердження Clash Royale).
- `+effect:level_up` — підняти рівень сутності (усі статистики разом).
- `+window:loadout-select`, `+window:choice-window` — підтвердження.
- `+ui:phase-timer` — таймер фази перестановки.
- `+axis:time=timed-turn` — хід, але з real-time вікном на планування.

## Джерела
- ⭐ [Wikipedia: Crystal Defenders](https://en.wikipedia.org/wiki/Crystal_Defenders) — розділ Vanguard Storm (4×8, права половина, крок за хід, правий край = поразка, підкріплення 1 з 2, рівень = хвиля, наземні / стійкі / летючі, Paladin, White Mage) і база серії.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/クリスタルディフェンダーズ) — два поля 4×4, падіння й підйом юнітів, кристали, призови, польові кристали W2.
- [Pocket Gamer: огляд](https://www.pocketgamer.com/crystal-defenders-vanguard-storm/review/) — кілька секунд на перестановку, свайп по сітці, ворог бʼє клітину праворуч, 8 класів, Bishop лікує.
- YouTube: [пошук «Crystal Defenders Vanguard Storm gameplay»](https://www.youtube.com/results?search_query=Crystal+Defenders+Vanguard+Storm+gameplay).

## Непевне
- (?) Форми атак кожного класу (Soldier впритул, Dragoon/Flintlock по лінії) — джерела кажуть лише «деякі бʼють кілька клітин у лінії або групі».
- (?) Рівень: Wikipedia — «рівень завжди = номер хвилі», Pocket Gamer — «досвід посилює ветеранів»; можливо, це одне й те саме.
- (?) JA-Вікі називає гру «real-time стратегією в дусі PvZ», EN і Pocket Gamer — покрокова з таймером; записано як хід.
- (?) Стійкі до фізики — нуль шкоди чи зменшена; кількість хвиль і стадій; чи є рахунок і випадковість у підкріпленнях.
- (?) Чи є HUD-таймер фази і сюжетні діалоги — не бачив.
