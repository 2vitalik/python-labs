---
title: Thronefall
slug: thronefall
aka: []
family: tower-lanes
also: [build-sim]
klass: hybrid
axes:
  field: free
  time: realtime
  opponent: ai
  info: partial
  random: none
  goal: survive
year: 2023
platforms: [PC, Mac, Switch, iOS]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Thronefall", best: true, note: "день/ніч, гравець сам кличе ніч, будівлі лише на заданих місцях, золото з домів і полів, відновлення після ночі, бій монарха луком і списом"}
  - {kind: steam, url: "https://store.steampowered.com/app/2239150/", note: "10 мап, 9 зброї, 50+ перків (до 5), мутатори, перелік будівель, юнітів і ворогів, поразка — знищено Castle Center"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=thronefall+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 55
mechanics: [tower-placement, tower-range, round-currency, enemy-waves, spawn-points, last-line-defense, enemy-reached-base, hp-damage, melee-vs-ranged, chase-greedy, respawn, level-select, level-unlock, difficulty-levels, rule-variants, run-relics, leaderboard, game-screen, end-screen, +day-night-cycle, +fixed-build-slots, +economy-buildings-income, +survival-income, +restore-after-wave, +player-calls-wave, +hero-in-td, +building-upgrade-branch, +mutators-score-multiplier]
proposes: ["+trigger:phase_start", "+effect:place", "+window:perk-select", "+ui:build-slot-cost", "+feature:mutators", "+card:fixed-build-slots", "+card:restore-after-wave"]
author: opus
date: 2026-11-09
---

# Thronefall — удень будуєш на фіксованих місцях за золото, вночі король на коні сам бʼється разом з вежами й загонами

## Суть
Мінімалістична стратегія з TD-ядром (Grizzly Games): гравець — монарх, що їздить мапою. Удень він витрачає золото на будівлі в заздалегідь заданих місцях: економіку (доми, поля, шахти, гавані), оборону (стіни, вежі, барикади, святилища) і військові (казарми, стрільбища). Коли готовий — сам кличе ніч: з країв ідуть хвилі ворогів, а король бʼється на передовій поруч зі своїми вежами й загонами. Вижив — уранці зруйноване відновлюється, а вцілілі економічні будівлі дають золото; Castle Center зруйновано — поразка.

## Поле і час
- Поле — вільна 3D-мапа (не сітка) з фіксованими «слотами» під будівлі; доріжки, річки, мости (міст — теж будівля).
- Цикл: день (без ворогів, будування, без ліку часу (?)) → ніч (хвилі в реальному часі) → ранок (відновлення й дохід).
- Кількість ночей на мапі обмежена; пройдена мапа — перемога (?).
- Видимість: напрямки атаки наступної ночі позначені (?) — `info: partial`.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Король (Warrior King) | player | HP, зброя (лук / спис / ще 7) | їздить, бʼється; здібність зброї; гине — відроджується (?) |
| Castle Center | static | HP | ядро; знищено — поразка; апгрейди |
| Слот будівлі | zone | ціна, тип | місце, де можна поставити лише свій тип будівлі |
| Дім, поле, млин, шахта, гавань | resource | дохід | дають золото щоранку, якщо вціліли |
| Міст | static | — | відкриває шлях (?) |
| Стіна, барикада | static | HP | блокує ворогів |
| Вежа | tower | дальність, урон | стріляє в ворогів у радіусі |
| Святилище (shrine) | tower | ефект | особлива оборонна будівля (?) |
| Казарма / стрільбище / Hero's Quarters | spawner | тип загону | дає Knights, Berserks, Crossbowmen, Fire Archers; героїв Golem, Mage |
| Загін | ally | HP, урон | стоїть на позиції, бʼється з ворогами поруч |
| Blacksmith, Royal Forge | static | — | апгрейди загонів/зброї (?) |
| Вороги | enemy | тип | Barrel Knights, Flying Mages, Ogres, Slimes, Wasps, Catapults… — ідуть до Castle Center, ламають будівлі |
| Точка появи | spawner | край мапи | звідки йде хвиля |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(build at slot)` → ЯКЩО `has(player, gold)` → ТО `take(player, gold)`, `place(building, slot)`.
- КОЛИ `input(upgrade building)` → ЯКЩО `has(player, gold)` → ТО `choose(upgrade options)` (?).
- КОЛИ `input(start night)` → ТО `phase_start(night)`, `spawn_at(wave, spawn points)`.
- КОЛИ `in_range(tower, enemy, r)` → ТО `damage(n)`.
- КОЛИ `contact(enemy, building)` → ТО `damage(n)`; КОЛИ `hp_zero(building)` → ТО `set_state(building, ruined)`.
- КОЛИ `hp_zero(Castle Center)` → ТО `lose`.
- КОЛИ `hp_zero(king)` → ТО `custom: «король вибуває до відродження»` (?).
- КОЛИ `wave_cleared` → ТО `custom: «відновити зруйновані будівлі й загони»`, `phase_start(day)`.
- КОЛИ `wave_cleared` → ТО `currency(+income)` `custom: «за кожну вцілілу економічну будівлю»`.
- КОЛИ `custom: «остання ніч мапи пережита»` → ТО `win`, `window(end-screen)` (?).
- КОЛИ `level_start` → ЯКЩО `custom: «увімкнено мутатори»` → ТО `custom: «вороги сильніші, множник рахунку»` (?).
- Перемога: пережити всі ночі мапи · Поразка: знищено Castle Center · Рахунок: очки мапи для лідерборду (?).

## Керування і ввід
- Рух короля (клавіатура/стік); будування — під'їхати до слота й утримувати кнопку (?).
- Атака — автоматична поруч або за кнопкою (?); здібність зброї — окрема кнопка.
- Підтримка геймпада; «мінімалістична» — кілька кнопок.

## Вікна, меню, HUD
- `level-select` / `world-map`: 10 мап з різним рельєфом, погодою, ворогами (?).
- `perk-select` (custom): перед мапою — зброя і до 5 перків, мутатори (?).
- `game-screen`: мапа, золото, `build-slot-cost` (custom-ui: ціна над слотом), HP короля й ядра, кнопка «почати ніч» (?).
- `end-screen`: перемога/поразка, рахунок, розблоковане.
- `settings-window`, 14 мов.

## Фічі поза полем
- `meta-progression`: розблокування зброї (9) і перків (50+) (?).
- `mutators` — опційні ускладнення; `leaderboard-online` (Steam), `achievements`, `cloud-save`.
- Ранній доступ серпень 2023, реліз 11.10.2024 (Windows, Switch), iOS — червень 2025.

## Варіації й родичі
- Kingdom: Two Crowns (сторонньо-ковзна економіка вдень, оборона вночі) (?); [they-are-billions](they-are-billions.md) (база й хвилі), [orcs-must-die](orcs-must-die.md) (герой у TD), [isle-of-arrows](isle-of-arrows.md).
- **Осі варіацій:** місця будівель (вільні / слоти) · хто кличе хвилю (таймер / гравець) · економіка (пасивний дохід / дохід лише вцілілих) · герой (нема / бʼється сам).

## Цікавинки для курсу
- Цикл день/ніч як машина станів фаз — 🌱.
- Фіксовані слоти з типом і ціною (замість вільної сітки) — 🌱.
- Дохід лише від вцілілих будівель + відновлення після ночі — 📎.
- Король як аватар у TD + загони, що тримають позицію — 🥉.
- Мутатори як модифікатори правил з множником рахунку — 📎.

## Мапа на каталог
- Є: `tower-placement` · `tower-range` · `round-currency` · `enemy-waves` · `spawn-points` · `last-line-defense` / `enemy-reached-base` (Castle Center) · `hp-damage` · `melee-vs-ranged` · `chase-greedy` (вороги) · `respawn` · `level-select` · `level-unlock` · `difficulty-levels` / `rule-variants` (мутатори) · `run-relics` (перки) · `leaderboard` · `game-screen` · `end-screen`.
- **Нема** → пропозиції карток:
  - `+day-night-cycle` (Knight Lore) — підтвердження.
  - `+fixed-build-slots` «Будівлі лише на заданих місцях свого типу» · levels · 🌱.
  - `+economy-buildings-income` · 🌱; `+survival-income` «Дохід лише від вцілілих» · 📎; `+restore-after-wave` · 📎.
  - `+player-calls-wave` «Гравець сам запускає наступну хвилю» · game-logic · 🌱; `+hero-in-td` · 🥉; `+building-upgrade-branch` · 📎; `+mutators-score-multiplier` · 📎.

## Пропозиції до словників
- `+trigger:phase_start`, `+effect:place` — уже в 🔥, тут вжито.
- `+window:perk-select`, `+ui:build-slot-cost`, `+feature:mutators`.
- `+card:fixed-build-slots`, `+card:restore-after-wave`.

## Джерела
- ⭐ [Wikipedia: Thronefall](https://en.wikipedia.org/wiki/Thronefall) — день/ніч, будівлі на заданих місцях, золото, юніти з казарм, лук і спис, відновлення після ночі, розробка, дати.
- [Steam: Thronefall](https://store.steampowered.com/app/2239150/) — 10 мап, 9 зброї, 50+ перків (до 5), мутатори, перелік будівель/юнітів/ворогів, поразка, лідерборди.
- YouTube: пошук «thronefall gameplay».

## Непевне
- (?) Кількість ночей на мапі, умова перемоги мапи, система рахунку й множник мутаторів — з памʼяті.
- (?) Будування утриманням кнопки біля слота, вибір апгрейда, смерть і відродження короля — з памʼяті.
- (?) Показ напрямків атаки, роль святилищ і мостів.
