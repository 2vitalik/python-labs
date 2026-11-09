---
title: Toodee and Topdee
slug: toodee-and-topdee
aka: []
family: thinky
also: [grid-platformer, push-slide]
klass: hybrid
axes:
  field: square
  time: realtime
  opponent: none
  info: full
  random: none
  goal: state
year: 2021
platforms: [PC, Switch]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1303950/Toodee_and_Topdee/", best: true, note: "суть: гібрид 2D-платформера і top-down пазла, перемикання персонажів міняє правила жанру; кооп, боси, складність змінює правила"}
  - {kind: other, url: "https://www.geekyhobbies.com/toodee-and-topdee-playstation-5-indie-video-game-review/", note: "рецензія PS5: перемикання заморожує одного, Topdee без гравітації носить ящики, обидва — до порталу, сонечка-колекційки 4 видів"}
  - {kind: official, url: "https://www.nintendo.com/us/store/products/toodee-and-topdee-switch/", note: "Switch-версія 14.04.2022, локальний кооп"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=Toodee+and+Topdee+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 50
mechanics: [party-switch, move-by-input, gravity-fall, move-4dir, keyboard-controls, push-object, key-and-door, touch-death, environment-death, reach-exit, restart-level, sequential-levels, level-unlock, world-map, difficulty-levels, time-bonus, mode-indicator, +perspective-switch, +freeze-inactive, +lift-and-carry, +all-must-exit, +mimic-entity, +optional-challenges, +assist-rule-changes, +local-coop]
proposes: ["+effect:toggle_perspective", "+axis:gravity-per-mode", "+card:perspective-switch", "+card:freeze-inactive", "+card:mimic-entity", "+feature:optional-challenges", "+ui:switch-counter"]
author: opus
date: 2026-11-09
---

# Toodee and Topdee — одна кімната, два жанри: платформер збоку і пазл згори, перемикаєшся кнопкою

## Суть
Кожен рівень — одна клітинна кімната, у якій живуть два персонажі: **Toodee** — героїня 2D-платформера (ходить, стрибає, падає під гравітацією) і **Topdee** — герой top-down пазла (ходить у 4 напрямки без гравітації, піднімає й переносить ящики). Активний лише один; кнопка перемикання заморожує поточного і «оживляє» іншого, і разом із цим кімната починає діяти за правилами іншого жанру. Мета — довести **обох** до порталу-виходу. Ядро — та сама розстановка клітин як два різні пазли: ящик, покладений згори, стає платформою збоку.

## Поле і час
- Квадратна сітка кімнати на один екран (?); у платформерному режимі вона — вид збоку з гравітацією вниз, у top-down — вид згори без гравітації («Topdee ходить по фону»).
- Real-time: рух, стрибки, вороги йдуть у реальному часі; час неактивного персонажа заморожено.
- Шари: тверді блоки (у Toodee-режимі — платформи, у Topdee-режимі — стіни (?)), ящики, шипи/небезпеки, ключі, портал.

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Toodee | player | активна / заморожена | ліво-право, стрибок, падає; збирає ключі; гине від небезпек |
| Topdee | player | активний / заморожений | рух у 4 напрямки без гравітації; піднімає й кладе/штовхає ящики |
| Ящик | object | — | Topdee піднімає, переносить, ставить; у Toodee-режимі — платформа, на яку стрибають |
| Твердий блок | static | — | стіна / підлога; не рухається |
| Ключ | pickup | — | Toodee підбирає; відкриває замкнений прохід для Topdee (за рецензією) |
| Замок / двері | gate | закрито / відкрито | відкриваються ключем (?) |
| Небезпека (шипи тощо) | hazard | — | дотик = смерть, рестарт кімнати (?) |
| Ворог | enemy | рух у реальному часі | дотик = смерть; сонечко-челендж — пройти, нікого не вбивши (значить, ворогів можна вбити (?)) |
| Портал-вихід | static | — | рівень пройдено, коли в ньому обидва |
| Пізні портали (телепорт) | static | парні (?) | переносять персонажа (?) |
| Двійник-мімік | neutral | — | повторює рухи гравця (згадано в рецензії; деталі (?)) |
| Бос | boss | фази | наприкінці кожного набору рівнів, перевіряє вивчені механіки |
| Сонечко | pickup | 4 види, один секретний | нагорода за челендж рівня, відкриває бонус-рівні |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(switch)` → ТО `custom: «активний персонаж заморожується, інший оживає, кімната переходить у правила його жанру»` (`set_state(a, frozen)` / `clear_state(b, frozen)`).
- КОЛИ `tick` → ЯКЩО `state(toodee, active)` і `not supported(toodee)` → ТО `fall(toodee)`.
- КОЛИ `input(jump)` → ЯКЩО `state(toodee, active)` і `supported(toodee)` → ТО `custom: «стрибок»`.
- КОЛИ `input(dir)` → ЯКЩО `state(topdee, active)` і `free(next_cell)` → ТО `move(topdee, dir)` (без гравітації, 4 напрямки).
- КОЛИ `input(grab)` → ЯКЩО `state(topdee, active)` і `adjacent(topdee, box)` → ТО `carry(box)`; повторно — `place(box, cell_ahead)` (?) механіка кидка/ставлення — з памʼяті.
- КОЛИ `contact(topdee, box)` → ЯКЩО `free(cell_behind)` → ТО `push` (?) — рецензія каже «pick up and slide boxes».
- У Toodee-режимі ящик — опора: `supported(toodee)` істинне над ящиком.
- КОЛИ `contact(toodee, key)` → ТО `pickup`, `custom: «відкрити замкнений прохід»`.
- КОЛИ `contact(player, hazard|enemy)` → ТО `lose` → `restart` кімнати (?).
- КОЛИ `custom: «обидва персонажі в порталі»` → ТО `win`, `next_level`.
- КОЛИ `win` → ЯКЩО `custom: «виконано умову сонечка: час / к-сть перемикань / без убивств»` → ТО `give(ladybug)`.
- КОЛИ `counter(ladybugs, >=, n)` → ТО `unlock(bonus_levels)`.
- Перемога: обидва в порталі · Поразка: смерть одного → рестарт рівня (?) · Рахунку нема; є челенджі на час і на кількість перемикань.

## Керування і ввід
- Рух стрілками/стіком; стрибок (Toodee); дія «підняти/поставити» (Topdee); одна кнопка «перемкнути».
- Локальний кооп на 2: на одному екрані або спліт-скрін; як ділиться перемикання між гравцями — (?).
- Геймпад і клавіатура (?).

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: грати, кооп, налаштування (?).
- `map-window` / `level-select` — набори рівнів зі світами й босом у кінці кожного (?).
- `game-screen` — кімната на весь екран; HUD — індикатор активного персонажа (`mode-indicator`), сонечка рівня (?).
- `settings-window` / `difficulty-select` — налаштування складності, що «змінюють деякі правила гри» для тих, хто застряг.
- `pause-menu` — рестарт, вихід на карту (?).
- `end-screen` — рівень пройдено, отримані сонечка (?).

## Фічі поза полем
- `difficulty-presets` / `assist-mode` — складність змінює правила гри (Steam).
- `mode-coop` (локальний, спліт або спільний екран), Remote Play Together.
- `collectibles` (сонечка 4 видів, одне секретне після фіналу) → `unlockables`: найважчі бонус-рівні.
- `achievements`, `cloud-save`, `localization` (11 мов).
- `levels-sequential` + боси наприкінці наборів; секрети.

## Варіації й родичі
- Родичі в корпусі: `baba-is-you` (правила як обʼєкти), `snakebird` (платформер-пазл з гравітацією), Fez (поворот перспективи), Gravity flip-ігри; Lost Vikings / Kwirk (`party-switch`).
- Розробник — dietzribi (Toodee and Topdee виріс з гейм-джему (?)).
- **Осі варіацій:** перемикання — персонажа (Lost Vikings) / персонажа + правил світу (Toodee and Topdee) / самого світу (VVVVVV — гравітація, Fez — вісь); неактивний — заморожений / діє за інерцією; мета — один вихід / усі на виході.

## Цікавинки для курсу
- Один рівень — два набори правил руху (платформер з гравітацією vs 4-напрямки без неї) над тим самим масивом клітин — 🥈 (стратегія/режим як обʼєкт).
- Заморожування неактивного персонажа: один `update` для активного, інший пропускається — 📎.
- Ящик, що міняє роль (у top-down — вантаж, у side-view — платформа) — 🥉.
- Челенджі рівня (час, ліміт перемикань, без убивств) як окремі предикати над логом гри — 📎.
- Двійник-мімік, що повторює ввід гравця — 🥉.
- Розвʼязувач (BFS з перемиканням як окремою дією) — 🥇 через real-time платформну частину.

## Мапа на каталог
- Є: `party-switch` ↔ перемикання персонажів; `move-by-input` + `gravity-fall` ↔ Toodee; `move-4dir` + `push-object` ↔ Topdee; `key-and-door` ↔ ключі; `touch-death` + `environment-death` ↔ вороги, шипи; `reach-exit` ↔ портал; `restart-level`; `sequential-levels` + `level-unlock` + `world-map` ↔ набори рівнів; `difficulty-levels` ↔ складність; `time-bonus` ↔ сонечко на час; `mode-indicator` ↔ хто активний.
- **Нема** → пропозиції карток:
  - `+perspective-switch` «Перемикання жанру/проєкції кімнати» · entities/move · 🥈.
  - `+freeze-inactive` «Неактивний персонаж заморожений» · entities/state · 🌱.
  - `+lift-and-carry` «Підняти й перенести обʼєкт» · entities/interact · 📎.
  - `+all-must-exit` (Kwirk) — усі аватари мають бути на виході.
  - `+mimic-entity` «Сутність повторює ввід гравця» · entities/move · 🥉.
  - `+optional-challenges` «Додаткові умови рівня (час, ліміт дій, пацифізм)» · game-logic/score · 📎.
  - `+assist-rule-changes` «Складність, що міняє правила» · game-logic/difficulty · 📎.
  - `+local-coop` «Двоє на одному екрані/спліті» · game-logic/opponent · 🥉.

## Пропозиції до словників
- `+effect:toggle_perspective` — перемкнути набір правил кімнати разом з активним персонажем.
- `+axis:gravity-per-mode` — нове значення осі `gravity`: `per-mode` (гравітація лише в одному з режимів).
- `+card:perspective-switch`, `+card:freeze-inactive`, `+card:mimic-entity` — див. «Мапа на каталог».
- `+feature:optional-challenges` — необовʼязкові умови рівня з нагородою (сонечка, черепи Felix the Reaper).
- `+ui:switch-counter` — лічильник перемикань для челенджу (?) чи він видимий.

## Джерела
- ⭐ [Steam: Toodee and Topdee](https://store.steampowered.com/app/1303950/Toodee_and_Topdee/) — гібрид платформера й top-down пазла, перемикання, «гра підлаштовується під правила поточного жанру», кооп (спільний/спліт-екран), боси, складність змінює правила, секрети, dietzribi, 04.08.2021.
- [Geeky Hobbies: рецензія PS5](https://www.geekyhobbies.com/toodee-and-topdee-playstation-5-indie-video-game-review/) — перемикання заморожує одного, Topdee без гравітації носить і посуває ящики, Toodee збирає ключі, обидва до порталу, боси, пізні механіки (портали, вороги, мімік), сонечка 4 видів.
- [Nintendo eShop](https://www.nintendo.com/us/store/products/toodee-and-topdee-switch/) — Switch 14.04.2022, локальний кооп.
- YouTube: [пошук «Toodee and Topdee gameplay»](https://www.youtube.com/results?search_query=Toodee+and+Topdee+gameplay).

## Непевне
- (?) Як саме Topdee діє з ящиком: піднімає над головою і кидає/ставить чи лише посуває; що стається з ящиком у Toodee-режимі (падає чи висить).
- (?) Чи тверді блоки — стіни в top-down, а «порожнеча» збоку — підлога згори; чи є ями, у які падає Topdee.
- (?) Поведінка ворогів (свині, що бігають (?)), чи можна їх убити і чим.
- (?) Смерть = рестарт кімнати; наявність undo — не бачив.
- (?) Кількість рівнів і світів; правила перемикання в коопі; пункти меню.
- (?) Сім'я: черга відносить гру до межових → `grid-platformer`; лишив у `thinky`, бо ядро — подвійні правила однієї кімнати, а платформна частина — у `also`.
