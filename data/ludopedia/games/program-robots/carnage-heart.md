---
title: Carnage Heart
slug: carnage-heart
aka: [カルネージハート, Carnage Heart EXA, Carnage Heart Portable]
family: program-robots
also: [tactics]
klass: figure
axes:
  field: hex
  time: programmed
  opponent: ai
  info: partial
  random: runtime
  goal: territory
year: 1995
platforms: [PS1, PSP, PS3]
links:
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Carnage_Heart", best: true, note: "Artdink 1995: OKE, корпуси й деталі, плата чипів-блок-схема, бази й лінії збирання, сиквели"}
  - {kind: other, url: "https://docs.google.com/document/d/1rOIMUhlfBcAM_xldo1Li8GDSNo6c86mq3FrdPgFMFys/export?format=txt", note: "фан-FAQ оригіналу: усі групи чипів, червона/зелена стрілки, розміри плат, бій 150 с, паливо/набої/нагрів, гекс-мапа"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=carnage+heart+ps1+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [command-program, sensor-predicates, step-execution, code-editor-window, ai-opponent, hp-damage, projectile-shot, line-of-sight-attack, shoot-cooldown, time-out, round-currency, shop-window, map-window, hot-seat, match-setup, save-game, +flowchart-chip-grid, +board-wraparound-flow, +radar-sweep-sensor, +team-radio-channels, +counter-variables, +random-branch-chip, +hardware-budget-design, +heat-overheat, +fuel-ammo-supply, +hex-strategy-layer, +base-production-lines, +tech-unlock-by-turn, +auto-battle-programmed-units]
proposes: ["+window:chip-board-editor", "+window:hardware-design", "+window:strategy-map", "+window:battle-view", "+ui:chip-arrows", "+ui:heat-gauge", "+cond:radar(kind, angle, width, range)", "+cond:radio(channel, color)", "+effect:radio_send(channel, color)", "+effect:var_op(var, op, n)", "+trigger:board_exit", "+feature:vs-mode-saved-units"]
author: opus
date: 2026-11-09
---

# Carnage Heart — проєктуй меха й програмуй його плату чипів-блок-схему; у бою він воює сам

## Суть
Покрокова стратегія на гекс-мапі, де бої вирішують не гравці, а програми. Гравець проєктує бойового меха (OKE — Overkill Engine): корпус, зброю, двигун, процесор, броню; потім розкладає на квадратній **платі чипів** блок-схему поведінки — рух, стрільба, радари-умови, змінні, радіоканали команди. Керування OKE в бою нема зовсім: коли ворожий загін заходить у гекс, бій 150 с вирішують лише програми. Мета кампанії — захопити всі ворожі бази.

## Поле і час
- **Стратегічна мапа** — гексова сітка з базами; загін (до 3 OKE) ходить на 1 гекс за хід.
- Хід = фаза стратегії (дизайн, покупки, виробництво, накази загонам) → фаза дії (рух, бої, захоплення); гравець керує лише першою.
- **Бій** — неперервний 3D-простір (не сітка), 150 с у кампанії; обидва боки живі наприкінці → нічия.
- **Плата CPU** — квадратна сітка: 100nc — 10×10, з них 8×8 редаговані, 256nc — 14×14; зовнішнє кільце — лише шлях повернення.
- Час програми: швидкість процесора — мс на чип (повільний 24 мс, середній 12, швидкий 8).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| OKE (мех) | piece | корпус (двоногий / танк / багатоногий / літаючий), зброя, допзброя, двигун, CPU, бак, броня, опції | у бою виконує програму плати; керування нема |
| Загін | piece | до 3 OKE, наказ (оборона / захоплення / патруль / рух) | ходить по гексах; бій при зустрічі з ворожим загоном |
| База | zone | власник, лінії збирання (2 відкриті, 3–6 всього, рівень до 9), запас палива | будує OKE; заправляє; захоплюється |
| Чип дії | tile | параметри (напрям, кількість пострілів 1–5) | рух, поворот, бокові кроки, висота, стрибки, удар, постріл, самознищення, глушилка |
| Чип радара | tile | вид цілі, центр-кут, ширина, дальність 5–300 м | умова: чи є ворог / союзник / снаряд / ракета / перешкода / міна у секторі |
| Чип стану | tile | ресурс, поріг | умова: набої / паливо / шкода / температура / живі союзники / таймер |
| Спецчип | tile | — | Neutral, Stop, Wait, Random (з шансом) |
| Чип радіо | tile | канал 1–5, колір | записати/перевірити колір каналу — спільний для команди |
| Чип лічильника | tile | змінна A–E | +, −, ×, ÷, присвоєння, порівняння (1–100); на старті бою 0 |
| Снаряд / ракета / міна | projectile | — | шкодить OKE; радари їх бачать |
| Перешкода | static | — | у бою заважає руху |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `phase_start(battle)` → ТО `custom: «керування на лівому верхньому чипі плати»`, змінні A–E = 0.
- КОЛИ `exec(chip)` → ТО `custom: «наступний чип — за зеленою стрілкою»`.
- КОЛИ `exec(condition_chip)` → ЯКЩО умова істинна → ТО `custom: «перейти за червоною стрілкою»`; інакше — за зеленою.
- КОЛИ `custom: «потік вийшов за край плати»` → ТО `custom: «повернення на лівий верхній чип»` (програма — нескінченний цикл).
- КОЛИ `exec(radar kind)` → ЯКЩО `custom: «у секторі (кут, ширина, дальність) є kind»` → ТО `custom: «істина»`; лінія видимості не перевіряється.
- КОЛИ `exec(status res)` → ЯКЩО `counter(res, op, n)` → ТО `custom: «істина»`.
- КОЛИ `exec(random p)` → ЯКЩО `prob(p)` → ТО `custom: «червона стрілка»`.
- КОЛИ `exec(radio ch, color)` → ТО `custom: «канал ch команди = color»` — так OKE домовляються.
- КОЛИ `exec(counter A op n)` → ТО `counter(A, op n)`.
- КОЛИ `exec(fire_main)` → ЯКЩО `has(oke, ammo)` → ТО `spawn(projectile)`, `counter(heat, +n)`.
- КОЛИ `counter(heat, >, red_zone)` → ТО `damage(oke)` (перегрів; лазери гріються найбільше).
- КОЛИ `counter(fuel, <=, 0)` → ТО `custom: «OKE не рухається, але стріляє»`; літаючий — `fall`, `explode(oke)`.
- КОЛИ `contact(projectile, oke)` → ТО `damage(oke)`; `hp_zero(oke)` → `disappear_a`.
- КОЛИ `exec(self_destruct)` → ТО `explode(area)`.
- КОЛИ `timer(150 s)` → ЯКЩО `custom: «живі обидва боки»` → ТО `draw`.
- КОЛИ `enter(enemy_team, hex_with_team)` → ТО `custom: «почати бій програм»`.
- КОЛИ `enter(team, enemy_base)` → ЯКЩО `custom: «оборонців нема»` → ТО `set_side(base, player)`.
- КОЛИ `turn_end` → ТО `custom: «поповнення набоїв: 1 AU = повний загін»`, `custom: «база переганяє ~500 л палива»`.
- КОЛИ `turn_end` → ЯКЩО `custom: «гравець тримає всі бази»` → ТО `win`.
- КОЛИ `custom: «настав глобальний номер ходу»` → ТО `unlock(hardware)` у 6 постачальників.
- Перемога: усі бази наприкінці ходу · Поразка: втрата всіх баз (?) · Рахунок: —; гроші, процесні бали ліній.

## Керування і ввід
- Редактор плати: курсор по клітинах, вибір чипа з груп (дія / радар / стан / спец / памʼять), налаштування параметрів слайдерами; L2 + ←/→ — напрям зеленої стрілки, окремо — червоної (?).
- Редактор заліза: корпус і деталі з урахуванням маси й потужності двигуна; складніший дизайн — довше виробництво й кращі лінії.
- Стратегія: накази загонам на гекс-мапі; бій лише спостерігається.
- PS1-кнопки: Трикутник / Коло / X / Квадрат, L1 / R2.

## Вікна, меню, HUD
- `main-menu` → кампанія / `match-setup` (VS-режим) / завантаження (`save-slots`).
- `strategy-map`: гекси, бази, загони, кнопки фаз; `turn-counter`, гроші.
- `hardware-design` (`custom-window`): корпус, деталі, маса/потужність, вартість.
- `chip-board-editor` (`code-editor`): плата N×N, палітра чипів, `chip-arrows` (зелена/червона), параметри чипа.
- `shop-window` — переговори з 6 постачальниками: купівля, дослідження, апгрейди; розвідка ворожих покупок.
- `battle-view` (`game-screen`): 3D-бій, `hp-bar`, `heat-gauge`, паливо, набої, `timer-countdown` 150 с.
- `end-screen` бою і мапи.

## Фічі поза полем
- VS-режим — бій двох збережених дизайнів (довші бої) (`vs-mode-saved-units`).
- Збереження на картку памʼяті; кампанія з картами різного розміру й складності.
- Прогресія техніки за глобальним ходом: швидке проходження = гірше залізо.
- Гроші кожні 15 ходів і за мапу.

## Варіації й родичі
- Серія: Carnage Heart EZ, Zeus Carnage Heart Second, Zeus II (PSN 2009), Carnage Heart Portable, Carnage Heart EXA (PSP, NA 2013).
- [Kara](kara.md) — автомат стан × сенсори; тут — блок-схема на сітці з поверненням; [Befunge](befunge.md) — програма-сітка зі стрілками; [Gladiabots](gladiabots.md) — дерево умов на команду; [RoboRally](roborally.md), [Bot Arenas](bot-arenas.md) — програмовані бої.
- Осі варіацій: **форма програми** (список / блок-схема на сітці / дерево пріоритетів / автомат); **сенсори** (сектор радара / клітина попереду / глобальний стан); **координація** (нема / радіоканали / спільні змінні); **рамки** (розмір плати = CPU, швидкість чипа).

## Цікавинки для курсу
- Інтерпретатор блок-схеми на сітці: зелена/червона стрілки, вихід за край → старт — 🥈.
- Радар-сектор (центр-кут, ширина, дальність) як умова — 🥉.
- Радіоканали з кольорами для координації трьох юнітів — 🥉.
- Бюджет «потужність двигуна / маса / тип корпусу» в редакторі юніта — 🥉.
- Гекс-мапа загонів + автобій програм між ними — 🥇.
- Нагрів зброї з червоною зоною й шкодою — 📎.

## Мапа на каталог
- Є: `command-program`, `sensor-predicates` ↔ радари/стани; `step-execution` ↔ чип за чипом зі швидкістю CPU; `code-editor-window` ↔ плата; `ai-opponent`; `hp-damage`; `projectile-shot`, `line-of-sight-attack`, `shoot-cooldown`; `time-out` ↔ 150 с; `round-currency`, `shop-window`; `map-window` ↔ стратегічна мапа; `hot-seat`/`match-setup` ↔ VS (?); `save-game`.
- **Нема** → пропозиції карток:
  - `+flowchart-chip-grid` «Програма — блок-схема чипів на сітці з двома стрілками» · game-logic/program · 🥈.
  - `+board-wraparound-flow` «Вихід за край плати → на старт» · game-logic/program · 🌱.
  - `+radar-sweep-sensor` «Сенсор-сектор з кутом, шириною й дальністю» · game-logic/program · 🥉.
  - `+team-radio-channels` «Спільні канали-кольори команди» · game-logic/program · 🥉.
  - `+counter-variables` «Змінні A–E з арифметикою в програмі юніта» · game-logic/program · 📎.
  - `+random-branch-chip` «Випадкове розгалуження з шансом» · game-logic/program · 🌱.
  - `+hardware-budget-design` «Конструктор юніта з балансом маси й потужності» · entities/state · 🥈.
  - `+heat-overheat` «Нагрів і шкода від перегріву» · entities/state · 📎.
  - `+fuel-ammo-supply` «Паливо й набої, поповнення на базі» · game-logic/economy · 🥉.
  - `+hex-strategy-layer` «Стратегічна гекс-мапа над боями» · levels/progression · 🥈.
  - `+base-production-lines` «Бази з лініями виробництва» · game-logic/economy · 🥉.
  - `+tech-unlock-by-turn` «Техніка відкривається за номером ходу» · levels/progression · 📎.
  - `+auto-battle-programmed-units` «Бій без керування — лише програми» · game-logic/opponent · 🥈.

## Пропозиції до словників
- `+window:chip-board-editor` — редактор плати-сітки з чипами й стрілками (різновид `code-editor`).
- `+window:hardware-design` — конструктор юніта з деталей.
- `+window:strategy-map` — стратегічна мапа над боями.
- `+window:battle-view` — спостереження автобою.
- `+ui:chip-arrows` — стрілки переходу «так/ні» на чипах.
- `+ui:heat-gauge` — шкала нагріву.
- `+cond:radar(kind, angle, width, range)` — сенсор-сектор.
- `+cond:radio(channel, color)` / `+effect:radio_send(channel, color)` — канали команди.
- `+effect:var_op(var, op, n)` — арифметика над змінною програми.
- `+trigger:board_exit` — потік вийшов за межу плати.
- `+feature:vs-mode-saved-units` — бій двох збережених дизайнів гравців.

## Джерела
- ⭐ [Wikipedia: Carnage Heart](https://en.wikipedia.org/wiki/Carnage_Heart) — OKE, 4 корпуси × 3 дизайни, двигун/маса, плата за розміром CPU, старт зліва вгорі й повернення, групи чипів, радіоканали, бази й лінії, загони до 3, дати й сиквели.
- [Фан-FAQ (Google Docs, txt)](https://docs.google.com/document/d/1rOIMUhlfBcAM_xldo1Li8GDSNo6c86mq3FrdPgFMFys/export?format=txt) — червона = так, зелена = ні/далі; радари 5–300 м без лінії видимості; стани; радіо 5 каналів; змінні A–E; плати 100nc/256nc; 24/12/8 мс на чип; бій 150 с; AU; нагрів; гекс-мапа; лінії; паливо 500 л; техніка за ходом.

## Непевне
- (?) Окреме керування червоною стрілкою в редакторі; повний перелік чипів (FAQ прочитано не до кінця, ~10 % тексту).
- (?) Стартові гроші: FAQ сам собі суперечить (50–300 тис. проти 10–30 тис.).
- (?) Умова поразки кампанії й чи VS-режим — hotseat із двома картками памʼяті.
- (?) Наскільки радари «бачать» крізь перешкоди в EXA/Portable — опис стосується оригіналу PS1.
- Поле `field: hex` — стратегічна мапа; бій — неперервний 3D, програма — квадратна сітка чипів.
