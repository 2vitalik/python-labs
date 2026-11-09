---
title: Сучасні mazing-TD (Electromaze, Tower Maze Defense, Thornline TD, Maul Tactics, Back to the Roots 2)
slug: mazing-td-modern
aka: [maze TD, mazing tower defense, maze-building tower defense, Electromaze Defense, Pathless Maze TD]
family: tower-lanes
also: []
klass: cursor
axes:
  field: square
  time: realtime
  opponent: online
  info: full
  random: setup
  goal: survive
year: 2018
platforms: [PC]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/5300580/Thornline_TD_Maze_Tower_Defense/", best: true, note: "Thornline TD: вежі = стіни, не можна закрити шлях, правила світів, броня, PvP до 8 з відправкою юнітів"}
  - {kind: steam, url: "https://store.steampowered.com/app/769410/Electromaze_Tower_Defense/", note: "Electromaze (2018): вейпоінти на сітці, 14 веж × 4 utility-апгрейди, випадкова генерація рівнів"}
  - {kind: steam, url: "https://store.steampowered.com/app/3109150/Tower_Maze_Defense/", note: "Tower Maze Defense (2024): вежі будь-де, 60 хвиль, боси кожні 10, endless з підсиленнями кожні 3 хвилі"}
  - {kind: steam, url: "https://store.steampowered.com/app/4433930/Maul_Tactics/", note: "Maul Tactics (2026): змагальний mazing, гілки апгрейдів, вежа 2×2 tier IV, Wretch +дохід"}
  - {kind: steam, url: "https://store.steampowered.com/app/4741830/Tower_Defence_Back_to_the_roots_2/", note: "Back to the Roots 2 (2026): 1v1 mazing, відправка монстрів → дохід, будівельники"}
  - {kind: other, url: "https://store.steampowered.com/search/?term=maze+tower+defense", note: "Steam-пошук: тисячі TD, mazing — меншість"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=maze+tower+defense+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [tower-placement, tower-range, chase-bfs, reachability-check, enemy-waves, spawn-schedule, spawn-points, enemy-reached-base, player-death, round-currency, in-round-upgrades, shop-buyback, shop-catalog, hp-damage, speed-per-type, status-effects, multi-cell-size, run-relics, difficulty-levels, level-select, level-unlock, online-multiplayer, ai-opponent, leaderboard, character-select, mode-select, +maze-by-towers, +path-recompute, +waypoint-route, +send-units-to-opponent, +income-economy, +world-rule-modifiers, +armor-flat, +tower-branch-upgrade, +reverse-path-boss, +mid-path-entry, +revive-once, +regen-when-unhit, +enrage-on-damage, +gold-thief, +split-on-death, +random-map-generation]
proposes: ["+trigger:path_changed", "+effect:recompute_path", "+effect:sell", "+effect:upgrade", "+effect:income", "+effect:steal", "+cond:not_hit_for", "+role:waypoint", "+feature:world-rules", "+feature:star-upgrades", "+ui:range-circle"]
author: opus
date: 2026-11-09
---

# Сучасні mazing-TD — відкрите поле без дороги: шлях зʼявляється лише з веж, які ти ставиш

## Суть
Сімейний файл для пачки сучасних (2018–2026) інді-TD, що продовжують [desktop-tower-defense](desktop-tower-defense.md) і [fieldrunners](fieldrunners.md): дороги на мапі нема, вороги біжать найкоротшим шляхом від входу до виходу через відкрите поле, а кожна вежа — водночас стіна. Гравець «будує лабіринт»: подовжує маршрут і проводить його повз найсильніші вежі. Головне обмеження спільне для всіх — **повністю закрити шлях не можна**. Різняться ці ігри тим, що додають до ядра: вейпоінти (Electromaze), правила світів і роглайт-реліквії (Thornline), PvP з відправкою юнітів суперникові (Maul Tactics, Back to the Roots 2, Thornline).

## Поле і час
- Квадратна сітка без дороги (тег Steam «Grid-Based Movement» у Electromaze і Back to the Roots 2); вхід(и) і вихід/фортеця — фіксовані точки мапи.
- Вежа займає клітину; у Maul Tactics фірмова вежа tier IV потребує вільного квадрата **2×2**.
- Electromaze: на сітці стоять **вейпоінти** — вороги мусять пройти їх по черзі перед виходом; лабіринт будується між ними.
- Real-time: хвилі за розкладом, будувати можна між і під час хвиль; у PvP-режимах кожен гравець має **свій лабіринт**, суперники бачать чужі поля (?).
- Thornline: та сама мапа рівня на кожній спробі — можна переробити лабіринт після поразки.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Вежа | tower | ціна, шкода, дальність, рівень | атакує автоматично в радіусі; водночас непрохідна стіна для наземних |
| Вежа tier III (Maul) | tower | 1 з 3 спеціалізацій | розгалуження: після tier II обираєш одну гілку |
| Вежа tier IV (Maul) | tower | 2×2, gold + lumber | «вознесіння» фірмової вежі після Escalation |
| Вежі Thornline | tower | Arrow, Cannon, Frost, Poison, Lightning, Catapult, Flamethrower, Sniper | відкриваються по кілька, кожна апгрейдиться двічі |
| Вежі Electromaze | tower | 14 типів | кожна бере 1 з 4 Utility Upgrades |
| Вхід | spawner | 1+ | хвиля виходить тут |
| Вихід / фортеця (keep) | static | життя | ворог дійшов → втрата життя |
| Вейпоінт (Electromaze) | static (`+role:waypoint`) | номер | ворог мусить пройти через нього по черзі |
| Звичайний ворог | enemy | HP, швидкість, броня | іде найкоротшим відкритим шляхом |
| Броньований | enemy | броня (плоска) | броня віднімає фіксоване число з кожного удару — важкі постріли кращі за часті легкі |
| Wrecker (Thornline) | enemy | — | краде золото, поки йде |
| Scarab (Thornline) | enemy | броня | броня ламається з кожним влученням |
| Boar (Thornline) | enemy | — | пришвидшується, коли отримує шкоду |
| Ghoul (Thornline) | enemy | — | лікується, коли його не бʼють |
| Knight (Thornline) | enemy | — | при смерті розпадається на жуків |
| Blink / healer / summoner (Electromaze) | enemy | — | телепортується вперед / лікує / кличе нових |
| Бос | boss | HP | Thornline — кінець кожного рівня з 2-го; Electromaze — підсилює кораблі поруч; TMD — кожні 10 хвиль зі своїм power-up |
| Найманець суперника | enemy | ціна | куплений суперником юніт, що біжить твоїм лабіринтом (PvP) |
| Wretch (Maul) | enemy | 10 gold | відправлений супернику; +2 доходу кожні 15 с до кінця матчу, навіть після смерті |
| Реліквія (Thornline) | pickup | — | вибір кожен 4-й раунд: реліквія на рівень або золото |
| Будівельник / раса | piece | набір веж | Back to the Roots 2 — свої вежі й апгрейди; Maul — 15 рас |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(place, tower, cell)` → ЯКЩО `has(gold, cost)` and `free(cell)` and `path_exists(entrance, exit)` → ТО `place(tower, cell)`, `currency(-cost)`, `custom: «effect recompute_path для всіх наземних»`; інакше `block`.
- КОЛИ `custom: «trigger path_changed»` → ТО кожен ворог `custom: «новий найкоротший шлях від своєї клітини»`.
- КОЛИ `tick` → ТО ворог `move(enemy, next_on_path)`; в Electromaze — `custom: «наступна ціль — найближчий непройдений вейпоінт по черзі»`.
- КОЛИ `in_range(tower, enemy, r)` → ТО `damage(enemy, n)` з періодом перезарядки; Frost — `speed(enemy, ×k)`; Poison — `set_state(enemy, poison, dur)`.
- КОЛИ `contact(shot, enemy)` → ЯКЩО `state(enemy, armored)` → ТО `damage(enemy, n − armor)`.
- КОЛИ `contact(shot, scarab)` → ТО `custom: «броня Scarab −1»`.
- КОЛИ `contact(shot, boar)` → ТО `speed(boar, +n)`.
- КОЛИ `custom: «ghoul не отримував шкоди N тіків»` → ТО `heal(ghoul, n)`.
- КОЛИ `tick` → ЯКЩО `occupied(cell, wrecker)` → ТО `custom: «effect steal: −золото гравця»`.
- КОЛИ `hp_zero(enemy)` → ТО `disappear(enemy)`, `currency(+bounty)`; Knight — `spawn(beetles)`; у світі «graveyard» — `respawn(enemy, here)` ЯКЩО `first_time`.
- КОЛИ `reach(enemy, keep)` → ТО `lives(-n)`, `disappear(enemy)`; КОЛИ `counter(lives, ==, 0)` → ТО `lose`.
- КОЛИ `input(upgrade, tower)` → ЯКЩО `has(gold, price)` → ТО `custom: «effect upgrade»`; у Maul після tier II — `choose(3 спеціалізації)`; tier IV — ЯКЩО `fits(2x2, cell)` and `has(lumber, n)` → ТО `transform(tower, tier4)`.
- КОЛИ `input(sell|delete, tower)` → ТО `custom: «effect sell»`, `disappear(tower)`, `custom: «path_changed»`.
- КОЛИ `input(send, unit)` → ЯКЩО `has(gold, cost)` → ТО `currency(-cost)`, `custom: «effect income: +дохід до кінця матчу»`, `spawn_at(unit, opponent_entrance)`.
- КОЛИ `timer(15s)` → ТО `currency(+income)` (Maul; Wretch дає +2).
- КОЛИ `wave_start` → ЯКЩО `mode(desert)` → ТО `spawn_at(wave, quarter_of_path)` — хвиля входить на чверті шляху, оминаючи початок лабіринту (Thornline).
- КОЛИ `wave_start` → ЯКЩО `mode(snow)` and `custom: «хвиля боса»` → ТО `spawn_at(boss, keep)` — бос іде лабіринтом **назад**.
- КОЛИ `wave_start` → ЯКЩО `mode(swamp)` and `custom: «кожна друга хвиля»` → ТО `custom: «×2 ворогів з ½ HP»`.
- КОЛИ `counter(round, %4, 0)` → ТО `choose(relic | gold)` (Thornline); TMD endless — `counter(wave, %3, 0)` → `choose(power-up)` з пулу за типами веж на полі (не випадково).
- КОЛИ `custom: «endless: кожні 10 раундів»` → ТО `custom: «світ змінюється разом з його правилом»` (Thornline).
- КОЛИ `hp_zero(boss)` → ЯКЩО `counter(wave, ==, last)` → ТО `win`; у PvP — `custom: «останній, хто вижив, перемагає»`.
- Перемога: пережити всі хвилі рівня / останнім вижити в PvP · Поразка: життя фортеці = 0 · Рахунок: найкращий раунд endless — у світовій таблиці (Thornline), зірки за рівень.

## Керування і ввід
- Миша: вибір вежі з панелі → «привид» на клітині → клік ставить; клік по вежі — апгрейд / продаж (видалення).
- Maul: вибір гілки tier III при апгрейді; фірмова вежа — на вільний квадрат 2×2.
- PvP: окрема панель відправки юнітів супернику (купівля = атака + дохід).
- TMD: «mega attack» — разова сильна дія гравця (?), на Hard без неї можна пройти.

## Вікна, меню, HUD
- `main-menu` → `mode-select`: Solo / Skirmish / Online PvP / Endless (Thornline); Story / Endless (TMD); Story Campaign / Gauntlet / Skirmish / Wave Survivor / Online (Maul).
- `difficulty-select`: Easy / Medium / Hard (TMD).
- `character-select`: будівельник (Back to the Roots 2) / раса (Maul).
- `level-select` / `map-window`: 10 світів × 5 рівнів (Thornline), сотні мап (BttR2), випадкова мапа (Electromaze).
- `lobby-window`: PvP-лобі, порожні місця — боти.
- `game-screen`: поле, панель веж з цінами, `coins`, `lives`, `wave-counter`, `next-wave-preview` (?), у PvP — `+ui:income-panel`, `+ui:send-panel`, `opponent-boards` (?).
- `upgrade-window`: вибір реліквії/золота кожен 4-й раунд (Thornline), power-up кожні 3 хвилі (TMD endless).
- `tutorial-window` + челенджі (Electromaze) · `leaderboard` (Thornline endless) · `achievements-window`.

## Фічі поза полем
- `mode-endless` (усі); `mode-versus` / `online-multiplayer` до 8 гравців (Thornline), 1v1 і FFA 2–4 (Maul), 1v1 (BttR2); `ai-opponent-levels` — skirmish проти 7 ботів (Thornline).
- `meta-progression`: зірки відкривають постійні апгрейди (Thornline); після 50 рівнів світи повторюються складніше.
- `+feature:world-rules`: у кожного світу своє правило, що ламає звичну геометрію лабіринту.
- Генерація: нескінченні випадкові мапи й рівні (Electromaze).
- `level-editor` — тег Steam у BttR2 (?).
- `leaderboard-online`, achievements, cloud-save (Thornline).

## Варіації й родичі
- Корені: maze-TD мапи Warcraft III/StarCraft → [desktop-tower-defense](desktop-tower-defense.md), [flash-element-td](flash-element-td.md), [fieldrunners](fieldrunners.md), [element-td-2](element-td-2.md) (режим Mazing); PvP з відправкою — [legion-td](legion-td.md); блоки замість веж — [emberward](emberward.md); шлях-плитки — [rogue-tower](rogue-tower.md), [isle-of-arrows](isle-of-arrows.md).
- **Осі варіацій**:
  - маршрут: вхід → вихід / через вейпоінти по черзі / з середини шляху (desert) / задом наперед (snow-бос);
  - стіна: вежа = стіна / окремі блоки / вежі-фігури 2×2;
  - суперник: AI-хвилі / PvP, де хвилі — це покупки суперника, що водночас дають дохід;
  - прогресія: фіксовані рівні / випадкові мапи / роглайт-реліквії й зірки;
  - апгрейди: лінійні / одна з N «utility» / дерево з розгалуженням.

## Цікавинки для курсу
- Заборона закрити шлях + перерахунок маршруту кожного ворога з його клітини — 🥇 (BFS перед кожною посадкою й після продажу).
- Вейпоінти: шлях як конкатенація BFS між послідовними точками — 🥈.
- Правила світів (вхід на чверті шляху, бос задом наперед, ×2 ворогів з ½ HP, одноразове воскресіння) — 📎 кожне; набір модифікаторів як конфіг — 🥉.
- Плоска броня проти частих/важких пострілів + Scarab, що «облазить» — 📎.
- Ghoul (реген без шкоди), Boar (прискорення від шкоди) — 🌱/📎: стан з таймером «від останнього удару».
- PvP-економіка «відправ ворога — отримай дохід назавжди» — 🥈 (два поля, синхронізація, баланс).

## Мапа на каталог
- Є: `tower-placement` + `tower-range` · `chase-bfs` + `reachability-check` ↔ шлях і заборона перекриття · `enemy-waves` + `spawn-schedule` + `spawn-points` · `enemy-reached-base` + `player-death` · `round-currency` · `in-round-upgrades` · `shop-buyback` ↔ продаж · `shop-catalog` ↔ панель веж · `hp-damage` · `speed-per-type` · `status-effects` ↔ отрута/сповільнення · `multi-cell-size` ↔ tier IV 2×2 · `run-relics` ↔ реліквії · `difficulty-levels` · `level-select` + `level-unlock` · `online-multiplayer` · `ai-opponent` ↔ боти · `leaderboard` · `character-select` ↔ будівельники/раси · `mode-select`.
- **Нема** → пропозиції карток:
  - `+maze-by-towers`, `+path-recompute`, `+send-units-to-opponent`, `+income-economy`, `+waypoint-route`, `+split-on-death` — уже пропоновані сімʼєю (DTD, Fieldrunners, Legion TD, Element TD 2).
  - `+world-rule-modifiers` «Правило світу» · game-logic/waves · 🥉 · слоти {entry_offset, reverse_boss, wave_mult, revive_once}.
  - `+armor-flat` «Плоска броня» · entities/combat · 📎 · слот {armor}.
  - `+tower-branch-upgrade` «Гілка апгрейда на рівні N» · game-logic/economy · 📎 · слот {tier, options}.
  - `+reverse-path-boss` / `+mid-path-entry` «Нестандартна точка входу хвилі» · entities/spawn · 🌱.
  - `+revive-once`, `+regen-when-unhit`, `+enrage-on-damage`, `+gold-thief` — малі поведінки ворогів · entities/state · 🌱–📎.
  - `+random-map-generation` «Випадкова TD-мапа з входом/виходом/вейпоінтами» · levels/generation · 🥈.

## Пропозиції до словників
- `+trigger:path_changed`, `+effect:recompute_path`, `+effect:sell`, `+effect:upgrade`, `+effect:income` — підтвердження з родичів (DTD, Fieldrunners, Legion TD).
- `+effect:steal` — ворог забирає ресурс гравця на ходу (Wrecker).
- `+cond:not_hit_for(a, n)` — сутність не отримувала шкоди N тіків (Ghoul).
- `+role:waypoint` — обовʼязкова точка маршруту ворога (Electromaze; як у Element TD 2).
- `+feature:world-rules` — світ/розділ міняє одне правило гри для всіх рівнів.
- `+feature:star-upgrades` — зірки за рівні купують постійні апгрейди (Thornline).
- `+ui:range-circle` — підтвердження.

## Джерела
- ⭐ [Steam: Thornline TD](https://store.steampowered.com/app/5300580/Thornline_TD_Maze_Tower_Defense/) — вежі як стіни, заборона закрити шлях, правила 5 світів, вороги з поведінками, броня, режими Solo/Skirmish/Endless/PvP до 8, реліквії, зірки.
- [Steam: Electromaze Tower Defense](https://store.steampowered.com/app/769410/Electromaze_Tower_Defense/) — вейпоінти, 14 веж, 4 utility-апгрейди, blink/heal/summon, боси-підсилювачі, випадкові рівні.
- [Steam: Tower Maze Defense](https://store.steampowered.com/app/3109150/Tower_Maze_Defense/) — вежі будь-де, 60 хвиль, боси кожні 10, складності, endless з вибором power-up кожні 3 хвилі.
- [Steam: Maul Tactics](https://store.steampowered.com/app/4433930/Maul_Tactics/) — змагальний mazing, tier I–IV, 2×2, lumber, Wretch +2/15 с, 15 рас, режими.
- [Steam: Tower Defence: Back to the Roots 2](https://store.steampowered.com/app/4741830/Tower_Defence_Back_to_the_roots_2/) — 1v1 maze-building, відправка монстрів → дохід, будівельники, сотні мап.
- [Steam-пошук «maze tower defense»](https://store.steampowered.com/search/?term=maze+tower+defense) — огляд пачки.

## Непевне
- (?) «Pathless Maze TD» з черги в Steam-пошуку не знайдено — найімовірніше, описова назва групи, не гра.
- (?) Чи вежі Electromaze теж є стінами, чи лабіринт будується окремими блоками; чи можна закрити шлях.
- (?) Розміри сіток, кількість життів фортеці, частка повернення при продажі — ніде не вказано.
- (?) Чи видно в PvP поле суперника; як саме між гравцями ділиться час хвиль.
- (?) Що таке «mega attack» у Tower Maze Defense і «Escalation» у Maul Tactics — в описах лише згадки.
- (?) Режими Back to the Roots 2 («different game modes») і чи є там редактор (лише тег Level Editor).
- (?) Thornline TD ще не вийшов (демо) — опис за сторінкою магазину.
