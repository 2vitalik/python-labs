---
title: Helltaker
slug: helltaker
family: push-slide
also: [thinky]
klass: avatar
axes:
  field: square
  time: turn
  opponent: none
  info: full
  random: none
  goal: state
year: 2020
platforms: [PC (Windows, macOS, Linux), Switch (фан-порт), PS Vita (фан-порт)]
links:
  - {kind: steam, url: "https://store.steampowered.com/app/1289310/Helltaker/", best: true, note: "безкоштовна; проходиться за ~1 год — найшвидший вхід — зіграти"}
  - {kind: wiki, url: "https://en.wikipedia.org/wiki/Helltaker", note: "Sokoban-подібні пазли, ліміт ходів, шипи, ключі, питання після рівня, бос Judgement, Examtaker"}
  - {kind: wiki, url: "https://ru.wikipedia.org/wiki/Helltaker", note: "ліміт ходів, скелети знищуються, неправильна відповідь = смерть і рестарт, пропуск пазла"}
  - {kind: wiki, url: "https://ja.wikipedia.org/wiki/Helltaker", note: "структура глави: пазл + розмова з вибором з двох; 9-та глава — екшн-фаза"}
  - {kind: other, url: "https://github.com/D3fau4/Helltaker-switch", note: "авторизований фан-порт на Switch"}
  - {kind: steam, url: "https://store.steampowered.com/app/1298590/Helltaker_Artbook_Pancake_Recipe/", note: "артбук (підтримка автора)"}
  - {kind: youtube, url: "https://www.youtube.com/results?search_query=helltaker+gameplay", note: "пошук; геймплей"}
stage: v1
coverage: 75
mechanics: [move-4dir, keyboard-controls, push-object, impassable-cells, key-and-door, item-pickup, reach-exit, player-death, no-moves-left, sequential-levels, level-select, +move-limit, +kick-in-place, +kick-destroy, +toggle-spikes, +step-cost-cell, +skip-level, +dialogue-choice, +dodge-phase, +secret-ending-input]
proposes: ["+trigger:input", "+trigger:counter", "+trigger:blocked", "+cond:free", "+cond:has", "+cond:state", "+effect:counter", "+effect:take", "+effect:set_state", "+effect:choose", "+role:hazard", "+role:gate", "+ui:move-counter", "+window:dialogue-window", "+window:chapter-select", "+feature:skip-level", "+card:kick-in-place", "+card:dialogue-choice"]
author: opus
date: 2026-11-02
---

# Helltaker — Sokoban з бюджетом ходів: штовхай камені, копай скелетів, дійди до демониці й не помились у відповіді

## Суть
Герой у костюмі на маленькому полі мусить дійти до демониці, вклавшись у **фіксовану кількість ходів**; лічильник видно великими цифрами збоку. Він не входить у клітину з каменем чи скелетом — він **б'є ногою на місці**: камінь зсувається на 1, скелет зсувається або, якщо далі не можна, розсипається; кожен такий удар коштує хід. Шипи віднімають додатковий хід, ключ відкриває замок-скриню. Після пазла — діалог з питанням на два варіанти: неправильна відповідь — «смерть» і повтор пазла. Елегантність: один лічильник ходів одночасно є «HP», таймером і мірою оптимальності.

## Поле і час
- Невелика квадратна сітка (кімната пекла, приблизно 7–9 клітин у бік (?)), статична камера, видно все.
- Шари: підлога (звичайна / шипи постійні / шипи, що перемикаються) + обʼєкти (герой, камінь, скелет, ключ, скриня-замок, демониця-ціль).
- Хід = одна дія героя (крок або удар); після кожної дії перемикаються змінні шипи. Таймера реального часу нема.
- Глава 9 (бос Judgement): поле стає ареною з атаками ланцюгами по рядах/стовпцях — real-time-подібні ухиляння (?) у ритм музики (?).

## Сутності
| Сутність | Роль | Параметри | Поведінка |
|---|---|---|---|
| Helltaker | player | — | рух 4 напрямки; у камінь/скелета не входить, а б'є, лишаючись на місці |
| Лічильник ходів | — (стан рівня) | N на старті | −1 за кожну дію; −1 додатково на шипах |
| Стіна / скеля | static | — | непрохідна |
| Камінь (валун) | object | — | удар → зсув на 1, якщо за ним вільно; інакше стоїть (хід усе одно витрачено) |
| Скелет | enemy | — | пасивний; удар → зсув на 1; якщо за ним не можна — знищується |
| Шипи постійні | hazard | — | стати/стояти → додатковий −1 хід |
| Шипи змінні | hazard | фаза up/down | перемикаються щоходу; підняті — як постійні; скелет на піднятих гине (?) |
| Ключ | pickup | — | береться кроком |
| Скриня-замок (lockbox) | gate | — | непрохідна без ключа; з ключем — відкривається й зникає |
| Демониця | static | — | ціль: стати поруч → кінець пазла, діалог |
| Фрагмент скрижалі (у 3 рівнях) | pickup | — | потрібні для таємної кінцівки Abysstaker |
| Judgement (глава 9) | boss | фази | атаки ланцюгами по екрану; треба вижити й уразити цілі (?) |

## Правила (КОЛИ → ЯКЩО → ТО)
- КОЛИ `input(dir)` → ЯКЩО `free(next_cell)` → ТО `move(hero, dir)`, `counter(moves, -1)`.
- КОЛИ `input(dir)` → ЯКЩО `cell(next_cell, wall)` → ТО `block` (хід не витрачається (?)).
- КОЛИ `contact(hero, rock)` → ТО `counter(moves, -1)`; ЯКЩО `free(cell_behind)` → ТО `push`; герой **лишається** на місці (`custom: «удар без кроку»`).
- КОЛИ `contact(hero, skeleton)` → ТО `counter(moves, -1)`; ЯКЩО `free(cell_behind)` → ТО `push`; інакше `disappear_b` (скелет розсипається об стіну, камінь, іншого скелета, замок).
- КОЛИ `enter(hero, spikes)` або `custom: «хід закінчено на піднятих шипах»` → ТО `counter(moves, -1)` додатково.
- КОЛИ `turn_end(hero)` → ТО `set_state(toggle_spikes, flip)`; ЯКЩО `occupied(toggle_spikes, skeleton)` і шипи піднялись → ТО `disappear_b` (?).
- КОЛИ `contact(hero, key)` → ТО `pickup`.
- КОЛИ `contact(hero, lockbox)` → ЯКЩО `has(hero, key)` → ТО `disappear_b`, `take(hero, key)`; інакше `block`.
- КОЛИ `adjacent(hero, demon)` → ТО `window(dialogue-window)` — пазл розвʼязано.
- КОЛИ `counter(moves, <, 0)` або `custom: «ходи скінчились, а демониця не досягнута»` → ТО `lose`, `restart` (?) точна межа: 0 чи −1.
- Діалог: КОЛИ `choose(answer_A, answer_B)` → ЯКЩО `custom: «відповідь відповідає характеру демониці»` → ТО `next_level` (демониця приєднується); інакше `lose` (комікс-«bad end») → `restart` пазла. У двох главах підходять обидві відповіді.
- КОЛИ `input(skip)` (меню) → ТО `custom: «пропустити пазл, одразу діалог»` — але таємна кінцівка (скрижалі) тоді недоступна.
- Епілог: КОЛИ `custom: «зібрано 3 скрижалі»` → ТО `custom: «введення послідовності ходів на килимі»` → портал → кінцівка Abysstaker.
- Перемога: дійти до демониці в межах ходів + правильна відповідь; гра — пройти 9 глав. · Поразка: ходи вичерпано / неправильна відповідь / атака боса. · Рахунок: нема, лише «чи вклався» (ліміт = оптимум або близько).

## Керування і ввід
- Стрілки / WASD — крок або удар у напрямку.
- R — рестарт пазла (?); Esc — меню: пропустити пазл, рестарт, вибір глави (?), вихід.
- Діалог: вибір з двох відповідей (стрілки + Enter / миша (?)).
- Глава 9: ті самі стрілки, але дії під тиском атак.

## Вікна, меню, HUD
- `splash-screen` → `main-menu`: Нова гра · Вибір глави (?) · Вихід.
- `game-screen`: поле; HUD — великий `move-counter` (лишилось ходів) з боків, номер глави римськими цифрами (?), підказка клавіш рестарту/меню.
- `dialogue-window`: портрет демониці, текст, дві відповіді; правильна → наступна глава; неправильна → «bad end» (`end-screen` поразки з коміксом) → рестарт.
- `pause-menu`: Skip puzzle · Restart · Chapter select (?) · Music · Exit.
- `end-screen` фінальний (кінцівка, кредити) і окремо — таємна кінцівка Abysstaker.
- Переходи: main-menu → game-screen глави N → (дійшов) dialogue-window → (вірно) game-screen глави N+1; (невірно або ходи скінчились) → смерть → game-screen глави N з початку.

## Фічі поза полем
- `levels-sequential` (9 глав + Examtaker, бонусна глава 2021 з важчими рівнями).
- `skip-level` з ціною: втрачається таємна кінцівка — пропуск як фіча, а не «чит».
- `restart-level`; **нема undo** — бюджет ходів малий, рестарт дешевий.
- Таємна кінцівка за колекційні предмети + введення послідовності на полі — `collectibles`.
- Безкоштовна; артбук окремо (підтримка автора); авторизовані фан-порти.

## Варіації й родичі
- Осі варіацій штовхання (для push-slide):
  - **чи входить гравець у клітину при поштовху**: так (Sokoban) / ні — удар на місці (Helltaker);
  - **що робить обʼєкт, коли йому нема куди**: нічого (камінь) / знищується (скелет) / знищує інше (Pengo — розчавлює ворога);
  - **ресурс**: необмежено (Sokoban) / бюджет ходів (Helltaker) / таймер (Chip's Challenge);
  - **ціна клітини**: 1 хід / 2 ходи на шипах (зважений граф для BFS).
- Родичі: Sokoban, Baba Is You-хвиля thinky; фанатські «таки» (Examtaker, моди); бюджет ходів — у Rush Hour-подібних «за N ходів», Hitman GO (бонус за ходи).

## Цікавинки для курсу
- Удар на місці (поштовх без кроку) + скелет, що гине, коли нема куди — 🌱: дві гілки в одній функції руху.
- Бюджет ходів із клітинами вагою 2 (шипи) і змінними шипами, що перемикаються щоходу — 📎.
- Розвʼязувач «чи вкладаюсь у N ходів» (BFS по станах: позиція, камені, скелети, ключ, фаза шипів, ходи) — 🥈: стан має парність шипів.
- Діалог після рівня з вибором, де неправильна відповідь = поразка — 🌱 механіка, 📎 з вікном і текстами.
- Пропуск рівня з «ціною» (недоступна таємна кінцівка) — 🌱.
- Фаза-ухиляння боса з атаками по рядах/стовпцях — 🥉 (окремий режим на тому ж полі).

## Мапа на каталог
- Є: `move-4dir` + `keyboard-controls` ↔ стрілки; `push-object` ↔ каміння; `impassable-cells` ↔ стіни; `key-and-door` + `item-pickup` ↔ ключ і скриня; `reach-exit` ↔ дійти до демониці; `player-death` + `no-moves-left` ↔ ходи вичерпано; `sequential-levels` + `level-select` ↔ глави.
- **Нема** → пропозиції карток:
  - `+move-limit` (вже пропонована XOR) · слот {moves} — тут ядро гри; правило трьох наближається.
  - `+kick-in-place` «Поштовх без кроку» · entities/legality · 🌱 — гравець лишається, обʼєкт зсувається.
  - `+kick-destroy` «Обʼєкт гине, якщо нема куди зсунути» · entities/interact · 🌱 — родич Pengo `+crush-by-slide`.
  - `+toggle-spikes` (також Tomb of the Mask) · слот {period: 1 хід}.
  - `+step-cost-cell` «Клітина з ціною ходу» · entities/interact · 📎 · слот {cost} — зважений граф.
  - `+skip-level` (вже пропонована Supaplex) · слот {penalty}.
  - `+dialogue-choice` «Вибір відповіді в діалозі, хибна = поразка» · game-logic/lose · 📎.
  - `+dodge-phase` «Фаза ухиляння від атак боса» · entities/combat · 🥉.
  - `+secret-ending-input` «Таємна послідовність ходів на полі» · game-logic/win · 🌱.

## Пропозиції до словників
- `+trigger:input`; `+trigger:counter` — ходи вичерпано; `+trigger:blocked` — скелету нема куди.
- `+cond:free`, `+cond:has` (ключ), `+cond:state` (шипи підняті).
- `+effect:counter` — бюджет ходів; `+effect:take` — витрата ключа; `+effect:set_state` — фаза шипів; `+effect:choose` — відповідь у діалозі.
- `+role:hazard` — шипи; `+role:gate` — скриня-замок.
- `+ui:move-counter` — тут «лишилось» (спадний), а не «зроблено».
- `+window:dialogue-window` — діалог з вибором як частина ігрового циклу; `+window:chapter-select`.
- `+feature:skip-level`.
- `+card:kick-in-place`, `+card:dialogue-choice`.

## Джерела
- ⭐ [Steam: Helltaker](https://store.steampowered.com/app/1289310/Helltaker/) — безкоштовна гра (~1 год): «kick around skeletons», «solve puzzles as efficiently as possible», пропуск пазлів через меню.
- [Wikipedia: Helltaker](https://en.wikipedia.org/wiki/Helltaker) — каміння й скелети, ліміт ходів, шипи, ключі, питання з поганою кінцівкою або рестартом, бос Judgement з ланцюгами, скрижалі Abysstaker, Examtaker.
- [Wikipedia RU](https://ru.wikipedia.org/wiki/Helltaker) — скелетів знищують, пропуск пазла, кінцівка за фрагменти.
- [Wikipedia JA](https://ja.wikipedia.org/wiki/Helltaker) — глава = пазл + розмова з вибором з двох; у деяких главах обидві відповіді правильні; 9-та глава — екшн, не пропускається.
- [Helltaker-switch](https://github.com/D3fau4/Helltaker-switch) — авторизований фан-порт.
- YouTube: пошук «helltaker gameplay».

## Непевне
- (?) Точна ціна шипів (−1 додатково при вході / при закінченні ходу на них) і чи блок-хід у стіну витрачає хід — з памʼяті.
- (?) Чи гине скелет на змінних шипах, що піднялись під ним — з памʼяті.
- (?) Межа смерті: при 0 ходів чи при спробі ходити з 0 — не перевірено.
- (?) Наявність меню вибору глави і клавіші R — з памʼяті; Steam підтверджує лише пропуск через меню.
- (?) Механіка боса Judgement (ритм, кількість «життів», цілі для ураження) — Wikipedia лише «фазові атаки ланцюгами, bullet hell»; фан-вікі (Fandom) недоступна (402).
- (?) Розмір поля пазла.
