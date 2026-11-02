---
title: "'One Way Heroics (Mystery Chronicle: One Way Heroics)'"
slug: one-way-heroics
family: roguelike
also: []
klass: avatar
axes:
  field: square
  time: turn
  opponent: ai
  info: partial
  random: both
  goal: state
year: 2012
platforms: [PC, PS4, PS Vita]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/266210/One_Way_Heroics/", best: true, note: "оригінал Smoking WOLF / PLAYISM: темрява зліва, кожна дія її наближає, класи, Dimensional Vault, світ за імʼям"}
  - {kind: steam, url: "https://store.steampowered.com/app/352840/One_Way_Heroics_Plus/", note: "розширена версія"}
  - {kind: steam, url: "https://store.steampowered.com/app/409000/Mystery_Chronicle_One_Way_Heroics/", note: "Spike Chunsoft: Shine Raid, 20+ класів, напарники, щоденні світи"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Mystery_Chronicle:_One_Way_Heroics", note: "спін-оф Mystery Dungeon, «екран скролиться з кожним ходом»"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=one+way+heroics+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 60
mechanics: [move-8dir, infinite-field, hp-damage, inventory, inventory-items, inventory-limit, item-pickup, chase-player, random-walk, round-currency, shop-catalog, player-death, score-records, player-camera, keyboard-controls, progress-acceleration, +permadeath, +hunger-clock, +forced-scroll, +death-wall, +seed-by-name, +vault-carryover, +perk-select, +equipment-durability, +recruit-ally, +roaming-boss, +distance-score]
proposes: ["+trigger:scroll", "+trigger:caught_by_edge", "+cond:column(a, op, x)", "+cond:distance(op, n)", "+effect:scroll(n)", "+effect:advance_wall", "+effect:vault_store(item)", "+role:wall-hazard", "+role:boss", "+role:ally", "+ui:distance-counter", "+ui:danger-line", "+window:perk-select", "+window:character-select", "+window:vault-window", "+window:world-name-input", "+feature:seed-input", "+feature:meta-progression", "+feature:permadeath", "+feature:mode-daily", "+axis:camera=forced-scroll"]
author: opus
date: 2026-11-02
---

# One Way Heroics — роглайк з примусовим скролом: світло/темрява зʼїдає лівий край, назад дороги нема

## Суть
Герой іде вправо крізь процедурну смугу світу (поля, ліси, гори, міста, підземелля), б'ється, торгує, наймає напарників і шукає силу, щоб перемогти Короля демонів. Усе це — під **рухомою стіною зліва**: з кожною дією межа світу насувається на одну колонку, і все, що вона накрила, зникає разом із героєм. Тож кожен відступ, бій чи похід у бік коштує «відстані», а мапа — одноразова. Оригінал — фріваре Smoking WOLF (2012 (?)), Steam 2014; Spike Chunsoft переробила її як Mystery Chronicle (2015 JP / 2016 Захід).

## Поле і час
- Квадратна сітка; світ — **нескінченна горизонтальна смуга** обмеженої висоти (?), генерується колонками праворуч (`infinite-field`).
- Камера показує вікно смуги; ліва межа вікна = край поглинання: темрява (оригінал) або «Shine Raid» — світло (Mystery Chronicle).
- Хід = будь-яка дія гравця (крок, удар, використання предмета); після неї край просувається (Steam: «with each movement or action you take, the void creeps ever closer»; WP: «with every turn that passes, the screen will scroll»).
- `info: partial`: видно лише вікно; що праворуч за екраном — невідомо; входи в підземелля/замки — окремі карти (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Герой | player | клас, рівень, HP, стаміна, атака/захист, інвентар з вагою (?) | рух 8 напрямків (?), бій ударом у сусіда |
| Край поглинання (темрява / Shine Raid) | hazard | колонка x | щоходу +1 колонка вправо; клітини лівіше — знищені |
| Король демонів | boss | дуже сильний на початку | зʼявляється й переслідує героя; перемога над ним — ціль |
| Монстри | enemy | рівень росте з відстанню (?) | бродять / переслідують у полі зору |
| Мандрівні герої (NPC) | neutral / ally | клас | можна найняти або вони ворожі (?) |
| Напарник | ally | HP | бʼється поруч; його теж зʼїдає край |
| Торговець / місто | neutral | товар, ціна | купівля й продаж за золото |
| Ліс / гори / вода | terrain | вартість руху / прохідність (?) | гори й вода непрохідні без спорядження (?) |
| Скриня, предмети | pickup / container | — | зброя, броня (з міцністю), їжа, зілля, сувої |
| Вхід у підземелля / замок | static | — | окрема зона; поки ти там, край теж іде (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `turn_end(player)` → ТО `advance_wall`: колонка `x_wall` +1, `scroll(1)` камери.
- КОЛИ `caught_by_edge(a)` (клітина a лівіше краю) → ТО `disappear_a`; для героя → `lose` миттєво.
- КОЛИ `input(move)` → ЯКЩО `free(cell)` → ТО `move(hero)`; крок уліво чи вгору/вниз не дає відстані, але край однаково наступає.
- КОЛИ `scroll` → ТО `custom: «згенерувати нову колонку праворуч»` (місцевість, вороги, NPC, міста).
- КОЛИ `turn_end` → ТО `counter(stamina, −1)` (?); ЯКЩО `count(stamina, ==, 0)` → ТО `hp(hero, −n)` щоходу.
- КОЛИ `input(eat)` → ТО `counter(stamina, +n)`.
- КОЛИ `contact(hero, enemy)` (удар) → ТО `damage(atk − def)` (?), зброя `custom: «міцність −1»`; міцність 0 → предмет ламається (?).
- КОЛИ `hp_zero(enemy)` → ТО `counter(xp, +n)`, `rng(p)` → `spawn(item)`.
- КОЛИ `contact(hero, npc_hero)` → ЯКЩО згода/плата (?) → ТО `make_ally`.
- КОЛИ `distance(>=, n)` (?) → ТО `spawn_at(demon_lord, near hero)`; він переслідує.
- КОЛИ `hp_zero(demon_lord)` → ТО `win`.
- КОЛИ `hp_zero(hero)` або `caught_by_edge(hero)` → ТО `lose`; ТО `custom: «очки героя за відстань/рівень»` → відкриття перків/класів (?).
- КОЛИ `input(vault store item)` → ТО `vault_store(item)` — предмет переходить у наступний забіг (Steam: «Lock away your inventory and save it for your next run!»).
- Перемога: перемогти Короля демонів. Поразка: HP = 0 або край поглинув героя. Рахунок: пройдена відстань + рівень → очки на мета-відкриття (?).

## Керування і ввід
- Клавіатура / геймпад: 8 напрямків, удар — рух у ворога; меню інвентаря; очікування на місці (теж хід — і край наступає).
- Діалоги з NPC (найм, торгівля), вибір у подіях.
- Steam: «freeze time and work out a new strategy» — поза ходом часу нема, можна думати скільки завгодно (`time: turn`).

## Вікна, меню, HUD
- `game-screen` — вікно смуги, лівий край — `danger-line` темряви; HUD: `hp-bar`, стаміна (`hunger-bar`), `distance-counter` (пройдено), рівень, золото, `message-log`.
- `character-select` — клас; `perk-select` — перки забігу за очки (?); `world-name-input` — назва світу як seed (повтор «вимірювання»).
- `vault-window` — Dimensional Vault: покласти/взяти предмет між забігами.
- `inventory-window` (з міцністю спорядження), `shop-window`, `dialogue-window` (найм).
- `end-screen` — підсумок забігу (відстань, причина), `stats-window`/рекорди (?); `main-menu`, `settings-window` (складність).
- Переходи: `main-menu` → `character-select` → `perk-select` → (`world-name-input`) → `game-screen` → `end-screen` → `main-menu`.

## Фічі поза полем
- `permadeath`; `meta-progression` — нові класи й перки, Dimensional Vault (предмет на наступний забіг).
- `seed-input` — світ за імʼям, можна переграти той самий (Steam); `share-code` — поділитись світом (Mystery Chronicle).
- `difficulty-presets` (?) ; `mode-daily` — Daily Campaign Worlds (Mystery Chronicle); `achievements`, `cloud-save`.
- Mystery Chronicle: 20+ класів, напарники, Twitter-публікація результату (`share-result`).

## Варіації й родичі
- One Way Heroics Plus — розширення; Mystery Chronicle — ремейк у стилі Mystery Dungeon (Shiren/Danganronpa-класи).
- Родичі: Crossy Road / Frogger (`infinite-field` з тиском), Downwell, «Temple Run» (примусовий рух), FTL (флот повстанців як фронт, що наздоганяє), Super Mario auto-scroll рівні.
- Осі варіацій: **що рухає фронт** (кожен хід / таймер / лише крок гравця) · **швидкість фронту** (стала / росте) · **напрям** (вправо / вниз / з усіх боків — «зона» в battle royale) · **що фронт робить** (вбиває / шкодить / лише зачиняє дорогу назад).

## Цікавинки для курсу
- Примусовий скрол: стіна смерті +1 колонка за хід, поглинання сутностей лівіше — 📎 (одна змінна `x_wall` змінює всю гру).
- Генерація колонками праворуч і викидання лівих — 🥉 (кільцевий буфер / deque колонок, `infinite-field`).
- Світ за назвою як seed — 🌱 (хеш рядка → `random.seed`), гарний приклад відтворюваності.
- Dimensional Vault: один предмет переживає смерть — 🌱 (мета-збереження поза забігом).
- Бос, що зʼявляється за відстанню й переслідує, поки не готовий — 📎.
- «Чи можна ще встигнути»: оцінка, скільки ходів до краю, у `path-preview` — 🥉.

## Мапа на каталог
- Є: `move-8dir` · `infinite-field` · `hp-damage` · `inventory` + `inventory-items` + `inventory-limit` · `item-pickup` · `chase-player` · `random-walk` · `round-currency` · `shop-catalog` · `player-death` · `score-records` · `player-camera` · `keyboard-controls` · `progress-acceleration` (вороги сильнішають з відстанню (?)).
- **Нема** → пропозиції карток:
  - `+forced-scroll` «Камера/світ зсуваються щоходу» · levels/generation · 📎 · слот {per_turn}.
  - `+death-wall` «Межа поглинання знищує все позаду» · game-logic/lose · 📎.
  - `+seed-by-name` «Світ за текстовою назвою» · levels/generation · 🌱.
  - `+vault-carryover` «Предмет переходить у наступний забіг» · game-logic/save · 🌱.
  - `+perk-select` «Перки на старті забігу» · game-logic/economy · 📎.
  - `+equipment-durability` «Міцність зброї/броні» · entities/state · 📎.
  - `+recruit-ally` «Найняти NPC» · entities/interact · 📎 (як у DotE).
  - `+roaming-boss` «Бос-переслідувач між рівнями» · entities/move · 📎.
  - `+distance-score` «Рахунок = пройдена відстань» · game-logic/score · 🌱.
  - `+permadeath`, `+hunger-clock` — як у Rogue.

## Пропозиції до словників
- `+trigger:scroll` — світ зсунувся на колонку; `+trigger:caught_by_edge` — сутність лівіше краю поглинання.
- `+cond:column(a, op, x)` — положення відносно краю; `+cond:distance(op, n)` — пройдена відстань.
- `+effect:scroll(n)` · `+effect:advance_wall` · `+effect:vault_store(item)`.
- `+role:wall-hazard` — рухома межа-стихія (не `hazard`: не в клітині, а лінія); `+role:boss`, `+role:ally` — вжито.
- `+ui:distance-counter`; `+ui:danger-line` (⏳) — вжито.
- `+window:perk-select` · `+window:vault-window` · `+window:world-name-input` · `+window:character-select` (⏳).
- `+feature:seed-input` (⏳), `+feature:meta-progression`, `+feature:permadeath`, `+feature:mode-daily`.
- `+axis:camera=forced-scroll` — камера не слідує за героєм, а тисне на нього (нова вісь: `follow | static | forced-scroll`).

## Джерела
- ⭐ [Steam: One Way Heroics](https://store.steampowered.com/app/266210/One_Way_Heroics/) — темрява зліва, «кожен рух чи дія» її наближає, Король демонів, класи, Dimensional Vault, світ за назвою, Smoking WOLF / PLAYISM, 28.02.2014.
- [Steam: Mystery Chronicle](https://store.steampowered.com/app/409000/Mystery_Chronicle_One_Way_Heroics/) — Shine Raid, 20+ класів, напарники, щоденні світи, поділитись світом.
- [Steam: One Way Heroics Plus](https://store.steampowered.com/app/352840/One_Way_Heroics_Plus/).
- [Wikipedia: Mystery Chronicle](https://en.wikipedia.org/wiki/Mystery_Chronicle:_One_Way_Heroics) — історія ремейку, скрол з кожним ходом.
- YouTube: пошук «one way heroics gameplay».

## Непевне
- (?) Рік фріваре-оригіналу 2012 — з брифу куратора; Steam-реліз 28.02.2014.
- (?) Висота смуги, 8 напрямків, чи край іде за кожну дію чи лише частину — Steam і WP формулюють різно.
- (?) Стаміна, міцність спорядження, найм NPC-героїв, поява Короля демонів за відстанню, очки за відстань, перки — з памʼяті.
- (?) Чи край рухається, поки герой у підземеллі/місті.
