---
title: We Are Gum
slug: we-are-gum
aka: []
family: push-slide
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2026
platforms: [PC (Windows — Steam, демо), Windows (прототип на itch, 2025)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/4105470/", best: true, note: "реліз 01.09.2026: трейлер, безкоштовне демо, опис механік, 19 досягнень"}
  - {kind: itch, url: "https://themono.itch.io/we-are-gum", note: "прототип команди Wethmon (2025) і девлог"}
  - {kind: other, url: "https://ladiesgamers.com/we-are-gum-review/", note: "огляд: портал-ціль, багнюка, H — підказка, Z / R, світ-мапа"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=we+are+gum+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 35
mechanics: [move-4dir, keyboard-controls, push-object, reach-exit, world-map, level-unlock, undo-unlimited, restart-level, save-multi-slot, +sync-avatars, +sticky-avatar, +sticky-floor, +hint-reveal, +split-boards-one-input]
proposes: ["+card:sticky-avatar", "+axis:actors"]
author: opus
date: 2026-11-19
---

# We Are Gum — жуйки-прибульці ходять усі разом і липнуть до всього: зміни формацію й доведи їх до порталу

## Суть
Кілька жуйок-прибульців на острівцях сітки рухаються одночасно від одного вводу («Every Gum moves at the same time, whether you're ready or not!»). Мета — змінити початкову формацію так, щоб жуйки дійшли до порталу, що відправить їх додому.

Жуйки липнуть до стін, блоків і кутів і застрягають у багнюці. Камені штовхаються, як у Sokoban, але, підійшовши впритул, жуйка може приклеїтися до каменя.

Проєкт студентів (команда Wethmon, DDCT, Bangmod, Таїланд) з Global Game Jam 2025 → Steam-реліз 01.09.2026 (Curious Nessie Club, Unity 6): 60+ рівнів, світ-мапа, вбудовані підказки; Best Student Game BIDC 2025.

## Поле і час
- Квадратна сітка, вид згори; рівень — один чи кілька острівців серед води, буває по жуйці на кожному острівці, і всі рухаються разом.
- Хід = один крок усіх жуйок; без таймінгу й одночасних натискань (Steam: «no time-critical inputs»).
- Шари: вода / острови → багнюка → стіни, камені → жуйки; портал-вихід.
- Розміри полів — (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Жуйка | player | кілька на рівні | крок 4 боки разом з усіма; липне до стін, блоків, кутів; штовхає камінь |
| Стіна | static | — | непрохідна; жуйка, що торкнулась, прилипає (?) |
| Камінь (блок) | object | важкий | штовхається на 1; жуйка впритул може до нього приклеїтися |
| Багнюка | terrain | — | жуйка в ній застрягає |
| Портал | zone | — | відправляє жуйок додому |
| Вода | terrain | — | розділяє острівці (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ТО `move(gum, dir)` для кожної жуйки одночасно; жуйка, якій щось заважає, лишається (?), решта йде — так змінюється формація.
- КОЛИ `contact(gum, wall)` → ТО `attach(gum, wall)`: жуйка прилипає до стіни, блоку чи кута; як і коли вона відлипає — (?).
- КОЛИ `contact(gum, stone)` → ЯКЩО `free(cell_behind)` → ТО `push` («shove stones like classic Sokoban»).
- КОЛИ `custom: «жуйка впритул до каменя»` → ТО `attach(gum, stone)` («don't push too hard... you might just glue yourself to them»); чи тягне жуйка приклеєний камінь, не перевірено (?).
- КОЛИ `enter(gum, mud)` → ТО `set_state(gum, stuck)`.
- КОЛИ `reach(gum, portal)` → ТО `custom: «жуйка йде додому»`; рівень пройдено, коли дійшли всі (?).
- КОЛИ `input(hint)` (утримання H) → ТО `custom: «рожеві позначки: куди мають стати жуйки й як іти»`.
- КОЛИ `input(undo)` → ТО `undo`.
- КОЛИ `input(reset)` → ТО `restart`.
- Перемога: жуйки в порталі (?). · Поразки нема: жуйка, що застрягла не там, — привід для undo / рестарту. · Рахунку нема.

## Керування і ввід
- Клавіатура або геймпад, без миші; без одночасних натискань.
- Напрямки — крок усіх жуйок; Z — undo; R — рестарт; утримати H — підказка.
- Розкладка напрямків (стрілки чи WASD) — (?).

## Вікна, меню, HUD
- `map-window`: світ-мапа, де ходиш і обираєш наступний рівень (оглядачці нагадало Mario Bros 3); нові області відкриваються з прогресом; рівні позначено кольором — Tutorial / Normal / EX (патч 1.0.0.1).
- `save-slots`: меню слотів збереження з видаленням (патч 1.0.0.8).
- `game-screen`: рівень; `hint-marker` — рожеві позначки, поки тримаєш H.
- Меню TAB і ESC (згадані в патчі 1.0.0.1), налаштування гучності (Steam).
- Сюжетні сцени між частинами гри (огляд: «a few scenes here and there»).
- Переходи: світ-мапа → рівень → (портал) → світ-мапа.

## Фічі поза полем
- `undo` без ліміту й `restart-level`; `hint` утриманням H (натяк, не повний розвʼязок).
- `world-map` з відкриттям областей; рівні трьох типів: навчальні, звичайні, EX.
- `save-slots` + Steam Cloud; 19 досягнень («GUM Doesn't Like Mud», «Leave No Wall Unchecked», «Ichthyologist»…); «Adjustable Difficulty» у категоріях Steam (?).
- Гра на 5–6 годин; повна підтримка геймпада.

## Варіації й родичі
- [Pluricubus](pluricubus.md): кілька аватарів одним вводом.
- [Sokobond](../thinky/sokobond.md): злипання при дотику (`stick-together`); тут липнуть до стін і каменів.
- [Sokoban](sokoban.md): штовхання каменів.
- Осі варіацій:
  - **хто рухається**: один аватар / усі разом одним вводом (тут);
  - **прилипання**: нема / до сусіднього обʼєкта, групою (Sokobond) / до стін, кутів і каменів (тут);
  - **як змінити формацію**: стіни зупиняють частину групи / липкі поверхні тримають (тут) / ями забирають.

## Цікавинки для курсу
- Один ввід → кілька аватарів, кожен перевіряє свій шлях окремо — 📎.
- Прилипання як стан, що змінює подальший рух; студентам — сформулювати правила самим і описати їх таблицею — 🥉.
- Підказка-оверлей «куди мають стати фігури» — 🌱.
- Світ-мапа з рівнями трьох типів (навчальні / звичайні / EX) — 🌱.

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ крок; `push-object` ↔ камені; `reach-exit` ↔ портал; `world-map` + `level-unlock` ↔ світ-мапа з областями; `undo-unlimited` + `restart-level` ↔ Z і R; `save-multi-slot` ↔ слоти збереження.
- **Нема** → пропозиції карток:
  - `+sync-avatars` (уже пропонована): усі жуйки одним вводом.
  - `+sticky-avatar` «Аватар прилипає до стін, блоків і кутів» · entities/interact · 🥉 · слоти {to: walls|blocks|corners, release: ?}.
  - `+sticky-floor` (уже пропонована): багнюка.
  - `+hint-reveal` (уже пропонована): рожеві позначки за утриманням H.
  - `+split-boards-one-input` (уже пропонована): жуйки на окремих острівцях, один ввід.

## Пропозиції до словників
- `+card:sticky-avatar` — див. «Мапу на каталог».
- `+axis:actors` — `swarm`: кілька однакових аватарів одним вводом (тут, What Gophers Go For).

## Джерела
- ⭐ [Steam: We Are Gum](https://store.steampowered.com/app/4105470/) — «All Gums Move Together», «Stick to Literally Everything: Walls, blocks and more blocks», «Push It, Then Stick It», 60+ рівнів, підказки, досягнення; новини — патчі (рівні Tutorial / Normal / EX, слоти збереження).
- [itch.io: We Are Gum](https://themono.itch.io/we-are-gum) — прототип і склад команди; «Stick to Literally Everything: Walls, blocks, corners», «don't get too close... You might just glue yourself to them».
- [LadiesGamers: огляд](https://ladiesgamers.com/we-are-gum-review/) — портал додому, зміна формації, «stuck in walls, corners, mud and also to heavy stones», H / Z / R, світ-мапа, острівці з однією жуйкою.

## Непевне
- (?) Точні правила прилипання: чи жуйка, що торкнулась стіни, більше не рухається, чи відлипає, рухаючись геть; чи тягне вона приклеєний камінь (черга каже «тягнуть камені», джерела — лише «glue yourself to them»).
- (?) Рибки — лише назви досягнень «Ichthyologist» / «Supreme Ichthyologist»; яка це механіка, невідомо.
- (?) Чи всі жуйки мають дійти до порталу; чи вода непрохідна; розміри полів.
- (?) Анімовані комікси між розділами: згадані в одному підсумку пошуку, на сторінці Steam при перевірці не знайдені.
- (?) Рік у черзі — 2025: це рік джему й прототипу на itch; Steam-реліз — 01.09.2026.
